from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from blogapp.models import Post
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class PostInline(admin.TabularInline):
    model = Post

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username']
    inlines = [PostInline]


UserAdmin.fieldsets += ('Custom fields set', {'fields': ('avatar', 'ip_address')}),

admin.site.register(CustomUser, CustomUserAdmin)
