import logging
import json
import copy
import numpy as np

from flask import request, jsonify
import math

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/social-distancing', methods=['POST'])
def socialdistancing():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for i in data:
        result.append(calsocialdistancing(i))
    
    logging.info("result: {}".format(result))
    return json.dumps(result)

def getDistance(grid,h,w):
    if h>0:
        grid[h-1][w] = "N"
    if w>0:
        grid[h][w-1] = "N"
    if w>0 and h>0:
        grid[h-1][w-1] = "N"
    if h<len(grid)-1:
        grid[h+1][w] = "N"
    if w<len(grid[0])-1:
        grid[h][w+1] = "N"
    if h<len(grid)-1 and w<len(grid[0])-1:
        grid[h+1][w+1] = "N"
    if h>0 and w<len(grid[0])-1:
        grid[h-1][w+1] = "N"
    if w>0 and h<len(grid)-1:
        grid[h+1][w-1] = "N"
    
def calNo(grid,n,w,h,ans):
    if (n==0):
        ans.add(','.join(str(item) for innerlist in grid for item in innerlist))
    nochange = True
    for i in range(h):
        for j in range(w):
            if grid[i][j] == "":
                nochange = False
                dup = copy.deepcopy(grid)
                dup[i][j] = "V"
                getDistance(dup,i,j)
                calNo(dup,n-1,w,h,ans)

def calsocialdistancing(s):
    d = s.split(", ")
    fixed = (len(d)-3)//2
    w = int(d[0])
    h = int(d[1])
    n = int(d[2])-fixed
    if n > 1 and w*h <= (round(math.sqrt(n))+1)**2:
        return "No Solution"
    if int(d[2])>4:
        return "No Solution"
    grid = []
    for i in range(h):
        grid.append([""]*w)
    for i in range(fixed):
        grid[int(d[3+i*2])][int(d[4+i*2])] = "V"
        getDistance(grid,int(d[3+i*2]),int(d[4+i*2]))

    ans = set()
    calNo(grid,n,w,h,ans)
    if len(ans) == 0:
        return "No Solution"
    return len(ans)
    