#!/usr/bin/python3
"""this script contains the view for amenity objects"""

from flask import Flask, jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def listing_all_amens():
    """this fucntion will list all of the amenity objs"""
    tot_anems = storage.all(Amenity).values()
    amens_ls = []
    for onea in tot_anems:
        amens_ls.append(onea.to_dict())
    return jsonify(amens_ls)


@app_views.route(
        '/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def listingone_amen(amenity_id):
    """this fucntion will get a specific
    amenity based on its id"""
    target_amen = storage.get(Amenity, amenity_id)
    if not target_amen:
        abort(404)
    return jsonify(target_amen.to_dict())


@app_views.route(
        '/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def removing_amen(amenity_id):
    """this fucntion will remove a specific anemity obj"""
    target_amen = storage.get(Amenity, amenity_id)
    if not target_amen:
        abort(404)
    storage.delete(target_amen)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def making_new_amen():
    """this fucntion will create a new anemity obj"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    fetched= request.get_json()
    new_amen = Amenity(**fetched)
    new_amen.save()
    return make_response(jsonify(new_amen.to_dict()), 201)


@app_views.route(
        '/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def editing_amen(amenity_id):
    """this fucntion will edit the anemity obj"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    tar_amen = storage.get(Amenity, amenity_id)
    if not tar_amen:
        abort(404)
    fetched = request.get_json()
    for fk, fv in fetched.items():
        if fk not in ['id', 'created_at', 'updated_at']:
            setattr(tar_amen, fk, fv)
    storage.save()
    return make_response(jsonify(tar_amen.to_dict()), 200)
