#!/usr/bin/python3
"""Amenities API module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, Response, make_response
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', strict_slashes=False)
def list_amenities():
    """Retrieves the list of all Amenities objects"""
    allamenities = storage.all('Amenity').values()
    amenities = []
    for obj in allamenities:
        amenities.append(obj.to_dict())

    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def fetch_amenity(amenity_id):
    """Retrieves an Amenity object for a given id"""
    object_amenity = storage.get('Amenity', amenity_id)
    if object_amenity is None:
        abort(404)
    amenity = object_amenity.to_dict()

    return jsonify(amenity)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity object maching id"""
    object_amenity = storage.get('Amenity', amenity_id)
    if object_amenity is None:
        abort(404)

    storage.delete(object_amenity)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """Create an Amenity object if method == post and body contains
    json format and contains at least name key"""
    if not request.json:
        abort(400, "Not a JSON")
    object_data = request.json
    if 'name' not in object_data.keys():
        abort(400, "Missing name")
    instance = Amenity(**object_data)
    storage.new(instance)
    storage.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Update an Amenity object if exixts"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)

    if not request.json:
        abort(400, "Not a JSON")

    data = request.json
    for key, value in data.items():
        setattr(amenity, key, value)

    storage.save()

    return make_response(jsonify(amenity.to_dict()), 200)
