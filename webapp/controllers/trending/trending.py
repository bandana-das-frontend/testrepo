from webapp.controllers.common.template_render import render_to_template
from webapp.controllers.utils.get_ads import  get_ads_list
from webapp.tasks.ad_tasks import update_ad_impressions
from webapp.models import *
from webapp.controllers.helpers.pagination import *
from datetime import  timedelta
from webapp.controllers.widgets import web_widgets
from webapp.tasks.email_tasks import send_mail_to_tech


def trending_view(request, language=None):
    # Todo: Change the logic to get community later
    page = 1
    ads_list = []
    community = request.community
    if request.session['lang_code'] != language and language is not None:
        request.session['lang_code'] = language

    if community.enable_widgets:
        covid_data = web_widgets.get_covid_api_data()
        ADS_PER_PAGE = 2                # First pos_imition of the ad will be occupied by widget
    else:
        covid_data = { }
        ADS_PER_PAGE = 3

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


    # getting date time of 2 days before's i.e, 48 hours back
    last_2_days = datetime.now() - timedelta(hours=48)

    if community.content_language_filter:
        language_code = request.session['lang_code']
        language = Language.objects.filter(language_code=request.session['lang_code']).first()

        trending_news = Post.objects.filter(community=community, is_hidden=False, language=language, is_breaking_news=False,
                                             views__gte=1, published_date__gte=last_2_days).exclude(is_story=True)\
            .exclude(people_to_meet__unique_id__icontains="Citizen_News").order_by('-views','-published_date')

    else:
        language_code = None

        trending_news = Post.objects.filter(community=community, is_hidden=False, is_breaking_news=False,
                                            views__gte=1, published_date__gte=last_2_days).exclude(is_story=True)\
            .exclude(people_to_meet__unique_id__icontains="Citizen_News").order_by('-views','-published_date')


    posts = paginate(trending_news, page, 30)

    trending_news_count = len(posts)

    live = LiveNews.objects.get(community=community, is_live=True)
    live_id = live.id
    comments = ProgramComment.objects.filter(program=live.id).order_by("-created")
    total_comments = comments.count()

    return render_to_template('trending/trending.html',
                              {
                                  "community": community,
                                  "first_post": posts[0] if posts else None,
                                  "posts": posts[1:] if trending_news_count >= 1 else None,
                                  "live": live,
                                  "live_id": live_id,
                                  'language_code': language_code,
                                  'comments': comments[:15],
                                  'total_comments': total_comments,
                                  'trending_news_count': trending_news_count,
                                  'ads_list': ads_list,
                              }, request)


