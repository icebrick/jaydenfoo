from django.db import models
from DjangoUeditor.models import UEditorField
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class Tag(models.Model):
    '''文章标签'''
    name = models.CharField(max_length=10, unique=True) # 标签名称
    count_post = models.IntegerField(default=0, editable=False) # 包含该标签的文章

    def __str__(self):
        return self.name

class Article(models.Model):
    '''文章'''
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=10)
    pub_date = models.DateTimeField('date publishded')
    abstract = models.CharField(max_length=2000, blank=True)
    # content = UEditorField(u'content    ', width=600, height=300, toolbars="full", imagePath="blog/article_image/", filePath="blog/article_file/", upload_settings={"imageMaxSize":1204000}, settings={}, command=None, blank=True)
    content = MarkdownxField()
    count_hit = models.IntegerField(default=0, editable=False)
    tags = models.ManyToManyField(Tag, blank=True)

    @property
    def formatted_markdown(self):
        return markdownify(self.content)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('blog.views.BlogDetailView', args=[str(self.id)])

class Comment(models.Model):
    '''对文章的评论'''
    nick_name = models.CharField(max_length=10)
    content = models.CharField(max_length=2000)
    pub_date = models.DateTimeField(auto_now=True)
    article  = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.nick_name + ': ' + self.content[:10]
