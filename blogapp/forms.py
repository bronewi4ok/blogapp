from django import forms
from .models import Post, NewComment
# from captcha.fields import CaptchaField



class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'cover')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cover'].widget.attrs.update({'class': 'custom-file-input h-100'})


class NewCommentForm(forms.ModelForm):
    # captcha = CaptchaField(label='Are you an human? ')

    class Meta:
        model = NewComment
        fields = ('text',)