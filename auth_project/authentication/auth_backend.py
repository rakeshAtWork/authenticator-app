from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.utils.crypto import constant_time_compare
from rest_framework.authentication import BaseAuthentication
from .models import AuthToken

class CookieAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_token = request.COOKIES.get('auth_token')
        if not auth_token:
            return None

        try:
            token_obj = AuthToken.objects.get(token=auth_token)
        except AuthToken.DoesNotExist:
            return None

        if not constant_time_compare(token_obj.token, auth_token):
            return None

        return (token_obj.user, None)
