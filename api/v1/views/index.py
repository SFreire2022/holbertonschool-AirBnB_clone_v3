#!/usr/bin/python3
"""index"""
import models
from api.v1.views import app_views
from flask import jsonify
from models.base_model import BaseModel


@app_views.route('/status')
def status_ok():
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def ret_count():
    dic = {'amenities': Amenity, 'cities': City,
           'places': Place, 'reviews': Review,
           'states': State, 'users': User}
    for key in dic:
        dic[key] = storage.count(dic[key])
    return jsonify(dic)
