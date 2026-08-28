# Deployment and Operational Notes

## Overview

The FastAPI health service was deployed to an Amazon Linux 2023 EC2 instance as a Docker container. Nginx provides the public HTTP entry point and proxies requests to the container on the host's loopback interface.

## Runtime Configuration

- Docker image: `aws-linux-support-lab`
- Container binding: `127.0.0.1:8000`
- Public entry point: Nginx on TCP port 80
- Container restart policy: `unless-stopped`
- Nginx configuration: [`infra/nginx-reverse-proxy.conf`](../infra/nginx-reverse-proxy.conf)

## Validation

The public `/health` endpoint returned HTTP 200 through the full request path:

```text
Client -> Nginx :80 -> Docker :8000 -> FastAPI /health
```

The EC2 instance was rebooted and the endpoint was verified again after instance status checks completed. Nginx, Docker and the application recovered successfully.

## Operational Scenarios

### Port conflict

A direct Docker publish to port 80 failed because Nginx was already listening on that port. The final design retains Nginx on port 80 and binds the container to `127.0.0.1:8000`.

### Backend recovery

Stopping the application container caused the public endpoint to return `502 Bad Gateway`. Nginx remained available, isolating the failure to the upstream container. Restarting the container restored HTTP 200 from the public health endpoint.

## Useful Commands

```bash
docker ps
docker logs --tail 20 aws-linux-support-lab
docker restart aws-linux-support-lab
curl http://127.0.0.1/health
```

## Security and Cost Controls

- The EC2 private key is not stored in the repository.
- The application port is not exposed publicly.
- SSH source ranges should be restricted for a production deployment.
- Stop non-production EC2 instances when they are not in use.
