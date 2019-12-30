from django.urls import path
from .views import emailView


app_name = 'mailer'
urlpatterns = [
    path('email/', emailView, name='email'),
]
