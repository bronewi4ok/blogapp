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


class SearchForm(forms.Form):
    q = forms.CharField(max_length=120, required=False, label="how are you?",  widget=forms.TextInput(attrs={'class': 'col form-control'}))
    # author = forms.ChoiceField(choices=[CHOICES], required=False)

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        name = cleaned_data.get('q')