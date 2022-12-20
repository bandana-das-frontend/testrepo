from django.shortcuts import render_to_response
from webapp.controllers.common.template_render import render_to_template
from django.http import HttpResponseRedirect, HttpResponse


def jobs_view(request):
    community = request.community
    return render_to_template('jobs/jobs.html', {"community": community}, request)