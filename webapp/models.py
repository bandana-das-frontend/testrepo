#
#                       _oo0oo_
#                      o8888888o
#                      88" . "88
#                      (| -_- |)
#                      0\  =  /0
#                    ___/`---'\___
#                  .' \\|     |// '.
#                 / \\|||  :  |||// \
#                / _||||| -:- |||||- \
#               |   | \\\  -  /// |   |
#               | \_|  ''\---/''  |_/ |
#               \  .-\__  '-'  ___/-. /
#             ___'. .'  /--.--\  `. .'___
#          ."" '<  `.___\_<|>_/___.' >' "".
#         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#         \  \ `_.   \_ __\ /__ _/   .-` /  /
#     =====`-.____`.___ \_____/___.-`___.-'=====
#                       `=---='
#
#
#     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#           Bless this code to be bug free
#


import uuid
import os
import re
from django.utils.encoding import smart_str, filepath_to_uri
import uuid
import random, string
from urlparse import urlparse
from os.path import splitext, basename
from webapp.meta_models import *
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group, UserManager
from django.core.files.storage import default_storage as storage
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.contrib.auth.signals import user_logged_in
from django.db import IntegrityError
from django.core.files.storage import default_storage as storage
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from datetime import datetime, timedelta
from PIL import Image
from datetime import date
from StringIO import StringIO



import pytz

TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

LAST_SCHOOL_ID_WITHOUT_LINK = 60766


class MyUser(User):
    auth_type = models.CharField(max_length=20, default='NONE')
    verification_code = models.CharField(max_length=255, null=True, blank=True)
    language = models.ForeignKey('Language', null=True, blank=True, default='', on_delete=models.SET_NULL)
    is_registered = models.BooleanField(default=False)
    number_of_friends = models.IntegerField(default=0)
    ip = models.GenericIPAddressField(null=True, blank=True)
    uuid = models.CharField(max_length=255, null=True, blank=True)
    external_user_id = models.CharField(max_length=255, null=True, blank=True)
    private_url = models.CharField(max_length=255, null=True, blank=True)
    verification_url = models.CharField(max_length=255, null=True, blank=True)
    unsubscribe = models.BooleanField(default=False)
    score = models.BigIntegerField(default=0)
    tracking_polls = models.ManyToManyField('Poll', related_name='tracking_polls', null=True, blank=True)
    topics = models.ManyToManyField('Topic', null=True, blank=True, through='UserTopic')
    network = models.ManyToManyField('MyUser', through='Friendship', related_name='friendship_network')
    last_activity_time = models.DateTimeField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to=upload_users_to, null=True, blank=True)
    profile_picture_ref = models.ForeignKey('ProfilePicture', null=True, blank=True, on_delete=models.SET_NULL)
    is_profile_pic_private = models.BooleanField(default=False)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    move_in_date = models.DateField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    last_lat = models.FloatField(null=True, blank=True)
    last_long = models.FloatField(null=True, blank=True)
    last_location = models.CharField(max_length=255, null=True, blank=True)
    test_user = models.BooleanField(default=False)
    invite_code_used = models.CharField(max_length=255, null=True, blank=True)
    is_invited_by_friend = models.BooleanField(default=False)
    number_of_invites = models.IntegerField(default=10, null=True, blank=True)
    d_registered = models.BooleanField(default=False)
    m_registered = models.BooleanField(default=False)
    is_onboarded = models.BooleanField(default=False)
    is_sdk_onboarded = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    unseen_notifications = models.IntegerField(default=0)
    # unseen_messages is the sum of unread conversations and pending chat requests
    unseen_messages = models.IntegerField(default=0)
    # unread_msg_count is the total of unread messages for the user
    unread_msg_count = models.IntegerField(default=0)
    post_clicked = models.ForeignKey('Post', null=True, blank=True)
    invited_user = models.ForeignKey('MyUser', null=True, blank=True, on_delete=models.SET_NULL)
    status = models.TextField(blank=True, null=True)
    passion = models.CharField(max_length=255, null=True, blank=True)
    email_notification = models.BooleanField(default=True)
    push_notification = models.BooleanField(default=True)  # In App, settings screen
    notification_status = models.BooleanField(
        default=False)  # This is OS settings whether notification permission is given or denied
    group_message_notif_status = models.BooleanField(default=True)
    new_user_notif_status = models.BooleanField(default=True)
    android_app_version = models.IntegerField(default=0)
    android_sdk_version = models.IntegerField(default=0)
    ios_app_version = models.IntegerField(default=0)
    play_store_rated = models.BooleanField(default=False)
    rating_requested_timestamp = models.DateTimeField(null=True, blank=True)
    post_type_training = models.BooleanField(default=False)
    post_followed = models.BooleanField(default=False)
    seen_college_info = models.BooleanField(default=False)
    referrer_user = models.ForeignKey('MyUser', null=True, blank=True, related_name='referrer_user_key',
                                      on_delete=models.SET_NULL)
    college = models.ForeignKey('College', null=True, blank=True)
    college_relation = models.CharField(max_length=50, choices=COLLEGE_USER_RELATION().get_choices(), null=True,
                                        blank=True, default=COLLEGE_USER_RELATION.NONE)
    college_dept = models.CharField(max_length=255, null=True, blank=True)
    college_join_date = models.DateTimeField(null=True, blank=True)
    college_end_date = models.DateTimeField(null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    country_code = models.CharField(max_length=10, null=True, blank=True, default='91')
    headquarters_place_ref = models.ForeignKey('Place', null=True, blank=True, related_name='headquarters_place_ref',
                                               on_delete=models.SET_NULL)
    website = models.CharField(max_length=100, null=True, blank=True, default='')
    college_place_ref = models.ForeignKey('Place', null=True, blank=True, related_name='college_place_ref',
                                          on_delete=models.SET_NULL)
    area_place_ref = models.ForeignKey('Place', null=True, blank=True, related_name='area_place_ref',
                                       on_delete=models.SET_NULL)
    city_place_ref = models.ForeignKey('Place', null=True, blank=True, related_name='city_place_ref',
                                       on_delete=models.SET_NULL)
    country_place_ref = models.ForeignKey('Place', null=True, blank=True, related_name='country_place_ref',
                                          on_delete=models.SET_NULL)
    home_state_place_ref = models.ForeignKey('Place', null=True, blank=True, related_name='home_state_place_ref',
                                             on_delete=models.SET_NULL)
    hometown_place_ref = models.ForeignKey('Place', null=True, blank=True, related_name='hometown_place_ref',
                                           on_delete=models.SET_NULL)
    education_ref = models.ForeignKey('Education', null=True, blank=True, related_name='education_ref',
                                      on_delete=models.SET_NULL)
    college_location = models.CharField(max_length=255, null=True, blank=True)
    college_branch_ref = models.ForeignKey('CollegeBranch', null=True, blank=True, related_name='college_branch_ref',
                                           on_delete=models.SET_NULL)
    workplace_ref = models.ForeignKey('WorkPlace', null=True, blank=True, related_name='workplace_ref',
                                      on_delete=models.SET_NULL)
    school_ref = models.ForeignKey('School', null=True, blank=True, related_name='school_ref',
                                   on_delete=models.SET_NULL)
    schools = models.ManyToManyField('School', through='SchoolGoing')
    year_of_school_graduation = models.IntegerField(blank=True, null=True)
    work_designation_ref = models.ForeignKey('WorkDesignation', null=True, blank=True,
                                             related_name='work_designation_ref', on_delete=models.SET_NULL)
    workplace_location = models.CharField(max_length=255, null=True, blank=True)
    community_branch = models.CharField(max_length=255, default='', blank=True)
    likes = models.ManyToManyField('Like', null=True, blank=True)
    people_to_meet = models.ManyToManyField('PeopleToMeet', null=True, blank=True, through='MyUserPeopleToMeet')
    num_people_to_meet = models.IntegerField(default=0)
    saved_posts = models.ManyToManyField('Post', null=True, blank=True, related_name='saved_posts')
    is_place_owner = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    num_reports = models.IntegerField(default=0)
    is_post_created = models.BooleanField(default=False)
    is_delete_requested = models.BooleanField(default=False)
    num_sessions = models.IntegerField(default=0)
    show_rate_us_count = models.IntegerField(default=15)
    is_discover_settings_everyone = models.BooleanField(default=True)
    fb_work_id = models.CharField(max_length=255, null=True, blank=True)
    fb_work_name = models.CharField(max_length=255, null=True, blank=True)
    fb_education_id = models.CharField(max_length=255, null=True, blank=True)
    fb_education_name = models.CharField(max_length=255, null=True, blank=True)
    num_notifs_sent_per_day = models.IntegerField(default=0)
    meeting_room_credits = models.IntegerField(default=1000)
    used_credits = models.IntegerField(default=0)
    bonus_credits = models.IntegerField(default=0)
    popularity = models.IntegerField(default=-1)
    initial_notifs_sent = models.BooleanField(default=False)
    go_offline = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    online_status_timestamp = models.DateTimeField(null=True, blank=True)
    min_friends_not_required = models.BooleanField(default=False)
    receive_chat_request = models.BooleanField(default=True)
    chat_req_receive_limit = models.IntegerField(default=5)
    # num_posts_created = models.IntegerField(default=False)
    # num_comments_created = models.IntegerField(default=False)
    # is_inactive_user = models.IntegerField(default=False)
    max_friend_requests_per_day = models.IntegerField(default=10)
    views = models.BigIntegerField(default=0)
    total_thanks = models.BigIntegerField(default=0)
    total_likes = models.BigIntegerField(default=0)
    total_followers = models.BigIntegerField(default=0)
    total_following = models.BigIntegerField(default=0)
    client_type = models.CharField(default='android', max_length=100)
    total_friends = models.IntegerField(default=0)
    last_my_feed_post_id = models.IntegerField(null=False, default=False)
    is_status_default = models.BooleanField(default=True)
    community = models.ManyToManyField('Community', null=True, blank=True, related_name='community')
    blacklisted_community = models.ManyToManyField('Community', null=True, blank=True,
                                                   through='MyuserBlacklistedCommunity',
                                                   through_fields=('myuser', 'community'),
                                                   related_name='myuserblacklistedcommunity')
    otp = models.CharField(max_length=50, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    mac = models.CharField(max_length=255, blank=True, null=True)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    model = models.CharField(max_length=255, blank=True, null=True)
    device_data = models.CharField(max_length=255, blank=True, null=True)
    email_address = models.CharField(max_length=255, blank=True, null=True)
    official_email = models.CharField(max_length=255, blank=True, null=True)
    apartment_tower = models.CharField(max_length=255, blank=True, null=True)
    apartment_flat_number = models.CharField(max_length=255, blank=True, null=True)
    house_id = models.CharField(max_length=15, blank=True, null=True, db_index=True)
    hide_apartment_flat_details = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    num_posts = models.BigIntegerField(default=0)
    num_comments = models.BigIntegerField(default=0)
    num_meetups = models.BigIntegerField(default=0)
    fb_uid = models.BigIntegerField(default=0)
    shake_count = models.BigIntegerField(default=0)
    referral_code = models.CharField(max_length=255, null=True, blank=True)
    shake_option = models.BooleanField(default=True)
    year_of_graduation = models.IntegerField(blank=True, null=True)
    year_of_admission = models.IntegerField(blank=True, null=True)
    work_status = models.BooleanField(default=True)
    work_designation = models.CharField(max_length=255, blank=True, null=True)
    free_until_time = models.DateTimeField(null=True, blank=True)
    previous_login = models.DateTimeField(null=True, blank=True)
    access_token = models.TextField(blank=True, null=True)
    show_age = models.BooleanField(default=True)
    uninstalled = models.BooleanField(default=False)
    num_referrals = models.IntegerField(default=0)
    sdk_type = models.CharField(max_length=50, default='')
    client_auth_data = models.TextField(blank=True, null=True)
    skills = models.ManyToManyField('Skill', null=True, blank=True)
    nps_survey_completed = models.BooleanField(default=False)
    num_user_created_groups = models.IntegerField(default=0)
    tenant_id = models.CharField(max_length=50, null=True, blank=True, default='')
    is_active_tenant = models.NullBooleanField(null=True, blank=True)
    user_tag = models.CharField(max_length=50, choices=USER_TAGS().get_choices(), null=True, blank=True, default='')
    is_dashboard_admin = models.BooleanField(default=False)
    sdk_login_state = models.BooleanField(default=True)
    is_guest_user = models.BooleanField(default=False)
    admin_interests = models.TextField(blank=False, null=False, default='')
    program_interests_order = models.TextField(blank=False, null=False, default='')
    objects = UserManager()

    class Meta:
        app_label = 'webapp'

    def __unicode__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.id:
            self.last_activity_time = datetime.now()
            self.uuid = uuid.uuid4()

            # Manually setting up auth type on 'create_user_record_by_phone' method on signup
            # self.auth_type = 'facebook'

            # Remove default country and city as India, Bengaluru
            # Set country as 'India' by default
            # self.country_place_ref = Place.objects.get(pk=2914)

            # Set city to 'Bangalore' by default
            # self.city_place_ref = Place.objects.get(pk=2)

            # Set default prev login field
            self.last_login = datetime.now()
            self.previous_login = datetime.now()

        return super(MyUser, self).save(*args, **kwargs)

    def get_profile_picture(self, is_large=False):

        if self.profile_picture_ref:
            if is_large:
                return self.profile_picture_ref.get_profile_picture_large()
            else:
                return self.profile_picture_ref.get_profile_picture()
        else:
            profile_picture_ref = ProfilePicture.objects.filter(user__id=self.id, is_default=True).first()
            if profile_picture_ref:
                return profile_picture_ref.get_profile_picture()
            else:
                return "https://d267x6x6dh1ejh.cloudfront.net/profile_pictures/aac2e403-afd3-4746-aae7-c397cd45547a.png"

    def get_age(self):
        """ method to get the age of the user"""
        user_birthday = self.birthday
        if user_birthday:
            days_in_year = 365.2425
            age = int((date.today() - user_birthday).days / days_in_year)
            return age
        else:
            return ''

    def get_full_name(self):
        """ method to get the age of the user"""
        if self.first_name and self.last_name:
            return '{0} {1}'.format(self.first_name, self.last_name)
        elif self.first_name:
            return self.first_name
        else:
            return ''

    def is_blacklisted(self):
        """ this method is used to check the user is blacklisted or not """
        if self.blacklisted_community.all().count() > 0:
            return True
        return False

    def get_news_category_order(self):
        news_category_ids = []
        if self.admin_interests:
            news_category_ids = self.admin_interests.split(',')
            news_category_ids = filter(None, news_category_ids)
        return news_category_ids

    def get_program_category_order(self):
        program_category_ids = []
        if self.program_interests_order:
            program_category_ids = self.program_interests_order.split(',')
            program_category_ids = filter(None, program_category_ids)
        return program_category_ids


MyUser._meta.get_field('email').null = True
MyUser._meta.get_field('email').blank = True
MyUser._meta.get_field('username').null = True
MyUser._meta.get_field('username').blank = True


class ProfilePicture(models.Model):
    profile_picture = models.ImageField(upload_to=upload_users_to, null=True, blank=True)
    profile_picture_large = models.ImageField(upload_to=upload_users_to, null=True, blank=True)
    user = models.ForeignKey('MyUser', null=True, blank=True)
    is_default = models.BooleanField(default=False)
    is_facebook_dp = models.BooleanField(default=False)
    is_insta_dp = models.BooleanField(default=False)
    is_google_dp = models.BooleanField(default=False)
    original_source_url = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        self.modified = datetime.now()
        return super(ProfilePicture, self).save(*args, **kwargs)

    def create_optimal_image(self):
        basewidth = 160
        profile_picture_large_path = self.profile_picture_large.name

        if not profile_picture_large_path:
            return

        base_path = 'profile_pictures/'
        disassembled = urlparse(profile_picture_large_path)
        filename, file_ext = splitext(basename(disassembled.path))
        profile_picture_path = base_path + str(uuid.uuid4()) + file_ext

        try:
            f = storage.open(profile_picture_large_path, 'r')
            image = Image.open(f)
            width = image.size[0]
            height = image.size[1]
            wpercent = (basewidth / float(image.size[0]))
            hsize = int((float(height) * float(wpercent)))
            image = image.resize((basewidth, hsize), Image.ANTIALIAS)

            f_thumb = storage.open(profile_picture_path, "w")
            image.save(f_thumb)
            f_thumb.close()
            self.profile_picture = profile_picture_path
            self.save()
        except:
            pass

    def get_profile_picture(self):
        file_path = self.profile_picture.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return 'https://d267x6x6dh1ejh.cloudfront.net/profile_pictures/aac2e403-afd3-4746-aae7-c397cd45547a.png'

    def get_profile_picture_large(self):
        file_path = self.profile_picture_large.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return 'https://d267x6x6dh1ejh.cloudfront.net/profile_pictures/aac2e403-afd3-4746-aae7-c397cd45547a.png'

    def __unicode__(self):
        if self.user:
            return str(self.user.username)
        else:
            return str(self.profile_picture)


class Community(models.Model):
    name = models.CharField(max_length=255, unique=True)
    registered_brand_name = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    banner_image = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    app_icon = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    invite_icon = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    ui_theme = models.ForeignKey('UITheme', related_name='community_ui_theme', null=True, blank=True)
    ui_theme_sdk = models.ForeignKey('UITheme', related_name='community_ui_theme_sdk', null=True, blank=True)
    is_hidden = models.BooleanField(default=False)
    email_alias = models.CharField(max_length=255, unique=True, default="")
    unique_code = models.CharField(max_length=255, null=True, blank=True)
    sub_domain = models.CharField(max_length=255, null=True, blank=True)
    custom_domain = models.CharField(max_length=255, null=True, blank=True)
    share_link_code = models.CharField(max_length=255, null=True, blank=True)
    community_type = models.CharField(max_length=25, choices=CommunityType().get_choices(), null=True, blank=True)
    languages = models.ManyToManyField('Language', null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    num_users = models.IntegerField(default=0)
    num_days_to_verify_account = models.IntegerField(default=6)
    education_ref = models.ForeignKey('Education', null=True, blank=True, related_name='community_education_ref',
                                      on_delete=models.SET_NULL)
    workplace_ref = models.ForeignKey('WorkPlace', null=True, blank=True, related_name='community_workplace_ref',
                                      on_delete=models.SET_NULL)
    workplace_locations = models.TextField(null=True, blank=True)
    college_locations = models.TextField(null=True, blank=True)
    apartment_towers = models.TextField(blank=True, null=True)
    branches = models.TextField(blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    is_apna_complex = models.BooleanField(default=False)
    onboarding_screens = models.TextField(blank=False, null=False,
                                          default='WELCOME_SCREEN,COLLECT_NAME,COLLECT_GENDER,COLLECT_DOB,COLLECT_AREA,COLLECT_HOMETOWN,COLLECT_COLLEGE,COLLECT_WORKPLACE,COLLECT_PROFILE_PIC,COLLECT_INTERESTS',
                                          help_text=OnboardingScreens().get_str_list())
    user_profile_infos = models.TextField(blank=False, null=False,
                                          default='INFO_CURRENT_CITY,INFO_HOME_TOWN,INFO_EDUCATION,INFO_WORKPLACE',
                                          help_text=ProfileInfo().get_str_list())
    discover_profile_infos = models.TextField(blank=False, null=False,
                                              default='INFO_CURRENT_CITY,INFO_HOME_TOWN,INFO_EDUCATION,INFO_WORKPLACE',
                                              help_text=ProfileInfo().get_str_list())
    profile_sections_order = models.TextField(blank=False, null=False,
                                              default='ABOUT_SECTION,USER_MEDIA_SECTION,INTERESTS_SECTION,SKILLS_SECTION,PROMPTS_SECTION',
                                              help_text=ProfileUISections().get_str_list())
    activities = models.TextField(blank=False, null=False,
                                  default='12,20,17,30,45,31,41,18,33,21,25,51,42,40,37,35,39,52,48,46,43,38,36,32,26,24,22,56,55,54,53,50,49,34,29,27,23')
    post_activities = models.TextField(blank=False, null=False, default='59,60,61,62,63,64,65,66,67,68,69')
    work_designations = models.TextField(null=True, blank=True)
    community_interests = models.TextField(blank=False, null=False,
                                           default='4,17,86,13,28,10,22,9,80,7,70,109,107,75,6,3,72,18,5,108,20,15,79,8,32,90,82,25,1,12,77,74,64,83,35,96,81,65,84,88,34,27,106,73')
    create_post_interests = models.TextField(blank=False, null=False,
                                             default='1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,25,27,28,29,30,31,32,33,34,35,36,37,38,39,59,64,65,66,68,69,70,71,72,73,74,75,77,78,79,81,82,83,84,86,88,89,90,98,99,102,104,105,106,107,108,109')
    create_post_tags = models.TextField(blank=True, null=True, default='')
    program_interests = models.TextField(blank=True, null=True, default='')
    skills = models.TextField(blank=False, null=False, default='1,2,3,4,5,6,7,8,9,10')
    admin_interests = models.TextField(blank=False, null=False, default='110,112,115,116,114,111,117')
    profile_prommpts = models.TextField(blank=True, null=True, default='')
    fix_admin_interests = models.BooleanField(default=True)
    show_fb_post_option = models.BooleanField(default=False)
    show_fb_comments_on_post_details = models.BooleanField(default=False)
    show_fb_post_on_feed = models.BooleanField(default=False)
    show_custom_gifs = models.BooleanField(default=False)
    show_meetup_location = models.BooleanField(default=True)
    show_powered_by_glynk = models.BooleanField(default=True)
    enable_meetup_shake = models.BooleanField(default=True)
    enable_cp_tags = models.BooleanField(default=False)
    enable_cp_moderation = models.BooleanField(default=False)
    enable_invite = models.BooleanField(default=True)
    feed_filters = models.TextField(blank=True, null=True, default='', help_text=FeedContentType().get_str_list())
    meetup_type = models.CharField(max_length=20, choices=(('LIVE', 'LIVE'), ('MEETUP', 'MEETUP'), ('EVENT', 'EVENT')),
                                   default='MEETUP')
    feed_tab_type = models.CharField(max_length=20, choices=(('FEED', 'FEED'), ('NEWS', 'NEWS')), default='FEED')
    enable_theme_interest_tag = models.BooleanField(default=False)
    allow_users_to_create_polls = models.BooleanField(default=True)
    email_verification_required = models.BooleanField(default=False)
    show_create_post_prompts = models.BooleanField(default=True)
    invite_url = models.CharField(max_length=255, null=True, blank=True)
    sdk_invite_url = models.CharField(max_length=255, null=True, blank=True)
    enable_reports = models.BooleanField(default=False)
    places = models.ManyToManyField('Place', null=True, blank=True, default=list([2914]))
    daily_gc_title = models.CharField(max_length=255, null=True, blank=True)
    daily_gc_text = models.TextField(blank=True, null=True)
    daily_gc_entry_question = models.TextField(blank=True, null=True)
    daily_gc_image = models.ImageField(upload_to=upload_posts_to, null=True, blank=True)
    api_key = models.CharField(max_length=255, null=True, blank=True)
    meta_data = models.TextField(blank=True, null=True)
    default_tab = models.CharField(max_length=25, choices=DefaultTab().get_choices(), default="INTERACT")
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')
    play_store_url = models.CharField(max_length=255, default="", blank=True)
    app_store_url = models.CharField(max_length=255, default="", blank=True)
    community_play_store_url = models.CharField(max_length=255, default="", blank=True)
    about_url = models.CharField(max_length=255, default="", blank=True, null=True)
    terms_url = models.CharField(max_length=255, default="", blank=True, null=True)
    privacy_url = models.CharField(max_length=255, default="", blank=True, null=True)
    deeplink_url_groups = models.CharField(max_length=255, default="", blank=True, null=True)
    nps_survey_session = models.IntegerField(default=5)
    enable_nps_survey = models.BooleanField(default=False)
    create_automated_groups = models.BooleanField(default=True)
    add_community_icon = models.BooleanField(default=False)
    has_buildings = models.BooleanField(default=False)
    skip_hometown_onbd = models.BooleanField(default=False)
    skip_workplace_onbd = models.BooleanField(default=False)
    skip_college_onbd = models.BooleanField(default=False)
    show_open_in_app = models.BooleanField(default=False)
    show_gallery_in_feed = models.BooleanField(default=True)
    max_user_created_groups = models.IntegerField(default=10)
    login_options = models.TextField(blank=False, null=False, default='phone_number', help_text='phone_number,email')
    min_android_app_version = models.IntegerField(default=7)
    latest_android_app_version = models.IntegerField(default=7)
    min_ios_app_version = models.IntegerField(default=7)
    latest_ios_app_version = models.IntegerField(default=7)
    sdk_open_in_app_link = models.CharField(max_length=255, default='', blank=True, null=True)
    sdk_show_create_groups = models.BooleanField(default=True)
    sdk_show_search_groups = models.BooleanField(default=True)
    show_search_groups = models.BooleanField(default=True)
    sdk_use_parent_app_profile = models.BooleanField(default=False)
    sdk_allow_update_profile_info = models.BooleanField(default=True)
    show_members_list_bar = models.BooleanField(default=True)
    show_timestamp_on_feed = models.BooleanField(default=False)
    show_members_count = models.BooleanField(default=True)
    show_skills = models.BooleanField(default=True)
    send_group_message_notification = models.BooleanField(default=False)
    enable_new_member_notification = models.BooleanField(default=True)
    enable_add_bio_notification = models.BooleanField(default=True)
    enable_interest_post_notification = models.BooleanField(default=False)
    enable_meetups_distance_filter = models.BooleanField(default=True)

    # admin_section_layout field is used to set how the admin tiles should look.
    # We support Interest layout with image and Tile layout with icon. In cove we use TILES Layout.
    admin_section_layout = models.CharField(max_length=20, choices=(('TILES', 'TILES'), ('INTEREST', 'INTEREST')),
                                            default='TILES')

    # The below four fields are only temp, we need to move this to a KV database sometime in the future.
    # The only reason we did not create a KV database at the time of this implementation is because we were about to
    # move to a different AWS account and adding a new infra at this time will complicate the move.
    access_token_sys1 = models.TextField(default='', blank=False, null=False)
    refresh_token_sys1 = models.TextField(default='', blank=False, null=False)
    access_token_sys2 = models.TextField(default='', blank=False, null=False)
    refresh_token_sys2 = models.TextField(default='', blank=False, null=False)
    discover_profile_card_type = models.CharField(max_length=250, choices=DISCOVER_PROFILE_CARD_TYPE().get_choices(),
                                                  null=True, blank=True, default="RICH")
    whitelist_numbers = models.TextField(blank=True, null=True)
    whitelist_domains = models.TextField(blank=True, null=True)
    chat_support_user = models.ForeignKey('MyUser', null=True, blank=True, related_name='community_chat_support_user')
    chat_support_hook_url = models.CharField(max_length=255, null=True, blank=True)
    create_complaint_hook_url = models.CharField(max_length=255, null=True, blank=True)
    create_complaint_comment_hook_url = models.CharField(max_length=255, null=True, blank=True)
    chat_support_channel = models.CharField(max_length=20, choices=ChatSupportChannel().get_choices(),
                                            default=ChatSupportChannel().GLYNK)
    email_report_recipients = models.TextField(blank=True, null=True)
    user_tags = models.TextField(blank=True, null=True)
    enable_guest_login = models.BooleanField(default=False)
    show_profile_stats = models.BooleanField(default=True)
    show_user_in_gallery = models.BooleanField(default=True)
    show_add_to_gallery = models.BooleanField(default=True)
    show_login_success_popup = models.BooleanField(default=False)
    show_gdpr_info = models.BooleanField(default=True)
    allow_user_create_post = models.BooleanField(default=True)
    show_create_group = models.BooleanField(default=True)
    enable_connection_requests = models.BooleanField(default=True)
    enable_email_notification = models.BooleanField(default=True)
    enable_activity_notification = models.BooleanField(default=True)
    show_privacy_setting = models.BooleanField(default=True)
    show_app_setting = models.BooleanField(default=True)
    show_notification_setting = models.BooleanField(default=True)
    show_loading_messages = models.BooleanField(default=True)
    enable_complaint_comments = models.BooleanField(default=True)
    show_explore_groups = models.BooleanField(default=True)
    enable_invite_only_access = models.BooleanField(default=False)
    enable_social_notification = models.BooleanField(default=True)
    content_language_filter = models.BooleanField(default=False)
    ga_tracking_id = models.CharField(max_length=255, null=True, blank=True, default='')
    og_image = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    og_title = models.TextField(blank=True, null=True)
    og_description = models.TextField(blank=True, null=True)

    show_footer_banner = models.BooleanField(default=False)
    footer_banner_cta_link = models.TextField(null=True, blank=True, default='')
    footer_banner_icon = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    jobs_image = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    enable_ads = models.BooleanField(default=False) # This attribute used to enable or disable ads in web
    google_adsense_id = models.CharField(max_length=255,blank=True, null=True, default='')# Field for google adsense id
    enable_google_ads = models.BooleanField(default=False)
    enable_ads_post_mobile_web = models.BooleanField(default=True)
    enable_ads_post_desktop_web = models.BooleanField(default=True)
    facebook_page_url = models.CharField(max_length=255, blank=True, default="")
    instagram_page_url = models.CharField(max_length=255, blank=True, default="")
    twitter_page_url = models.CharField(max_length=255, blank=True, default="")
    linkedin_page_url = models.CharField(max_length=255, blank=True, default="")
    enable_widgets = models.BooleanField(default=False)

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()

        self.modified = datetime.now()

        return super(Community, self).save(*args, **kwargs)

    def get_banner_image(self):
        file_path = self.banner_image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return "https://d267x6x6dh1ejh.cloudfront.net/questions/b30565be-0029-4432-9507-f03521d8de71.jpg"

    def get_image(self):
        file_path = self.image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return "https://d267x6x6dh1ejh.cloudfront.net/questions/b30565be-0029-4432-9507-f03521d8de71.jpg"

    def get_app_icon_image(self):
        if self.app_icon.name:
            file_path = self.app_icon.name
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        elif self.image.name:
            file_path = self.image.name
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return "https://d267x6x6dh1ejh.cloudfront.net/posts/770eb818-0185-44c7-819a-7c4d1d050311.png"

    def get_invite_icon(self):
        if not self.invite_icon:
            return ''

        file_path = self.invite_icon.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(str(file_path))
            return storage.url(filename_base) + filename_ext
        else:
            return ''

    def get_registered_brand_name(self):
        if not self.registered_brand_name:
            return 'Glynk'

        return self.registered_brand_name

    def get_onboarding_screens(self):
        onboarding_screens_list = []
        if self.onboarding_screens:
            onboarding_screens_list = self.onboarding_screens.split(',')
            onboarding_screens_list = filter(None, onboarding_screens_list)
        return onboarding_screens_list

    def get_whitelist_numbers(self):
        whitelist_numbers = []
        if self.whitelist_numbers:
            whitelist_numbers = self.whitelist_numbers.split(',')
            whitelist_numbers = filter(None, whitelist_numbers)
        return whitelist_numbers

    def get_whitelist_domains(self):
        whitelist_domains = []
        if self.whitelist_domains:
            whitelist_domains = self.whitelist_domains.split(',')
            whitelist_domains = filter(None, whitelist_domains)
        return whitelist_domains

    def get_user_profile_infos(self):
        user_profile_infos = []
        if self.user_profile_infos:
            user_profile_infos = self.user_profile_infos.split(',')
            user_profile_infos = filter(None, user_profile_infos)
        return user_profile_infos

    def get_discover_profile_infos(self):
        discover_profile_infos = []
        if self.discover_profile_infos:
            discover_profile_infos = self.discover_profile_infos.split(',')
            discover_profile_infos = filter(None, discover_profile_infos)
        return discover_profile_infos

    def get_profile_sections_order(self):
        profile_sections_order = []
        if self.profile_sections_order:
            profile_sections_order = self.profile_sections_order.split(',')
            profile_sections_order = filter(None, profile_sections_order)
        return profile_sections_order

    def get_profile_prompts(self):
        profile_prompts_ids = []
        if self.profile_prommpts:
            profile_prompts_ids = self.profile_prommpts.split(',')
            profile_prompts_ids = filter(None, profile_prompts_ids)
        return profile_prompts_ids

    def get_community_interests(self):
        community_interests_ids = []
        if self.community_interests:
            community_interests_ids = self.community_interests.split(',')
            community_interests_ids = filter(None, community_interests_ids)
        return community_interests_ids

    def get_community_admin_interests(self):
        admin_interests_ids = []
        if self.admin_interests:
            admin_interests_ids = self.admin_interests.split(',')
            admin_interests_ids = filter(None, admin_interests_ids)
        return admin_interests_ids

    def get_community_program_interests(self):
        program_interests_ids = []
        if self.program_interests:
            program_interests_ids = self.program_interests.split(',')
            program_interests_ids = filter(None, program_interests_ids)
        return program_interests_ids

    def get_feed_filters(self):
        feed_filters = []
        if self.feed_filters:
            feed_filters = self.feed_filters.split(',')
            feed_filters = filter(None, feed_filters)
        return feed_filters

    def __unicode__(self):
        return self.name

    def get_email_report_recipients(self):
        email_report_recipients = []
        if self.email_report_recipients:
            email_report_recipients = self.email_report_recipients.split(',')
            email_report_recipients = filter(None, email_report_recipients)
        return email_report_recipients

    def get_user_tags(self):
        user_tags = []
        if self.user_tags:
            user_tags = self.user_tags.split(',')
            user_tags = filter(None, user_tags)
        return user_tags

    def get_og_image(self):
        file_path = self.og_image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base)+filename_ext
        else:
            return "https://d267x6x6dh1ejh.cloudfront.net/questions/b30565be-0029-4432-9507-f03521d8de71.jpg"

    def get_footer_banner_icon(self):
        file_path = self.footer_banner_icon.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base)+filename_ext
        else:
            return ""

    def get_jobs_image(self):
        file_path = self.jobs_image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base)+filename_ext
        else:
            return ""

class CommunityConfigurations(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    community = models.ForeignKey('Community', null=True, blank=True)
    filter_parameter = models.CharField(max_length=255, null=True, blank=True)
    admin_interests = models.TextField(blank=False, null=False, default='110,112,115,116,114,111,117')
    program_interests = models.TextField(blank=True, null=True, default='')

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()

        self.modified = datetime.now()

        return super(CommunityConfigurations, self).save(*args, **kwargs)

    def __unicode__(self):
        name = str(self.created)

        if self.community:
            name = self.community.name
            if self.filter_parameter:
                name = name + ' ' + self.filter_parameter
            return name

    def get_community_admin_interests(self):
        admin_interests_ids = []
        if self.admin_interests:
            admin_interests_ids = self.admin_interests.split(',')
            admin_interests_ids = filter(None, admin_interests_ids)
        return admin_interests_ids

    def get_community_program_interests(self):
        program_interests_ids = []
        if self.program_interests:
            program_interests_ids = self.program_interests.split(',')
            program_interests_ids = filter(None, program_interests_ids)
        return program_interests_ids


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)
    unique_id = models.CharField(max_length=255, null=True, blank=True)
    polls = models.ManyToManyField('Poll', null=True, blank=True, related_name='topic_polls')
    image = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    sites = models.ManyToManyField('Site', null=True, blank=True)
    rank = models.IntegerField(default=0)
    score = models.BigIntegerField(default=0)
    trending_score = models.BigIntegerField(default=0)
    type = models.CharField(max_length=20, choices=TOPIC_TYPE_CHOICES().get_choices(), default=TOPIC_TYPE_CHOICES.TAG)
    related_topics = models.ManyToManyField('Topic', null=True, blank=True)
    people_to_meet = models.ForeignKey('PeopleToMeet', null=True, blank=True)
    color_code = models.CharField(max_length=10, default='666666')
    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        app_label = 'webapp'

    def get_image(self):
        file_path = self.image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return "https://d267x6x6dh1ejh.cloudfront.net/polls/20141025221704.png"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
            self.unique_id = re.sub('[^A-Za-z0-9]+', '_', self.name)

        self.modified = datetime.now()

        return super(Topic, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Poll(models.Model):
    created_by = models.ForeignKey('MyUser', null=True, blank=True)
    question = models.TextField()
    poll_image = models.ImageField(upload_to=upload_questions_to, null=True, blank=True)
    community = models.ForeignKey('Community', null=True, blank=True)
    end_date = models.DateTimeField(blank=True, null=True)
    privacy_type = models.CharField(choices=PRIVACY_TYPE_CHOICES, default='FRIENDS', max_length=30)
    country = models.CharField(max_length=255, null=True, blank=True)
    unique_url = models.CharField(max_length=255)
    is_anonymous = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_homepage = models.BooleanField(default=False)
    is_usercreated = models.BooleanField(default=False)
    is_predicted = models.BooleanField(default=False)
    is_announcement = models.BooleanField(default=False)
    winning_option = models.ForeignKey('Option', null=True, blank=True, related_name='winning_option')
    total_votes = models.BigIntegerField(default=0)
    shares = models.BigIntegerField(default=0)
    likes = models.BigIntegerField(default=0)
    comments = models.BigIntegerField(default=0)
    views = models.BigIntegerField(default=0)
    seo_description = models.TextField(blank=True, null=True)
    seo_keywords = models.TextField(blank=True, null=True)
    robots = models.CharField(max_length=100, null=True, blank=True)
    short_title = models.TextField(null=True, blank=True)
    score = models.IntegerField(default=0)
    active_user_score = models.IntegerField(default=0)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    voted = models.DateTimeField()
    sites = models.ManyToManyField('Site', null=True, blank=True)
    not_approval_element = models.CharField(max_length=100, null=True, blank=True)
    not_approval_reason = models.TextField(null=True, blank=True)
    nickname = models.CharField(max_length=100, default='', null=True, blank=True)
    background_color = models.CharField(max_length=100, null=True, blank=True)
    image = models.ForeignKey('Media', null=True, blank=True, related_name='images')
    prediction_winning_points = models.IntegerField(default=2)
    prediction_losing_points = models.IntegerField(default=2)
    prediction_missed_points = models.IntegerField(default=1)
    prev_topic = models.ForeignKey('Topic', null=True, blank=True)
    requires_moderation = models.BooleanField(default=False)
    moderation_reason = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-modified", "-total_votes"]
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
            self.voted = datetime.now()
        self.modified = datetime.now()
        return super(Poll, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return '/polls/' + str(self.unique_url)

    def get_image(self):
        if not self.poll_image:
            return ''

        file_path = self.poll_image.name
        if file_path:
            return storage.url(file_path)
        else:
            return ''

    def __unicode__(self):
        return self.question


class PollComment(models.Model):
    created_by = models.ForeignKey('MyUser', null=True, blank=True)
    poll = models.ForeignKey('Poll', null=False, blank=False)
    text = models.TextField()
    text_len = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    likes = models.BigIntegerField(default=0)
    spam = models.BigIntegerField(default=0)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    preview_image = models.ImageField(upload_to=upload_posts_to, null=True, blank=True)
    preview_title = models.CharField(max_length=255, null=True, blank=True)
    preview_source = models.CharField(max_length=255, null=True, blank=True)
    preview_link = models.CharField(max_length=255, null=True, blank=True)
    community = models.ManyToManyField('Community', null=True, blank=True)
    is_hidden = models.BooleanField(default=0)
    is_video = models.BooleanField(default=0)
    entry_point = models.CharField(max_length=100, null=True, blank=True, default='')
    fb_comment_id = models.CharField(max_length=255, null=True, blank=True)
    user_mentions = models.TextField(null=True, blank=True)
    requires_moderation = models.BooleanField(default=False)
    moderation_reason = models.TextField(null=True, blank=True)

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        self.modified = datetime.now()
        self.text_len = len(self.text)
        return super(PollComment, self).save(*args, **kwargs)

    def get_preview_image(self):
        file_path = self.preview_image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)

            if filename_ext == '.cms':
                return storage.url(filename_base) + filename_ext

            return storage.url(filename_base) + filename_ext
        else:
            return ''

    def __unicode__(self):
        return self.text


class Friendship(models.Model):
    user = models.ForeignKey('MyUser', related_name='user')
    follower = models.ForeignKey('MyUser', related_name='follower')
    type = models.CharField(max_length=20, choices=FRIENDSHIP_TYPE_CHOICES, default='NONE')
    connected = models.BooleanField(default=False)
    other_system = models.CharField(max_length=20, null=True, blank=True)
    is_autocreated = models.BooleanField(default=False)

    class Meta:
        app_label = 'webapp'

    def __unicode__(self):
        return self.user.email


class UserTopic(models.Model):
    user = models.ForeignKey('MyUser', related_name='usertopic_user')
    topic = models.ForeignKey('Topic', related_name='usertopic_topic')
    is_following = models.BooleanField(default=False)
    number_of_questions_answered = models.IntegerField(default=0)

    class Meta:
        app_label = 'webapp'

    def __unicode__(self):
        return self.user.email


class Option(models.Model):
    poll = models.ForeignKey('Poll')
    option = models.TextField()
    votes = models.BigIntegerField(default=0)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    user = models.ManyToManyField('MyUser', null=True, blank=True)
    rank = models.IntegerField(default=0)

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        self.modified = datetime.now()
        super(Option, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.option


class UserOpinion(models.Model):
    poll = models.ForeignKey('Poll')
    option = models.ForeignKey('Option')
    user = models.ForeignKey('MyUser')
    created = models.DateTimeField()

    class Meta:
        unique_together = ('poll', 'user')
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        super(UserOpinion, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.email


class Media(models.Model):
    poll = models.ForeignKey('Poll', null=True, blank=True)
    image = models.ImageField(upload_to=upload_questions_to, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    resized_height = models.FloatField(default=0.0)
    height = models.FloatField(default=0.0)
    click = models.BooleanField(default=False)
    youtube = models.TextField(blank=True, null=True)
    media_type = models.CharField(max_length=10, default='IMAGE')

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        super(Media, self).save(*args, **kwargs)

        if self.media_type == 'IMAGE':
            self.create_thumbs()

        if self.youtube is not None:
            if self.youtube.startswith("https"):
                self.youtube = self.youtube.replace("https://www.youtube.com/watch?v=", "")

    # This function makes sure that create_thumbs method does not get called again when save is called within
    # create_thumbs.
    def save_without_other_images(self, *args, **kwargs):
        super(Media, self).save(*args, **kwargs)

    def create_thumbs(self):
        basewidth = settings.IMAGE_BASE_WIDTH
        file_path = self.image.name
        if not file_path:
            return
        filename_base, filename_ext = os.path.splitext(file_path)
        thumb_file_path = "%s_optimal%s" % (filename_base, filename_ext)
        try:
            f = storage.open(file_path, 'r')
            image = Image.open(f)

            wpercent = (basewidth / float(image.size[0]))
            hsize = int((float(image.size[1]) * float(wpercent)))
            image = image.resize((basewidth, hsize), Image.ANTIALIAS)

            f_thumb = storage.open(thumb_file_path, "w")
            image.save(f_thumb)
            f_thumb.close()

            self.height = image.size[1]
            self.resized_height = hsize
            self.save_without_other_images()
        except:
            pass

    def __unicode__(self):
        if self.media_type == 'IMAGE':
            from django.core.files.storage import default_storage as storage
            file_path = self.image.name
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        elif self.media_type == 'VIDEO':
            return self.youtube
        else:
            return "NONE"

class Post(models.Model):
    external_post_id = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey('MyUser', null=True, blank=True, related_name='post_created_by')
    topic = models.ForeignKey('Topic', null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    new_title = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    label = models.CharField(max_length=255, null=True, blank=True, default='')
    text_len = models.IntegerField(default=0)
    unique_url = models.CharField(max_length=255)
    shares = models.BigIntegerField(default=0)
    likes = models.BigIntegerField(default=0)
    comments = models.BigIntegerField(default=0)
    spam = models.BigIntegerField(default=0)
    score = models.BigIntegerField(default=1)
    type = models.CharField(choices=POST_TYPES, max_length=100, null=True, default='DISCUSS')
    poll = models.ForeignKey('Poll', null=True, blank=True)
    event = models.ForeignKey('Meetup', null=True, blank=True, on_delete=models.SET_NULL)
    activity = models.ForeignKey('Activity', null=True, blank=True, on_delete=models.SET_NULL)
    people_to_meet = models.ManyToManyField('PeopleToMeet', null=True, blank=True)
    sub_interest = models.ForeignKey('SubInterest', null=True, blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    edited_datetime = models.DateTimeField(null=True, blank=True)
    action_datetime = models.DateTimeField(null=True, blank=True)
    offer_start_date = models.DateField(null=True, blank=True)
    offer_end_date = models.DateField(null=True, blank=True)
    privacy = models.CharField(max_length=50, choices=POST_PRIVACY().get_choices(), default='ALL')
    college = models.ForeignKey('College', null=True, blank=True)
    image = models.ImageField(upload_to=upload_posts_to, null=True, blank=True)
    is_image_compressed = models.BooleanField(default=1)
    preview_image = models.ImageField(upload_to=upload_posts_to, null=True, blank=True)
    original_preview_image = models.TextField(null=True, blank=True)
    preview_title = models.CharField(max_length=255, null=True, blank=True)
    preview_source = models.CharField(max_length=255, null=True, blank=True)
    preview_source_icon = models.ImageField(upload_to=upload_posts_to, null=True, blank=True)
    preview_link = models.CharField(max_length=255, null=True, blank=True)
    is_usercreated = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=0)
    places = models.ManyToManyField('Place', null=True, blank=True)
    is_mandatory_post = models.BooleanField(default=False)
    external_source = models.CharField(max_length=255, null=True, blank=True)
    external_source_id = models.CharField(max_length=255, null=True, blank=True)
    external_integration = models.CharField(max_length=255, null=True, blank=True)
    external_integration_id = models.CharField(max_length=255, null=True, blank=True)
    mcp_notif_sent = models.BooleanField(default=False)
    is_video = models.BooleanField(default=False)
    is_announcement = models.BooleanField(default=False)
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    book_author = models.CharField(max_length=255, null=True, blank=True)
    height = models.FloatField(default=0.0)
    width = models.FloatField(default=0.0)
    resized_height = models.FloatField(default=0.0)
    resized_width = models.FloatField(default=0.0)
    preview_height = models.FloatField(default=0.0)
    preview_width = models.FloatField(default=0.0)
    resized_preview_height = models.FloatField(default=0.0)
    resized_preview_width = models.FloatField(default=0.0)
    is_big_preview_image = models.BooleanField(default=False)
    views = models.BigIntegerField(default=0)
    status = models.CharField(max_length=20, choices=POST_STATUS, default='ACTIVE')
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    locations = models.CharField(max_length=255, null=True, blank=True)
    background_color = models.CharField(max_length=100, null=True, blank=True)
    temp_old_type = models.CharField(choices=POST_TYPES, max_length=100, null=True, default='DISCUSS')
    ready_to_push = models.BooleanField(default=False)
    is_new_user_push_notif = models.BooleanField(default=False)
    new_user_push_notif_text = models.TextField(null=True, blank=True)
    community = models.ManyToManyField('Community', null=True, blank=True)
    comments_enabled = models.BooleanField(default=True)
    entry_point = models.CharField(max_length=100, null=True, blank=True, default = '')
    fb_post_id = models.CharField(max_length=255, null=True, blank=True)
    user_mentions = models.TextField(null=True, blank=True)
    video = models.FileField(upload_to=upload_posts_to, null=True, blank=True)
    price = models.CharField(null=True, blank=True,  default = '', max_length=255)
    is_top_post = models.BooleanField(default=False)
    post_cta = models.CharField(choices=POST_CTA().get_choices(), max_length=100, null=True, default=POST_CTA.NONE)
    post_cta_text = models.CharField(max_length=50, null=True, blank=True)
    post_cta_arg = models.TextField(null=True, blank=True)
    complaint_status = models.CharField(choices=COMPLAINT_STATUS().get_choices(), max_length=100, null=True, default=COMPLAINT_STATUS.NONE)
    complaint_priority = models.CharField(choices=COMPLAINT_PRIORITY().get_choices(), max_length=100, null=True, default=COMPLAINT_PRIORITY.NONE)
    requires_moderation = models.BooleanField(default=False)
    moderation_reason = models.TextField(null=True, blank=True)
    pushed_to_web = models.BooleanField(default=False)
    layout_type = models.CharField(choices=POST_LAYOUT_TYPE().get_choices(), max_length=100, null=True, default=POST_LAYOUT_TYPE.DEFAULT)
    top_post_order_no = models.IntegerField(default=0)
    is_story = models.BooleanField(default=False)
    short_description = models.TextField(null=True, blank=True)
    uploaded_by = models.ForeignKey('MyUser', null=True, blank=True, related_name='post_uploaded_by')
    is_deleted = models.BooleanField(default=False)
    language = models.ForeignKey('Language', null=True, blank=True, default='', on_delete=models.SET_NULL)
    is_anonymous = models.BooleanField(default=False)
    incident_datetime = models.DateTimeField(null=True, blank=True)
    submission_status = models.CharField(max_length=20, choices=SUBMISSION_STATUS().get_choices(), null=True, blank=True)
    is_breaking_news = models.BooleanField(default=False)
    is_trending_news = models.BooleanField(default=False)
    submission_feedback = models.TextField(null=True, blank=True, default='')
    post_tags = models.TextField(null=True, blank=True, default='')
    accepted_solution = models.ForeignKey('PostComment', null=True, blank=True, default='', related_name='post_accepted_solution', on_delete=models.SET_NULL)
    seo_page_title = models.CharField(max_length=255, null=True, blank=True, default='')
    seo_meta_description = models.TextField(null=True, blank=True, default='')
    seo_meta_keywords = models.TextField(null=True, blank=True)
    seo_slug = models.TextField(null=True, blank=True)
    is_featured_post = models.BooleanField(default=False)
    featured_post_date = models.DateTimeField(null=True, blank=True)
    fb_instant_article_response_id = models.CharField(max_length=255, blank=True, null=True, default='')
    unique_id = models.CharField(max_length=20, null=True, blank=True, unique=True)
    admin_approval = models.CharField(max_length=20, choices=ADMIN_APPROVAL, null=True, default='APPROVED')
    bulleted_highlights = models.TextField(null=True, blank=True, default='')
    enable_seo = models.BooleanField(default=True)
    editor_type = models.CharField(max_length=50, choices=POST_EDITOR_TYPE().get_choices(), default=POST_EDITOR_TYPE.DEFAULT)


    class Meta:
        app_label = 'webapp'


    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
            self.action_datetime = datetime.now()
            self.edited_datetime = datetime.now()

        self.modified = datetime.now()
        if self.text:
            self.text_len = len(self.text)
        super(Post, self).save(*args, **kwargs)

    def save_without_image_actions(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
            self.action_datetime = datetime.now()

        self.modified = datetime.now()

        self.text_len = len(self.text)
        super(Post, self).save(*args, **kwargs)

    def get_preview_image(self):
        file_path = self.preview_image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(str(file_path))

            if filename_ext in settings.WRONG_IMAGE_EXT:
                return storage.url(filename_base) + filename_ext

            # return storage.url(filename_base + '_optimal') + filename_ext
            return storage.url(filename_base) + filename_ext
        elif self.original_preview_image:
            original_preview_image = self.original_preview_image
            return original_preview_image
        else:
            return ''

    def get_image(self, force_large=False):
        post_media = PostMedia.objects.filter(post=self.id).first()
        if post_media is None:
            return ''

        return post_media.get_image(force_large)

    def get_large_image(self):
        post_media = PostMedia.objects.filter(post=self.id).first()
        if post_media is None:
            return ''

        return post_media.get_image(True)

    def get_desktop_image(self):
        post_media = PostMedia.objects.filter(post=self.id).first()
        if post_media is None:
            return ''
        return post_media.get_resized_image(652, 366)

    def get_mobile_image(self):
        post_media = PostMedia.objects.filter(post=self.id).first()
        if post_media is None:
            return ''
        return post_media.get_resized_image(376, 211)

    def get_image_name(self):
        post_media = PostMedia.objects.filter(post=self.id).first()

        if post_media:
            image_name = str(post_media.image.name).replace("//", "/")
            return image_name
        else:
            return ''

    def get_share_link(self):
        community = self.community.all().first()
        unique_code = community.unique_code
        if self.layout_type == POST_LAYOUT_TYPE.BIG_NEWS or self.layout_type == POST_LAYOUT_TYPE.NEWS:
            people_to_meet = self.people_to_meet.first()
            post_type = 'article'
            if people_to_meet and people_to_meet.url_path:
                post_type = "article/{0}".format(people_to_meet.url_path)
            id_prefix = "news_id"
        else:
            post_type = "post"
            id_prefix = "p_id"

        if community.custom_domain:
            unique_url = community.invite_url + "/" + post_type + "/" + str(
                self.unique_url.encode('ascii', 'ignore')) + "/?" + id_prefix + "=" + str(self.id)
        else:
            unique_url = community.invite_url + "/" + unique_code + "/" + post_type + "/" + str(
                self.unique_url.encode('ascii', 'ignore')) + "/?" + id_prefix + "=" + str(self.id)

        return unique_url

    def get_webapp_share_link(self):
        community = self.community.all().first()
        unique_code = community.unique_code
        if self.layout_type == POST_LAYOUT_TYPE.BIG_NEWS or self.layout_type == POST_LAYOUT_TYPE.NEWS:
            people_to_meet = self.people_to_meet.first()
            post_type = 'article'
            if people_to_meet and people_to_meet.url_path:
                post_type = "article/{0}".format(people_to_meet.url_path)
        else:
            post_type = "post"

        if community.custom_domain:
            unique_url = community.invite_url + "/" + post_type + "/" + self.unique_url
        else:
            unique_url = community.invite_url + "/" + unique_code + "/" + post_type + "/" + self.unique_url
        return unique_url

    def get_images(self, force_large=False):
        images = []
        post_medias = PostMedia.objects.filter(post=self.id)
        for post_media in post_medias:
            if post_media:
                images.append(post_media.get_image(force_large))

        return images

    def get_preview_source_icon(self):
        file_path = self.preview_source_icon.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return 'https://d267x6x6dh1ejh.cloudfront.net/posts/8c9ab9b5-d7df-42ca-950c-7e94de9484a7.png'

    def get_video(self):
        post_media = PostMedia.objects.filter(post=self.id, type=POST_MEDIA_TYPES.VIDEO).first()
        if post_media is not None and post_media != '':
            return post_media.get_video()
        else:
            return ''

    def get_doc(self):
        post_media = PostMedia.objects.filter(post=self.id, type=POST_MEDIA_TYPES.DOCUMENT).first()
        if post_media:
            return post_media.get_doc()
        else:
            return ''

    def has_video(self):
        post_media = PostMedia.objects.filter(post=self.id, type=POST_MEDIA_TYPES.VIDEO).first()
        if post_media is not None and post_media != '':
            return True
        return False

    def is_complaint(self):
        if self.people_to_meet.all().first().unique_id == 'Complaints':
            return True
        return False

    def __unicode__(self):
        return self.text

    def is_offer_expired(self):
        now = datetime.now().date()
        start_date = self.offer_start_date
        end_date = self.offer_end_date
        status = False

        if start_date and end_date:
            if end_date < now:
                status = True
            else:
                status = False
        return status

    def get_amp_url(self):
        community = self.community.all().first()
        post_type = 'article'
        # unique_amp_url = community.invite_url + "/" + "amp" + "/" + post_type + "/" + str(
        #     self.unique_url.encode('ascii', 'ignore'))
        unique_amp_url = community.invite_url + "/" + "amp" + "/" + post_type + "/" + self.unique_url
        return unique_amp_url

    def get_absolute_url(self):
        community = self.community.all().first()
        unique_code = community.unique_code
        if self.layout_type == POST_LAYOUT_TYPE.BIG_NEWS or self.layout_type == POST_LAYOUT_TYPE.NEWS:
            people_to_meet = self.people_to_meet.first()
            post_type = 'article'
            if people_to_meet and people_to_meet.url_path:
                post_type = "article/{0}".format(people_to_meet.url_path)
        else:
            post_type = "post"

        if community.custom_domain:
            unique_url = "/" + post_type + "/" + self.unique_url
        else:
            unique_url = "/" + unique_code + "/" + post_type + "/" + self.unique_url
        return unique_url

    def get_meta_title(self):
        if self.seo_page_title:
            return str(self.seo_page_title.encode("utf8")).strip()
        elif self.title:
            return str(self.title.encode("utf8")).strip()
        else:
            return ""

    def get_meta_description(self):
        if self.seo_meta_description:
            return str(self.seo_meta_description.encode("utf8")).strip()
        elif self.text:
            return str(self.text.encode("utf8")).strip()
        else:
            return ""


class PostComment(models.Model):
    created_by = models.ForeignKey('MyUser', null=True, blank=True)
    post = models.ForeignKey('Post', null=False, blank=False)
    text = models.TextField()
    text_len = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    likes = models.BigIntegerField(default=0)
    spam = models.BigIntegerField(default=0)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    image = models.ImageField(upload_to=upload_posts_to, null=True, blank=True)
    preview_image = models.ImageField(upload_to=upload_posts_to, null=True, blank=True)
    preview_title = models.CharField(max_length=255, null=True, blank=True)
    preview_source = models.CharField(max_length=255, null=True, blank=True)
    preview_link = models.CharField(max_length=255, null=True, blank=True)
    community = models.ManyToManyField('Community', null=True, blank=True)
    is_hidden = models.BooleanField(default=0)
    is_video = models.BooleanField(default=0)
    entry_point = models.CharField(max_length=100, null=True, blank=True, default='')
    fb_comment_id = models.CharField(max_length=255, null=True, blank=True)
    external_integration = models.CharField(max_length=255, null=True, blank=True)
    external_integration_id = models.CharField(max_length=255, null=True, blank=True)
    user_mentions = models.TextField(null=True, blank=True)
    requires_moderation = models.BooleanField(default=False)
    moderation_reason = models.TextField(null=True, blank=True, default='')

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        self.modified = datetime.now()
        self.text_len = len(self.text)
        return super(PostComment, self).save(*args, **kwargs)

    def get_preview_image(self):
        file_path = self.preview_image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)

            if filename_ext == '.cms':
                return storage.url(filename_base) + filename_ext

            return storage.url(filename_base) + filename_ext
        else:
            return ''

    def get_image(self):
        file_path = self.image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)

            if filename_ext == '.cms':
                return storage.url(filename_base) + filename_ext

            return storage.url(filename_base) + filename_ext
        else:
            return ''

    def __unicode__(self):
        return self.text


class Meetup(models.Model):
    created_by = models.ForeignKey('MyUser', null=True, blank=True)
    topic = models.ForeignKey('Topic', null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField()
    type = models.CharField(max_length=50, default='', choices=GROUP_CHAT_TYPE().get_choices())
    entry_question = models.TextField(blank=True, null=True)
    is_entry_question_mandatory = models.BooleanField(default=False)
    pinned_topic = models.TextField(null=True, blank=True)
    unique_url = models.CharField(max_length=255)
    shares = models.BigIntegerField(default=0)
    going = models.BigIntegerField(default=0)
    comments = models.BigIntegerField(default=0)
    spam = models.BigIntegerField(default=0)
    score = models.BigIntegerField(default=1)
    activity = models.ForeignKey('Activity', null=True, blank=True)
    people_to_meet = models.ManyToManyField('PeopleToMeet', null=True, blank=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    action_datetime = models.DateTimeField(null=True, blank=True)
    privacy = models.CharField(max_length=50, choices=POST_PRIVACY().get_choices(), default='ALL')
    college = models.ForeignKey('College', null=True, blank=True)
    college_branch_ref = models.ForeignKey('CollegeBranch', null=True, blank=True,
                                           related_name='meetup_college_branch_ref', on_delete=models.SET_NULL)
    year_of_admission = models.IntegerField(blank=True, null=True)
    education_ref = models.ForeignKey('Education', null=True, blank=True, related_name='meetup_education_ref',
                                      on_delete=models.SET_NULL)
    workplace_ref = models.ForeignKey('WorkPlace', null=True, blank=True, related_name='meetup_workplace_ref',
                                      on_delete=models.SET_NULL)
    school_ref = models.ForeignKey('School', null=True, blank=True, related_name='meetup_school_ref',
                                   on_delete=models.SET_NULL)
    work_designation_ref = models.ForeignKey('WorkDesignation', null=True, blank=True,
                                             related_name='meetup_work_designation_ref', on_delete=models.SET_NULL)
    workplace_location = models.CharField(max_length=255, null=True, blank=True)
    apartment_tower = models.CharField(max_length=255, blank=True, null=True)
    community_branch = models.CharField(max_length=255, default='', blank=True)
    house_id = models.CharField(max_length=15, blank=True, null=True, db_index=True)
    image = models.ImageField(upload_to=upload_posts_to, null=True, blank=True)
    is_image_compressed = models.BooleanField(default=1)
    preview_image = models.ImageField(upload_to=upload_posts_to, null=True, blank=True)
    preview_title = models.CharField(max_length=255, null=True, blank=True)
    preview_source = models.CharField(max_length=255, null=True, blank=True)
    preview_link = models.CharField(max_length=255, null=True, blank=True)
    is_usercreated = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=0)
    is_expired = models.BooleanField(default=False)
    chat_access = models.CharField(max_length=50, default=GROUP_CHAT_ACCESS.ALL,
                                   choices=GROUP_CHAT_ACCESS().get_choices())
    chat_access_message = models.CharField(max_length=255, null=True, blank=True)
    places = models.ManyToManyField('Place', null=True, blank=True)
    is_mandatory_post = models.BooleanField(default=False)
    external_source = models.CharField(max_length=255, null=True, blank=True)
    external_source_id = models.CharField(max_length=255, null=True, blank=True)
    mcp_notif_sent = models.BooleanField(default=False)
    is_video = models.BooleanField(default=False)
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    height = models.FloatField(default=0.0)
    width = models.FloatField(default=0.0)
    resized_height = models.FloatField(default=0.0)
    resized_width = models.FloatField(default=0.0)
    preview_height = models.FloatField(default=0.0)
    preview_width = models.FloatField(default=0.0)
    resized_preview_height = models.FloatField(default=0.0)
    resized_preview_width = models.FloatField(default=0.0)
    is_big_preview_image = models.BooleanField(default=False)
    views = models.BigIntegerField(default=0)
    status = models.CharField(max_length=20, choices=MEETUP_STATUS, default='FUTURE')
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    locations = models.CharField(max_length=255, null=True, blank=True)
    background_color = models.CharField(max_length=100, null=True, blank=True)
    ready_to_push = models.BooleanField(default=False)
    is_notif_sent = models.BooleanField(default=False)
    community = models.ManyToManyField('Community', null=True, blank=True)
    user_mentions = models.TextField(null=True, blank=True)
    entry_point = models.CharField(max_length=100, null=True, blank=True, default='')
    address = models.CharField(max_length=255, null=True, blank=True)
    max_participants = models.IntegerField(default=5)
    is_system_created = models.BooleanField(default=False)
    is_community_meetup = models.BooleanField(default=False)
    is_area_meetup = models.BooleanField(default=False)
    is_city_meetup = models.BooleanField(default=False)
    is_state_meetup = models.BooleanField(default=False)
    gender_privacy = models.CharField(max_length=50, default='w_m', choices=GENDER_PRIVACY)
    is_admin_created = models.BooleanField(default=False)
    auto_join = models.BooleanField(default=False)
    eligibility_json = models.TextField(null=True, blank=True)
    pushed_to_web = models.BooleanField(default=False)

    # This field is used to uniquely identify the group based on a raw string id.
    # This was added for Lokal SDK's case where in the input to create a live group is
    # based on just a string id like bangalore_cricket_fans
    live_group_unique_parameter = models.CharField(max_length=255, null=True, blank=True)

    pinned_message_id = models.TextField(null=True, blank=True, default='')

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
            self.action_datetime = datetime.now()
            self.unique_url = self.get_meetup_unique_url()

        self.modified = datetime.now()
        super(Meetup, self).save(*args, **kwargs)

    def save_without_image_actions(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
            self.action_datetime = datetime.now()

        self.modified = datetime.now()

        super(Meetup, self).save(*args, **kwargs)

    def get_meetup_unique_url(self):

        if self.type == GROUP_CHAT_TYPE.USER_CREATED:
            text = self.title
        elif self.is_admin_created:
            text = self.title
        elif self.live_group_unique_parameter:
            text = self.live_group_unique_parameter
        elif not self.is_online and self.activity:
            text = self.activity.name
        elif self.title.strip():
            text = self.title
        elif self.text.strip():
            text = self.text
        else:
            text = uuid.uuid4()

        title = smart_str(text)
        title = re.sub(r'[^\x00-\x7F]+', '', title)
        title.replace("\r", " ").replace("\n", " ").replace("\t", '').replace("\"", "")
        safe_str = title[:70].encode('ascii', 'ignore')
        urnique_url_title = safe_str

        while 1:
            urnique_url_title = urnique_url_title + '_' + str(random.randint(1000, 9999))
            url = re.sub('[^0-9a-zA-Z]+', '-', str(urnique_url_title))
            post_exists = Meetup.objects.filter(unique_url=url)
            if not post_exists:
                return url

    def create_optimal_image(self):
        basewidth = settings.IMAGE_BASE_WIDTH
        file_path = self.image.name

        if not file_path:
            return

        filename_base, filename_ext = os.path.splitext(file_path)
        thumb_file_path = "%s_optimal%s" % (filename_base, filename_ext)

        try:
            f = storage.open(file_path, 'r')
            image = Image.open(f)
            width = image.size[0]
            height = image.size[1]
            wpercent = (basewidth / float(image.size[0]))
            hsize = int((float(height) * float(wpercent)))
            image = image.resize((basewidth, hsize), Image.ANTIALIAS)

            f_thumb = storage.open(thumb_file_path, "w")
            image.save(f_thumb)
            f_thumb.close()

            self.width = width
            self.height = height
            self.resized_width = basewidth
            self.resized_height = hsize

            self.save_without_image_actions()
        except:
            pass

    def get_share_link(self):
        community = self.community.all().first().unique_code
        if self.is_online:
            unique_url = "https://getmilo.app/" + str(community) + "/groups/" + str(self.unique_url) + "/?p_id=" + str(
                self.id)
        else:
            unique_url = "https://getmilo.app/" + str(community) + "/meetup/" + str(self.unique_url) + "/?p_id=" + str(
                self.id)
        return unique_url

    def get_preview_image(self):
        file_path = self.preview_image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(str(file_path))

            if filename_ext in settings.WRONG_IMAGE_EXT:
                return storage.url(filename_base) + filename_ext

            return storage.url(filename_base + '_optimal') + filename_ext
        else:
            return ''

    def get_image(self, force_large=False):
        if not self.image:
            return ''

        file_path = self.image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(str(file_path))

            if force_large:
                return storage.url(filename_base) + filename_ext

            return storage.url(filename_base) + filename_ext
            # if self.is_image_compressed:
            #     return storage.url(filename_base) + filename_ext
            # else:
            #     return storage.url(filename_base + '_optimal') + filename_ext
        else:
            return ''

    def __unicode__(self):
        return self.text


class MeetupGoing(models.Model):
    user = models.ForeignKey('MyUser', null=True, blank=True)
    meetup = models.ForeignKey('Meetup', null=True, blank=True)
    status = models.CharField(max_length=100, choices=MEETUP_GOING_STATUS, default='APPROVED')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    has_messaged = models.BooleanField(default=False)
    is_muted = models.BooleanField(default=False)
    is_group_admin = models.BooleanField(default=False)

    class Meta:
        unique_together = ('meetup', 'user')

    def __unicode__(self):
        return self.user.first_name


class MeetupComment(models.Model):
    created_by = models.ForeignKey('MyUser', null=True, blank=True)
    meetup = models.ForeignKey('Meetup', null=False, blank=False)
    text = models.TextField()
    status = models.BooleanField(default=False)
    likes = models.BigIntegerField(default=0)
    spam = models.BigIntegerField(default=0)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    type = models.CharField(choices=COMMENT_TYPES, max_length=100, null=True, default='TEXT')
    preview_image = models.ImageField(upload_to=upload_posts_to, null=True, blank=True)
    preview_title = models.CharField(max_length=255, null=True, blank=True)
    preview_source = models.CharField(max_length=255, null=True, blank=True)
    preview_link = models.CharField(max_length=255, null=True, blank=True)
    image_ref = models.ForeignKey('MeetupMedia', null=True, blank=True, on_delete=models.SET_NULL)
    community = models.ManyToManyField('Community', null=True, blank=True)
    is_hidden = models.BooleanField(default=0)
    is_system_generated = models.BooleanField(default=0)
    is_video = models.BooleanField(default=0)
    user_mentions = models.TextField(null=True, blank=True)
    system_message_type = models.CharField(max_length=100, choices=MEETUP_COMMENT_SYSTEM_MESSAGE_TYPE, default='')

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        self.modified = datetime.now()
        return super(MeetupComment, self).save(*args, **kwargs)

    def get_preview_image(self):
        file_path = self.preview_image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)

            if filename_ext == '.cms':
                return storage.url(filename_base) + filename_ext

            return storage.url(filename_base) + filename_ext
        else:
            return ''

    def __unicode__(self):
        return self.text


class UserActivity(models.Model):
    user = models.ForeignKey('MyUser')
    activity_type = models.CharField(max_length=20, choices=ActivityType().get_choices())
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    god_content_type = models.ForeignKey(ContentType, related_name='god_content_type', null=True)
    god_object_id = models.PositiveIntegerField(null=True)
    god_content_object = GenericForeignKey('god_content_type', 'god_object_id')
    object_type = models.CharField(max_length=20, choices=ObjectType().get_choices(), null=True, blank=True)
    privacy_type = models.CharField(choices=PRIVACY_TYPE_CHOICES, default='ALL', max_length=30)
    is_autocreated = models.BooleanField(default=False)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        self.modified = datetime.now()

        # Update god ids based on the activity type. Doing only for posts now.
        if self.activity_type == ActivityType.CREATE_POST:
            self.god_content_object = self.content_object

        if self.activity_type == ActivityType.LIKE_POST:
            self.god_content_object = self.content_object

        if self.activity_type == ActivityType.COMMENT_POST:
            self.god_content_object = self.content_object.post

        if self.activity_type == ActivityType.LIKE_POST_COMMENT:
            self.god_content_object = self.content_object.post

        if self.activity_type == ActivityType.CREATE_MEETUP:
            self.god_content_object = self.content_object

        return super(UserActivity, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.activity_type


class Site(models.Model):
    name = models.CharField(max_length=255, unique=True)
    google_analytics_code = models.TextField(null=True, blank=True)
    analytics_blacklist_user_ids = models.TextField(null=True, blank=True)
    show_from_categories = models.BooleanField(default=False)
    include_tags = models.BooleanField(default=False)
    exclude_tags = models.BooleanField(default=False)
    title = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)
    robots = models.CharField(max_length=100, null=True, blank=True)
    language = models.CharField(max_length=10, null=True, blank=True, default='en')
    fb_page = models.CharField(max_length=255, null=True, blank=True)
    info_display_name = models.CharField(max_length=100, null=True, blank=True)
    search_engine_verify_code = models.CharField(max_length=255, null=True, blank=True)
    fb_app_id = models.CharField(max_length=255, null=True, blank=True)
    fb_app_secret = models.CharField(max_length=255, null=True, blank=True)
    fb_app_admin = models.CharField(max_length=255, null=True, blank=True)
    fb_title = models.CharField(max_length=255, null=True, blank=True)
    fb_description = models.CharField(max_length=255, null=True, blank=True)
    site_name = models.CharField(max_length=255, null=True, blank=True)
    parent_domain = models.CharField(max_length=255, null=True, blank=True)
    is_prediction = models.BooleanField(default=False)
    image = models.CharField(max_length=255, null=True, blank=True)
    show_categories = models.BooleanField(default=True)
    link = models.TextField(null=True, blank=True)
    show_winner = models.BooleanField(default=False)
    is_subdomain = models.BooleanField(default=False)
    crawl_social = models.BooleanField(default=False)

    class Meta:
        app_label = 'webapp'

    def __unicode__(self):
        return self.name


class ScoreWeight(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    vote = models.IntegerField(default=1)
    like = models.IntegerField(default=1)
    comment = models.IntegerField(default=1)
    min_opinions_criteria = models.IntegerField(default=1)
    min_questions_onboaridng = models.IntegerField(default=10)
    min_questions_for_opinion_match = models.IntegerField(default=100)
    user_matching_questions_threshold = models.IntegerField(default=9)
    share = models.IntegerField(default=1)
    track = models.IntegerField(default=1)
    freshness = models.IntegerField(default=1)
    freshness_delta = models.IntegerField(default=1)
    expiry = models.IntegerField(default=1)
    expiry_delta = models.IntegerField(default=1)
    landslide_multiplier = models.IntegerField(default=1)
    controversial_multiplier = models.IntegerField(default=1)
    trending_multiplier = models.IntegerField(default=1)
    controversial_criteria_lhs = models.IntegerField(default=40)
    controversial_criteria_rhs = models.IntegerField(default=55)
    trending_criteria_days = models.IntegerField(default=5)
    trending_criteria_polls = models.IntegerField(default=20)
    landslide_criteria = models.IntegerField(default=75)
    related_topic_criteria_percent = models.IntegerField(default=20)
    post_like_score = models.IntegerField(default=10)
    post_comment_score = models.IntegerField(default=20)
    post_like_comment_score = models.IntegerField(default=1)

    class Meta:
        app_label = 'webapp'

    def __unicode__(self):
        return self.name


class InviteRequest(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True, choices=INVITE_REQUEST_STATUS, default='RECEIVED')
    invite_code_sent = models.CharField(max_length=255, null=True, blank=True)
    num_mails_sent = models.IntegerField(default=0)
    m_clicks = models.IntegerField(default=0)
    d_clicks = models.IntegerField(default=0)
    created = models.DateTimeField(null=True, blank=True)
    modified = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
            self.modified = datetime.now()
        self.modified = datetime.now()
        return super(InviteRequest, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.email


class UserBoard(models.Model):
    user = models.ForeignKey('MyUser', null=True, blank=True)
    matches_total = models.BigIntegerField(default=0)
    matches_polled = models.BigIntegerField(default=0)
    matches_won = models.BigIntegerField(default=0)
    matches_lost = models.BigIntegerField(default=0)
    points_scored = models.BigIntegerField(default=0)

    class Meta:
        ordering = ["-points_scored"]
        app_label = 'webapp'

    def __unicode__(self):
        return self.user.email


class PollMetaData(models.Model):
    poll = models.ForeignKey('Poll')
    shares = models.BigIntegerField(default=0)
    likes = models.BigIntegerField(default=0)
    comments = models.BigIntegerField(default=0)
    votes = models.BigIntegerField(default=0)
    created = models.DateTimeField()

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        super(PollMetaData, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.poll.question


class Configuration(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, default='default')
    daily_gc_title = models.CharField(max_length=255, null=True, blank=True)
    daily_gc_text = models.TextField(blank=True, null=True)
    daily_gc_entry_question = models.TextField(blank=True, null=True)
    daily_gc_image = models.ImageField(upload_to=upload_posts_to, null=True, blank=True)
    percentage_match_bucket_1 = models.FloatField(default=0.7)
    percentage_match_bucket_2 = models.FloatField(default=0.3)
    min_percentage_match_to_chat = models.FloatField(default=0.9)
    chat_character_limit = models.IntegerField(default=100)
    min_num_friends = models.IntegerField(default=50)
    invite_limit = models.IntegerField(default=50)
    recommendation_break = models.IntegerField(default=12)
    invite_break = models.IntegerField(default=20)
    min_polls_to_create_post = models.IntegerField(default=8)
    min_onboarding_polls = models.IntegerField(default=10)
    num_poll_recommendations = models.IntegerField(default=1)
    character_limit_status = models.IntegerField(default=200)
    character_limit_post = models.IntegerField(default=200)
    min_character_limit_post = models.IntegerField(default=10)
    character_limit_post_comment = models.IntegerField(default=200)
    feed_limit_per_user = models.IntegerField(default=100)
    push_notif_post_text_limit = models.IntegerField(default=50)
    notif_limit_per_user = models.IntegerField(default=100)
    num_posts_insert_on_follow = models.IntegerField(default=50)
    min_android_app_version = models.IntegerField(default=7)
    latest_android_app_version = models.IntegerField(default=7)
    min_ios_app_version = models.IntegerField(default=7)
    latest_ios_app_version = models.IntegerField(default=7)
    enable_ios_onboard_skip = models.BooleanField(default=False)
    network_limit_per_topic = models.IntegerField(default=100)
    min_opinions_active_users_master = models.IntegerField(default=25)
    min_opinions_active_users_topic = models.IntegerField(default=6)
    min_compute_percentage_match = models.FloatField(default=0.5)
    num_days_for_expired_event = models.IntegerField(default=7)
    personality_match_weight = models.FloatField(default=0.25)
    checkout_threshold_time = models.FloatField(default=6)
    checkin_radius = models.FloatField(default=50)
    min_checkin_note_len = models.IntegerField(default=10)
    max_checkin_note_len = models.IntegerField(default=80)
    # num_polls_to_create_post = models.IntegerField(default=5)
    upper_age_threshold = models.IntegerField(default=5)
    lower_age_threshold = models.IntegerField(default=5)
    banned_words = models.TextField(null=True, blank=True)
    collect_college_work_home_info = models.BooleanField(default=False)
    show_mcp = models.BooleanField(default=False)
    show_mcp_skip = models.BooleanField(default=False)
    new_user_indian_posts = models.CharField(max_length=255, blank=True, null=True)
    new_user_usa_posts = models.CharField(max_length=255, blank=True, null=True)
    female_restricted_prefs = models.CharField(max_length=255, blank=True, null=True)
    male_restricted_prefs = models.CharField(max_length=255, blank=True, null=True)
    signup_notif_timer = models.IntegerField(default=5)
    people_discovery_distance = models.IntegerField(default=50)
    people_discovery_distance_usa = models.IntegerField(default=500)
    people_discovery_age = models.IntegerField(default=7)
    max_chat_requests = models.IntegerField(default=10)
    max_chat_receive_requests = models.IntegerField(default=25)
    max_ask_reco_char_limit = models.IntegerField(default=200)
    show_online_status = models.BooleanField(default=True)
    suppress_words = models.TextField(null=True, blank=True)
    new_user_landing_screen = models.CharField(max_length=255, default='0')
    dont_show_footer_seconds = models.IntegerField(default=0)
    my_feed_enabled = models.BooleanField(default=True)
    my_feed_enabled_cities = models.TextField(null=True, blank=True)
    default_my_switch = models.CharField(null=True, blank=True, default="PUBLIC", max_length=255)
    meetup_up_break = models.IntegerField(default=2)
    shake_sensitivity = models.FloatField(default=3.5)
    shake_count = models.IntegerField(default=6)
    shake_sensitivity_in_app = models.FloatField(default=2.5)
    shake_count_in_app = models.IntegerField(default=4)
    bing_subscription_key = models.CharField(max_length=255, default="")
    google_subscription_key = models.CharField(max_length=255, default="")
    tmdb_subscription_key = models.CharField(max_length=255, default="")
    create_shortcut = models.BooleanField(default=False)
    suppressed_keywords = models.TextField(null=True, blank=True)
    phone_auth = models.CharField(max_length=50, choices=PhoneAuth().get_choices(), default="FIREBASE_SMS")

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        super(Configuration, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class UserSession(models.Model):
    user = models.ForeignKey(User)
    session = models.ForeignKey(Session)

    class Meta:
        app_label = 'webapp'

    def __unicode__(self):
        return self.user.username


def user_logged_in_handler(sender, request, user, **kwargs):
    try:
        UserSession.objects.get_or_create(
            user=user,
            session_id=request.session.session_key
        )
    except IntegrityError:
        pass


user_logged_in.connect(user_logged_in_handler)


class Device(models.Model):
    dev_id = models.CharField(max_length=50, blank=True, null=True)
    reg_id = models.TextField()
    device_type = models.CharField(max_length=50, default='android')
    name = models.CharField(max_length=255, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey('MyUser', null=True, blank=True)
    registered = models.BooleanField(default=True)

    class Meta:
        app_label = 'webapp'

    def __str__(self):
        return self.user.username


class Feedback(models.Model):
    feedback = models.TextField()
    issue_type = models.CharField(max_length=255, choices=FEEDBACK_TYPES, default='FEEDBACK')
    user = models.ForeignKey('MyUser', blank=True, null=True, on_delete=models.SET_NULL)
    device = models.TextField()
    email = models.CharField(max_length=255, blank=True, null=True)
    is_responded = models.BooleanField(default=False)
    created = models.DateTimeField(null=True, blank=True)
    modified = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
            self.modified = datetime.now()
        self.modified = datetime.now()
        return super(Feedback, self).save(*args, **kwargs)

    def __str__(self):
        return self.feedback


class College(models.Model):
    govt_id = models.CharField(max_length=255, blank=True, null=True)
    other_id = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    alias = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state_short_code = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=100, choices=COLLEGE_STATUS_CHOICES, default='LOCKED')
    created = models.DateTimeField(null=True, blank=True)
    modified = models.DateTimeField(null=True, blank=True)
    number_of_users = models.IntegerField(default=0)
    number_of_students = models.IntegerField(default=0)
    number_of_alumni = models.IntegerField(default=0)
    min_students_users = models.IntegerField(default=25)

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        self.modified = datetime.now()
        return super(College, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class EventPartner(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    site = models.TextField(max_length=255, blank=True, null=True)
    button_image = models.ImageField(upload_to=upload_events_to, null=True, blank=True)
    created = models.DateTimeField(default=datetime.now, blank=True)
    modified = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        self.modified = datetime.now()
        return super(EventPartner, self).save(*args, **kwargs)

    def get_button_image(self):
        file_path = self.button_image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return ""

    def __unicode__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey('MyUser', null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    topic = models.ForeignKey('Topic', null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    attending = models.IntegerField(default=0)
    college = models.ForeignKey('College', null=True, blank=True)
    comments = models.BigIntegerField(default=0)
    spam = models.BigIntegerField(default=0)
    privacy = models.CharField(max_length=50, choices=EVENT_PRIVACY, default='ALL')
    type = models.CharField(max_length=50, choices=EVENT_TYPE, default='NATIVE_EVENT')
    image = models.ImageField(upload_to=upload_events_to, null=True, blank=True)
    theme_id = models.CharField(max_length=255, blank=True, null=True)
    is_online = models.BooleanField(default=False)
    timezone = models.CharField(max_length=255, blank=True, null=True)
    why_attend = models.TextField(blank=True, null=True)
    looking_for = models.TextField(blank=True, null=True)
    is_notif_sent = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    resized_height = models.FloatField(default=0.0)
    height = models.FloatField(default=0.0)
    unique_url = models.CharField(max_length=255, blank=True, null=True)
    place = models.ForeignKey('Place', null=True, blank=True)
    places = models.ManyToManyField('Place', null=True, blank=True, related_name='places')

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        self.modified = datetime.now()

        super(Event, self).save(*args, **kwargs)

        self.create_thumbs()

    def get_image(self):
        file_path = self.image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return ""

    def save_without_other_images(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)

    def create_thumbs(self):
        basewidth = settings.IMAGE_BASE_WIDTH
        file_path = self.image.name
        if not file_path:
            return
        filename_base, filename_ext = os.path.splitext(file_path)
        thumb_file_path = "%s_optimal%s" % (filename_base, filename_ext)
        try:
            f = storage.open(file_path, 'r')
            image = Image.open(f)
            width = image.size[0]
            height = image.size[1]
            wpercent = (basewidth / float(image.size[0]))
            hsize = int((float(height) * float(wpercent)))
            image = image.resize((basewidth, hsize), Image.ANTIALIAS)

            f_thumb = storage.open(thumb_file_path, "w")
            image.save(f_thumb)
            f_thumb.close()

            self.height = height
            self.resized_height = hsize

            self.save_without_other_images()
        except:
            pass

    def __unicode__(self):
        return self.title


class PostMedia(models.Model):
    post = models.ForeignKey('Post', null=True, blank=True)
    static_info = models.ForeignKey('StaticInfo', null=True, blank=True)
    image = models.ImageField(upload_to=upload_posts_to, null=True, blank=True)
    video = models.FileField(upload_to=upload_posts_to, null=True, blank=True)
    doc = models.FileField(upload_to=upload_posts_to, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True, choices=POST_MEDIA_TYPES().get_choices(), default='')
    original_url = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=255, default='')
    height = models.FloatField(default=0.0)
    width = models.FloatField(default=0.0)
    resized_height = models.FloatField(default=0.0)
    resized_width = models.FloatField(default=0.0)
    created = models.DateTimeField(default=datetime.now, blank=True)
    modified = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        self.modified = datetime.now()

        if not self.type:
            if self.video == None or self.video == '' or self.video.name == '':
                self.type = POST_MEDIA_TYPES.IMAGE
            else:
                self.type = POST_MEDIA_TYPES.VIDEO
        self.update_metadata()

        super(PostMedia, self).save(*args, **kwargs)

    def get_image(self, force_large=True):
        file_path = self.image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(str(file_path))
            if filename_ext == '.gif':
                force_large = True

            if force_large:
                return storage.url(filename_base) + filename_ext

            else:
                if self.resized_height:
                    return storage.url(filename_base + '_optimal') + filename_ext

                else:
                    return storage.url(filename_base) + filename_ext

        else:
            return ''

    def get_resized_image(self, width, height):
        file_path = self.image.name
        if file_path:
            # try:
            file_path = str(filepath_to_uri(file_path)).replace("//", "/")
            # except:
            #     file_path = file_path
            resized_file_path = 'fit-in/{0}x{1}/'.format(width, height) + file_path
            return settings.ARGUS_IMAGE_RESIZE_CDN + '/' + resized_file_path
        else:
            return ''

    def get_video(self):
        file_path = self.video.name
        if file_path:
            try:
                filename_base, filename_ext = os.path.splitext(str(file_path))
                return storage.url(filename_base) + filename_ext
            except UnicodeEncodeError:
                return ''
        else:
            return ''

    def get_doc(self):
        file_path = self.doc.name
        if file_path:
            try:
                filename_base, filename_ext = os.path.splitext(str(file_path))
                return storage.url(filename_base) + filename_ext
            except UnicodeEncodeError:
                return ''
        else:
            return ''

    def update_metadata(self):
        file_path = self.image.name
        if not file_path:
            return
        try:
            f = storage.open(file_path, 'r')
            image = Image.open(f)
            width = image.size[0]
            height = image.size[1]

            self.height = height
            self.width = width
            self.create_optimal_image()
        except:
            pass

    def create_optimal_image(self, *args, **kwargs):
        basewidth = settings.IMAGE_BASE_WIDTH
        file_path = self.image.name

        if not file_path:
            return

        filename_base, filename_ext = os.path.splitext(file_path)
        thumb_file_path = "%s_optimal%s" % (filename_base, filename_ext)

        if filename_ext == '.gif':
            return

        try:
            f = storage.open(file_path, 'r')
            image = Image.open(f)
            width = image.size[0]
            height = image.size[1]
            wpercent = (basewidth / float(image.size[0]))
            hsize = int((float(height) * float(wpercent)))
            image = image.resize((basewidth, hsize), Image.ANTIALIAS)

            f_thumb = storage.open(thumb_file_path, "w")
            image.save(f_thumb)
            f_thumb.close()

            self.width = width
            self.height = height
            self.resized_width = basewidth
            self.resized_height = hsize

            super(PostMedia, self).save(*args, **kwargs)
        except:
            pass

    def __unicode__(self):
        if self.type == 'IMAGE':
            file_path = self.get_image()
        else:
            file_path = str(self.id)
        return file_path


class EventMedia(models.Model):
    event = models.ForeignKey('Event', null=True, blank=True)
    image = models.ImageField(upload_to=upload_events_to, null=True, blank=True)
    resized_height = models.FloatField(default=0.0)
    height = models.FloatField(default=0.0)
    click = models.BooleanField(default=False)
    spam = models.BigIntegerField(default=0)
    media_type = models.CharField(max_length=10, default='IMAGE')
    uploaded_by = models.ForeignKey('MyUser', null=True, blank=True)
    upload_date = models.DateTimeField()

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.upload_date = datetime.now()

        super(EventMedia, self).save(*args, **kwargs)

        if self.media_type == 'IMAGE':
            self.create_thumbs()

    def get_image(self):
        file_path = self.image.name
        if file_path:
            return storage.url(file_path)
        else:
            return ""

    def save_without_other_images(self, *args, **kwargs):
        super(EventMedia, self).save(*args, **kwargs)

    def create_thumbs(self):
        basewidth = settings.IMAGE_BASE_WIDTH
        file_path = self.image.name
        if not file_path:
            return
        filename_base, filename_ext = os.path.splitext(file_path)
        thumb_file_path = "%s_optimal%s" % (filename_base, filename_ext)
        try:
            f = storage.open(file_path, 'r')
            image = Image.open(f)
            height = image.size[1]
            wpercent = (basewidth / float(image.size[0]))
            hsize = int((float(image.size[1]) * float(wpercent)))
            image = image.resize((basewidth, hsize), Image.ANTIALIAS)

            f_thumb = storage.open(thumb_file_path, "w")
            image.save(f_thumb)
            f_thumb.close()

            self.height = height
            self.resized_height = hsize
            self.save_without_other_images()
        except:
            pass

    def __unicode__(self):
        if self.media_type == 'IMAGE':
            file_path = self.image.name
            return storage.url(file_path)
        else:
            return "NONE"


class MeetupMedia(models.Model):
    meetup = models.ForeignKey('Meetup', null=True, blank=True)
    image = models.ImageField(upload_to=upload_events_to, null=True, blank=True)
    resized_height = models.FloatField(default=0.0)
    height = models.FloatField(default=0.0)
    click = models.BooleanField(default=False)
    spam = models.BigIntegerField(default=0)
    media_type = models.CharField(max_length=10, default='IMAGE')
    uploaded_by = models.ForeignKey('MyUser', null=True, blank=True)
    upload_date = models.DateTimeField()

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.upload_date = datetime.now()

        super(MeetupMedia, self).save(*args, **kwargs)

        if self.media_type == 'IMAGE':
            self.create_thumbs()

    def get_image(self):
        file_path = self.image.name
        if file_path:
            return storage.url(file_path)
        else:
            return ""

    def save_without_other_images(self, *args, **kwargs):
        super(MeetupMedia, self).save(*args, **kwargs)

    def create_thumbs(self):
        basewidth = settings.IMAGE_BASE_WIDTH
        file_path = self.image.name
        if not file_path:
            return
        filename_base, filename_ext = os.path.splitext(file_path)
        thumb_file_path = "%s_optimal%s" % (filename_base, filename_ext)
        try:
            f = storage.open(file_path, 'r')
            image = Image.open(f)
            height = image.size[1]
            wpercent = (basewidth / float(image.size[0]))
            hsize = int((float(image.size[1]) * float(wpercent)))
            image = image.resize((basewidth, hsize), Image.ANTIALIAS)

            f_thumb = storage.open(thumb_file_path, "w")
            image.save(f_thumb)
            f_thumb.close()

            self.height = height
            self.resized_height = hsize
            self.save_without_other_images()
        except:
            pass

    def __unicode__(self):
        if self.media_type == 'IMAGE':
            file_path = self.image.name
            return storage.url(file_path)
        else:
            return "NONE"


class EventComment(models.Model):
    created_by = models.ForeignKey('MyUser', null=True, blank=True)
    event = models.ForeignKey('Event', null=False, blank=False)
    text = models.TextField()
    likes = models.BigIntegerField(default=0)
    spam = models.BigIntegerField(default=0)
    preview_image = models.ImageField(upload_to=upload_posts_to, null=True, blank=True)
    preview_title = models.CharField(max_length=255, null=True, blank=True)
    preview_source = models.CharField(max_length=255, null=True, blank=True)
    preview_link = models.CharField(max_length=255, null=True, blank=True)
    is_hidden = models.BooleanField(default=0)
    is_video = models.BooleanField(default=0)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        self.modified = datetime.now()
        return super(EventComment, self).save(*args, **kwargs)

    def get_preview_image(self):
        file_path = self.preview_image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return ""

    def __unicode__(self):
        return self.text


class Theme(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    topic = models.ForeignKey('Topic', null=True, blank=True)
    people_to_meet = models.ForeignKey('PeopleToMeet', null=True, blank=True)
    image = models.ImageField(upload_to=upload_events_to, null=True, blank=True)
    created = models.DateTimeField(default=datetime.now, blank=True)
    modified = models.DateTimeField(default=datetime.now, blank=True)

    def get_image(self):
        file_path = self.image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return ""

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        self.modified = datetime.now()
        return super(Theme, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to=upload_places_to, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True, choices=PLACE_TYPES, default='AREA')
    google_id = models.CharField(max_length=150, null=True, blank=True, unique=True)
    google_tags = models.TextField()
    internal_tags = models.TextField()
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(default=datetime.now, blank=True)
    modified = models.DateTimeField(default=datetime.now, blank=True)
    city = models.ForeignKey('Place', related_name='place_city', blank=True, null=True, on_delete=models.SET_NULL)
    country = models.ForeignKey('Place', related_name='place_country', blank=True, null=True, on_delete=models.SET_NULL)
    num_user_count = models.IntegerField(
        default=0)  # this was added alternative to number_of_users since number_of_users was derived from college table

    # From college table
    govt_id = models.CharField(max_length=255, blank=True, null=True)
    other_id = models.CharField(max_length=255, blank=True, null=True)
    alias = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=COLLEGE_STATUS_CHOICES, default='LOCKED')
    number_of_users = models.IntegerField(default=0)
    number_of_students = models.IntegerField(default=0)
    number_of_alumni = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()

        self.modified = datetime.now()

        return super(Place, self).save(*args, **kwargs)

    def get_image(self):
        file_path = self.image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return ""

    def __unicode__(self):
        return self.name


class PlaceConversation(models.Model):
    text = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True, choices=PLACE_CONVERSATION_TYPES, default='CHAT')
    image = models.ImageField(upload_to=upload_places_to, null=True, blank=True)
    created_by = models.ForeignKey('MyUser')
    place = models.ForeignKey('Place')
    # upvotes = models.IntegerField(default=0)
    # downvotes = models.IntegerField(default=0)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()

        self.modified = datetime.now()

        return super(PlaceConversation, self).save(*args, **kwargs)

    def get_image(self):
        file_path = self.image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return "https://d267x6x6dh1ejh.cloudfront.net/events/6d3fb62c-8e48-4b77-96ac-ca58fe49f414.jpg"

    def __unicode__(self):
        return self.text


class PlaceOwner(models.Model):
    place = models.ForeignKey('Place')
    user = models.ForeignKey('MyUser')
    created = models.DateTimeField()
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()

        self.modified = datetime.now()

        # Mark the user as a place owner if there is a field here with his reference.
        self.user.is_place_owner = True
        self.user.save()

        return super(PlaceOwner, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.place.name


class Like(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    fb_id = models.CharField(max_length=150, null=True, blank=True, unique=True)
    fb_category = models.CharField(max_length=255, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    topics = models.ManyToManyField('Topic', null=True, blank=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        app_label = 'webapp'

    def get_image(self):
        file_path = self.image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return "https://d267x6x6dh1ejh.cloudfront.net/polls/20141025221704.png"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        self.modified = datetime.now()
        return super(Like, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class PeopleToMeet(models.Model):
    name = models.CharField(max_length=255)
    unique_id = models.CharField(max_length=255, null=True, blank=True)
    url_path = models.CharField(max_length=255, null=True, blank=True)
    score = models.IntegerField(default=1)
    community = models.ForeignKey('Community', null=True, blank=True)
    group_chat_title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    # 'icon' field is used in admin section cards when community admin_section_layout field is set to TILES
    icon = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    topics = models.ManyToManyField('Topic', null=True, blank=True)
    hide_in_create_post = models.BooleanField(default=False)
    hide_posts = models.BooleanField(default=False)
    num_chosen_in_pd = models.BigIntegerField(default=0)
    num_following = models.BigIntegerField(default=0)
    show_opp_gender = models.BooleanField(default=False)
    type = models.CharField(max_length=20, choices=TOPIC_TYPE_CHOICES().get_choices(),
                            default=TOPIC_TYPE_CHOICES.CATEGORY)
    is_admin_only = models.BooleanField(default=False)
    is_default_create_post = models.BooleanField(default=False)
    is_default_selected = models.BooleanField(default=False)
    is_fixed = models.BooleanField(default=False)
    is_non_interest = models.BooleanField(default=False)
    disable_group_chat = models.BooleanField(default=True)
    link_url = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    height = models.FloatField(default=0.0)
    width = models.FloatField(default=0.0)
    resized_height = models.FloatField(default=0.0)
    resized_width = models.FloatField(default=0.0)
    seo_page_title = models.CharField(max_length=255, default='', blank=True)
    seo_description = models.TextField(default='', blank=True)

    class Meta:
        app_label = 'webapp'

    def get_image(self):
        file_path = self.image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return "https://d301sr5gafysq2.cloudfront.net/dc4237fa9a20/img/unmapped_author_32.png"

    def get_icon(self):
        file_path = self.icon.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return "https://d301sr5gafysq2.cloudfront.net/dc4237fa9a20/img/unmapped_author_32.png"

    def create_optimal_image(self):
        basewidth = 48
        file_path = self.image.name

        if not file_path:
            return

        filename_base, filename_ext = os.path.splitext(file_path)
        thumb_file_path = "%s_optimal%s" % (filename_base, filename_ext)

        try:
            f = storage.open(file_path, 'r')
            image = Image.open(f)
            format = image.format
            width = image.size[0]
            height = image.size[1]
            wpercent = (basewidth / float(image.size[0]))
            hsize = int((float(height) * float(wpercent)))
            image = image.resize((basewidth, hsize), Image.ANTIALIAS)

            f_thumb = storage.open(thumb_file_path, "w")
            # image.save(f_thumb)
            resized_thumbnail_image_file = StringIO()
            image.save(resized_thumbnail_image_file, format)
            f_thumb.write(resized_thumbnail_image_file.getvalue())
            f_thumb.close()

            self.width = width
            self.height = height
            self.resized_width = basewidth
            self.resized_height = hsize

            self.save()
        except:
            pass

    def get_optimal_image(self):
        file_path = self.image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(str(file_path))
            if self.resized_height:
                return storage.url(filename_base + '_optimal') + filename_ext
            else:
                return storage.url(filename_base) + filename_ext
        else:
            return "https://d301sr5gafysq2.cloudfront.net/dc4237fa9a20/img/unmapped_author_32.png"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
            self.unique_id = self.name
        self.modified = datetime.now()
        return super(PeopleToMeet, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class LangPeopleToMeet(models.Model):
    language = models.ForeignKey('Language', null=True, blank=True, default='', on_delete=models.SET_NULL)
    people_to_meet = models.ForeignKey('PeopleToMeet')
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.people_to_meet.name


class SubInterest(models.Model):
    name = models.CharField(max_length=255)
    unique_id = models.CharField(max_length=255, null=True, blank=True)
    score = models.IntegerField(default=1)
    people_to_meet = models.ForeignKey('PeopleToMeet')
    community = models.ForeignKey('Community', null=True, blank=True)
    image = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'webapp'

    def get_image(self):
        file_path = self.image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return "https://d301sr5gafysq2.cloudfront.net/dc4237fa9a20/img/unmapped_author_32.png"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        self.modified = datetime.now()
        return super(SubInterest, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class MyUserPeopleToMeet(models.Model):
    myuser = models.ForeignKey('MyUser')
    peopletomeet = models.ForeignKey('PeopleToMeet')
    rank = models.IntegerField(default=0)

    class Meta:
        db_table = 'webapp_myuser_people_to_meet'


class Activity(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    rectangle_image = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    image_color = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    rank = models.IntegerField(default=0)  # Rank 0 means, they are activities
    topics = models.ManyToManyField('Topic', null=True, blank=True)
    people_to_meet = models.ForeignKey('PeopleToMeet', null=True, blank=True)
    is_college = models.BooleanField(default=True)
    is_apartment = models.BooleanField(default=True)
    is_virtual = models.BooleanField(default=True)
    messaging_type = models.CharField(max_length=255, choices=ACTIVITY_MESSAGING_TYPES, default='MEETUP')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    text = models.TextField(null=True, blank=True, default='')
    comment_suggestions = models.TextField(null=True, blank=True, default='')
    enable_pricing = models.BooleanField(default=False)

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        self.modified = datetime.now()

        return super(Activity, self).save(*args, **kwargs)

    def get_image(self):
        file_path = self.image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return "https://d301sr5gafysq2.cloudfront.net/dc4237fa9a20/img/unmapped_author_32.png"

    def get_image_color(self):
        file_path = self.image_color.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return "https://d301sr5gafysq2.cloudfront.net/dc4237fa9a20/img/unmapped_author_32.png"

    def get_rectangle_image(self):
        file_path = self.rectangle_image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return "https://d301sr5gafysq2.cloudfront.net/dc4237fa9a20/img/unmapped_author_32.png"

    def __unicode__(self):
        return self.name


class Analytics(models.Model):
    type = models.CharField(max_length=50, choices=ANALYTICS_TYPE, default='DEFAULT')
    user = models.ForeignKey('MyUser', null=True, blank=True)
    device_id = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        self.modified = datetime.now()

        return super(Analytics, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.type


class QueryAnalytics(models.Model):
    type = models.CharField(max_length=50, choices=QUERY_ANALYTICS_TYPE, default='DEFAULT')
    user = models.ForeignKey('MyUser', null=True, blank=True)
    user_age = models.IntegerField(default=0)
    user_country = models.ForeignKey('Place', null=True, blank=True, related_name='user_country')
    user_location = models.ForeignKey('Place', null=True, blank=True, related_name='user_location')
    user_search_pref = models.CharField(max_length=255, default='')
    user_search_distance = models.IntegerField(default=0)
    num_female_results = models.IntegerField(default=0)
    num_nearby_results = models.IntegerField(default=0)
    currently_online = models.BooleanField(default=False)
    gender = models.CharField(max_length=15, default='all')
    num_results = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        self.modified = datetime.now()

        return super(QueryAnalytics, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.type


class ChatRequest(models.Model):
    sender = models.ForeignKey('MyUser', null=False, related_name='sender', blank=False)
    receiver = models.ForeignKey('MyUser', null=False, related_name='receiver', blank=False)
    status = models.CharField(max_length=100, choices=CHAT_REQUEST_STATUS, default='BLANK')
    message = models.CharField(max_length=255, null=True, blank=True, default='')
    is_deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.sender.first_name + " -> " + self.receiver.first_name


class CreditsConfiguration(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, default='default')
    sign_up = models.IntegerField(default=250)
    active_user = models.IntegerField(default=250)
    daily_active = models.IntegerField(default=50)
    like = models.IntegerField(default=2)
    invite_friend = models.IntegerField(default=50)
    chat_request = models.IntegerField(default=10)
    create_meetup = models.IntegerField(default=20)
    join_meetup = models.IntegerField(default=10)

    def __unicode__(self):
        return self.name


class Otp(models.Model):
    otp = models.CharField(max_length=10)
    login_id = models.CharField(max_length=100)
    expiry = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.login_id


class PushAnalytics(models.Model):
    user = models.ForeignKey('MyUser', null=True, blank=True)
    action = models.CharField(max_length=50, default='')
    label = models.CharField(max_length=50, default='')
    is_delivered = models.BooleanField(default=False)
    is_glynk_notif = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user.first_name


class MockUsers(models.Model):
    mock_user = models.ForeignKey('MyUser', related_name='mock_user', null=True, blank=True)
    user = models.ForeignKey('MyUser', related_name='org_user', null=True, blank=True)
    city = models.ForeignKey('Place', null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.mock_user.first_name


class UserMessaging(models.Model):
    community = models.ForeignKey('Community', null=True, blank=True)
    language = models.ForeignKey('Language', null=True, blank=True, default='', on_delete=models.SET_NULL)
    feed_create_post_card = models.CharField(max_length=255, default='')
    discover_tab_header = models.CharField(max_length=255, default='')
    discover_tab_filter_show_to = models.CharField(max_length=255, default='')
    discover_tab_loading = models.CharField(max_length=255, default='')
    discover_tab_empty_screen = models.CharField(max_length=255, default='')
    friends_tab_footer = models.CharField(max_length=255, default='Groups')
    friends_tab_header = models.CharField(max_length=255, default='Groups')
    meetup_tab_footer = models.CharField(max_length=255, default='Meetup')
    meetup_tab_header = models.CharField(max_length=255, default='Meetup')
    sdk_groups_header = models.CharField(max_length=255, default='Community')
    meetup_create_cta = models.CharField(max_length=255, default='MEET')
    meetup_empty_screen_label = models.TextField(null=True, blank=True,
                                                 default='Instantly let other members know that \nyou are free for a live discussion')
    interact_tab_footer = models.CharField(max_length=255, default='Feed')
    interact_tab_header = models.CharField(max_length=255, default='Feed')
    gallery_title = models.CharField(max_length=255, default='Gallery')
    support_email = models.CharField(max_length=255, default='')
    intro_welcome_text = models.CharField(max_length=255, default='')
    intro_welcome_message = models.CharField(max_length=255, default='')
    user_nomenclature = models.CharField(max_length=255, null=True, blank=True)
    admin_nomenclature = models.CharField(max_length=255, null=True, blank=True, default='Admin')
    area_screen_hint_text = models.CharField(max_length=255, default='E.g. Indiranagar')
    measurement_system = models.CharField(max_length=100, choices=(('IMPERIAL', 'Imperial'), ('METRIC', 'Metric')),
                                          default='METRIC')
    splash_app_name = models.CharField(max_length=100, default='Milo', null=True, blank=True)
    splash_image_1 = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    splash_image_2 = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    splash_image_3 = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    splash_image_4 = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    splash_text_1 = models.CharField(max_length=100, default='Know  your community', null=True, blank=True)
    splash_text_2 = models.CharField(max_length=100, default='Got free time?', null=True, blank=True)
    splash_text_3 = models.CharField(max_length=100, default='Shake your phone...', null=True, blank=True)
    splash_text_4 = models.CharField(max_length=100, default='Meet up!', null=True, blank=True)
    link_preview_title = models.CharField(max_length=100, null=True, blank=True, default='YOUR EXCLUSIVE ACCESS')
    link_preview_description = models.CharField(max_length=200, null=True, blank=True)
    link_preview_image = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    community_invite_message = models.TextField(null=True, blank=True,
                                                default='Quite a convenient way to know and meet people from our community. I\'ve already joined. Get it here and spread the word: [INVITE_LINK] \n\n _Please do not share this invite with anyone outside [COMMUNITY_NAME]._')
    sdk_invite_message = models.TextField(null=True, blank=True,
                                          default='Why haven\'t you joined yet? Join now using this link: [INVITE_LINK]')
    sdk_group_invite_message = models.TextField(null=True, blank=True,
                                                default='Hey, I would like you to join [GROUP_NAME] group on [COMMUNITY_NAME] app.\nDownload the app here: [DEEP_LINK]')
    nps_rating_view_title = models.TextField(null=True, blank=True, default='')
    nps_complete_view_title = models.TextField(null=True, blank=True, default='')
    nps_play_store_rating_view_title = models.TextField(null=True, blank=True, default='')
    nps_rating_image = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    nps_thanks_image = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    nps_play_store_rating_image = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    trial_experience_title_message = models.TextField(null=True, blank=True, default='')
    trial_experience_description_message = models.TextField(null=True, blank=True, default='')
    invite_screen_message1 = models.TextField(null=True, blank=True,
                                              default='Know someone who should be part of this community?\n Invite them!')
    invite_screen_message2 = models.TextField(null=True, blank=True, default='')
    onbd_interests_title = models.CharField(max_length=100, default='Pick your interests', null=True, blank=True)
    invite_button_text = models.CharField(max_length=20, default="Invite", blank=True, null=True)
    loading_screen_app_name = models.CharField(max_length=20, default="", blank=True, null=True)

    footer_banner_title = models.TextField(null=True, blank=True, default='')
    footer_banner_description = models.TextField(null=True, blank=True, default='')
    footer_banner_cta_text = models.TextField(null=True, blank=True, default='')

    def get_splash_image1(self):
        if not self.splash_image_1:
            return ''

        file_path = self.splash_image_1.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(str(file_path))
            return storage.url(filename_base) + filename_ext
        else:
            return ''

    def get_splash_image2(self):
        if not self.splash_image_2:
            return ''

        file_path = self.splash_image_2.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(str(file_path))
            return storage.url(filename_base) + filename_ext
        else:
            return ''

    def get_splash_image3(self):
        if not self.splash_image_3:
            return ''

        file_path = self.splash_image_3.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(str(file_path))
            return storage.url(filename_base) + filename_ext
        else:
            return ''

    def get_splash_image4(self):
        if not self.splash_image_4:
            return ''

        file_path = self.splash_image_4.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(str(file_path))
            return storage.url(filename_base) + filename_ext
        else:
            return ''

    def get_link_preview_image(self):
        if not self.link_preview_image:
            return self.community.get_image()

        file_path = self.link_preview_image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(str(file_path))
            return storage.url(filename_base) + filename_ext
        else:
            return ''

    def get_nps_rating_image(self):
        file_path = self.nps_rating_image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return ''

    def get_nps_thanks_image(self):
        file_path = self.nps_thanks_image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return ''

    def get_nps_play_store_rating_image(self):
        file_path = self.nps_play_store_rating_image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return ''

    def __unicode__(self):
        return self.community.name


class Education(models.Model):
    name = models.TextField()
    image = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    linkedin_id = models.CharField(max_length=150, null=True, blank=True)
    google_entity_id = models.CharField(max_length=150, null=True, blank=True)
    image_url = models.TextField()

    def get_image(self):
        file_path = self.image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return ""

    def __unicode__(self):
        return self.name


class WorkPlace(models.Model):
    name = models.TextField()
    image = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    linkedin_id = models.CharField(max_length=150, null=True, blank=True)
    google_entity_id = models.CharField(max_length=150, null=True, blank=True)
    community_specific = models.ForeignKey('Community', null=True, blank=True)
    image_url = models.TextField()

    def get_image(self):
        file_path = self.image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return ""

    def __unicode__(self):
        return self.name


class WorkDesignation(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to=upload_posts_to, null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def get_image(self):
        if not self.image:
            return ''

        file_path = self.image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(str(file_path))
            return storage.url(filename_base) + filename_ext
        else:
            return ''

    def __unicode__(self):
        return self.name or ''


class CollegeBranch(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    display_name = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=50, default='', choices=BRANCH_CATEGORIES)
    image = models.ImageField(upload_to=upload_posts_to, null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def get_image(self):
        if not self.image:
            return ''

        file_path = self.image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(str(file_path))
            return storage.url(filename_base) + filename_ext
        else:
            return ''

    def __unicode__(self):
        return self.name


class UserContacts(models.Model):
    user = models.ForeignKey('MyUser', null=True, blank=True)
    phone_number = models.CharField(max_length=20, default='')
    name = models.CharField(max_length=100, default='')
    community = models.ManyToManyField('Community', null=True, blank=True)

    class Meta:
        app_label = 'webapp'
        unique_together = (('phone_number', 'user'))


class UserDevice(models.Model):
    user = models.ForeignKey('MyUser', null=True, blank=True)
    device_id = models.TextField()
    device_type = models.CharField(max_length=100, default='')

    class Meta:
        app_label = 'webapp'

    def __unicode__(self):
        return self.user.first_name


class UITheme(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, default='')
    main_theme = models.CharField(max_length=100, null=True, blank=True)
    main_icon_color = models.CharField(max_length=100, null=True, blank=True)
    dual_tone_icon_color = models.CharField(max_length=100, null=True, blank=True)
    pri_cta_bgr = models.CharField(max_length=100, null=True, blank=True)
    pri_cta_label = models.CharField(max_length=100, null=True, blank=True)
    sec_cta_bgr = models.CharField(max_length=100, null=True, blank=True)
    sec_cta_label = models.CharField(max_length=100, null=True, blank=True)
    link_text = models.CharField(max_length=100, null=True, blank=True)
    sec_theme = models.CharField(max_length=100, null=True, blank=True)
    sec_theme_label = models.CharField(max_length=100, null=True, blank=True)
    status_icon_theme = models.CharField(max_length=100, choices=(('DARK', 'Dark'), ('LIGHT', 'Light')), default='Dark')
    counter_bgr = models.CharField(max_length=100, null=True, blank=True)
    counter_text = models.CharField(max_length=100, null=True, blank=True)
    highlight_1 = models.CharField(max_length=100, null=True, blank=True)
    highlight_2 = models.CharField(max_length=100, null=True, blank=True)
    web_css = models.TextField(default='', null=True, blank=True)

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.name and self.community:
            self.name = self.community.name
        return super(UITheme, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Reward(models.Model):
    title = models.CharField(max_length=50, default='', null=True, blank=True)
    community = models.ForeignKey('Community', null=True, blank=True)
    status = models.CharField(max_length=25, choices=REWARD_STATUS().get_choices(), null=True, blank=True)
    description = models.CharField(max_length=300, default='', null=True, blank=True)
    card_colour_default = models.CharField(max_length=10, default='', null=True, blank=True)
    card_colour_redeemed = models.CharField(max_length=10, default='', null=True, blank=True)
    total_referrals_required = models.IntegerField(default=0)
    terms_and_condition_url = models.CharField(max_length=500, default='', null=True, blank=True)
    logo = models.ImageField(upload_to=upload_misc_to, null=True, blank=True)
    expiry_date = models.DateTimeField()
    redeemed_title = models.CharField(max_length=100, default='', null=True, blank=True)
    redeemed_description = models.CharField(max_length=300, default='', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    reward_type = models.CharField(max_length=25, choices=REWARD_TYPE().get_choices(), null=True, blank=True)

    class Meta:
        app_label = 'webapp'

    def get_logo(self):
        file_path = self.logo.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return "https://d301sr5gafysq2.cloudfront.net/dc4237fa9a20/img/unmapped_author_32.png"

    def __unicode__(self):
        return self.title


class RewardCoupon(models.Model):
    reward = models.ForeignKey('Reward', null=True, blank=True)
    coupon_code = models.CharField(max_length=50, default='', null=True, blank=True)
    is_used = models.BooleanField(default=False)
    user_who_redeemed = models.ForeignKey('MyUser', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'webapp'

    def __unicode__(self):
        return self.coupon_code


class RewardTransaction(models.Model):
    user = models.ForeignKey('MyUser', blank=True, null=True, on_delete=models.SET_NULL)
    reward = models.ForeignKey('Reward', null=True, blank=True, related_name='reward')
    reward_coupon = models.ForeignKey('RewardCoupon', null=True, blank=True)
    transaction_status = models.CharField(max_length=25, choices=REWARD_TRANSACTIONS_STATUS().get_choices(), null=True,
                                          blank=True)
    is_redeemed = models.BooleanField(default=False)
    cash = models.IntegerField(default=0)
    pay_tm_cash = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'webapp'

    def __unicode__(self):
        return str(self.modified)


class UserPrivacySetting(models.Model):
    user = models.ForeignKey('MyUser', blank=True, null=True)
    tower = models.CharField(max_length=25, choices=PRIVACY_VISIBLE_TO().get_choices(),
                             default=PRIVACY_VISIBLE_TO.ALL_MEMBERS)
    gender = models.CharField(max_length=25, choices=PRIVACY_VISIBLE_TO().get_choices(),
                              default=PRIVACY_VISIBLE_TO.ALL_MEMBERS)
    birthday = models.CharField(max_length=25, choices=PRIVACY_VISIBLE_TO().get_choices(),
                                default=PRIVACY_VISIBLE_TO.ALL_MEMBERS)
    area = models.CharField(max_length=25, choices=PRIVACY_VISIBLE_TO().get_choices(),
                            default=PRIVACY_VISIBLE_TO.ALL_MEMBERS)
    city = models.CharField(max_length=25, choices=PRIVACY_VISIBLE_TO().get_choices(),
                            default=PRIVACY_VISIBLE_TO.ALL_MEMBERS)
    hometown = models.CharField(max_length=25, choices=PRIVACY_VISIBLE_TO().get_choices(),
                                default=PRIVACY_VISIBLE_TO.ALL_MEMBERS)
    workplace = models.CharField(max_length=25, choices=PRIVACY_VISIBLE_TO().get_choices(),
                                 default=PRIVACY_VISIBLE_TO.ALL_MEMBERS)
    designation = models.CharField(max_length=25, choices=PRIVACY_VISIBLE_TO().get_choices(),
                                   default=PRIVACY_VISIBLE_TO.ALL_MEMBERS)
    education = models.CharField(max_length=25, choices=PRIVACY_VISIBLE_TO().get_choices(),
                                 default=PRIVACY_VISIBLE_TO.ALL_MEMBERS)

    class Meta:
        app_label = 'webapp'

    def __unicode__(self):
        return str(self.user)


class GifMedia(models.Model):
    gif = models.ImageField(upload_to=upload_events_to, null=True, blank=True)
    preview = models.ImageField(upload_to=upload_events_to, null=True, blank=True)
    community = models.ForeignKey('Community')
    created = models.DateTimeField()
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()

        self.modified = datetime.now()

        return super(GifMedia, self).save(*args, **kwargs)

    def get_gif_url(self):
        file_path = self.gif.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(str(file_path))
            return storage.url(filename_base) + filename_ext
        else:
            return ''

    def get_preview_url(self):
        file_path = self.preview.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(str(file_path))
            return storage.url(filename_base) + filename_ext
        else:
            return ''

    def __unicode__(self):
        return self.gif.name


class ProfilePrompt(models.Model):
    question = models.TextField()
    hint_text = models.TextField(blank=True, null=True)
    is_hidden = models.BooleanField(default=False)
    user_tag = models.CharField(max_length=50, choices=USER_TAGS().get_choices(), null=True, blank=True, default='')
    created = models.DateTimeField()
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()

        self.modified = datetime.now()

        return super(ProfilePrompt, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.question


class MyUserProfilePrompt(models.Model):
    user = models.ForeignKey('MyUser', blank=True, null=True)
    profile_prompt = models.ForeignKey('ProfilePrompt')
    answer = models.TextField()
    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()

        self.modified = datetime.now()

        return super(MyUserProfilePrompt, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.answer


class Skill(models.Model):
    name = models.TextField(blank=False, null=False)
    selection_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class NPSSurvey(models.Model):
    user = models.ForeignKey('MyUser', blank=True, null=True)
    rating = models.IntegerField(default=0)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()

        self.modified = datetime.now()

        return super(NPSSurvey, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.user)


class PostGenericThrough(models.Model):
    post = models.ForeignKey('Post', blank=False, null=False)
    community = models.ForeignKey('Community', blank=False, null=False)
    content_type = models.ForeignKey(ContentType)
    content_id = models.CharField(max_length=10, blank=False, null=False)
    content_object = None

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if self.content_object is not None and isinstance(self.content_object, models.Model):
            self.content_type = ContentType.objects.get_for_model(self.content_object)
            self.content_id = str(self.content_object.pk)

        return super(PostGenericThrough, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.post) + ' -> ' + str(self.content_type) + ' -> ' + str(self.content_id)


class MyUserGenericThrough(models.Model):
    user = models.ForeignKey('Myuser', blank=False, null=False)
    community = models.ForeignKey('Community', blank=False, null=False)
    content_type = models.ForeignKey(ContentType)
    content_id = models.CharField(max_length=10, blank=False, null=False)
    content_object = None

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if self.content_object is not None and isinstance(self.content_object, models.Model):
            self.content_type = ContentType.objects.get_for_model(self.content_object)
            self.content_id = str(self.content_object.pk)

        return super(MyUserGenericThrough, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.user) + ' -> ' + str(self.content_type) + ' -> ' + str(self.content_id)


class Room(models.Model):
    reference_id = models.CharField(max_length=10, null=True, blank=True)  # Their system id
    name = models.CharField(max_length=100, null=True, blank=True)
    community = models.ForeignKey('Community', blank=True, null=True)
    apartment = models.ForeignKey('Apartment', null=True, blank=True)
    address = models.TextField(default='')
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    postcode = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        app_label = 'webapp'

    def __unicode__(self):
        return str(self.name)


class Apartment(models.Model):
    reference_id = models.CharField(max_length=10, null=True, blank=True)  # Their system id
    name = models.CharField(max_length=100, null=True, blank=True)
    community = models.ForeignKey('Community', blank=True, null=True)
    building = models.ForeignKey('Building', null=True, blank=True)
    address = models.TextField(default='')
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    postcode = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        app_label = 'webapp'

    def __unicode__(self):
        return str(self.name)


class Building(models.Model):
    reference_id = models.CharField(max_length=10, null=True, blank=True)  # Their system id
    name = models.CharField(max_length=100, null=True, blank=True)
    community = models.ForeignKey('Community', blank=True, null=True)
    lat = models.FloatField(default=0)
    long = models.FloatField(default=0)
    area = models.TextField(default='')
    address = models.TextField(default='')
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    postcode = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        app_label = 'webapp'

    def __unicode__(self):
        return str(self.name)


class ModerationKeyword(models.Model):
    community = models.ForeignKey('Community', blank=True, null=True)
    keyword = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return str(self.keyword)


class Language(models.Model):
    english_text = models.CharField(max_length=250, default='')
    native_text = models.CharField(max_length=250, default='')
    text_direction = models.CharField(max_length=50, default='')
    language_code = models.CharField(max_length=250, default='')

    class Meta:
        app_label = 'webapp'

    def __unicode__(self):
        return self.english_text


class StaticInfoSection(models.Model):
    name = models.CharField(max_length=255)
    unique_id = models.CharField(max_length=255, null=True, blank=True, unique=True,
                                 help_text="E.g: CommunityName_RelatedText")
    rank = models.IntegerField(default=1)
    community = models.ForeignKey('Community', null=True, blank=True)
    image = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    # 'icon' field is used in admin section cards when community admin_section_layout field is set to TILES
    icon = models.ImageField(upload_to=upload_topics_to, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_hidden = models.BooleanField(default=False)
    android_screen = models.CharField(max_length=250, choices=STATIC_INFO_SECTION_ANDROID_SCREEN, null=True, blank=True,
                                      default="")
    ios_screen = models.CharField(max_length=250, choices=STATIC_INFO_SECTION_IOS_SCREEN, null=True, blank=True,
                                  default="")
    parameters = models.TextField(null=True, blank=True)

    class Meta:
        app_label = 'webapp'

    def get_image(self):
        file_path = self.image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return "https://d301sr5gafysq2.cloudfront.net/dc4237fa9a20/img/unmapped_author_32.png"

    def get_icon(self):
        file_path = self.icon.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return "https://d301sr5gafysq2.cloudfront.net/dc4237fa9a20/img/unmapped_author_32.png"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
            self.unique_id = self.name
        self.modified = datetime.now()
        return super(StaticInfoSection, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class StaticInfo(models.Model):
    user = models.ManyToManyField('MyUser', null=True, blank=True)
    community = models.ForeignKey('Community', null=True, blank=True)

    title = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField()
    text_len = models.IntegerField(default=0)
    unique_url = models.CharField(max_length=255)
    rank = models.IntegerField(default=1)

    section = models.ForeignKey('StaticInfoSection', null=True, blank=True, on_delete=models.SET_NULL)
    sub_section = models.CharField(max_length=250, choices=STATIC_INFO_SUB_SECTION, null=True, blank=True, default="")

    is_hidden = models.BooleanField(default=0)
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    user_mentions = models.TextField(null=True, blank=True)
    privacy = models.CharField(max_length=50, choices=POST_PRIVACY().get_choices(), default='ALL')

    created = models.DateTimeField()
    modified = models.DateTimeField()

    image = models.ImageField(upload_to=upload_posts_to, null=True, blank=True)
    height = models.FloatField(default=0.0)
    width = models.FloatField(default=0.0)
    resized_height = models.FloatField(default=0.0)
    resized_width = models.FloatField(default=0.0)
    is_image_compressed = models.BooleanField(default=1)

    preview_image = models.ImageField(upload_to=upload_posts_to, null=True, blank=True)
    preview_height = models.FloatField(default=0.0)
    preview_width = models.FloatField(default=0.0)
    resized_preview_height = models.FloatField(default=0.0)
    resized_preview_width = models.FloatField(default=0.0)
    is_big_preview_image = models.BooleanField(default=False)

    original_preview_image = models.TextField(null=True, blank=True)
    preview_title = models.CharField(max_length=255, null=True, blank=True)
    preview_source = models.CharField(max_length=255, null=True, blank=True)
    preview_source_icon = models.ImageField(upload_to=upload_posts_to, null=True, blank=True)
    preview_link = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
            self.action_datetime = datetime.now()

        self.modified = datetime.now()
        super(StaticInfo, self).save(*args, **kwargs)

    def save_without_image_actions(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
            self.action_datetime = datetime.now()

        self.modified = datetime.now()

        super(StaticInfo, self).save(*args, **kwargs)

    def get_preview_image(self):
        file_path = self.preview_image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(str(file_path))

            if filename_ext in settings.WRONG_IMAGE_EXT:
                return storage.url(filename_base) + filename_ext

            return storage.url(filename_base + '_optimal') + filename_ext
        elif self.original_preview_image:
            original_preview_image = self.original_preview_image
            return original_preview_image
        else:
            return ''

    def get_image(self, force_large=False):
        post_media = PostMedia.objects.filter(post=self.id).first()
        if post_media is None:
            return ''

        return post_media.get_image(force_large)

    def get_images(self, force_large=False):
        images = []
        post_medias = PostMedia.objects.filter(post=self.id)
        for post_media in post_medias:
            if post_media:
                images.append(post_media.get_image(force_large))

        return images

    def get_preview_source_icon(self):
        file_path = self.preview_source_icon.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return 'https://d267x6x6dh1ejh.cloudfront.net/posts/8c9ab9b5-d7df-42ca-950c-7e94de9484a7.png'

    def get_video(self):
        post_media = PostMedia.objects.filter(post=self.id, type='VIDEO').first()
        if post_media is not None and post_media != '':
            return post_media.get_video()
        else:
            return ''

    def __unicode__(self):
        return self.text


class School(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    school_id = models.BigIntegerField(default=0)
    search_text = models.TextField(blank=True, null=True)
    block = models.CharField(max_length=100, null=True, blank=True)
    block_id = models.BigIntegerField(default=0)
    district = models.CharField(max_length=100, null=True, blank=True)
    district_id = models.BigIntegerField(default=0)
    community = models.ForeignKey('Community', blank=True, null=True)
    website = models.CharField(max_length=255, default='', blank=True)

    class Meta:
        app_label = 'webapp'

    def __unicode__(self):
        return str(self.id)


class SchoolGoing(models.Model):
    user = models.ForeignKey('MyUser')
    school = models.ForeignKey('School')
    year = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return str(self.user.id) + '-->' + str(self.school.id)


class MeetingRoom(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    image = models.ImageField(upload_to=upload_posts_to, null=True, blank=True)
    number_of_seats = models.IntegerField(default=0)
    interval_min = models.IntegerField(default=30)
    community = models.ForeignKey('Community', null=True, blank=True)
    community_branch = models.CharField(max_length=255, default='', blank=True)
    amenities = models.CharField(max_length=255, default='', blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    interval_credit_charges = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()

        self.modified = datetime.now()

        return super(MeetingRoom, self).save(*args, **kwargs)

    def get_image(self):
        file_path = self.image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return ""

    def __unicode__(self):
        return self.name


class MyuserBlacklistedCommunity(models.Model):
    myuser = models.ForeignKey('MyUser', related_name='myuserblacklistedcommunity_myuser')
    community = models.ForeignKey('Community', related_name='myuserblacklistedcommunity_community')
    reason = models.TextField(null=True, blank=True, default='')
    blacklisted_by = models.ForeignKey('MyUser', related_name='myuserblacklistedcommunity_blacklistedby', null=True,
                                       blank=True)
    blacklisted_on = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'webapp_myuser_blacklisted_community'

    def __unicode__(self):
        return self.myuser.first_name


class Booking(models.Model):
    user = models.ForeignKey('MyUser', null=True, blank=True)
    meeting_room = models.ForeignKey('MeetingRoom', null=True, blank=True)
    meeting_date = models.DateField()
    booked_slots = models.TextField(default='')
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    booking_status = models.CharField(max_length=25, choices=BOOKING_TYPE().get_choices(), null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()

        self.modified = datetime.now()

        super(Booking, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.first_name


class Auth(models.Model):
    user = models.ForeignKey('MyUser', null=True, blank=True)
    type = models.CharField(max_length=50)
    login_id = models.CharField(max_length=100)
    extra_data = models.TextField(default='')
    invite_ref = models.ForeignKey('Invite', null=True, blank=True)

    def __unicode__(self):
        return self.login_id


class Invite(models.Model):
    community = models.ForeignKey('Community', null=True, blank=True)
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    headquarters_place_ref = models.ForeignKey('Place', null=True, blank=True,
                                               related_name='invite_headquarters_place_ref', on_delete=models.SET_NULL)
    website = models.CharField(max_length=100, null=True, blank=True, default='')
    type = models.CharField(max_length=50, choices=INVITEE_TYPE().get_choices(), null=True, blank=True, default='')
    status = models.CharField(max_length=50, choices=INVITEE_STATUS().get_choices(), null=True, blank=True, default='')
    trial_start_date = models.DateTimeField(null=True, blank=True)
    trial_end_date = models.DateTimeField(null=True, blank=True)
    num_users = models.IntegerField(default=0)

    def __unicode__(self):
        return self.community.name + '-' + self.name


class ViewEmailActivity(models.Model):
    user = models.ForeignKey('MyUser', related_name='viewemailactivity_user')
    user_viewed = models.ForeignKey('MyUser', related_name='viewemailactivity_user_viewed')
    viewed_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user.username


class EmailSubscription(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255, unique=True, default="")

    def __unicode__(self):
        return self.email


class WebPluginTheme(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, default='')
    community = models.ManyToManyField('Community', null=True, blank=True)
    intro_title = models.CharField(max_length=100, null=True, blank=True, default='#212d33')
    intro_divider = models.CharField(max_length=100, null=True, blank=True, default='#00aeef')
    primary_cta_label = models.CharField(max_length=100, null=True, blank=True, default='#ffffff')
    primary_cta_bg = models.CharField(max_length=100, null=True, blank=True, default='#ff4081')
    events_title = models.CharField(max_length=100, null=True, blank=True, default='#212d33')
    events_divider = models.CharField(max_length=100, null=True, blank=True, default='#00aeef')
    events_dot = models.CharField(max_length=100, null=True, blank=True, default='#4a4a4a')
    secondary_cta_label = models.CharField(max_length=100, null=True, blank=True, default='#ffffff')
    secondary_cta_bg = models.CharField(max_length=100, null=True, blank=True, default='#00b7d8')
    secondary_theme_label = models.CharField(max_length=100, null=True, blank=True, default='#4a4a4a')
    secondary_theme_bg = models.CharField(max_length=100, null=True, blank=True, default='#ffea00')
    posts_title = models.CharField(max_length=100, null=True, blank=True, default='#212d33')
    posts_divider = models.CharField(max_length=100, null=True, blank=True, default='#00aeef')
    link_text = models.CharField(max_length=100, null=True, blank=True, default='#00b7d8')
    like_btn = models.CharField(max_length=100, null=True, blank=True, default='#ff4081')
    intro_bg = models.CharField(max_length=100, null=True, blank=True, default='#ffffff')
    events_bg = models.CharField(max_length=100, null=True, blank=True, default='#ffffff')
    posts_bg = models.CharField(max_length=100, null=True, blank=True, default='#f8f8f8')
    font_weight_normal = models.CharField(max_length=100, null=True, blank=True, default='400')
    font_weight_bold = models.CharField(max_length=100, null=True, blank=True, default='600')
    font_weight_xbold = models.CharField(max_length=100, null=True, blank=True, default='700')
    font_family = models.CharField(max_length=100, null=True, blank=True, default='')

    def __unicode__(self):
        return self.name

    def get_font_url(self):
        if self.font_family:
            fonts_url = "https://fonts.googleapis.com/css?family=" + self.font_family + ":100,200,300,400,500,600,700,800,900"
            return fonts_url
        return ''


class WebPluginMessaging(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, default='')
    community = models.ManyToManyField('Community', null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True, default='')
    description = models.TextField(null=True, blank=True, default='')
    cta_text = models.CharField(max_length=100, null=True, blank=True, default='')
    cta_link = models.TextField(null=True, blank=True, default='')

    def __unicode__(self):
        return self.name


class LiveNews(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    topic = models.CharField(max_length=255, null=True, blank=True, default='')
    unique_url = models.CharField(max_length=255)
    shares = models.BigIntegerField(default=0)
    likes = models.BigIntegerField(default=0)
    comments = models.BigIntegerField(default=0)
    spam = models.BigIntegerField(default=0)
    people_to_meet = models.ManyToManyField('PeopleToMeet', null=True, blank=True)
    created_by = models.ForeignKey('MyUser', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    edited_datetime = models.DateTimeField(null=True, blank=True)
    video = models.FileField(upload_to=upload_posts_to, null=True, blank=True)
    video_url = models.TextField()
    image = models.ImageField(upload_to=upload_posts_to, null=True, blank=True)
    is_hidden = models.BooleanField(default=0)
    height = models.FloatField(default=0.0)
    width = models.FloatField(default=0.0)
    resized_height = models.FloatField(default=0.0)
    resized_width = models.FloatField(default=0.0)
    views = models.BigIntegerField(default=0)
    community = models.ManyToManyField('Community', null=True, blank=True)
    comments_enabled = models.BooleanField(default=True)
    is_top_video = models.BooleanField(default=False)
    top_video_order_no = models.IntegerField(default=0)
    is_live = models.BooleanField(default=False)
    seo_page_title = models.CharField(max_length=255, null=True, blank=True, default='')
    seo_meta_description = models.TextField(null=True, blank=True, default='')
    youtube_video_id = models.TextField(null=True, blank=True)
    is_youtube_video = models.BooleanField(default=False)

    def get_image(self):
        file_path = self.image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return ""

    def get_optimal_image(self):
        file_path = self.image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(str(file_path))
            if self.resized_height:
                return storage.url(filename_base + '_optimal') + filename_ext
            else:
                return storage.url(filename_base) + filename_ext
        else:
            return ""

    def get_video(self):
        file_path = self.video.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return ""

    def get_share_link(self):
        unique_code = self.community.all().first().unique_code
        community = self.community.all().first()
        people_to_meet = self.people_to_meet.first()
        if community.custom_domain:
            invite_url = self.community.all().first().invite_url
        else:
            invite_url = self.community.all().first().invite_url + "/" + unique_code
        unique_url = invite_url + "/video/" + people_to_meet.url_path + "/" + str(self.unique_url.encode('ascii', 'ignore')) + "/?program_id=" + str(self.id)
        return unique_url

    def get_webapp_share_link(self):
        community = self.community.all().first()
        unique_code = community.unique_code
        people_to_meet = self.people_to_meet.first()
        post_type = None
        if people_to_meet and people_to_meet.url_path:
            post_type = "video/{0}".format(people_to_meet.url_path)

        if post_type:
            if community.custom_domain:
                unique_url = community.invite_url + "/" + post_type + "/" + self.unique_url
            else:
                unique_url = community.invite_url + "/" + unique_code + "/" + post_type + "/" + self.unique_url
            return unique_url

        return None

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        community = self.community.all().first()
        unique_code = community.unique_code
        people_to_meet = self.people_to_meet.first()
        post_type = None
        if people_to_meet and people_to_meet.url_path:
            post_type = "video/{0}".format(people_to_meet.url_path)

        if post_type:
            if community.custom_domain:
                unique_url = "/" + post_type + "/" + self.unique_url
            else:
                unique_url = "/" + unique_code + "/" + post_type + "/" + self.unique_url
            return unique_url

        return None

    def get_meta_title(self):
        if self.seo_page_title:
            return str(self.seo_page_title.encode("utf8")).strip()
        elif self.title:
            return str(self.title.encode("utf8")).strip()
        else:
            return ""

    def get_meta_description(self):
        if self.seo_meta_description:
            return str(self.seo_meta_description.encode("utf8")).strip()
        elif self.text:
            return str(self.text.encode("utf8")).strip()
        else:
            return ""


class InsightsKeyword(models.Model):
    community = models.ManyToManyField('Community', null=True, blank=True)
    keyword = models.CharField(max_length=255, null=True, blank=True, default='')
    type = models.CharField(max_length=50, choices=INSIGHTS_KEYWORD_TYPE().get_choices(), null=True, blank=True,
                            default='')

    def __unicode__(self):
        return self.keyword


class LoginRecord(models.Model):
    user = models.ForeignKey('MyUser', null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.id)


class ProgramComment(models.Model):
    created_by = models.ForeignKey('MyUser', null=True, blank=True)
    program = models.ForeignKey('LiveNews', null=False, blank=False)
    text = models.TextField()
    text_len = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    likes = models.BigIntegerField(default=0)
    spam = models.BigIntegerField(default=0)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    image = models.ImageField(upload_to=upload_posts_to, null=True, blank=True)
    preview_image = models.ImageField(upload_to=upload_posts_to, null=True, blank=True)
    preview_title = models.CharField(max_length=255, null=True, blank=True)
    preview_source = models.CharField(max_length=255, null=True, blank=True)
    preview_link = models.CharField(max_length=255, null=True, blank=True)
    community = models.ManyToManyField('Community', null=True, blank=True)
    is_hidden = models.BooleanField(default=0)
    is_video = models.BooleanField(default=0)
    entry_point = models.CharField(max_length=100, null=True, blank=True, default='')
    fb_comment_id = models.CharField(max_length=255, null=True, blank=True)
    external_integration = models.CharField(max_length=255, null=True, blank=True)
    external_integration_id = models.CharField(max_length=255, null=True, blank=True)
    user_mentions = models.TextField(null=True, blank=True)
    requires_moderation = models.BooleanField(default=False)
    moderation_reason = models.TextField(null=True, blank=True, default='')

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        self.modified = datetime.now()
        self.text_len = len(self.text)
        return super(ProgramComment, self).save(*args, **kwargs)

    def get_preview_image(self):
        file_path = self.preview_image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)

            if filename_ext == '.cms':
                return storage.url(filename_base) + filename_ext

            return storage.url(filename_base) + filename_ext
        else:
            return ''

    def get_image(self):
        file_path = self.image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)

            if filename_ext == '.cms':
                return storage.url(filename_base) + filename_ext

            return storage.url(filename_base) + filename_ext
        else:
            return ''

    def __unicode__(self):
        return self.text


class Advertisement(models.Model):
    ad_image = models.ImageField(upload_to=upload_advertisements_to, null=True, blank=True)
    ad_link = models.TextField(null=True, blank=True, default='')
    created = models.DateTimeField()
    is_hidden = models.BooleanField(default=False)
    community = models.ManyToManyField('Community', null=True, blank=True)
    ad_platform = models.CharField(max_length=256, choices=AD_PLATFORMS().get_choices(), default="Mobile_web") # Platform field for ads
    ad_type = models.CharField(max_length=256, choices=AD_TYPES().get_choices(), default="Square") # Type field for ads
    ad_format = models.CharField(max_length=256, choices=AD_FORMATS().get_choices(), default="Image")            # Format field for ads
    ad_media = models.FileField(upload_to=upload_advertisements_to, null=True, blank=True)   # ad_media field for videos
    posts = models.ManyToManyField('Post', null=True, blank=True)
    ad_visibility = models.CharField(max_length=256, choices=AD_VISIBILITY().get_choices(), default="ALL_ARTICLES")
    ad_clicks = models.BigIntegerField(default=0)
    ad_impressions = models.BigIntegerField(default=0)
    daily_impression_limit = models.BigIntegerField(default=0)
    has_limit = models.BooleanField(default=False)
    reached_daily_limit = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.id)

    def get_ad_image(self):
        file_path = self.ad_image.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return ""

    def get_ad_image_in_webp(self):
        file_path = self.ad_image.name
        if file_path:
            file_path = str(filepath_to_uri(file_path)).replace("//", "/")
            return settings.ARGUS_IMAGE_RESIZE_CDN + '/' + file_path
        else:
            return ""

    def get_ad_media(self):
        file_path = self.ad_media.name
        if file_path:
            filename_base, filename_ext = os.path.splitext(file_path)
            return storage.url(filename_base) + filename_ext
        else:
            return ""


class Widget(models.Model):
    type = models.CharField(max_length=50, choices=WIDGET_TYPES().get_choices(), default=WIDGET_TYPES.NONE)
    community = models.ForeignKey('Community', null=True, blank=True)
    is_hidden = models.BooleanField(default=False)
    config = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.type)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        super(Widget, self).save(*args, **kwargs)


class GoogleAdsConfig(models.Model):
    ad_unit_path = models.CharField(max_length=255, blank=True, default='')
    ad_unit_id = models.CharField(max_length=255, blank=True, default='')
    ad_height = models.IntegerField(default=0)
    ad_width = models.IntegerField(default=0)
    ad_platform = models.CharField(max_length=256, choices=GOOGLE_AD_PLATFORMS().get_choices(), default=GOOGLE_AD_PLATFORMS.MOBILE)
    ad_type = models.CharField(max_length=256, choices=GOOGLE_AD_TYPES().get_choices(), default=GOOGLE_AD_TYPES.TOP)
    community = models.ForeignKey('Community', null=True, blank=True)

    def __unicode__(self):
        return str(self.ad_platform) + "_" + str(self.ad_type) + "_google_ad"


class Contest(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True, default="")
    unique_url = models.TextField(null=True, blank=True, default='')
    link_url = models.TextField(null=True, blank=True, default='')
    status = models.BooleanField(default=True)
    community = models.ForeignKey('Community', null=True, blank=True)
    created = models.DateTimeField()

    class Meta:
        app_label = 'webapp'

    def __unicode__(self):
        return str(self.id) + "-" + str(self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        super(Contest, self).save(*args, **kwargs)

    def get_contest_share_link(self):
        community = self.community
        unique_url = community.invite_url + "/" + "contest" + "/" + self.unique_url
        return unique_url


class CommunityEmailSubscription(models.Model):
    email = models.CharField(max_length=255, null=True, blank=True)
    community = models.ForeignKey('Community', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __unicode__(self):
        return str(self.id) + "_" + str(self.email)


class AdImpression(models.Model):
    ad = models.ForeignKey('Advertisement', null=True, blank=True, related_name='ads_impressions',
                           on_delete=models.SET_NULL)
    date_time = models.DateTimeField(auto_now_add=True)
    session_id = models.TextField(null=True, blank=True, default='')
    type = models.CharField(max_length=50, choices=AD_IMPRESSION_TYPE().get_choices(), null=True, blank=True,
                            default='')

    def __unicode__(self):
        if self.ad:
            return str(self.ad.id)
        else:
            return "NONE"


class AdClick(models.Model):
    ad = models.ForeignKey('Advertisement', null=True, blank=True, related_name='ads_clicks',
                           on_delete=models.SET_NULL)
    date_time = models.DateTimeField(auto_now_add=True)
    session_id = models.TextField(null=True, blank=True, default='')
    type = models.CharField(max_length=50, choices=AD_IMPRESSION_TYPE().get_choices(), null=True, blank=True,
                            default='')

    def __unicode__(self):
        if self.ad:
            return str(self.ad.id)
        else:
            return "NONE"



class EmailLog(models.Model):
    community = models.ForeignKey('Community', null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey('MyUser', null=True, blank=True, on_delete=models.SET_NULL)
    email_id = models.CharField(max_length=255, null=True, blank=True)
    email_type = models.CharField(max_length=50, choices=EMAIL_TEMPLATE_TYPE().get_choices())
    content_type = models.CharField(max_length=255, null=True, blank=True)
    content_id = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        self.modified = datetime.now()
        return super(EmailLog, self).save(*args, **kwargs)


class LiveUpdate(models.Model):
    created_by = models.ForeignKey('MyUser', null=True, blank=True, related_name='live_update_created_by')
    title = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    unique_url = models.CharField(max_length=255)
    published_date = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField()
    modified = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=upload_live_updates_to, null=True, blank=True)
    is_hidden = models.BooleanField(default=False)
    community = models.ManyToManyField('Community', null=True, blank=True)
    unique_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    language = models.ForeignKey('Language', null=True, blank=True, default='', on_delete=models.SET_NULL)
    seo_meta_title = models.CharField(max_length=255, null=True, blank=True, default='')
    seo_meta_description = models.TextField(null=True, blank=True, default='')
    is_enable = models.BooleanField(default=False)

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
            self.unique_id = shortuuid.ShortUUID(alphabet="23456789abcdefghijkmnopqrstuvwxyz").random(length=12)

        self.modified = datetime.now()
        super(LiveUpdate, self).save(*args, **kwargs)

    def get_image(self):
        file_path = self.image.name
        if file_path:
            return storage.url(file_path)
        else:
            return ""

    def __unicode__(self):
        return self.title

    def get_webapp_share_link(self):
        community = self.community.all().first()
        post_type = 'live-updates'
        if community.custom_domain:
            unique_url = community.invite_url + "/" + post_type + "/" + self.unique_url
            return unique_url
        else:
            return ""

    def get_meta_title(self):
        if self.seo_meta_title:
            return str(self.seo_meta_title.encode("utf8")).strip()
        elif self.title:
            return str(self.title.encode("utf8")).strip()
        else:
            return ""

    def get_meta_description(self):
        if self.seo_meta_description:
            return str(self.seo_meta_description.encode("utf8")).strip()
        elif self.text:
            return str(self.text.encode("utf8")).strip()
        else:
            return ""


class LiveUpdateDetail(models.Model):
    created_by = models.ForeignKey('MyUser', null=True, blank=True, related_name='live_update_detail_created_by')
    live_update = models.ForeignKey('LiveUpdate', null=False, blank=False)
    title = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField()
    modified = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=upload_live_updates_to, null=True, blank=True)
    is_hidden = models.BooleanField(default=False)
    unique_id = models.CharField(max_length=50, unique=True, null=True, blank=True)

    class Meta:
        app_label = 'webapp'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
            self.unique_id = shortuuid.ShortUUID(alphabet="23456789abcdefghijkmnopqrstuvwxyz").random(length=12)

        self.modified = datetime.now()
        super(LiveUpdateDetail, self).save(*args, **kwargs)

    def get_image(self):
        file_path = self.image.name
        if file_path:
            return storage.url(file_path)
        else:
            return ""

    def __unicode__(self):
        return self.title
