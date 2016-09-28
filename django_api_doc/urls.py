# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.APIDocView.as_view(), name='api_doc'),
    url(r'^menu/$', views.MenuView.as_view(), name='menu'),
    url(r'^(?P<url_name>.+)/', views.DocContentView.as_view(), name='doc_content'),
]