from webapp.models import *
import random
from django.views.decorators.csrf import csrf_exempt
from webapp.controllers.common.template_render import render_to_template
from webapp.controllers.utils.track_ads import update_ad_impressions
from webapp.tasks.ad_tasks import update_ad_impressions
from webapp.controllers.dispatchers.responses.send_pass_http_response import send_pass_http_response
from webapp.tasks.email_tasks import send_mail_to_tech


# Function returns ads list per page
def ads_generator(request, ADS_PER_PAGE, page_identifier_for_ads):
    ads_list = []
    for i in range(ADS_PER_PAGE):
        # get the last element from ads id list and using that id append ads object to ads_list
        ad_id = request.session[page_identifier_for_ads].pop()
        ad_obj = Advertisement.objects.filter(id=ad_id, is_hidden=False, reached_daily_limit=False).first()
        ads_list.append(ad_obj)
        if not request.session[page_identifier_for_ads]:
            break
    return ads_list


# Function to get ads list for latest page and details page (upper main pages)
def get_ads_list(request, ADS_PER_PAGE, page_identifier_for_ads):
    ads_list = []
    community = request.community
    if request.user_agent.is_mobile:
        ad_ids = list(
            Advertisement.objects.filter(community=community, ad_visibility=AD_VISIBILITY.ALL_ARTICLES,
                                         ad_platform__in=(AD_PLATFORMS.Mobile_web, AD_PLATFORMS.All),
                                         ad_type=AD_TYPES.Square,
                                         is_hidden=False,reached_daily_limit=False).values_list('id', flat=True))
    else:
        ad_ids = list(Advertisement.objects.filter(community=community, ad_platform=AD_PLATFORMS.Desktop,
                                                   ad_visibility=AD_VISIBILITY.ALL_ARTICLES,
                                                   ad_type=AD_TYPES.Horizontal, is_hidden=False, reached_daily_limit=False).values_list('id',
                                                                                                             flat=True))

    if page_identifier_for_ads not in request.session:
        request.session[page_identifier_for_ads] = []
    if ad_ids:
        random.shuffle(ad_ids)
        request.session[page_identifier_for_ads] = ad_ids
        ads_list = ads_generator(request, ADS_PER_PAGE, page_identifier_for_ads)
    return ads_list


# Function to get ads list for pagination pages in latest page and details page
def get_pagination_ads_list(request, ADS_PER_PAGE, page_identifier_for_ads):
    ads_list = []
    # Condition to make session key list for ads to empty if key doesn't exist in session
    if page_identifier_for_ads not in request.session:
        request.session[page_identifier_for_ads] = []
    if request.session[page_identifier_for_ads]:
        # Append 3 ads to ad_list (12 news cards per page, 12/4 = 3 ads)
        ads_list = ads_generator(request, ADS_PER_PAGE, page_identifier_for_ads)
    return ads_list

# Function to get ads for mobile and desktop top ad.
def get_top_ad(request):
    community = request.community
    top_ad_ids = []
    if request.user_agent.is_mobile:
        top_ad_ids = list(
            Advertisement.objects.filter(community=community, ad_platform=AD_PLATFORMS.Mobile_web, ad_type=AD_TYPES.Top,
                                         is_hidden=False,reached_daily_limit=False).values_list('id', flat=True))
    else:
        top_ad_ids = list(
            Advertisement.objects.filter(community=community, ad_platform=AD_PLATFORMS.Desktop, ad_type=AD_TYPES.Top,
                                         is_hidden=False,reached_daily_limit=False).values_list('id', flat=True))
    if top_ad_ids:
        random.shuffle(top_ad_ids)
        top_ad_ids = top_ad_ids[0:3]
        top_ads = Advertisement.objects.filter(id__in=top_ad_ids, is_hidden=False, reached_daily_limit=False)
        return top_ads

    else:
        return []

# Function to get desktop right section ad.
def get_desktop_square_ads(request):
    community = request.community
    desktop_square_ad_ids = []
    if request.user_agent.is_mobile:
        return []
    else:
        desktop_square_ad_ids = list(
            Advertisement.objects.filter(community=community, ad_platform__in=(AD_PLATFORMS.Desktop, AD_PLATFORMS.All),
                                         ad_type=AD_TYPES.Square,
                                         is_hidden=False,reached_daily_limit=False).values_list('id', flat=True))
    if desktop_square_ad_ids:
        random.shuffle(desktop_square_ad_ids)
        desktop_square_ad_ids = desktop_square_ad_ids[0:3]
        desktop_square_ad = Advertisement.objects.filter(id__in=desktop_square_ad_ids, is_hidden=False,reached_daily_limit=False)
        return desktop_square_ad
    else:
        return []


# Function to get ads for mobile and desktop top ad.
@csrf_exempt
def get_top_ads(request):
    community = request.community
    top_ad_ids = []
    if request.user_agent.is_mobile:
        top_ad_ids = list(
            Advertisement.objects.filter(community=community, ad_platform=AD_PLATFORMS.Mobile_web, ad_type=AD_TYPES.Top,
                                         is_hidden=False, reached_daily_limit=False).values_list('id', flat=True))
    else:
        top_ad_ids = list(
            Advertisement.objects.filter(community=community, ad_platform=AD_PLATFORMS.Desktop, ad_type=AD_TYPES.Top,
                                         is_hidden=False, reached_daily_limit=False).values_list('id', flat=True))
    if top_ad_ids:
        random.shuffle(top_ad_ids)
        top_ad_ids = top_ad_ids[0:3]
        top_ads = Advertisement.objects.filter(id__in=top_ad_ids, is_hidden=False, reached_daily_limit=False)
    else:
        top_ads = None

    if top_ads:
        try:
            ad_ids_list = top_ads.values_list('id', flat=True)
            update_ad_impressions.delay(ad_ids_list,  request.session.session_key)
        except Exception as e:
            send_mail_to_tech.delay('Argus Ad impression count update failed ', str(e))

    if request.user_agent.is_mobile:
        return render_to_template('components/home_page/mobile_top_ad.html',
                                  {"community": community, "top_ads": top_ads}, request)

    else:
        return render_to_template('components/home_page/desktop_top_ad.html',
                                  {"community": community, "top_ads": top_ads}, request)

@csrf_exempt
def get_desktop_square_ad(request):
    community = request.community
    desktop_square_ad_ids = []
    desktop_square_ads = None
    if request.user_agent.is_mobile:
        desktop_square_ad_ids = []
    else:
        desktop_square_ad_ids = list(
            Advertisement.objects.filter(community=community, ad_platform__in=(AD_PLATFORMS.Desktop, AD_PLATFORMS.All),
                                         ad_type=AD_TYPES.Square,
                                         is_hidden=False,reached_daily_limit=False).values_list('id', flat=True))
    if desktop_square_ad_ids:
        random.shuffle(desktop_square_ad_ids)
        desktop_square_ad_ids = desktop_square_ad_ids[0:3]
        desktop_square_ads = Advertisement.objects.filter(id__in=desktop_square_ad_ids, is_hidden=False,reached_daily_limit=False)

        if desktop_square_ads:
            try:
                ad_ids_list = desktop_square_ads.values_list('id', flat=True)
                update_ad_impressions.delay(ad_ids_list,  request.session.session_key)
            except Exception as e:
                send_mail_to_tech.delay('Argus Ad impression count update failed ', str(e))

    return render_to_template('components/home_page/desktop_square_ad.html',
                              {"desktop_square_ads": desktop_square_ads,'community':community,'test':"test"}, request)



@csrf_exempt
def get_main_ad(request):
    community = request.community
    ad_ids_list = []

    if 'main_ads' in request.session:
        ad_ids_list = request.session['main_ads']
        if ad_ids_list is None:
            ad_ids_list = ad_ids_list

    if request.user_agent.is_mobile:
        ad_obj = Advertisement.objects.filter(community=community, ad_visibility=AD_VISIBILITY.ALL_ARTICLES,
                                         ad_platform__in=(AD_PLATFORMS.Mobile_web, AD_PLATFORMS.All),
                                         ad_type=AD_TYPES.Square,
                                         is_hidden=False, reached_daily_limit=False).exclude(id__in=ad_ids_list).order_by('?').values('id', 'ad_link','ad_image').first()
    else:
        ad_obj = Advertisement.objects.filter(community=community, ad_platform=AD_PLATFORMS.Desktop,
                                                   ad_visibility=AD_VISIBILITY.ALL_ARTICLES,
                                                   ad_type=AD_TYPES.Horizontal, is_hidden=False,
                                                   reached_daily_limit=False).exclude(id__in=ad_ids_list).order_by('?').values('id', 'ad_link','ad_image').first()
    if ad_obj:
        ad_ids_list.append(int(ad_obj['id']))
        request.session['main_ads'] = list(ad_ids_list)
        ad_obj['ad_image'] = storage.url(ad_obj['ad_image'])
    return send_pass_http_response(ad_obj)


def get_amp_top_ads(request):
    community = request.community
    top_ad_ids = list(Advertisement.objects.filter(community=community, ad_platform=AD_PLATFORMS.Mobile_web, ad_type=AD_TYPES.Top,
                                     is_hidden=False, reached_daily_limit=False).values_list('id', flat=True))
    if top_ad_ids:
        random.shuffle(top_ad_ids)
        top_ad_ids = top_ad_ids[0:3]
        top_ads = Advertisement.objects.filter(id__in=top_ad_ids, is_hidden=False, reached_daily_limit=False)
    else:
        top_ads = None

    if top_ads:
        try:
            ad_ids_list = top_ads.values_list('id', flat=True)
            update_ad_impressions.delay(ad_ids_list,  request.session.session_key)
        except Exception as e:
            send_mail_to_tech.delay('Argus Ad impression count update failed ', str(e))

    return top_ads



