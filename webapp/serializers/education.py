

def education_serializers(education, user = None):
    if not education:
        return {}

    year_of_graduation = ''
    year_of_admission = ''
    if user:
        if user.year_of_graduation:
            year_of_graduation = user.year_of_graduation

        if user.year_of_admission:
            year_of_admission = user.year_of_admission

    branch = ''
    branch_category = ''
    if user.college_branch_ref:
        branch = user.college_branch_ref.name
        branch_category = user.college_branch_ref.category

    college_relation = ''
    if user.college_relation:
        college_relation = user.college_relation

    college_location = ''
    if user.college_location:
        college_location = user.college_location

    serialized_education = {
        'id': education.id,
        'linkedin_id': education.linkedin_id,
        'name': education.name,
        'image_url': education.image_url,
        'year_of_graduation': year_of_graduation,
        'branch': branch,
        'branch_category': branch_category,
        'year_of_admission': year_of_admission,
        'college_relation': college_relation,
        'college_location': college_location,
    }

    return serialized_education
