import logging
import json
import copy
import numpy as np

from flask import request, jsonify
import math

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/payload_stack', methods=['GET'])
def payload_stack():
    with open('/app/codeitsuisse/routes/payload', mode='rb') as file: # b is important -> binary
        fileContent = file.read()
        return fileContent