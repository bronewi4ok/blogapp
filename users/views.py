from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from blogapp.models import Post
from .models import CustomUser
from .forms import CustomUserChangeForm
from ipware import get_client_ip
import mptt

@login_required
def user_edit_form(request, pk=id):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_edit_form')
    else:
        form = CustomUserChangeForm()
    return render(request, 'users/user_edit.html', {'form': form})


@login_required
def post_author_profile(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post_author = post.author

    return render(request, 'users/post_author_profile.html', {'post_author': post_author})