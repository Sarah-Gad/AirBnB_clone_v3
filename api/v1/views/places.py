#!/usr/bin/python3
"""this script contains the view for place objects"""

from flask import jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.user import User
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def listing_places(city_id):
    """this function will list all the places objs"""
    tar_ct = storage.get(City, city_id)
    if tar_ct is None:
        abort(404)
    tot_plcz = tar_ct.places
    return jsonify([onep.to_dict() for onep in tot_plcz])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def listingone_plc(place_id):
    """this method will get a specific
    place obj based it its id"""
    tar_plc = storage.get(Place, place_id)
    if tar_plc is None:
        abort(404)
    return jsonify(tar_plc.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def removing_plc(place_id):
    """this fucntion will remove the specifi
    plc pbj based on its id"""
    tar_plc = storage.get(Place, place_id)
    if tar_plc is None:
        abort(404)
    storage.delete(tar_plc)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def makingnw_plc(city_id):
    """this fucntion will create a new plc pbj"""
    tar_ct = storage.get(City, city_id)
    if tar_ct is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    fetched = request.get_json()
    tar_usr = storage.get(User, fetched['user_id'])
    if tar_usr is None:
        abort(404)
    if 'name' not in fetched:
        abort(404)
    fetched['city_id'] = city_id
    newly_created = Place(**fetched)
    newly_created.save()
    return make_response(jsonify(newly_created.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def editing_plc(place_id):
    """this fucntion will edit the plc obj"""
    tar_plc = storage.get(Place, place_id)
    if tar_plc is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    fetched = request.get_json()
    for fk, fv in fetched.items():
        if fk not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(tar_plc, fk, fv)
    storage.save()
    return make_response(jsonify(tar_plc.to_dict()), 200)
