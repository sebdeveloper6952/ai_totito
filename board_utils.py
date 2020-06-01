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
    # returns valid moves on board
    valid_moves = []
    for a in range(len(board[0])):
        if board[0][a] == EMPTY:
            valid_moves.append([0, a])
        if board[1][a] == EMPTY:
            valid_moves.append([1, a])
    return valid_moves

def calculate_scores(board):
    p1_score, p2_score = 0, 0
    for a in range(len(board[0])):
        h = board[0][a]
        v = board[1][a]
        if h is not EMPTY and h is not 0:
            if h > 0:
                p1_score += h
            else:
                p2_score += h
        if v is not EMPTY and v is not 0:
            if v > 0:
                p1_score += v
            else:
                p2_score += v
    return p1_score, abs(p2_score)

def is_full(board):
    # returns whether the board is full
    for i in range(2):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
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
    # returns number of new squares created with move
    b = count_squares(board)
    # apply move
    board[move[0]][move[1]] = 0
    a = count_squares(board)
    board[move[0]][move[1]] = EMPTY
    return a - b

def static_evaluation(board):
    """
    Returns one number associated with this board:
    p1_score - p2_score. If possitive, this board
    is beneficial for MAX player and if negative,
    this board is better for MIN player
    """
    p1_score, p2_score = calculate_scores(board)
    return (p1_score - p2_score)