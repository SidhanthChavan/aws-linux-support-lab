"""Bounded, sequential traffic for the local observability lab only."""
import argparse
import json
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import uuid


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scenario', choices=['normal', 'errors', 'slow', 'recovery'])
    parser.add_argument('--seconds', type=int, default=150)
    args = parser.parse_args()
    if not 1 <= args.seconds <= 900:
        parser.error('--seconds must be between 1 and 900')
    path = {'normal': '/work', 'errors': '/work?fail=true',
            'slow': '/work?delay_ms=500', 'recovery': '/work'}[args.scenario]
    end = time.monotonic() + args.seconds
    counts = {}
    while time.monotonic() < end:
        req = Request('http://127.0.0.1:8001' + path,
                      headers={'X-Request-ID': 'demo-' + uuid.uuid4().hex})
        try:
            with urlopen(req, timeout=4) as response:
                status = str(response.status)
        except HTTPError as error:
            status = str(error.code)
        counts[status] = counts.get(status, 0) + 1
        time.sleep(.1)
    print(json.dumps({'scenario': args.scenario, 'seconds_requested': args.seconds,
                      'status_counts': counts}, indent=2))


if __name__ == '__main__':
    main()
