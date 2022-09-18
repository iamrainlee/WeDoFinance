import logging
import json
import copy
import numpy as np

from flask import request, jsonify
import math

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/payload_shellcode', methods=['GET'])
def payload_shellcode():
    with open('/app/codeitsuisse/routes/answer_2.bin', mode='rb') as file: # b is important -> binary
        fileContent = file.read()
        return fileContent