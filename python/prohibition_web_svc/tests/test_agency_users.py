import pytest
import responses
from python.prohibition_web_svc.config import Config, TestConfig
from datetime import datetime
import python.prohibition_web_svc.middleware.keycloak_middleware as middleware
from python.prohibition_web_svc.models import db, UserRole, User
import logging
import json


@pytest.fixture
def roles(database):
    today = datetime.strptime("2021-07-21", "%Y-%m-%d")
    users = [
        User(user_guid="john@idir",
             agency='RCMP Terrace',
             badge_number='0508',
             first_name='John',
             last_name='Smith',
             business_guid='RCMP-GUID'),
        User(user_guid="larry@idir",
             agency='RCMP Terrace',
             badge_number='0555',
             first_name='Larry',
             last_name='Smith',
             business_guid='RCMP-GUID'),
        User(user_guid="mo@idir",
             agency='RCMP Terrace',
             badge_number='8088',
             first_name='Mo',
             last_name='Smith',
             business_guid='RCMP-GUID'),
        User(user_guid="outsider@idir",
             agency='Oak Bay Police',
             badge_number='123',
             first_name='Out',
             last_name='Side',
             business_guid='OAK-BAY-GUID'),
        User(user_guid="officer@idir",
             agency='Oak Bay Police',
             badge_number='8088',
             first_name='Officer',
             last_name='User',
             business_guid='OAK-BAY-GUID')
    ]
    db.session.bulk_save_objects(users)
    user_role = [
        UserRole(user_guid='john@idir', role_name='officer', submitted_dt=today),
        UserRole(user_guid='larry@idir', role_name='officer', submitted_dt=today, approved_dt=today),
        UserRole(user_guid='mo@idir', role_name='agency_admin', submitted_dt=today, approved_dt=today),
        UserRole(user_guid='mo@idir', role_name='officer', submitted_dt=today, approved_dt=today),
        UserRole(user_guid="outsider@idir", role_name="agency_admin", submitted_dt=today, approved_dt=today),
        UserRole(user_guid="officer@idir", role_name="officer", submitted_dt=today, approved_dt=today)
    ]
    db.session.bulk_save_objects(user_role)
    db.session.commit()



@responses.activate
def test_rcmp_agency_administrator_can_get_all_their_users(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_rcmp_agency_admin)
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/agency/{}/users".format("RCMP-GUID"),
                        follow_redirects=True,
                        content_type="application/json",
                        headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    logging.debug("dump query response: " + json.dumps(resp.json))
    assert resp.status_code == 200
    assert len(resp.json) == 3
    assert resp.json[0]['user_guid'] == 'john@idir'
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'get users',
            'business_guid': 'RCMP-GUID',
            'requesting_user_guid': 'mo@idir',
            'requesting_username': 'mo@idir'
        },
        'source': 'be78d6'
    })


@responses.activate
def test_rcmp_agency_admins_cannot_get_users_at_oak_bay_police(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_rcmp_agency_admin)
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/agency/{}/users".format("RCMP-GUID"),
                        follow_redirects=True,
                        content_type="application/json",
                        headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    logging.debug(json.dumps(resp.json))
    assert resp.status_code == 200
    assert len(resp.json) == 3
    assert {"user_guid"} not in resp.json
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'get users',
            'business_guid': 'RCMP-GUID',
            'requesting_user_guid': 'mo@idir',
            'requesting_username': 'mo@idir'
        },
        'source': 'be78d6'
    })


@responses.activate
def test_oak_bay_agency_admin_cannot_see_users_at_rcmp(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_oak_bay_agency_admin)
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/agency/{}/users".format("RCMP-GUID"),
                        follow_redirects=True,
                        content_type="application/json",
                        headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    logging.debug(json.dumps(resp.json))
    assert resp.status_code == 400
    assert resp.json == {'error': 'you cannot access or update users at a different agency'}


@responses.activate
def test_oak_bay_agency_admin_cannot_create_user_within_rcmp_agency(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_oak_bay_agency_admin)
    resp = as_guest.post(Config.URL_PREFIX + "/api/v1/agency/{}/users".format("RCMP-GUID"),
                         json={},
                         follow_redirects=True,
                         content_type="application/json",
                         headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    logging.debug(json.dumps(resp.json))
    assert resp.status_code == 400
    assert resp.json == {'error': 'you cannot access or update users at a different agency'}


@responses.activate
def test_oak_bay_agency_admin_cannot_create_user_within_administrator_role(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_oak_bay_agency_admin)
    resp = as_guest.post(Config.URL_PREFIX + "/api/v1/agency/{}/users".format("OAK-BAY-GUID"),
                         json={
                             "user_guid": "frank@bceid",
                             "business_guid": "OAK-BAY-GUID",
                             "agency": "Oay Bay Police Dept",
                             "badge_number": "8088",
                             "first_name": "Frank",
                             "last_name": "Smith",
                             "roles": ["officer", "administrator"]
                         },
                         follow_redirects=True,
                         content_type="application/json",
                         headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    logging.debug(json.dumps(resp.json))
    assert resp.status_code == 400
    assert resp.json == {
        'errors': {
            'roles': [{'1': ['unallowed value administrator']}]
         },
        'message': 'failed validation'
    }


@responses.activate
def test_oak_bay_agency_admin_can_add_an_officer_within_their_agency(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_oak_bay_agency_admin)
    resp = as_guest.post(Config.URL_PREFIX + "/api/v1/agency/{}/users".format("OAK-BAY-GUID"),
                         json={
                             "user_guid": "frank@bceid",
                             "business_guid": "OAK-BAY-GUID",
                             "agency": "Oay Bay Police Dept",
                             "badge_number": "8088",
                             "first_name": "Frank",
                             "last_name": "Smith",
                             "roles": ["officer"]
                         },
                         follow_redirects=True,
                         content_type="application/json",
                         headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    assert resp.status_code == 201
    assert responses.calls[0].request.body.decode() == json.dumps({
        "event": {
            "event": "create user",
            "requesting_user_guid": "outsider@idir",
            "requesting_username": "outsider@idir",
            "business_guid": "OAK-BAY-GUID",
            "payload": {
                "agency": "Oay Bay Police Dept",
                "badge_number": "8088",
                "business_guid": "OAK-BAY-GUID",
                "first_name": "Frank",
                "last_name": "Smith",
                "roles": ["officer"],
                "user_guid": "frank@bceid"
            }},
        "source": "be78d6"
    })


@responses.activate
def test_oak_bay_agency_admin_can_update_an_officer_within_their_agency(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_oak_bay_agency_admin)
    resp = as_guest.patch(Config.URL_PREFIX + "/api/v1/agency/{}/users/{}".format("OAK-BAY-GUID", "officer@idir"),
                          json={
                              "user_guid": "officer@idir",
                              "business_guid": "OAK-BAY-GUID",
                              "agency": "Oay Bay Police Dept",
                              "badge_number": "8088",
                              "first_name": "Frank",
                              "last_name": "Smith",
                              "roles": ["officer"]
                          },
                          follow_redirects=True,
                          content_type="application/json",
                          headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    assert resp.status_code == 200
    assert responses.calls[0].request.body.decode() == json.dumps({
        "event": {
            "event": "update user",
            "requesting_user_guid": "outsider@idir",
            "requesting_username": "outsider@idir",
            "business_guid": "OAK-BAY-GUID",
            "payload": {
                "agency": "Oay Bay Police Dept",
                "badge_number": "8088",
                "business_guid": "OAK-BAY-GUID",
                "first_name": "Frank",
                "last_name": "Smith",
                "roles": ["officer"],
                "user_guid": "officer@idir"
            }},
        "source": "be78d6"
    })


@responses.activate
def test_oak_bay_agency_admin_cannot_change_the_user_guid(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_oak_bay_agency_admin)
    resp = as_guest.patch(Config.URL_PREFIX + "/api/v1/agency/{}/users/{}".format("OAK-BAY-GUID", "officer@idir"),
                          json={
                              "user_guid": "frank@bceid",
                              "business_guid": "OAK-BAY-GUID",
                              "agency": "Oay Bay Police Dept",
                              "badge_number": "8088",
                              "first_name": "Frank",
                              "last_name": "Smith",
                              "roles": ["officer"]
                          },
                          follow_redirects=True,
                          content_type="application/json",
                          headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    assert resp.status_code == 400
    assert resp.json == {'error': 'You cannot change the user guid; create a new user instead'}


@responses.activate
def test_oak_bay_agency_admin_cannot_change_the_business_guid(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_oak_bay_agency_admin)
    resp = as_guest.patch(Config.URL_PREFIX + "/api/v1/agency/{}/users/{}".format("OAK-BAY-GUID", "officer@idir"),
                          json={
                              "user_guid": "officer@idir",
                              "business_guid": "OTHER-GUID",
                              "agency": "Oay Bay Police Dept",
                              "badge_number": "8088",
                              "first_name": "Frank",
                              "last_name": "Smith",
                              "roles": ["officer"]
                          },
                          follow_redirects=True,
                          content_type="application/json",
                          headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    assert resp.status_code == 400
    assert resp.json == {'error': 'You cannot change the business guid; create a new user instead'}


@responses.activate
def test_oak_bay_agency_admin_cannot_update_an_officer_at_another_agency(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_oak_bay_agency_admin)
    resp = as_guest.patch(Config.URL_PREFIX + "/api/v1/agency/{}/users/{}".format("OAK-BAY-GUID", "john@idir"),
                          json={
                              "user_guid": "frank@bceid",
                              "business_guid": "OAK-BAY-GUID",
                              "agency": "Oay Bay Police Dept",
                              "badge_number": "8088",
                              "first_name": "Frank",
                              "last_name": "Smith",
                              "roles": ["officer"]
                          },
                          follow_redirects=True,
                          content_type="application/json",
                          headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    assert resp.status_code == 400
    assert resp.json == {'error': 'you cannot access or update users at a different agency'}


@responses.activate
def test_oak_bay_agency_admin_can_delete_an_officer_within_their_agency(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_oak_bay_agency_admin)
    resp = as_guest.delete(Config.URL_PREFIX + "/api/v1/agency/{}/users/{}".format("OAK-BAY-GUID", "officer@idir"),
                           follow_redirects=True,
                           content_type="application/json",
                           headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    assert resp.status_code == 200


@responses.activate
def test_oak_bay_agency_admin_cannot_delete_an_officer_at_another_agency(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_oak_bay_agency_admin)
    resp = as_guest.delete(Config.URL_PREFIX + "/api/v1/agency/{}/users/{}".format("OAK-BAY-GUID", "john@idir"),
                           follow_redirects=True,
                           content_type="application/json",
                           headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    assert resp.status_code == 400
    assert resp.json == {'error': 'you cannot access or update users at a different agency'}



def _get_keycloak_access_token() -> str:
    return 'some-secret-access-token'


def _get_keycloak_auth_header(access_token) -> dict:
    return dict({
        'Authorization': 'Bearer {}'.format(access_token)
    })


def _mock_keycloak_certificates(**kwargs) -> tuple:
    logging.warning("inside _mock_keycloak_certificates()")
    return True, kwargs


def _get_authorized_user(**kwargs) -> tuple:
    logging.warning("inside _get_authorized_user()")
    kwargs['decoded_access_token'] = {'preferred_username': 'larry@idir'}
    return True, kwargs


def _get_rcmp_officer_user(**kwargs) -> tuple:
    kwargs['decoded_access_token'] = {
        'preferred_username': 'larry@idir',
        'bceid_userid': 'larry@idir',
        'bceid_business_guid': 'RCMP-GUID'
    }
    return True, kwargs


def _get_rcmp_agency_admin(**kwargs) -> tuple:
    kwargs['decoded_access_token'] = {
        'preferred_username': 'mo@idir',
        'bceid_userid': 'mo@idir',
        'bceid_business_guid': 'RCMP-GUID'
    }
    return True, kwargs


def _get_oak_bay_agency_admin(**kwargs) -> tuple:
    kwargs['decoded_access_token'] = {
        'preferred_username': 'outsider@idir',
        'bceid_userid': 'outsider@idir',
        'bceid_business_guid': 'OAK-BAY-GUID'
    }
    return True, kwargs
