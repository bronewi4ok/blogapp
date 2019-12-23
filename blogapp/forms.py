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
        self.fields['title'].widget.attrs.update({'class': 'col form-control'})
        self.fields['text'].widget.attrs.update({'class': 'col form-control'})


class PictureForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'cover')


class NewCommentForm(forms.ModelForm):
    # captcha = CaptchaField(label='Are you an human? ')

    class Meta:
        model = NewComment
        fields = ('text',)


DATE_CHOICES = [
    (100000, 'All'),
    (7, 'Week'),
    (30, 'Month'),
    (365, 'Year'),
]

AUTHOR_CHOICES = [
    ('all', 'All'),
    ('my', 'My'),
    ('other', 'Other'),
]


class SearchForm(forms.Form):
    q = forms.CharField(max_length=120, required=False, label="how are you?")
    date = forms.ChoiceField(choices=DATE_CHOICES, required=False, label="how are you?")
    author = forms.ChoiceField(choices=AUTHOR_CHOICES, required=False, label="how are you?")

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        name = cleaned_data.get('q')