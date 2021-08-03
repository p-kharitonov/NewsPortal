from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils.translation import gettext as _  # импортируем функцию для перевода
from django.utils.translation import pgettext_lazy


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    rating = models.IntegerField(default=0, verbose_name=_('Rating'))

    def update_rating(self):
        posts = Post.objects.filter(author=self.id)
        rating_posts = sum([int(post.rating) for post in posts]) * 3
        rating_comments = sum([int(comment.rating) for comment in Comment.objects.filter(user=self.id)])
        rating_comments_posts = sum([int(comment.rating) for post in posts for comment in Comment.objects.filter(post=post.id)])
        self.rating = sum([rating_posts, rating_comments, rating_comments_posts])
        self.save()
        return self.rating

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True, verbose_name=_('Title'))
    subscribers = models.ManyToManyField(User, verbose_name=_('Subscribers'), blank=True, null=True)

    def __str__(self):
        return f'{self.category}'

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NS'
    POST_CHOICES = (
        (ARTICLE, _('Article')),
        (NEWS, pgettext_lazy('Singular', 'News')),
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_('Author'))
    type_post = models.CharField(max_length=2, choices=POST_CHOICES,
                                 default=ARTICLE, verbose_name=_('Type'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date of creation'))
    category = models.ManyToManyField(Category, through='PostCategory', verbose_name=_('Category'))
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    content = models.TextField(verbose_name=_('Content'))
    rating = models.IntegerField(default=0, verbose_name=_('Rating'))

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    class Meta:
        verbose_name = _('Publication')
        verbose_name_plural = _('Publications')
        ordering = ('-id',)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category}'

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_('Publication'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    content = models.TextField(verbose_name=_('Comment'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date of creation'))
    rating = models.IntegerField(default=0, verbose_name=_('Rating'))

    def preview(self):
        if len(str(self.content)) > 124:
            return ''.join((self.content[:124], '...'))
        else:
            return str(self.content)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
