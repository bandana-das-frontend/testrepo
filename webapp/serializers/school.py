

def school_serializer(school):
    if not school:
        return {}

    return {
        'name': school.name.title(),
        'id': school.id,
        'block': school.block,
        'district': school.district,
    }
