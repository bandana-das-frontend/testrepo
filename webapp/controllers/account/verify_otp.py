from django.views.decorators.csrf import csrf_exempt
from webapp.models import *
from webapp.controllers.dispatchers.responses.send_pass_http_response import send_pass_http_response
from webapp.controllers.dispatchers.responses.send_fail_http_response import send_fail_http_response
import python_jwt as jwt


@csrf_exempt
def verify_phone_number_otp(request):

    if 'phone_number' not in request.POST or 'otp' not in request.POST:
        return send_fail_http_response()

    phone_number = request.POST['phone_number']
    otp_code = request.POST['otp']

    phone_number = phone_number.replace('+', '')

    otp = Otp.objects.filter(otp=otp_code, login_id=phone_number)

    if not otp:
        return send_fail_http_response()

    otp = otp[0]

    if datetime.now() > otp.expiry.replace(tzinfo=None):
        return send_fail_http_response(args={'error': "OTP_EXPIRED"})

    auth_payload = {'phone_number': phone_number}
    exp = timedelta(minutes=60)
    token = jwt.generate_jwt(auth_payload, settings.SOCKETIO_PRIVATE_KEY, "RS256", exp)

    return send_pass_http_response(args={
        'access_token': token
    })


@csrf_exempt
def verify_email_otp(request):

    if 'email' not in request.POST or 'otp' not in request.POST:
        return send_fail_http_response()

    email = request.POST['email']
    email = email.replace(' ', '')

    otp_code = request.POST['otp']

    otp = Otp.objects.filter(otp=otp_code, login_id=email)
    if not otp:
        return send_fail_http_response()

    otp = otp[0]

    if datetime.now() > otp.expiry.replace(tzinfo=None):
        return send_fail_http_response(args={'error': "OTP_EXPIRED"})

    auth_payload = {'email': email}
    exp = timedelta(minutes=60)
    token = jwt.generate_jwt(auth_payload, settings.SOCKETIO_PRIVATE_KEY, "RS256", exp)


    return send_pass_http_response(args={
        'access_token': token
    })
