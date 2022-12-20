import firebase_admin
from firebase_admin.auth import *
import requests
import json
import jwt

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt

from webapp.controllers.account.common.create_user import create_user_record_by_email, create_user_record_by_phone
# from webapp.controllers.clients.corpgini import get_corpgini_invite, create_corpgigni_user_record
# from webapp.controllers.clients.moschool import set_default_interests, update_designation_for_deo_beo
from webapp.controllers.utils.get_client_version import get_client_version
from webapp.controllers.dispatchers.responses.send_fail_http_response import send_fail_http_response
from webapp.controllers.dispatchers.responses.send_pass_http_response import send_pass_http_response
from webapp.serializers.auth import auth_serializers
# from webapp.utils.notification import *
from webapp.models import *
# from webapp.tasks.email_tasks import send_mail_to_marketing

# from webapp.tasks.user_tasks import get_nomadx_user_data
# from webapp.controllers.clients.nestaway import check_nestaway_user, pre_fill_nestaway_user_data
# from webapp.controllers.clients.cove import get_cove_tenant_details, check_if_cove_tenant
from webapp.controllers.account.logout import logout


whitelist_phonenumbers = ['9634446420', '8123437303', '8801289655', '9908608000', '9964535578',
                          '9535212562', '9820194157', '8106956781', '8108214975', '9845057198',
                          '9611594353', '9886736036', '7780189404', '8005159369',
                          '8660842388', '9738952723', '9902426738', '9999209669', '7987153008',
                          '7026653965', '8074528715', '8054007004', '9980528128', '9945086181',
                          '8848705313', '9113991058', '9966009281', '7506050997', '9949058290',
                          '7795007899', '9014337318', '9986391519', '9819527737', '9999048267',
                          '9920948677', '8848705313', '9845097273', '9524954238', '8553042424',
                          '7795083186', '9818243839', '9067652015', '9619218906', '7415828424',
                          '8809908040', '9535615900', '7906501173', '9740144107', '9980973068',
                          '8217098343', '9741046188']

PASSWORD = "62043777!"
AUTH_PHONE_NUMBER = "phone_number"
AUTH_EMAIL = "email"


class ErrorMessages(object):
    """
        Error handling for sign up
    """
    ERROR_MESSAGES = {
        'NOT_REGISTERED': 'Please enter your community code',
        'TOKEN_EXPIRED': 'Authentication error',
        'INVALID_TOKEN': 'Authentication error',
        'USER_BLACKLISTED': 'Oops! There was an issue with sign up. Please reach out to your admin',
        'INVITE_NOT_FOUND': 'You are not invited to the community yet',
        'INVITE_LIMIT_EXCEEDED': 'Your organization invite has exceeded the user limit',
        'INVITE_EXPIRED': 'Your invite has expired',
        'INVITE_TRIAL_ENDED': 'Your trial has expired',
        'EMAIL_NOT_REGISTERED': 'Email not registered. Please try again or contact your admin',
    }

    @staticmethod
    def get_error(error_code):
        error_message = ''
        if error_code in ErrorMessages.ERROR_MESSAGES:
            error_message = ErrorMessages.ERROR_MESSAGES[error_code]
        return {
            'error': error_code,
            'error_message': error_message
        }


@csrf_exempt
def signup_with_token(request):
    """
        A end point API that accepts a token from the frontend which are in turn generated by
        Facebook's Account Kit, Firebase Auth or our own JWT tokens generated for custom phone number and email login.

        With the token we either sign up (create new record) or login the user (allow access to existing records).
    """

    phone_number = None
    email = None
    is_new_user = False
        
    access_token = request.POST['access_token']

    backend_type = ""
    if 'backend_type' in request.POST:
        backend_type = request.POST['backend_type']

    # We are explicitly getting country code from the frontend because Firebase has country coded embedded
    # in it's phone number data but we are not using country code in our username field.
    country_code = ""
    if 'country_code' in request.POST:
        country_code = request.POST['country_code']

    # Firebase login
    if backend_type == USER_AUTH_TYPES.FIREBASE_SMS:
        # Firebase schema from their API
        # {
        #     "iss": "https://securetoken.google.com/glynk-communities-dev",
        #     "aud": "glynk-communities-dev",
        #     "auth_time": 1571473448,
        #     "user_id": "EU4vqEqkpZQeuDaQKjB1zkEnLRj2",
        #     "sub": "EU4vqEqkpZQeuDaQKjB1zkEnLRj2",
        #     "iat": 1571473449,
        #     "exp": 1571477049,
        #     "phone_number": "+919886156126",
        #     "firebase": {
        #         "identities": {
        #             "phone": [
        #                 "+919886156126"
        #             ]
        #         },
        #         "sign_in_provider": "phone"
        #     },
        #     "uid": "EU4vqEqkpZQeuDaQKjB1zkEnLRj2"
        # }

        if (not len(firebase_admin._apps)):
            default_app = firebase_admin.initialize_app()

        try:
            firebase_auth_data = verify_id_token(access_token)
        except ExpiredIdTokenError:
            return send_fail_http_response(args=ErrorMessages.get_error("TOKEN_EXPIRED"))
        except:
            return send_fail_http_response(args=ErrorMessages.get_error("INVALID_TOKEN"))

        phone_number = firebase_auth_data['phone_number']

        # Remove country code, since we do not support it yet.
        if country_code:
            phone_number = phone_number.replace(country_code, "")

    # Custom SMS - to save money
    elif backend_type == USER_AUTH_TYPES.CUSTOM_SMS:
        # Accept the token from the frontend and decode the phone number.
        # We use a token so that no one sniffs out users' phone number.

        try:
            token_data = jwt.decode(access_token, settings.SOCKETIO_PUBLIC_KEY, algorithms=['RS256'])
        except jwt.ExpiredSignatureError:
            return send_fail_http_response(args=ErrorMessages.get_error("TOKEN_EXPIRED"))
        except:
            return send_fail_http_response(args=ErrorMessages.get_error("INVALID_TOKEN"))

        phone_number = token_data['phone_number']

    # Email login
    elif backend_type == USER_AUTH_TYPES.CUSTOM_EMAIL:
        # Accept the token from the frontend and decode the email address.
        # We use a token so that no one sniffs out users' email address.

        try:
            token_data = jwt.decode(access_token, settings.SOCKETIO_PUBLIC_KEY, algorithms=['RS256'])
        except jwt.ExpiredSignatureError:
            return send_fail_http_response(args=ErrorMessages.get_error("TOKEN_EXPIRED"))
        except:
            return send_fail_http_response(args=ErrorMessages.get_error("INVALID_TOKEN"))

        email = token_data['email']

    # Account kit phone number
    else:
        # Account kit schema from their API
        # {
        #     "id": "",
        #     "phone": {
        #         "number": "91XXXXXXXXXX",
        #         "country_prefix": "91",
        #         "national_number": "XXXXXXXXXX"
        #     },
        #     "application": {
        #         "id": ""
        #     }
        # }

        r = requests.get('https://graph.accountkit.com/v1.3/me/?access_token={0}'.format(access_token), verify=False)
        fb_data = r.json()

        phone_number = fb_data['phone']['national_number']
        country_code = fb_data['phone']['country_prefix']

    # Get the community code
    community_code = ''
    community_code = settings.COMMUNITY_UNIQUE_CODE
    if 'referral_code' in request.POST:
        # This is for old apks. We moved to community_code in newer versions.
        community_code = request.POST['referral_code']
        community_code = community_code.replace(' ', '')
    elif 'community_code' in request.POST:
        community_code = request.POST['community_code']
        community_code = community_code.replace(' ', '')

    # Some kind of a override
    if phone_number and phone_number in ['9845787038']:
        community_code = 'moschool'

    # If a user referred the user who is currently signing up, get user id of the person who referred.
    user_referral_code = None
    if 'user_referral_code' in request.POST:
        user_referral_code = request.POST['user_referral_code']
        user_referral_code = user_referral_code.replace(' ', '')

    # Send fail response if this end point is called without any phone number or email
    if not phone_number and not email:
        return send_fail_http_response()

    # Check if this is an existing user - this is a login case
    user_exists = None
    community_obj = Community.objects.filter(unique_code='THEARGUS').first()
    if email:
        user_exists = MyUser.objects.filter(email=email, community=community_obj).first()

    elif phone_number:
        user_exists = MyUser.objects.filter(phone_number=phone_number, community=community_obj).first()
    else:
        # If the user comes with nothing, then fail the response
        return send_fail_http_response()

    # To store the user login type.
    payload = {}
    payload["auth_type"] = backend_type

    # This is for sign up case, where there is not existing user record.
    nestaway_response = None
    if not user_exists:

        # If the user record does not exist then the user is a new user.
        is_new_user = True

        # In sign up case, here user came without community code
        if not community_code:
            return send_fail_http_response(args=ErrorMessages.get_error("NOT_REGISTERED"))

            # if phone_number:
            #     # Phone number case: We have exception with Nestaway where we check with their database if they come
            #     # without community code. If the ph number is available in Nestaway database
            #     # we create a new user record for them.
            #     exists, nestaway_response = check_nestaway_user(phone_number)
            #     if exists:
            #         community = Community.objects.get(pk=1)
            #         community_name = community.name
            #         new_user = create_user_record_by_phone(phone_number, {}, community_name, country_code)
            #         new_user.access_token = json.loads(json.dumps({'access_token': access_token}))
            #     else:
            #         # Here we have to handle phone number user without CC and from other communities
            #         # who have given API access such as NomadX, Cove etc. But we are not doing this as of now and
            #         # instead we are just sending a fail request and showing enter community
            #         # code screen in the frontend.
            #         return send_fail_http_response_with_error("NOT_REGISTERED")
            # else:
            #     # Email case: Tte control will reach here if user comes with email but without community code.
            #     return send_fail_http_response_with_error("NOT_REGISTERED")

        # In this case, user has the community code.
        else:
            communities = Community.objects.filter(unique_code=community_code)

            # Not a valid CC
            if not communities:
                return send_fail_http_response(args=ErrorMessages.get_error("NOT_REGISTERED"))


            community = communities[0]
            community_name = community.name
            whitelist_phonenumbers = community.get_whitelist_numbers()


            # Phone account
            if phone_number:
                new_user = create_user_record_by_phone(phone_number, payload, community, country_code)

                # Store the access token whatever we get from the frontend as it is.
                # We probably don't use this anywhere.
                new_user.access_token = json.loads(json.dumps({'access_token': access_token}))

            # Email account
            elif email:
                if check_domain_access(email, community):
                    new_user = create_user_record_by_email(email, community)
                else:
                    return send_fail_http_response(args=ErrorMessages.get_error("EMAIL_NOT_REGISTERED"))
            else:
                return send_fail_http_response(args=ErrorMessages.get_error("NOT_REGISTERED"))

        # Make first three users of the community as admin.
        # This is more for ease of use from community management from our side.
        num_admins = MyUser.objects.filter(community=community, is_admin=True).count()
        if num_admins < 3:
            new_user.is_admin = True

        if community.community_type == CommunityType.COLLEGE:
            new_user.education_ref = community.education_ref

        if community.community_type == CommunityType.OFFICE:
            new_user.workplace_ref = community.workplace_ref
        # Prefill End #

        # Checking for referrer user
        if user_referral_code:
            referrer_user = MyUser.objects.filter(referral_code=user_referral_code)

            if referrer_user:
                referrer_user = referrer_user[0]
                referrer_user.num_referrals += 1
                referrer_user.save()
                new_user.referrer_user = referrer_user

        request.session['new_user'] = True

        new_user.save()

        # Setting the user_exists var with new user to handle any other logic below
        # this onwards as is for returning or existing user
        user_exists = new_user

    if user_exists:
        user = user_exists
        community = user.community.all()[0]

        if community in user.blacklisted_community.all():
            return send_fail_http_response(args=ErrorMessages.get_error("USER_BLACKLISTED"))

        if backend_type == USER_AUTH_TYPES.CUSTOM_EMAIL:
            authed_user = MyUser.objects.filter(email=email, community=community).first()
            authed_user.backend = 'django.contrib.auth.backends.ModelBackend'
        else:
            email_alias = community.email_alias
            authed_user = authenticate(username=phone_number + '@' + email_alias, password=PASSWORD)

        # Logout guest user
        logout(request)
        login(request, authed_user)

        client_version, client_type, is_sdk = get_client_version(request)
        user.client_type = client_type

        if 'manufacturer' in request.POST:
            user.manufacturer = request.POST['manufacturer']
        if 'model' in request.POST:
            user.model = request.POST['model']
        if 'device' in request.POST:
            user.device_data = request.POST['device']
        if 'mac' in request.POST:
            user.mac = request.POST['mac']

        if 'device_id' in request.POST:
            device_id = request.POST['device_id']
            user_device, n = UserDevice.objects.get_or_create(device_id=device_id)
            user_device.user = user
            user_device.device_type = client_type
            user_device.save()

        if 'language_code' in request.POST:
            language_code = request.POST['language_code']
            language = Language.objects.filter(language_code=language_code)
            if language:
                user.language = language[0]

        user.save()

        # Login Record for statistics purpouse
        new_login_record = LoginRecord()
        new_login_record.user = user
        new_login_record.save()

        return send_pass_http_response(args=auth_serializers(request, user))

    return send_fail_http_response()


def check_domain_access(email, community):
    domain = email.split('@')[1]
    # If no whitelist domains are set, allow all domains.
    if len(community.get_whitelist_domains()) == 0:
        return True
    else:
        # If whitelist domains are set, allow only specifiec domains.
        if domain in community.get_whitelist_domains():
            return True
        else:
            return False
