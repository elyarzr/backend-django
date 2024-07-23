from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.forms import ModelForm
from django.db.models import Avg


class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub')
    sub_cat = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='category', null=True, blank=True)
    slug = models.SlugField(allow_unicode=True, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:category', args=[self.slug, self.id])


class Product(models.Model):
    VARIANT = (
        ('None', 'none'),
        ('Size', 'size'),
        ('Color', 'color'),
    )
    category = models.ManyToManyField(Category, blank=True, related_name='cat_product')
    name = models.CharField(max_length=200)
    amount = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(blank=True, null=True)
    total_price = models.PositiveSmallIntegerField()
    information = RichTextUploadingField(blank=True, null=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='product')
    status = models.CharField(null=True, blank=True, max_length=200, choices=VARIANT)

    tags = TaggableManager(blank=True)

    like = models.ManyToManyField(User, blank=True, related_name='product_like')
    total_like = models.IntegerField(default=0)
    unlike = models.ManyToManyField(User, blank=True, related_name='product_unlike')
    total_unlike = models.IntegerField(default=0)

    def average(self):
        data = Comment.objects.filter(is_reply=False, product=self).aggregate(avg=Avg('rate'))
        star = 0
        if data['avg'] is not None:
            star = round(data['avg'], 1)
        return star

    def total_like(self):
        return self.like.count()

    def total_unlike(self):
        return self.unlike.count()

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price


class Size(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Variants(models.Model):
    name = models.CharField(max_length=100)
    update = models.DateTimeField(auto_now=True)
    product_variant = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pr')
    size_variant = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    color_variant = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(blank=True, null=True)
    total_price = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rate = models.PositiveIntegerField(default=1)
    create = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='comment_reply')
    is_reply = models.BooleanField(default=False)
    comment_like = models.ManyToManyField(User, blank=True, related_name='com_like')
    total_comment_like = models.PositiveIntegerField(default=0)

    def total_like_comment(self):
        return self.comment_like.count()

    def __str__(self):
        return self.product.name


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'rate']


class ReplayForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='image/', blank=True, null=True)
