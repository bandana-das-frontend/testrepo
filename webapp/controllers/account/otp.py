import random
from django.views.decorators.csrf import csrf_exempt
from webapp.controllers.account.signup import check_domain_access, ErrorMessages
from webapp.controllers.utils.get_client_version import get_client_version
from webapp.models import *
from webapp.controllers.dispatchers.responses.send_pass_http_response import send_pass_http_response
from webapp.controllers.dispatchers.responses.send_fail_http_response import send_fail_http_response
from webapp.controllers.utils.send_sms import send_msg91_otp, send_2factor_otp
from templated_email import send_templated_mail


@csrf_exempt
def send_otp_to_phone_number(request):

    if 'phone_number' not in request.POST or 'country_code' not in request.POST:
        return send_fail_http_response()

    community_code = None
    if 'community_code' in request.POST:
        community_code = request.POST['community_code']

    phone_number = request.POST['phone_number']

    country_code = request.POST['country_code']

    otps = Otp.objects.filter(login_id=phone_number)

    if otps:
        otp_details = otps[0]

        if otp_details.expiry.replace(tzinfo=None) > datetime.now():
            otp_code = otp_details.otp
        else:
            otp_code = str(random.randint(100000, 999999))
            otp_details.otp = otp_code
            otp_details.expiry = datetime.now() + timedelta(minutes=15)
            otp_details.save()

    else:
        otp_code = str(random.randint(100000, 999999))
        Otp.objects.create(login_id=phone_number, otp=otp_code, expiry=datetime.now() + timedelta(minutes=15))

    community = request.community
    if community:
        community_name = community.name

    if settings.DEBUG:
        hash_code = "jBRPdYs7cGu"
    else:
        hash_code = "c+r/uaui0Ce"

    extra_param = "{\"VAR1\":\"" + community_name + "\",\"VAR2\":\"" + hash_code + "\"}"

    send_2factor_otp(country_code + phone_number, otp_code)
    return send_pass_http_response()


@csrf_exempt
def send_otp_to_email(request):

    if 'email' not in request.POST:
        return send_fail_http_response()

    community_code = None
    if 'community_code' in request.POST:
        community_code = request.POST['community_code']
    community = None
    if community_code:
        community = Community.objects.filter(unique_code=community_code).first()

    email = request.POST['email']
    email = email.replace(' ', '')

    version, client, is_sdk = get_client_version(request)
    if client == 'android' and version >= 320:
        if community and not check_domain_access(email, community):
            return send_fail_http_response(args=ErrorMessages.get_error("EMAIL_NOT_REGISTERED"))

    otps = Otp.objects.filter(login_id=email)
    if otps:
        otp_details = otps[0]
        if otp_details.expiry.replace(tzinfo=None) > datetime.now():
            key = otp_details.otp
        else:
            key = str(random.randint(100000, 999999))
            otp_details.otp = key
            otp_details.expiry = datetime.now() + timedelta(minutes=15)
            otp_details.save()
    else:
        key = str(random.randint(100000, 999999))
        otp_details = Otp.objects.create(login_id=email, otp=key, expiry=datetime.now() + timedelta(minutes=15))

    community_name = 'Milo'
    if community:
        community_name = community.name

    year = datetime.now().year

    try:
        send_templated_mail(
            template_name='otp_email',
            from_email= 'no-reply@mail.argusnews.in',
            recipient_list=[email],
            context={'email': email, 'otp': key, 'community_name': community_name, 'community_image' : "https://d267x6x6dh1ejh.cloudfront.net/posts/b3fa2717-bcd0-4b17-9c1c-25101104bbdf.png",'year':year},
        )
    except:
        pass
    finally:
        email_log = EmailLog()
        email_log.community = community
        email_log.user = None
        email_log.email_type = EMAIL_TEMPLATE_TYPE.OTP_EMAIL
        email_log.email_id = email
        email_log.content_type = str(ContentType.objects.get_for_model(otp_details).model)
        email_log.content_id = otp_details.id

        email_log.save()

    return send_pass_http_response()


