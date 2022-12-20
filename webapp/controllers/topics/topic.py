from django.conf import settings
from django.shortcuts import render_to_response
from webapp.controllers.common.template_render import render_to_template
from django.template import RequestContext
from webapp.tasks.ad_tasks import update_ad_impressions
from webapp.controllers.errors.error_404 import handle404
from webapp.controllers.widgets import web_widgets
from webapp.controllers.utils.get_ads import get_top_ad, get_desktop_square_ads, get_ads_list, get_pagination_ads_list
from webapp.models import *
from webapp.controllers.helpers.pagination import *
from webapp.tasks.email_tasks import send_mail_to_tech


def topic_view(request, topic=None):
    # Todo: Change the logic to get community later
    page = 1
    ads_list = []
    top_ads = []
    community = request.community

    topic_obj = PeopleToMeet.objects.filter(url_path=topic, community=community).first()
    if not topic_obj:
        return handle404(request)

    topic_id = topic_obj.id

    if community.content_language_filter:
        language_code = request.session['lang_code']
        language = Language.objects.filter(language_code=request.session['lang_code']).first()

        posts = Post.objects.filter(community=community, is_hidden=False, people_to_meet=topic_id, language=language).exclude(is_story=True).order_by("-created")

    else:
        language_code = None

        posts = Post.objects.filter(community=community, is_hidden=False, people_to_meet=topic_id).exclude(is_story=True).order_by("-created")

    posts = paginate(posts, page)

    if community.enable_widgets:
        covid_data = web_widgets.get_covid_api_data()
        ADS_PER_PAGE = 2                # First position of the ad will be occupied by widget
    else:
        covid_data = { }
        ADS_PER_PAGE = 3

    if community.enable_ads:
        ads_list = get_ads_list(request, ADS_PER_PAGE, "topics_page_ads_id") # list of ads used between the news feed.

        if ads_list:
            try:
                ad_ids_list = []
                for ad in ads_list:
                    ad_ids_list.append(ad.id)
                update_ad_impressions.delay(ad_ids_list, request.session.session_key)
            except Exception as e:
                send_mail_to_tech.delay('Argus Ad impression count update failed ', str(e))


    live = LiveNews.objects.get(community=community, is_live=True)
    live_id = live.id

    comments = ProgramComment.objects.filter(program=live.id).order_by("-created")
    total_comments = comments.count()


    if community.enable_widgets:
        covid_data = web_widgets.get_covid_api_data()
    else:
        covid_data = {}

    return render_to_template('topics/topic.html',
                              {
                                  "community": community,
                                  "first_post": posts[0] if posts else None,
                                  'topic_obj': topic_obj,
                                  "posts": posts[1:] if len(posts) >= 1 else None,
                                  "live": live,
                                  "live_id": live_id,
                                  'comments': comments[:15],
                                  'total_comments': total_comments,
                                  'topic_id': topic_id,
                                  'language_code': language_code,
                                  'covid_data': covid_data,
                                  'ads_list': ads_list,
                              }, request)


def video_topic_view(request, topic=None):
    # Todo: Change the logic to get community later
    page = 1
    top_ads = []
    community = request.community

    topic_obj = PeopleToMeet.objects.filter(url_path=topic).first()

    live = LiveNews.objects.filter(community=community, is_hidden=False, people_to_meet=topic_obj.id).order_by("-created")
    live = paginate(live, page)

    current_live = LiveNews.objects.get(community=community, is_live=True)
    live_id = current_live.id

    comments = ProgramComment.objects.filter(program=current_live.id).order_by("-created")
    total_comments = comments.count()

    community_program_interests_ids = community.get_community_program_interests()
    # filter community program interests which are present in peoplestomeet
    video_topics = PeopleToMeet.objects.filter(id__in=community_program_interests_ids)

    return render_to_template('live_tv/live_tv.html',
                              {
                                  "community": community,
                                  "current_live": current_live,
                                  "live": live,
                                  "live_id": live_id,
                                  "topic": topic,
                                  "top_ads": top_ads,
                                  'comments': comments[:5],
                                  'total_comments': total_comments,
                                  'video_topics': video_topics,
                              }, request)


def pagination_topic_posts(request):
    community = request.community
    posts = None
    ADS_PER_PAGE = 3

    if 'page' in request.GET:
        page = int(str(request.GET["page"]))
        topic_id = int(str(request.GET["topic_id"]))
        language = Language.objects.filter(language_code=request.session['lang_code']).first()
        if community.content_language_filter:
            posts = Post.objects.filter(community=community, is_hidden=False, language=language,people_to_meet=topic_id).exclude(is_story=True).order_by("-created")
        else:
            posts = Post.objects.filter(community=community, is_hidden=False,people_to_meet=topic_id).exclude(is_story=True).order_by("-created")
        posts = paginate(posts, page)

        # If community.enable_ads is enabled (set to true) show the ads in web pages.
        # Get the shuffled list of ad ids from session.
        # If the list is empty render empty ads_list.
        ads_list = []
        if community.enable_ads:
            ads_list = get_pagination_ads_list(request, ADS_PER_PAGE, "topics_page_ads_id")
            if ads_list:
                try:
                    ad_ids_list = []
                    for ad in ads_list:
                        if ad:
                            ad_ids_list.append(ad.id)
                    update_ad_impressions.delay(ad_ids_list, request.session.session_key)
                except Exception as e:
                    send_mail_to_tech.delay('Argus Ad impression count update failed ', str(e))

    return render_to_template('pagination/home_posts.html', {
                                    "posts": posts,
                                     'ads_list': ads_list,
                                    'community': community
                                }, request)