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
    data = request.get_data().decode('utf-8')
    logging.info("data sent for evaluation {}".format(data))
    grid = np.asarray(makegrid(data))
    grids = []
    e_grids = []
    i_grids = []
    s_grids = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "E":
                e_grids.append([i,j])
            if grid[i][j] == "I":
                i_grids.append([i,j])
            if grid[i][j] == "S":
                s_grids.append([i,j])
    for e in range(2):
        for i in range(2):
            for s in range(3):
                for s2 in range(2):
                    s2_grid = [x for x in s_grids if x != s_grids[s]]
                    temp = copy.deepcopy(grid)
                    temp[e_grids[e][0]][e_grids[e][1]] = "1"
                    temp[i_grids[i][0]][i_grids[i][1]] = "2"
                    temp[s_grids[s][0]][s_grids[s][1]] = "3"
                    temp[s2_grid[s2][0]][s2_grid[s2][1]] = "4"
                    grids.append(temp)
                    
    min_count = -1
    final_result = ""
    for j in grids:
        x = np.where(j=="X")
        x = [x[0][0],x[1][0]]
        x_facing = 0 # 0: TOP, 1: RIGHT, 2: BOTTOM, 3: LEFT
        count = 0
        result = ""
        for i in "COD12T3UI4SE": #"CODEITSUISSE"
            cur = np.where(j==i)
            cur = [cur[0][0],cur[1][0]]
            if (x[0] - cur[0])>0:
                result += turnto(x_facing,0)
                x_facing = 0
            elif (x[0] - cur[0])<0:
                result += turnto(x_facing,2)
                x_facing = 2
            result += "S" * abs(x[0] - cur[0])
            count += abs(x[0] - cur[0])
            if (x[1] - cur[1])>0:
                result += turnto(x_facing,3)
                x_facing = 3
            elif (x[1] - cur[1])<0:
                result += turnto(x_facing,1)
                x_facing = 1
            result += "S" * abs(x[1] - cur[1])
            count += abs(x[1] - cur[1])
            result += "P"
            j[cur[0]][cur[1]] = " "
            x = cur
        if min_count == -1  or count < min_count:
            final_result = result
            min_count = count

    logging.info("result: {}".format(final_result))
    resp = flask.Response(final_result)
    resp.headers['Content-Type'] = 'text/plain'
    return resp

def makegrid(data):
    data = data.split("\n")
    data = data[1:-2]
    grid = []
    for i in data:
        grid.append(list(i[1:-1]))
    return grid
def turnto(cur, target):
    if cur == target:
        return ""
    if cur-target <=2 and cur-target >= 0:
        return "L"*(cur-target)
    if cur-target < 0 and cur-target >=-2:
        return "R"*abs(cur-target)
    if cur-target == 3:
        return "R"
    if cur-target == -3:
        return "L"