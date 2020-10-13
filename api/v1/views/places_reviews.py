#!/usr/bin/python3
""" This file sets the States view"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def list_reviews(place_id):
    """ This view is for listing all the reviews"""
    items = storage.all("Place", place_id).items()
    if (items is None):
        return abort(404)
    ouch = []
    for item in items:
        if place_id == item['place_id']:
            ouch.append(item.to_dict())
    return jsonify(ouch)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """ This view is for getting a specific Review """
    estadito = storage.get("Review", review_id)
    if estadito is None:
        return abort(404)
    estadito = estadito.to_dict()
    return jsonify(estadito)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """ This view allows to erase an state"""
    estadito = storage.get("Review", review_id)
    if estadito is None:
        return jsonify(abort(404))
    estadito.delete()
    storage.save()
    dictio = {}
    return jsonify(dictio), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def post_review(place_id):
    """ This view allows to post info in the server"""
    place = storage.get("Place", place_id)
    if (place is None):
        return abort(404)
    if request.is_json:
        dicto = request.get_json()
    else:
        return jsonify(abort(400, 'Not a JSON'))
    if 'user_id' not in dicto:
        return jsonify(abort(400, 'Missing user_id'))
    if 'text' not in dicto:
        return jsonify(abort(400, 'Missing text'))
    enviando = Review()
    for key, value in dicto.items():
        setattr(enviando, key, value)
    storage.new(enviando)
    storage.save()
    return jsonify(enviando.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_review(review_id):
    """This view sends PUT request to update info on this case"""
    enviando = storage.get("Review", review_id)
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
