# Cloud Support Portfolio Labs

Two connected personal projects: an AWS/Linux recovery lab and an instrumented service with Prometheus monitoring. These are learning environments, not production services.

| Project | Evidence | Start here |
| --- | --- | --- |
| AWS Deployment & Service Recovery | Original EC2 deployment observations, health checks, local proxy recovery exercise | This page and [recovery guide](docs/testing.md) |
| Service Observability & Prometheus Monitoring | Request counters, duration histogram, request-ID logs, controlled faults, alert rules and tests | [Monitoring project](observability/README.md) |

The original service remains in `app/`. The monitoring service is separate in `observability/`; it does not change the original health contract.

## What this demonstrates

- Linux server administration and SSH-based deployment
- Docker image builds, container lifecycle management, and restart policies
- Nginx reverse proxying and secure local-only container binding
- Public health checks, incident isolation, service recovery, and reboot validation

## Architecture

```text
Client
  |
  v
EC2 security group - TCP 80
  |
  v
Nginx - TCP 80
  |
  v
Docker container - 127.0.0.1:8000
  |
  v
FastAPI - GET /health
```

## Project structure

```text
app/                         FastAPI application
infra/nginx-reverse-proxy.conf  Nginx reverse-proxy configuration
docs/                        Deployment and operational notes
Dockerfile                   Container build definition
requirements.txt             Python dependencies
```

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Verify the service:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok","service":"aws-linux-support-lab"}
```

## Run with Docker

```bash
docker build -t aws-linux-support-lab .
docker run --rm -p 127.0.0.1:8000:8000 aws-linux-support-lab
```

Then open `http://127.0.0.1:8000/health`.

## Deployment design

The EC2 host runs Nginx on port 80. The FastAPI container is bound to `127.0.0.1:8000`, with Nginx forwarding incoming requests to the application. This keeps the application port off the public network while retaining a standard HTTP entry point.

See [deployment and operational notes](docs/deployment-and-troubleshooting.md) for the validated deployment and recovery scenarios.

## Scope

This repository is a focused cloud-support lab rather than a production platform. Production hardening would include HTTPS, restricted SSH source ranges, monitoring and alerting, infrastructure as code, and a managed container deployment strategy.

## Tests and recovery checks

See [testing guide](docs/testing.md) for automated HTTP smoke checks, manual recovery steps and explicit coverage limits.

### Reproduce proxy recovery locally

Requires Docker with the Compose plugin and Python 3.12. From the repository root:

```bash
python3 scripts/check_recovery.py
```

This builds an isolated local stack, checks HTTP **200 → 502 → 200** while stopping and starting its backend, runs the original smoke checks and removes the stack. It uses `127.0.0.1:8080`; free that port first. The exercise interrupts only the Compose project named `sidhanth-recovery-check`. It does not connect to AWS or validate a host reboot.

### Application tests

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest -q
```

### Continuous integration

[The workflow](.github/workflows/labs.yml) runs application tests, validates alert rules with `promtool`, builds both container stacks and checks backend recovery plus Prometheus scraping. It is build/test automation, **not automated deployment**. No AWS credentials are required. Consult the actual workflow run before claiming a passing CI result.

### Evidence and interview preparation

- [Verification record](docs/verification.md): what was actually run and what remains unverified.
- [Hands-on session](docs/hands-on-session.md): a bounded exercise to complete personally and explain in an interview.
- [Incident runbook](observability/RUNBOOK.md): distinguish service errors, latency and scrape failure.
