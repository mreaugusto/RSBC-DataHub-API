# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas


class DocumentDocumentidCorrelationid(Resource):

    def get(self, documentId, correlationId):
        print(g.args)

        return None, 200, None