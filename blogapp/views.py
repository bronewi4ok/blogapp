from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from .models import Post, NewComment
from .forms import PostForm, NewCommentForm, SearchForm
from ipware import get_client_ip
import mptt
from user_agents import parse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from datetime import datetime, timedelta

from users.models import CustomUser
from .filters import UserFilter

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def post_list(request):
    client_ip = get_client_ip(request)[0]
    search = request.GET.get('q', '')

    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
    else:
        form = SearchForm(initial={})
    
    
    post_range = Post.objects.published().filter(
        Q(title__icontains=search) |
        Q(text__icontains=search) 
    )
    post_range = post_range.distinct()

    search_amount = post_range.count()

    paginator = Paginator(post_range, 9)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {'page': page,
        'posts': posts,
        'post_range': post_range,
        'search_q': search,
        'search_amount': search_amount,
        'form': form,
        }
    # if horible != None:
    #     return render(request, 'blogapp/ajax_post_list.html', context)
    # else:
    return render(request, 'blogapp/post_list.html', context)



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


@login_required
def profile(request):
    client_ip = get_client_ip(request)[0]
    q_author = request.GET.get("author")
    q_date = request.GET.get("date")

    if q_author == 'other':
        filter_author = Post.objects.published().exclude(author=request.user)
    elif q_author == 'my':
        filter_author = Post.objects.published().filter(author=request.user)
    else:
        filter_author = Post.objects.published().filter()


    if q_date:
        data_range = timezone.now() - timedelta(days=int(q_date))
        post_range = filter_author.filter(published_date__gte=data_range)
    else:
        post_range = filter_author

    search_amount = post_range.count()
    paginator = Paginator(post_range, 9)
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
        'post_range': post_range,
        'filter_autor': filter_author,
        'search_amount': search_amount
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
    post.publish()
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


def search(request):
    user_list = CustomUser.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, 'blogapp/user_list.html', {'filter': user_filter})