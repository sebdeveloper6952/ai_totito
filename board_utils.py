def print_board(board):
    for i in range(11):
        if i % 2 == 0:
            print("*", end="", flush=True)
            for j in range(5):
                if board[0][(i // 2) + (j * 6)] == 99:
                    print("   ", end="", flush=True)
                else:
                    print("---", end="", flush=True)
                print("*", end="", flush=True)
        else:
            for j in range(6):
                if board[1][j + ((i // 2) * 6)] == 99:
                    print(" ", end="", flush=True)
                else:
                    print("|", end="", flush=True)
                print("   ", end="", flush=True)
        print("")

def get_valid_moves(board):
    valid_moves = [[],[]]
    for a in range(len(board[0])):
        if board[0][a] == 99:
            valid_moves[0].append(a)
        if board[1][a] == 99:
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