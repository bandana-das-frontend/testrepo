from webapp.models import SchoolGoing
from webapp.serializers.school import school_serializer


def user_school_serializer(user):
    if user.schools.count() <= 0:
        return {}

    school = {}
    school_going = SchoolGoing.objects.filter(user=user).first()

    if school_going:
        school = school_going_serializer(school_going)

    return school


def user_school_going_serializer(user):
    school_going_serialized = []

    school_goings = SchoolGoing.objects.filter(user=user)

    if school_goings.count() <= 0:
        return school_going_serialized

    if school_goings.count > 0:
        for school_going in school_goings:
            school_going_serialized.append(
                school_going_serializer(school_going)
            )

    return school_going_serialized


def school_going_serializer(school_going):
    school_going_serialized = school_serializer(school_going.school)
    school_going_serialized['year_of_graduation'] = school_going.year
    school_going_serialized['school_going_id'] = school_going.id

    return school_going_serialized
