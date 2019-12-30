from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# def keep_in_touch(request):
#     name = request.GET.get('name', None)
#     email = request.GET.get('email', None)
#     message = request.GET.get('message', None)
#     if email and '@' in email:
#         body = 'This is a test message sent to {}.'.format(email)
#         send_mail('Hello', body, 'noreply@mysite.com', [email, ])
#         return HttpResponse('<h1>Sent.</h1>')
#     else:
#         return HttpResponse('<h1>No email was sent.</h1>')


def emailView(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            html_message = render_to_string('mailer/single-news.html',)
            try:
                send_mail(name, message, email, [ 'bronewi4ok@gmail.com', email], html_message=html_message)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
    else:
        form = ContactForm()

    return redirect('blogapp:post_list')

def successView(request):
    return HttpResponse('Success! Thank you for your message.')



# subject = 'Subject'
# html_message = render_to_string('single-news.html', {'context': 'values'})
# plain_message = strip_tags(html_message)
# from_email = 'From <from@example.com>'
# to = 'to@example.com'

# mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
