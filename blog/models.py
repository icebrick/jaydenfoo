from django.db import models
# from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField

from DjangoUeditor.models import UEditorField

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    count_post = models.IntegerField(default=0, editable=False)
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date publishded')
    abstract = models.CharField(max_length=2000, blank=True)
    # content = RichTextUploadingField()
    content = UEditorField(u'content    ', width=600, height=300, toolbars="full", imagePath="blog/article_image/", filePath="blog/article_file/", upload_settings={"imageMaxSize":1204000}, settings={}, command=None, blank=True)
    count_hit = models.IntegerField(default=0, editable=False)
    tags = models.ManyToManyField(Tag, blank=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('blog.views.BlogDetailView', args=[str(self.id)])

class Comment(models.Model):
    nick_name = models.CharField(max_length=10)
    content = models.CharField(max_length=2000)
    pub_date = models.DateTimeField(auto_now=True)
    article  = models.ForeignKey(Article, null=True)
    def __str__(self):
        return self.nick_name

class Name(models.Model):
    name = models.CharField(max_length=5)
    def __str__(self):
        return self.name
