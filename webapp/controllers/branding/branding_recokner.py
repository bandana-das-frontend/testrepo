from django.views.decorators.csrf import csrf_exempt
from webapp.controllers.errors.error_404 import *


@csrf_exempt
def branding_recokner(request):
    return render_to_template('branding/branding_recokner.html',
                              {}, request)
