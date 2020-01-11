from django.urls import path, re_path
from . import views


app_name = 'blogapp'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('category/<str:param>', views.category_list, name='category_list'),
    path('post/<slug:slug_date>/<slug:slug_title>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/edit/<slug:slug_date>/<slug:slug_title>/', views.post_edit, name='post_edit'),
    path('post/<slug:slug_date>/<slug:slug_title>/remove_post/', views.post_remove, name='post_remove'),
    path('post/draft/', views.post_draft, name='post_draft'),
    path('post/<slug:slug_date>/<slug:slug_title>/publish/', views.post_publish, name='post_publish'),
    # path('post/<int:pk>/newcomment/', views.add_comment_to_comment, name='add_comment_to_comment'),
    path('post/<slug:slug_date>/<slug:slug_title>/<int:com_id>/newcomment/', views.add_comment_to_comment, name='add_comment_to_comment'),
    path('post/<slug:slug_date>/<slug:slug_title>/remove_comment/<int:com_id>/', views.remove_comment, name='remove_comment'),
    path('profile', views.profile, name='profile'),
    path('search/', views.search, name='search'),
    re_path(r'^category/(?P<hierarchy>.+)/$', views.show_category, name='category'),
]
