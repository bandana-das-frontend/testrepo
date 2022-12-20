from django.views.decorators.csrf import csrf_exempt
from webapp.controllers.dispatchers.responses.send_fail_http_response import send_fail_http_response
from webapp.controllers.dispatchers.responses.send_pass_http_response import send_pass_http_response
from webapp.models import MyUser


@csrf_exempt
def update_name_gender(request):
    if request.method != 'POST':
        return send_fail_http_response()
    else:
        user = MyUser.objects.get(pk=request.user.id)

        if 'first_name' in request.POST:
            user.first_name = request.POST["first_name"]
        
        if 'last_name' in request.POST:
            user.last_name = request.POST["last_name"]

        if 'gender' in request.POST:
            user.gender = request.POST["gender"]

        user.save()
        return send_pass_http_response()
 