#!/usr/bin/python3
"""Users API module"""
import models
from api.v1.views import app_views
from flask import jsonify, abort, request, Response, make_response
from models.user import User
from models import storage


@app_views.route('/users', strict_slashes=False)
def list_users():
    """Return all Users using to dict"""
    allusers = storage.all('User').values()
    users = []
    for obj in allusers:
        users.append(obj.to_dict())

    return jsonify(users)


@app_views.route('/users/<user_id>', strict_slashes=False)
def fetch_user(user_id):
    """Retrieves a User object for a given id"""
    object_user = storage.get('User', user_id)
    if object_user is None:
        abort(404)
    user = object_user.to_dict()

    return jsonify(user)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object maching id"""
    object_user = storage.get('User', user_id)
    if object_user is None:
        abort(404)

    storage.delete(object_user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a User object if method post and body contains json format"""
    if not request.json:
        abort(400, "Not a JSON")
    object_data = request.json
    if 'password' not in object_data.keys():
        abort(400, "Missing password")
    if 'email' not in object_data.keys():
        abort(400, "Missing email")
    instance = User(**object_data)
    storage.new(instance)
    storage.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update a User object if exixts"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    if not request.json:
        abort(400, "Not a JSON")

    data = request.json
    for key, value in data.items():
        setattr(user, key, value)

    storage.save()

    return make_response(jsonify(user.to_dict()), 200)
