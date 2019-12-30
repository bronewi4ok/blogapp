from django.urls import path, include
from . import views


urlpatterns = [
    path('user_edit_form/', views.user_edit_form, name='user_edit_form'),
    path('post_author_profile/<int:pk>', views.post_author_profile, name='post_author_profile'),
    path('ajax/validate_username/', views.validate_username, name='validate_username'),
]