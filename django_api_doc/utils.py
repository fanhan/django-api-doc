# -*- coding: utf-8 -*-


def resolve_urls(url_patterns, prefix='', with_name=False):
    """
    resolve url

    example: your urls.py like this

        url(r'^signup/$', views.SignupView.as_view(), name='signup'),
        url(r'^login/$', views.LoginView.as_view(), name='login'),
        url(r'^logout/$', views.LogoutView.as_view(), name='logout'),

        url(r'^accounts/', include('apps.account.urls', namespace='accounts')),

    :return: {
        'login': LoginView,
        'signup': SignupView,
        'logout': LogoutView,
        'account-user_info': UserInfoView,
        'account-like_user': LikeUserView,
    }
    """
    data = {}
    for url_pattern in url_patterns:
        if not hasattr(url_pattern, 'name') and not hasattr(url_pattern, 'namespace'):
            continue

        if hasattr(url_pattern, 'namespace') and url_pattern.namespace == 'django_api_doc':
            continue

        if hasattr(url_pattern, 'name') and url_pattern.name:
            key = '%s-%s' % (prefix, url_pattern.name) if prefix else url_pattern.name
            data[key] = url_pattern.name if with_name else url_pattern
        else:
            key = '%s-%s' % (prefix, url_pattern.namespace) if prefix else url_pattern.namespace
            data.update(resolve_urls(url_pattern.urlconf_module.urlpatterns, prefix=key, with_name=with_name))
    return data
