import pytest
import responses
import python.prohibition_web_svc.middleware.keycloak_middleware as middleware
from python.prohibition_web_svc.models import db, User, UserRole
from python.prohibition_web_svc.config import Config, TestConfig
import logging
from datetime import datetime


@pytest.fixture
def roles(database):
    today = datetime.strptime("2021-07-21", "%Y-%m-%d")
    roles = [
        UserRole(user_guid="aaaa-bbbb-cccc-eeee", role_name='agency_admin', submitted_dt=today, approved_dt=today),
    ]
    users = [
        User(first_name="Bob",
             last_name="MacDonald",
             badge_number="4000",
             agency="RCMP Campbell River",
             user_guid="aaaa-bbbb-cccc-eeee",
             business_guid="RCMP_GUID"),
    ]
    db.session.bulk_save_objects(users)
    db.session.bulk_save_objects(roles)
    db.session.commit()


@responses.activate
def test_agency_administrator_can_query_mock_bceid_web_services_for_user_bsmith(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_administrative_user)

    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/bceid?username={}".format("bsmith"),
                        follow_redirects=True,
                        content_type="application/json",
                        headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    assert resp.status_code == 200
    assert resp.json == [{
            "badge_number": "8088",
            "first_name": "Bob",
            "last_name": "Smith",
            "business_guid": "AAAA-BBBB-CCCC-DDDD",
            "user_guid": "EEEE-FFFF-GGGG-HHHH",
            "agency": "RoadSafety"
        }]


@responses.activate
def test_agency_administrator_can_query_mock_bceid_web_services_is_case_insensitive(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_administrative_user)

    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/bceid?username={}".format("BSMITH"),
                        follow_redirects=True,
                        content_type="application/json",
                        headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    assert resp.status_code == 200
    assert resp.json == [{
            "badge_number": "8088",
            "first_name": "Bob",
            "last_name": "Smith",
            "business_guid": "AAAA-BBBB-CCCC-DDDD",
            "user_guid": "EEEE-FFFF-GGGG-HHHH",
            "agency": "RoadSafety"
        }]


@responses.activate
def test_regular_user_cannot_query_mock_bceid_web_services(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_authorized_user)

    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/bceid?username={}".format("bsmith"),
                        follow_redirects=True,
                        content_type="application/json",
                        headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    assert resp.status_code == 401


@responses.activate
def test_agency_administrator_receives_404_when_querying_mock_bceid_web_services_for_non_existent_user(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_administrative_user)

    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/bceid?username={}".format("sammy"),
                        follow_redirects=True,
                        content_type="application/json",
                        headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    assert resp.status_code == 404
    assert resp.json == {'error': 'record not found'}


@responses.activate
def test_agency_administrator_receives_404_when_querying_mock_bceid_web_services_for_no_user(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_administrative_user)

    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/bceid",
                        follow_redirects=True,
                        content_type="application/json",
                        headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    assert resp.status_code == 404
    assert resp.json == {'error': 'record not found'}


def _get_keycloak_access_token() -> str:
    return 'some-secret-access-token'


def _get_keycloak_auth_header(access_token) -> dict:
    return dict({
        'Authorization': 'Bearer {}'.format(access_token)
    })


def _mock_keycloak_certificates(**kwargs) -> tuple:
    logging.warning("inside _mock_keycloak_certificates()")
    return True, kwargs


def _get_unauthorized_user(**kwargs) -> tuple:
    logging.warning("inside _get_unauthorized_user()")
    kwargs['decoded_access_token'] = {'preferred_username': 'john@idir'}  # keycloak username
    return True, kwargs


def _get_authorized_user(**kwargs) -> tuple:
    logging.warning("inside _get_authorized_user()")
    kwargs['decoded_access_token'] = {'preferred_username': 'larry@idir'}  # keycloak username
    return True, kwargs


def _get_administrative_user(**kwargs) -> tuple:
    logging.warning("inside _get_authorized_user()")
    kwargs['decoded_access_token'] = {'preferred_username': 'aaaa-bbbb-cccc-eeee'}  # keycloak username
    return True, kwargs

