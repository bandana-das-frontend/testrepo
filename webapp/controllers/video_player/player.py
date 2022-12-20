from django.views.generic import View
from django.shortcuts import render_to_response
from django.template import RequestContext


def player(request, community_code=None):
    return render_to_response('video_player/player.html', {}, context_instance=RequestContext(request))
