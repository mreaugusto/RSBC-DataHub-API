# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.impoundments_correlationId import ImpoundmentsCorrelationid
from .api.impoundments_impoundmentId_correlationId import ImpoundmentsImpoundmentidCorrelationid
from .api.search_correlationId import SearchCorrelationid
from .api.prohibitions_correlationId import ProhibitionsCorrelationid
from .api.prohibitions_prohibitionId_correlationId import ProhibitionsProhibitionidCorrelationid
from .api.document_correlationId import DocumentCorrelationid
from .api.document_documentId_correlationId import DocumentDocumentidCorrelationid
from .api.documents_correlationId import DocumentsCorrelationid
from .api.document_association_notice_documentId_correlationId import DocumentAssociationNoticeDocumentidCorrelationid
from .api.dfDocument_dfId_correlationId import DfdocumentDfidCorrelationid
from .api.configuration_correlationId import ConfigurationCorrelationid


routes = [
    dict(resource=ImpoundmentsCorrelationid, urls=['/impoundments/<correlationId>'], endpoint='impoundments_correlationId'),
    dict(resource=ImpoundmentsImpoundmentidCorrelationid, urls=['/impoundments/<impoundmentId>/<correlationId>'], endpoint='impoundments_impoundmentId_correlationId'),
    dict(resource=SearchCorrelationid, urls=['/search/<correlationId>'], endpoint='search_correlationId'),
    dict(resource=ProhibitionsCorrelationid, urls=['/prohibitions/<correlationId>'], endpoint='prohibitions_correlationId'),
    dict(resource=ProhibitionsProhibitionidCorrelationid, urls=['/prohibitions/<prohibitionId>/<correlationId>'], endpoint='prohibitions_prohibitionId_correlationId'),
    dict(resource=DocumentCorrelationid, urls=['/document/<correlationId>'], endpoint='document_correlationId'),
    dict(resource=DocumentDocumentidCorrelationid, urls=['/document/<documentId>/<correlationId>'], endpoint='document_documentId_correlationId'),
    dict(resource=DocumentsCorrelationid, urls=['/documents/<correlationId>'], endpoint='documents_correlationId'),
    dict(resource=DocumentAssociationNoticeDocumentidCorrelationid, urls=['/document/association/notice/<documentId>/<correlationId>'], endpoint='document_association_notice_documentId_correlationId'),
    dict(resource=DfdocumentDfidCorrelationid, urls=['/dfDocument/<dfId>/<correlationId>'], endpoint='dfDocument_dfId_correlationId'),
    dict(resource=ConfigurationCorrelationid, urls=['/configuration/<correlationId>'], endpoint='configuration_correlationId'),
]