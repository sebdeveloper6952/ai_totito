import socketio
from board_utils import *
import os
import time
from math import inf

# data
username = input("Username: ")
tid = input("Tournament ID: ")
url = "http://localhost:4000"
game_id = 0
curr_board = []

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
    time.sleep(0.1)

    global game_id
    global curr_board

    curr_board = data["board"]
    game_id = data["game_id"]

    print(f"********** MOVEMENT NUMBER {data['movementNumber']}*********************")
    # keep track of best_score and best_move
    # for each valid move
    #     modify board with valid move (0)
    #     score = minimax(board, 0, !bool)
    #     unmodify board 
    #     if score > best_score:
    #         best_move = move
    #         best_score = score
    # apply best_move to board
    # play_move(best_move)

    valid_moves = get_valid_moves(curr_board)
    print(valid_moves)
    best_score = -inf
    best_move = []
    is_max = not data["player_turn_id"] == 1
    for i in range(2):
        for j in range(len(valid_moves[i])):
            curr_board[i][valid_moves[i][j]] = 0
            score = minimax(curr_board, 0, is_max)
            curr_board[i][valid_moves[i][j]] = 99
            if score > best_score:
                best_score = score
                best_move = [i, valid_moves[i][j]]
    print(f"Playing move {best_move}")
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

def minimax(position, depth, is_max):
    # get number of winner
    if is_full(position):
        p1, p2 = calculate_scores(position)
        return p1 if p1 > p2 else p2
    valid_moves = get_valid_moves(position)
    if is_max:
        best_score = -inf
        for i in valid_moves:
            for j in range(len(curr_board[i])):
                if position[i][valid_moves[i][j]] == '':
                    curr_board[i][valid_moves[i][j]] = 0
                    score = minimax(curr_board, depth + 1, False)
                    curr_board[i][valid_moves[i][j]] = 99
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = inf
        for i in valid_moves:
            for j in range(len(curr_board[i])):
                if position[i][valid_moves[i][j]] == '':
                    curr_board[i][valid_moves[i][j]] = 0
                    score = minimax(curr_board, depth + 1, True)
                    curr_board[i][valid_moves[i][j]] = 99
                    best_score = min(score, best_score)
        return best_score
