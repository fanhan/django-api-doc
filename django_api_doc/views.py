# -*- coding: utf-8 -*-

import markdown
import re

from django.views.generic import View
from django.shortcuts import render
from django.core import urlresolvers
from django.core.urlresolvers import RegexURLPattern, reverse
from django.http import Http404
from django.utils.encoding import smart_unicode

from .utils import resolve_urls


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
        url_patterns = urlresolvers.get_resolver().url_patterns
        for url_pattern in url_patterns:
            if not hasattr(url_pattern, 'name') and not hasattr(url_pattern, 'namespace'):
                continue

            if hasattr(url_pattern, 'namespace'):
                space_url = url_pattern.regex.pattern.replace('^', '/')
                if space_url == doc_base_url:
                    continue

            if hasattr(url_pattern, 'name') and url_pattern.name:
                data['url_names'].append(url_pattern.name)
            elif hasattr(url_pattern, 'namespace') and url_pattern.namespace:
                url_names = resolve_urls(
                    url_pattern.urlconf_module.urlpatterns,
                    prefix=url_pattern.namespace,
                    with_name=True
                )
                data['url_namespaces'].append({
                    'name': url_pattern.namespace,
                    'url_names': [{'key': k, 'name': v} for k, v in url_names.iteritems()]
                })

        if url_path:
            url_pattern_dict = resolve_urls(url_patterns)
            url_pattern = url_pattern_dict.get(url_path)
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