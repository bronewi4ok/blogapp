from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from .models import Post, NewComment
from .forms import PostForm, NewCommentForm
from ipware import get_client_ip
import mptt
from user_agents import parse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse
from django.core import serializers


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def post_list(request):
    client_ip = get_client_ip(request)[0]
    search_q = request.GET.get("q")
    if search_q:
        post_range = Post.objects.filter(
            Q(title__icontains=search_q) |
            Q(text__icontains=search_q) 
        )
        post_range = post_range.filter(published_date__lte=timezone.now()).distinct()
    else:
        post_range = Post.objects.filter(published_date__lte=timezone.now())
    paginator = Paginator(post_range, 6)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {'page': page, 'posts': posts, 'client_ip': client_ip, 'post_range':post_range, 'search_q': search_q}
    return render(request, 'blogapp/post_list.html', context)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


@login_required
def profile(request):
    client_ip = get_client_ip(request)[0]
    firter_author = request.GET.get("q")
    if firter_author == 'my':
        post_range = Post.objects.filter(published_date__lte=timezone.now(), author_id=request.user.id)
    elif firter_author == 'other':
        post_range = Post.objects.filter(published_date__lte=timezone.now()).exclude(author_id=request.user.id)
    else:
        post_range = Post.objects.filter(published_date__lte=timezone.now())
    paginator = Paginator(post_range, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'page': page,
        'posts': posts,
        'client_ip': client_ip,
        'post_range': post_range
        }
    return render(request, 'blogapp/post_list.html', context)

# from datetime import date
# Post.objects.filter(published_date__date=date.today())
# Post.objects.filter(published_date__month=date.month())



# @login_required
# def profile(request):
#     client_ip = get_client_ip(request)[0]
#     post_range = Post.objects.filter(published_date__lte=timezone.now(), author_id=request.user.id)
#     paginator = Paginator(post_range, 6)
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     context = {
#         'page': page,
#         'posts': posts,
#         'client_ip': client_ip,
#         'post_range': post_range
#         }
#     return render(request, 'blogapp/post_list.html', context)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

@login_required
def post_detail(request, pk):
    hoho = request.META['DESKTOP_SESSION']
    post = get_object_or_404(Post, pk=pk)
    new_comments = NewComment.objects.filter(post__pk=post.pk)
    paginator = Paginator(new_comments, 3)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    context = {
        'post': post,
        'comments': comments,
        'new_comments': new_comments,
        'hoho': hoho,
        }
    return render(request, 'blogapp/post_detail.html', context)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.author.user_browser = request.user_agent.browser
            post.author.os = request.user_agent.os
            post.author.device = request.user_agent.device
            post.author.ip_address = get_client_ip(request)[0]
            post.author.save()
            post.save()
            return redirect(reverse('blogapp:post_detail', args=[post.pk]))
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'blogapp/post_edit.html', context)

# , author__id=request.user.id

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse('blogapp:post_detail', args=[pk]))
    else:
        form = PostForm(instance=post)
    context = {'form': form}
    return render(request, 'blogapp/post_edit.html', context)
    # reverse('blogapp:post_edit')
    # 'blogapp/post_edit.html' 
    
@login_required    
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blogapp:post_list')

@login_required
def post_draft(request):
    ip = get_client_ip(request)[0]
    posts = Post.objects.exclude(published_date__lte=timezone.now()).order_by('-created_date')
    posts = posts.filter(author=request.user)
    return render(request, 'blogapp/post_list.html', {'posts':posts, 'ip':ip})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.published_date = timezone.now()
    post.save()
    return redirect(reverse('blogapp:post_detail', kwargs={'pk': pk}))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def add_comment_to_comment(request, pk, redid=None):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.commented_by = request.user
            comment.save()
            if redid:
                happy_comment = get_object_or_404(NewComment, pk = redid)
                comment.parent = happy_comment
                comment.save()
            return redirect(reverse('blogapp:post_detail', kwargs={'pk': pk}))
    else:
        form = NewCommentForm(initial={'author': request.user})
    return render(request, 'blogapp/add_comment_to_comment.html', {'form': form})

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


