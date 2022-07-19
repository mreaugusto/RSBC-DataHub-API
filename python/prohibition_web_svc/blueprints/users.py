from python.prohibition_web_svc.config import Config
from python.common.helper import middle_logic
import python.prohibition_web_svc.business.keycloak_logic as keycloak_logic
import python.prohibition_web_svc.http_responses as http_responses
import python.prohibition_web_svc.middleware.splunk_middleware as splunk_middleware
import python.common.splunk as splunk
from flask import request, Blueprint, make_response, jsonify
from flask_cors import CORS
import logging.config
import python.prohibition_web_svc.middleware.user_middleware as user_middleware


logging.config.dictConfig(Config.LOGGING)
logging.info('*** users blueprint loaded ***')

bp = Blueprint('users', __name__, url_prefix=Config.URL_PREFIX + '/api/v1')
CORS(bp, resources={Config.URL_PREFIX + "/api/v1/users*": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})


@bp.route('/users', methods=['GET'])
def index():
    """
    Get current user's details
    """
    if request.method == 'GET':
        kwargs = middle_logic(
            keycloak_logic.get_keycloak_user() + [
                {"try": splunk_middleware.get_user, "fail": []},
                {"try": splunk.log_to_splunk, "fail": []},
                {"try": user_middleware.get_user, "fail": [
                    {"try": http_responses.record_not_found, "fail": []}
                ]}
            ],
            request=request,
            config=Config)
        return kwargs.get('response')


@bp.route('/users', methods=['POST'])
def create():
    """
    DEPRECATED - New users no longer apply by creating a user record
    """
    if request.method == 'POST':
        return make_response({"error": "method not implemented"}, 405)


@bp.route('/users/<string:user_guid>', methods=['GET'])
def get(user_guid):
    if request.method == 'GET':
        return make_response({"error": "method not implemented"}, 405)


@bp.route('/users/<string:user_guid>', methods=['PATCH'])
def update(user_guid):
    if request.method == 'PATCH':
        return make_response({"error": "method not implemented"}, 405)


@bp.route('/users/<string:user_guid>', methods=['DELETE'])
def delete(user_guid):
    if request.method == 'DELETE':
        return make_response({"error": "method not implemented"}, 405)

