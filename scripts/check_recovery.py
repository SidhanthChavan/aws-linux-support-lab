"""Reproduce a 200 -> 502 -> 200 sequence in an isolated local Compose lab."""
import json
from pathlib import Path
import subprocess
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
COMPOSE = ['docker', 'compose', '-p', 'sidhanth-recovery-check', '-f', str(ROOT / 'compose.yml')]


def docker(*args):
    subprocess.run([*COMPOSE, *args], cwd=ROOT, check=True)


def wait_for(expected):
    deadline = time.monotonic() + 60
    last = None
    while time.monotonic() < deadline:
        try:
            with urlopen('http://127.0.0.1:8080/health', timeout=2) as response:
                last = response.status
        except HTTPError as error:
            last = error.code
        except (URLError, TimeoutError):
            last = None
        if last == expected:
            return {'expected_http_status': expected, 'observed_http_status': last}
        time.sleep(.5)
    raise RuntimeError(f'Expected {expected}; last response was {last}')


def main():
    observations = []
    try:
        docker('up', '--build', '-d')
        observations.append(wait_for(200))
        docker('stop', 'app')
        observations.append(wait_for(502))
        # start preserves the container IP that Nginx resolved at startup.
        docker('start', 'app')
        observations.append(wait_for(200))
        subprocess.run([sys.executable, str(ROOT / 'tests/smoke_health.py'),
                        'http://127.0.0.1:8080'], check=True)
        print(json.dumps({'scenario': 'local-compose-backend-recovery',
                          'observations': observations,
                          'scope': 'Does not validate EC2 or host reboot recovery'}, indent=2))
    finally:
        docker('down')


if __name__ == '__main__':
    main()
