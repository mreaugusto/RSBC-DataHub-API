import python.prohibition_web_svc.middleware.keycloak_middleware as keycloak_middleware
from python.prohibition_web_svc.config import Config
import python.prohibition_web_svc.middleware.splunk_middleware as splunk_middleware
import python.common.splunk as splunk
import python.common.helper as helper
from flask import request, Blueprint, make_response
from flask_cors import CORS
import logging.config
import python.prohibition_web_svc.business.keycloak_logic as keycloak_logic
import python.prohibition_web_svc.http_responses as http_responses
import python.prohibition_web_svc.middleware.user_middleware as user_middleware
import python.prohibition_web_svc.middleware.form_middleware as form_middleware
import python.prohibition_web_svc.data.validation_schemas as validation_schemas


logging.config.dictConfig(Config.LOGGING)
logging.info('*** agency users blueprint loaded ***')

bp = Blueprint('agency_users', __name__, url_prefix=Config.URL_PREFIX + '/api/v1')
CORS(bp, resources={Config.URL_PREFIX + "/api/v1/agency/*": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})


@bp.route('/agency/<business_guid>/users', methods=['GET'])
def index(business_guid):
    """
    If the requesting user has the role of "agency_admin" return all users
    with the same buisness_guid as the requesting user
    """
    if request.method == 'GET':
        kwargs = helper.middle_logic(
            keycloak_logic.get_authorized_keycloak_user() + [
                {"try": keycloak_middleware.url_business_guid_matches_business_guid_in_token, "fail": [
                    {"try": http_responses.cannot_access_users_at_another_agency, "fail": []},
                ]},
                {"try": user_middleware.query_all_agency_users, "fail": [
                    {"try": http_responses.server_error_response, "fail": []},
                ]},
                {"try": splunk_middleware.get_users, "fail": []},
                {"try": splunk.log_to_splunk, "fail": []},
            ],
            url_business_guid=business_guid,
            required_permission='agency_admin_users-index',
            request=request,
            config=Config)
        return kwargs.get('response')


@bp.route('/agency/<business_guid>/users', methods=['POST'])
def create(business_guid):
    """
    Create a new user at agency
    """
    if request.method == 'POST':
        kwargs = helper.middle_logic(
            keycloak_logic.get_authorized_keycloak_user() + [
                {"try": keycloak_middleware.url_business_guid_matches_business_guid_in_token, "fail": [
                    {"try": http_responses.cannot_access_users_at_another_agency, "fail": []},
                ]},
                {"try": form_middleware.request_contains_a_payload, "fail": [
                    {"try": http_responses.payload_missing, "fail": []},
                ]},
                {"try": form_middleware.validate_payload, "fail": [
                    {"try": http_responses.failed_validation, "fail": []},
                ]},
                {"try": splunk_middleware.create_user, "fail": []},
                {"try": splunk.log_to_splunk, "fail": []},
                {"try": user_middleware.create_a_user, "fail": [
                    {"try": http_responses.server_error_response, "fail": []},
                ]},
                {"try": http_responses.successful_create_response, "fail": []},
            ],
            validation_schema=validation_schemas.agency_user_schema(),
            url_business_guid=business_guid,
            required_permission='agency_admin_users-create',
            request=request,
            config=Config)
        return kwargs.get('response')


@bp.route('/agency/<business_guid>/users/<string:user_guid>', methods=['PATCH'])
def update(business_guid, user_guid):
    if request.method == 'PATCH':
        kwargs = helper.middle_logic(
            keycloak_logic.get_authorized_keycloak_user() + [

                {"try": keycloak_middleware.url_business_guid_matches_business_guid_in_token, "fail": [
                    {"try": http_responses.cannot_access_users_at_another_agency, "fail": []},
                ]},
                {"try": user_middleware.user_belongs_to_business, "fail": [
                    {"try": http_responses.cannot_access_users_at_another_agency, "fail": []},
                ]},
                {"try": form_middleware.request_contains_a_payload, "fail": [
                    {"try": http_responses.payload_missing, "fail": []},
                ]},
                {"try": form_middleware.validate_payload, "fail": [
                    {"try": http_responses.failed_validation, "fail": []},
                ]},
                {"try": user_middleware.payload_user_matches_url_user_guid, "fail": [
                    {"try": http_responses.cannot_change_user_guid, "fail": []},
                ]},
                {"try": user_middleware.payload_business_guid_matches_url_business_guid, "fail": [
                    {"try": http_responses.cannot_change_business_guid, "fail": []},
                ]},
                {"try": splunk_middleware.update_user, "fail": []},
                {"try": splunk.log_to_splunk, "fail": []},
                {"try": user_middleware.update_the_user, "fail": [
                    {"try": http_responses.server_error_response, "fail": []},
                ]},
                {"try": http_responses.successful_update_response, "fail": []},
            ],
            validation_schema=validation_schemas.agency_user_schema(),
            url_user_guid=user_guid,
            url_business_guid=business_guid,
            required_permission='agency_admin_users-update',
            request=request,
            config=Config)
        return kwargs.get('response')


@bp.route('/agency/<business_guid>/users/<string:user_guid>', methods=['DELETE'])
def delete(business_guid, user_guid):
    if request.method == 'DELETE':
        kwargs = helper.middle_logic(
            keycloak_logic.get_authorized_keycloak_user() + [
                {"try": keycloak_middleware.url_business_guid_matches_business_guid_in_token, "fail": [
                    {"try": http_responses.cannot_access_users_at_another_agency, "fail": []},
                ]},
                {"try": user_middleware.user_belongs_to_business, "fail": [
                    {"try": http_responses.cannot_access_users_at_another_agency, "fail": []},
                ]},
                {"try": splunk_middleware.delete_user, "fail": []},
                {"try": splunk.log_to_splunk, "fail": []},

                {"try": user_middleware.delete_a_user, "fail": [
                    {"try": http_responses.server_error_response, "fail": []},
                ]},
                {"try": http_responses.successful_update_response, "fail": []},
            ],
            validation_schema=validation_schemas.agency_user_schema(),
            url_user_guid=user_guid,
            url_business_guid=business_guid,
            required_permission='agency_admin_users-delete',
            request=request,
            config=Config)
        return kwargs.get('response')


@bp.route('/agency/<business_guid>/users/<string:user_guid>', methods=['GET'])
def get(business_guid, user_guid):
    if request.method == 'GET':
        return make_response({"error": "method not implemented"}, 405)

