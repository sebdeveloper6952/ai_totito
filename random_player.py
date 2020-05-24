import socketio
from random import seed
from random import randint
from random import choice
from board_utils import *
import os
import time

# SEED
# seed(int(time.time()))
seed(69)

# data
username = input("Username: ")
tid = input("Tournament ID: ")
# url = "http://3.12.129.126:4000"
url = "http://localhost:4000"
game_id = 0

# global client
client = socketio.Client()

# temp
curr_board = []

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
    print(data)
    print(data["board"])
    p1_score, p2_score = calculate_scores(data["board"])
    print("***************** GAME OVER ********************")
    print(f"* Player {data['winner_turn_id']} won!")
    print("******************* SCORE **********************")
    print(f"* Player 1: {p1_score}")
    print(f"* Player 2: {p2_score}")
    print("************************************************")
    # rematch
    time.sleep(int(data["player_turn_id"]))
    client.emit('player_ready', {
        'tournament_id': tid,
        'player_turn_id': data["player_turn_id"],
        'game_id': game_id
    })

@client.event
def ready(data):
    os.system('clear')

    global game_id
    global curr_board

    curr_board = data["board"]
    game_id = data["game_id"]

    print(f"********** MOVEMENT NUMBER {data['movementNumber']}*********************")

    # print the current board, before sending this move
    print_board(curr_board)

    # valid moves
    valid_moves = get_valid_moves(curr_board)
    move = choice(valid_moves)

    # TODO: remove for online testing
    # time.sleep(0.5)

    # random valid move
    # h_or_v, pos = 0, 0
    # if len(valid_moves[0]) > 0 and len(valid_moves[1]) > 0:
    #     h_or_v = randint(0,1)
    #     pos = randint(0, len(valid_moves[h_or_v]) - 1)
    # elif len(valid_moves[0]) == 0:
    #     h_or_v = 1
    #     pos = randint(0, len(valid_moves[1]) - 1)
    # else:
    #     pos = randint(0, len(valid_moves[0]) - 1)
    # play_move(h_or_v, valid_moves[h_or_v][pos], data["player_turn_id"])
    play_move(move, data["player_turn_id"])
    
    # player input
    # for row in curr_board:
    #     print(row)
    # h_or_v = int(input("H(0) or V(1): "))
    # pos = int(input("Pos: "))
    # play_move(h_or_v, pos)

# Main Program
client.connect(url)

####################################### Dots And Boxes ###############################################
def play_move(move, player_turn_id):
    print(f"Player {player_turn_id} is sending move [{move[0]},{move[1]}]")
    client.emit('play', {
        'tournament_id': tid,
        'game_id': game_id,
        'player_turn_id': player_turn_id,
        'movement': move
    })
