#!/usr/bin/python3
"""this script contains the view for city objects"""

from flask import Flask, jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.state import State
from models.state import City

@app_views.route(
    '/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def listing_ctzz(state_id):
    """This fucntion will list all the cities in the state"""
    tar_stat = storage.get(State, state_id)
    if tar_stat is None:
        abort(404)
    allctzz = tar_stat.cities
    return jsonify([onec.to_dict() for onec in allctzz])


@app_views.route(
    '/cities/<city_id>', methods=['GET'], strict_slashes=False)
def listingone_city(city_id):
    """Get City obj through passed IDthis fucntion will get the city 
    based on its id"""
    tar_ct = storage.get(City, city_id)
    if tar_ct is None:
        abort(404)
    return jsonify(tar_ct.to_dict())


@app_views.route(
    '/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def removing_ct(city_id):
    """this fucntion will remove the specific city ob"""
    tar_ct = storage.get(City, city_id)
    if tar_ct is None:
        abort(404)
    tar_ct.delete()
    tar_ct.save()
    return make_response(jsonify({}), 200)


@app_views.route(
    '/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def addingnw_ct(state_id):
    """ this fucntion will add a new city obj"""
    tar_st = storage.get(State, state_id)
    if tar_st is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    fetched = request.get_json()
    if 'name' not in fetched:
        abort(400, description="Missing name")
    fetched['state_id']= state_id
    newly_made = City(**fetched)
    storage.save()
    return make_response(jsonify(newly_made.to_dict()), 201)


@app_views.route(
    '/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def editing_ct(city_id):
    """this fucntion will edit the city
    obj based on its id"""
    tar_ct= storage.get(City, city_id)
    if tar_ct is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    fetched = request.get_json()
    for fk, fv in fetched.items():
        if fk not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(tar_ct, fk, fv)
    tar_ct.save()
    return make_response(jsonify(tar_ct.to_dict()), 200)
