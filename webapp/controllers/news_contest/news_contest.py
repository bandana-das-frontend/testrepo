from django.views.decorators.csrf import csrf_exempt
from webapp.controllers.dispatchers.responses.send_fail_http_response import send_fail_http_response
from webapp.controllers.dispatchers.responses.send_pass_http_response import send_pass_http_response
from webapp.models import *
from webapp.controllers.errors.error_404 import *


def show_contest_form(request, unique_url=""):
    unique_url = str(unique_url)
    community = request.community
    contest = None
    contest = Contest.objects.filter(community=community, unique_url=unique_url, status=True).first()

    if contest is None:
        return handle404(request)

    webview = "webview" in str(request.user_agent).lower()
    if request.user_agent.os.family == "iOS":
        webview = True

    if not webview:
        return HttpResponseRedirect("https://argusnews.page.link/download")
    return render_to_template('contest/contest.html',
                              {
                                  "contest": contest,
                                  "webview": webview,
                                  "community": community,
                              }, request)


# Get the contest popup data(image and url) to show them once in a session
@csrf_exempt
def get_contest_popup_data(request):
    if request.method == 'POST':
        community = request.community
        # try:
        popup_ad = Advertisement.objects.filter(community=community, ad_platform=AD_PLATFORMS.Web_all,
                                                ad_type=AD_TYPES.Popup, ad_format=AD_FORMATS.Image,
                                                is_hidden=False, reached_daily_limit=False).first()
        if not popup_ad is None:
            popup_img = popup_ad.get_ad_image_in_webp()
            popup_url = popup_ad.ad_link
            return send_pass_http_response({'popup_img': popup_img, 'popup_url': popup_url})
    return send_fail_http_response()
