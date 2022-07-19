from python.prohibition_web_svc.config import Config
from python.prohibition_web_svc.business.keycloak_logic import get_authorized_keycloak_user
from flask import make_response, jsonify
import python.prohibition_web_svc.http_responses as http_responses
from python.common.helper import middle_logic
from flask import request, Blueprint
from flask_cors import CORS
import logging.config

logging.config.dictConfig(Config.LOGGING)
logging.info('*** bceid blueprint loaded ***')

bp = Blueprint('bceid', __name__, url_prefix=Config.URL_PREFIX + '/api/v1')
CORS(bp, resources={Config.URL_PREFIX + "/api/v1/bceid": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})


@bp.route('/bceid', methods=['GET'])
def get_users():
    if request.method == 'GET':
        kwargs = middle_logic(
            get_authorized_keycloak_user() + [
              {"try": _get_bceid_user, "fail": [
                  {"try": http_responses.record_not_found, "fail": []},
              ]},
            ],
            required_permission='bceid-get-users',
            request=request,
            config=Config)
        return kwargs.get('response')


def _get_bceid_user(**kwargs) -> tuple:
    request = kwargs.get('request')
    requested_username = request.args.get('username', '').lower()
    try:
        data = {
            "bsmith": {
                "first_name": "Bob",
                "last_name": "Smith",
                "badge_number": "8088",
                "business_guid": "AAAA-BBBB-CCCC-DDDD",
                "user_guid": "EEEE-FFFF-GGGG-HHHH",
                "agency": "RoadSafety"
            },
            "treed": {
                "first_name": "Tim",
                "last_name": "Reed",
                "badge_number": "1235",
                "business_guid": "AAAA-BBBB-CCCC-DDDD",
                "user_guid": "QQQQ-RRRR-TTTT-MMMM",
                "agency": "RoadSafety"
            },
            "cross": {
                "first_name": "Christine",
                "last_name": "Ross",
                "badge_number": "1111",
                "business_guid": "AAAA-BBBB-CCCC-DDDD",
                "user_guid": "SSSS-RRRR-HHHH-EEEE",
                "agency": "RoadSafety"
            }
        }
        kwargs['response'] = make_response(jsonify([data[requested_username]]), 200)
        return True, kwargs
    except Exception as e:
        logging.warning("error cannot find user {} ".format(requested_username))
        return False, kwargs

