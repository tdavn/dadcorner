from django.conf import settings
from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from taggit.models import TagBase, ItemBase
from taggit.managers import TaggableManager


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name']),]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('kitchen:by_cat_list', args=[self.slug])


class KitchenTag(TagBase):
    class Meta:
        verbose_name = "Kitchen Tag"
        verbose_name_plural = "Kitchen Tags"

class TaggedDish(ItemBase):
    tag = models.ForeignKey(
        KitchenTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )
    content_object = models.ForeignKey('Dish', on_delete=models.CASCADE)


class Dish(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='created')
    category = models.ForeignKey(Category, related_name='dishes', on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='kitchen_recipe')
    image = models.ImageField(upload_to='images/kitchen/%Y/', blank=True)
    intro = models.TextField(max_length=500)
    ingredients = models.TextField()
    recipe = models.TextField(blank=True)
    album = models.ImageField(blank=True)
    calories = models.DecimalField(max_digits=10, decimal_places=2)
    prep = models.IntegerField(default=0, blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager(through=TaggedDish)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['id', 'slug']), models.Index(fields=['name']), models.Index(fields=['-created']),]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('kitchen:dish_detail', args=[self.id, self.slug])

    def get_cat_slug(self):
        return Category.objects.get(name=self.category).slug


class Comment(models.Model):
    post = models.ForeignKey(Dish, on_delete=models.CASCADE,  related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created']),]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


class PostImage(models.Model):
    post = models.ForeignKey(Dish, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/album/%Y/%m')
    title = models.CharField(max_length=120, blank=True, default='Food')
    description = models.CharField(max_length=250, blank=True)
    alt_text = models.CharField(
        max_length=120,
        blank=True,
        help_text="Optional alt text. Falls back to title if blank.",
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Lower numbers appear first.",
        db_index=True,
    )
    def __str__(self):
        return self.post.name

    @property
    def alt(self):
        return self.alt_text or self.title


