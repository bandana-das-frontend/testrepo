from django.views.decorators.csrf import csrf_exempt
from webapp.controllers.errors.error_404 import *
from webapp.controllers.utils.get_ads import  get_ads_list
from webapp.tasks.ad_tasks import update_ad_impressions
from webapp.models import *
from webapp.controllers.widgets import web_widgets


@csrf_exempt
def channel_number(request):

    community = request.community
    live = LiveNews.objects.get(community=community, is_live=True)
    live_id = live.id
    comments = ProgramComment.objects.filter(program=live.id).order_by("-created")
    total_comments = comments.count()

    return render_to_template('channel/channel_number.html',
                              {
                               "community": community,
                               "live": live,
                               "live_id": int(live_id),
                               'comments': comments[:15],
                               'total_comments': total_comments,
                               }, request)

