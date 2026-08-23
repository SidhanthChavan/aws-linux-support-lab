# AWS Linux Support Lab

A practical cloud-support lab covering Linux administration, Docker deployment, AWS EC2 operations, SSH access, networking, troubleshooting, and service recovery.

## Objective

Deploy and operate a small FastAPI service on an Amazon Linux 2023 EC2 instance using Docker, then verify that the service remains recoverable after failure and reboot.

## Architecture

```text
Local Mac
   │ SSH / SCP
   ▼
AWS EC2 — Amazon Linux 2023
   │
   ▼
Docker container
   │
   ▼
FastAPI + Uvicorn
   │
   ▼
GET /health


```

## Technologies

AWS EC2 · Amazon Linux 2023 · Docker · FastAPI · Uvicorn · Linux CLI · SSH · SCP · Git

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Test the service:

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
docker run -d --name aws-linux-support-lab -p 8000:8000 aws-linux-support-lab
docker logs aws-linux-support-lab
```

## AWS deployment

The service was copied to an EC2 instance running Amazon Linux 2023, built into a Docker image, and exposed through the configured security-group port.

Operational checks included SSH access, Docker service management, container logs, connectivity troubleshooting, automatic restart after reboot, and public health-endpoint verification.

## Scope

This is a hands-on junior cloud-support lab, not a production architecture. It demonstrates practical Linux, Docker, AWS, and troubleshooting workflow.
