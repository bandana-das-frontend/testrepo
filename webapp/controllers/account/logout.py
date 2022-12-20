from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt

from webapp.controllers.api.utils.authtoken_decorators import get_user_from_authtoken
# from webapp.dbplatform import *
from webapp.controllers.dispatchers.responses.send_fail_http_response import send_fail_http_response
from webapp.controllers.dispatchers.responses.send_pass_http_response import send_pass_http_response


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def logout_app(request):
    logout(request)
    return send_pass_http_response()


@csrf_exempt
@get_user_from_authtoken
def logout_app_post(request):
    if request.method != 'POST':
        return send_fail_http_response()

    devices = Device.objects.filter(user=request.user)
    for dev in devices:
        dev.delete()

    logout(request)
    return send_pass_http_response()
