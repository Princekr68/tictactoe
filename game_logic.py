import random

EMPTY = ""
HUMAN = "X"
AI = "O"


WINNING_LINES = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6)
]


def new_board():
    return [EMPTY] * 9


def winning_line(board):
    for line in WINNING_LINES:
        a, b, c = line

        if (
            board[a] != EMPTY
            and board[a] == board[b]
            and board[b] == board[c]
        ):
            return list(line)

    return []


def check_winner(board):
    line = winning_line(board)

    if line:
        return board[line[0]]

    if EMPTY not in board:
        return "Draw"

    return None


def available_moves(board):
    return [
        index
        for index, value in enumerate(board)
        if value == EMPTY
    ]


def minimax(board, depth, maximizing, alpha, beta):

    result = check_winner(board)

    if result == AI:
        return 10 - depth

    if result == HUMAN:
        return depth - 10

    if result == "Draw":
        return 0


    if maximizing:

        best_score = float("-inf")

        for move in available_moves(board):

            board[move] = AI

            score = minimax(
                board,
                depth + 1,
                False,
                alpha,
                beta
            )

            board[move] = EMPTY

            best_score = max(
                best_score,
                score
            )

            alpha = max(
                alpha,
                best_score
            )

            if beta <= alpha:
                break

        return best_score


    best_score = float("inf")

    for move in available_moves(board):

        board[move] = HUMAN

        score = minimax(
            board,
            depth + 1,
            True,
            alpha,
            beta
        )

        board[move] = EMPTY

        best_score = min(
            best_score,
            score
        )

        beta = min(
            beta,
            best_score
        )

        if beta <= alpha:
            break

    return best_score


def best_move(board):

    moves = available_moves(board)

    if not moves:
        return None

    # Sometimes make a random move
    if random.random() < 0.30:
        return random.choice(moves)

    # Otherwise make the best move
    best_score = float("-inf")
    move_choice = None

    for move in moves:

        board[move] = AI

        score = minimax(
            board,
            0,
            False,
            float("-inf"),
            float("inf")
        )

        board[move] = EMPTY

        if score > best_score:
            best_score = score
            move_choice = move

    return move_choice