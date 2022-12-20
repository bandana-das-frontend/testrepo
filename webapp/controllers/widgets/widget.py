#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Sangamesh Deshetti

from django.shortcuts import render_to_response
from django.template import RequestContext
from webapp.models import *
from weather import fetch_weather_api_data
from covid import fetch_covid_api_data
import json


def widget(request):
    # read user ID from request
    user_id = request.GET.get("user_id", None)

    user = None
    # If user id is present, fetch the user
    if user_id:
        user = MyUser.objects.filter(id=user_id).first()

    # fetch community or use Argus if not available
    if user:
        # Use first to handle case where user may be part of multiple communities
        community = user.community.first()
    else:
        community = Community.objects.filter(unique_code="THEARGUS").first()

    # Fetch Covid data from API
    covid_data = fetch_covid_api_data()

    # Fetch Weather data from API
    weather_data = fetch_weather_api_data(user)

    widgets_list = Widget.objects.filter(community=community, is_hidden=False)
    num_widgets = widgets_list.count()

    # Fetch Covid widget data from DB
    covid_widget = Widget.objects.filter(community=community, type="COVID").first()

    # Fetch Weather widget data from DB
    weather_widget = Widget.objects.filter(community=community, type="WEATHER").first()

    # Fetch Custom widget data from DB
    custom_widget = Widget.objects.filter(community=community, type="CUSTOM").first()

    # Fetch covid config json data from Covid Widget Model
    covid_parsed_json = fetch_widget_config(covid_widget) if hasattr(covid_widget, 'config') else None

    # Fetch weather config json data from Weather Widget Model
    weather_parsed_json = fetch_widget_config(weather_widget) if hasattr(weather_widget, 'config') else None

    # Fetch custom config json data from Custom Widget Model
    custom_parsed_json = fetch_widget_config(custom_widget) if hasattr(weather_widget, 'config') else None

    return render_to_response(
        'widgets/widget.html',
        {
            'widgets_list': widgets_list,
            'num_widgets': num_widgets,
            'covid_data': covid_data,
            'weather_data': weather_data,
            "weather_widget": weather_widget,
            "weather_config": weather_parsed_json,
            "covid_widget": covid_widget,
            "covid_config": covid_parsed_json,
            "custom_widget": custom_widget,
            "custom_widget_config": custom_parsed_json
        },
        context_instance=RequestContext(request)
    )


def fetch_widget_config(widget_obj):
    # Note: config field of Widget model is of string type, but actually stores a json/dictionary
    widget_config = widget_obj.config if hasattr(widget_obj, 'config') else ""
    widget_parsed_json = {}

    # Not empty check
    if widget_config:
        try:
            # Try to parse config string as JSON
            widget_parsed_json = json.loads(widget_config)
        except:
            widget_parsed_json = {}

    return widget_parsed_json
