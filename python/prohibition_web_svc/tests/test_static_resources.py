import responses
import json
from python.prohibition_web_svc.config import TestConfig


@responses.activate
def test_unauthorized_can_get_agencies(as_guest):
    responses.add(responses.POST, "{}:{}/services/collector".format(
        TestConfig.SPLUNK_HOST, TestConfig.SPLUNK_PORT), status=200)

    resp = as_guest.get(TestConfig.URL_PREFIX + "/api/v1/static/agencies",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert "2101" in resp.json
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'get static resource',
            'resource': 'agencies',
            'user_guid': '',
            'username': ''
        },
        'source': 'be78d6'
    })


@responses.activate
def test_unauthorized_user_gets_impound_lot_operators(as_guest):
    responses.add(responses.POST, "{}:{}/services/collector".format(
        TestConfig.SPLUNK_HOST, TestConfig.SPLUNK_PORT), status=200)

    resp = as_guest.get(TestConfig.URL_PREFIX + "/api/v1/static/impound_lot_operators",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert "24 HOUR TOWING" in resp.json[0]['name']
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'get static resource',
            'resource': 'impound_lot_operators',
            'user_guid': '',
            'username': ''
        },
        'source': 'be78d6'
    })


@responses.activate
def test_unauthorized_user_gets_provinces(as_guest):
    responses.add(responses.POST, "{}:{}/services/collector".format(
        TestConfig.SPLUNK_HOST, TestConfig.SPLUNK_PORT), status=200)

    resp = as_guest.get(TestConfig.URL_PREFIX + "/api/v1/static/provinces",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert 'objectCd' in resp.json[2]
    assert 'objectDsc' in resp.json[2]
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'get static resource',
            'resource': 'provinces',
            'user_guid': '',
            'username': ''
        },
        'source': 'be78d6'
    })


@responses.activate
def test_unauthorized_user_gets_jurisdictions(as_guest):
    responses.add(responses.POST, "{}:{}/services/collector".format(
        TestConfig.SPLUNK_HOST, TestConfig.SPLUNK_PORT), status=200)
    resp = as_guest.get(TestConfig.URL_PREFIX + "/api/v1/static/jurisdictions",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert "AB" in resp.json[2]['objectCd']
    assert "Alberta" in resp.json[2]['objectDsc']
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'get static resource',
            'resource': 'jurisdictions',
            'user_guid': '',
            'username': ''
        },
        'source': 'be78d6'
    })


@responses.activate
def test_unauthorized_user_can_get_countries(as_guest):
    responses.add(responses.POST, "{}:{}/services/collector".format(
        TestConfig.SPLUNK_HOST, TestConfig.SPLUNK_PORT), status=200)
    resp = as_guest.get(TestConfig.URL_PREFIX + "/api/v1/static/countries",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert 'objectCd' in resp.json[2]
    assert 'objectDsc' in resp.json[2]
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'get static resource',
            'resource': 'countries',
            'user_guid': '',
            'username': ''
        },
        'source': 'be78d6'
    })


@responses.activate
def test_unauthorized_user_gets_cities(as_guest):
    responses.add(responses.POST, "{}:{}/services/collector".format(
        TestConfig.SPLUNK_HOST, TestConfig.SPLUNK_PORT), status=200)

    resp = as_guest.get(TestConfig.URL_PREFIX + "/api/v1/static/cities",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert "VICTORIA" in resp.json
    assert "100 MILE HOUSE" in resp.json
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'get static resource',
            'resource': 'cities',
            'user_guid': '',
            'username': ''
        },
        'source': 'be78d6'
    })


@responses.activate
def test_unauthorized_user_can_get_vehicles(as_guest):
    resp = as_guest.get(TestConfig.URL_PREFIX + "/api/v1/static/vehicles",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert "ABAR" == resp.json[0]['mk']
    assert "ABARTH - " == resp.json[0]['search']
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'get static resource',
            'resource': 'vehicles',
            'user_guid': '',
            'username': ''
        },
        'source': 'be78d6'
    })


@responses.activate
def test_unauthorized_user_can_get_vehicle_styles(as_guest):
    resp = as_guest.get(TestConfig.URL_PREFIX + "/api/v1/static/vehicle_styles",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert {"code": "2DR", "name": "2-DOOR SEDAN"} == resp.json[0]
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'get static resource',
            'resource': 'vehicle_styles',
            'user_guid': '',
            'username': ''
        },
        'source': 'be78d6'
    })


@responses.activate
def test_unauthorized_user_can_get_keycloak_config(as_guest):
    resp = as_guest.get(TestConfig.URL_PREFIX + "/api/v1/static/keycloak",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 200
    assert 'realm' in resp.json
    assert 'url' in resp.json
    assert 'clientId' in resp.json
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'get static resource',
            'resource': 'keycloak',
            'user_guid': '',
            'username': ''
        },
        'source': 'be78d6'
    })
