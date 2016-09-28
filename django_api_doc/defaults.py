# -*- coding: utf-8 -*-

from django.conf import settings

ignore_namespaces = ()

API_DOC_IGNORE_NAMESPACES = getattr(settings, 'API_DOC_IGNORE_NAMESPACES', ignore_namespaces)

api_doc_title = 'Welcome to Django API Document'

API_DOC_TITLE = getattr(settings, 'API_DOC_TITLE', api_doc_title)



