from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.BlogPaginatorView.as_view(), name='index'),
    url(r'^page/(?P<page>[0-9]+)$', views.BlogPaginatorView.as_view(), name='paginator'),
    url(r'^tags/(?P<tag_id>[0-9]+)/page/(?P<page>[0-9]+)$', views.BlogPaginatorView.as_view(), name='tags'),
    url(r'^(?P<pk>[0-9]+)$', views.BlogDetailView.as_view(), name='detail'),
    url(r'^comment/(?P<pk>[0-9]+)/$', views.BlogCommentRedirectView.as_view(), name='blog_redirect'),
]
