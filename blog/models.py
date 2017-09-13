from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
# Create your models here.

class Category(models.Model):
    """
    文章分类
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    """
    文章标签
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    # 文章标题
    title = models.CharField(max_length=70)
    # 文章正文
    body = models.TextField()

    # 文章创建与修改时间
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    # 文章摘要
    excerpt = models.CharField(max_length=200,blank=True)
    # 文章对应的数据库表和分类、标签对应的数据库表关联了起来
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag,blank=True)
    # 文章作者
    author = models.ForeignKey(User)
    # 记录阅读量
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:50]

        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_time']



