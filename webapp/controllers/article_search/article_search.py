from webapp.controllers.helpers.pagination import *
from webapp.controllers.errors.error_404 import *
from webapp.models import *
from django.db.models import Q  # Importing for global search
from itertools import chain
from webapp.controllers.utils.get_language import get_language


def get_search_articles(request, search_type=None):
    community = request.community
    query_string = ""
    topic_string = ""
    location_string = ""
    citizen_news = PeopleToMeet.objects.get(unique_id='THEARGUS_Citizen_News')

    if 'search_string' in request.GET and request.GET['search_string'].strip():
        query_string = str(request.GET['search_string'].encode("utf8")).strip()

    if 'topic' in request.GET and request.GET['topic'].strip():
        topic_string = str(request.GET['topic'].encode("utf8"))

    if 'location' in request.GET and request.GET['location'].strip():
        location_string = str(request.GET['location'].encode("utf8")).strip()

    POSTS_PAGINATION_SIZE = 12
    posts = []
    post_counts = 0
    article_ids = []
    video_ids = []
    articles = []
    videos = []
    sub_filter = Q()
    live_topic_filter = Q()

    # query to get the posts and videos wrt entered input string
    q = Q(text__icontains=query_string) | Q(title__icontains=query_string) | Q(label__icontains=query_string) | Q(locations__icontains=query_string)
    v = Q(text__icontains=query_string) | Q(title__icontains=query_string) | Q(topic__icontains=query_string)

    language = get_language(request)

    if topic_string and location_string:
        lang_people_to_meet = LangPeopleToMeet.objects.filter(name=topic_string, language=language).first()
        if lang_people_to_meet and lang_people_to_meet.name:
            people_to_meet_id = lang_people_to_meet.people_to_meet.id
        else:
            people_to_meet_id = PeopleToMeet.objects.filter(name=topic_string, community=community).first()
        sub_filter = Q(people_to_meet=people_to_meet_id) & Q(locations__icontains=location_string)
        live_topic_filter = Q(people_to_meet=people_to_meet_id)

    elif topic_string:
        lang_people_to_meet = LangPeopleToMeet.objects.filter(name=topic_string, language=language).first()
        if lang_people_to_meet and lang_people_to_meet.name:
            people_to_meet_id = lang_people_to_meet.people_to_meet.id
        else:
            people_to_meet_id = PeopleToMeet.objects.filter(name=topic_string, community=community).first()
        sub_filter = Q(people_to_meet=people_to_meet_id)
        live_topic_filter = Q(people_to_meet=people_to_meet_id)

    elif location_string:
        sub_filter = Q(locations__icontains=location_string)

    if query_string:
        if search_type == "news":
            article_ids = Post.objects.filter(community=community, is_hidden=False, language=language).filter(q).filter(sub_filter).order_by('-published_date').exclude(Q(is_story=True) | Q(people_to_meet=citizen_news)).values_list('id', flat=True)
        elif search_type == "videos":
            video_ids = LiveNews.objects.filter(community=community, is_hidden=False).filter(v).filter(live_topic_filter).order_by('-published_date').values_list('id', flat=True)
        else:
            article_ids = Post.objects.filter(community=community, is_hidden=False, language=language).filter(q).filter(sub_filter).order_by('-published_date').exclude(Q(is_story=True) | Q(people_to_meet=citizen_news)).values_list('id', flat=True)
            video_ids = LiveNews.objects.filter(community=community, is_hidden=False).filter(v).filter(live_topic_filter).order_by('-published_date').values_list('id', flat=True)
    else:
        if search_type == "news":
            article_ids = Post.objects.filter(community=community, is_hidden=False, language=language).filter(sub_filter).order_by('-published_date').exclude(Q(is_story=True) | Q(people_to_meet=citizen_news)).values_list('id', flat=True)
        elif search_type == "videos":
            video_ids = LiveNews.objects.filter(community=community, is_hidden=False).filter(live_topic_filter).order_by('-published_date').values_list('id', flat=True)
        else:
            article_ids = Post.objects.filter(community=community, is_hidden=False, language=language).filter(sub_filter).order_by('-published_date').exclude(Q(is_story=True) | Q(people_to_meet=citizen_news)).values_list('id', flat=True)
            video_ids = LiveNews.objects.filter(community=community, is_hidden=False).filter(live_topic_filter).order_by('-published_date').values_list('id', flat=True)

    #  get the total length of the result
    if article_ids:
        post_counts = article_ids.count()
    if video_ids:
        post_counts = post_counts + video_ids.count()

    #  Apply pagination for first 12 post and videos.
    #  Chain them and Sort them based on publish date.

    article_ids = paginate(article_ids, 1, POSTS_PAGINATION_SIZE)
    video_ids = paginate(video_ids, 1, POSTS_PAGINATION_SIZE)

    articles = Post.objects.filter(pk__in=article_ids)
    videos = LiveNews.objects.filter(pk__in=video_ids)

    posts = list(chain(articles, videos))
    posts.sort(key=lambda post: post.published_date, reverse=True)

    locations = ["Angul", "Balangir", "Balasore", "Bargarh", "Bhadrak", "Boudh", "Cuttack", "Deogarh", "Dhenkanal",
                 "Gajapati", "Ganjam", "Jagatsinghapur", "Jajpur", "Jharsuguda", "Kalahandi", "Kandhamal",
                 "Kendrapara", "Kendujhar", "Khordha", "Koraput", "Malkangiri", "Mayurbhanj", "Nabarangpur",
                 "Nayagarh", "Nuapada", "Puri", "Rayagada", "Sambalpur", "Sonepur", "Sundargarh"]

    language_code_long = 'LANGUAGE_' + language.language_code.upper()
    community_config_view = CommunityConfigurations.objects.filter(community=community, filter_parameter=language_code_long).first()
    community_program_interests_ids = community_config_view.get_community_program_interests()
    community_admin_interests_ids = community_config_view.get_community_admin_interests()

    all_people_to_meet_ids = list(set(community_program_interests_ids + community_admin_interests_ids))
    all_people_to_meet = []
    for people_to_meet_id in all_people_to_meet_ids:
        people_to_meet = PeopleToMeet.objects.filter(pk=people_to_meet_id).first()
        if people_to_meet:
            lang_people_to_meet = LangPeopleToMeet.objects.filter(people_to_meet=people_to_meet, language=language).first()
            if lang_people_to_meet and lang_people_to_meet.name:
                people_to_meet.name = lang_people_to_meet.name
            all_people_to_meet.append(people_to_meet)

    if request.user_agent.is_mobile:
        mobile_view = render_to_template('post_search/post_searched.html',
                                         {'posts': posts,
                                          'query_string': query_string,
                                          "search_type": search_type,
                                          'locations': locations,
                                          'topic': topic_string,
                                          'location': location_string,
                                          "post_counts": post_counts,
                                          "all_people_to_meet": all_people_to_meet
                                          }, request)
        return mobile_view

    else:
        recommended_posts = Post.objects.filter(community=community, is_hidden=False, is_story=False, language=language).exclude(
            people_to_meet=citizen_news).order_by("-published_date")[:7]
        latest_videos = LiveNews.objects.filter(community=community, is_hidden=False, is_live=False).order_by("-published_date")
        latest_videos = paginate(latest_videos, 1, 4)
        desktop_view = render_to_template('post_search/post_searched.html',
                                  {'posts': posts,
                                   'query_string': query_string,
                                   'recommended_posts': recommended_posts,
                                   "community": community,
                                   'locations': locations,
                                   'topic': topic_string,
                                   'location': location_string,
                                   "search_type": search_type,
                                   "latest_video_1": latest_videos[0],
                                   "latest_video_2": latest_videos[1],
                                   "latest_video_3": latest_videos[2],
                                   "latest_video_4": latest_videos[3],
                                   "post_counts": post_counts,
                                   "all_people_to_meet": all_people_to_meet
                                   }, request)
        return desktop_view


def pagination_search_result(request, search_type=None):
    POSTS_PAGINATION_SIZE = 12
    community = request.community
    page = 2
    query_string = ""
    topic_string = ""
    location_string = ""
    sub_filter = Q()
    live_topic_filter = Q()

    if 'page' in request.GET:
        page = int(str(request.GET["page"]))

    if 'search_string' in request.GET and request.GET['search_string'].strip():
        query_string = str(request.GET['search_string'].encode("utf8"))

    if 'topic' in request.GET and request.GET['topic'].strip():
        topic_string = str(request.GET['topic'].encode("utf8"))

    if 'location' in request.GET and request.GET['location'].strip():
        location_string = str(request.GET['location'].encode("utf8"))


    q = Q(text__icontains=query_string) | Q(title__icontains=query_string) | Q(label__icontains=query_string) | Q(locations__icontains=query_string)
    v = Q(text__icontains=query_string) | Q(title__icontains=query_string) | Q(topic__icontains=query_string)

    scroll_posts = []
    article_ids = []
    video_ids = []
    articles = []
    videos = []

    language = get_language(request)

    if topic_string and location_string:
        lang_people_to_meet = LangPeopleToMeet.objects.filter(name=topic_string, language=language).first()
        if lang_people_to_meet and lang_people_to_meet.name:
            people_to_meet_id = lang_people_to_meet.people_to_meet.id
        else:
            people_to_meet_id = PeopleToMeet.objects.filter(name=topic_string, community=community).first()
        sub_filter = Q(people_to_meet=people_to_meet_id) & Q(locations__icontains=location_string)
        live_topic_filter = Q(people_to_meet=people_to_meet_id)
    elif topic_string:
        lang_people_to_meet = LangPeopleToMeet.objects.filter(name=topic_string, language=language).first()
        if lang_people_to_meet and lang_people_to_meet.name:
            people_to_meet_id = lang_people_to_meet.people_to_meet.id
        else:
            people_to_meet_id = PeopleToMeet.objects.filter(name=topic_string, community=community).first()
        sub_filter = Q(people_to_meet=people_to_meet_id)
        live_topic_filter = Q(people_to_meet=people_to_meet_id)
    elif location_string:
        sub_filter = Q(locations__icontains=location_string)

    if query_string:
        if search_type == "news":
            article_ids = Post.objects.filter(community=community, is_hidden=False, language=language).filter(q).filter(sub_filter).order_by('-published_date').exclude(is_story=True).values_list('id', flat=True)
        elif search_type == "videos":
            video_ids = LiveNews.objects.filter(community=community, is_hidden=False).filter(v).filter(live_topic_filter).order_by('-published_date').values_list('id', flat=True)
        else:
            article_ids = Post.objects.filter(community=community, is_hidden=False, language=language).filter(q).filter(sub_filter).order_by('-published_date').exclude(is_story=True).values_list('id', flat=True)
            video_ids = LiveNews.objects.filter(community=community, is_hidden=False).filter(v).filter(live_topic_filter).order_by('-published_date').values_list('id', flat=True)
    else:
        if search_type == "news":
            article_ids = Post.objects.filter(community=community, is_hidden=False, language=language).filter(sub_filter).order_by('-published_date').exclude(is_story=True).values_list('id', flat=True)
        elif search_type == "videos":
            video_ids = LiveNews.objects.filter(community=community, is_hidden=False).filter(live_topic_filter).order_by('-published_date').values_list('id', flat=True)
        else:
            article_ids = Post.objects.filter(community=community, is_hidden=False, language=language).filter(sub_filter).order_by('-published_date').exclude(is_story=True).values_list('id', flat=True)
            video_ids = LiveNews.objects.filter(community=community, is_hidden=False).filter(live_topic_filter).order_by('-published_date').values_list('id', flat=True)

    #  Apply pagination for 12 post and videos.
    #  Chain them and Sort them based on publish date.

    article_ids = paginate(article_ids, page, POSTS_PAGINATION_SIZE)
    video_ids = paginate(video_ids, page, POSTS_PAGINATION_SIZE)

    articles = Post.objects.filter(pk__in=article_ids)
    videos = LiveNews.objects.filter(pk__in=video_ids)

    scroll_posts = list(chain(articles, videos))
    scroll_posts.sort(key=lambda post: post.published_date, reverse=True)

    return render_to_template('post_search/searched_posts_page.html', {
                                    "scroll_posts": scroll_posts,
                                    'query_string':query_string,
                                    'search_type':search_type,
                                    "community": community,
                                }, request)
