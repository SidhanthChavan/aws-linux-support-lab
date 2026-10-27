"""Black-box HTTP smoke checks; run against an already running lab service."""
import json
import sys
import unittest
from urllib.error import HTTPError
from urllib.request import urlopen

BASE_URL = (sys.argv.pop(1) if len(sys.argv) > 1 else 'http://127.0.0.1:8000').rstrip('/')

class HealthContractTests(unittest.TestCase):
    def test_health_status_and_body(self):
        with urlopen(BASE_URL + '/health', timeout=5) as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(response.headers.get_content_type(), 'application/json')
            self.assertEqual(json.load(response), {'status': 'ok', 'service': 'aws-linux-support-lab'})

    def test_unknown_route_returns_not_found(self):
        with self.assertRaises(HTTPError) as caught:
            urlopen(BASE_URL + '/not-a-lab-route', timeout=5)
        self.assertEqual(caught.exception.code, 404)

if __name__ == '__main__':
    unittest.main()
