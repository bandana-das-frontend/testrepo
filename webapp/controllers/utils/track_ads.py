from webapp.models import *
from webapp.controllers.dispatchers.responses.send_fail_http_response import send_fail_http_response
from webapp.controllers.dispatchers.responses.send_pass_http_response import send_pass_http_response
from django.views.decorators.csrf import csrf_exempt
import json
from webapp.tasks.ad_tasks import *
from django.http import HttpResponseRedirect
from django.shortcuts import  redirect


@csrf_exempt
def update_ad_clicks(request):
    community = request.community
    if request.method == "POST":
        try:
            ad_id = request.POST["ad_id"]
            update_ad_click_count.delay(ad_id, community, request.session.session_key)
            return send_pass_http_response()
        except:
            send_fail_http_response()
    else:
        return send_fail_http_response()


@csrf_exempt
def update_ad_clicks_by_id(request):
    community = request.community

    type = ''
    if 'type' in request.GET:
        type = request.GET['type']

    if "ad_id" in request.GET:
        ad_id = request.GET["ad_id"]
        ad_obj = Advertisement.objects.filter(id=ad_id).first()
        try:
            update_ad_click_count.delay(ad_id, community, request.session.session_key, type)
            return redirect(ad_obj.ad_link)
        except:
            return redirect(ad_obj.ad_link)
    else:
        return redirect("/")


# Update_ad_impressions function accepts list of ad ids
def update_ad_impressions(ad_list, request):
    if ad_list:
        for ad in ad_list:
            if ad:
                ad.ad_impressions += 1
                ad.save(update_fields=["ad_impressions"])
                AdImpression.objects.create(ad=ad, session_id=request.session.session_key)


# Update_ad_impressions function accepts list of ad ids
@csrf_exempt
def update_ad_impressions_from_ui(request):

    if request.method == 'POST':

        try:
            ads_list = str(request.POST['ads_id_list']).encode('utf-8')
            top_ads = str(request.POST['top_ads']).encode('utf-8')
            desktop_ads = request.POST['desktop_ads']


            if ads_list:
                ads_id_list = json.loads(ads_list)
                for id in ads_id_list:
                    ad_obj = Advertisement.objects.filter(id=id).first()
                    ad_obj.ad_impressions += 1
                    ad_obj.save(update_fields=["ad_impressions"])
                    AdImpression.objects.create(ad=ad_obj, session_id=request.session.session_key)

            if top_ads:
                top_ads_id = json.loads(top_ads)
                for id in top_ads_id:
                    ad_obj = Advertisement.objects.filter(id=id).first()
                    ad_obj.ad_impressions += 1
                    ad_obj.save(update_fields=["ad_impressions"])
                    AdImpression.objects.create(ad=ad_obj, session_id=request.session.session_key)

            if desktop_ads:
                ad_obj = Advertisement.objects.filter(id=int(desktop_ads)).first()
                ad_obj.ad_impressions += 1
                ad_obj.save(update_fields=["ad_impressions"])
                AdImpression.objects.create(ad=ad_obj, session_id=request.session.session_key)

        except :
            pass

    return send_pass_http_response()



@csrf_exempt
def update_ad_impression_by_id(request):
    type = ''
    if 'type' in request.GET:
        type = request.GET['type']
    if 'ad_id' in request.GET:
        ad_id = request.GET['ad_id']
        try:
            ad_id = request.GET['ad_id']
            update_ad_impressions_fb.delay(ad_id, request.session.session_key, type)
        except :
            pass
    return send_pass_http_response()


@csrf_exempt
def redirect_to_amp_ad_link(request):
    community = request.community
    if request.method == "GET":
        try:
            ad_id = request.GET["ad_id"]
            ad_obj = Advertisement.objects.filter(id=int(ad_id)).first()
            update_ad_click_count.delay(ad_id, community, request.session.session_key)
            return HttpResponseRedirect(ad_obj.ad_link)
        except:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
