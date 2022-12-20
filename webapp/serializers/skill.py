

def skill_serializer(skill):
    if not skill:
        return

    return {
        'name': skill.name,
        'id': skill.id
    }