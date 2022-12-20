import random

from webapp.meta_models import ProfileInfo
from webapp.meta_models import PeopleDiscoveryFilter as FILTERS


def get_profile_infos(show_section_headers, user, is_request_user, profile_infos):
    """
    Params
    -------------

    :param show_section_headers:
    :param user: User object
    :param is_request_user: True if the user is same as the request.user
    :param profile_infos: Profile info list configured
    :return: List of formatted profile info objects
    """

    user_profile_obj = {
        'user_profile_infos': [],
        'section_header': None,
        'sections': [],
        'section_footers': [],
        'current_section_header_title': None,
        'show_section_headers': show_section_headers,
    }

    valid_profile_infos = ProfileInfo().convert_to_list()

    for profile_info in profile_infos:
        """
        For each profile info we show the information in a formatted text if the data is available.
        When the data is not available and if the is_request_user flag is True,
        we show profile prompt text to collect the data

        ------------------------------
        Check if the screen exists in the list of supported screen.
        If screen is not part of valid screens list remove the screen to avoid front-end crash

        """

        if profile_info not in valid_profile_infos:
            continue
        {
            ProfileInfo.INFO_CURRENT_CITY: add_current_city,
            ProfileInfo.INFO_HOME_TOWN: add_home_town,
            ProfileInfo.INFO_EDUCATION: add_college,
            ProfileInfo.INFO_WORKPLACE: add_workplace,
            ProfileInfo.INFO_HEAD_QUARTERS: add_head_quarters,
            ProfileInfo.INFO_WEB_URL: add_web_url,
            ProfileInfo.INFO_VIEW_EMAIL: add_email,
            ProfileInfo.INFO_SCHOOL: add_schools,
            ProfileInfo.INFO_JOINED_DATE: add_joined_date,
            ProfileInfo.INFO_READ_ARTICLES: add_read_articles,
            ProfileInfo.INFO_NUM_COMMENTS: add_num_comments,
        }.get(profile_info, do_nothing)(user, is_request_user, profile_info, user_profile_obj)

    " To add last sections, section_header and section_footer in the item list "
    add_to_profile_list(user_profile_obj)

    return user_profile_obj['user_profile_infos']


def do_nothing(user, is_request_user, profile_info, user_profile_obj):
    pass


def append_profile_info(formatted_text, profile_info, is_empty, show_edit_icon, data_id, user_profile_obj):
    if formatted_text:
        section_header_title = get_section_header_title(profile_info)
        if user_profile_obj['current_section_header_title'] != section_header_title:
            add_to_profile_list(user_profile_obj)

            user_profile_obj['section_header'] = None
            user_profile_obj['sections'] = []
            user_profile_obj['section_footers'] = []

            add_section_header(profile_info, user_profile_obj)

        profile_info_obj = {
                'type': profile_info,
                'formatted_text': formatted_text,
                'is_empty': is_empty,
                'show_edit_icon': show_edit_icon,
                'data_id': data_id
            }

        if not is_empty:
            user_profile_obj['sections'].append(profile_info_obj)
        else:
            user_profile_obj['section_footers'].append(profile_info_obj)


def get_filter_tag(filter_type, filter_id, filter_text):
    return '<profile filter-type="{}" filter-id="{}">{}</profile>'.format(filter_type, filter_id,
                                                                          filter_text.encode("utf8"))


def add_section_header(profile_info, user_profile_obj):
    user_profile_obj['section_header'] = {
        'type': 'SECTION_HEADER',
        'formatted_text': get_section_header_title(profile_info),
    }

    user_profile_obj['current_section_header_title'] = get_section_header_title(profile_info)


def get_section_header_title(profile_info):
    text = {
        ProfileInfo.INFO_CURRENT_CITY: 'Places',
        ProfileInfo.INFO_HOME_TOWN: 'Places',
        ProfileInfo.INFO_COMMUNITY_BRANCH: 'Places',
        ProfileInfo.INFO_HEAD_QUARTERS: 'Places',

        ProfileInfo.INFO_EDUCATION: 'Education',
        ProfileInfo.INFO_COLLEGE_BRANCH: 'Education',
        ProfileInfo.INFO_COLLEGE_ADMIS_YEAR: 'Education',
        ProfileInfo.INFO_SCHOOL: 'Education',

        ProfileInfo.INFO_WORKPLACE: 'Work',
        ProfileInfo.INFO_WEB_URL: 'Work',
        ProfileInfo.INFO_VIEW_EMAIL: 'Work',
    }

    return text.get(profile_info, 'About')


def add_to_profile_list(user_profile_obj):
    if user_profile_obj['section_header'] and user_profile_obj['show_section_headers']:
        user_profile_obj['user_profile_infos'].append(user_profile_obj['section_header'])

    if user_profile_obj['sections']:
        user_profile_obj['user_profile_infos'].extend(user_profile_obj['sections'])

    if user_profile_obj['section_footers']:
        user_profile_obj['user_profile_infos'].extend(user_profile_obj['section_footers'])


def add_current_city(user, is_request_user, profile_info, user_profile_obj):
    """
    Area and City info format: 'living in <area>, <city>', 'living in <area>',
    'living in <city>', 'Add your area'
    """

    data_id = ""
    is_empty = False
    formatted_text = None
    show_edit_icon = is_request_user

    if user.area_place_ref and user.city_place_ref:
        formatted_text = "living in {}, {}".format(
            get_filter_tag(FILTERS.FILTER_TYPE_AREA, user.area_place_ref.id, user.area_place_ref.name),
            get_filter_tag(FILTERS.FILTER_TYPE_CURRENT_CITY, user.city_place_ref.id, user.city_place_ref.name))

    elif user.area_place_ref:
        formatted_text = "living in {}".format(
            get_filter_tag(FILTERS.FILTER_TYPE_AREA, user.area_place_ref.id, user.area_place_ref.name))

    elif user.city_place_ref:
        formatted_text = "living in {}".format(
            get_filter_tag(FILTERS.FILTER_TYPE_CURRENT_CITY, user.city_place_ref.id, user.city_place_ref.name))

    else:
        if is_request_user:
            is_empty = True
            show_edit_icon = False
            formatted_text = get_filter_tag(FILTERS.FILTER_TYPE_AREA, "", "Add area")

    append_profile_info(formatted_text, profile_info, is_empty, show_edit_icon, data_id, user_profile_obj)


def add_home_town(user, is_request_user, profile_info, user_profile_obj):
    """
    Hometown info format: 'from <hometown>', 'Add your hometown'
    """

    data_id = ""
    is_empty = False
    formatted_text = None
    show_edit_icon = is_request_user

    if user.hometown_place_ref:
        formatted_text = "from {}".format(
            get_filter_tag(FILTERS.FILTER_TYPE_HOMETOWN, user.hometown_place_ref.id,
                           user.hometown_place_ref.name))

    else:
        if is_request_user:
            is_empty = True
            show_edit_icon = False
            formatted_text = get_filter_tag(FILTERS.FILTER_TYPE_HOMETOWN, "", "Add hometown")

    append_profile_info(formatted_text, profile_info, is_empty, show_edit_icon, data_id, user_profile_obj)


def add_college(user, is_request_user, profile_info, user_profile_obj):
    """
    College info format: 'studied at <college_name>', 'Add your college'
    """

    data_id = ""
    is_empty = False
    formatted_text = None
    show_edit_icon = is_request_user

    if user.education_ref:
        formatted_text = "studied at {}".format(
            get_filter_tag(FILTERS.FILTER_TYPE_COLLEGE, user.education_ref.id, user.education_ref.name))

    else:
        if is_request_user:
            is_empty = True
            show_edit_icon = False
            formatted_text = get_filter_tag(FILTERS.FILTER_TYPE_COLLEGE, "", "Add college")

    append_profile_info(formatted_text, profile_info, is_empty, show_edit_icon, data_id, user_profile_obj)


def add_workplace(user, is_request_user, profile_info, user_profile_obj):
    """
    Workplace info format: 'is <designation> at <workplace>', 'works at <workplace>', 'is <designation>', 'Add your workplace'
    """

    data_id = ""
    is_empty = False
    formatted_text = None
    show_edit_icon = is_request_user

    if user.workplace_ref and user.work_designation_ref:
        formatted_text = "is {} at {}".format(
            get_filter_tag(FILTERS.FILTER_TYPE_DESIGNATION, user.work_designation_ref.name,
                           user.work_designation_ref.name),
            get_filter_tag(FILTERS.FILTER_TYPE_WORKPLACE, user.workplace_ref.id, user.workplace_ref.name))

    elif user.workplace_ref:
        formatted_text = "works at {}".format(
            get_filter_tag(FILTERS.FILTER_TYPE_WORKPLACE, user.workplace_ref.id, user.workplace_ref.name))

    elif user.work_designation_ref:
        formatted_text = "is {}".format(
            get_filter_tag(FILTERS.FILTER_TYPE_DESIGNATION, user.work_designation_ref.name,
                           user.work_designation_ref.name))

    else:
        if is_request_user and user.work_status:
            is_empty = True
            show_edit_icon = False
            formatted_text = get_filter_tag(FILTERS.FILTER_TYPE_WORKPLACE, "", "Add workplace")

    append_profile_info(formatted_text, profile_info, is_empty, show_edit_icon, data_id, user_profile_obj)


def add_head_quarters(user, is_request_user, profile_info, user_profile_obj):
    """
    Headquaters info format: 'headquartered at <city_name>', 'Add your head quarters'
    """
    data_id = ""
    is_empty = False
    formatted_text = None
    show_edit_icon = is_request_user

    if user.headquarters_place_ref:
        headquarters = user.headquarters_place_ref.name
        if user.headquarters_place_ref.country:
            headquarters += ', ' + user.headquarters_place_ref.country.name
        formatted_text = "headquartered at {}".format(
            get_filter_tag(FILTERS.FILTER_TYPE_HEADQUARTERS, user.headquarters_place_ref.id, headquarters))
    else:
        if is_request_user:
            is_empty = True
            show_edit_icon = False
            formatted_text = get_filter_tag(FILTERS.FILTER_TYPE_HEADQUARTERS, "", "Add headquarters")

    append_profile_info(formatted_text, profile_info, is_empty, show_edit_icon, data_id, user_profile_obj)


def add_web_url(user, is_request_user, profile_info, user_profile_obj):
    """
    Website info format: '<website_url>', 'Add your website'
    """
    data_id = ""
    is_empty = False
    formatted_text = None
    show_edit_icon = False

    if user.website:
        formatted_text = get_filter_tag("WEBSITE", user.website, user.website)

    append_profile_info(formatted_text, profile_info, is_empty, show_edit_icon, data_id, user_profile_obj)


def add_email(user, is_request_user, profile_info, user_profile_obj):
    """
    Email info format: 'View email'
    """
    data_id = ""
    is_empty = False
    formatted_text = None
    show_edit_icon = False

    if user.official_email:
        formatted_text = get_filter_tag("VIEW_EMAIL", "", "View email")

    append_profile_info(formatted_text, profile_info, is_empty, show_edit_icon, data_id, user_profile_obj)


def add_schools(user, is_request_user, profile_info, user_profile_obj):
    """
    School info format: 'went to <school_name> (Batch of <year>)' 'Add your school'
    """

    formatted_text = None
    show_edit_icon = is_request_user

    if user.schools.count() > 0:

        for school_going in user.schools.through.objects.filter(user=user).order_by('-year'):

            if school_going.school and school_going.year:
                formatted_text = "went to {} (Batch of {})".format(
                    get_filter_tag(FILTERS.FILTER_TYPE_SCHOOL, school_going.school.id,
                                   school_going.school.name),
                    str(school_going.year))

            elif school_going.school:
                formatted_text = "went to {}".format(
                    get_filter_tag(FILTERS.FILTER_TYPE_SCHOOL, school_going.school.id,
                                   school_going.school.name))
            data_id = school_going.id
            append_profile_info(formatted_text, profile_info, False, show_edit_icon, data_id, user_profile_obj)

    if is_request_user:
        if user.schools.count() < 3:
            formatted_text = get_filter_tag(FILTERS.FILTER_TYPE_SCHOOL, "", "Add school")
            append_profile_info(formatted_text, profile_info, True, False, "", user_profile_obj)


def add_joined_date(user, is_request_user, profile_info, user_profile_obj):
    """
    Website info format: '<website_url>', 'Add your website'
    """
    data_id = ""
    is_empty = False
    formatted_text = None
    show_edit_icon = False

    if user.date_joined:
        formatted_text = "member since {}".format(get_filter_tag("FILTER_TYPE_DATA", "FILTER_TYPE_DATA", str(user.date_joined.strftime("%b %Y"))))

    append_profile_info(formatted_text, profile_info, is_empty, show_edit_icon, data_id, user_profile_obj)


def add_read_articles(user, is_request_user, profile_info, user_profile_obj):
    """
    Website info format: '<website_url>', 'Add your website'
    """
    data_id = ""
    is_empty = False
    formatted_text = None
    show_edit_icon = False

    formatted_text = "read {} articles".format(get_filter_tag("FILTER_TYPE_DATA", "FILTER_TYPE_DATA", str(random.randint(10, 100))))

    append_profile_info(formatted_text, profile_info, is_empty, show_edit_icon, data_id, user_profile_obj)


def add_num_comments(user, is_request_user, profile_info, user_profile_obj):
    """
    Website info format: '<website_url>', 'Add your website'
    """
    data_id = ""
    is_empty = False
    formatted_text = None
    show_edit_icon = False

    formatted_text = "wrote {} comments".format(get_filter_tag("FILTER_TYPE_DATA", "FILTER_TYPE_DATA", str(random.randint(10, 100))))

    append_profile_info(formatted_text, profile_info, is_empty, show_edit_icon, data_id, user_profile_obj)
