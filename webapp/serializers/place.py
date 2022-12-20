from webapp.templatetags.filters import urlize_html


def place_serializers(place):
    if not place:
        return {}

    serialized_place = {
        'id': place.id,
        'name': place.name,
        'google_id': place.google_id,
        'lat': place.lat,
        'long': place.long,
        'type': place.type if place.type else '',
        'image': place.get_image(),
        'address': place.address if place.address else ''
    }
    return serialized_place


def worldwide_place_serializers():
    return {
        'id': -1,
        'name': 'Worldwide',
        'type': 'WORLDWIDE',
        'google_id': -1,
        'lat': 0,
        'long': 0,
    }