# from django.views.generic import ListView
from django.db.models import Count
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from .forms import CommentForm
from django.http import Http404
from .models import Post, Category
from taggit.models import Tag


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 6)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request,'headquarter/post/by_tag.html',{'posts': posts, 'tag': tag}
)


def post_by_cat(request, category_slug=None):
    category = None
    posts = None
    categories = Category.objects.all()
    published_posts = Post.published.all()
    page_number = request.GET.get('page', 1)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        paginator = Paginator(published_posts.filter(category=category), 6) 
        try:
            posts = paginator.page(page_number)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            posts = paginator.page(1)

    return render(
        request,
        'headquarter/post/by_cat.html',
        {'category': category, 'catgories': categories, 'posts': posts}
    )

def idx_page(request):
    cat1_posts = Post.published.filter(category=1)[:12]
    cat2_posts = Post.published.filter(category=2)[:10]
    cat3_posts = Post.published.filter(category=3)[:10]
    cat4_posts = Post.published.filter(category=4)[:15]
    featured_posts = cat1_posts[:4]
    cat1_featured = cat1_posts[0]
    cat1_next31 = cat1_posts[1:4]
    cat1_next32 = cat1_posts[4:7]
    cat2_featured = cat2_posts[0]
    cat2_col8 = cat2_posts[1]
    cat2_col41 = cat2_posts[2]
    cat2_col3 = cat2_posts[3:]
    cat3_featured = cat3_posts[0]
    cat3_for = cat3_posts[2:8]
    cat3_col8 = cat3_posts[1]
    cat3_col4 = cat3_posts[8]
    cat4_featured = cat4_posts[0]
    cat4_col41 = cat4_posts[1:3]
    cat4_col2 = cat4_posts[3:6]
    cat4_col3 = cat4_posts[6:9]
    cat4_col4 = cat4_posts[9:]

    return render(
        request,
        'headquarter/post/idx_page.html',
        {'cat1_posts': cat1_posts, 'cat2_posts': cat2_posts, 'cat3_posts': cat3_posts, 'cat4_posts': cat4_posts, 'featured_posts': featured_posts,
         'cat1_featured': cat1_featured,'cat1_next31': cat1_next31, 'cat1_next32':cat1_next32, 'cat2_featured': cat2_featured,
         'cat2_col41': cat2_col41, 'cat2_col8': cat2_col8, 'cat2_col3': cat2_col3,
         'cat3_featured': cat3_featured, 'cat3_for': cat3_for, 'cat3_col8': cat3_col8, 'cat3_col4': cat3_col4,
         'cat4_featured': cat4_featured, 'cat4_col41': cat4_col41, 'cat4_col2': cat4_col2, 'cat4_col3': cat4_col3, 'cat4_col4': cat4_col4}
    )
# class PostListView(ListView):
#     """
#     Alternative post list view
#     """
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'headquarter/post/list.html'



def post_detail(request, year, month, day, post):
    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("No Post found.")
    post = get_object_or_404(
        Post,  
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request,'headquarter/post/detail.html', {'post': post, 'comments': comments, 'form': form,'similar_posts': similar_posts})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
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
    return render(request, 'headquarter/post/comment.html', {'post': post, 'form': form, 'comment': comment})