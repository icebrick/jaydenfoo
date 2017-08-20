#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import url

from . import views

urlpatterns = [
       url(r'^$', views.AlbumIndexView.as_view(), name='index'),
       url(r'^demo$', views.AlbumDemoView, name='demo'),
       url(r'^(?P<album_e_name>[0-9a-zA-Z]+)$', views.AlbumDetailView.as_view(), name='detail'),
        ]
