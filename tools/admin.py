from django.contrib import admin
from .models import Weather, ScheduleItem

# Register your models here.
class WeatherAdmin(admin.ModelAdmin):
    readonly_fields=('city', 'city_id', 'updata_time', 'aqi', 'pm25', 'tmp', 'condition', 'pcpn', 'vis', 'wind_direction', 'wind_speed', 'humidity')
admin.site.register(Weather, WeatherAdmin)
admin.site.register(ScheduleItem)
