from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.tools_index_view, name='index'),
    url(r'^tempo$', views.tools_tempo_view, name='tempo'),
    url(r'^weather$', views.tools_weather_view, name='weather'),
    url(r'^weather-statistics$', views.tools_weather_statistics, name='weather_statistics'),
    url(r'^schedule$', views.schedule_view, name='schedule'),
]
