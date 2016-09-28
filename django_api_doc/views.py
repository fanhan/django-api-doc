# -*- coding: utf-8 -*-

import re
import json

from django.views.generic import View
from django.shortcuts import render
from django.core import urlresolvers
from django.core.urlresolvers import RegexURLPattern, reverse
from django.http import Http404, HttpResponse

from django_api_doc.utils import resolve_urls, get_url_pattern_by_name
from django_api_doc import defaults as settings


class APIDocView(View):
    template_name = 'django_api_doc/docs.html'

    def get(self, request):
        return render(request, self.template_name, {})


class MenuView(View):
    """
    Api doc menu
    """

    def get(self, request):
        """
        api doc menu

        #### returns
            {
                "url_namespaces": [
                    {
                        "url_names": [
                            {
                                "key": "url_namespace_name-url_name",
                                "name": "url_name"
                            }
                        ],
                        "name": "url_namespace_name"
                    }
                ],
                "url_names": [
                    {
                        "key": "url_name",
                        "name": "url_name",
                    }
                ]
            }
        """
        doc_base_url = request.get_full_path().replace('menu/', '')
        data = {
            'url_namespaces': [],
            'url_names': [],
            'doc_title': settings.API_DOC_TITLE,
        }

        # get all name and namespace by url conf
        url_patterns = urlresolvers.get_resolver().url_patterns
        for url_pattern in url_patterns:
            if hasattr(url_pattern, 'name') and url_pattern.name:
                data['url_names'].append({
                    'key': url_pattern.name,
                    'name': url_pattern.name
                })
            elif hasattr(url_pattern, 'namespace') and url_pattern.namespace:
                # if namespace in ignore namespaces setting
                if url_pattern.namespace in settings.API_DOC_IGNORE_NAMESPACES:
                    continue

                # if namespace is api_doc's namespace
                space_url = url_pattern.regex.pattern.replace('^', '/')
                if space_url == doc_base_url:
                    continue

                url_names = resolve_urls(
                    url_pattern.urlconf_module.urlpatterns,
                    prefix=url_pattern.namespace,
                )
                data['url_namespaces'].append({
                    'name': url_pattern.namespace,
                    'url_names': url_names
                })
        return HttpResponse(content=json.dumps(data), content_type='application/json')


class DocContentView(View):
    """
    api doc content
    """
    def get(self, request, url_name):
        """
        api doc content

        #### return

            {
                "title": "test",
                "url": "/test/",
                "items": [
                    {
                        "method": "POST",
                        "content": "test"
                    }
                ]
            }
        """
        url_patterns = urlresolvers.get_resolver().url_patterns
        url_pattern = get_url_pattern_by_name(url_patterns, url_name)
        if not isinstance(url_pattern, RegexURLPattern):
            raise Http404

        view = url_pattern.callback.view_class
        items = []
        for method in view.http_method_names:
            if method == 'options' or not hasattr(view, method):
                continue

            doc_item = []
            for i in getattr(view, method).__doc__.split('\n'):
                doc_item.append(i[8:])

            doc_content = '\n'.join(doc_item)
            items.append({
                'method': method.upper(),
                'content': doc_content,
            })

        try:
            url = reverse(url_name.replace('--', ':'))
        except Exception, e:
            ret = re.findall('(?:pattern\(s\) tried: \[)(.+)(?:\])', e.__str__())
            if ret:
                url = ret[0]
            else:
                url = url_pattern.regex.pattern

        doc_content = {
            'title': view.__doc__ if view.__doc__ else view.__name__,
            'url': url,
            'items': items,
        }
        return HttpResponse(content=json.dumps(doc_content), content_type='application/json')


