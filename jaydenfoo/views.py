#!/usr/bin/env python
# encoding: utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import RegisterForm


def RegisterView(request):
    '''注册视图'''
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/tools/')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
