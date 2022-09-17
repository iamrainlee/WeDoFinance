import logging
import json
import copy
import numpy as np

from flask import request, jsonify
from math import gcd

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/stig/warmup', methods=['POST'])
def stigwarmup():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for i in data:
        result.append(calculatestig(i['questions'],i['maxRating']))
    
    logging.info("result: {}".format(result))
    return json.dumps(result)

def calculatestig(questions,maxRating):
    questions = list(set(questions))
    questions = sorted(questions, key=lambda d: d['lower']) 
    # l_accurate = []
    # count = 0
    # min_l = -1
    # max_l = -1
    # for i in questions:
    #     if (i['lower']  < min_l):
    #         min_l = i['lower']
    #     if (i['upper'] == 2 > max_l):
    #         l_accurate.append(1)
    #         count += 1
    count = 0
    for i in range(1,maxRating+1):
        possible_guesses = list(range(1,maxRating+1))
        for q in questions:
            if (i >= q["lower"] and i <= q["higher"]):
                possible_guesses = [x for x in possible_guesses if x >= q["lower"] and x <= q["higher"]]
            else:
                possible_guesses = [x for x in possible_guesses if x < q["lower"] or x > q["higher"]]
        if (i == min(possible_guesses)):
            count += 1
    d = gcd(count, maxRating)
 
    return {"p": count // d, "q": maxRating // d}
    


