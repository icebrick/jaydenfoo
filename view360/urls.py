from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.TestView, name='test'),
]
