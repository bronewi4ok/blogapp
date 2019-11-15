from django.urls import path, include
from . import views


urlpatterns = [
    path('edit/', views.user_edit_form, name='user_edit_form'),
]