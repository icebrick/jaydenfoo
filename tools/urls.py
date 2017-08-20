from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ToolsIndexView, name='index'),
    url(r'^tempo$', views.ToolsTempoView, name='tempo'),
    url(r'^weather$', views.ToolsWeatherView, name='weather'),
    url(r'^weather-statistics$', views.ToolsWeatherStatistics, name='weather_statistics'),
    url(r'^weather-get-data$', views.ToolsWeatherGetDataView, name='weather_get_data'),
    url(r'^weather-get-data-timely$', views.WeatherGetDataTimelyView, name='tools_weather_get_data_timely'),
    url(r'^schedule$', views.ScheduleView, name='schedule'),
]
