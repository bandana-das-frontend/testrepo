from django.shortcuts import render_to_response
from webapp.controllers.common.template_render import render_to_template
from django.http import HttpResponseRedirect, HttpResponse

def handle404(request):
    community = request.community
    template = 'errors/404.html'
    response = render_to_template(template, {"community": community}, request)
    response.status_code = 404
    return response