from django.shortcuts import HttpResponse
import json


def send_pass_http_response(args=None):
    if not args:
        args = {}

    args['status'] = 'PASS'

    the_data = json.dumps(args)
    response = HttpResponse(the_data, content_type='application/json')

    return response


def send_pass_http_response_with_cors(args=None):
    if not args:
        args = {}

    args['status'] = 'PASS'

    the_data = json.dumps(args)
    response = HttpResponse(the_data, content_type='application/json')
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Headers"] = "*"
    return response