from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(ModelForm):

    class Meta:
            model = CustomUser
            fields = ('avatar',)

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['avatar'].widget.attrs.update({'class': 'custom-file-input h-100'})

    # class Meta:
    #     model = CustomUser
    #     fields = ('username', 'email', 'avatar')
    #     exclude = ('password', 'password1', 'password2')
