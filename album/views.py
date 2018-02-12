# -*- coding:utf-8 -*-
from django.views import generic
from django.shortcuts import get_object_or_404

from .models import Album
from hitcount.views import HitCountDetailView


class AlbumIndexView(generic.ListView):
    '''相册首页视图'''
    template_name = 'album/album_index.html'
    context_object_name = 'album_list'

    def get_queryset(self):
        return Album.objects.order_by('-established_date')

class AlbumDetailView(HitCountDetailView):
    '''相册内图片展示视图'''
    model = Album
    template_name = 'album/album_detail.html'
    context_object_name = 'this_album'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['this_album'] = get_object_or_404(Album, id=self.kwargs['pk'])
        return context

