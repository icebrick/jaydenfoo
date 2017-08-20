# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
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

    def __unicode__(self):
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
