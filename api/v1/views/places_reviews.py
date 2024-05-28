#!/usr/bin/python3
"""this script contains the view for review objects"""

from flask import jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def listing_all_reviews(place_id):
    """this fucntion will list all the reviews objs"""
    tar_plc = storage.get(Place, place_id)
    if not tar_plc:
        abort(404)
    tot_revz = [oner.to_dict() for oner in tar_plc.reviews]
    return jsonify(tot_revz)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def listingone_rev(review_id):
    """this fucntion will get a specific
    review based on its id"""
    tar_rev = storage.get(Review, review_id)
    if not tar_rev:
        abort(404)
    return jsonify(tar_rev.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def removing_rev(review_id):
    """This fucntion will remove a secific
    review obj based on its id"""
    tar_rev = storage.get(Review, review_id)
    if not tar_rev:
        abort(404)
    storage.delete(tar_rev)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def addingnew_rev(place_id):
    """This fucntion will add a new
    review obj"""
    tar_plc = storage.get(Place, place_id)
    if not tar_plc:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    fetched = request.get_json()
    tar_usr = storage.get(User, fetched['user_id'])
    if not tar_usr:
        abort(404)
    if 'text' not in request.get_json():
        abort(400, description="Missing text")
    fetched['place_id'] = place_id
    new_revy = Review(**fetched)
    new_revy.save()
    return make_response(jsonify(new_revy.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def editing_rev(review_id):
    """This fucntion will edit the specific review obj"""
    tar_rev = storage.get(Review, review_id)
    if not tar_rev:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    fetched = request.get_json()
    for fk, fv in fetched.items():
        if fk not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(tar_rev, fk, fv)
    storage.save()
    return make_response(jsonify(tar_rev.to_dict()), 200)
