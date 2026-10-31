# A 30-minute recovery exercise

Code and documentation were developed with AI assistance. Run the checks personally, retain terminal output and explain each observation before presenting the newly added automation as hands-on experience.

## First 15 minutes

With Python 3.12 and Docker Compose installed, run `python3 scripts/check_recovery.py` from the repository root. The script creates the local stack, verifies 200, stops the backend, verifies 502, starts the backend, verifies 200, runs two smoke checks and removes its stack.

Explain which component is still alive during the 502, why starting the backend restores service, and why the backend does not need a public host port in this local Compose arrangement.

## Next 15 minutes

Read `infra/nginx-compose.conf` alongside `infra/nginx-reverse-proxy.conf`. Explain why the Compose upstream uses the service name while the original EC2 configuration uses `127.0.0.1:8000`.

Write a short incident note: symptom, checks, action, observed recovery and limits. Local container stop/start is not proof of EC2 reboot recovery; the earlier EC2 exercise is separate evidence.

The next exercise is in the [companion monitoring repository](https://github.com/SidhanthChavan/service-observability-lab).
