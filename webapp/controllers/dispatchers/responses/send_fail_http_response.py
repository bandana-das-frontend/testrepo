from django.shortcuts import HttpResponse
import json


def send_fail_http_response(args=None):
    if not args:
        args = {}
    args['status'] = 'FAIL'
    the_data = json.dumps(args)
    response = HttpResponse(the_data, content_type='application/json')
    return response