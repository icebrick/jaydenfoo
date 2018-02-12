#!/usr/bin/env python
# encoding:utf-8
from django.shortcuts import get_object_or_404
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Tag, Article
from .forms import CommentForm
#hitcount通用视图
from hitcount.views import HitCountDetailView


class BlogPaginatorView(generic.ListView):
    '''文章列表分页视图'''

    template_name='blog/blog_paginator.html'
    context_object_name = 'article_paginator_list'

    def get_queryset(self):
        # 使用标签分类文章
        if 'tag_id' in self.kwargs:
            self.tag = get_object_or_404(Tag, id=self.kwargs['tag_id'])
            article_list = self.tag.article_set.order_by('-pub_date')
        else:
            article_list = Article.objects.order_by('-pub_date')

        # 每页显示10篇文章
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
        context = super().get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        if 'tag_id' in self.kwargs:
            context['this_tag'] = self.tag
        return context

class BlogDetailView(HitCountDetailView):
    '''文章详细展示页视图'''

    model = Article
    template_name = 'blog/blog_detail.html'
    context_object_name = 'this_article'
    count_hit = True # 打开统计点击数功能

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['tag_list'] = Tag.objects.all()
        self.article = get_object_or_404(Article, id=self.kwargs['pk'])
        context['comment_list'] = self.article.comment_set.all()
        return context

class BlogCommentRedirectView(generic.base.RedirectView):
    '''文章评论重定向试图．
    　　提交评论时，将评论和当前文章关联，保存评论，
    　　使用重定向刷新文章页面．
    　　'''
    # TODO: 使用Ajax实现该功能

    permanent = False
    pattern_name = 'blog:detail' # 重定向的目标地址

    def get_redirect_url(self, *args, **kwargs):
        if self.request.method == 'POST':
            this_article = get_object_or_404(Article, pk=kwargs['pk'])
            form = CommentForm(self.request.POST)
            if form.is_valid():
                form_clean = CommentForm(form.cleaned_data)
                new_comment = form_clean.save(commit = False)
                new_comment.article = this_article
                new_comment.save()
        return super().get_redirect_url(*args, **kwargs)

