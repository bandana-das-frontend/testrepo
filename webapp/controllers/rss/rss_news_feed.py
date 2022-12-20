from django.contrib.syndication.views import Feed
from webapp.models import *
from datetime import timedelta


class ArgusRSSNewsFeed(Feed):
    language_obj = Language.objects.get(language_code='OR')
    title = 'Argus News'
    link = "https://argusnews.in/"
    description = 'Odisha Latest News, Breaking News, Politics, Jobs, Education, Entertainment, Lifestyle News'

    def get_object(self, request, language_code):
        self.community = request.community
        if language_code:
            self.language_obj = Language.objects.filter(language_code=language_code).first()
        posts = Post.objects.filter(community=self.community, is_hidden=False, language=self.language_obj)\
            .exclude(is_story=True).order_by("-created")
        return posts[:10]

    def items(self, obj):
        return obj

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.text

    def item_link(self, item):
       return item.get_webapp_share_link()

    def item_author_name(self, item):
        return item.created_by.get_full_name()

    def item_categories(self, item):
        categories = item.people_to_meet.all().values_list('name', flat=True)
        return categories

    def item_pubdate(self, item):
        return item.published_date


class ArgusRSSTopicNewsFeed(Feed):
    title = 'Argus News'
    link = "https://argusnews.in/"
    description = 'Odisha Latest News, Breaking News, Politics, Jobs, Education, Entertainment, Lifestyle News'

    def get_object(self, request, language_code, topic):
        self.community = request.community
        posts = []
        language_obj = None
        people_to_meet = None
        if language_code:
            language_obj = Language.objects.filter(language_code=language_code).first()
        if not language_obj:
            language_obj = Language.objects.filter(language_code='OR').first()
        if topic:
            people_to_meet = PeopleToMeet.objects.filter(url_path=topic, community=self.community).first()

        if people_to_meet:
            posts = Post.objects.filter(community=self.community, is_hidden=False, language=language_obj,
                                        people_to_meet=people_to_meet).exclude(is_story=True).order_by("-created")
        return posts[:10]

    def items(self, obj):
        return obj

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.text

    def item_link(self, item):
       return item.get_webapp_share_link()

    def item_author_name(self, item):
       return item.created_by.get_full_name()

    def item_categories(self, item):
        categories = item.people_to_meet.all().values_list('name', flat=True)
        return categories

    def item_pubdate(self, item):
        return item.published_date


class ArgusRSSTrending(Feed):
    language_obj = Language.objects.get(language_code='OR')
    title = 'Argus News'
    link = "https://argusnews.in/"
    description = 'Odisha Latest News, Breaking News, Politics, Jobs, Education, Entertainment, Lifestyle News'

    def get_object(self, request, language_code):
        self.community = request.community

        # getting date time of 2 days before's i.e, 48 hours back
        last_2_days = datetime.now() - timedelta(hours=48)

        if language_code:
            self.language_obj = Language.objects.filter(language_code=language_code).first()
        posts = Post.objects.filter(community=self.community, is_hidden=False, language=self.language_obj,
                                    is_breaking_news=False, views__gte=1, published_date__gte=last_2_days)\
            .exclude(is_story=True).order_by('-views','-published_date')
        return posts[:10]

    def items(self, obj):
        return obj

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.text

    def item_link(self, item):
       return item.get_webapp_share_link()

    def item_author_name(self, item):
        return item.created_by.get_full_name()

    def item_categories(self, item):
        categories = item.people_to_meet.all().values_list('name', flat=True)
        return categories

    def item_pubdate(self, item):
        return item.published_date
