#!/usr/bin/python3
""" This file sets the States view"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def list_places(city_id):
    """ This view is for listing all the amenities"""
    city = storage.get("City", city_id)
    if (city is None):
        abort(404)
    items = storage.all("Place").items()
    ouch = []
    for item in items:
        if city_id == item['city_id']:
            ouch.append(item.to_dict())
    return jsonify(ouch)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """ This view is for getting a specific Place """
    estadito = storage.get("Place", place_id)
    if estadito is None:
        return abort(404)
    estadito = estadito.to_dict()
    return jsonify(estadito)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """ This view allows to erase an state"""
    estadito = storage.get("Place", place_id)
    if estadito is None:
        return jsonify(abort(404))
    estadito.delete()
    storage.save()
    dictio = {}
    return jsonify(dictio), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def post_place():
    """ This view allows to post info in the server"""
    city = storage.get("City", city_id)
    if (city is None):
        abort(404)
    if request.is_json:
        dicto = request.get_json()
    else:
        return jsonify(abort(400, 'Not a JSON'))
    if 'name' not in dicto:
        return jsonify(abort(400, 'Missing name'))
    if 'user_id' not in dicto:
        return jsonify(abort(400, 'Missing name'))
    user = storage.get("User", dicto.get('user_id'))
    if (user is None):
        abort(404)
    enviando = Place()
    for key, value in dicto.items():
        setattr(enviando, key, value)
    storage.new(enviando)
    storage.save()
    return jsonify(enviando.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def put_place(place_id):
    """This view sends PUT request to update info on this case"""
    enviando = storage.get("Place", place_id)
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
