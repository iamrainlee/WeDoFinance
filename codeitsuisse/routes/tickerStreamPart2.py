import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/tickerStreamPart2', methods=['POST'])
def tickerStreamPart2():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputList = data.get("stream")
    inputQuantity = data.get("quantityBlock")
    result = to_cumulative_delayed(inputList,inputQuantity)
    logging.info("result: {}".format(result))
    return json.dumps({"Result":result})

def to_cumulative_delayed(stream: list, quantity_block: int):
    result = {}
    for i in range(len(stream)):
        data = stream[i].split(",")
        if data[0] in result:
            if data[1] not in result[data[0]]:
                result[data[0]][data[1]] = []
            result[data[0]][data[1]].append([int(data[2]),oneDpToInt(data[3])])
        else:
            result[data[0]] = {}
            result[data[0]][data[1]] = []
            result[data[0]][data[1]].append([int(data[2]),oneDpToInt(data[3])])
    strresult = []
    sum_vol = {}
    sum_turnover = {}
    timeoutput = []
    for i in sorted(result.keys()):
        for j in sorted(result[i].keys()):
            t_sum = 0
            t_sum_turnover = 0
            if j not in sum_vol:
                sum_vol[j] = 0
                sum_turnover[j] = 0
            for k in result[i][j]:
                if (sum_vol[j] + k[0])// quantity_block > (sum_vol[j])// quantity_block :
                    if str(i) not in timeoutput:
                        timeoutput.append(str(i))
                        strresult.append(str(i)+ "," + str(j) + "," + str((sum_vol[j] + k[0])// quantity_block * quantity_block) + "," + intToOneDp(sum_turnover[j] + k[1] * ((sum_vol[j] + k[0])// quantity_block * quantity_block - sum_vol[j])))
                    else:
                        strresult[len(strresult)-1] =  (strresult[len(strresult)-1]+ "," + str(j) + "," + str((sum_vol[j] + k[0])// quantity_block * quantity_block) + "," + intToOneDp(sum_turnover[j] + k[1] * ((sum_vol[j] + k[0])// quantity_block * quantity_block - sum_vol[j])))
                t_sum += k[0]
                t_sum_turnover += k[1]*k[0]
            sum_vol[j] += t_sum
            sum_turnover[j] += t_sum_turnover
    return strresult

def oneDpToInt(num: str):
    return int(num[:-2])*10+int(num[-1])


def intToOneDp(num: int):
    return f"{num//10}.{num%10}"