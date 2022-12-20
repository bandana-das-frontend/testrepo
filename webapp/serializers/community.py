# -*- coding: utf-8 -*-
from webapp.dbplatform import *
# from webapp.mongodb import MeetupMessages
import datetime


def community_serializers(community):
    if not community:
        return None

    # Change image for Nestaway
    image = community.get_image()

    is_apartment = False
    if community.community_type == CommunityType.APARTMENT:
        is_apartment = True

    num_branches = 0
    branches = community.branches
    if branches:
        num_branches = len(branches.split(','))

    moderation_posts_count = Post.objects.filter(community=community, requires_moderation=True).count()
    moderation_polls_count = Poll.objects.filter(community=community, requires_moderation=True).count()
    moderation_comments_count = PostComment.objects.filter(created_by__community=community, requires_moderation=True).count()
    # moderation_messages_count = MeetupMessages().count({'community_id': community.id, 'requires_moderation': True})
    # moderation_total_count = moderation_posts_count + moderation_comments_count + moderation_messages_count + moderation_polls_count
    num_languages = community.languages.all().count()

    current_year = datetime.datetime.now().year
    copyright_message = '© {} {}. All Rights Reserved.'.format(community.get_registered_brand_name(), current_year)

    user_tags = []
    if community.unique_code.upper() == 'MOSCHOOL':
        user_tags.append({
            'name': USER_TAGS.CELEBRITY,
            'num_users': MyUser.objects.filter(community=community, user_tag=USER_TAGS.CELEBRITY).count()
        })

    serialized_community = {
        'id': community.id,
        'name': community.name,
        'is_apartment': is_apartment,
        'community_type': community.community_type,
        'image': image,
        'app_icon': community.get_app_icon_image(),
        'unique_code': community.unique_code,
        'show_fb_post_option': community.show_fb_post_option,
        'total_users': get_total_users(community.id),
        'min_users_to_unlock': 50,
        'num_days_to_verify_account': community.num_days_to_verify_account,
        'num_branches': num_branches,
        'num_languages': num_languages,
        'allow_users_to_create_polls': community.allow_users_to_create_polls,
        'default_tab': community.default_tab,
        'email_verification_required': community.email_verification_required,
        'nps_survey_session': community.nps_survey_session,
        'enable_nps_survey': community.enable_nps_survey,
        'play_store_url': community.play_store_url,
        'add_community_icon': community.add_community_icon,
        'has_buildings': community.has_buildings,
        'skip_hometown_onbd': community.skip_hometown_onbd,
        'skip_workplace_onbd': community.skip_workplace_onbd,
        'skip_college_onbd': community.skip_college_onbd,
        'about_url': community.about_url,
        'terms_url': community.terms_url,
        'privacy_url': community.privacy_url,
        'moderation_posts_count': moderation_posts_count,
        'moderation_comments_count': moderation_comments_count,
        # 'moderation_messages_count': moderation_messages_count,
        'moderation_polls_count': moderation_polls_count,
        # 'moderation_total_count': moderation_total_count,
        'max_user_created_groups': community.max_user_created_groups,
        'show_open_in_app': community.show_open_in_app, # There is a deprecated field. The latest field is in 'configurations'
        'user_tags': user_tags,
        'copyright_message': copyright_message
    }

    return serialized_community


def get_total_users(community_id):
    community_through = MyUser.community.through
    total_users = community_through.objects.filter(community_id=community_id).count()
    return total_users