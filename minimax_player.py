import socketio
from board_utils import *
import os
import time
from math import inf

# data
username = input("Username: ")
tid = input("Tournament ID: ")
# url = "http://3.12.129.126:4000"
url = "http://localhost:4000"
game_id = 0
curr_board = []
counter = 0

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
    # os.system('clear')

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

    is_max = data["player_turn_id"] == 1
    # print(f"is MAX turn? {is_max}")

    # valid_moves = get_valid_moves(curr_board)
    # print(valid_moves)
    # best_score = -inf
    best_move = [0,0]

    global counter
    counter = 0

    start = time.time()
    best_score = minimax(curr_board, 60, is_max, -inf, inf, best_move)
    print(f"Time to compute next move: {time.time() - start}")
    print(f"Considered {counter} positions.")
    # print the current board, before sending this move
    print_board(curr_board)
    
    print(f"Playing move {best_move}, with score {best_score}")
    # input("press to play move...")
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

def minimax(board, depth, is_max, a, b, best_move):
    # TODO: remove for final
    # print(f"is_max: {is_max}, @ depth: {depth}, eval board: {board}")
    # input("step...")
    global counter
    counter += 1

    if depth == 0 or is_full(board):
        return static_evaluation(board)

    valid_moves = get_valid_moves(board)
    if is_max:
        best_score = -inf
        for m in valid_moves:
            sq = new_squares_created(board, [m[0], m[1]])
            board[m[0]][m[1]] = sq if sq > 0 else 0
            score = minimax(board, depth - 1, False, a, b, best_move)
            board[m[0]][m[1]] = EMPTY
            a = max(a, score)
            if b <= a:
                break
            if score > best_score:
                best_score = score
                best_move[0] = m[0]
                best_move[1] = m[1]
        return best_score
    else:
        best_score = inf
        for m in valid_moves:
            sq = new_squares_created(board, [m[0], m[1]])
            board[m[0]][m[1]] = sq if sq > 0 else 0
            score = minimax(board, depth - 1, True, a, b, best_move)
            board[m[0]][m[1]] = EMPTY
            b = min(b, score)
            if b <= a:
                break
            if score < best_score:
                best_score = score
                best_move[0] = m[0]
                best_move[1] = m[1]
        return best_score
