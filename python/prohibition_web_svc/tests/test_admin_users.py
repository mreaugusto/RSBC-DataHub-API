import pytest
import responses
from python.prohibition_web_svc.config import Config
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
             last_name='Wall',
             business_guid='RCMP_GUID'),
        User(user_guid="larry@idir",
             agency='RCMP Terrace',
             badge_number='0555',
             first_name='Larry',
             last_name='Smith',
             business_guid='RCMP_GUID'),
        User(user_guid="mo@idir",
             agency='RCMP Terrace',
             badge_number='8088',
             first_name='Mo',
             last_name='Walker',
             business_guid='RCMP_GUID')
    ]
    db.session.bulk_save_objects(users)
    user_role = [
        UserRole(user_guid='john@idir', role_name='officer', submitted_dt=today),
        UserRole(user_guid='larry@idir', role_name='officer', submitted_dt=today, approved_dt=today),
        UserRole(user_guid='mo@idir', role_name='administrator', submitted_dt=today, approved_dt=today),
        UserRole(user_guid='mo@idir', role_name='officer', submitted_dt=today, approved_dt=today)
    ]
    db.session.bulk_save_objects(user_role)
    db.session.commit()


@responses.activate
def test_administrator_can_get_all_users(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_administrative_user)
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/admin/users",
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
            'business_guid': 'IDIR',
            'requesting_user_guid': 'mo@idir',
            'requesting_username': 'mo@idir'
        },
        'source': 'be78d6'
    })


@responses.activate
def test_administrator_can_get_filter_users_by_last_name(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_administrative_user)
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/admin/users?last_name=walker",
                        follow_redirects=True,
                        content_type="application/json",
                        headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    logging.debug("dump query response: " + json.dumps(resp.json))
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['user_guid'] == 'mo@idir'
    assert resp.json[0]['last_name'] == 'Walker'


@responses.activate
def test_non_administrators_cannot_get_all_users(as_guest, monkeypatch, roles):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_authorized_user)
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/admin/users",
                         follow_redirects=True,
                         content_type="application/json",
                         headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    logging.debug(json.dumps(resp.json))
    assert resp.status_code == 401
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'permission denied',
            'user_guid': 'larry@idir',
            'username': 'larry@idir'
        },
        'source': 'be78d6'
    })


@responses.activate
def test_admin_can_add_a_new_user(as_guest, monkeypatch, roles, database):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_administrative_user)
    resp = as_guest.post(Config.URL_PREFIX + "/api/v1/admin/users",
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
    assert database.session.query(User) \
               .filter(User.user_guid == 'frank@bceid') \
               .filter(User.business_guid == 'OAK-BAY-GUID') \
               .count() == 1


@responses.activate
def test_admin_can_update_a_user(as_guest, monkeypatch, roles, database):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_administrative_user)
    resp = as_guest.patch(Config.URL_PREFIX + "/api/v1/admin/users/{}".format("john@idir"),
                         json={
                             "user_guid": "john@idir",
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
    assert database.session.query(User) \
               .filter(User.user_guid == 'john@idir') \
               .filter(User.first_name == 'Frank') \
               .count() == 1


@responses.activate
def test_admin_cannot_change_the_user_guid_of_an_existing_user(as_guest, monkeypatch, roles, database):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_administrative_user)
    resp = as_guest.patch(Config.URL_PREFIX + "/api/v1/admin/users/{}".format("john@idir"),
                          json={
                              "user_guid": "frank@idir",
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
def test_admin_can_delete_any_user(as_guest, monkeypatch, roles, database):
    monkeypatch.setattr(middleware, "get_keycloak_certificates", _mock_keycloak_certificates)
    monkeypatch.setattr(middleware, "decode_keycloak_access_token", _get_administrative_user)
    resp = as_guest.delete(Config.URL_PREFIX + "/api/v1/admin/users/{}".format('john@idir'),
                           follow_redirects=True,
                           content_type="application/json",
                           headers=_get_keycloak_auth_header(_get_keycloak_access_token()))
    assert resp.status_code == 200
    assert database.session.query(User) \
               .filter(User.user_guid == 'john@idir') \
               .count() == 0


@responses.activate
def test_unauthenticated_user_cannot_get_all_users(as_guest, monkeypatch, roles):
    resp = as_guest.get(Config.URL_PREFIX + "/api/v1/admin/users",
                         follow_redirects=True,
                         content_type="application/json")
    logging.debug(json.dumps(resp.json))
    assert resp.status_code == 401
    assert responses.calls[0].request.body.decode() == json.dumps({
        'event': {
            'event': 'unauthenticated',
        },
        'source': 'be78d6'
    })


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


def _get_administrative_user(**kwargs) -> tuple:
    kwargs['decoded_access_token'] = {
        'preferred_username': 'mo@idir',
        'idir_guid': 'mo@idir'
    }
    return True, kwargs
