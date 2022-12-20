from django.shortcuts import HttpResponse


def apple_app_site_association(request):
    apple_file = open('apple-app-site-association-unsigned', 'rb')
    response = HttpResponse(apple_file, content_type='application/json')

    return response