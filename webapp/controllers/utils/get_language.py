from webapp.models import Language


def get_language(request):
    language = None
    if 'lang_code' in request.session:
        language_code = request.session['lang_code']
        language = Language.objects.filter(language_code=language_code).first()

    if not language:
        language_code = 'OR'
        language = Language.objects.filter(language_code=language_code).first()

    return language
