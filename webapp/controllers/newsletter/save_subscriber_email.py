from webapp.controllers.dispatchers.responses.send_fail_http_response import send_fail_http_response
from webapp.controllers.dispatchers.responses.send_pass_http_response import send_pass_http_response
from webapp.models import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def save_subscriber_email(request):
    if request.method != 'POST':
        return send_fail_http_response()
    email = ''

    if 'email' in request.POST and request.POST['email']:
        email = request.POST['email']
    else:
        return send_fail_http_response()
    community = request.community

    email_exist = None
    email_exist = CommunityEmailSubscription.objects.filter(community=community, email=email).first()

    if email_exist:
        return send_pass_http_response()
    else:
        CommunityEmailSubscription.objects.create(community=community, email=email)
    return send_pass_http_response()
