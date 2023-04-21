import json

from django.http import HttpResponse


# Generate HTTP response
def generate_response(msg: str, data: object = None):
    response_dict = {'msg': msg}
    if object is not None:
        response_dict['data'] = data
    response = HttpResponse(json.dumps(response_dict, ensure_ascii=False))
    return response
