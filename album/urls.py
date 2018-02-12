#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import url

from . import views

urlpatterns = [
       url(r'^$', views.AlbumIndexView.as_view(), name='index'),
       url(r'^(?P<pk>\d+)$', views.AlbumDetailView.as_view(), name='detail'),
]
