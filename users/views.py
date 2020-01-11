from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse, HttpResponse

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
    return render(request, 'users/post_author_profile.html', {'post_author': pk})


def validate_username(request):
    email = request.GET.get('email', None)
    if CustomUser.objects.filter(email__iexact=email).exists():
        is_available = "false"
    else:
        is_available = "true"
    return HttpResponse(is_available)


# def validate_username(request):
#     username = request.GET.get('username', None)
#     data = {
#         'is_taken': CustomUser.objects.filter(email__iexact=username).exists()
#     }
#     if data['is_taken']:
#         data['error_message'] = 'A user with this username already exists.'
#     return JsonResponse(data)