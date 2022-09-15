import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/tickerStreamPart1', methods=['POST'])
def tickerStreamPart1():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("stream")
    
    return json.dumps({"Result":to_cumulative(inputValue)})

def to_cumulative(stream: list):
    result = {}
    for i in range(len(stream)):
        data = stream[i].split(",")
        if data[0] in result:
            if data[1] in result[data[0]]:
                result[data[0]][data[1]][0] = result[data[0]][data[1]][0] + int(data[2])
                result[data[0]][data[1]][1] = result[data[0]][data[1]][1] + int(data[2])*oneDpToInt2(data[3])
            else:
                result[data[0]][data[1]] = [int(data[2]),int(data[2])*oneDpToInt2(data[3])]
        else:
            result[data[0]] = {}
            result[data[0]][data[1]] = [int(data[2]),int(data[2])*oneDpToInt2(data[3])]
    
    strresult = []
    sum_vol = {}
    sum_turnover = {}
    for i in sorted(result.keys()):
        temp =  str(i) 
        for j in sorted(result[i].keys()):
            if j not in sum_vol:
                sum_vol[j] = 0
                sum_turnover[j] = 0
            sum_vol[j] = sum_vol[j] + result[i][j][0]
            sum_turnover[j] = sum_turnover[j] + result[i][j][1]
            temp +=  "," + str(j) + "," + str(sum_vol[j]) + "," + intToOneDp2(sum_turnover[j])
        strresult.append(temp)
    return strresult

def oneDpToInt2(num: str):
    return int(num[:-2])*10+int(num[-1])


def intToOneDp2(num: int):
    return f"{num//10}.{num%10}"