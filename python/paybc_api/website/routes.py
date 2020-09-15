from flask import Blueprint, request, jsonify, make_response
from python.paybc_api.website.oauth2 import authorization, require_oauth
import python.common.helper as helper
import python.common.business as rules
from python.paybc_api.website.config import Config
import logging
import json
from datetime import datetime


logging.basicConfig(level=Config.LOG_LEVEL)
logging.warning('*** Pay BC API initialized ***')
bp = Blueprint(__name__, 'home')


@bp.route('/oauth/token', methods=['POST'])
def issue_token():
    return authorization.create_token_response()


@bp.route('/oauth/revoke', methods=['POST'])
def revoke_token():
    return authorization.create_endpoint_response('revocation')


@bp.route('/api_v2/search', methods=['GET'])
@require_oauth()
def search():
    """
    On the Pay_BC site, a user lookups an prohibition_number (invoice) to be paid.
    PayBC searches for the invoice in our system using a GET request with an
    invoice number and a check_value.  We return an array of items to be paid.
    """
    if request.method == 'GET':
        # invoke middleware business logic
        prohibition_number = request.args.get('invoice_number')
        driver_last_name = request.args.get('check_value')
        logging.info('inputs: {}, {}'.format(prohibition_number, driver_last_name))
        args = helper.middle_logic(
            rules.ready_for_payment(),
            config=Config,
            prohibition_number=prohibition_number,
            driver_last_name=driver_last_name)
        if 'error_string' not in args:
            # TODO - http replaced with https for local development - REMOVE BEFORE FLIGHT!
            host_url = request.host_url.replace('http', 'https')
            return jsonify({
                "items": [{"selected_invoice": {
                       "$ref": host_url + 'api_v2/invoice/' + args.get('prohibition_number')}
                    }
                ]
            })
        return jsonify({"error": args.get('error_string')})


@bp.route('/api_v2/invoice/<prohibition_number>', methods=['GET'])
@require_oauth()
def show(prohibition_number):
    """
    PayBC requests details on the item to be paid from this endpoint.
    """
    if request.method == 'GET':
        # invoke middleware business logic
        args = helper.middle_logic(rules.ready_for_invoicing(),
                                   prohibition_number=prohibition_number,
                                   config=Config)
        if 'error_string' not in args:
            presentation_type = args.get('presentation_type')
            amount_due = args.get('amount_due')
            service_date = args.get('service_date')
            return jsonify(dict({
                "invoice_number": args.get('prohibition_number'),
                "pbc_ref_number": "10008",
                "party_number": 0,
                "party_name": "RSI",
                "account_number": "0",
                "site_number": "0",
                "cust_trx_type": "Review Notice of Driving Prohibition",
                "term_due_date": service_date.isoformat(),
                "total": amount_due,
                "amount_due": amount_due,
                "attribute1": args.get('vips_data')['noticeTypeCd'],
                "attribute2": service_date.strftime("%b %-d, %Y"),
                "attribute3": presentation_type,
                "amount": amount_due
            }))
        return make_response({"error": args.get('error_string')}, 404)


@bp.route('/api_v2/receipt', methods=['POST'])
@require_oauth()
def receipt():
    """
    After PayBC verifies that the payment has been approved, it submits
    a list of invoices that have been paid (a user can pay multiple
    payments simultaneously), we'll notify VIPS of the payment and
    return the following to show that the receipt has been received.
    """
    if request.method == 'POST':
        payload = request.json
        # invoke middleware business logic
        logging.info('receipt payload: {}'.format(json.dumps(payload)))
        args = helper.middle_logic(rules.generate_pay_bc_receipt(),
                                   payload=payload,
                                   config=Config)

        if not args.get('payment_success'):
            # TODO - set the http response code from middleware
            return make_response(dict({"status": "INCMP"}), 400)

        return jsonify(dict({
            "status": "APP",
            "receipt_number": payload['receipt_number'],
            "receipt_date ": payload['receipt_date'],
            "receipt_amount": payload['receipt_amount']
        }))





