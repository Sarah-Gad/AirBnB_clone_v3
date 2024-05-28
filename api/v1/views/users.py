#!/usr/bin/python3
"""this script contains the view for user objects"""

from flask import Flask, jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def listing_users():
    """this function will list all usersss"""
    tot_usrz = storage.all(User).values()
    return jsonify([oneu.to_dict() for oneu in tot_usrz])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def listingone_user(user_id):
    """this fucntion will get a specific
    user based on its id"""
    target_u = storage.get(User, user_id)
    if target_u is None:
        abort(404)
    return jsonify(target_u.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def removing_user(user_id):
    """this fucntion will remove a specific
    user based on his/her id"""
    tar_u = storage.get(User, user_id)
    if tar_u is None:
        abort(404)
    storage.delete(tar_u)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def makingnew_user():
    """this fucntion will create a new user obj"""
    fetched = request.get_json()
    if fetched is None:
        abort(400, description="Not a JSON")
    if 'email' not in fetched:
        abort(400, description="Missing email")
    if 'password' not in fetched:
        abort(400, description="Missing password")
    newly_created = User(**fetched)
    storage.save()
    return make_response(jsonify(newly_created.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def editing_user(user_id):
    """this function will edit the user
    obj based on his/her id"""
    tar_u = storage.get(User, user_id)
    if tar_u is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    fetched = request.get_json()
    for fk, fv in fetched.items():
        if fk not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(tar_u, fk, fv)
    storage.save()
    return make_response(jsonify(tar_u.to_dict()), 200)
