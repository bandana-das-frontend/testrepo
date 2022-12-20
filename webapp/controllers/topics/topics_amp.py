from webapp.controllers.common.template_render import render_to_template
from webapp.models import *
from webapp.controllers.utils.get_ads import get_amp_top_ads


def topics_amp(request, language_code=None, topic=None):
    community = request.community
    if request.session['lang_code'] != language_code and language_code is not None:
        request.session['lang_code'] = language_code

    topic_obj = PeopleToMeet.objects.filter(url_path=topic, community=community).first()
    topic_id = topic_obj.id

    language = Language.objects.filter(language_code=language_code).first()
    posts = Post.objects.filter(community=community, is_hidden=False, people_to_meet=topic_id,
                                language=language).exclude(is_story=True).order_by("-created")[:20]

    top_ads = get_amp_top_ads(request)

    return render_to_template('topics/topics_amp.html',
                              {
                                  "first_post": posts[0] if posts else None,
                                  "posts": posts[1:] if len(posts) >= 1 else None,
                                  "community": community,
                                  "topic_obj": topic_obj,
                                  "language": language_code,
                                  "top_ads": top_ads
                              }, request)
