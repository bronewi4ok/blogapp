from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core import serializers

from ipware import get_client_ip
import mptt
from user_agents import parse
from users.models import CustomUser

from .models import Post, NewComment
from .forms import PostForm, NewCommentForm, SearchForm
from .filters import UserFilter

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def post_list(request):
    form = SearchForm()

    post_range = Post.objects.published()
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
        'search_q': search,
        'search_amount': search_amount,
        'form': form,
        }

    return render(request, 'blogapp/post_list.html', context)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


@login_required
def profile(request):
    q_author = request.GET.get("author", None)
    q_date = request.GET.get("date", None)
    search_q = request.GET.get('q', None)
    current_user = request.user
    
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
    else:
        form = SearchForm()
    
    filter_author = Post.objects.author(q_author, current_user)
    post_range = filter_author.date_range(q_date, filter_author)
    post_range = post_range.search(search_q)

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
        'filter_autor': filter_author,
        'search_amount': search_amount,
        'form': form,
        }
    return render(request, 'blogapp/post_list.html', context)

# from datetime import date
# Post.objects.filter(published_date__date=date.today())
# Post.objects.filter(published_date__month=date.month())

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


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
 

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blogapp:post_list')


@login_required
def post_draft(request):
    ip = get_client_ip(request)[0]
    form = SearchForm()
    posts = Post.objects.exclude(published_date__lte=timezone.now()).order_by('-created_date')
    posts = posts.filter(author=request.user)
    
    search_amount = Post.objects.published().count()
    return render(request, 'blogapp/post_list.html', {'posts':posts, 'ip':ip,'form':form,'search_amount':search_amount})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect(reverse('blogapp:post_detail', kwargs={'pk': pk}))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# POST DETAIL and COMMENTS
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    new_comments = NewComment.objects.filter(post__pk=post.pk)
    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.commented_by = request.user
            comment.save()
            serialized_comment = serializers.serialize('json', [comment,])
            context = {
                'post': post,
                'new_comments': new_comments,
                'form': form
                }
            return render(request, 'blogapp/post_detail_ajax.html', context)

            if pk:
                happy_comment = get_object_or_404(NewComment, pk = pk)
                comment.parent = happy_comment
                comment.save()
                comment = comment.values()
                print('!!!!!' + comment)
                return redirect(reverse('blogapp:post_detail', kwargs={'pk': pk}))
    else:
        form = NewCommentForm(initial={'author': request.user})

    context = {
        'post': post,
        'new_comments': new_comments,
        'form': form
        }
    return render(request, 'blogapp/post_detail.html', context)


@login_required
def add_comment_to_comment(request, pk, com_id=None):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.commented_by = request.user
            comment.save()
            if com_id:
                happy_comment = get_object_or_404(NewComment, pk = com_id)
                comment.parent = happy_comment
                comment.save()
            return redirect(reverse('blogapp:post_detail', kwargs={'pk': pk}))
            
    else:
        form = NewCommentForm(initial={'author': request.user})
    return render(request, 'blogapp/add_comment_to_comment.html', {'form': form})


@login_required
def comment_remove(request, pk, com_id):
    comment = get_object_or_404(NewComment, pk=com_id)
    comment.delete()
    if request.is_ajax():
        return JsonResponse({"good_news": "Huray!"})
    else:
        return redirect(reverse('blogapp:post_detail', kwargs={'pk': pk}))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


def search(request):
    user_list = CustomUser.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, 'blogapp/user_list.html', {'filter': user_filter})