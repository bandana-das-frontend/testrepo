from webapp.controllers.common.template_render import render_to_template


def terms_of_use(request):
    community = request.community
    return render_to_template('meta_pages/terms_of_use.html',{"community":community},request)