from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Dish, PostImage, KitchenTag, Comment


class PostImageAdmin(admin.StackedInline):
    model = PostImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(KitchenTag)
class StoreTagAdmin(admin.ModelAdmin):
    # This is required so the autocomplete dropdown knows what to search for
    search_fields = ['name']  # Replace 'name' with the actual field you want to search by
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'calories', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['calories', 'available']
    inlines = [PostImageAdmin]
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['tags']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'ingredients']

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display        = ("thumbnail", "title", "order")
    list_display_links  = ("thumbnail", "title")
    list_editable       = ("order",)
    search_fields       = ("title", "description")
    ordering            = ("order", "id")

    @admin.display(description="Preview")
    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:50px;border-radius:6px;" />',
                obj.image.url,
            )
        return "—"