#!/usr/bin/python3
"""Places API module"""
import models
from api.v1.views import app_views
from flask import jsonify, abort, request, Response, make_response
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def list_city_places(city_id):
    """Retrieves the list of all Place objects for a given city_id"""
    object_city = storage.get('City', city_id)
    if object_city is None:
        abort(404)
    allplaces = object_city.places
    places = []
    for obj in allplaces:
        places.append(obj.to_dict())

    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False)
def fetch_place(place_id):
    """Retrieves a Place object for a given id"""
    object_place = storage.get('Place', place_id)
    if object_place is None:
        abort(404)
    place = object_place.to_dict()

    return jsonify(place)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object maching id"""
    object_place = storage.get('Place', place_id)
    if object_place is None:
        abort(404)

    storage.delete(object_place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_city_place(city_id):
    """Create a Place object for given City ID if method post and body contains
    json format and contains user_id and name key"""
    object_city = storage.get('City', city_id)
    if object_city is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    object_data = request.json
    if 'user_id' not in object_data.keys():
        abort(400, "Missing user_id")
    if 'name' not in object_data.keys():
        abort(400, "Missing name")
    object_user = storage.get('User', object_data['user_id'])
    if object_user is None:
        abort(404)
    object_data['city_id'] = city_id
    instance = Place(**object_data)
    storage.new(instance)
    storage.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a Place object if exixts"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    if not request.json:
        abort(400, "Not a JSON")

    data = request.json
    for key, value in data.items():
        setattr(place, key, value)

    storage.save()

    return make_response(jsonify(place.to_dict()), 200)
