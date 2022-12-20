from django.shortcuts import render_to_response
from webapp.controllers.common.template_render import render_to_template
from django.http import HttpResponseRedirect, HttpResponse


def handle500(request):
    community = request.community
    template = 'errors/500.html'

    return render_to_template(template, {"community": community}, request)