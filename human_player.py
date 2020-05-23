import socketio
from random import seed
from random import randint
from board_utils import *
import os
import time

# SEED
seed(int(time.time()))

# data
username = input("Username: ")
tid = input("Tournament ID: ")
url = "http://localhost:4000"
game_id = 0
player_num = 0

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

    global player_num
    global game_id
    global curr_board

    curr_board = data["board"]
    game_id = data["game_id"]

    print(f"********** MOVEMENT NUMBER {data['movementNumber']}*********************")

    # print the current board, before sending this move
    print_board(curr_board)

    # valid moves
    valid_moves = get_valid_moves(curr_board)
    print("")
    print("Valid moves: ")
    print(valid_moves[0])
    print(valid_moves[1])
    print("")
    
    # player input
    for row in curr_board:
        print(row)
    h_or_v = int(input("H(0) or V(1): "))
    pos = int(input("Pos: "))

    squares = new_squares_created(curr_board, [h_or_v, pos])
    print(f"Squares created in this move: {squares}")

    play_move(h_or_v, pos, data["player_turn_id"])

# Main Program
client.connect(url)

####################################### Dots And Boxes ###############################################
def play_move(h_or_v, pos, player_turn_id):
    print(f"Player {player_num} is sending move [{h_or_v},{pos}]")
    client.emit('play', {
        'tournament_id': tid,
        'game_id': game_id,
        'player_turn_id': player_turn_id,
        'movement': [h_or_v, pos]
    })
