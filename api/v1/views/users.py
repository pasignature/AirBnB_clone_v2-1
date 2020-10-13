#!/usr/bin/python3
""" This file sets the States view"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def list_users():
    """ This view is for listing all the amenities"""
    lista = storage.all("User")
    ouch = []
    for items in lista.values():
        ouch.append(items.to_dict())
    return jsonify(ouch)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """ This view is for getting a specific amenity """
    estadito = storage.get("User", user_id)
    if estadito is None:
        return abort(404)
    estadito = estadito.to_dict()
    return jsonify(estadito)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ This view allows to erase an state"""
    estadito = storage.get("User", user_id)
    if estadito is None:
        return jsonify(abort(404))
    estadito.delete()
    storage.save()
    dictio = {}
    return jsonify(dictio), 200


@app_views.route('/users', methods=['POST'])
def post_user():
    """ This view allows to post info in the server"""
    if request.is_json:
        dicto = request.get_json()
    else:
        return jsonify(abort(400, 'Not a JSON'))
    if 'email' not in dicto:
        abort(400, 'Missing email')
    if 'password' not in dicto:
        abort(400, 'Missing password')

    enviando = User()
    for key, value in dicto.items():
        setattr(enviando, key, value)
    storage.new(enviando)
    storage.save()
    return jsonify(enviando.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def put_user(user_id):
    """This view sends PUT request to update info on this case"""
    enviando = storage.get("User", user_id)
    if enviando is None:
        return abort(404)
    if request.is_json:
        dicto = request.get_json()
    else:
        return jsonify(abort(400, 'Not a JSON'))
    for key, value in dicto.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(enviando, key, value)
    storage.save()
    return jsonify(enviando.to_dict()), 200
