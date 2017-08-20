#!/usr/bin/env python
# encoding: utf-8

from django import forms
from .models import ScheduleItem

class ScheduleItemForm(forms.ModelForm):
    class Meta:
        model = ScheduleItem
        fields = ['content', 'deadline', 'user', 'finish']

