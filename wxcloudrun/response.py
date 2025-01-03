import json

from flask import Response
from objtyping import to_primitive


def success_empty_response():
    data = json.dumps({'code': 0, 'data': {}})
    return Response(data, mimetype='application/json')


def success_response(data):
    data = json.dumps(to_primitive({'code': 0, 'data': data}), ensure_ascii=False)
    return Response(data, mimetype='application/json')


def err_response(err_msg):
    data = json.dumps({'code': -1, 'errorMsg': err_msg})
    return Response(data, mimetype='application/json')
