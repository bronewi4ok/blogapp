from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        path = "{{request.path}}"
        return path
        # path = "/accounts/{username}/"
        # return path.format(username=request.user.username)