import logging
import json
import copy
import numpy as np

from flask import request, jsonify
from math import gcd

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/stig/full', methods=['POST'])
def stigfull():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for i in data:
        result.append(calculatestigfull(i['questions'],i['maxRating'],i['lucky']))
    
    logging.info("result: {}".format(result))
    return json.dumps(result)

def calculatestigfull(questions,maxRating,lucky):
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
    min_val = -1
    correct =  set()
    p = -1
    q1 = -1
    # min_list = set()
    max_list = set()
    for q in questions:
        if p == -1:
            correct.add(q['lower'])
            if q['lower'] != 1:
                correct.add(1)
            else:
                correct.add(q['upper']+1)
            p = 2 // gcd(2,maxRating)
            q1 = maxRating // gcd(2,maxRating)
            max_list.add(q['upper'])
            # min_list.add(q['from'])
            if q["lower"] == 1:
                min_val = q["upper"] + 1
            else:
                min_val = 1
            continue
        f = (q['lower'] + p*lucky -1)%(maxRating)+1
        t = (q['upper'] + p*lucky -1)%(maxRating)+1
        if f>t:
            temp = f
            f = t
            t = temp
        correct.add(f)
        for i in list(max_list):
            if i >f and i<t:
                correct.add(i+1)
        if f == 1 or min_val != 1:
            if min_val >= f:
                min_val = t + 1
        correct.add(min_val)
        max_list.add(t)
        # min_list.add(f)
        p = len(correct) // gcd(len(correct),maxRating)
        q1 = maxRating // gcd(len(correct),maxRating)
    # for i in range(1,maxRating+1):
    #     possible_guesses = list(range(1,maxRating+1))
    #     for q in questions:
    #         if (i >= q["from"] and i <= q["to"]):
    #             possible_guesses = [x for x in possible_guesses if x >= q["from"] and x <= q["to"]]
    #         else:
    #             possible_guesses = [x for x in possible_guesses if x < q["from"] or x > q["to"]]
    #     if (i == min(possible_guesses)):
    #         count += 1
    # d = gcd(count, maxRating)
 
    return {"p": p, "q": q1}

    


