import logging
import json
import copy
import numpy as np

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/rubiks', methods=['POST'])
def rubiks():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    ops = data.get('ops')
    state = data.get('state')
    for i in state:
        state[i] = np.array(state[i])
    while True:
        if len(ops) == 0:
            break
        if len(ops) > 1 and ops[1] == 'i':
            state = turnrubiks(state,ops[0:1])
            ops = ops[2:]
        else:
            state = turnrubiks(state,ops[0])
            ops = ops[1:]
    for i in state:
        state[i] = state[i].tolist()
    logging.info("result: {}".format(state))
    return json.dumps({'output':state})

def turnrubiks(state,ops):
    if len(ops) == 1:
        state[ops.lower()] =  rotate(state[ops.lower()])
    else:
        state[ops[0].lower()] =  antirotate(state[ops[0].lower()])
    if ops == "U":
        temp = copy.deepcopy(state['l'][0])
        state['l'][0] = state['f'][0]
        state['f'][0] = state['r'][0]
        state['r'][0] = state['b'][0]
        state['b'][0] = temp
        return state
    if ops == "Ui":
        temp = copy.deepcopy(state['f'][0])
        state['f'][0] = state['l'][0]
        state['l'][0] = state['b'][0]
        state['b'][0] = state['r'][0]
        state['r'][0] = temp
        return state
    if ops == "Ui":
        temp = copy.deepcopy(state['f'][0])
        state['f'][0] = state['l'][0]
        state['r'][0] = state['f'][0]
        state['b'][0] = state['r'][0]
        state['r'][0] = temp
        return state
    if ops == "L":
        temp = copy.deepcopy(state['u'][:,0])
        state['u'][:,0] = state['b'][:,2]
        state['b'][:,2] = state['d'][:,0]
        state['d'][:,0] = state['f'][:,0]
        state['f'][:,0] = temp
        return state
    if ops == "Li":
        temp = copy.deepcopy(state['u'][:,0])
        state['u'][:,0] = state['f'][:,0]
        state['f'][:,0] = state['d'][:,0]
        state['d'][:,0] = state['b'][:,2]
        state['b'][:,2] = temp
        return state
    if ops == "F":
        temp = copy.deepcopy(state['u'][2])
        state['u'][2] = state['l'][:,2]
        state['l'][:,2] = state['d'][0]
        state['d'][0] = state['r'][:,0]
        state['r'][:,0] = temp
        return state
    if ops == "Fi":
        temp = copy.deepcopy(state['u'][2])
        state['u'][2] = state['r'][:,0]
        state['r'][:,0] = state['d'][0]
        state['d'][0] = state['l'][:,2]
        state['l'][:,2] = temp
        return state
    if ops == "R":
        temp = copy.deepcopy(state['u'][:,2])
        state['u'][:,2] = state['f'][:,2]
        state['f'][:,2] = state['d'][:,2]
        state['d'][:,2] = state['b'][:,0]
        state['b'][:,0] = temp
        return state
    if ops == "Ri":
        temp = copy.deepcopy(state['u'][:,2])
        state['u'][:,2] = state['b'][:,0]
        state['b'][:,0] = state['d'][:,2]
        state['d'][:,2] = state['f'][:,0]
        state['f'][:,0] = temp
        return state
    if ops == "B":
        temp = copy.deepcopy(state['u'][0])
        state['u'][0] = state['r'][:,2]
        state['r'][:,2] = state['d'][2]
        state['d'][2] = state['l'][:,0]
        state['l'][:,0] = temp
        return state
    if ops == "Bi":
        temp = copy.deepcopy(state['u'][0])
        state['u'][0] = state['l'][:,0]
        state['l'][:,0] = state['d'][2]
        state['d'][2] = state['r'][:,2]
        state['r'][:,2] = temp
        return state
    if ops == "D":
        temp = copy.deepcopy(state['f'][2])
        state['f'][2] = state['l'][2]
        state['l'][2] = state['b'][2]
        state['b'][2] = state['r'][2]
        state['r'][2] = temp
        return state
    if ops == "Di":
        temp = copy.deepcopy(state['f'][2])
        state['f'][2] = state['r'][2]
        state['r'][2] = state['b'][2]
        state['b'][2] = state['l'][2]
        state['l'][2] = temp
        return state
def rotate(s):
    return np.array([[s[2][0],s[1][0],s[0][0]],[s[2][1],s[1][1],s[1][0]],[s[2][2],s[1][2],s[0][2]]])

def antirotate(s):
    return np.array([[s[0][2],s[1][2],s[2][2]],[s[0][1],s[1][1],s[2][1]],[s[0][0],s[1][0],s[2][0]]])
