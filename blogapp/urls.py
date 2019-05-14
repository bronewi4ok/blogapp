from django.urls import path
from . import views


# app_name = 'blogapp'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),
    path('post/draft/', views.post_draft, name='post_draft'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<int:pk>/newcomment/', views.add_comment_to_comment, name='add_comment_to_comment'),
    path('post/<int:pk>/<int:redid>/newcomment/', views.add_comment_to_comment, name='add_comment_to_comment'),
]
