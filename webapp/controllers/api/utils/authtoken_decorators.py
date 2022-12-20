from webapp.models import *
import jwt
from django.contrib.auth.models import AnonymousUser


def get_user_from_authtoken(func):
    def wrapper(*fargs, **kw):
        request = fargs[0]
        global auth_user

        if not request.user.is_authenticated():
            if 'HTTP_AUTHORIZATION' in request.META and request.META['HTTP_AUTHORIZATION']:
                auth_token = request.META['HTTP_AUTHORIZATION']
                auth_token = auth_token.replace('Token ', '')
                token_data = jwt.decode(auth_token, settings.SOCKETIO_PUBLIC_KEY, algorithms=['RS256'])
                user_id = token_data['user_id']
                request.user = MyUser.objects.get(pk=user_id)
            else:
                request.user = AnonymousUser()

        result = func(*fargs, **kw)

        return result

    return wrapper


# CBF - class based functions
def get_user_from_authtoken_for_cbf(func):
    def wrapper(*fargs, **kw):
        request = fargs[1]
        global auth_user

        if not request.user.is_authenticated():
            if 'HTTP_AUTHORIZATION' in request.META and request.META['HTTP_AUTHORIZATION']:
                auth_token = request.META['HTTP_AUTHORIZATION']
                auth_token = auth_token.replace('Token ', '')
                token_data = jwt.decode(auth_token, settings.SOCKETIO_PUBLIC_KEY, algorithms=['RS256'])
                user_id = token_data['user_id']
                request.user = MyUser.objects.get(pk=user_id)
            else:
                request.user = AnonymousUser()

        result = func(*fargs, **kw)

        return result

    return wrapper
