from webapp.controllers.common.template_render import render_to_template


def contact_us(request):
    community = request.community
    return render_to_template('meta_pages/contact_us.html',{"community":community},request)