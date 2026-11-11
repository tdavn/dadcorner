from django.shortcuts import get_object_or_404, render
from django.db.models import Count
from django.views.decorators.http import require_POST
from .models import Category, Dish, PostImage
from .forms import CommentForm
from menu.forms import MenuAddDishForm
from .models import KitchenTag
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator

def dish_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    dishes = Dish.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        dishes = dishes.filter(category=category)
    return render(request, 'kitchen/dish/list.html', {'category': category, 'categories': categories, 'dishes': dishes}
    )

def dish_detail(request, id, slug):
    dish = get_object_or_404(Dish, id=id, slug=slug, available=True)
    meal_dish_form = MenuAddDishForm()
        # List of active comments for this post
    comments = dish.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()
    # List of similar posts
    post_tags_ids = dish.tags.values_list('id', flat=True)
    similar_dishes = Dish.objects.filter(tags__in=post_tags_ids).exclude(id=dish.id)
    similar_dishes = similar_dishes.annotate(same_tags=Count('tags')).order_by('-same_tags', '-updated')[:4]
    gallery_items = PostImage.objects.filter(post=dish)
    return render(request, 'kitchen/dish/detail.html', 
                  {'dish': dish, 'meal_dish_form': meal_dish_form, 'comments': comments, 'form': form, 
                   'similar_dishes': similar_dishes, 'gallery_items': gallery_items}
                  )


def idx_page(request):
    return render(request, 'kitchen/kitchen_idx.html', {})


@require_POST
def dish_comment(request, dish_id, dish_slug):
    post = get_object_or_404(Dish, id=dish_id, slug=dish_slug, available=True)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    print(post.get_absolute_url)
    return render(request, 'kitchen/dish/comment.html', {'post': post, 'form': form, 'comment': comment})


def tag_list(request, tag_slug=None):
    tag_list = Dish.objects.filter(available=True)
    tag = None
    ingredients = KitchenTag.objects.all()
    if tag_slug:
        tag = get_object_or_404(KitchenTag, slug=tag_slug)
        tag_list = tag_list.filter(tags__in=[tag])

    paginator = Paginator(tag_list, 6)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request,'kitchen/dish/by_tag.html',{'posts': posts, 'tag': tag, 'ingredients': ingredients}
)
