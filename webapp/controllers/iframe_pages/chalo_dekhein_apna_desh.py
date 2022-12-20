from django.views.decorators.csrf import csrf_exempt
from webapp.controllers.errors.error_404 import *
from django.shortcuts import  redirect


@csrf_exempt
def chalo_dekhein_apna_desh(request):
    return redirect("https://cdad.argusnews.co/")
    # return render_to_template('iframe_pages/chalo_dekhein_apna_desh.html',
    #                           {}, request)
