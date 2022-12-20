from django.conf import settings
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from webapp.controllers.common.template_render import render_to_template
from django.template import RequestContext
from datetime import datetime, timedelta

from webapp.controllers.errors.error_404 import handle404
from webapp.controllers.helpers.pagination import *
from webapp.controllers.utils.get_ads import get_top_ad, get_desktop_square_ads, get_ads_list, get_pagination_ads_list
from webapp.tasks.ad_tasks import update_ad_impressions
from webapp.models import *
from webapp.controllers.widgets import web_widgets
from webapp.tasks.email_tasks import send_mail_to_tech

def live_details_view(request, topic_video=None, unique_url=None):

    community = request.community
    top_ads = []
    ads_list = []
    video_post = LiveNews.objects.filter(unique_url=unique_url, community=community).first()

    today = datetime.today()
    one_week_ago = today - timedelta(days=7)

    if not video_post:
        return handle404(request)

    live_id = video_post.id
    scroll_posts = LiveNews.objects.filter(community=community , is_hidden=False, published_date__gte=one_week_ago).exclude(id=live_id).order_by("-published_date")[:5]

    # comments = ProgramComment.objects.filter(program=video_post).order_by("-created")
    # total_comments = comments.count()

    if community.content_language_filter:
        language_code = request.session['lang_code']
        language = Language.objects.filter(language_code=request.session['lang_code']).first()

    else:
        language_code = None

    if language_code:

        post_obj = list(Post.objects.filter(community=community, is_hidden=False, language=language, is_story=False, published_date__gte=one_week_ago).order_by("-published_date")[:35])

        recommended_posts = post_obj[10:17]

        top_stories = post_obj[20:34]

    else:
        post_obj = list(Post.objects.filter(community=community, is_hidden=False, is_story=False, published_date__gte=one_week_ago).order_by("-published_date")[:35])

        recommended_posts = post_obj[10:17]

        top_stories = post_obj[20:34]

    if community.enable_widgets:
        covid_data = web_widgets.get_covid_api_data()
        ADS_PER_PAGE = 2                # First position of the ad will be occupied by widget
    else:
        covid_data = { }
        ADS_PER_PAGE = 3

    arr_of_post_tuples = []
    if community.enable_ads:
        ads_list = get_ads_list(request, ADS_PER_PAGE, "video_details_page_ads_id") # list of ads used between the news feed.
        if ads_list:
            try:
                ad_ids_list = []
                for ad in ads_list:
                    if ad:
                        ad_ids_list.append(ad.id)
                update_ad_impressions.delay(ad_ids_list, request.session.session_key)
            except Exception as e:
                send_mail_to_tech.delay('Argus Ad impression count update failed ', str(e))


    try:
        first_post = recommended_posts[0]
        for i in range(0, 7):
            arr = top_stories[i * 2:][:2]
            arr_of_post_tuples.append((arr[0], arr[-1]))
    except:
        post_obj = list(Post.objects.filter(community=community, is_hidden=False, is_story=False).order_by("-published_date")[:35])
        first_post = post_obj[10]
        top_stories = post_obj[20:34]
        for i in range(0, 7):
            arr = top_stories[i * 2:][:2]
            arr_of_post_tuples.append((arr[0], arr[-1]))

    return render_to_template('live_details/live_details.html',
                              {'video_post': video_post,
                               "live_id": live_id,
                               'scroll_posts': scroll_posts,
                               'recommended_posts': recommended_posts,
                               'first_post': first_post,
                               'arr_of_post_tuples': arr_of_post_tuples,
                               "community": community,
                               'language_code': language_code,
                                'ads_list': ads_list,
                               }, request)



def pagination_live_details_comments(request):
    comments = None

    if 'page' in request.GET:
        page = int(str(request.GET["page"]))

        live = request.GET['live_id']

        comments = ProgramComment.objects.filter(program=live).order_by("-created")
        comments = paginate(comments, page, 5)

    return render_to_template('pagination/detail_comments.html', {
        "comments": comments,
    }, request)


def pagination_details_videos(request):
    community = request.community
    scroll_posts = None
    ADS_PER_PAGE = 3

    if 'page' in request.GET:
        video = request.GET['video_id']
        page = int(str(request.GET["page"]))
        scroll_posts = LiveNews.objects.filter(id__lt=video, community=community, is_hidden=False).order_by("-published_date")
        scroll_posts = paginate(scroll_posts, page, 5)

        # If community.enable_ads is enabled (set to true) show the ads in web pages.
        # Get the shuffled list of ad ids from session.
        # If the list is empty render empty ads_list.
        ads_list = []
        if community.enable_ads:
            ads_list = get_pagination_ads_list(request, ADS_PER_PAGE, "video_details_page_ads_id")
            if ads_list:
                try:
                    ad_ids_list = []
                    for ad in ads_list:
                        if ad:
                            ad_ids_list.append(ad.id)
                    update_ad_impressions.delay(ad_ids_list, request.session.session_key)
                except Exception as e:
                    send_mail_to_tech.delay('Argus Ad impression count update failed ', str(e))

    return render_to_template('pagination/details_live.html', {
                                    "scroll_posts": scroll_posts,
                                    'ads_list': ads_list,
                                    'community': community
                                }, request)

