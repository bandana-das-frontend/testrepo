__author__ = 'spaceman'


def people_to_meet_serializers(people_to_meet, user=None, request_source=''):
    if not people_to_meet:
        return None

    name = people_to_meet.name
    image = str(people_to_meet.get_image())
    icon = str(people_to_meet.get_icon())

    # Show 'Announcements' interest as the community name
    # in feed's admin section but during admin create post show it as 'Announcements'
    # if user and people_to_meet.unique_id == 'Announcements' and request_source != 'CREATE_ANNOUNCEMENT':
    #     community = user.community.all()
    #     community = community[0]
    #     name = community.name
    #     image = str(community.get_image())

    if user and user.is_authenticated():
        users_options = user.people_to_meet.all()
    else:
        users_options = []

    if people_to_meet in users_options:
        is_following = True
    else:
        is_following = False

    serialized_people_to_meet = {
        'id': people_to_meet.id,
        'unique_id': people_to_meet.unique_id,
        'name': name,
        'image': image,
        'icon': icon,
        'is_following': is_following,
        'is_fixed': people_to_meet.is_fixed,
        'score': people_to_meet.score,
        'link_url': people_to_meet.link_url if people_to_meet.link_url else '',
        'is_selected': True if people_to_meet.community else False,
        'type': people_to_meet.type,
        'num_following': people_to_meet.num_following,
        'is_admin_only': people_to_meet.is_admin_only,
        'is_default_create_post': people_to_meet.is_default_create_post,
        'is_default_selected': people_to_meet.is_default_selected,
        'new_posts': people_to_meet.new_posts if hasattr(people_to_meet, 'new_posts') else 0,
        'total_posts': people_to_meet.total_posts if hasattr(people_to_meet, 'total_posts') else 0,
    }

    return serialized_people_to_meet


