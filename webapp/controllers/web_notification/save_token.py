from django.views.decorators.csrf import csrf_exempt
from webapp.controllers.dispatchers.responses.send_pass_http_response import send_pass_http_response
from webapp.models import *
import requests
import json
import uuid

PASSWORD = "62043777!"

# Save notification token once user permits to receive notification
@csrf_exempt
def save_notification_token(request):
    system_fingerprint = request.POST['system_fingerprint']
    system_fingerprint = str(system_fingerprint)
    community = Community.objects.filter(unique_code='THEARGUS').first()
    if 'currentToken' in request.POST:
        currentToken = str(request.POST["currentToken"])
    else:
        currentToken = ""

    email = system_fingerprint + '@' + community.email_alias
    user = MyUser.objects.filter(community=community, email=email, is_guest_user=True).first()

    if user:
        devices = Device.objects.filter(user__community=community, user__email=email, device_type='web')
        for dev in devices:
            dev.delete()
        create_web_device(currentToken, user)
    else:
        user = create_guest_user_record_by_mac(system_fingerprint, community)
        create_web_device(currentToken, user)
    return send_pass_http_response()


def create_web_device(currentToken, user):
    device = Device()
    device.device_type = "web"
    device.reg_id = currentToken
    device.user = user
    device.save()
    return send_pass_http_response()

# Create a guest user for web notification using fingerprint
def create_guest_user_record_by_mac(system_fingerprint, community):
    first_name = 'Guest ' + ''.join(random.choice(string.digits) for _ in range(4))
    last_name = ''
    email = system_fingerprint + '@' + community.email_alias

    user = MyUser.objects.create(username=email,
                                 email=email,
                                 first_name=first_name,
                                 last_name=last_name)
    user.set_password(PASSWORD)
    user.last_login = datetime.now()
    user.auth_type = USER_AUTH_TYPES.GUEST_LOGIN
    user.is_guest_user = True
    user.is_onboarded = True
    user.save()
    user = MyUser.objects.get(pk=user.id)
    user.community.add(community)
    return user
