from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import CustomUser
from .forms import CustomUserChangeForm
from ipware import get_client_ip
import mptt

@login_required
def user_edit_form(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blogapp:post_list')
    else:
        form = CustomUserChangeForm()
    return render(request, 'users/user_edit.html', {'form': form})
