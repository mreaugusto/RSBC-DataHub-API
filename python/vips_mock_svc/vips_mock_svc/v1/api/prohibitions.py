# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from python.vips_mock_svc.vips_mock_svc.v1.api import require_basic_authentication, validate
from python.vips_mock_svc.vips_mock_svc.validation_schema import prohibition

from . import Resource


class Prohibitions(Resource):

    @require_basic_authentication
    def get(self, prohibitionId, correlationId):
        data = self.get_json_data("prohibitions")
        if prohibitionId in data:
            return data[prohibitionId], 200
        else:
            return {"message": "not found"}, 404

    @require_basic_authentication
    @validate(prohibition)
    def post(self, correlationId):
        # TODO - verify with NTT that the swagger doc should have a 200 and 201 response in the POST method
        return {"vipsProhibitionId": 0, "dfId": 0, "respMsg": "string"}, 201
