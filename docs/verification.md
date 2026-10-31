# Verification record — 30 October 2026

## Executed in the development environment

| Check | Observed result |
| --- | --- |
| Python/FastAPI monitoring behaviour | 7 pytest tests passed |
| Original service through a live local Uvicorn process | 2 HTTP smoke checks passed: health contract and unknown route |
| Monitoring service through a live local Uvicorn process | HTTP 200 and controlled 503, request-ID propagation and metric export checked |
| Prometheus 3.5.0 `promtool check rules` | Success; 3 rules found |
| Prometheus 3.5.0 `promtool test rules` | Success; fixtures cover target failure/recovery, error rate, latency and absent traffic |
| YAML files | Parsed successfully |

The Python test run emitted upstream pytest/Starlette deprecation warnings; these did not fail the tests.

## Docker/CI validation

Docker is unavailable in the development environment. Container builds, Compose networking, the automated 200→502→200 exercise and live Prometheus scraping therefore require the GitHub Actions workflow or a local Docker run. The workflow is included; its presence alone is not evidence of a passing run. Record the actual run URL and result separately.

## Original EC2 exercise

The pre-existing [deployment notes](deployment-and-troubleshooting.md) record an EC2 deployment, port conflict, backend failure/recovery and reboot check. These are earlier project observations. No fresh AWS deployment, security-group audit or EC2 reboot was executed for this update.

## Ownership and claim boundaries

Code and documentation were developed with AI assistance. Follow the [hands-on session](hands-on-session.md), retain your own observations and understand the implementation before describing newly added features as personal practical experience.

Neither project demonstrates production availability, business impact, commercial cloud administration, automated AWS deployment, container orchestration or an SLO/error budget.
