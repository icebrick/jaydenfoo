from django.db import models

# Create your models here.
class WechatData(models.Model):
    test = models.TextField(max_length=99999)
