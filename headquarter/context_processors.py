from django.db.models import Count
from taggit.models import Tag

def tag_cloud(request):
    # Fetch tags, count occurrences, and limit to the top 20 most popular tags
    tags = Tag.objects.annotate(
        num_times=Count('taggit_taggeditem_items')
    ).order_by('-num_times')[:11]
    
    return {'tag_cloud_tags': tags}