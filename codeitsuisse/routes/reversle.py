import logging
import json
import copy
import numpy as np
import random

from flask import request, jsonify, Response

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/reversle', methods=['POST'])
def reversle():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    equationLength = data.get("equationLength")
    attemptsAllowed = data.get("attemptsAllowed")
            
    if "equationHistory" not in data:
        possibles = generate_possibles(equationLength)
        while len(possibles) == 0:
            possibles = generate_possibles(equationLength)
        result = random.choice(possibles)
    else:
        d = [0,1,2,3,4,5,6,7,8,9]
        s = ["+","-", "*", "/", "\\", "^" ]
        poss = [""] * equationLength
        equationHistory = data.get("equationHistory")
        resultHistory = data.get("resultHistory")
        ans_length = -1
        equal_sign = -1
        ans_lens = []
        for i in range(len(equationHistory)):
            ans_lens.append(equationLength - equationHistory[i].index("=") - 1)
            if(resultHistory[i][equationHistory[i].index("=")] == "2"):
                ans_length = equationLength - equationHistory[i].index("=") - 1
                equal_sign = equationHistory[i].index("=")
        if ans_length > 0:
            for i in range(len(equationHistory)):
                for j in range(len(equationHistory[i])):
                    if resultHistory[i][j] == "2":
                        poss[j] = equationHistory[i][j]
                    if resultHistory[i][j] == "0":
                        if equationHistory[i][j].isnumeric(): if int(equationHistory[i][j]) in d: d.remove(int(equationHistory[i][j]))
                        if equationHistory[i][j] in s: s.remove(equationHistory[i][j])
        if poss.count("") >= equationLength // 2 :
            if ans_length == -1:
                logging.info("equals not found, d: {},s: {}".format(d,s))
                poss_ans_length = []
                if (min(ans_lens)-1>=1 and (equationLength - min(ans_lens) - 2)%2 == 1):
                    poss_ans_length.append(min(ans_lens)-1)
                if (max(ans_lens)+1>=1 and (equationLength - max(ans_lens) )%2 == 1):
                    poss_ans_length.append(max(ans_lens)+1)
                ans_length = random.choice(poss_ans_length)
                if len(poss_ans_length) == 0:
                    if (min(ans_lens)-2>=1 and (equationLength - min(ans_lens) - 3)%2 == 1):
                        poss_ans_length.append(min(ans_lens)-2)
                    if (max(ans_lens)+2>=1 and (equationLength - max(ans_lens) +1 )%2 == 1):
                        poss_ans_length.append(max(ans_lens)+2)
                    ans_length = random.choice(poss_ans_length)
                possibles = generate_possibles_fixed_length(equationLength,ans_length,d,s)
                while len(possibles) == 0:
                    possibles = generate_possibles_fixed_length(equationLength,ans_length,d,s)
                result = random.choice(possibles)
            else:
                logging.info("equals found, ans_length:{}, d: {},s: {}".format(ans_length,d,s))
                possibles = generate_possibles_fixed_length(equationLength,ans_length,d,s)
                while len(possibles) == 0:
                    possibles = generate_possibles_fixed_length(equationLength,ans_length,d,s)
                result = random.choice(possibles)
        else:
            logging.info("near to answer, ans_length:{}, d: {},s: {}".format(ans_length,d,s))
            tries = []
            for i in range(equal_sign):
                if poss[i] == "":
                    if i == 1 or i%2 == 0:
                        for a in d:
                            temp = poss[:]
                            temp[i] = a
                            tries.append(temp)
                    else:
                        for a in s:
                            temp = poss[:]
                            temp[i] = a
                            tries.append(temp)
                    poss[i] = " "
                    break
            for i in range(equal_sign):
                if poss[i] == "":
                    tries_temp = []
                    if i == 1 or i%2 == 0:
                        for t in tries:
                            for a in d:
                                temp = t[:]
                                temp[i] = a
                                tries.append(temp)
                    else:
                        for t in tries:
                            for a in s:
                                temp = t[:]
                                temp[i] = a
                                tries.append(temp)
                    tries = tries_temp[:]
            for i in range(equal_sign+1,equationLength):
                if poss[i] == "":
                    tries_temp = []
                    for t in tries:
                        for a in d:
                            temp = t[:]
                            temp[i] = a
                            tries.append(temp)
                    tries = tries_temp[:]
            pos_tries = []
            for t in tries:
                ans = int(''.join(tries[equal_sign+1:]))
                if valid(d,ans):
                    temp = []
                    for a in d:
                        temp.append(str(a))
                    temp.append("=")
                    temp.extend(list(str(ans)))      
                    pos_tries.append(temp)
            result = random.choice(pos_tries)
            
                
    logging.info("result: {}".format(result))
    return Response(json.dumps({"equation":result}), mimetype='application/json')

def valid(digits, ans):
    if (len(digits) == 1):
        return round(digits[0],3) == ans
    if (digits[2] == "+"):
        return valid([digits[0] + digits[1]] + digits[3:],ans)
    if (digits[2] == "-"):
        return valid([digits[0] - digits[1]] + digits[3:],ans)
    if (digits[2] == "*"):
        return valid([digits[0] * digits[1]] + digits[3:],ans)
    if (digits[2] == "/"):
        if (digits[1] == 0):
            return False
        return valid([digits[0] / digits[1]] + digits[3:],ans)
    if (digits[2] == "\\"):
        if (digits[0] == 0):
            return False
        return valid([digits[1] / digits[0]] + digits[3:],ans)
    if (digits[2] == "^"):
        return valid([digits[0] ** digits[1]] + digits[3:],ans)
    return []

def generate_possibles(equationLength):
    possibilities = []
    
    anses = [random.randint(1,10**(equationLength//3)-1),random.randint(1,10**(equationLength//3)-1)]
    for ans in anses:
        remaining = equationLength - len(str(ans)) - 1

        for j in range(1,remaining-1):
            if j != remaining - j - 1:
                continue
            digits = [[1],[2],[3],[4],[5],[6],[7],[8],[9]]
            for z in range(j):
                r = []
                for k in range(0,10):
                    for d in digits:
                        r.append(d[:]+[k])
                digits = r[:]
                r = []
                for d in digits:
                    if len(d) >= 2:
                        for l in ["+","-", "*", "/", "\\", "^" ]:
                            r.append(copy.deepcopy(d)+[l])
                        digits = r[:]
            for d in digits:
                if valid(d,ans):
                    temp = []
                    for a in d:
                        temp.append(str(a))
                    temp.append("=")
                    temp.extend(list(str(ans)))      
                    possibilities.append(temp)
    return possibilities

def generate_possibles_fixed_length(equationLength,ans_length,di,s):
    possibilities = []
    anses = []
    while len(anses) < 2:
        a = random.randint(10**(ans_length-1),10**ans_length-1)
        for i in str(a):
            if int(i) not in di:
                continue
        anses.append(a)
    for ans in anses:
        remaining = equationLength - len(str(ans)) - 1

        for j in range(1,remaining-1):
            if j != remaining - j - 1:
                continue
            digits = []
            for abc in di:
                digits.append([abc])
            for z in range(j):
                r = []
                for k in di:
                    for d in digits:
                        r.append(d[:]+[k])
                digits = r[:]
                r = []
                for d in digits:
                    if len(d) >= 2:
                        for l in s:
                            r.append(copy.deepcopy(d)+[l])
                        digits = r[:]
            for d in digits:
                if valid(d,ans):
                    temp = []
                    for a in d:
                        temp.append(str(a))
                    temp.append("=")
                    temp.extend(list(str(ans)))      
                    possibilities.append(temp)
    return possibilities