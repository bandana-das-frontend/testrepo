from webapp.controllers.common.template_render import render_to_template
from webapp.models import *
from webapp.controllers.utils.get_language import get_language
from webapp.controllers.utils.get_ads import get_amp_top_ads

def home_amp(request, language=None):
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

        posts = Post.objects.filter(community=community, is_breaking_news=False, is_hidden=False, is_story=False, language=language)\
            .order_by('-is_top_post', 'top_post_order_no', '-published_date')[:20]

    else:
        language_code = None
        english_text = None

        # checking for breaking news that is not older than 24 hrs
        breaking_news = Post.objects.filter(community=community, is_breaking_news=True,\
                                            is_hidden=False, published_date__gte=datetime.now()-timedelta(hours=24)).first()

        posts = Post.objects.filter(community=community, is_breaking_news=False, is_hidden=False, is_story=False)\
            .order_by('-is_top_post', 'top_post_order_no', '-published_date')[:20]

    if breaking_news is not None:
        breaking_news_post = breaking_news
    else:
        breaking_news_post = None

    first_post = posts[0]
    posts = posts[1:]

    top_ads = get_amp_top_ads(request)

    return render_to_template('home/home_amp.html',
                              {
                                  "first_post": first_post,
                                  "posts": posts,
                                  "community": community,
                                  "breaking_news_post": breaking_news_post,
                                  "language": language_code,
                                  "top_ads": top_ads
                              }, request)
