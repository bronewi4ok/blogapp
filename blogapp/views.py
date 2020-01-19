from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core import serializers

from .models import Post, NewComment, Category, Slider
from .forms import PostForm, NewCommentForm, SearchForm
from .filters import UserFilter
from cart.models import Cart

from ipware import get_client_ip
import mptt
from user_agents import parse
from users.models import CustomUser



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def post_list(request):
    cart_obj = Cart.objects.new_or_get(request)
    form = SearchForm()
    slider = Slider.objects.filter(show=True)
    post_range = Post.published.all()
    search_amount = post_range.count()
    paginator = Paginator(post_range, 9)
    page = request.GET.get('page')

    genres = Category.objects.all()
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'page': page,
        'posts': posts,
        'genres':genres,
        'search_q': search,
        'search_amount': search_amount,
        'form': form,
        'slider': slider,
        'cart':cart_obj,
        }
    return render(request, 'blogapp/post_list.html', context)


def category_list(request, category=None):
    form = SearchForm()
    slider = Slider.objects.filter(show=True)
    post_range = Category.objects.get(name__iexact=category)
    post_range = post_range.get_descendants(include_self=True)
    post_range = Post.published.filter(category__in=post_range)
    search_amount = post_range.count()
    paginator = Paginator(post_range, 9)
    page = request.GET.get('page')

    genres = Category.objects.all()
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {'page': page,
        'posts': posts,
        'genres':genres,
        'search_q': search,
        'search_amount': search_amount,
        'form': form,
        'slider': slider,
        }

    return render(request, 'blogapp/post_list.html', context)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def profile(request):
    q_author = request.GET.get("author", None)
    q_date = request.GET.get("date", None)
    search_q = request.GET.get('q', None)
    current_user = request.user

    slider = Slider.objects.filter(show=True)
    genres = Category.objects.all()

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
        'genres':genres,
        'filter_autor': filter_author,
        'search_amount': search_amount,
        'form': form,
        'slider':slider,
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
            post.author.user_os = request.user_agent.os
            post.author.user_device = request.user_agent.device
            post.author.ip_address = get_client_ip(request)[0]
            post.author.save()
            post.save()
            return redirect(reverse('blogapp:post_detail', kwargs={'slug_title': post.slug_title, 'slug_date': post.slug_date}))
        else:
            print('bottom')
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'blogapp/post_edit.html', context)


@login_required
def post_edit(request, slug_title, slug_date):
    post = get_object_or_404(Post, slug_title=slug_title, slug_date=slug_date)
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse('blogapp:post_detail', kwargs={'slug_title':post.slug_title, 'slug_date':post.slug_date}))
    else:
        form = PostForm(instance=post)
    context = {'form': form}
    return render(request, 'blogapp/post_edit.html', context)
 

@login_required
def post_remove(request, slug_title, slug_date):
    post = get_object_or_404(Post, slug_title=slug_title, slug_date=slug_date)
    post.delete()
    return redirect('blogapp:post_list')


@login_required
def post_draft(request):
    ip = get_client_ip(request)[0]
    form = SearchForm()
    slider = Slider.objects.filter(show=True)
    posts = Post.objects.exclude(published_date__lte=timezone.now()).order_by('-created_date')
    posts = posts.filter(author=request.user)
    genres = Category.objects.all()
    search_amount = Post.objects.published().count()
    context = {
        'posts': posts,
        'ip': ip,
        'form': form,
        'search_amount': search_amount,
        'genres': genres,
        'slider':slider,
        }
    return render(request, 'blogapp/post_list.html', context)


@login_required
def post_publish(request, slug_title, slug_date):
    post = get_object_or_404(Post, slug_title=slug_title, slug_date=slug_date)
    post.publish()
    return redirect(reverse('blogapp:post_detail', kwargs={'slug_title':post.slug_title, 'slug_date':post.slug_date}))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# POST DETAIL and COMMENTS
def post_detail(request, slug_title, slug_date):
    cart_obj, cart_new_obj = Cart.objects.new_or_get(request)
    post = get_object_or_404(Post, slug_title=slug_title, slug_date=slug_date)
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
                'form': form,
                'cart':cart_obj,
                }
            return render(request, 'blogapp/post_detail_ajax.html', context)

            if pk:
                happy_comment = get_object_or_404(NewComment, pk = pk)
                comment.parent = happy_comment
                comment.save()
                comment = comment.values()
                print('!!!!!' + comment)
                return redirect(reverse('blogapp:post_detail', kwargs={'slug_title':post.slug_title, 'slug_date':post.slug_date}))
    else:
        form = NewCommentForm(initial={'author': request.user})

    context = {
        'post': post,
        'new_comments': new_comments,
        'form': form,
        'cart':cart_obj,
        }
    return render(request, 'blogapp/post_detail.html', context)


@login_required
def add_comment_to_comment(request,slug_title, slug_date, com_id=None):
    post = get_object_or_404(Post, slug_title=slug_title, slug_date=slug_date)
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
            return redirect(reverse('blogapp:post_detail', kwargs={'slug_title':post.slug_title, 'slug_date':post.slug_date}))
            
    else:
        form = NewCommentForm(initial={'author': request.user})
    return render(request, 'blogapp/add_comment_to_comment.html', {'form': form})


@login_required
def remove_comment(request, slug_title, slug_date, com_id):
    comment = get_object_or_404(NewComment, pk=com_id)
    comment.delete()
    if request.is_ajax():
        return JsonResponse({"good_news": "Huray!"})
    else:
        return redirect(reverse('blogapp:post_detail', kwargs={'slug_title': slug_title, 'slug_date': slug_date }))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


def search(request):
    user_list = CustomUser.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, 'blogapp/user_list.html', {'filter': user_filter})

# -------------------------------------------------------------------------------------

def show_category(request, hierarchy= None):
    category_slug = hierarchy.split('/')
    parent = None
    root = Category.objects.all()

    for slug in category_slug[:-1]:
        parent = root.get(parent=parent, slug = slug)

    try:
        instance = Category.objects.get(parent=parent,slug=category_slug[-1])
    except:
        instance = get_object_or_404(Post, slug = category_slug[-1])
        return render(request, "postDetail.html", {'instance':instance})
    else:
        return render(request, 'categories.html', {'instance':instance})
 
