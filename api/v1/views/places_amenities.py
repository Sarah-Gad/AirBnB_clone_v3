#!/usr/bin/python3
""" this script contains the the relatio
between Place objects and Amenity objects"""
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from os import environ
from flask import abort, jsonify, make_response, request


@app_views.route('places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def listingall_amens(place_id):
    """This fucntion will list all the amenity objs
    in a specific place"""
    tar_plc = storage.get(Place, place_id)
    if not tar_plc:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        tot_amens = [oneam.to_dict() for oneam in tar_plc.amenities]
    else:
        tot_amens = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in tar_plc.amenity_ids]
    return jsonify(tot_amens)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def removing_anem(place_id, amenity_id):
    """This fucntio removes a specific anemity
    form a specicif place"""
    tar_plc = storage.get(Place, place_id)
    if not tar_plc:
        abort(404)
    tar_amen = storage.get(Amenity, amenity_id)
    if not tar_amen:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if tar_amen not in tar_plc.amenities:
            abort(404)
        tar_plc.amenities.remove(tar_amen)
    else:
        if amenity_id not in tar_plc.amenity_ids:
            abort(404)
        tar_plc.amenity_ids.remove(amenity_id)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def relation(place_id, amenity_id):
    """This fucntion will link a specific anem
    to a specific place"""
    tar_plc = storage.get(Place, place_id)
    if not tar_plc:
        abort(404)
    tar_amen = storage.get(Amenity, amenity_id)
    if not tar_amen:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if tar_amen in tar_plc.amenities:
            return make_response(jsonify(tar_amen.to_dict()), 200)
        else:
            tar_plc.amenities.append(tar_amen)
    else:
        if amenity_id in tar_plc.amenity_ids:
            return make_response(jsonify(tar_amen.to_dict()), 200)
        else:
            tar_plc.amenity_ids.append(amenity_id)
    storage.save()
    return make_response(jsonify(tar_amen.to_dict()), 201)
