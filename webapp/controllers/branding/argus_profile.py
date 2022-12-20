from django.views.decorators.csrf import csrf_exempt
from webapp.controllers.errors.error_404 import *


@csrf_exempt
def argus_profile(request):
    return render_to_template('branding/argus_profile.html',
                              {}, request)
