from webapp.templatetags.filters import urlize_html


def college_serializers(college):
    if not college:
        return None

    serialized_college = {
        'id': college.id,
        'name': college.name,
        'city': college.city,
        'country': college.country,
        'number_of_students': college.number_of_students,
        'number_of_alumni': college.number_of_alumni,
        'status': college.status
    }
    return serialized_college