#!/usr/bin/python3
"""Create a new view for User object that handles all default RestFul API"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def retr_users():
    """retrieve the list of all users objects"""
    users = []
    for user in storage.all("User").values():
        users.append(user.to_dict())
    return jsonify(user)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def retr_user(user_id):
    """retrieve a specific user object"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delet_user(user_id):
    """deletes an object user based on its user_id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def creat_user():
    """create a new user object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({'error': 'Missing password'}), 400)
    user = User(**request.get_json())
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def reupdat_user(user_id):
    """update an exist object user"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for k, val in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(user, k, val)
    user.save()
    return jsonify(user.to_dict())
