#!/usr/bin/python3
"""index"""
import models
from api.v1.views import app_views
from flask import jsonify
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status')
def status_ok():
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def ret_count():
    dic = {'amenities': Amenity, 'cities': City,
           'places': Place, 'reviews': Review,
           'states': State, 'users': User}
    for key in dic:
        dic[key] = storage.count(dic[key])
    return jsonify(dic)
