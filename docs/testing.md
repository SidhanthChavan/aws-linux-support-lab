# Health-service validation

These checks were added after the original deployment exercise. They validate
the HTTP contract of a running service; they do not prove production readiness.

## Automated HTTP checks

Start the application using the README instructions, then run from the repository root:

```bash
python tests/smoke_health.py http://127.0.0.1:8000
```

The test uses only Python's standard library. It checks HTTP 200, a JSON content
type and the expected health payload, plus HTTP 404 for an unknown route.
Use the Nginx base URL instead to check the proxy path. An unhealthy or unreachable
service causes the test to fail. Do not run against unrelated systems.

## Manual recovery checks

Run only on your own non-production EC2 lab. Record the date, command, status
and recovery action. These steps intentionally interrupt the service.

1. Check `/health` through Nginx and directly through `127.0.0.1:8000`.
2. Stop the application container. Check for HTTP 502 through Nginx; confirm
   that Nginx is running and the backend is unavailable.
3. Start the container again, rerun the HTTP checks and record HTTP 200.
4. During a planned lab reboot, check Nginx, Docker, the container restart
   policy and the public endpoint after EC2 status checks finish.

Use the actual container name from `docker ps -a`; `docker start` is needed
after an intentional stop. An `unless-stopped` policy does not automatically
start a container that was explicitly stopped.

## Coverage and limitations

The automated checks exercise a live HTTP endpoint. They do not test Docker
builds, EC2 provisioning, security-group rules, TLS, monitoring, load, reboot
recovery or availability. EC2 and reboot scenarios remain manual. The new
`scripts/check_recovery.py` reproduces the backend stop/start sequence in local
Docker Compose. The CI workflow validates application tests, container builds,
local proxy recovery, Prometheus scraping and alert-rule behaviour. It does
not deploy to AWS. See `deployment-and-troubleshooting.md` for the original
deployment observations and `verification.md` for the latest validation scope.
