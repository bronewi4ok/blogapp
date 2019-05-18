from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.forms import ModelForm

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(ModelForm):

    class Meta:
            model = CustomUser
            fields = ('avatar',)

    # class Meta:
    #     model = CustomUser
    #     fields = ('username', 'email', 'avatar')

    #     # exclude = ('password', 'password1', 'password2')
