#!/usr/bin/python3
"""this script contains the view for amenity objects"""

from flask import Flask, jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def listing_all_amens():
    """this fucntion will list all of the amenity objs"""
    tot_amen = storage.all(Amenity).values()
    return jsonify([oneam.to_dict() for oneam in tot_amen])


@app_views.route(
        '/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def listingone_amen(amenity_id):
    """this fucntion will get a specific
    amenity based on its id"""
    target_amen = storage.get(Amenity, amenity_id)
    if target_amen is None:
        abort(404)
    return jsonify(target_amen.to_dict())


@app_views.route(
        '/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def removing_amen(amenity_id):
    """this fucntion will remove a specific anemity obj"""
    target_amen = storage.get(Amenity, amenity_id)
    if target_amen is None:
        abort(404)
    storage.delete(target_amen)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def making_new_amen():
    """this fucntion will create a new anemity obj"""
    fetched = request.get_json()
    if not fetched:
        abort(400, description='Not a JSON')
    if 'name' not in fetched:
        abort(400, description='Missing name')
    newly_created = Amenity(**fetched)
    storage.save()
    return make_response(jsonify(newly_created.to_dict()), 201)


@app_views.route(
        '/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def editing_amen(amenity_id):
    """this fucntion will edit the anemity obj"""
    target_amen = storage.get(Amenity, amenity_id)
    if target_amen is None:
        abort(404)
    fetched = request.get_json()
    if not fetched:
        abort(400, description='Not a JSON')
    for fk, fv in fetched.items():
        if fk not in ['id', 'created_at', 'updated_at']:
            setattr(target_amen, fk, fv)
    storage.save()
    return make_response(jsonify(target_amen.to_dict()), 200)
