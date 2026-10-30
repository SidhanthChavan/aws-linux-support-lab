# Your next 60-minute practical session

The code and documentation were developed with AI assistance. Complete the checks yourself before presenting them as personal hands-on experience. Keep your own terminal output and explain each result in your own words.

## 0–15 minutes: proxy recovery

Run `python3 scripts/check_recovery.py`. Explain which component is still alive during the 502 and why starting the backend restores 200. This is local Compose; the original EC2 notes are separate evidence.

## 15–30 minutes: counters and request IDs

Start the monitoring stack using its README. Generate normal and error traffic. Send `curl -i -H 'X-Request-ID: my-check-1' http://127.0.0.1:8001/work`. Find that ID in the app logs. Identify the 200/503 counter series in `/metrics`.

## 30–45 minutes: slow service and target failure

Run the slow phase and inspect the histogram and latency alert. Then stop the app, observe `up=0` and restore it using the runbook. State which observations prove reachability, successful requests and latency separately.

## 45–60 minutes: write and explain evidence

Write one incident note from your actual run. Capture the query/alert before and after recovery. Answer aloud:

1. Why should a request ID never be a metric label here?
2. Why did a controlled 503 not make the Prometheus target go down?
3. What do the histogram buckets mean, and why is p95 approximate?
4. Which checks ran locally, which ran in CI, and which still require EC2?

Finish by stopping the local stacks. Do not add production scale, customer impact, uptime improvements or AWS automation claims to your CV from these exercises.
