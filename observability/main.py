"""Single-worker learning service with bounded metrics and opt-in fault injection."""
import asyncio
import json
import logging
import os
import re
import time
import uuid

from fastapi import FastAPI, HTTPException, Query, Request
from prometheus_client import CollectorRegistry, Counter, Histogram, generate_latest
from starlette.responses import JSONResponse, Response

LOGGER = logging.getLogger("lab.requests")
REQUEST_ID = re.compile(r"[A-Za-z0-9_-]{1,64}\Z")


def create_app(*, faults_enabled: bool = False) -> FastAPI:
    app = FastAPI(title="Service Observability Lab")
    registry = CollectorRegistry()
    requests = Counter("lab_http_requests_total", "Completed requests (excludes metrics)",
                       ["method", "route", "status"], registry=registry)
    duration = Histogram("lab_http_request_duration_seconds", "Response duration",
                         ["method", "route"],
                         buckets=(.005, .025, .05, .1, .3, .5, 1, 2, 5), registry=registry)
    app.state.registry = registry

    @app.middleware("http")
    async def observe(request: Request, call_next):
        supplied = request.headers.get("X-Request-ID", "")
        request_id = supplied if REQUEST_ID.fullmatch(supplied) else uuid.uuid4().hex
        started = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            # Deliberate lab scope: record failure without logging payloads or secrets.
            response = JSONResponse({"detail": "Internal server error"}, status_code=500)
        elapsed = time.perf_counter() - started
        route_object = request.scope.get("route")
        route = getattr(route_object, "path", "unmatched")
        method = request.method if request.method in {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"} else "OTHER"
        response.headers["X-Request-ID"] = request_id
        if route != "/metrics":
            requests.labels(method, route, str(response.status_code)).inc()
            duration.labels(method, route).observe(elapsed)
            LOGGER.info(json.dumps({"event": "http_request", "request_id": request_id,
                                    "method": method, "route": route,
                                    "status": response.status_code,
                                    "duration_seconds": round(elapsed, 6)}))
        return response

    @app.get("/health")
    async def health():
        return {"status": "ok", "service": "observability-lab"}

    @app.get("/work")
    async def work(delay_ms: int = Query(0, ge=0, le=2000), fail: bool = False):
        if (delay_ms or fail) and not faults_enabled:
            raise HTTPException(403, "Lab fault injection is disabled")
        await asyncio.sleep(delay_ms / 1000)
        if fail:
            raise HTTPException(503, "Controlled lab failure")
        return {"result": "completed", "delay_ms": delay_ms}

    @app.get("/items/{item_id}")
    async def item(item_id: int):
        return {"item_id": item_id}

    @app.get("/metrics", include_in_schema=False)
    async def metrics():
        return Response(generate_latest(registry), media_type="text/plain; version=0.0.4; charset=utf-8")

    return app


app = create_app(faults_enabled=os.getenv("LAB_FAULTS_ENABLED", "false").lower() == "true")
