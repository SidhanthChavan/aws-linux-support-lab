# AWS Linux Support Lab

A hands-on cloud support project that deploys a containerised FastAPI health service on Amazon Linux 2023 EC2 behind Nginx.

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
docker run --rm -p 8000:8000 aws-linux-support-lab
```

Then open `http://127.0.0.1:8000/health`.

## Deployment design

The EC2 host runs Nginx on port 80. The FastAPI container is bound to `127.0.0.1:8000`, with Nginx forwarding incoming requests to the application. This keeps the application port off the public network while retaining a standard HTTP entry point.

See [deployment and operational notes](docs/deployment-and-troubleshooting.md) for the validated deployment and recovery scenarios.

## Scope

This repository is a focused cloud-support lab rather than a production platform. Production hardening would include HTTPS, restricted SSH source ranges, monitoring and alerting, infrastructure as code, and a managed container deployment strategy.
