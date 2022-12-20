from webapp.models import PostMedia
from webapp.meta_models import ProfileUISections


def get_profile_section_order(user, is_request_user):

    community = user.community.all().first()
    community_profile_sections_order = community.get_profile_sections_order()

    user_profile_sections_order = []
    for profile_section in community_profile_sections_order:

        if profile_section == ProfileUISections().USER_MEDIA_SECTION:
            has_media = PostMedia.objects.filter(post__created_by=user, post__is_announcement=False).count() > 0
            if not has_media and not is_request_user:
                continue

        user_profile_sections_order.append(profile_section)

    return user_profile_sections_order
