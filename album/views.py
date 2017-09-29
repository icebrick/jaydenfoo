# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404

from .models import Album, Photo
from hitcount.views import HitCountDetailView
# Create your views here.

#相册的首页
class AlbumIndexView(generic.ListView):
    template_name = 'album/album_index.html'
    context_object_name = 'album_list'

    def get_queryset(self):
        return Album.objects.order_by('-established_date')

class AlbumDetailView(HitCountDetailView):
    model = Album
    template_name = 'album/album_detail.html'
    context_object_name = 'this_album'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(AlbumDetailView, self).get_context_data(**kwargs)
        context['this_album'] = get_object_or_404(Album, id=self.kwargs['pk'])
        return context
    # def get_queryset(self):
    #     this_album = get_object_or_404(Album, e_name=self.kwargs['album_e_name'])
    #     return this_album
    #
    # model = Article
    # template_name = 'blog/blog_detail.html'
    # context_object_name = 'this_article'
    # count_hit = True
    #
    # def get_context_data(self, **kwargs):
    #     context = super(BlogDetailView, self).get_context_data(**kwargs)
    #     context['form'] = CommentForm()
    #     context['tag_list'] = Tag.objects.all()
    #     self.article = get_object_or_404(Article, id=self.kwargs['pk'])
    #     context['comment_list'] = self.article.comment_set.all()
    #     return context
def AlbumDemoView(request):
    return render(request, 'album/album_demo.html')
