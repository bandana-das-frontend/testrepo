from webapp.controllers.common.template_render import render_to_template
from webapp.models import *
from webapp.controllers.utils.get_ads import get_ads_list
from webapp.tasks.ad_tasks import update_ad_impressions
from webapp.tasks.email_tasks import send_mail_to_tech
from webapp.tasks.article_tasks import update_article_views

def google_amp_post_details_view(request, topic_article=None, unique_url=None):
    # Todo: Change the logic to get community later
    post = Post.objects.filter(unique_url=unique_url).first()
    community = post.community.all().first()

    scroll_posts = Post.objects.filter(community=community, is_hidden=False, language=post.language, is_story=False).exclude(
        id=post.id).order_by("-published_date")[:3]

    update_article_views.delay(post.id)

    language = post.language.language_code

    ad = get_ads_list(request, 1, "amp_page_ads_id")
    ad_object = None

    if ad:
        ad_object = ad[0]
        try:
            ad_id_list = [int(ad_object.id)]
            update_ad_impressions.delay(ad_id_list, request.session.session_key)
        except Exception as e:
            send_mail_to_tech.delay('Argus Ad impression count update failed ', str(e))

    return render_to_template('post/google_amp_template.html',
                              {'post': post,
                               'community': community,
                               'ad_object': ad_object,
                               'language': language,
                               'scroll_posts': scroll_posts
                               }, request)
