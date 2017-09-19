# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class WeatherNow(models.Model):
    # basic
    city = models.CharField(max_length=100)
    city_id = models.CharField('city id', max_length=100)
    update_loc = models.CharField('update time(local) from weather api', max_length=100)
    update_utc = models.CharField('update time(utc) from weather api', max_length=100)
    # now
    # 天气情况代码说明 https://www.heweather.com/documents/condition
    cond_code = models.CharField('weather condition code', max_length=100)
    cond_txt = models.CharField('weather condition text', max_length=100)
    fl = models.CharField('sendible temperature', max_length=100)
    hum = models.CharField('relative humidity', max_length=100)
    pcpn = models.CharField('precipitation', max_length=100)
    pres = models.CharField('pressure', max_length=100)
    tmp = models.CharField('temperature', max_length=100)
    vis = models.CharField('visibility', max_length=100)
    wind_deg = models.CharField('wind degree', max_length=100)
    wind_dir = models.CharField('wind direction', max_length=100)
    wind_sc = models.CharField('wind scale', max_length=100)
    wind_spd = models.CharField('wind speed', max_length=100)
    # aqi
    aqi_index = models.CharField(max_length=100)
    aqi_qlty = models.CharField(max_length=100)

    def __str__(self):
        return self.city+'  '+self.update_utc

class WeatherForecast(models.Model):
    fc_city = models.CharField('city name', max_length=100)
    fc_index = models.IntegerField()
    # 天文指数
    fc_mr = models.CharField('moon rise time', max_length=100)
    fc_ms = models.CharField('moon set time', max_length=100)
    fc_sr = models.CharField('sun rise time', max_length=100)
    fc_ss = models.CharField('sun set time', max_length=100)
    # condition
    fc_txt_d = models.CharField('day condition', max_length=100)
    fc_txt_n = models.CharField('night condition', max_length=100)
    # general
    fc_date = models.CharField(max_length=100)
    fc_hum = models.CharField('humidity', max_length=100)
    fc_pcpn = models.CharField('precipitation', max_length=100)
    fc_pop = models.CharField('precipitation optitunity', max_length=100)
    fc_pres = models.CharField('pressure', max_length=100)
    fc_uv = models.CharField('uv', max_length=100)
    fc_vis = models.CharField('visibility', max_length=100)
    # temperature
    fc_tmp_max = models.CharField('maximum temperature', max_length=100)
    fc_tmp_min = models.CharField('minimum temperature', max_length=100)
    # wind
    fc_wind_deg = models.CharField('wind degree', max_length=100)
    fc_wind_dir = models.CharField('wind direction', max_length=100)
    fc_wind_sc = models.CharField('wind scale', max_length=100)
    fc_wind_spd = models.CharField('wind speed', max_length=100)
    # forecast foreignkey
    weathernow = models.ForeignKey('WeatherNow', on_delete=models.CASCADE, )

    def __str__(self):
        return self.fc_date


class Weather(models.Model):
    city = models.CharField(max_length=200, editable=False)
    city_id = models.CharField(max_length=200, editable=False)
    updata_time = models.DateTimeField(auto_now=True, editable=False)
    aqi = models.IntegerField(verbose_name='空气质量指数', editable=False)
    pm25 = models.IntegerField(editable=False)
    tmp = models.IntegerField(verbose_name='温度', editable=False)
    condition = models.IntegerField(verbose_name='天气情况', editable=False)
    pcpn = models.IntegerField(verbose_name='降雨量mm')
    vis = models.IntegerField(verbose_name='能见度km')
    wind_direction = models.IntegerField(verbose_name='风向', editable=False)
    wind_speed = models.IntegerField(verbose_name='风速', editable=False)
    humidity = models.IntegerField(verbose_name='湿度', editable=False)

    def __str__(self):
        return self.city + '  ' + self.updata_time.strftime('%Y-%m-%d-%H-%M') + '   id=' + str(self.id)

class ScheduleItem(models.Model):
    content = models.TextField(max_length=500, verbose_name='计划内容')
    deadline = models.DateTimeField(verbose_name='截止时间')
    pub_date = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    finish = models.BooleanField(default=False)
    user = models.CharField(max_length=100)

    def __unicode__(self):
        return self.user
