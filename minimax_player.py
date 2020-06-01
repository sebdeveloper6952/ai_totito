import socketio
from board_utils import *
import os
import time
from math import inf
from random import choice, seed
from copy import deepcopy

# data
# username = input("Username: ")
username = "SebasArriola"
tid = 1
# tid = input("Tournament ID: ")
# url = "http://3.12.129.126:5000"
url = "http://localhost:4000"
game_id = 0
curr_board = []
# starting_depth = int(input("Lookahead: "))
starting_depth = 3
algo_depth = starting_depth

# global client
client = socketio.Client()

# sign in to the server using constants above
def sign_in():
    client.emit('signin', {
        'user_name': username,
        'tournament_id': tid,
        'user_role': "player"
    })

# server events
@client.event
def connect():
    print("Connected to server!")
    sign_in()

@client.event
def disconnect():
    print("Connection to server closed!")

@client.event
def ok_signin():
    print("Sign in succesful!")

@client.event
def error_signin(data):
    print('error signing in')

@client.event
def finish(data):
    global algo_depth
    algo_depth = starting_depth
    p1_score, p2_score = calculate_scores(data["board"])
    print("***************** GAME OVER ********************")
    print(f"* Player {data['winner_turn_id']} won!")
    print("******************* SCORE **********************")
    print(f"* Player 1: {p1_score}")
    print(f"* Player 2: {p2_score}")
    print("************************************************")
    # rematch
    client.emit('player_ready', {
        'tournament_id': tid,
        'player_turn_id': data["player_turn_id"],
        'game_id': game_id
    })

@client.event
def ready(data):
    global game_id
    global curr_board
    global algo_depth

    curr_board = data["board"]
    game_id = data["game_id"]

    start = time.time()
    moves_left = len(get_valid_moves(curr_board))
    (best_score, best_move) = minimax(curr_board, algo_depth, True, -inf, inf)
    diff = time.time() - start

    if algo_depth < 7 and moves_left < 25 and diff < 0.1:
        algo_depth += 1

    if diff > 1.0:
        print("******************************************************")
        print(f"Diff was: {diff}, moves left: {moves_left}, depth: {algo_depth}")
        print("******************************************************")
    
    print(f"Time: {diff}, Depth: {algo_depth}")
    print(f"Playing move {best_move}, with score {best_score}")
    play_move(best_move[0], best_move[1], data["player_turn_id"])
    

# Main Program
client.connect(url)

####################################### Dots And Boxes ###############################################
def play_move(h_or_v, pos, player_turn_id):
    client.emit('play', {
        'tournament_id': tid,
        'game_id': game_id,
        'player_turn_id': player_turn_id,
        'movement': [h_or_v, pos]
    })

def minimax(board, depth, is_max, alpha, beta):
    if depth == 0 or is_full(board):
        return (static_evaluation(board), None)

    valid_moves = get_valid_moves(board)
    if is_max:
        max_score = -inf
        b_move = [0,0]
        for m in valid_moves:
            sq = new_squares_created(board, m)
            board_c = deepcopy(board)
            board_c[m[0]][m[1]] = sq
            (score, move) = minimax(board_c, depth - 1, sq > 0, alpha, beta)
            if score > max_score:
                max_score = score
                b_move = m
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return (max_score, b_move)
    else:
        min_score = inf
        b_move = [0,0]
        for m in valid_moves:
            sq = new_squares_created(board, m)
            board_c = deepcopy(board)
            board_c[m[0]][m[1]] = -sq if sq > 0 else 0
            (score, move) = minimax(board_c, depth - 1, not (sq > 0), alpha, beta)
            if score < min_score:
                min_score = score
                b_move = m
            beta = min(beta, score)
            if beta <= alpha:
                break
        return (min_score, b_move)
