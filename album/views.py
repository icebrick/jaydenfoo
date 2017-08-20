# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404

from .models import Album, Photo
# Create your views here.

#相册的首页
class AlbumIndexView(generic.ListView):
    template_name = 'album/album_index.html'
    context_object_name = 'album_list'

    def get_queryset(self):
        return Album.objects.order_by('-estblished_date')

class AlbumDetailView(generic.ListView):
    template_name = 'album/album_detail.html'
    context_object_name = 'this_album'

    def get_queryset(self):
        this_album = get_object_or_404(Album, e_name=self.kwargs['album_e_name'])
        return this_album

def AlbumDemoView(request):
    return render(request, 'album/album_demo.html')
