from django.shortcuts import render_to_response
from django.template import RequestContext
from webapp.controllers.widgets.weather import fetch_weather_api_data
from webapp.controllers.utils.get_language import get_language
from webapp.models import *
from django.utils import translation
from django.core.cache import cache


def render_to_template(template_name, data, request):
    community = request.community
    language = get_language(request)

    translation.activate(request.session['lang_code'])
    language_code_long = 'LANGUAGE_' + language.language_code.upper()
    # Get weather data

    people_to_meet_list_key = "people_to_meet_data_key_" + str(language_code_long)
    people_to_meet_list = cache.get(people_to_meet_list_key)
    if not people_to_meet_list:
        community_config_view = CommunityConfigurations.objects.filter(community=community, filter_parameter=language_code_long).first()
        community_admin_interests_ids = community_config_view.get_community_admin_interests()
        people_to_meet_list = []
        for people_to_meet_id in community_admin_interests_ids:
            people_to_meet = PeopleToMeet.objects.filter(pk=people_to_meet_id).first()
            if people_to_meet:
                lang_people_to_meet = LangPeopleToMeet.objects.filter(people_to_meet=people_to_meet, language=language).first()
                if lang_people_to_meet and lang_people_to_meet.name:
                    people_to_meet.name = lang_people_to_meet.name
                people_to_meet_list.append(people_to_meet)

        data['people_to_meet'] = people_to_meet_list
        cache.set(people_to_meet_list_key, people_to_meet_list, 1 * 60 * 60)
    else:
        data['people_to_meet'] = people_to_meet_list

    hot_link_people_to_meet = PeopleToMeet.objects.filter(is_fixed=True, community=community).first()
    if hot_link_people_to_meet:
        hot_link_lang_people_to_meet = LangPeopleToMeet.objects.filter(people_to_meet=hot_link_people_to_meet,
                                                              language=language).first()
        if hot_link_lang_people_to_meet and hot_link_lang_people_to_meet.name:
            hot_link_people_to_meet.name = hot_link_lang_people_to_meet.name

        data['hot_link'] = hot_link_people_to_meet
    else:
        data['hot_link'] = ""

    # community_config_view = CommunityConfigurations.objects.filter(community=community, filter_parameter=language_code_long).first()
    # community_program_interests_ids = community_config_view.get_community_program_interests()
    # community_admin_interests_ids = community_config_view.get_community_admin_interests()

    # live_people_to_meet = []
    # for people_to_meet_id in community_program_interests_ids:
    #     people_to_meet = PeopleToMeet.objects.filter(pk=people_to_meet_id).first()
    #     if people_to_meet:
    #         lang_people_to_meet = LangPeopleToMeet.objects.filter(people_to_meet=people_to_meet,
    #                                                               language=language).first()
    #         if lang_people_to_meet and lang_people_to_meet.name:
    #             people_to_meet.name = lang_people_to_meet.name
    #         live_people_to_meet.append(people_to_meet)

    # all_people_to_meet_ids = list(set(community_program_interests_ids + community_admin_interests_ids))
    # all_people_to_meet = []
    # for people_to_meet_id in all_people_to_meet_ids:
    #     people_to_meet = PeopleToMeet.objects.filter(pk=people_to_meet_id).first()
    #     if people_to_meet:
    #         lang_people_to_meet = LangPeopleToMeet.objects.filter(people_to_meet=people_to_meet, language=language).first()
    #         if lang_people_to_meet and lang_people_to_meet.name:
    #             people_to_meet.name = lang_people_to_meet.name
    #         all_people_to_meet.append(people_to_meet)

    # data['all_people_to_meet'] = all_people_to_meet
    data['people_to_meet'] = people_to_meet_list
    # data['live_people_to_meet'] = live_people_to_meet
    lang_list = Community.objects.filter(unique_code=community.unique_code).values_list("languages", flat=True)
    data['language_list'] = Language.objects.filter(id__in=lang_list)
    data['total_people_to_meet'] = 0
    data['theme'] = UITheme.objects.get(community_ui_theme=community)

    data['language_code'] = request.session['lang_code']
    data['english_text'] = language.english_text


    # fetch weather cache data
    user = None
    weather_data = fetch_weather_api_data(user)
    data['weather_data'] = weather_data

    return render_to_response(template_name,
                              data, context_instance=RequestContext(request))