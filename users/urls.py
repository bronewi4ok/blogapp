from django.urls import path
from . import views


urlpatterns = [
    path('edit/', views.user_edit_form, name='user_edit_form'),
]