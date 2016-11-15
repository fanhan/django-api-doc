# -*- coding: utf-8 -*-

from django.conf import settings

# api doc default settings
ignore_namespaces = ()
api_doc_title = 'Welcome to Django API Document'
api_doc_permission = ''


API_DOC_IGNORE_NAMESPACES = getattr(settings, 'API_DOC_IGNORE_NAMESPACES', ignore_namespaces)
API_DOC_TITLE = getattr(settings, 'API_DOC_TITLE', api_doc_title)
API_DOC_PERMISSION = getattr(settings, 'API_DOC_PERMISSION', api_doc_permission)
