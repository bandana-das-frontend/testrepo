# -*- coding: utf-8 -*-

import datetime
import math
from datetime import datetime, timedelta

import python_jwt as jwt
import pytz
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from webapp.controllers.utils.get_client_version import get_client_version
from webapp.meta_models import CommunityType, USER_TAGS, ProfileInfo
from webapp.models import MyUser, UserPrivacySetting
from webapp.models import *
from webapp.serializers.college import college_serializers
from webapp.serializers.community import community_serializers
from webapp.serializers.education import education_serializers
from webapp.serializers.people_to_meet import people_to_meet_serializers
from webapp.serializers.place import place_serializers
from webapp.serializers.posts.post_media import media_serializer
from webapp.serializers.profile_info import get_profile_infos
from webapp.serializers.profile_sections import get_profile_section_order
from webapp.serializers.skill import skill_serializer
from webapp.serializers.user_school import user_school_serializer, user_school_going_serializer
from webapp.serializers.workplace import workplace_serializers
from webapp.utils.user import get_age


def is_request_user(request, user):
    if request and request.user and user:
        if request.user.id == user.id:
            return True
    return False


def basic_user_serializers(user, is_request_user=False):
    if not user:
        return None

    age = 0
    birthday = ''

    privacy_setting = UserPrivacySetting.objects.filter(user=user)
    if privacy_setting:
        privacy_setting = privacy_setting[0]
    else:
        privacy_setting, new = UserPrivacySetting.objects.get_or_create(user=user)

    if user.birthday:
        community = user.community.all()[0]
        if community.community_type == 'COLLEGE':
            if privacy_setting.birthday == PRIVACY_VISIBLE_TO.ALL_MEMBERS:
                birthday = user.birthday
                age = get_age(user)

        elif privacy_setting.birthday == PRIVACY_VISIBLE_TO.ALL_MEMBERS:
                age = get_age(user)

    if can_city_be_shown(is_request_user, user, privacy_setting):
        city = user.city_place_ref.name
    else:
        city = ''

    user.is_online = False
    try:
        if user.last_login.replace(tzinfo=pytz.UTC) >= (datetime.now() - timedelta(minutes=3)).replace(tzinfo=pytz.UTC):
            user.is_online = True
    except:
        pass

    if can_apartment_tower_be_shown(is_request_user, user, privacy_setting):
        apartment_tower = user.apartment_tower
    else:
        apartment_tower = ''

    if can_apartment_flat_be_shown(is_request_user, user, privacy_setting):
        apartment_flat_number = user.apartment_flat_number
    else:
        apartment_flat_number = ''

    hide_apartment_flat_details = user.hide_apartment_flat_details

    if user.profile_picture_ref:
        profile_pic_available = True
    else:
        profile_pic_available = False

    area = ''
    if can_area_be_shown(is_request_user, user, privacy_setting):
        if user.area_place_ref:
            area = user.area_place_ref.name

    college_branch = ''
    if user.college_branch_ref:
        college_branch = user.college_branch_ref.name

    college_relation = ''
    if user.college_relation:
        college_relation = user.college_relation

    work_designation = ''
    workplace_name = ''
    if can_workplace_be_shown(is_request_user, user, privacy_setting):
        if user.workplace_ref:
            workplace_name = user.workplace_ref.name

        if user.work_designation_ref:
            work_designation = user.work_designation_ref.name

    year_of_admission = ''
    if user:
        if user.year_of_admission:
            year_of_admission = user.year_of_admission

    first_name = user.first_name
    if first_name and first_name != '':
        first_name = user.first_name.title()

    last_name = user.last_name
    if last_name and last_name != '':
        last_name = user.last_name.title()

    gender = ''
    if can_gender_be_shown(is_request_user, user, privacy_setting):
        gender = user.gender

    community_branch = ''
    if user.community_branch:
        community_branch = user.community_branch

    community = user.community.all()[0]
    meta_data = ''
    if community:
        community_type = community.community_type
        if community.unique_code.upper() == 'MOSCHOOL':
            if user.school_ref and user.year_of_school_graduation:
                try:
                    meta_data = str(user.year_of_school_graduation) + u' Batch, ' + str(user.school_ref.name.title())
                except UnicodeEncodeError:
                    meta_data = ""
            elif user.school_ref:
                meta_data = user.school_ref.name
            elif city:
                meta_data = city
            else:
                meta_data = ''

        elif community_type == CommunityType.CO_WORKING or community_type == CommunityType.VC_FIRM or community_type == CommunityType.TECH_PARK:
            if workplace_name:
                meta_data = workplace_name
        elif community_type == CommunityType.APARTMENT:
            if apartment_tower and apartment_flat_number:
                meta_data = apartment_tower + ', ' + apartment_flat_number
            elif apartment_tower:
                meta_data = apartment_tower
            elif apartment_flat_number:
                meta_data = apartment_flat_number
        else:
            if area and city:
                meta_data = area + ', ' + city
            elif area:
                meta_data = area
            elif city:
                meta_data = city
            else:
                meta_data = ''

    discovery_meta_data = ''
    if community:
        community_type = community.community_type
        if community.unique_code.upper() == 'MOSCHOOL':
            if user.year_of_school_graduation:
                discovery_meta_data = 'Batch of ' + str(user.year_of_school_graduation)
            elif city:
                discovery_meta_data = city
            else:
                discovery_meta_data = ''

        elif community_type == CommunityType.APARTMENT:
            if apartment_tower and apartment_flat_number:
                discovery_meta_data = apartment_tower + ', ' + apartment_flat_number
            elif apartment_tower:
                discovery_meta_data = apartment_tower
            elif apartment_flat_number:
                discovery_meta_data = apartment_flat_number
        else:
            if area and city:
                discovery_meta_data = area + ', ' + city
            elif area:
                discovery_meta_data = area
            elif city:
                discovery_meta_data = city
            else:
                discovery_meta_data = ''

    receive_chat_request = user.receive_chat_request
    if hasattr(user, 'is_my_follower') and user.is_my_follower:
        receive_chat_request = True

    is_group_admin = False
    if hasattr(user, 'is_group_admin'):
        is_group_admin = user.is_group_admin

    blacklisted_by = None
    if hasattr(user, 'blacklisted_by'):
        blacklisted_by = basic_user_serializers(user.blacklisted_by)

    reason = ''
    if hasattr(user, 'reason'):
        reason = user.reason

    blacklisted_on = ''
    if hasattr(user, 'blacklisted_on'):
        blacklisted_on = user.blacklisted_on

    user_obj = {
        'id': user.id,
        'community_id': community.id,
        'type': 'PEOPLE',
        'username': user.username,
        'profile_picture': str(user.get_profile_picture()),
        'profile_picture_large': str(user.get_profile_picture(is_large=True)),
        'first_name': first_name,
        'last_name': last_name,
        'is_admin': user.is_admin,
        'area': area,
        'location': city,
        'age': age,
        'birthday': str(birthday),
        'gender': gender,
        'last_login_time': str(user.last_login),
        'work_name': user.fb_work_name if user.fb_work_name else '',
        'education_name': user.fb_education_name if user.fb_education_name else '',
        'credits': user.popularity,
        'remaining_credits': 0,
        'popularity': user.popularity,
        'is_verified': user.is_verified,
        'receive_chat_request': receive_chat_request,
        'is_online': user.is_online,
        'apartment_tower': apartment_tower,
        'apartment_flat_number': apartment_flat_number,
        'hide_apartment_flat_details': hide_apartment_flat_details,
        'profile_pic_available': profile_pic_available,
        'num_posts': user.num_posts,
        'num_comments': user.num_comments,
        'num_meetups': user.num_meetups,
        'auth_type': user.auth_type,
        'referral_code': user.referral_code,
        'date_joined': str(user.date_joined),
        'college_branch':  str(college_branch),
        'year_of_admission': str(year_of_admission),
        'passion': user.passion if user.passion else '',
        'college_relation': college_relation,
        'workplace_name': workplace_name,
        'work_designation': work_designation,
        'community_branch': community_branch,
        'meta_data': meta_data,
        'discovery_meta_data': discovery_meta_data,
        'is_group_admin': is_group_admin,
        'user_tag': user.user_tag if user.user_tag else '',
        'external_user_id': user.external_user_id if user.external_user_id else '',
        'blacklisted_by': blacklisted_by if blacklisted_by else {},
        'reason': reason,
        'blacklisted_on': str(blacklisted_on),
    }

    return user_obj


def user_serializers(user, request=None):
    if not user:
        return None

    community = user.community.all().first()
    client_version, client_type, is_sdk = get_client_version(request)

    privacy_setting = UserPrivacySetting.objects.filter(user=user)
    if privacy_setting:
        privacy_setting = privacy_setting[0]
    else:
        privacy_setting, new = UserPrivacySetting.objects.get_or_create(user=user)

    is_request_user = False
    if request and request.user.id == user.id:
        is_request_user = True
    basic_serialized_user = basic_user_serializers(user, is_request_user)

    skill_serialized = []
    for skill in user.skills.all():
        skill_serialized.append(skill_serializer(skill))
    basic_serialized_user['skills'] = skill_serialized

    # try:
    #     facebook_id = user.social_auth.get(provider='facebook').uid
    # except ObjectDoesNotExist:
    #     facebook_id = ''

    # basic_serialized_user['facebook_id'] = facebook_id
    basic_serialized_user['last_activity_time'] = str(user.last_activity_time)
    basic_serialized_user['number_of_topics'] = user.usertopic_user.filter(is_following=True).count()
    basic_serialized_user['number_of_opinions'] = user.useropinion_set.all().count()
    basic_serialized_user['number_of_followers'] = user.total_followers
    basic_serialized_user['number_of_following'] = user.total_following

    if hasattr(user, 'blocked_by'):
        basic_serialized_user['blocked_by'] = user.blocked_by
    else:
        basic_serialized_user['blocked_by'] = ""

    chat_system = 'SOCKETIO'
    if user.android_app_version <= 38 or user.ios_app_version > 10:
        chat_system = 'FIREBASE'
    basic_serialized_user['chat_system'] = chat_system

    college = user.college
    if college:
        serialized_college = college_serializers(college)
        if user.college_relation:
            college_relation = user.college_relation
        else:
            college_relation = ''

        if user.college_dept:
            college_dept = user.college_dept
        else:
            college_dept = ''

        basic_serialized_user['college'] = serialized_college
        basic_serialized_user['college_relation'] = college_relation
        basic_serialized_user['college_dept'] = college_dept

    if user.status:
        basic_serialized_user['status'] = user.status.strip()
    else:
        basic_serialized_user['status'] = ''

    basic_serialized_user['is_status_default'] = user.is_status_default

    if hasattr(user, 'is_follower'):
        basic_serialized_user['is_follower'] = user.is_follower

    if hasattr(user, 'percentage_match'):
        basic_serialized_user['percentage_match'] = round(float(user.percentage_match), 2)
    else:
        basic_serialized_user['percentage_match'] = 0

    if hasattr(user, 'percentage_match_topic'):
        basic_serialized_user['percentage_match_topic'] = {}

    if hasattr(user, 'allowed_to_chat'):
        basic_serialized_user['allowed_to_chat'] = user.allowed_to_chat

    if hasattr(user, 'num_common_interests'):
        basic_serialized_user['number_of_common_interests'] = user.num_common_interests

    if hasattr(user, 'rsvp_status'):
        basic_serialized_user['rsvp_status'] = user.rsvp_status

    if hasattr(user, 'meetup_request_status'):
        basic_serialized_user['meetup_request_status'] = user.meetup_request_status

    if hasattr(user, 'distance'):
        basic_serialized_user['distance'] = int(user.distance)
    else:
        basic_serialized_user['distance'] = "0"

    if hasattr(user, 'chat_status'):
        basic_serialized_user['chat_status'] = user.chat_status

    if hasattr(user, 'is_profile_pic_private'):
        basic_serialized_user['is_profile_pic_private'] = user.is_profile_pic_private

    if hasattr(user, 'common_people_to_meet'):
        people_to_meet = []
        for item in user.common_people_to_meet:
            if request and request.user:
                people_to_meet.append(people_to_meet_serializers(item, request.user))
            else:
                people_to_meet.append(people_to_meet_serializers(item))

        basic_serialized_user['people_to_meet'] = people_to_meet

    if hasattr(user, 'total_thanks'):
        basic_serialized_user['total_thanks'] = format_num_to_str(user.total_thanks)

    if hasattr(user, 'total_likes'):
        basic_serialized_user['total_likes'] = format_num_to_str(user.total_likes)

    if hasattr(user, 'total_favourites'):
        basic_serialized_user['total_favourites'] = format_num_to_str(user.total_followers)

    basic_serialized_user['views'] = format_num_to_str(user.views)

    if can_hometown_be_shown(is_request_user, user, privacy_setting):
        basic_serialized_user['hometown'] = place_serializers(user.hometown_place_ref)
    else:
        basic_serialized_user['hometown'] = {}

    if user.home_state_place_ref and can_hometown_be_shown(is_request_user, user, privacy_setting):
        basic_serialized_user['home_state'] = place_serializers(user.home_state_place_ref)
    else:
        basic_serialized_user['home_state'] = {}

    if can_area_be_shown(is_request_user, user, privacy_setting):
        basic_serialized_user['area_place'] = place_serializers(user.area_place_ref)
    else:
        basic_serialized_user['area_place'] = None

    if can_city_be_shown(is_request_user, user, privacy_setting):
        basic_serialized_user['city_place'] = place_serializers(user.city_place_ref)
        basic_serialized_user['city'] = user.city_place_ref.name
    else:
        basic_serialized_user['city_place'] = None
        basic_serialized_user['city'] = ''

    if can_education_be_shown(is_request_user, user, privacy_setting):
        basic_serialized_user['education'] = education_serializers(user.education_ref, user)
    else:
        basic_serialized_user['education'] = {}

    if can_workplace_be_shown(is_request_user, user, privacy_setting):
        basic_serialized_user['workplace'] = workplace_serializers(user.workplace_ref, user)
    else:
        basic_serialized_user['workplace'] = workplace_serializers(None, None)

    if hasattr(user, 'has_messaged'):
        basic_serialized_user['has_messaged'] = user.has_messaged

    if hasattr(user, 'num_photos'):
        basic_serialized_user['num_photos'] = user.num_photos

    if hasattr(user, 'num_videos'):
        basic_serialized_user['num_videos'] = user.num_videos

    if hasattr(user, 'num_documents'):
        basic_serialized_user['num_documents'] = user.num_documents

    if hasattr(user, 'photos'):
        photos_serialized = []
        for photo in user.photos:
            photos_serialized.append(media_serializer(photo))
        basic_serialized_user['photos'] = photos_serialized

    if hasattr(user, 'videos'):
        videos_serialized = []
        for video in user.videos:
            videos_serialized.append(media_serializer(video))
        basic_serialized_user['videos'] = videos_serialized

    if hasattr(user, 'documents'):
        documents_serialized = []
        for document in user.documents:
            documents_serialized.append(media_serializer(document))
        basic_serialized_user['documents'] = documents_serialized

    basic_serialized_user['community_branch'] = user.community_branch

    basic_serialized_user['is_admin'] = user.is_admin

    basic_serialized_user['school'] = user_school_serializer(user)
    basic_serialized_user['schools'] = user_school_going_serializer(user)

    basic_serialized_user['headquarters_place'] = place_serializers(user.headquarters_place_ref)

    basic_serialized_user['website'] = user.website if user.website else ''

    # Unused
    basic_serialized_user['notify_me'] = False

    show_section_headers = ((client_type == 'android' and client_version > 302) or (client_type == 'ios' and client_version >= 108)) \
                           and is_request_user

    user_profile_infos = community.get_user_profile_infos()
    if community.unique_code == 'CorpGini':
        if user.user_tag == USER_TAGS.STARTUP:
            user_profile_infos = [ProfileInfo.INFO_WEB_URL, ProfileInfo.INFO_HEAD_QUARTERS]

    # get profile infos list for user profile
    basic_serialized_user['user_profle_infos'] = get_profile_infos(show_section_headers, user, is_request_user,
                                                                   user_profile_infos)

    # get profile infos list for discover card
    basic_serialized_user['discover_profle_infos'] = get_profile_infos(False, user, False,
                                                                       community.get_discover_profile_infos())

    basic_serialized_user['profile_sections_order'] = get_profile_section_order(user, is_request_user)

    if request and request.user and request.user.id == user.id:
        basic_serialized_user['official_email'] = user.official_email if user.official_email else ''

    return basic_serialized_user


def user_serializers_on_auth(request, user):
    data = user_serializers(user, request)
    privacy_setting = UserPrivacySetting.objects.filter(user=user)
    if privacy_setting:
        privacy_setting = privacy_setting[0]
    else:
        privacy_setting, new = UserPrivacySetting.objects.get_or_create(user=user)

    # try:
    #     facebook_id = user.social_auth.get(provider='facebook').uid
    # except ObjectDoesNotExist:
    #     facebook_id = ''

    # credits is overridden from  parent serializer
    data['credits'] = 0

    # Meeting room credits
    data['total_meeting_room_credits'] = user.meeting_room_credits

    # data['facebook_id'] = facebook_id
    data['auth_type'] = user.auth_type
    data['is_onboarded'] = user.is_onboarded
    data['is_guest_user'] = user.is_guest_user
    data['email'] = user.email
    data['key_is_app_rated'] = user.play_store_rated
    data['key_is_post_type_trained'] = user.post_type_training
    data['post_followed'] = user.post_followed
    data['seen_college_info'] = user.seen_college_info
    data['number_of_topics'] = user.usertopic_user.filter(is_following=True).count()
    data['number_of_opinions'] = user.useropinion_set.all().count()
    data['is_place_owner'] = user.is_place_owner
    data['is_post_created'] = user.is_post_created
    data['num_people_to_meet'] = user.people_to_meet.all().count()
    data['settings_discover_everyone'] = user.is_discover_settings_everyone
    data['go_offline'] = user.go_offline
    data['firebase_token'] = get_firebase_token(request, {"uid": str(request.user.id)})
    data['socketio_token'] = get_socketio_token(request.user, True)
    data['max_friend_requests_per_day'] = user.max_friend_requests_per_day
    data['is_admin'] = user.is_admin
    data['num_sessions'] = user.num_sessions
    data['referral_code'] = user.referral_code
    data['shake_option'] = user.shake_option
    data['community_branch'] = user.community_branch
    data['is_delete_requested'] = user.is_delete_requested

    data['show_age'] = privacy_setting.birthday == PRIVACY_VISIBLE_TO.ALL_MEMBERS
    if user.birthday:
        data['birthday'] = str(user.birthday)
        data['is_dob_set'] = True
    else:
        data['birthday'] = ''
        data['is_dob_set'] = False

    # City is being used in the APKs older than 1.4.14
    if user.lat and user.long:
        data['latitude'] = user.lat
        data['longitude'] = user.long
    else:
        data['latitude'] = 0
        data['longitude'] = 0

    if user.country_place_ref:
        data['country_place_ref'] = place_serializers(user.country_place_ref)

        # US follows imperial system
        if user.country_place_ref.id == 2913:
            data['measurement_system'] = 'IMPERIAL'
        else:
            data['measurement_system'] = 'METRIC'
    else:
        data['country_place_ref'] = None
        data['measurement_system'] = 'METRIC'

    if user.last_location:
        data['last_location'] = user.last_location
    else:
        data['last_location'] = ''

    if user.college and user.college.status != 'UNVERIFIED' and user.college_relation:
        data['college_relation'] = user.college_relation
        data['college_status'] = user.college.status

        college = user.college

        serialized_college = college_serializers(college)
        if user.college_relation:
            college_relation = user.college_relation
        else:
            college_relation = ''
        data['college'] = serialized_college
        data['college_relation'] = college_relation
    else:
        data['college_relation'] = ''
        data['college_status'] = ''

    communities = user.community.all()
    if communities:
        data['community'] = community_serializers(communities[0])
    else:
        data['community'] = None

    blacklisted_communities = user.blacklisted_community.all()
    data['is_blacklisted'] = False
    if communities and blacklisted_communities:
        if communities[0] == blacklisted_communities[0]:
            data['is_blacklisted'] = True

    if user.free_until_time and user.free_until_time.replace(tzinfo=None) > datetime.now():
        data['is_user_free'] = True
    else:
        data['is_user_free'] = False

    return data


def user_search_serializer(user):
    data = user_serializers(user)
    data['obj_type'] = 'USER'

    return data


def get_invite_people():
    return {
        'type': 'PEOPLE_INVITE'
    }


# We should show up to 4 numbers (or 5 total chars). which means, up to 9999 we show the actual number. beyond that,
# round it off to 10K, 10.1K. 100K, 101K etc. (no decimals once it crosses 100K
def format_num_to_str(value):
    value_str = str(value)
    if value > 9999:
        value = round(value/1000.0, 1)
        (decimal_val, int_val) = math.modf(value)
        if int_val >= 100:
            value_str = str(int(int_val)) + 'K'
        elif decimal_val == 0.0:
            value_str = str(int(int_val)) + 'K'
        else:
            value_str = str(value) + 'K'
    elif value > 999999:
        value = round(value/1000000.0, 2)
        (decimal_val, int_val) = math.modf(value)
        if decimal_val == 0.0:
            value_str = str(int(int_val)) + 'M'
        else:
            value_str = str(value) + 'M'

    return value_str


def external_user_serializers(user):
    if not user:
        return None

    birthday = ''

    if user.birthday:
        birthday = str(user.birthday)

    college_branch = ''
    if user.college_branch_ref:
        college_branch = user.college_branch_ref.name

    year_of_graduation = ''
    if user:
        if user.year_of_graduation:
            year_of_graduation = user.year_of_graduation

    if user.hometown_place_ref:
        hometown = user.hometown_place_ref.name
    else:
        hometown = ''

    if user.home_state_place_ref:
        home_state = user.hometown_place_ref.name
    else:
        home_state = ''

    if user.area_place_ref:
        area = user.area_place_ref.name
    else:
        area = ''

    if user.city_place_ref:
        city = user.city_place_ref.name
    else:
        city = ''

    if user.education_ref:
        college = user.education_ref.name
    else:
        college = ''

    if user.workplace_ref:
        work_place = user.workplace_ref.name
    else:
        work_place = ''

    work_designation = ''
    if user.work_designation_ref:
        work_designation = user.work_designation_ref.name

    first_name = user.first_name
    if first_name and first_name != '':
        first_name = first_name[0].upper() + first_name[1:]

    last_name = user.last_name
    if last_name and last_name != '':
        last_name = last_name[0].upper() + last_name[1:]

    user = {
        'first_name': first_name,
        'last_name': last_name,
        'phone_number': user.phone_number,
        'bio': user.status.strip(),
        'area': area,
        'city': city,
        'home_town': hometown,
        'home_state': home_state,
        'birthday': str(birthday),
        'gender': user.gender if user.gender else '',
        'college': college,
        'college_branch':  college_branch,
        'work_place': work_place,
        'work_designation': work_designation,
        'year_of_graduation': str(year_of_graduation),
        'passion': user.passion if user.passion else '',
        'interests': user.interests
    }

    return user


def minimal_user_serializers(user):
    if not user:
        return None
    first_name = user.first_name
    if first_name and first_name != '':
        first_name = first_name[0].upper() + first_name[1:]
    last_name = user.last_name
    if last_name and last_name != '':
        last_name = last_name[0].upper() + last_name[1:]
    user = {
        'id': user.id,
        'external_user_id': user.external_user_id,
        'first_name': first_name,
        'last_name': last_name,
        'full_name': user.get_full_name(),
        'gender': user.gender if user.gender else '',
    }
    return user


def can_gender_be_shown(is_request_user, user, privacy_settings):
    if is_request_user:
        return user.gender is not None
    else:
        return user.gender and privacy_settings.gender == PRIVACY_VISIBLE_TO.ALL_MEMBERS


def can_apartment_tower_be_shown(is_request_user, user, privacy_settings):
    if is_request_user:
        return user.apartment_tower is not None
    else:
        return user.apartment_tower and privacy_settings.tower == PRIVACY_VISIBLE_TO.ALL_MEMBERS


def can_apartment_flat_be_shown(is_request_user, user, privacy_settings):
    if is_request_user:
        return user.apartment_flat_number is not None
    else:
        return user.apartment_flat_number and privacy_settings.tower == PRIVACY_VISIBLE_TO.ALL_MEMBERS


def can_workplace_be_shown(is_request_user, user, privacy_settings):
    if is_request_user:
        return True
    else:
        return privacy_settings.workplace == PRIVACY_VISIBLE_TO.ALL_MEMBERS


def can_area_be_shown(is_request_user, user, privacy_settings):
    return can_city_be_shown(is_request_user, user, privacy_settings)


def can_city_be_shown(is_request_user, user, privacy_settings):
    if is_request_user:
        return user.city_place_ref is not None
    else:
        return user.city_place_ref and privacy_settings.city == PRIVACY_VISIBLE_TO.ALL_MEMBERS


def can_hometown_be_shown(is_request_user, user, privacy_settings):
    if is_request_user:
        return user.hometown_place_ref is not None
    else:
        return user.hometown_place_ref and privacy_settings.hometown == PRIVACY_VISIBLE_TO.ALL_MEMBERS


def can_education_be_shown(is_request_user, user, privacy_settings):
    if is_request_user:
        return user.education_ref is not None
    else:
        return user.education_ref and privacy_settings.education == PRIVACY_VISIBLE_TO.ALL_MEMBERS


def get_socketio_token(user, is_request_user):
    try:
        user = MyUser.objects.get(pk=user.id)
        auth_payload = {
            "user_id": str(user.id),
            "user": basic_user_serializers(user, is_request_user)
        }
        exp = timedelta(minutes=60)
        token = jwt.generate_jwt(auth_payload, settings.SOCKETIO_PRIVATE_KEY, "RS256", exp)
        return token
    except Exception as e:
        print "Error creating custom token: " + e.message
        return ''


def get_firebase_token(request, auth_payload):
    try:
        claims = {}
        for key in auth_payload:
            claims[key] = auth_payload[key]

        payload = {
            "iss": settings.SERVICE_ACCOUNT_EMAIL,
            "sub": settings.SERVICE_ACCOUNT_EMAIL,
            "aud": "https://identitytoolkit.googleapis.com/google.identity.identitytoolkit.v1.IdentityToolkit",
            "uid": auth_payload['uid'],
            "claims": claims,
        }

        exp = timedelta(minutes=60)
        firebase_token = jwt.generate_jwt(payload, settings.FIREBASE_PRIVATE_KEY, "RS256", exp)
        return firebase_token
    except Exception as e:
        print "Error creating custom token: " + e.message
        return ''

