from webapp.models import PostMedia


def post_media_serializer(post):
    post_media_serialized = []
    if post is None:
        return post_media_serialized

    post_media = PostMedia.objects.filter(post=post)
    for media in post_media:
        post_media_object = media_serializer(media)
        post_media_serialized.append(post_media_object)

    return post_media_serialized


def static_info_media_serializer(static_info):
    post_media_serialized = []
    if static_info is None:
        return post_media_serialized

    post_media = PostMedia.objects.filter(static_info=static_info)
    for media in post_media:
        post_media_object = media_serializer(media)
        post_media_serialized.append(post_media_object)

    return post_media_serialized


def media_serializer(media):
    if not media:
        return None

    media_serialized = {
        'image': media.get_image(force_large=True),
        'video': media.get_video(),
        'doc': media.get_doc(),
        'type': media.type,
        'height': media.height,
        'width': media.width,
        'name': media.name,
    }

    return media_serialized