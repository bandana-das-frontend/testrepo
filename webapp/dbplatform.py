from webapp.models import *
from webapp.cache import *

from django.contrib.sites.models import get_current_site
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

'''
Note:
    Use _no_cache functions when you get objects to update.
    Use normal cached functions when you just read.
'''


def site(request):
    return {
        'site': lambda: get_current_site(request),
    }


# Site Related DB Wrap
def get_curr_site(request):
    this_site = site(request)['site']
    return this_site


def filter_site(request):
    this_site = get_curr_site(request)
    this_site = get_domain_site(this_site())
    if len(this_site) > 0:
        return this_site[0]
    else:
        return None


@CacheIt()
def get_domain_site(domain):
    this_site = Site.objects.filter(name=domain)
    return this_site


@CacheIt('all_sites')
def get_sites():
    return Site.objects.all()


@CacheIt()
def get_obj_site(db_field):
    this_site = Site.objects.filter(eval(db_field))
    return this_site


def get_all_polls():
    return Poll.objects.select_related().all()


@CacheIt()
def get_obj_poll(db_field, polls=None):
    if polls:
        return polls.select_related().filter(**db_field)
    return Poll.objects.select_related().filter(**db_field)


@CacheIt()
def get_single_obj_poll(db_field):
    try:
        return Poll.objects.get(**db_field)
    except ObjectDoesNotExist:
        return None


def get_single_obj_poll_no_cache(db_field):
    try:
        return Poll.objects.get(**db_field)
    except ObjectDoesNotExist:
        return None


def get_poll_total_votes(db_field):
    total_votes = 0
    for option in Poll.objects.get(**db_field).option_set.all():
        total_votes += option.votes
    return total_votes


def get_all_users():
    return MyUser.objects.all()


@CacheIt()
def get_obj_user(db_field, users=None):
    if users:
        return users.filter(**db_field)
    return MyUser.objects.filter(**db_field)


@CacheIt()
def get_obj_user_excluding_country(exclude_countries):
    return MyUser.objects.filter(
        test_user=False,
        is_registered=True,
        is_onboarded=True
    ).exclude(country__in=exclude_countries)


def get_single_obj_user(db_field):
    try:
        return MyUser.objects.get(**db_field)
    except ObjectDoesNotExist:
        return None


@CacheIt()
def get_obj_option(db_field, options=None):
    if options:
        return options.filter(**db_field)
    return Option.objects.filter(**db_field)


@CacheIt()
def get_single_obj_option(db_field):
    try:
        return Option.objects.get(**db_field)
    except ObjectDoesNotExist:
        return None


def get_obj_useropinion(db_field, useropinions=None):
    if useropinions:
        return useropinions.filter(**db_field)
    return UserOpinion.objects.filter(**db_field)


def get_single_obj_useropinion(db_field):
    return UserOpinion.objects.get(**db_field)


@CacheIt()
def get_obj_media(db_field, medias=None):
    if medias:
        return medias.filter(**db_field)
    return Media.objects.filter(**db_field)


@CacheIt()
def get_single_obj_media(db_field):
    return Media.objects.get(**db_field)


@CacheIt(page=None)
def get_all_topics():
    return Topic.objects.filter(is_hidden=False)


@CacheIt()
def get_obj_topic(db_field, topics=None):
    if topics:
        return topics.filter(**db_field)
    return Topic.objects.filter(**db_field)


@CacheIt()
def get_single_obj_topic(db_field):
    try:
        return Topic.objects.get(**db_field)
    except ObjectDoesNotExist:
        return None


@CacheIt()
def get_obj_friendship(db_field, friendships=None):
    if friendships:
        friendships.filter(**db_field)
    return Friendship.objects.filter(**db_field)


@CacheIt()
def get_single_obj_friendship(db_field):
    try:
        return Friendship.objects.get(**db_field)
    except ObjectDoesNotExist:
        return None


def does_obj_exists_friendship(db_field):
    try:
        friendship = Friendship.objects.get(**db_field)
        return friendship
    except ObjectDoesNotExist:
        return False
    except MultipleObjectsReturned:
        return True


@CacheIt()
def get_all_activities():
    return UserActivity.objects.all()


@CacheIt()
def get_post_following_count(dbfield):
    return UserActivity.objects.filter(**dbfield).count()


def get_obj_activities(dbfield, activities=None):
    if activities:
        return activities.filter(**dbfield)
    return UserActivity.objects.filter(**dbfield)


def get_single_obj_activities(dbfield):
    try:
        return UserActivity.objects.get(**dbfield)
    except ObjectDoesNotExist:
        return None


@CacheIt()
def get_default_score_weights():
    return ScoreWeight.objects.get(name='default')


def get_single_obj_invite_request(db_field):
    try:
        return InviteRequest.objects.get(**db_field)
    except ObjectDoesNotExist:
        return None


def get_single_obj_post(db_field):
    try:
        return Post.objects.get(**db_field)
    except ObjectDoesNotExist:
        return None


@CacheIt()
def get_obj_post(db_field):
    try:
        return Post.objects.filter(**db_field)
    except ObjectDoesNotExist:
        return None


def get_single_obj_post_comment(db_field):
    try:
        return PostComment.objects.get(**db_field)
    except ObjectDoesNotExist:
        return None


def get_obj_post_comment(db_field):
    try:
        return PostComment.objects.filter(**db_field)
    except ObjectDoesNotExist:
        return None


def get_obj_invite_request(db_field):
    try:
        return InviteRequest.objects.filter(**db_field)
    except ObjectDoesNotExist:
        return None


@CacheIt()
def get_following_users(user):
    return Friendship.objects.filter(follower=user)


@CacheIt()
def get_followers(user):
    return Friendship.objects.filter(user=user)


@CacheIt()
def get_users_by_country(country, users=None):
    if users:
        return users.filter(country=country)
    return MyUser.objects.filter(country=country)


@CacheIt()
def get_useropinions_by_country(country, useropinions=None):
    if useropinions:
        return useropinions.filter(user__country=country)
    return []


@CacheIt()
def get_users_following_in_topic(topic):
    return topic.myuser_set.values_list('id', flat=True).filter(test_user=True)


@CacheIt()
def get_users_following_in_topic_excluding_country(topic, countries):
    return topic.myuser_set.values_list('id', flat=True).filter(test_user=True).exclude(country__in=countries)


def get_topics_followed_by_user(user):
    return Topic.objects.filter(is_hidden=False,
                                id__in=UserTopic.objects.filter(user=user, is_following=True)
                                .values_list('topic', flat=True)).order_by('name')


def get_non_banned_topics_followed_by_user(user):
    # Relationships
    banned_topics = [2]

    return Topic.objects.filter(id__in=UserTopic.objects.filter(user=user, is_following=True)
                            .values_list('topic', flat=True)).exclude(id__in=banned_topics)


def get_sorted_topics_followed_by_user(user, sort_type):
        return Topic.objects.filter(id__in=UserTopic.objects.filter(user=user, is_following=True)
                                .values_list('topic', flat=True)).order_by(sort_type)

@CacheIt()
def get_score_weight(db_field):
    return ScoreWeight.objects.get(**db_field)


def get_user_topic_questions(user, topic):
    return user.useropinion_set.filter(poll__topic_polls=topic).values_list('poll', flat=True)


@CacheIt()
def get_unanswered_polls(user):
    voted_questions = user.useropinion_set.filter(user=user).values_list('poll')
    return Poll.objects.select_related().exclude(id__in=voted_questions)


@CacheIt()
def get_unanswered_polls_in_all_topics(user):
    voted_questions = user.useropinion_set.filter(user=user).values_list('poll')
    return Poll.objects.select_related()\
        .filter(topic_polls__id__in=user.usertopic_user
                .filter(is_following=True)
                .values('topic__id'))\
        .exclude(id__in=voted_questions).order_by('?')


@CacheIt()
def get_unanswered_polls_in_a_topic(topic, user):
    voted_questions = user.useropinion_set.filter(user=user).values_list('poll')
    return Poll.objects.select_related().filter(topic_polls=topic).exclude(id__in=voted_questions).order_by('?')


def get_answered_polls(user):
    voted_questions = user.useropinion_set.filter(user=user).values_list('poll')
    return Poll.objects.select_related().filter(id__in=voted_questions)


def get_polls_from_topic(topic):
    polls = Poll.objects.filter(topic_polls=topic)
    return polls


@CacheIt()
def get_total_number_of_topics():
    return Topic.objects.all().count()


@CacheIt()
def get_number_of_topics_following_by_user(user):
    return UserTopic.objects.filter(user=user, is_following=True).count()


@CacheIt()
def get_number_of_users_answered_question(question):
    return UserOpinion.objects.filter(poll=question, user__test_user=False).count()


@CacheIt()
def get_number_of_users_answered_question_excluding_country(question, country):
    return UserOpinion.objects.filter(poll=question, user__test_user=False).exclude(user__country__in=country).count()


def get_number_of_users_answered_in_topic(topic):
    return UserOpinion.objects.filter(poll__in=topic.polls.all()).count()


@CacheIt()
def get_number_of_users_following_topic(topic, country):
    return topic.myuser_set.filter(country=country, test_user=False).count()


def get_configuration():
    return Configuration.objects.get(name='default')


def get_credit_configuration():
    return CreditsConfiguration.objects.get(name='default')


@CacheIt()
def get_number_of_comments_by_user(user):
    return PostComment.objects.filter(created_by=user).count()


@CacheIt()
def get_number_of_posts_by_user(user):
    return Post.objects.filter(created_by=user).count()


@CacheIt()
def get_number_of_events_by_user(user):
    return Event.objects.filter(created_by=user).count()


def get_user_opinions(user_id):
    current_user_option_ids = map(int, UserOpinion.objects.filter(user__id=user_id).values_list('option_id', flat=True))
    current_user_option_ids.append(0)
    current_user_option_ids.append(-1)
    current_user_option_ids_tuple = tuple(current_user_option_ids)
    return current_user_option_ids_tuple


def get_user_polls(user_id):
    current_user_poll_ids = map(int, UserOpinion.objects.filter(user__id=user_id).values_list('poll_id', flat=True))
    current_user_poll_ids.append(0)
    current_user_poll_ids.append(-1)
    current_user_poll_ids_tuple = tuple(current_user_poll_ids)
    return current_user_poll_ids_tuple


def get_single_obj_event(db_field):
    try:
        return Event.objects.get(**db_field)
    except ObjectDoesNotExist:
        return None


def get_community_user_messaging(community_id, language_code):
    user_messaging = UserMessaging.objects.filter(community__id=community_id, language__language_code=language_code)
    if user_messaging:
        user_messaging = user_messaging[0]
    else:
        user_messaging = UserMessaging.objects.filter(community__id=community_id)
        if user_messaging:
            user_messaging = user_messaging[0]
        else:
            # Purva Skywood's user messaging table because it has the default values for user messaging
            user_messaging = UserMessaging.objects.filter(pk=10)[0]

    return user_messaging


def verify_community(community, community_code):
    if community.unique_code.lower() == community_code.lower():
        return True
    return False