from django import template
from ..models import Dish
import markdown
from django.utils.safestring import mark_safe

register = template.Library()

@register.inclusion_tag('kitchen/dish/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Dish.objects.order_by('-created')[:count]
    return {'latest_posts': latest_posts}


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))