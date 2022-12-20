from webapp.controllers.common.template_render import render_to_template
from webapp.models import *
from datetime import timedelta
from webapp.controllers.utils.get_ads import get_amp_top_ads


def trending_amp(request, language_code=None):
    community = request.community
    if request.session['lang_code'] != language_code and language_code is not None:
        request.session['lang_code'] = language_code

    language = Language.objects.filter(language_code=language_code).first()
    # getting date time of 2 days before's i.e, 48 hours back
    last_2_days = datetime.now() - timedelta(hours=48)

    posts = Post.objects.filter(community=community, is_hidden=False, language=language, is_breaking_news=False,
                                views__gte=1, published_date__gte=last_2_days).exclude(is_story=True) \
                .exclude(people_to_meet__unique_id__icontains="Citizen_News").order_by('-views', '-published_date')[:20]

    top_ads = get_amp_top_ads(request)

    return render_to_template('trending/trending_amp.html',
                              {
                                  "first_post": posts[0] if posts else None,
                                  "posts": posts[1:] if len(posts) >= 1 else None,
                                  "community": community,
                                  "language": language_code,
                                  "top_ads": top_ads
                              }, request)
