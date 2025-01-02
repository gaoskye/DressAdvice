import json
from datetime import datetime

from flask import Response

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        if isinstance(obj, int):
            return int(obj)
        elif isinstance(obj, float):
            return float(obj)
        else:
            return super(MyEncoder, self).default(obj)

def success_empty_response():
    data = json.dumps({'code': 0, 'data': {}})
    return Response(data, mimetype='application/json')


def success_response(data):
    data = json.dumps({'code': 0, 'data': data}, cls=MyEncoder)
    return Response(data, mimetype='application/json')


def err_response(err_msg):
    data = json.dumps({'code': -1, 'errorMsg': err_msg})
    return Response(data, mimetype='application/json')
