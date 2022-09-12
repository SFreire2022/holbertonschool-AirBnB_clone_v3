#!/usr/bin/python3
"""States"""
import models
from api.v1.views import app_views
from flask import jsonify, abort, request, Response, make_response
from models.state import State
from models import storage


@app_views.route('/states', strict_slashes=False)
def list_states():
    """Return all states using to dict"""
    allstates = storage.all('State').values()
    states = []
    for obj in allstates:
        states.append(obj.to_dict())

    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False)
def fetch_state(state_id):
    """Retrieves a State object for a given id"""
    object_state = storage.get('State', state_id)
    if object_state is None:
        abort(404)
    state = object_state.to_dict()

    return jsonify(state)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object maching id"""
    object_state = storage.get('State', state_id)
    if object_state is None:
        abort(404)

    storage.delete(object_state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a State object if method post and body contains json format"""
    if not request.json:
        abort(400, "Not a JSON")
    object_data = request.json
    if 'name' not in object_data.keys():
        abort(400, "Missing name")
    instance = State(**object_data)
    storage.new(instance)
    storage.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a State object if exixts"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    if not request.json:
        abort(400, "Not a JSON")

    data = request.json
    for key, value in data.items():
        setattr(state, key, value)

    storage.save()

    return make_response(jsonify(state.to_dict()), 200)
