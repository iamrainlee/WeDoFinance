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
    correct =  dict.fromkeys(questions, 0)
    min_val = list(range(1,maxRating+1))
    p = -1
    q = -1
    min_list = set()
    max_list = set()
    for q in questions:
        if p == -1:
            correct[q['from']] = 1
            if q['from'] != 1:
                correct[1] = 1
            else:
                correct[q['to']+1] = 1
            p = 2 // gcd(2,maxRating)
            q = maxRating // gcd(2,maxRating)
            max_list.add(q['to'])
            min_list.add(q['from'])
            min_val = [x for x in min_val if x < q["from"] or x > q["to"]]
            continue
        f = (q['from'] + p*lucky)%(maxRating-1)+1
        t = (q['to'] + p*lucky)%(maxRating-1)+1
        if f>t:
            temp = f
            f = t
            t = temp
        correct[f] = 1
        for i in list(max_list):
            if i >f and i<t:
                correct[i+1] = 1
        min_val = [x for x in min_val if x < f or x > t]
        correct[min_val] = 1
        max_list.add(t)
        min_list.add(f)
        count = sum(value == 1 for value in correct.values())
        p = count // gcd(count,maxRating)
        q = maxRating // gcd(count,maxRating)
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
 
    return {"p": p, "q": q}

    


