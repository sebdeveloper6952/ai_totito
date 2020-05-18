EMPTY = 99

def print_board(board):
    for i in range(11):
        if i % 2 == 0:
            print("*", end="", flush=True)
            for j in range(5):
                if board[0][(i // 2) + (j * 6)] == EMPTY:
                    print("   ", end="", flush=True)
                else:
                    print("---", end="", flush=True)
                print("*", end="", flush=True)
        else:
            for j in range(6):
                if board[1][j + ((i // 2) * 6)] == EMPTY:
                    print(" ", end="", flush=True)
                else:
                    print("|", end="", flush=True)
                print("   ", end="", flush=True)
        print("")

def get_valid_moves(board):
    valid_moves = [[],[]]
    for a in range(len(board[0])):
        if board[0][a] == EMPTY:
            valid_moves[0].append(a)
        if board[1][a] == EMPTY:
            valid_moves[1].append(a)
    return valid_moves

def calculate_scores(board):
    p1_score, p2_score = 0, 0
    for a in range(len(board[0])):
        if board[0][a] > 0:
            p1_score += board[0][a]
        elif board[0][a] < 0:
            p2_score += abs(board[0][a])
        if board[1][a] > 0:
            p1_score += board[1][a]
        elif board[1][a] < 0:
            p2_score += abs(board[1][a])
    return p1_score, p2_score

def get_minimax_scores(board):
    p1_score, p2_score = 0, 0
    for a in range(len(board[0])):
        if board[0][a] > 0:
            p1_score += board[0][a]
        elif board[0][a] < 0:
            p2_score += board[0][a]
        if board[1][a] > 0:
            p1_score += board[1][a]
        elif board[1][a] < 0:
            p2_score += board[1][a]
    return p1_score, p2_score

def is_full(board):
    # returns number of winner or -1 for no winner
    for i in board:
        for j in board:
            if j == 0:
                return False
    return True

def count_squares(board):
    # returns number of closed squares
    N = 6
    a = 0
    c = 0
    square_count = 0
    for i in range(len(board[0])):
        if ((i + 1) % N) != 0:
            if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][c + a] != EMPTY and board[1][c + a + 1] != EMPTY:
                square_count += 1
            a = a + N
        else:
            c += 1
            a = 0
    return square_count

def new_squares_created(board, move):
    # returns number of new squares created
    b = count_squares(board)
    # apply move
    board[move[0]][move[1]] = 0
    a = count_squares(board)
    board[move[0]][move[1]] = EMPTY
    return a - b