from django.core.cache import cache
from webapp.controllers.common.template_render import render_to_template
import datetime
import random
from webapp.controllers.helpers.pagination import *
from webapp.controllers.errors.error_404 import *
from webapp.controllers.utils.get_language import get_language
from webapp.controllers.utils.get_ads import get_ads_list,get_pagination_ads_list, get_top_ad, get_desktop_square_ads
from webapp.models import *
from webapp.tasks.ad_tasks import update_ad_impressions
import urllib
from webapp.controllers.widgets import web_widgets
from django.core.mail import send_mail
from webapp.controllers.dispatchers.responses.send_pass_http_response import send_pass_http_response

from webapp.tasks.article_tasks import update_article_views
from webapp.tasks.email_tasks import send_mail_to_tech


def post_details_view(request, topic_article=None, unique_url=None):

    # Todo: Change the logic to get community later
    community = request.community
    POSTS_PAGINATION_SIZE = 6

    post = Post.objects.filter(unique_url=unique_url).first()
    if not post:
        post = Post.objects.filter(unique_url=urllib.quote(unique_url.encode('utf8'))).first()
        if not post:
            return handle404(request)

    if post.is_hidden:
        return handle404(request)

    if post.is_story:
        return handle404(request)

    post_id = post.id
    update_article_views.delay(post.id)

    # below logic is to handle old posts which have multiple location,so that to render only one location
    try:
        location = post.locations.strip()
        if location:
            if len(location.split(',')) > 0:
                location = location.split(',')[0]
                post.locations = location
    except:
        pass

    # Check if cached template is available
    if request.user_agent.is_mobile:
        cache_data = cache.get("MOBILE_" + str(post_id))
        if cache_data:
            return cache_data
    else:
        cache_data = cache.get("DESKTOP_" + str(post_id))
        if cache_data:
            return cache_data

    if request.user_agent.is_mobile:
        specific_ad = Advertisement.objects.filter(community=community, posts=post_id, ad_platform=AD_PLATFORMS.Mobile_web,
                                                   ad_type=AD_TYPES.Square, is_hidden=False, reached_daily_limit=False).order_by('-created').first()
        article_ad_status = community.enable_ads_post_mobile_web
    else:
        specific_ad = Advertisement.objects.filter(community=community, posts=post_id, ad_platform=AD_PLATFORMS.Desktop,
                                                   ad_type=AD_TYPES.Horizontal, is_hidden=False, reached_daily_limit=False).order_by('-created').first()
        article_ad_status = community.enable_ads_post_desktop_web

    if specific_ad and community.enable_widgets:
        ADS_PER_PAGE = 2
    elif specific_ad or community.enable_widgets:
        if specific_ad:
            ADS_PER_PAGE = 3
        else:
            if article_ad_status:
                ADS_PER_PAGE = 3
            else:
                ADS_PER_PAGE = 2
    else:
        if article_ad_status:
            ADS_PER_PAGE = 4
        else:
            ADS_PER_PAGE = 3

    # google_desktop_top_ad = GoogleAdsConfig.objects.filter(community=community, ad_platform=GOOGLE_AD_PLATFORMS.DESKTOP,
    #                                                        ad_type=GOOGLE_AD_TYPES.TOP).first()
    # google_mobile_top_ad = GoogleAdsConfig.objects.filter(community=community, ad_platform=GOOGLE_AD_PLATFORMS.MOBILE,
    #                                                       ad_type=GOOGLE_AD_TYPES.TOP).first()
    # google_desktop_horizontal_ad = GoogleAdsConfig.objects.filter(community=community, ad_platform=GOOGLE_AD_PLATFORMS.DESKTOP,
    #                                                               ad_type=GOOGLE_AD_TYPES.HORIZONTAL).first()
    # google_square_ad = GoogleAdsConfig.objects.filter(community=community, ad_platform=GOOGLE_AD_PLATFORMS.BOTH, ad_type=GOOGLE_AD_TYPES.SQUARE).first()

    # If community.enable_ads is enabled(set to true) show the ads in details page.
    # Get the list of ad ids from Advertisement model and shuffle and store the shuffled list in session.
    # if the list is empty render empty ads_list
    ads_list = []
    # top_ads = []
    # desktop_square_ads = []
    if community.enable_ads:
        ads_list = get_ads_list(request, ADS_PER_PAGE, "details_page_ad_ids")

        if specific_ad and community.enable_widgets:                # if specific ads ad and widget are present send only 2 ads out of 4
            ads_list.insert(0, specific_ad)                         # to send  2 ads out of 4, insert ads_arr 0th position with specific ad and 2nd with none
            ads_list.insert(1, None)
        elif specific_ad or community.enable_widgets:               # If either one is present check which field is present and fill the ads arr accordingly
            if specific_ad:
                ads_list.insert(0, specific_ad)                     # Article_ad_status is a field for controlling post detail ad( ad after first para)
            elif community.enable_widgets:
                if article_ad_status:
                    ads_list.insert(1, None)
                else:
                    ads_list.insert(0, None)
                    ads_list.insert(1, None)
        elif not article_ad_status:
            ads_list.insert(0, None)

        if ads_list:
            try:
                ad_ids_list = []
                for ad in ads_list:
                    if ad:
                        ad_ids_list.append(ad.id)
                update_ad_impressions.delay(ad_ids_list, request.session.session_key)
            except Exception as e:
                send_mail_to_tech.delay('Argus Ad impression count update failed ', str(e))


    if community.content_language_filter:
        language = get_language(request)
        language_code = language.language_code

        if 'lang_code' in request.session:
            if request.session['lang_code'] != post.language.language_code:
                request.session['lang_code'] = post.language.language_code
                language_code = request.session['lang_code']
                language = Language.objects.filter(language_code=language_code).first()

        scroll_posts = Post.objects.filter(community=community, is_hidden=False, language=language, is_story=False).exclude(id=post.id).order_by("-published_date")[:3]

    else:
        language_code = None
        scroll_posts = Post.objects.filter(community=community, is_hidden=False, is_story=False).exclude(id=post.id).order_by("-published_date")[:3]

    scroll_posts = list(scroll_posts)

    if community.enable_widgets:
        covid_data = web_widgets.get_covid_api_data()
    else:
        covid_data = { }

    if request.user_agent.is_mobile:
        mobile_view = render_to_template('post/post_details.html',
                                  {'post': post,
                                   'scroll_posts': scroll_posts,
                                   "post_id": post_id,
                                   "community": community,
                                   "ads_list": ads_list,
                                   # 'top_ads': top_ads,
                                   'covid_data':covid_data,
                                   # 'google_mobile_top_ad': google_mobile_top_ad,
                                   # 'google_square_ad': google_square_ad,
                                   'article_ad_status':article_ad_status,
                                   'language_code':language_code,
                                   }, request)
        # Cache for 10 minutes
        cache.set("MOBILE_" + str(post.id), mobile_view, 1 * 60 * 60)
        return mobile_view

    else:
        if language_code:
            recommended_posts = Post.objects.filter(community=community, is_hidden=False,
                                                    is_story=False, language=language).exclude(id=post.id).order_by("-published_date")[10:17]
        else:
            recommended_posts = Post.objects.filter(community=community, is_hidden=False, is_story=False).exclude(id=post.id).order_by("-published_date")[10:17]

        recommended_posts = list(recommended_posts)
        latest_videos = LiveNews.objects.filter(community=community, is_hidden=False, is_live=False).order_by("-published_date")[:4]

        desktop_view = render_to_template('post/post_details.html',
                                  {'post': post,
                                   'scroll_posts': scroll_posts,
                                   'recommended_posts': recommended_posts,
                                   "post_id": post_id,
                                   "ads_list": ads_list,
                                   # "top_ads": top_ads,
                                   'covid_data': covid_data,
                                   "community": community,
                                   "latest_video_1": latest_videos[0],
                                   "latest_video_2": latest_videos[1],
                                   "latest_video_3": latest_videos[2],
                                   "latest_video_4": latest_videos[3],
                                   # 'desktop_square_ads': desktop_square_ads,
                                   # 'google_desktop_top_ad': google_desktop_top_ad,
                                   # 'google_desktop_horizontal_ad': google_desktop_horizontal_ad,
                                   # 'google_square_ad': google_square_ad,
                                   'article_ad_status':article_ad_status,
                                   'language_code': language_code,
                                   }, request)

        # Cache for 10 minutes
        cache.set("DESKTOP_" + str(post.id), desktop_view, 1 * 60 * 60)
        return desktop_view


def pagination_comments(request):
    comments = None

    if 'page' in request.GET:
        page = int(str(request.GET["page"]))

        post = request.GET['post_id']

        comments = PostComment.objects.filter(post=post).order_by("-created")
        comments = paginate(comments, page, 5)

    return render_to_template('pagination/detail_comments.html', {
                                    "comments": comments,
                                }, request)


def pagination_details_posts(request):
    community = request.community
    scroll_posts = None

    if 'page' in request.GET:
        post = request.GET['post_id']
        page = int(str(request.GET["page"]))
        ADS_PER_PAGE = 2
        POSTS_PAGINATION_SIZE = 6

        ''' If community.enable_ads is enabled (set to true) show the ads in web pages.
            Get the shuffled list of ad ids from session.
            If the list is empty render empty ads_list.
        '''
        ads_list = []
        if community.enable_ads:
            ads_list = get_pagination_ads_list(request, ADS_PER_PAGE, "details_page_ad_ids")

        if ads_list:
            try:
                ad_ids_list = []
                for ad in ads_list:
                    if ad:
                        ad_ids_list.append(ad.id)
                update_ad_impressions.delay(ad_ids_list, request.session.session_key)
            except Exception as e:
                send_mail_to_tech.delay('Argus Ad impression count update failed ', str(e))

        if community.content_language_filter:
            language = Language.objects.filter(language_code=request.session['lang_code']).first()

            scroll_posts = Post.objects.filter(community=community, id__lt=post, is_hidden=False, language=language).exclude(is_story=True).order_by("-published_date")

        else:
            scroll_posts = Post.objects.filter(community=community, id__lt=post, is_hidden=False).exclude(is_story=True).order_by("-published_date")

        scroll_posts = paginate(scroll_posts, page, POSTS_PAGINATION_SIZE)

    return render_to_template('pagination/details_posts.html', {
                                    "scroll_posts": scroll_posts,
                                    "ads_list": ads_list,
                                    "community": community,
                                }, request)


def country_get(country_data):
    if country_data["Country_text"] == "India":
        return True
    else:
        return False
