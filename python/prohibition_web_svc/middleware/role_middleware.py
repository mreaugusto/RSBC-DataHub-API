from flask import jsonify, make_response
import pytz
from datetime import datetime
import logging
import json
from python.prohibition_web_svc.config import Config
from python.prohibition_web_svc.models import db, UserRole, User, UserRoleSchema, UserSchema


# def query_current_users_roles(**kwargs) -> tuple:
#     try:
#         my_roles = db.session.query(UserRole) \
#             .filter(UserRole.user_guid == kwargs['user_guid']) \
#             .filter(UserRole.approved_dt != None) \
#             .all()
#         user_role_schema = UserRoleSchema(many=True)
#         kwargs['response'] = make_response(jsonify(user_role_schema.dump(my_roles)))
#     except Exception as e:
#         logging.warning(str(e))
#         return False, kwargs
#     return True, kwargs


# def query_all_users_roles(**kwargs) -> tuple:
#     try:
#         user = db.session.query(User) \
#             .filter(User.user_guid == kwargs.get('requested_user_guid')) \
#             .limit(Config.MAX_RECORDS_RETURNED).first()
#         user_schema = UserSchema()
#         kwargs['response'] = make_response(jsonify(user_schema.dump(user)), 200)
#     except Exception as e:
#         logging.warning(str(e))
#         return False, kwargs
#     return True, kwargs


# def officer_has_not_applied_previously(**kwargs) -> tuple:
#     try:
#         roles = db.session.query(UserRole) \
#             .filter(UserRole.role_name == 'officer') \
#             .filter(UserRole.user_guid == kwargs.get('username')) \
#             .count()
#         logging.debug("inside officer_has_not_applied_previously(): " + str(roles))
#     except Exception as e:
#         logging.warning(str(e))
#         return False, kwargs
#     return roles == 0, kwargs


# def create_a_role(**kwargs) -> tuple:
#     tz = pytz.timezone('America/Vancouver')
#     try:
#         role_user = UserRole("officer", kwargs.get('username'), datetime.now(tz))
#         db.session.add(role_user)
#         db.session.commit()
#         user_role_schema = UserRoleSchema()
#         kwargs['response'] = make_response(jsonify(user_role_schema.dump(role_user)), 201)
#     except Exception as e:
#         logging.warning(str(e))
#         return False, kwargs
#     return True, kwargs


# def approve_officers_role(**kwargs) -> tuple:
#     try:
#         user_role = db.session.query(UserRole) \
#             .filter(UserRole.role_name == 'officer') \
#             .filter(UserRole.user_guid == kwargs.get('requested_user_guid')) \
#             .first()
#         logging.warning("user_guid: " + kwargs.get('requested_user_guid'))
#         tz = pytz.timezone('America/Vancouver')
#         user_role.approved_dt = datetime.now(tz)
#         db.session.commit()
#         user_role_schema = UserRoleSchema(many=False)
#         kwargs['response'] = make_response(user_role_schema.jsonify(user_role), 200)
#     except Exception as e:
#         logging.warning(str(e))
#         return False, kwargs
#     return True, kwargs
#
#
# def delete_a_role(**kwargs) -> tuple:
#
#     try:
#         user_role = db.session.query(UserRole) \
#             .filter(UserRole.role_name == kwargs.get('role_name')) \
#             .filter(UserRole.user_guid == kwargs.get('requested_user_guid')) \
#             .first()
#         db.session.delete(user_role)
#         db.session.commit()
#         kwargs['response'] = make_response("okay", 200)
#     except Exception as e:
#         logging.warning(str(e))
#         return False, kwargs
#     return True, kwargs


def admin_create_role(**kwargs) -> tuple:
    payload = kwargs.get('payload')
    try:
        tz = pytz.timezone('America/Vancouver')
        current_dt = datetime.now(tz)
        user_role = UserRole(payload.get('role_name'),
                             kwargs.get('requested_user_guid'),
                             current_dt,
                             current_dt)
        db.session.add(user_role)
        db.session.commit()
        user_role_schema = UserRoleSchema(many=False)
        kwargs['response'] = make_response(user_role_schema.jsonify(user_role), 201)
    except Exception as e:
        logging.warning(str(e))
        return False, kwargs
    return True, kwargs


def has_permission_to_view_all_users(**kwargs) -> tuple:
    required_permission = 'get-all-users'
    permissions = kwargs.get('permissions')
    user_roles = kwargs.get('user_roles')
    for role in user_roles:
        if required_permission in permissions[role['role_name']]['permissions']:
            return True, kwargs
    return False, kwargs


