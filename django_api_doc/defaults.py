# -*- coding: utf-8 -*-

from django.conf import settings

ignore_namespaces = ()

API_DOC_IGNORE_NAMESPACES = getattr(settings, 'API_DOC_IGNORE_NAMESPACES', ignore_namespaces)


