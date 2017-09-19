from django.contrib import admin
from .models import Weather, WeatherNow, WeatherForecast, ScheduleItem

# Register your models here.
class WeatherForecastInline(admin.StackedInline):
    model = WeatherForecast
    fieldsets = [('general', {'fields': ['fc_date', 'fc_tmp_max', 'fc_tmp_min'], 'classes':['collapse',]})]

class WeatherAdmin(admin.ModelAdmin):
    readonly_fields=('city', 'city_id', 'updata_time', 'aqi', 'pm25', 'tmp', 'condition', 'pcpn', 'vis', 'wind_direction', 'wind_speed', 'humidity')

class WeatherNowAdmin(admin.ModelAdmin):
    fieldsets = [('basic', {'fields': ['city', 'update_loc']}),
                 ('now', {'fields': ['cond_txt', 'tmp', 'wind_dir', 'wind_spd'], 'classes': ['collapse',]}),
                 ('aqi', {'fields': ['aqi_index', 'aqi_qlty'], 'classes': ['collapse',]})]
    inlines = [WeatherForecastInline,]
    list_display = ('city', 'update_loc')

class WeatherForecastAdmin(admin.ModelAdmin):
    list_display = ('fc_city', 'fc_date',)

admin.site.register(Weather, WeatherAdmin)
admin.site.register(WeatherNow, WeatherNowAdmin)
admin.site.register(WeatherForecast, WeatherForecastAdmin)
admin.site.register(ScheduleItem)
