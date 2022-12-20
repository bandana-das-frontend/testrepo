from django.conf import settings
from django.template import RequestContext
from webapp.controllers.common.template_render import render_to_template
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.http import HttpResponseRedirect

from webapp.models import *

@csrf_exempt
def profile_view(request, username):

    community = request.community
    if username != request.user.username:
        return HttpResponseRedirect('/')

    user = request.user

    user_people_to_meet = MyUserPeopleToMeet.objects.filter(myuser=user.id, peopletomeet__community=None).order_by('-rank').values_list("peopletomeet", flat=True)
    user_interests = []

    for topic_id in user_people_to_meet:
        people_to_meet = PeopleToMeet.objects.filter(pk=topic_id).first()
        user_interests.append(people_to_meet)

    user_activities = UserActivity.objects.filter(user=request.user, activity_type__in=[ActivityType.COMMENT_POST, ActivityType.LIKE_POST]).order_by('-created')
    saved_stories_count = UserActivity.objects.filter(user=request.user, activity_type__in=[ActivityType.SAVE_POST]).count()

    if community.content_language_filter:
        language_code = request.session['lang_code']
        language = Language.objects.filter(language_code=request.session['lang_code']).first()

    else:
        language_code = None

    return render_to_template('profile/profile.html',
                              {'user': user,
                               'community': community,
                               'user_interests': user_interests,
                               'user_activities': user_activities,
                               'user_activities_count': user_activities.count(),
                               'saved_stories_count': saved_stories_count,
                               'language_code': language_code,
                               }, request)


def activities(request):
    community = request.community
    user_activities = UserActivity.objects.filter(user=request.user, activity_type__in=[ActivityType.COMMENT_POST, ActivityType.LIKE_POST]).order_by('-created')

    if community.content_language_filter:
        language_code = request.session['lang_code']
        language = Language.objects.filter(language_code=request.session['lang_code']).first()
        english_text = language.english_text

    else:
        language_code = None
        english_text = None

    return render_to_template('profile/activities.html',
                              {'user': request.user,
                               'community': community,
                               'user_activities': user_activities,
                               'language_code': language_code,
                               'language': english_text,
                               }, request)


def saved_stories(request):
    community = request.community
    user_activities = UserActivity.objects.filter(user=request.user, activity_type__in=[ActivityType.SAVE_POST]).order_by('-created')

    if community.content_language_filter:
        language_code = request.session['lang_code']
        language = Language.objects.filter(language_code=request.session['lang_code']).first()
        english_text = language.english_text

    else:
        language_code = None
        english_text = None

    return render_to_template('profile/saved_stories.html',
                              {'user': request.user,
                               'community': community,
                               'user_activities': user_activities,
                               'language_code': language_code,
                               'language': english_text,
                               }, request)

