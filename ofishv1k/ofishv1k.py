import chess
import time

# Piece-square tables
piece_values_middlegame = {
    chess.PAWN: 82,
    chess.KNIGHT: 337,
    chess.BISHOP: 365,
    chess.ROOK: 477,
    chess.QUEEN: 1025,
    chess.KING: 0,
}

piece_values_endgame = {
    chess.PAWN: 94,
    chess.KNIGHT: 281,
    chess.BISHOP: 297,
    chess.ROOK: 512,
    chess.QUEEN: 936,
    chess.KING: 0,
}

piece_square_tables_middlegame = {
    chess.PAWN: [
      0,   0,   0,   0,   0,   0,  0,   0,
     98, 134,  61,  95,  68, 126, 34, -11,
     -6,   7,  26,  31,  65,  56, 25, -20,
    -14,  13,   6,  21,  23,  12, 17, -23,
    -27,  -2,  -5,  12,  17,   6, 10, -25,
    -26,  -4,  -4, -10,   3,   3, 33, -12,
    -35,  -1, -20, -23, -15,  24, 38, -22,
      0,   0,   0,   0,   0,   0,  0,   0,
    ],

    chess.KNIGHT: [
    -167, -89, -34, -49,  61, -97, -15, -107,
     -73, -41,  72,  36,  23,  62,   7,  -17,
     -47,  60,  37,  65,  84, 129,  73,   44,
      -9,  17,  19,  53,  37,  69,  18,   22,
     -13,   4,  16,  13,  28,  19,  21,   -8,
     -23,  -9,  12,  10,  19,  17,  25,  -16,
     -29, -53, -12,  -3,  -1,  18, -14,  -19,
    -105, -21, -58, -33, -17, -28, -19,  -23,
    ],

    chess.BISHOP: [
    -29,   4, -82, -37, -25, -42,   7,  -8,
    -26,  16, -18, -13,  30,  59,  18, -47,
    -16,  37,  43,  40,  35,  50,  37,  -2,
     -4,   5,  19,  50,  37,  37,   7,  -2,
     -6,  13,  13,  26,  34,  12,  10,   4,
      0,  15,  15,  15,  14,  27,  18,  10,
      4,  15,  16,   0,   7,  21,  33,   1,
    -33,  -3, -14, -21, -13, -12, -39, -21,
    ],

    chess.ROOK: [
     32,  42,  32,  51, 63,  9,  31,  43,
     27,  32,  58,  62, 80, 67,  26,  44,
     -5,  19,  26,  36, 17, 45,  61,  16,
    -24, -11,   7,  26, 24, 35,  -8, -20,
    -36, -26, -12,  -1,  9, -7,   6, -23,
    -45, -25, -16, -17,  3,  0,  -5, -33,
    -44, -16, -20,  -9, -1, 11,  -6, -71,
    -19, -13,   1,  17, 16,  7, -37, -26,
    ],

    chess.QUEEN: [
    -28,   0,  29,  12,  59,  44,  43,  45,
    -24, -39,  -5,   1, -16,  57,  28,  54,
    -13, -17,   7,   8,  29,  56,  47,  57,
    -27, -27, -16, -16,  -1,  17,  -2,   1,
     -9, -26,  -9, -10,  -2,  -4,   3,  -3,
    -14,   2, -11,  -2,  -5,   2,  14,   5,
    -35,  -8,  11,   2,   8,  15,  -3,   1,
     -1, -18,  -9,  10, -15, -25, -31, -50,
    ],

    chess.KING: [
    -65,  23,  16, -15, -56, -34,   2,  13,
     29,  -1, -20,  -7,  -8,  -4, -38, -29,
     -9,  24,   2, -16, -20,   6,  22, -22,
    -17, -20, -12, -27, -30, -25, -14, -36,
    -49,  -1, -27, -39, -46, -44, -33, -51,
    -14, -14, -22, -46, -44, -30, -15, -27,
      1,   7,  -8, -64, -43, -16,   9,   8,
    -15,  36,  12, -54,   8, -28,  24,  14,
    ]


}

piece_square_tables_endgame = {
    chess.PAWN: [
      0,   0,   0,   0,   0,   0,   0,   0,
    178, 173, 158, 134, 147, 132, 165, 187,
     94, 100,  85,  67,  56,  53,  82,  84,
     32,  24,  13,   5,  -2,   4,  17,  17,
     13,   9,  -3,  -7,  -7,  -8,   3,  -1,
      4,   7,  -6,   1,   0,  -5,  -1,  -8,
     13,   8,   8,  10,  13,   0,   2,  -7,
      0,   0,   0,   0,   0,   0,   0,   0,
    ],

    chess.KNIGHT: [
    -58, -38, -13, -28, -31, -27, -63, -99,
    -25,  -8, -25,  -2,  -9, -25, -24, -52,
    -24, -20,  10,   9,  -1,  -9, -19, -41,
    -17,   3,  22,  22,  22,  11,   8, -18,
    -18,  -6,  16,  25,  16,  17,   4, -18,
    -23,  -3,  -1,  15,  10,  -3, -20, -22,
    -42, -20, -10,  -5,  -2, -20, -23, -44,
    -29, -51, -23, -15, -22, -18, -50, -64,
    ],

    chess.BISHOP: [
    -14, -21, -11,  -8, -7,  -9, -17, -24,
     -8,  -4,   7, -12, -3, -13,  -4, -14,
      2,  -8,   0,  -1, -2,   6,   0,   4,
     -3,   9,  12,   9, 14,  10,   3,   2,
     -6,   3,  13,  19,  7,  10,  -3,  -9,
    -12,  -3,   8,  10, 13,   3,  -7, -15,
    -14, -18,  -7,  -1,  4,  -9, -15, -27,
    -23,  -9, -23,  -5, -9, -16,  -5, -17,
    ],

    chess.ROOK: [
    13, 10, 18, 15, 12,  12,   8,   5,
    11, 13, 13, 11, -3,   3,   8,   3,
     7,  7,  7,  5,  4,  -3,  -5,  -3,
     4,  3, 13,  1,  2,   1,  -1,   2,
     3,  5,  8,  4, -5,  -6,  -8, -11,
    -4,  0, -5, -1, -7, -12,  -8, -16,
    -6, -6,  0,  2, -9,  -9, -11,  -3,
    -9,  2,  3, -1, -5, -13,   4, -20,
    ],

    chess.QUEEN: [
     -9,  22,  22,  27,  27,  19,  10,  20,
    -17,  20,  32,  41,  58,  25,  30,   0,
    -20,   6,   9,  49,  47,  35,  19,   9,
      3,  22,  24,  45,  57,  40,  57,  36,
    -18,  28,  19,  47,  31,  34,  39,  23,
    -16, -27,  15,   6,   9,  17,  10,   5,
    -22, -23, -30, -16, -16, -23, -36, -32,
    -33, -28, -22, -43,  -5, -32, -20, -41,
    ],

    chess.KING: [
    -74, -35, -18, -18, -11,  15,   4, -17,
    -12,  17,  14,  17,  17,  38,  23,  11,
     10,  17,  23,  15,  20,  45,  44,  13,
     -8,  22,  24,  27,  26,  33,  26,   3,
    -18,  -4,  21,  24,  27,  23,   9, -11,
    -19,  -3,  11,  21,  23,  16,   7,  -9,
    -27, -11,   4,  13,  14,   4,  -5, -17,
    -53, -34, -21, -11, -28, -14, -24, -43
    ]


}

ENDGAME_OPP_KING_CORNERED_TABLE = [
    100,   95,   90,   85,   85,   90, 95,   100,
    95,   60,   50,   50,   50,   50,  60,   95,
    90,   50,   10,   10,   10,   10,  50,   90,
    85,   50,   10,   -20,   -20,   10,  50,   85,
    85,   50,   10,   -20,   -20,   10,  50,   85,
    90,   50,   10,   10,   10,   10,  50,   90,
    95,   60,   50,   50,   50,   50,  60,   95,
    100,   95,   90,   85,   85,   90,  95,   100,


]

def is_endgame_position(board):
    # Check if there are no major pieces
    no_major_pieces = (
        sum(1 for _ in board.pieces(chess.ROOK, chess.WHITE)) == 0 and
        sum(1 for _ in board.pieces(chess.QUEEN, chess.WHITE)) == 0 and
        sum(1 for _ in board.pieces(chess.ROOK, chess.BLACK)) == 0 and
        sum(1 for _ in board.pieces(chess.QUEEN, chess.BLACK)) == 0
    )
    if no_major_pieces:
        return True

    # Check for two rooks and no queens
    if sum(1 for _ in board.pieces(chess.ROOK, chess.WHITE)) <= 2 and sum(1 for _ in board.pieces(chess.QUEEN, chess.WHITE)) == 0 and sum(1 for _ in board.pieces(chess.QUEEN, chess.BLACK)) == 0:
        return True
    if sum(1 for _ in board.pieces(chess.ROOK, chess.BLACK)) <= 2 and sum(1 for _ in board.pieces(chess.QUEEN, chess.BLACK)) == 0 and sum(1 for _ in board.pieces(chess.QUEEN, chess.WHITE)) == 0:
        return True

    # Check for one queen and no rooks
    if sum(1 for _ in board.pieces(chess.QUEEN, chess.WHITE)) == 1 and sum(1 for _ in board.pieces(chess.ROOK, chess.WHITE)) == 0 and sum(1 for _ in board.pieces(chess.ROOK, chess.BLACK)) == 0:
        return True
    if sum(1 for _ in board.pieces(chess.QUEEN, chess.BLACK)) == 1 and sum(1 for _ in board.pieces(chess.ROOK, chess.BLACK)) == 0 and sum(1 for _ in board.pieces(chess.ROOK, chess.BLACK)) == 0:
        return True

    # Check for two queens, kings, and no other pieces
    if (
        sum(1 for _ in board.pieces(chess.QUEEN, chess.WHITE)) <= 1
        and sum(1 for _ in board.pieces(chess.KING, chess.WHITE)) == 1
        and sum(1 for _ in board.pieces(chess.KNIGHT, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.BISHOP, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.ROOK, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.PAWN, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.QUEEN, chess.BLACK)) <= 1
        and sum(1 for _ in board.pieces(chess.KING, chess.BLACK)) == 1
        and sum(1 for _ in board.pieces(chess.KNIGHT, chess.BLACK)) == 0
        and sum(1 for _ in board.pieces(chess.BISHOP, chess.BLACK)) == 0
        and sum(1 for _ in board.pieces(chess.ROOK, chess.BLACK)) == 0
        and sum(1 for _ in board.pieces(chess.PAWN, chess.BLACK)) == 0
    ):
        return True

    # If none of the above conditions are met, return False
    return False

def evaluate_board(board):

    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -10000
        else:
            return 10000
    if board.can_claim_draw() or board.is_stalemate() or board.is_insufficient_material():
        return 0

    total_evaluation = 0
    if not is_endgame_position(board):
        piece_square_tables = piece_square_tables_middlegame
        piece_values = piece_values_middlegame
    else:
        piece_square_tables = piece_square_tables_endgame
        piece_values = piece_values_endgame

    # Evaluate material
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            color = board.piece_at(square).color
            piece_type = board.piece_at(square).piece_type

            if color == chess.WHITE:
                square_value = piece_square_tables[piece_type][63 - square]
            else:
                square_value = piece_square_tables[piece_type][square]

            total_evaluation += piece_values[piece_type] if color == chess.WHITE else -piece_values[piece_type]
            total_evaluation += square_value if color == chess.WHITE else -square_value

    if is_endgame_position(board):

        # bonus for negating the opponent's king mobility
        opponent_king_square = board.king(chess.BLACK if board.turn == chess.WHITE else chess.WHITE)
        opponent_king_mobility = len(board.attackers(chess.WHITE, opponent_king_square) | board.attackers(chess.BLACK, opponent_king_square))
        total_evaluation -= 35 * opponent_king_mobility  # You can adjust the bonus value

        # King proximity bonus
        own_king_square = board.king(board.turn)
        distance_to_opponent_king = chess.square_distance(own_king_square, opponent_king_square)
        total_evaluation +=  35 * distance_to_opponent_king  # You can adjust the bonus value

        total_evaluation +=  ENDGAME_OPP_KING_CORNERED_TABLE[opponent_king_square]

    return total_evaluation

def is_king_and_rook_endgame(board):
    # Check for 1 rook, kings, and no other pieces
    if (
        sum(1 for _ in board.pieces(chess.QUEEN, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.KING, chess.WHITE)) == 1
        and sum(1 for _ in board.pieces(chess.KNIGHT, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.BISHOP, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.ROOK, chess.WHITE)) == 1
        and sum(1 for _ in board.pieces(chess.PAWN, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.QUEEN, chess.BLACK)) == 0
        and sum(1 for _ in board.pieces(chess.KING, chess.BLACK)) == 1
        and sum(1 for _ in board.pieces(chess.KNIGHT, chess.BLACK)) == 0
        and sum(1 for _ in board.pieces(chess.BISHOP, chess.BLACK)) == 0
        and sum(1 for _ in board.pieces(chess.ROOK, chess.BLACK)) == 0
        and sum(1 for _ in board.pieces(chess.PAWN, chess.BLACK)) == 0
    ):
        return True

    # Check for 1 rook, kings, and no other pieces
    if (
        sum(1 for _ in board.pieces(chess.QUEEN, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.KING, chess.WHITE)) == 1
        and sum(1 for _ in board.pieces(chess.KNIGHT, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.BISHOP, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.ROOK, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.PAWN, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.QUEEN, chess.BLACK)) == 0
        and sum(1 for _ in board.pieces(chess.KING, chess.BLACK)) == 1
        and sum(1 for _ in board.pieces(chess.KNIGHT, chess.BLACK)) == 0
        and sum(1 for _ in board.pieces(chess.BISHOP, chess.BLACK)) == 0
        and sum(1 for _ in board.pieces(chess.ROOK, chess.BLACK)) == 1
        and sum(1 for _ in board.pieces(chess.PAWN, chess.BLACK)) == 0
    ):
        return True

    return False

def is_king_and_queen_endgame(board):
    # Check for 1 rook, kings, and no other pieces
    if (
        sum(1 for _ in board.pieces(chess.QUEEN, chess.WHITE)) == 1
        and sum(1 for _ in board.pieces(chess.KING, chess.WHITE)) == 1
        and sum(1 for _ in board.pieces(chess.KNIGHT, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.BISHOP, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.ROOK, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.PAWN, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.QUEEN, chess.BLACK)) == 0
        and sum(1 for _ in board.pieces(chess.KING, chess.BLACK)) == 1
        and sum(1 for _ in board.pieces(chess.KNIGHT, chess.BLACK)) == 0
        and sum(1 for _ in board.pieces(chess.BISHOP, chess.BLACK)) == 0
        and sum(1 for _ in board.pieces(chess.ROOK, chess.BLACK)) == 0
        and sum(1 for _ in board.pieces(chess.PAWN, chess.BLACK)) == 0
    ):
        return True

    # Check for 1 rook, kings, and no other pieces
    if (
        sum(1 for _ in board.pieces(chess.QUEEN, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.KING, chess.WHITE)) == 1
        and sum(1 for _ in board.pieces(chess.KNIGHT, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.BISHOP, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.ROOK, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.PAWN, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.QUEEN, chess.BLACK)) == 1
        and sum(1 for _ in board.pieces(chess.KING, chess.BLACK)) == 0
        and sum(1 for _ in board.pieces(chess.KNIGHT, chess.BLACK)) == 0
        and sum(1 for _ in board.pieces(chess.BISHOP, chess.BLACK)) == 0
        and sum(1 for _ in board.pieces(chess.ROOK, chess.BLACK)) == 1
        and sum(1 for _ in board.pieces(chess.PAWN, chess.BLACK)) == 0
    ):
        return True

    return False



def quiescence(board, alpha, beta, color, depth):
    if depth == 0 or board.is_game_over():
        return color * evaluate_board(board)

    stand_pat = color * evaluate_board(board)
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    legal_captures = [move for move in board.legal_moves if board.is_capture(move)]

    for move in legal_captures:
        board.push(move)
        score = -quiescence(board, -beta, -alpha, -color, depth - 1)
        board.pop()

        if score >= beta:
            return beta
        if score > alpha:
            alpha = score

    return alpha

def negamax_alpha_beta(board, depth, alpha, beta, color, nodes):
    if depth == 0 or board.is_game_over():
        return quiescence(board, alpha, beta, color, 2), nodes

    legal_moves = list(board.legal_moves)

    for move in legal_moves:
        board.push(move)
        nodes += 1
        value, nodes = negamax_alpha_beta(board, depth - 1, -beta, -alpha, -color, nodes)
        value = -value
        board.pop()
        alpha = max(alpha, value)
        if alpha >= beta:
            break

    if is_king_and_queen_endgame(board) or is_king_and_rook_endgame(board):
        if alpha < beta:
            score = quiescence(board, alpha, beta, color, 2)
            alpha = max(alpha, score)

    return alpha, nodes

def get_best_move(board, depth):
    nodes = 0
    best_move = None
    best_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    legal_moves = list(board.legal_moves)

    if board.turn == chess.WHITE:
      color = 1
    else:
      color = -1

    for move in legal_moves:
        board.push(move)
        nodes += 1
        if board.is_checkmate():
            board.pop()
            return move, 10000, nodes
        else: 
            nodes = 0
            board.pop()

    for move in legal_moves:
        board.push(move)
        nodes += 1
        value, nodes = negamax_alpha_beta(board, depth - 1, -beta, -alpha, -color, nodes)
        value = -value
        board.pop()

        if value > best_value:
            best_value = value
            best_move = move

        alpha = max(alpha, value)

    return best_move, best_value, nodes
    
def calculateMaxTime(board, remaining_time):
    if board.fullmove_number < 15:
        return remaining_time / 60
    elif board.fullmove_number < 30:
        return remaining_time / 40
    else:
        return remaining_time / 50

def calculateMaxDepth(board):
    if is_king_and_rook_endgame(board):
        return 5
    return 3

def uci():
    print("id name Ofish1")
    print("id author Chess123easy")
    print("uciok")


def main():
    board = chess.Board()

    uci_mode = False
    wtime = 1000000
    btime = 1000000
    remainingtime = 1000000

    while True:
        input_line = input()
        if input_line == "uci":
            print("id name OfishV1K")
            print("id author Chess123easy")
            # Include any additional information about your engine
            print("uciok")
            uci_mode = True
        elif input_line == "isready":
            print("readyok")
        elif input_line.startswith("position"):
            parts = input_line.split()
            if len(parts) < 2:
                continue
            position_type = parts[1]
            if position_type == "startpos":
                board.set_fen(chess.STARTING_FEN)
                if len(parts) > 2 and parts[2] == "moves":
                    for move in parts[3:]:
                        board.push_uci(move)
            elif position_type == "fen":
                if len(parts) < 8:
                    continue
                fen = " ".join(parts[2:8])
                board.set_fen(fen)
                if len(parts) > 8 and parts[8] == "moves":
                    for move in parts[9:]:
                        board.push_uci(move)
            position_fen = board.fen()

        elif input_line.startswith("go"):
           if not uci_mode:
              continue

           # Parse additional parameters for search
           parameters = input_line.split()[1:]
           max_time = 0  # Set a default maximum time
           max_depth = 0 # Set a default maximum depth

           for i in range(len(parameters)):
                if parameters[i] == "depth" and i + 1 < len(parameters):
                    max_depth = int(parameters[i + 1])
                elif parameters[i] == "movetime" and i + 1 < len(parameters):
                    max_time = float(parameters[i + 1])
                elif parameters[i] == "wtime" and i + 1 < len(parameters):
                    wtime = float(parameters[i + 1])
                elif parameters[i] == "btime" and i + 1 < len(parameters):
                    btime = float(parameters[i + 1])

           remainingtime = wtime / 1000 if board.turn == chess.WHITE else btime / 1000

           start_time = time.time()  # Start the timer

           depth = 1  # Start with depth 1

           # Inside the while loop in uci_loop function
           while depth <= calculateMaxDepth(board):
                best_move, score, nodes = get_best_move(board, depth)

                # Check if the maximum time has been exceeded
                elapsed_time = time.time() - start_time
                if elapsed_time > calculateMaxTime(board, remainingtime):
                    break

                print(f"info depth {depth} score cp {score} nodes {nodes} pv {best_move}")

                # Increase the search depth for the next iteration
                depth += 1


           # Output the final result
           print("bestmove", best_move.uci())

        elif input_line == "quit":
            break


if __name__ == "__main__":
    main()