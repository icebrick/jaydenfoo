#!/usr/bin/env python
# encoding: utf-8

from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import RegisterForm

def RegisterView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/tools/')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

