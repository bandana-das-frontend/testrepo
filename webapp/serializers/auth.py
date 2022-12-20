from webapp.controllers.helpers.get_filter_choices import get_filter_choices
from webapp.dbplatform import *
from webapp.serializers.user import user_serializers_on_auth
# from webapp.tasks.email_tasks import send_mail_to_tech


def auth_serializers(request, user):
    config = get_configuration()

    if user.country_place_ref and user.country_place_ref.id == 2913:
        people_discovery_distance = config.people_discovery_distance_usa
    else:
        people_discovery_distance = config.people_discovery_distance

    my_feed_enabled_cities = get_configuration().my_feed_enabled_cities.split(",")
    filter(None, my_feed_enabled_cities)
    my_feed_enabled_cities = map(int, my_feed_enabled_cities)

    if config.my_feed_enabled and user.city_place_ref and user.city_place_ref.id in my_feed_enabled_cities:
        show_my_feed = True
    else:
        show_my_feed = False

    show_online_status = config.show_online_status

    if user.id == 139:
        show_online_status = False

    community = user.community.all()[0]

    if community.community_type == CommunityType.APARTMENT:
        show_my_feed = False

    filter_choices = get_filter_choices(community)

    create_post_prompt_messages_cta_text = 'POST TO COMMUNITY'
    create_post_prompt_messages = [
        {'question': 'What are you up to?',
         'cta': create_post_prompt_messages_cta_text,
         'image': user.community.all()[0].get_app_icon_image()},
        # {'question': 'Listening to a song on repeat?',
        #  'cta': create_post_prompt_messages_cta_text,
        #  'image': 'https://d267x6x6dh1ejh.cloudfront.net/topics/2bce24da-a10c-41ce-b604-b54f58612f1e.jpg'},
        # {'question': 'Loving the book you are reading?',
        #  'cta': create_post_prompt_messages_cta_text,
        #  'image': 'https://d267x6x6dh1ejh.cloudfront.net/topics/973d7d85-d348-4259-8e17-f25123d4e664.jpg'},
        # {'question': 'Do you write poems?',
        #  'cta': create_post_prompt_messages_cta_text,
        #  'image': 'https://d267x6x6dh1ejh.cloudfront.net/topics/84f378b8-0d78-4d44-b4f1-68fde85910d7.jpg'},
        # {'question': 'Which show are you watching?',
        #  'cta': create_post_prompt_messages_cta_text,
        #  'image': 'https://d267x6x6dh1ejh.cloudfront.net/topics/c284c2f2-55a2-448f-b418-fdddff29be2e.jpg'},
    ]

    # Get on-boarding steps for the user
    onboarding_steps = get_user_onboarding_steps(user)

    # Get feed filters for the user and community
    feed_filters = get_feed_filters(user)

    data = {
        'user': user_serializers_on_auth(request, user),
        'user_match_threshold': [
            config.percentage_match_bucket_1,
            config.percentage_match_bucket_2
        ],
        'configurations': {
            'feed_filters': feed_filters,
            'onboarding_steps': onboarding_steps,
            'character_limit_status': config.character_limit_status,
            'character_limit_post': config.character_limit_post,
            'min_character_limit_post': config.min_character_limit_post,
            'character_limit_post_comment': config.character_limit_post_comment,
            'min_onboarding_polls': config.min_onboarding_polls,
            'num_poll_recommendations': config.num_poll_recommendations,
            'checkout_threshold_time': config.checkout_threshold_time,
            'checkin_radius': config.checkin_radius,
            'min_percentage_match_to_chat': config.min_percentage_match_to_chat,
            'min_checkin_note_len': config.min_checkin_note_len,
            'max_checkin_note_len': config.max_checkin_note_len,
            'show_mcp': config.show_mcp,
            'show_mcp_skip': config.show_mcp_skip,
            'banned_words': config.banned_words,
            'people_discovery_distance': people_discovery_distance,
            'people_discovery_age': config.people_discovery_age,
            'daily_chat_request_limit': config.max_chat_receive_requests,
            'max_ask_reco_char_limit': config.max_ask_reco_char_limit,
            'show_online_status': show_online_status,
            'new_user_landing': config.new_user_landing_screen,
            'dont_show_footer_seconds': config.dont_show_footer_seconds,
            'show_my_feed': show_my_feed,
            'show_custom_gifs': community.show_custom_gifs,
            'show_meetup_location': community.show_meetup_location,
            'default_my_switch': community.default_tab,
            'share_url': community.invite_url,
            'collect_college_work_home_info': config.collect_college_work_home_info,
            'shake_sensitivity': config.shake_sensitivity,
            'shake_count': config.shake_count,
            'shake_sensitivity_in_app': config.shake_sensitivity_in_app,
            'shake_count_in_app': config.shake_count_in_app,
            'bing_subscription_key': config.bing_subscription_key,
            'google_subscription_key': config.google_subscription_key,
            'tmdb_subscription_key': config.tmdb_subscription_key,
            'people_discovery_filter_choices': filter_choices,
            'enable_ios_onboard_skip': config.enable_ios_onboard_skip,
            'create_shortcut': config.create_shortcut,
            'create_post_prompt_messages': create_post_prompt_messages,
        },
        'min_app_version': community.min_android_app_version,
        'latest_app_version': community.latest_android_app_version,
        'min_ios_app_version': community.min_ios_app_version,
        'latest_ios_app_version': community.latest_ios_app_version,
        'signup_notif_timer': config.signup_notif_timer,
    }

    return data


def get_user_onboarding_steps(user):
    onboarding_steps = []

    # Get community of the user
    community = user.community.all().first()

    # If community is not set return empty list
    if not community:
        return onboarding_steps

    if user.is_guest_user:
        return onboarding_steps

    # Get on-boarding screens configured for the community
    community_onboarding_screens = community.get_onboarding_screens()

    # For corpgini startup profile type overide the onboarding config list to remove workplace
    if community.unique_code == 'CorpGini':
        if user.user_tag == USER_TAGS.STARTUP:
            community_onboarding_screens = [OnboardingScreens.WELCOME_SCREEN,
                                            OnboardingScreens.COLLECT_PROFILE_PIC,
                                            OnboardingScreens.COLLECT_INTERESTS]

    valid_screens = OnboardingScreens().get_str_list()

    # Looping through the list of screens, to check if skip is enabled.
    for screen in community_onboarding_screens:
        skip = False
        # Check if '_$SKIP' exists in the screen name, if exists then skip flag should be enabled for the screen
        # example: 'COLLECT_HOMETOWN_$SKIP'
        if '_$SKIP' in screen:
            skip = True
            # Replace '_$SKIP' in the screen name with ''
            # example: 'COLLECT_HOMETOWN'
            screen = screen.replace('_$SKIP', '')

        # Check if the screen exists in the list of supported screen.
        # If screen is not part of valid screens list remove the screen to avoid front-end crash
        if screen not in valid_screens:
            # send_mail_to_tech.delay("Invalid Onboarding Screen : {} community : {}".format(screen, community.name), "")
            continue

        # If the user is on-boarded, show only the screens which are not skip-able and the data is not filled
        if user.is_onboarded:

            # WELCOME_SCREEN is not added for onboarded user
            if screen == OnboardingScreens.WELCOME_SCREEN:
                continue

            # COLLECT_COMMUNITY_BRANCH screen is not added, if user community_branch is set
            if screen == OnboardingScreens.COLLECT_COMMUNITY_BRANCH:
                if user.community_branch:
                    continue

            # COLLECT_NAME screen is not added, if user first_name or last_name is set
            if screen == OnboardingScreens.COLLECT_NAME:
                if user.first_name or user.last_name:
                    continue

            # COLLECT_GENDER screen is not added, if user gender is set
            elif screen == OnboardingScreens.COLLECT_GENDER:
                if user.gender:
                    continue

            # COLLECT_DOB screen is not added, if user birthday is set
            elif screen == OnboardingScreens.COLLECT_DOB:
                if user.birthday:
                    continue

            # COLLECT_AREA screen is not added, if user area_place_ref is set
            elif screen == OnboardingScreens.COLLECT_AREA:
                if user.area_place_ref:
                    continue

            # COLLECT_HOMETOWN screen is not added, if user hometown_place_ref is set
            elif screen == OnboardingScreens.COLLECT_HOMETOWN:
                if user.hometown_place_ref:
                    continue

            # COLLECT_PROFILE_PIC screen is not added, if user profile_picture_ref is set
            elif screen == OnboardingScreens.COLLECT_PROFILE_PIC:
                if user.profile_picture_ref:
                    continue

            # COLLECT_COLLEGE screen is not added, if user education_ref is set
            elif screen == OnboardingScreens.COLLECT_COLLEGE:
                if user.education_ref:
                    continue

            # COLLECT_COLLEGE_BRANCH screen is not added, if user college_branch_ref is set
            elif screen == OnboardingScreens.COLLECT_COLLEGE_BRANCH:
                if user.college_branch_ref:
                    continue

            # COLLECT_COLLEGE_RELATION screen is not added, if user college_relation is set
            elif screen == OnboardingScreens.COLLECT_COLLEGE_RELATION:
                if user.college_relation:
                    continue

            # COLLECT_SCHOOL screen is not added, if users schools is empty
            elif screen == OnboardingScreens.COLLECT_SCHOOL:
                if user.schools.count() > 0:
                    continue

            # COLLECT_APARTMENT screen is not added, if user apartment_flat_number is set
            elif screen == OnboardingScreens.COLLECT_APARTMENT:
                if user.apartment_flat_number:
                    continue

            # COLLECT_WORKPLACE screen is not added, if user workplace_ref is set or if user is marked as not working
            elif screen == OnboardingScreens.COLLECT_WORKPLACE:
                if user.workplace_ref or not user.work_status:
                    continue

            # COLLECT_INTERESTS screen is not added, if user has chosen at-least 1 interests
            elif screen == OnboardingScreens.COLLECT_INTERESTS:
                if user.people_to_meet.all().count() >= 1:
                    continue

            # In on-boarded case, skip enabled screens should not be added
            if skip:
                continue

        onboarding_steps.append({
            'name': screen,
            'skip': skip
        })
        # end of for loop

    return onboarding_steps


def get_feed_filters(user):
    community = user.community.all().first()
    if not community:
        return []

    feed_filters = community.get_feed_filters()
    feed_filters_list = []
    for filter_type in feed_filters:
        filter_text = None

        if filter_type == FeedContentType.ALL:
            filter_text = 'Everywhere'

        elif filter_type == FeedContentType.AREA:
            if user.area_place_ref:
                filter_text = user.area_place_ref.name

        elif filter_type == FeedContentType.CITY:
            if user.city_place_ref:
                filter_text = user.city_place_ref.name

        elif filter_type == FeedContentType.BRANCH:
            if user.community_branch:
                filter_text = user.community_branch

        if filter_text:
            feed_filters_list.append({
                'filter_text': filter_text,
                'filter_type': filter_type,
            })

    return feed_filters_list