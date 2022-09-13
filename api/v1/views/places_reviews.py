#!/usr/bin/python3
"""Places Review API module"""
import models
from api.v1.views import app_views
from flask import jsonify, abort, request, Response, make_response
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def list_place_review(place_id):
    """Retrieves the list of all reviews objects for a given place_id"""
    object_place = storage.get('Place', place_id)
    if object_place is None:
        abort(404)
    allreviews = object_place.reviews
    reviews = []
    for obj in allreviews:
        reviews.append(obj.to_dict())

    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def fetch_review(review_id):
    """Retrieves a Review object for a given review_id"""
    object_review = storage.get('Review', review_id)
    if object_review is None:
        abort(404)
    review = object_review.to_dict()

    return jsonify(review)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object maching review_id"""
    object_review = storage.get('Review', review_id)
    if object_review is None:
        abort(404)

    storage.delete(object_review)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_place_review(place_id):
    """Create a Review object for given Place ID if method post and body
    contains json format and contains user_id and name key"""
    if not request.json:
        abort(400, "Not a JSON")
    object_place = storage.get('Place', place_id)
    if object_place is None:
        abort(404)
    object_data = request.json
    if 'user_id' not in object_data.keys():
        abort(400, "Missing user_id")
    if 'text' not in object_data.keys():
        abort(400, "Missing text")
    object_user = storage.get('User', object_data['user_id'])
    if object_user is None:
        abort(404)
    instance = Review(**object_data)
    instance.place_id = object_place.id
    storage.new(instance)
    storage.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a Review object if exixts"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)

    if not request.json:
        abort(400, "Not a JSON")

    data = request.json
    for key, value in data.items():
        if key != "id" and key != "created_at" and key != "updated_at"\
           and key != "user_id" and key != "city_id":
            setattr(review, key, value)

    storage.save()

    return make_response(jsonify(review.to_dict()), 200)
