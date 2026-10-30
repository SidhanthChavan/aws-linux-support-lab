FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY observability/requirements.txt /app/observability/requirements.txt
RUN pip install --no-cache-dir -r observability/requirements.txt
COPY observability /app/observability
USER 10001:10001
EXPOSE 8000
CMD ["uvicorn", "observability.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--log-config", "observability/logging.json"]
