from django import forms
from .models import Post, NewComment


class PostForm(forms.ModelForm):

    
    class Meta:
        model = Post
        fields = ('title', 'text', 'cover')


class NewCommentForm(forms.ModelForm):

    class Meta:
        model = NewComment
        fields = ('author', 'text')