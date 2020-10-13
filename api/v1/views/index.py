#!/usr/bin/python3
""" This file sets two main routes for the blueprint mechanism"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """This route returns a json codified message """
    return jsonify(status="OK")


@app_views.route('/stats')
def stats():
    """This route returns a json codified message """
    return jsonify(amenities=storage.count("Amenity"),
                   reviews=storage.count("Review"),
                   states=storage.count("State"),
                   users=storage.count("User"), places=storage.count("Place"))
