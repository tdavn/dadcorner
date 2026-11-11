from django import forms
from .models import Comment, Dish


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class PostForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'slug', 'category', 'image', 'ingredients', 'tags']
        