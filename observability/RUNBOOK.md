# Lab incident runbook

## Service errors: LabHighErrorRate

1. Check `/health`, `/work` and `up{job="observability-lab"}` separately. A successful scrape does not prove successful workload responses.
2. Compare 200 and 503 counters and their one-minute rates.
3. Find a failing request ID in the JSON logs; confirm the route, status and timestamp.
4. In this exercise, stop the error traffic and generate `recovery` traffic. Check that 5xx rate falls and the alert clears after the rolling window/evaluation catches up.
5. Record the actual outcome. This is controlled fault injection, not a discovered production defect.

## Slow workload: LabHighLatency

1. Check request counts to distinguish low traffic from missing telemetry.
2. Inspect the p95 estimate and duration histogram buckets for `/work`.
3. Compare request-log durations with the configured 500ms injected delay.
4. Stop delayed traffic and generate normal traffic. Observe how the previous minute of slow samples continues to affect the estimate temporarily.

## Scrape target unavailable: LabTargetDown

Run only against this disposable local Compose project:

```bash
docker compose -p observability-lab -f observability/compose.yml stop app
```

1. Wait for the 5-second scrape and 30-second hold. Check the Prometheus target error and `up` value.
2. Inspect `docker compose -p observability-lab -f observability/compose.yml ps -a`.
3. Restore with `docker compose -p observability-lab -f observability/compose.yml start app`.
4. Confirm `/health`, scrape success and alert resolution. Counters restart from zero with the app process; Prometheus `rate` handles counter resets.

## Minimal incident note

Record: UTC timestamp; symptom; affected endpoint; HTTP status; target state; request ID; checks; action; result; remaining uncertainty. Keep real credentials and public IP addresses out of committed notes.

## Interview explanation

Be able to explain the difference between a counter and a histogram, why request IDs are excluded from metric labels, why `up=1` can coexist with 503 responses, and why a restarted container is not proof of EC2 reboot recovery.
