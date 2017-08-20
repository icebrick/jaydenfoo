"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve

from django.conf import settings
from django.conf.urls.static import static
from blog import views as blog_views
from .views import RegisterView
urlpatterns = [
    url(r'^$', blog_views.IndexView),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^tools/', include('tools.urls', namespace='tools')),
    url(r'hitcount/', include('hitcount.urls', namespace='hitcount')),
    url(r'^album/', include('album.urls', namespace='album')),
    url(r'^register/$', RegisterView, name='register'),
    url(r'^wechat/', include('wechat.urls', namespace='wechat')),
    url(r'^view360/', include('view360.urls', namespace='view360')),



]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

