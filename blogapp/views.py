from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post, NewComment
from .forms import PostForm, NewCommentForm
from ipware import get_client_ip
import mptt
from user_agents import parse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def post_list(request):
    ip = get_client_ip(request)[0]
    # post_list= NewComment.objects.all()
    post_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(post_list, 25)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,'blogapp/post_list.html',{'page': page,'posts': posts,'ip':ip})
    
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[ :20]
    # return render(request, 'blogapp/post_list.html', {'posts': posts, 'ip':ip})





# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -







# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    new_comments = NewComment.objects.filter(post__pk=post.pk)
    return render(request, 'blogapp/post_detail.html', {'post': post, 'new_comments': new_comments})
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
            return redirect('post_draft')
    else:
        form = PostForm()
    return render(request, 'blogapp/post_edit.html', {'form': form})

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
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'blogapp/post_edit.html', {'form': form})
    
@login_required    
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

@login_required
def post_draft(request):
    ip = get_client_ip(request)[0]
    posts = Post.objects.exclude(published_date__lte=timezone.now()).order_by('-created_date')
    return render(request, 'blogapp/post_list.html', {'posts':posts, 'ip':ip})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.published_date = timezone.now()
    post.save()
    return redirect('post_list')


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def add_comment_to_comment(request, pk, redid=None):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            if redid:
                happy_comment = get_object_or_404(NewComment, pk = redid)
                comment.parent = happy_comment
                comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = NewCommentForm()
    return render(request, 'blogapp/add_comment_to_comment.html', {'form': form})

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


