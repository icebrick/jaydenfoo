#!/usr/bin/env python
# encoding:utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail

from .models import Tag, Article, Comment, Name
from .forms import CommentForm

#hitcount通用视图
from hitcount.views import HitCountDetailView

# Create your views here.
# 网站的首页
def IndexView(request):
    return render(request, 'index.html')

class BlogIndexView(generic.ListView):
    template_name = 'blog/blog_index.html'
    context_object_name = 'latest_article_list'

    def get_queryset(self):
        return Article.objects.order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super(BlogIndexView, self).get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        return context

class BlogPaginatorView(generic.ListView):
    template_name='blog/blog_paginator.html'
    context_object_name = 'article_paginator_list'

    def get_queryset(self):
        if 'tag_id' in self.kwargs:
            self.tag = get_object_or_404(Tag, id=self.kwargs['tag_id'])
            article_list = self.tag.article_set.order_by('-pub_date')
        else:
            article_list = Article.objects.order_by('-pub_date')

        paginator = Paginator(article_list, 10)
        page = self.kwargs.get('page', 1)

        try:
            article_paginated = paginator.page(page)
        except PageNotAnInteger:
            article_paginated = paginator.page(1)
        except EmptyPage:
            article_paginated = paginator.page(paginator.num_pages)
        return article_paginated

    def get_context_data(self, **kwargs):
        context = super(BlogPaginatorView, self).get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        if 'tag_id' in self.kwargs:
            context['this_tag'] = self.tag
        return context

class BlogDetailView(HitCountDetailView):
    model = Article
    template_name = 'blog/blog_detail.html'
    context_object_name = 'this_article'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['tag_list'] = Tag.objects.all()
        self.article = get_object_or_404(Article, id=self.kwargs['pk'])
        context['comment_list'] = self.article.comment_set.all()
        return context

class BlogCommentRedirectView(generic.base.RedirectView):
    permanent = False
    pattern_name = 'blog:detail'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.method == 'POST':
            this_article = get_object_or_404(Article, pk=kwargs['pk'])
            form = CommentForm(self.request.POST)
            if form.is_valid():
                form_clean = CommentForm(form.cleaned_data)
                new_comment = form_clean.save(commit = False)
                new_comment.article = this_article
                new_comment.save()
        return super(BlogCommentRedirectView, self).get_redirect_url(*args, **kwargs)

