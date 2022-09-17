#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import json
from sseclient import SSEClient
import requests

from flask import request, jsonify

from codeitsuisse import app
import copy

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
    board = create_board(6, 7)
    state = State(board, "")
    youAre = ""
    myTurn = True
    columns = ['A','B','C','D','E','F','G']
    lastmove = ""
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
                        myTurn = True
                        logging.info("Prepare to make move")
                        given_row = ai_input(state)
                        state.turn = "x"
                        state = get_next_state(state, given_row)
                        rdata = {}
                        rdata['action'] = 'putToken'
                        rdata['column'] = columns[given_row]
                        lastmove = columns[given_row]
                        requests.post("https://cis2022-arena.herokuapp.com/connect4/play/"+battleId, data = rdata)
                        myTurn = False
                    else:
                        myTurn = True
            except:
                try:
                    if(data['player'] == youAre):
                        if not myTurn:
                            myTurn = True
                            if lastmove != data['column']:
                                rdata = {}
                                rdata['action'] = '(╯°□°)╯︵ ┻━┻'
                                requests.post("https://cis2022-arena.herokuapp.com/connect4/play/"+battleId, data = rdata)
                                break
                        else:
                            rdata = {}
                            rdata['action'] = '(╯°□°)╯︵ ┻━┻'
                            requests.post("https://cis2022-arena.herokuapp.com/connect4/play/"+battleId, data = rdata)
                            break
                        continue
                    else:
                        possible_moves = get_possible_moves(state)
                        move = columns.index(data['column'])
                        if move not in possible_moves:
                            rdata = {}
                            rdata['action'] = '(╯°□°)╯︵ ┻━┻'
                            requests.post("https://cis2022-arena.herokuapp.com/connect4/play/"+battleId, data = rdata)
                            break
                        else:
                            state.turn = 'o'
                            state = get_next_state(state, move)
                            given_row = ai_input(state)
                            state.turn = "x"
                            state = get_next_state(state, given_row)
                            rdata = {}
                            rdata['action'] = 'putToken'
                            rdata['column'] = columns[given_row]
                            lastmove = columns[given_row]
                            requests.post("https://cis2022-arena.herokuapp.com/connect4/play/"+battleId, data = rdata)
                            myTurn = False
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


SPACE = " "
P1 = "x"
P2 = "o"
NONE = ""
DEBUG = False
EMPTY = []
HUMAN = "human"
CPU = "cpu"

class State:
    def __init__(self, board, turn):
        self.board = board
        self.turn = turn
        
def create_board(height, width):
    board = []
    for y in range(height):
        line = []
        for x in range(width):
            line.append(SPACE)
        board.append(line)
    return board


def is_board_full(board):
    for line in board:
        for elem in line:
            if elem == P1 or elem == P2:
                continue
            return False
    return True

def get_possible_moves(state):
    board = state.board
    possible_moves = []
    for x in range(7):
        if is_row_filled(board, x) == False:
            possible_moves.append(x)
    return possible_moves

def get_winner(state):
    board = state.board
    if is_player_win(board, P1) == True:
        return P1
    elif is_player_win(board, P2) == True:
        return P2
    else:
        return NONE

def is_player_win(board, turn):
    #turn = state.turn
    #winner = state.winner
    #board = state.board
    max_connect = -1
    current_state = SPACE
    state_list = []

    for line in board:
        max_connect = calc_max_connect(turn, line)
        if max_connect >= 4:
            return True

    for x in range(7):
        state_list = []
        for y in range(height):
            state_list.append(board[y][x])
        max_connect = calc_max_connect(turn, state_list)
        if max_connect >= 4:
            return True

    state_list = []
    for x in range(7):
        state_list = get_right_diagonal_state(board, x, 0)
        max_connect = calc_max_connect(turn, state_list)
        if max_connect >= 4:
            return True
        state_list = get_left_diagonal_state(board, x, 0)
        max_connect = calc_max_connect(turn, state_list)
        if max_connect >= 4:
            return True
        
    for y in range(6):
        state_list = get_right_diagonal_state(board, 0, y)
        max_connect = calc_max_connect(turn, state_list)
        if max_connect >= 4:
            return True

    for y in range(6):
        state_list = get_left_diagonal_state(board, 7-1, y)
        max_connect = calc_max_connect(turn, state_list)
        if max_connect >= 4:
            return True
    return False
            
def get_right_diagonal_state(board, x, y):
    state_list = []
    while x < 7 and y < 6:
        state_list.append(board[y][x])
        x += 1
        y += 1
    return state_list           

def get_left_diagonal_state(board, x, y):
    state_list = []
    while 0 <= x and y < 6:
        state_list.append(board[y][x])
        x -= 1
        y += 1
    return state_list           
    
def calc_max_connect(turn, state_list):
    max_connect = 0
    max_connects = []
    for state in state_list:
        if state == turn:
            max_connect += 1
        else:
            max_connects.append(max_connect)
            max_connect = 0
    max_connects.append(max_connect)
    return max(max_connects)
        

def is_elem_filled(board, x, y):
    if board[y][x] == SPACE:
        return False
    else:
        return True

def is_row_filled(board, row):
    for y in range(6):
        if board[y][row] == SPACE:
            return False
    return True

def set_elem(state, x, y):
    state.board[y][x] = state.turn
    return state

def get_next_state(original_state, row):
    state = copy.deepcopy(original_state)
    board = state.board
    y = 6 - 1
    while 0 <= y:
        if is_elem_filled(board, row, y) == True:
            y -= 1
            continue
        else:
            state = set_elem(state, row, y)
            # state.turn = get_current_player(state)
            return state
    return NONE

def show_whos_win(state):
    winner = get_winner(state)
    # if winner == NONE:
    #     print "Drawn Game!"
    # elif winner == P1:
    #     print "Player 1 wins!"
    # elif winner == P2:
    #     print "Player 2 wins!"
    # else:
    #     print "Error: unknown winner..."
    # return

def get_state_score(state, alpha, beta):
    return _get_state_score(state, state.turn, alpha, beta)
    
def _get_state_score(original_state, turn, _alpha, _beta):
    alpha = _alpha
    beta = _beta
    state = copy.deepcopy(original_state)
    score = 0
    child_scores = []
    possible_moves = get_possible_moves(state)
    winner = get_winner(state)
    if winner == P1:
        return -1
    elif winner == P2:
        return 1
    else: # No winner
        if possible_moves == EMPTY: # Drawn Game
            return 0
        else:
            for move in possible_moves:
                if alpha >= beta:
                    #print "alpha="+str(alpha)+", beta="+str(beta)
                    break
                next_state = get_next_state(state, move)
                #show_board(next_state.board)
                score = _get_state_score(next_state, turn, alpha, beta)
                if state.turn == P1:
                    beta = min(beta, score)
                else:
                    alpha = max(alpha, score)
                child_scores.append(score)

    # Must have some score(s) from children
    if state.turn == P2:
        return max(child_scores)
    else:
        return min(child_scores)

def ai_input(original_state):
    state = copy.deepcopy(original_state)
    possible_moves = get_possible_moves(state)
    scores = []
    best_move = -1
    best_score = -100
    alpha = -100
    beta = 100
    for move in possible_moves:
        next_state = get_next_state(state, move)
        score = get_state_score(next_state, alpha, beta)
        if score > alpha:
            alpha = score
        #scores.append(score)
        if best_score < score:
            best_score = score
            best_move = move

    return best_move