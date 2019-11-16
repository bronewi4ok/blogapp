from django import forms
from .models import Post, NewComment
# from captcha.fields import CaptchaField



class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'cover')


class NewCommentForm(forms.ModelForm):
    # captcha = CaptchaField(label='Are you an human? ')

    class Meta:
        model = NewComment
        fields = ('text',)