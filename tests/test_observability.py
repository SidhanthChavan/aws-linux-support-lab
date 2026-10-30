import json
import logging
import re

from fastapi.testclient import TestClient
from prometheus_client.parser import text_string_to_metric_families

from observability.main import create_app


def samples(client, name):
    return [s for f in text_string_to_metric_families(client.get('/metrics').text)
            for s in f.samples if s.name == name]


def test_success_failure_and_histogram_counts():
    with TestClient(create_app(faults_enabled=True)) as client:
        assert client.get('/work').status_code == 200
        assert client.get('/work?fail=true').status_code == 503
        counts = {s.labels['status']: s.value for s in samples(client, 'lab_http_requests_total')}
        assert counts == {'200': 1, '503': 1}
        assert sum(s.value for s in samples(client, 'lab_http_request_duration_seconds_count')) == 2


def test_faults_are_opt_in_and_delay_is_bounded():
    with TestClient(create_app()) as client:
        assert client.get('/work').status_code == 200
        assert client.get('/work?fail=true').status_code == 403
        assert client.get('/work?delay_ms=1').status_code == 403
        assert client.get('/work?delay_ms=2001').status_code == 422
        assert client.get('/work?delay_ms=-1').status_code == 422


def test_delay_is_observed_in_histogram():
    with TestClient(create_app(faults_enabled=True)) as client:
        assert client.get('/work?delay_ms=50').status_code == 200
        assert sum(s.value for s in samples(client, 'lab_http_request_duration_seconds_sum')) >= .045


def test_labels_do_not_include_ids_urls_or_query_strings():
    with TestClient(create_app()) as client:
        for item in (1, 2, 999):
            assert client.get(f'/items/{item}?private=value').status_code == 200
        for path in ('/absent-a', '/absent-b'):
            assert client.get(path).status_code == 404
        counts = samples(client, 'lab_http_requests_total')
        assert {s.labels['route'] for s in counts} == {'/items/{item_id}', 'unmatched'}
        assert sorted(s.value for s in counts) == [2, 3]


def test_request_ids_and_structured_logs(caplog):
    caplog.set_level(logging.INFO, logger='lab.requests')
    with TestClient(create_app()) as client:
        response = client.get('/health?secret=never-log', headers={'X-Request-ID': 'demo-123'})
        assert response.headers['X-Request-ID'] == 'demo-123'
        generated = client.get('/health', headers={'X-Request-ID': 'bad id'}).headers['X-Request-ID']
        assert re.fullmatch('[a-f0-9]{32}', generated)
    events = [json.loads(r.message) for r in caplog.records if r.name == 'lab.requests']
    assert events[0]['route'] == '/health'
    assert events[0]['request_id'] == 'demo-123'
    assert 'secret' not in json.dumps(events)


def test_scrapes_do_not_change_request_metrics_and_registries_are_isolated():
    with TestClient(create_app()) as first, TestClient(create_app()) as second:
        first.get('/health')
        first.get('/metrics')
        first.get('/metrics')
        assert sum(s.value for s in samples(first, 'lab_http_requests_total')) == 1
        assert samples(second, 'lab_http_requests_total') == []


def test_unexpected_exception_is_counted_without_exposing_details():
    app = create_app()
    @app.get('/broken')
    async def broken():
        raise RuntimeError('private failure details')
    with TestClient(app) as client:
        response = client.get('/broken')
        assert response.status_code == 500
        assert 'private' not in response.text
        assert samples(client, 'lab_http_requests_total')[0].labels['status'] == '500'
