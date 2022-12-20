from webapp.controllers.common.template_render import render_to_template
from webapp.models import *
from webapp.controllers.helpers.pagination import *

def live_update(request, unique_url=None):
    page = 1

    community = request.community

    live_update = LiveUpdate.objects.filter(unique_url=unique_url, is_hidden=False).first()
    live_update_details =LiveUpdateDetail.objects.filter(live_update=live_update, is_hidden=False).order_by('-published_date')

    latest_videos = LiveNews.objects.filter(community=community, is_hidden=False, is_live=False).order_by(
        "-published_date")
    latest_videos = paginate(latest_videos, 1, 4)

    return render_to_template('live_update/live_update.html',
                              {
                                  "community": community,
                                  "live_update": live_update,
                                  "latest_video_1": latest_videos[0],
                                  "latest_video_2": latest_videos[1],
                                  "latest_video_3": latest_videos[2],
                                  "latest_video_4": latest_videos[3],
                                  "live_update_details": live_update_details,
                              }, request)

