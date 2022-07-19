from flask import jsonify, make_response
import logging
import json
from datetime import datetime
import pytz
from python.prohibition_web_svc.config import Config
from python.prohibition_web_svc.models import db, User, UserRole, UserSchema


def update_the_user(**kwargs) -> tuple:
    try:
        new_roles = []
        now = _get_now()
        for role in kwargs.get('payload')['roles']:
            new_roles.append(
                UserRole(
                    role_name=role,
                    submitted_dt=now,
                    approved_dt=now,
                    user_guid=kwargs.get('payload')['user_guid']
                ))
        user = db.session.query(User) \
            .filter(User.user_guid == kwargs.get('payload')['user_guid']) \
            .first()
        user.badge_number = kwargs.get('payload')['badge_number']
        user.agency = kwargs.get('payload')['agency']
        user.first_name = kwargs.get('payload')['first_name']
        user.last_name = kwargs.get('payload')['last_name']
        db.session.commit()
    except Exception as e:
        logging.warning(str(e))
        return False, kwargs
    return True, kwargs


def create_a_user(**kwargs) -> tuple:
    now = _get_now()
    try:
        payload = kwargs.get('payload')

        new_roles = []
        for role in payload.get('roles'):
            new_roles.append(
                UserRole(
                    role_name=role,
                    submitted_dt=now,
                    approved_dt=now,
                    user_guid=payload.get('user_guid')
                ))
        user = User(
            user_guid=payload.get('user_guid'),
            business_guid=payload.get('business_guid'),
            badge_number=payload.get('badge_number'),
            agency=payload.get('agency'),
            first_name=payload.get('first_name'),
            last_name=payload.get('last_name'),
            roles=new_roles
        )
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        logging.warning(str(e))
        return False, kwargs
    return True, kwargs


def delete_a_user(**kwargs) -> tuple:
    try:
        UserRole.query.filter_by(user_guid=kwargs.get('url_user_guid')).delete()
        User.query.filter_by(user_guid=kwargs.get('url_user_guid')).delete()
        db.session.commit()
    except Exception as e:
        logging.warning(str(e))
        return False, kwargs
    return True, kwargs


def request_contains_a_payload(**kwargs) -> tuple:
    request = kwargs.get('request')
    try:
        payload = request.get_json()
    except Exception as e:
        logging.warning(str(e))
        return False, kwargs
    kwargs['payload'] = payload
    logging.warning("payload: " + json.dumps(payload))
    return payload is not None, kwargs


def get_user(**kwargs) -> tuple:
    try:
        user = User.query.filter_by(user_guid=kwargs.get('user_guid')).first_or_404()
        user_schema = UserSchema(many=False)
        kwargs['response'] = make_response(user_schema.jsonify(user), 200)
    except Exception as e:
        logging.debug(str(e))
        return False, kwargs
    return True, kwargs


def query_all_users(**kwargs) -> tuple:
    request = kwargs.get('request')
    last_name = request.args.get('last_name')
    try:
        if last_name:
            search = "%{}%".format(last_name)
            users = User.query.filter(User.last_name.like(search)).limit(Config.MAX_RECORDS_RETURNED).all()
        else:
            users = User.query.limit(Config.MAX_RECORDS_RETURNED).all()
        user_schema = UserSchema(many=True)
        kwargs['response'] = user_schema.jsonify(users)
    except Exception as e:
        logging.warning(str(e))
        return False, kwargs
    return True, kwargs


def query_all_agency_users(**kwargs) -> tuple:
    try:
        users = User.query.filter_by(business_guid=kwargs.get('url_business_guid')).limit(Config.MAX_RECORDS_RETURNED).all()
        user_schema = UserSchema(many=True)
        kwargs['response'] = user_schema.jsonify(users)
    except Exception as e:
        logging.warning(str(e))
        return False, kwargs
    return True, kwargs


def user_belongs_to_business(**kwargs) -> tuple:
    try:
        user_count = User.query.filter_by(business_guid=kwargs.get('url_business_guid'),
                                          user_guid=kwargs.get('url_user_guid')).count()
        logging.warning("user_count: " + str(user_count))
    except Exception as e:
        logging.debug(str(e))
        return False, kwargs
    return user_count == 1, kwargs


def payload_user_matches_url_user_guid(**kwargs) -> tuple:
    """
    When updating a user, the user_guid cannot be changed.
    Create a new user instead.
    """
    payload_user_guid = kwargs.get("payload")["user_guid"]
    url_user_guid = kwargs.get("url_user_guid")
    return payload_user_guid == url_user_guid, kwargs


def payload_business_guid_matches_url_business_guid(**kwargs) -> tuple:
    """
    When updating a user, the business_guid cannot be changed.
    Create a new user instead.
    """
    payload_business_guid = kwargs.get("payload")["business_guid"]
    url_business_guid = kwargs.get("url_business_guid")
    return payload_business_guid == url_business_guid, kwargs


def _get_now() -> datetime:
    tz = pytz.timezone("America/Vancouver")
    return datetime.now(tz)