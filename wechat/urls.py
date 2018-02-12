#!/usr/bin/env python
# encoding: utf-8
from django.conf.urls import *

from . import views


urlpatterns = [
        url(r'^$', views.WechatIndexView, name='index' ),
        url(r'^test$', views.WechatTestView, name='test'),
        ]
