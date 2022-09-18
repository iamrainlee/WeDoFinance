#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import json
from sseclient import SSEClient
import requests
import random
import numpy as np

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

def flip(battleId):
    logging.info("Flip table")
    rdata = {}
    rdata['action'] = '(╯°□°)╯︵ ┻━┻'
    requests.post("https://cis2022-arena.herokuapp.com/connect4/play/" + battleId, data = rdata)

def sendmove(battleId,move):
    logging.info("sendmove: {}".format(move))
    rdata = {}
    rdata['column'] = move
    rdata['action'] = 'putToken'
    requests.post("https://cis2022-arena.herokuapp.com/connect4/play/" + battleId, data = rdata)

def create_board():
    board = np.zeros((6, 7))
    return board

def makemove(board,col):
    for i in range(5,-1,-1):
        if board[i][col] == 0:
            board[i][col] = 1
            return True
    return False

@app.route('/connect4', methods=['POST'])
def connect4():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    battleId = data.get("battleId")
    youAre = ""
    gameOn = True
    board = create_board()
    columns = ['A','B','C','D','E','F','G']
    lastmove = ""
    myturn = False
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
                    #if(data['youAre'] == "\xF0\x9F\x94\xB4"):
                    logging.info("Prepare to make move")
                    move = random.randint(0,6)
                    sendmove(battleId,columns[move])
                    lastmove = columns[move]
                    makemove(board,move)
                continue
                # if( data['youAre'] != ""):
                #     youAre = data['youAre']
                #     if(data['youAre'] == "\xF0\x9F\x94\xB4"):
                #         logging.info("Prepare to make move2")
                #         myturn = True
                #         move = random.randint(0,6)
                #         sendmove(battleId,columns[move])
                #         lastmove = columns[move]
                #         makemove(board,move)
                #     if youAre != "\xF0\x9F\x94\xB4" and youAre != "\xF0\x9F\x9F\xA1":
                #         flip(battleId)
                #         break
            except:
                try:
                    if data["column"] not in columns:
                        flip(battleId)
                        break
                    if data['player'] != "\xF0\x9F\x94\xB4" and data['player'] != "\xF0\x9F\x9F\xA1":
                        flip(battleId)
                        break
                    if data['action'] != '(╯°□°)╯︵ ┻━┻' and data['action'] != 'putToken':
                        flip(battleId)
                        break
                    else:
                        if data['player'] == youAre:
                            if lastmove != data['column']:
                                flip(battleId)
                                break
                            while True:
                                move = random.randint(0,6)
                                if makemove(board,move):
                                    sendmove(battleId,columns[move])
                                    lastmove = columns[move]
                                    break
                        else:
                            move = columns.index(data['column'])
                            if not makemove(board,move):
                                flip(battleId)
                                break
                            else:
                                while True:
                                    move = random.randint(0,6)
                                    if makemove(board,move):
                                        sendmove(battleId,columns[move])
                                        lastmove = columns[move]
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