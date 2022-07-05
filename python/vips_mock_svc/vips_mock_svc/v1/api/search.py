# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from python.vips_mock_svc.vips_mock_svc.v1.api import require_basic_authentication
from python.vips_mock_svc.vips_mock_svc.helper import load_json_into_dict

from flask import request, g
import os

from . import Resource
from .. import schemas


class Search(Resource):

    @require_basic_authentication
    def get(self, correlationId):
        noticeNo = request.args.get("noticeNo")
        data = self.get_json_data("prohibitions")
        # TODO - ask NTT: it's not clear from the documentation whether the search endpoints
        #  queries for prohibitions or impoundments or both
        # TODO - verify with NTT "noticeNo" is the same thing as "prohibitionNoticeNo"
        #  suggest changing the URL parameter so there's no confusion
        for key, value in data.items():
            if "prohibitionNoticeNo" not in value['result']:
                continue
            if value['result']['prohibitionNoticeNo'] == noticeNo:
                return {
                        "impoundmentId": "000",
                        "prohibitionId": value['result']['prohibitionNoticeNo']
                       }, 200
        return {"message": "not found"}, 404
