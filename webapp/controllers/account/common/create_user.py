# from webapp.controllers.account.referral_code import generate_referral_code
from webapp.models import *
import random, string

# from webapp.tasks.image_tasks import generate_user_photo
# from webapp.tasks.mongo_db_tasks import create_live_meetup_summary

PASSWORD = "62043777!"


def create_user_record_by_email(email, community, response=None):

    first_name = ''
    last_name = ''
    gender = None
    phone_number = ''

    user = MyUser.objects.create(email=email,
                                 username=uuid.uuid4().hex[:25],
                                 first_name=first_name,
                                 last_name=last_name,
                                 phone_number=phone_number)
    user.set_password(PASSWORD)
    user.last_login = datetime.now()
    user.auth_type = USER_AUTH_TYPES.CUSTOM_EMAIL
    user.community.add(community)

    if gender:
        user.gender = gender

        if gender == 'male':
            user.chat_req_receive_limit = 5
        else:
            user.chat_req_receive_limit = 1

    if community is not None:
        branches = community.branches
        if branches:
            split_branches = branches.split(',')
            if len(split_branches) == 1:
                user.community_branch = split_branches[0]

    # user.referral_code = generate_referral_code(user)
    user.save()

    for topic in Topic.objects.filter(type='CATEGORY', is_hidden=False):
        user_topic, n = UserTopic.objects.get_or_create(user=user, topic=topic)
        user_topic.is_following = True
        user_topic.save()

    privacy = UserPrivacySetting()
    privacy.user = user
    privacy.save()

    return user


def create_user_record_by_phone(phone_number, response, community, country_code='91'):

    if 'first_name' in response:
        first_name = response['first_name'].title()
    else:
        first_name = ''

    if 'last_name' in response:
        last_name = response['last_name'].title()
    else:
        last_name = ''

    if 'gender' in response:
        gender = response['gender']
    else:
        gender = None

    email = phone_number + '@' + community.email_alias

    user = MyUser.objects.create(email=email,
                                 username=phone_number,
                                 first_name=first_name,
                                 last_name=last_name,
                                 country_code=country_code,
                                 phone_number=phone_number)
    user.set_password(PASSWORD)
    user.last_login = datetime.now()

    if 'auth_type' in response and response['auth_type']:
        user.auth_type = response['auth_type']
    else:
        user.auth_type = USER_AUTH_TYPES.PHONE_NUMBER

    user.save()
    user.community.add(community)

    if gender:
        user.gender = gender

        if gender == 'male':
            user.chat_req_receive_limit = 5
        else:
            user.chat_req_receive_limit = 1

    if community is not None:
        branches = community.branches
        if branches:
            split_branches = branches.split(',')
            if len(split_branches) == 1:
                user.community_branch = split_branches[0]

    # user.referral_code = generate_referral_code(user)
    user.save()

    for topic in Topic.objects.filter(type='CATEGORY', is_hidden=False):
        user_topic, n = UserTopic.objects.get_or_create(user=user, topic=topic)
        user_topic.is_following = True
        user_topic.save()

    privacy = UserPrivacySetting()
    privacy.user = user
    privacy.save()

    return user


def create_guest_user_record_by_mac(mac, community):
    first_name = 'Guest ' + ''.join(random.choice(string.digits) for _ in range(4))
    last_name = ''
    email = mac + '@' + community.email_alias
    user = MyUser.objects.create(email=email,
                                 username=mac,
                                 first_name=first_name,
                                 last_name=last_name)
    user.set_password(PASSWORD)
    user.last_login = datetime.now()
    user.auth_type = USER_AUTH_TYPES.GUEST_LOGIN
    user.is_guest_user = True
    user.is_onboarded = True
    user.save()

    # generate_user_photo(user.id)
    user.community.add(community)
    # create_live_meetup_summary(user)

    privacy = UserPrivacySetting()
    privacy.user = user
    privacy.save()

    return user

