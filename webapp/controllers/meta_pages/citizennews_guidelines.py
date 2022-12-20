from webapp.controllers.common.template_render import render_to_template


def citizennews_guidelines(request):
    community = request.community
    return render_to_template('meta_pages/citizennews_guidelines.html',{"community":community},request)