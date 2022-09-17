import logging
import json
import copy
import numpy as np
import flask

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/travelling-suisse-robot', methods=['POST'])
def travellingsuisserobot():
    data = request.get_data()
    logging.info("data sent for evaluation {}".format(data))


    result = "SSPSSPSSPRSSSSSSPSSSSSSSPRSSSSPSSSSPRSSSSSPSSSSSSPSSSSSSSSPSSSSPSSP"
    resp = flask.Response(result)
    resp.headers['Content-Type'] = 'text/plain'
    return resp