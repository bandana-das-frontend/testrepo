from webapp.models import AdImpression, Advertisement, AdClick
from celery.task import task
# Update_ad_impressions function accepts list of ad ids


@task(name='update_ad_impressions')
def update_ad_impressions(ad_list, session_id):
    if ad_list:
        for id in ad_list:
            if id:
                ad_obj = Advertisement.objects.filter(id=int(id)).first()
                ad_obj.ad_impressions += 1
                ad_obj.save(update_fields=["ad_impressions"])
                AdImpression.objects.create(ad=ad_obj, session_id=session_id)


@task(name='update_ad_impressions_fb')
def update_ad_impressions_fb(ad_id, session_id, type=None):
    if ad_id:
        ad_obj = Advertisement.objects.filter(id=int(ad_id)).first()
        # ad_obj.ad_impressions += 1
        # ad_obj.save(update_fields=["ad_impressions"])
        AdImpression.objects.create(ad=ad_obj, type=type, session_id=session_id)


@task(name='update_ad_click_count')
def update_ad_click_count(ad_id, community, session_id, type=None):
    ad = Advertisement.objects.filter(community=community, id=ad_id).first()
    ad.ad_clicks += 1
    ad.save(update_fields=["ad_clicks"])
    AdClick.objects.create(ad=ad, type=type, session_id=session_id)



