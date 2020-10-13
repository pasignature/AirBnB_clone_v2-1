#!/usr/bin/python3
""" This file sets the States view"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.base_model import BaseModel
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def list_cities(state_id):
    """ This view is for listing all the states"""
    st = storage.get("State", state_id)
    if st is None:
        return abort(404)
    lista = storage.all("City")
    ouch = []
    for items in lista.values():
        ouch.append(items.to_dict())
    return jsonify(ouch)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """ This view is for getting a specific state """
    st = storage.get("City", city_id)
    if st is None:
        return abort(404)
    st = st.to_dict()
    return jsonify(st)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """ This view allows to erase an object"""
    st = storage.get("City", city_id)
    if st is None:
        return jsonify(abort(404))
    st.delete()
    storage.save()
    dictio = {}
    return jsonify(dictio), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def post_city(state_id):
    """ This view allows to post info in the server"""
    st = storage.get("State", state_id)
    dicto = request.get_json()
    if st is None:
        return jsonify(abort(404))
    if not dicto:
        return (abort(400), 'Not a JSON')
    elif dicto.get("name") is None:
        return (abort(400), 'Missing name')
    else:
        dicto["state_id"] = state_id
        enviando = City(dicto)
        storage.new(enviando)
        storage.save()
        enviando = storage.get("City", enviando.id)
        return (jsonify(enviando.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def put_city(city_id):
    """This view sends PUT request to update info on this case"""
    enviando = storage.get("City", city_id)
    dicto = request.get_json()
    if enviando is None:
        return abort(404)
    if dicto is None:
        return abort(400), 'Not a JSON'
    for key, value in dicto.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(enviando, key, value)
    storage.save()
    return jsonify(enviando.to_dict()), 200
