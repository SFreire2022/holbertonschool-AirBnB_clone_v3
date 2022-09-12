#!/usr/bin/python3
"""States"""
import models
from api.v1.views import app_views
from flask import jsonify, abort, request, Response, make_response
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def list_state_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    object_state = storage.get('State', state_id)
    if object_state is None:
        abort(404)
    allcities = object_state.cities
    cities = []
    for obj in allcities:
        cities.append(obj.to_dict())

    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def fetch_city(city_id):
    """Retrieves a City object for a given id"""
    object_city = storage.get('City', city_id)
    if object_city is None:
        abort(404)
    city = object_city.to_dict()

    return jsonify(city)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a city object maching id"""
    object_city = storage.get('City', city_id)
    if object_city is None:
        abort(404)

    storage.delete(object_city)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Create a City object for given state if method post and body contains
    json format adn contains at least name key"""
    object_state = storage.get('State', state_id)
    if object_state is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    object_data = request.json
    object_data['state_id'] = state_id
    if 'name' not in object_data.keys():
        abort(400, "Missing name")
    instance = City(**object_data)
    storage.new(instance)
    storage.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update a City object if exixts"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    if not request.json:
        abort(400, "Not a JSON")

    data = request.json
    for key, value in data.items():
        setattr(city, key, value)

    storage.save()

    return make_response(jsonify(city.to_dict()), 200)
