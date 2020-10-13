#!/usr/bin/python3
""" This file sets the States view"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def list_amenities():
    """ This view is for listing all the amenities"""
    lista = storage.all("Amenity")
    ouch = []
    for items in lista.values():
        ouch.append(items.to_dict())
    return jsonify(ouch)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """ This view is for getting a specific amenity """
    estadito = storage.get("Amenity", amenity_id)
    if estadito is None:
        return abort(404)
    estadito = estadito.to_dict()
    return jsonify(estadito)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ This view allows to erase an state"""
    estadito = storage.get("Amenity", amenity_id)
    if estadito is None:
        return jsonify(abort(404))
    estadito.delete()
    storage.save()
    dictio = {}
    return jsonify(dictio), 200


@app_views.route('/amenities', methods=['POST'])
def post_amenity():
    """ This view allows to post info in the server"""
    if request.is_json:
        dicto = request.get_json()
    else:
        return jsonify(abort(400, 'Not a JSON'))
    if 'name' not in dicto:
        return jsonify(abort(400, 'Missing name'))
    enviando = Amenity(name=dicto['name'])
    storage.new(enviando)
    storage.save()
    return jsonify(enviando.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def put_amenity(amenity_id):
    """This view sends PUT request to update info on this case"""
    enviando = storage.get("Amenity", amenity_id)
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
