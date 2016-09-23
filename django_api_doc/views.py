# -*- coding: utf-8 -*-

import markdown
import re

from django.views.generic import View
from django.shortcuts import render
from django.core import urlresolvers
from django.core.urlresolvers import RegexURLPattern, reverse
from django.http import Http404
from django.utils.encoding import smart_unicode

from django_api_doc.utils import resolve_urls, get_url_pattern_by_name
from django_api_doc import defaults as settings


class APIDocView(View):
    template_name = 'django_api_doc/docs.html'

    def get(self, request, url_path=''):
        doc_base_url = request.get_full_path().strip(url_path)
        data = {
            'url_namespaces': [],
            'url_names': [],
            'doc_base_url': doc_base_url,
            'url_path': url_path,
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

        if url_path:
            url_pattern = get_url_pattern_by_name(url_patterns, url_path)
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
                content = markdown.markdown(smart_unicode(doc_content), ['tables', 'attr_list'])
                items.append({
                    'method': method.upper(),
                    'content': content,
                })

            try:
                url = reverse(url_path.replace('-', ':'))
            except Exception, e:
                ret = re.findall('(?:pattern\(s\) tried: \[)(.+)(?:\])', e.__str__())
                if ret:
                    url = ret[0]
                else:
                    url = url_pattern.regex.pattern

            data['doc'] = {
                'title': view.__doc__ if view.__doc__ else view.__name__,
                'url': url,
                'items': items,
            }
        return render(request, self.template_name, data)