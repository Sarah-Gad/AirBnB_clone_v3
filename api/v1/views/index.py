#!/usr/bin/python3
"""This is the index file for the falsk app"""

from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status", methods=['GET'], strict_slashes=False)
def getsatus():
    """This method will be called when the user access this url"""
    return jsonify({"status": "OK"})
