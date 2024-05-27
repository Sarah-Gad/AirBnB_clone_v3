#!/usr/bin/python3
"""this script is contains the view for State objects"""

from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def listing_allsts():
    """This function will list alll the state objs"""
    tot_sts = storage.all(State).values()
    return jsonify([onest.to_dict() for onest in tot_sts])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def listing_one_state(state_id):
    """This fucntion will git one state based on its id"""
    target = storage.get(State, state_id)
    if target is None:
        abort(404)
    return jsonify(target.to_dict())


@app_views.route(
        '/states/<state_id>',
        methods=['DELETE'],
        strict_slashes=False)
def removing_st(state_id):
    """This fucntion wiil rrmove the state based on its id"""
    target = storage.get(State, state_id)
    if target is None:
        abort(404)
    storage.delete(target)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def addingnew_st():
    """This fucntion will add a new st"""
    fetched = request.get_json()
    if not fetched:
        abort(400, description="Not a JSON")
    if 'name' not in fetched:
        abort(400, description="Missing name")
    newly_made = State(**fetched)
    storage.new(newly_made)
    storage.save()
    return jsonify(newly_made.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def editing_st(state_id):
    """This function will edit the specific state"""
    target = storage.get(State, state_id)
    if target is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    fetched = request.get_json()
    for fk, fv in fetched.items():
        if fk not in ['id', 'created_at', 'updated_at']:
            setattr(target, fk, fv)
    storage.save()
    return jsonify(target.to_dict()), 200
