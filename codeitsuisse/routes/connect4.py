#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import json
from sseclient import SSEClient
import requests

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/connect4', methods=['POST'])
def connect4():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    battleId = data.get("battleId")
    # board_first = ['a','b','c','d','e','f','g','h','i']
    # board_second = board_first[::-1]
    # board = []
    # for i in range(9):
    #     board.append(['','','','','','','','',''])
    youAre = ""
    gameOn = True
    while gameOn:
        url = 'https://cis2022-arena.herokuapp.com/connect4/start/'+battleId
        headers = {'Accept': 'text/event-stream'}
        messages = SSEClient(url)
        for msg in messages:
            data = msg.data
            logging.info("data sent from arena {}".format(data))
            if type(data) is str:
                try:
                    data = json.loads(data)
                except:
                    continue
            try:
                if( data['youAre'] != ""):
                    youAre = data['youAre']
                    if(data['youAre'] == "\xF0\x9F\x94\xB4"):
                        logging.info("Prepare to make move")
                        rdata = {}
                        rdata['action'] = '(╯°□°)╯︵ ┻━┻'
                        requests.post("https://cis2022-arena.herokuapp.com/connect4/play/"+battleId, data = rdata)
            except:
                try:
                    if(data['player'] == "\xF0\x9F\x94\xB4"):
                        continue
                    else:
                        rdata = {}
                        rdata['action'] = '(╯°□°)╯︵ ┻━┻'
                        requests.post("https://cis2022-arena.herokuapp.com/connect4/play/"+battleId, data = rdata)
                        break
                except:
                    try:
                        if(data['winner'] == "draw" or data['winner'] == youAre):
                            logging.info("Win game!")
                        else:
                            logging.info("Possibly lost game!")
                        gameOn = False
                        break
                    except:
                        gameOn = False
                        break
    return json.dumps(data)

# def makemove2(board,youAre,battleId,players):
#     data = {}
#     data['action'] = "move"
#     data["position"] = ""
#     current_loc = int(players[0][1])
#     data["position"] = "e"+(current_loc+1)
#     players[0] = data["position"]
#     logging.info("My move :{}".format(data))
#     requests.post("https://cis2021-arena.herokuapp.com/quoridor/play/"+battleId, data = data)