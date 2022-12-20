from django.conf import settings
from webapp.controllers.common.template_render import render_to_template
from django.template import RequestContext
from webapp.controllers.utils.get_ads import get_top_ad, get_desktop_square_ads, get_ads_list
from webapp.tasks.ad_tasks import update_ad_impressions
from webapp.models import *
from webapp.controllers.helpers.pagination import *
from webapp.controllers.widgets import web_widgets
from webapp.tasks.email_tasks import send_mail_to_tech

def live_tv_view(request):
    page = 1
    top_ads = []
    ads_list = []
    ADS_PER_PAGE = 1

    community = request.community

    if community.enable_widgets:
        covid_data = web_widgets.get_covid_api_data()
    else:
        covid_data = { }

    if community.enable_ads:
        ads_list = get_ads_list(request, ADS_PER_PAGE, "latest_page_ads_id") # list of ads used between the news feed.
        if ads_list:
            try:
                ad_ids_list = []
                for ad in ads_list:
                    if ad:
                        ad_ids_list.append(ad.id)
                update_ad_impressions.delay(ad_ids_list, request.session.session_key)
            except Exception as e:
                send_mail_to_tech.delay('Argus Ad impression count update failed ', str(e))


    live = LiveNews.objects.filter(community=community, is_hidden=False).order_by('-is_top_video', 'top_video_order_no', '-published_date')
    live = paginate(live, page, 6)

    current_live = LiveNews.objects.get(community=community, is_live=True)

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
                                  "live_id": current_live.id,
                                  'comments': comments[:20],
                                  'total_comments': total_comments,
                                  'video_topics': video_topics,
                                  'ads_list': ads_list
                              }, request)


def pagination_live_tv(request, topic=None):

    community = request.community
    live = None

    if topic == "All":
        if 'page' in request.GET:
            page = int(str(request.GET["page"]))
            live = LiveNews.objects.filter(community=community, is_hidden=False).order_by('-is_top_video', 'top_video_order_no', '-published_date')
            live = paginate(live, page, 6)
    else:
        topic_obj = PeopleToMeet.objects.filter(url_path=topic).first()

        if 'page' in request.GET:
            page = int(str(request.GET["page"]))
            live = LiveNews.objects.filter(community=community, is_hidden=False, people_to_meet=topic_obj.id).order_by("-published_date")
            live = paginate(live, page, 6)

    return render_to_template('pagination/live_tv_video_list.html', {
                                    "live": live,
                                }, request)


def pagination_live_tv_comments(request):
    community = request.community
    comments = None

    if 'page' in request.GET:
        page = int(str(request.GET["page"]))

        live = request.GET['live_id']

        comments = ProgramComment.objects.filter(program=live, community=community).order_by("-created")
        comments = paginate(comments, page, 20)

    return render_to_template('pagination/home_comments.html', {
                                    "comments": comments,
                                }, request)


def command_shakti_view(request):
    page = 1
    top_ads = []

    community = request.community
    if community.enable_ads:
        top_ads = get_top_ad(request)
    command_shakti = PeopleToMeet.objects.get(unique_id='THEARGUSNEWS_Commando_Shakti')
    live = LiveNews.objects.filter(community=community, is_hidden=False, people_to_meet=command_shakti).order_by('-is_top_video', 'top_video_order_no',
                                                                                  '-published_date')
    live = paginate(live, page, 6)

    current_live = LiveNews.objects.get(community=community, is_live=True)

    comments = ProgramComment.objects.filter(program=current_live.id).order_by("-created")
    total_comments = comments.count()

    community_program_interests_ids = community.get_community_program_interests()
    # filter community program interests which are present in peoplestomeet
    video_topics = PeopleToMeet.objects.filter(id__in=community_program_interests_ids)

    if community.content_language_filter:
        language_code = request.session['lang_code']
        language = Language.objects.filter(language_code=request.session['lang_code']).first()

    else:
        language_code = None

    if language_code:
        trending_news_count = Post.objects.filter(community=community, is_hidden=False, language=language,
                                                  is_trending_news=True).exclude(is_story=True).count()
    else:
        trending_news_count = Post.objects.filter(community=community, is_hidden=False,
                                                  is_trending_news=True).exclude(is_story=True).count()

    return render_to_template('live_tv/command_shakti.html',
                              {
                                  "community": community,
                                  "current_live": current_live,
                                  "live": live,
                                  'top_ads': top_ads,
                                  "live_id": current_live.id,
                                  'comments': comments[:20],
                                  'total_comments': total_comments,
                                  'video_topics': video_topics,
                                  'trending_news_count': trending_news_count
                              }, request)



def pagination_commando_shakti(request):

    community = request.community
    live = None

    command_shakti = PeopleToMeet.objects.get(unique_id='THEARGUSNEWS_Commando_Shakti')

    if 'page' in request.GET:
        page = int(str(request.GET["page"]))
        live = LiveNews.objects.filter(community=community, is_hidden=False, people_to_meet=command_shakti).order_by(
            "-published_date")
        live = paginate(live, page, 6)

    return render_to_template('pagination/command_shakti_video_list.html', {
                                    "live": live,
                                }, request)