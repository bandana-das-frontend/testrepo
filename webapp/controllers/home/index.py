from django.conf import settings
from django.shortcuts import render_to_response
from webapp.controllers.common.template_render import render_to_template
from django.template import RequestContext
import random
from webapp.controllers.utils.get_language import get_language
from webapp.tasks.ad_tasks import update_ad_impressions
from webapp.models import *
from webapp.controllers.helpers.pagination import *
from datetime import datetime, timedelta
from django.db.models import Count, Max
from webapp.controllers.utils.get_ads import get_ads_list, get_pagination_ads_list, get_top_ad, get_desktop_square_ads
from webapp.controllers.widgets import web_widgets
from webapp.tasks.email_tasks import send_mail_to_tech

# Added by tpn
from i18n.translator import Translator


def home_view(request, language=None):
    page = 1
    POSTS_PAGINATION_SIZE = 12
    # ToDo: Make TOPICS_LIST a configurable field
    TOPICS_LIST = ['THEARGUS_Sports', 'THEARGUS_Entertainment'] # List of unique IDs

    topic_posts_first_row = None
    topic_posts_second_row = None

    citizen_news = PeopleToMeet.objects.get(unique_id='THEARGUS_Citizen_News')
    citizen_news_posts = list(Post.objects.filter(people_to_meet=citizen_news).values_list('id', flat=True))

    community = request.community
    if request.session['lang_code'] != language and language is not None:
        request.session['lang_code'] = language

    if community.content_language_filter:
        language = get_language(request)
        language_code = language.language_code
        native_text = language.native_text
        # checking for breaking news that is not older than 24 hrs for language switch
        breaking_news = Post.objects.filter(community=community, is_breaking_news=True, language=language,\
                                            is_hidden=False, published_date__gte=datetime.now()-timedelta(hours=24)).first()

        posts = Post.objects.filter(community=community, is_hidden=False, is_story=False, language=language, is_breaking_news=False)\
            .order_by('-is_top_post', 'top_post_order_no', '-published_date')

        live_update = LiveUpdate.objects.filter(is_enable=True, community=community, language=language,is_hidden=False).first()

    else:
        language_code = None
        english_text = None

        # checking for breaking news that is not older than 24 hrs
        breaking_news = Post.objects.filter(community=community, is_breaking_news=True,\
                                            is_hidden=False, published_date__gte=datetime.now()-timedelta(hours=24)).first()

        posts = Post.objects.filter(community=community, is_hidden=False, is_story=False, is_breaking_news=False)\
            .order_by('-is_top_post', 'top_post_order_no', '-published_date')

        live_update = LiveUpdate.objects.filter(is_enable=True, community=community,is_hidden=False).first()

    if community.enable_widgets:
        covid_data = web_widgets.get_covid_api_data()
        ADS_PER_PAGE = 2                # First position of the ad will be occupied by widget
    else:
        covid_data = { }
        ADS_PER_PAGE = 3


    # If community enable ads field is enabled, get the corresponding types of ads for specific platform
    ads_list = []
    # top_ads = []
    # desktop_square_ads = []
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
                send_mail_to_tech('Argus Ad impression count update failed ', str(e))

        # top_ads = get_top_ad(request)                                         # Top ad
        # if top_ads:
        #     update_ad_impressions(top_ads, request)
        # desktop_square_ads = get_desktop_square_ads(request)                   # Desktop ad in the right section
        # if desktop_square_ads:
        #     update_ad_impressions(desktop_square_ads, request)   #Update_ad_impressions function accepts list of ad ids
        if community.enable_widgets:
            ads_list.insert(0, None)                    # First position of the ad will be occupied by widget if enable_widgets is true

    # google_desktop_top_ad = GoogleAdsConfig.objects.filter(community=community, ad_platform=GOOGLE_AD_PLATFORMS.DESKTOP, ad_type=GOOGLE_AD_TYPES.TOP).first()
    # google_mobile_top_ad = GoogleAdsConfig.objects.filter(community=community, ad_platform=GOOGLE_AD_PLATFORMS.MOBILE, ad_type=GOOGLE_AD_TYPES.TOP).first()
    # google_desktop_horizontal_ad = GoogleAdsConfig.objects.filter(community=community, ad_platform=GOOGLE_AD_PLATFORMS.DESKTOP, ad_type=GOOGLE_AD_TYPES.HORIZONTAL).first()
    # google_square_ad = GoogleAdsConfig.objects.filter(community=community, ad_platform=GOOGLE_AD_PLATFORMS.BOTH, ad_type=GOOGLE_AD_TYPES.SQUARE).first()

    # removing citizen news posts from the vertical feed posts
    posts = posts.exclude(id__in=citizen_news_posts)

    post_ids = posts.values_list('id', flat=True)[:500]
    request.session['feed_post_ids'] = list(post_ids)
    post_ids = list(post_ids[:POSTS_PAGINATION_SIZE]) #paginate(posts, page, POSTS_PAGINATION_SIZE)

    feed_posts = []
    for post_id in post_ids:
        feed_posts.append(Post.objects.get(pk=post_id))

    if request.user_agent.is_mobile:
        if live_update:
            feed_posts.insert(0, live_update)
    else:
        if live_update and breaking_news == None:
            feed_posts.insert(0, live_update)
        elif live_update and breaking_news:
            feed_posts.insert(0, breaking_news)
            feed_posts.insert(1, live_update)
        elif breaking_news and live_update == None:
            feed_posts.insert(0, breaking_news)


    live = LiveNews.objects.get(community=community, is_live=True)
    live_id = live.id
    if not request.user_agent.is_mobile:
        comments = ProgramComment.objects.filter(program=live.id).order_by("-created")
        total_comments = comments.count()
        comments = paginate(comments, page, 15)
    else:
        comments = []
        total_comments = 0

    # if language_code:
    #     trending_news_count = Post.objects.filter(community=community, is_hidden=False, language=language,
    #                                         is_trending_news=True).exclude(is_story=True).count()
    #
    # else:
    #     trending_news_count = Post.objects.filter(community=community, is_hidden=False,
    #                                               is_trending_news=True).exclude(is_story=True).count()


    # Horizontal section Topics Row 1 logic:
    topic_first_row_obj = PeopleToMeet.objects.filter(unique_id=TOPICS_LIST[0]).first()
    if topic_first_row_obj:
        lang_people_to_meet = LangPeopleToMeet.objects.filter(people_to_meet=topic_first_row_obj, language=language).first()
        if lang_people_to_meet and lang_people_to_meet.name:
            topic_first_row_obj.name = lang_people_to_meet.name

        topic_posts_first_row = Post.objects.filter(community=community, language=language, is_hidden=False, \
                                                        people_to_meet=topic_first_row_obj) \
                                                        .exclude(is_story=True).exclude(is_breaking_news=True).order_by("-published_date")[:5]
    # Horizontal section Topics Row 2 logic:
    topic_second_row_obj = PeopleToMeet.objects.filter(unique_id=TOPICS_LIST[1]).first()
    if topic_second_row_obj:
        lang_people_to_meet = LangPeopleToMeet.objects.filter(people_to_meet=topic_second_row_obj, language=language).first()
        if lang_people_to_meet and lang_people_to_meet.name:
            topic_second_row_obj.name = lang_people_to_meet.name

        topic_posts_second_row = Post.objects.filter(community=community, language=language, is_hidden=False, \
                                                        people_to_meet=topic_second_row_obj) \
                                                        .exclude(is_story=True).exclude(is_breaking_news=True).order_by("-published_date")[:5]

    if breaking_news is not None:
        breaking_news_post = breaking_news
    else:
        breaking_news_post = None

    '''
        Posts are truncated because of hero tiles posts:
        1st, 2nd and 3rd (and 4th if breking news post does not exist)
    '''

    if request.user_agent.is_mobile:
        # First post is already handled for mobile site, so skip that, hence [1:]
        first_page_start_index = 1
    else:
        first_page_start_index = 3
    first_page_stop_index = POSTS_PAGINATION_SIZE
    first_page_start_index, first_page_stop_index = str(first_page_start_index), str(first_page_stop_index)

    today = datetime.today()
    one_week_ago = today - timedelta(days=7)

    # horizontal videos
    horizontal_videos = LiveNews.objects.filter(community=community, is_hidden=False, is_live=False, published_date__gte=one_week_ago).order_by("-published_date")[:5]

    return render_to_template('index.html',
                              {
                                  "community": community,
                                  "posts": feed_posts,
                                  "breaking_news_post": breaking_news_post,
                                  "first_page_start_index": first_page_start_index,
                                  "first_page_stop_index": first_page_stop_index,
                                  "live": live,
                                  "live_id": live_id,
                                  "language_code": language_code,
                                  "language": native_text,
                                  'comments': comments,
                                  'total_comments': total_comments,
                                  'topic_posts_first_row': topic_posts_first_row,
                                  'topic_posts_second_row': topic_posts_second_row,
                                  'topic_first_row_obj': topic_first_row_obj,
                                  'topic_second_row_obj': topic_second_row_obj,
                                  'ads_list': ads_list,
                                  # 'top_ads': top_ads,
                                  # 'desktop_square_ads':desktop_square_ads,
                                  # 'google_desktop_top_ad':google_desktop_top_ad,
                                  # 'google_mobile_top_ad': google_mobile_top_ad,
                                  # 'google_desktop_horizontal_ad': google_desktop_horizontal_ad,
                                  # 'google_square_ad': google_square_ad,
                                  'covid_data': covid_data,
                                  'horizontal_videos': horizontal_videos,
                                  'live_update': live_update
                              }, request)


def pagination_home_posts(request):
    community = request.community
    posts = None
    topic_first_row_obj = None
    topic_posts_first_row = None
    topic_second_row_obj = None
    # topic_posts_second_row = None
    ADS_PER_PAGE = 3
    POSTS_PAGINATION_SIZE = 12

    # ToDo: Make TOPICS_LIST a configurable field
    TOPICS_LIST = []

    citizen_news = PeopleToMeet.objects.get(unique_id='THEARGUS_Citizen_News')

    feed_post_ids = []
    if 'feed_post_ids' in request.session:
        feed_post_ids = request.session['feed_post_ids']


    if 'page' in request.GET:
        page = int(str(request.GET["page"]))

        language = Language.objects.filter(language_code=request.session['lang_code']).first()
        if community.content_language_filter:
            posts = Post.objects.filter(community=community,
                                        is_hidden=False,
                                        is_story=False, language=language, is_breaking_news=False)\
                .exclude(people_to_meet=citizen_news).order_by('-is_top_post', 'top_post_order_no', '-published_date')
        else:
            posts = Post.objects.filter(community=community,
                                        is_hidden=False,
                                        is_story=False, is_breaking_news=False)\
                .exclude(people_to_meet=citizen_news).order_by('-is_top_post', 'top_post_order_no', '-published_date')
        # If community.enable_ads is enabled (set to true) show the ads in web pages.
        # Get the shuffled list of ad ids from session.
        # If the list is empty render empty ads_list.
        ads_list = []
        if community.enable_ads:
            ads_list = get_pagination_ads_list(request, ADS_PER_PAGE, "latest_page_ads_id")
            if ads_list:
                try:
                    ad_ids_list = []
                    for ad in ads_list:
                        if ad:
                            ad_ids_list.append(ad.id)
                    update_ad_impressions.delay(ad_ids_list, request.session.session_key)
                except Exception as e:
                    send_mail_to_tech('Argus Ad impression count update failed ', str(e))

        if page == 2:
            ''' 
            Video Topic selection logic:
            Select the topic from last 7 to 30 days for which most number of videos were uploaded 
            '''
            today = datetime.today()
            one_week_ago = today - timedelta(days=7)
            one_month_ago = today - timedelta(days=30)

            video_topic_id = LiveNews.objects.filter(published_date__gte=one_month_ago, created__lte=one_week_ago) \
                                                        .annotate(ppl_to_meet=Count('pk')) \
                                                        .aggregate(max=Max('people_to_meet'))

            video_topic = PeopleToMeet.objects.filter(id = str(video_topic_id.get("max", None))) \
                                                        .first().unique_id if video_topic_id else None

            TOPICS_LIST = ['THEARGUS_Money', video_topic] # List of unique IDs

            # Horizontal section Topics Row 1 logic:
            topic_first_row_obj = PeopleToMeet.objects.filter(unique_id=TOPICS_LIST[0]).first()
            if topic_first_row_obj:
                lang_people_to_meet = LangPeopleToMeet.objects.filter(people_to_meet=topic_first_row_obj, language=language).first()
                if lang_people_to_meet and lang_people_to_meet.name:
                    topic_first_row_obj.name = lang_people_to_meet.name

                topic_posts_first_row = Post.objects.filter(community=community, language=language, is_hidden=False, \
                                                                people_to_meet=topic_first_row_obj) \
                                                                .exclude(is_story=True).exclude(is_breaking_news=True).order_by("-published_date")[:5]

        # removing breaking news posts from the vertical feed posts
        if len(feed_post_ids) > 0:
            posts = posts.filter(id__in=feed_post_ids)
        posts = paginate(posts, page, POSTS_PAGINATION_SIZE)

    return render_to_template('pagination/home_posts.html', {
                                    "community": community,
                                    "posts": posts,
                                    'topic_posts_first_row': topic_posts_first_row,
                                    'topic_first_row_obj': topic_first_row_obj,
                                    'topic_second_row_obj': topic_second_row_obj,
                                    'page_num': page,
                                    'ads_list': ads_list,
                                }, request)


def pagination_comments(request):
    community = request.community
    comments = None

    if 'page' in request.GET:
        page = int(str(request.GET["page"]))

        live = request.GET['live_id']

        comments = ProgramComment.objects.filter(program=live, community=community).order_by("-created")
        comments = paginate(comments, page, 15)

    return render_to_template('pagination/home_comments.html', {
                                    "comments": comments,
                                }, request)
