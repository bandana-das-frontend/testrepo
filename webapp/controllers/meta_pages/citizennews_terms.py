from webapp.controllers.common.template_render import render_to_template


def citizennews_terms(request):
    community = request.community
    return render_to_template('meta_pages/citizennews_terms.html',{"community":community},request)