from webapp.controllers.common.template_render import render_to_template


def privacy_policy(request):
    community = request.community
    return render_to_template('meta_pages/privacy_policy.html',{"community":community},request)