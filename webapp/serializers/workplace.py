

def workplace_serializers(workplace, user):
    id = ''
    linkedin_id = ''
    image_url = ''
    workplace_name = ''
    work_status = True
    work_designation = ''
    workplace_location = ''

    # Introducing this field to handle the case where we need to just show workplace name without
    # the location of the workplace
    just_workplace_name = ''

    if workplace:
        id = workplace.id
        linkedin_id = workplace.linkedin_id
        image_url = workplace.image_url
        workplace_name = workplace.name
        just_workplace_name = workplace_name

    if user:
        work_status = user.work_status

        if user.work_designation_ref:
            work_designation = user.work_designation_ref.name

        if user.workplace_location:
            workplace_name += ', ' + user.workplace_location
            workplace_location = user.workplace_location

    serialized_workplace = {
        'id': id,
        'linkedin_id': linkedin_id,
        'plain_name': just_workplace_name,
        'name': workplace_name,
        'image_url': image_url,
        'work_designation': work_designation,
        'work_status': work_status,
        'workplace_location': workplace_location
    }

    return serialized_workplace
