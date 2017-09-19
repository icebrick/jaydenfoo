#-*- coding: utf-8 -*-
from django.db import models

# Create your models here.
# 自定义动态路径名，如果upload_to参数是可调用的，则调用的函数会覆盖默认的generate_filename函数
def generate_filename(self, filename):
    url = 'album/%s/%s' %(self.album.e_name, filename)
    return url

class Album(models.Model):
    name = models.CharField(max_length=200, unique=True)
    e_name = models.CharField(max_length=200, unique=True)
    desc = models.TextField(blank=True)
    established_date = models.DateTimeField(auto_now_add=True, verbose_name='Establish Date')
    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

class Photo(models.Model):
    name = models.CharField(max_length=200, blank=True)
    desc = models.TextField(blank=True)
    album = models.ForeignKey(Album)
    image = models.ImageField(upload_to=generate_filename)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Publish Date')
    as_cover = models.BooleanField(default=False)

