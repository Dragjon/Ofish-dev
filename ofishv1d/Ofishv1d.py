import chess
import chess.svg
import time

# Piece values
PIECE_VALUES = {
    chess.PAWN: 82,
    chess.KNIGHT: 337,
    chess.BISHOP: 365,
    chess.ROOK: 477,
    chess.QUEEN: 1025,
    chess.KING: 0,  # The king's value is high to prioritize keeping it safe
}

# Piece Square Tables (example values, you should fine-tune these)
PST_PAWN = [
     0,   0,   0,   0,   0,   0,  0,   0,
    98, 134,  61,  95,  68, 126, 34, -11,
    -6,   7,  26,  31,  65,  56, 25, -20,
    -14,  13,   6,  21,  23,  12, 17, -23,
    -27,  -2,  -5,  12,  17,   6, 10, -25,
    -26,  -4,  -4, -10,   3,   3, 33, -12,
    -35,  -1, -20, -23, -15,  24, 38, -22,
    0,   0,   0,   0,   0,   0,  0,   0,
]

PST_KNIGHT = [
    -167, -89, -34, -49,  61, -97, -15, -107,
    -73, -41,  72,  36,  23,  62,   7,  -17,
    -47,  60,  37,  65,  84, 129,  73,   44,
    -9,  17,  19,  53,  37,  69,  18,   22,
    -13,   4,  16,  13,  28,  19,  21,   -8,
    -23,  -9,  12,  10,  19,  17,  25,  -16,
    -29, -53, -12,  -3,  -1,  18, -14,  -19,
    -105, -21, -58, -33, -17, -28, -19,  -23,
]

PST_BISHOP = [
    -14, -21, -11,  -8, -7,  -9, -17, -24,
    -8,  -4,   7, -12, -3, -13,  -4, -14,
    2,  -8,   0,  -1, -2,   6,   0,   4,
    -3,   9,  12,   9, 14,  10,   3,   2,
    -6,   3,  13,  19,  7,  10,  -3,  -9,
    -12,  -3,   8,  10, 13,   3,  -7, -15,
    -14, -18,  -7,  -1,  4,  -9, -15, -27,
    -23,  -9, -23,  -5, -9, -16,  -5, -17,
]

PST_ROOK = [
    32,  42,  32,  51, 63,  9,  31,  43,
    27,  32,  58,  62, 80, 67,  26,  44,
    -5,  19,  26,  36, 17, 45,  61,  16,
    -24, -11,   7,  26, 24, 35,  -8, -20,
    -36, -26, -12,  -1,  9, -7,   6, -23,
    -45, -25, -16, -17,  3,  0,  -5, -33,
    -44, -16, -20,  -9, -1, 11,  -6, -71,
    -19, -13,   1,  17, 16,  7, -37, -26,
]

PST_QUEEN = [
    -28,   0,  29,  12,  59,  44,  43,  45,
    -24, -39,  -5,   1, -16,  57,  28,  54,
    -13, -17,   7,   8,  29,  56,  47,  57,
    -27, -27, -16, -16,  -1,  17,  -2,   1,
    -9, -26,  -9, -10,  -2,  -4,   3,  -3,
    -14,   2, -11,  -2,  -5,   2,  14,   5,
    -35,  -8,  11,   2,   8,  15,  -3,   1,
    -1, -18,  -9,  10, -15, -25, -31, -50,
]

PST_KING = [
    # Standard King PST
     -65,  23,  16, -15, -56, -34,   2,  13,
      29,  -1, -20,  -7,  -8,  -4, -38, -29,
      -9,  24,   2, -16, -20,   6,  22, -22,
      -17, -20, -12, -27, -30, -25, -14, -36,
      -49,  -1, -27, -39, -46, -44, -33, -51,
      -14, -14, -22, -46, -44, -30, -15, -27,
      1,   7,  -8, -64, -43, -16,   9,   8,
      -15,  36,  12, -54,   8, -28,  24,  14,
]

PST_KING_ENDGAME = [
    # King PST for Endgame
    -74, -35, -18, -18, -11,  15,   4, -17,
    -12,  17,  14,  17,  17,  38,  23,  11,
    10,  17,  23,  15,  20,  45,  44,  13,
    -8,  22,  24,  27,  26,  33,  26,   3,
    -18,  -4,  21,  24,  27,  23,   9, -11,
    -19,  -3,  11,  21,  23,  16,   7,  -9,
    -27, -11,   4,  13,  14,   4,  -5, -17,
    -53, -34, -21, -11, -28, -14, -24, -43,
]

def evaluate_board(board):
    score = 0

    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return float('-inf')
        else:
            return float('inf')

    if board.can_claim_draw() or board.is_stalemate() or board.is_insufficient_material():
        return 0

    # Evaluate material
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            # Adjust the sign for black pieces
            sign = 1 if piece.color == chess.WHITE else -1

            # Evaluate piece values
            score += sign * (PIECE_VALUES[piece.piece_type] + get_pst_value(piece.piece_type, square, board))

            # Bonus for open files for rooks and queens
            if piece.piece_type in [chess.ROOK, chess.QUEEN]:
                file_mask = chess.BB_FILES[chess.square_file(square)]
                if not (file_mask & board.occupied_co[chess.WHITE] | board.occupied_co[chess.BLACK]):
                    score += sign * 10  # You can adjust the bonus value

    # Check bonus
    if board.is_check():
        if board.turn == chess.WHITE:
           score -= 60  # You can adjust the bonus value
        else:
           score += 60

    return score


def is_endgame_position(board):
    # Check if there are no major pieces
    major_pieces = (
        board.pieces(chess.ROOK, chess.WHITE) |
        board.pieces(chess.QUEEN, chess.WHITE) |
        board.pieces(chess.ROOK, chess.BLACK) |
        board.pieces(chess.QUEEN, chess.BLACK)
    )
    if not major_pieces:
        return True

    # Check for two rooks and no queens
    if sum(1 for _ in board.pieces(chess.ROOK, chess.WHITE)) == 2 and sum(1 for _ in board.pieces(chess.QUEEN, chess.WHITE)) == 0:
        return True
    if sum(1 for _ in board.pieces(chess.ROOK, chess.BLACK)) == 2 and sum(1 for _ in board.pieces(chess.QUEEN, chess.BLACK)) == 0:
        return True

    # Check for one queen and no rooks
    if sum(1 for _ in board.pieces(chess.QUEEN, chess.WHITE)) == 1 and sum(1 for _ in board.pieces(chess.ROOK, chess.WHITE)) == 0:
        return True
    if sum(1 for _ in board.pieces(chess.QUEEN, chess.BLACK)) == 1 and sum(1 for _ in board.pieces(chess.ROOK, chess.BLACK)) == 0:
        return True

    # Check for two queens, kings, and no other pieces
    if (
        sum(1 for _ in board.pieces(chess.QUEEN, chess.WHITE)) == 2
        and sum(1 for _ in board.pieces(chess.KING, chess.WHITE)) == 2
        and sum(1 for _ in board.pieces(chess.KNIGHT, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.BISHOP, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.ROOK, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.PAWN, chess.WHITE)) == 0
        and sum(1 for _ in board.pieces(chess.QUEEN, chess.BLACK)) == 2
        and sum(1 for _ in board.pieces(chess.KING, chess.BLACK)) == 2
        and sum(1 for _ in board.pieces(chess.KNIGHT, chess.BLACK)) == 0
        and sum(1 for _ in board.pieces(chess.BISHOP, chess.BLACK)) == 0
        and sum(1 for _ in board.pieces(chess.ROOK, chess.BLACK)) == 0
        and sum(1 for _ in board.pieces(chess.PAWN, chess.BLACK)) == 0
    ):
        return True

    # If none of the above conditions are met, return False
    return False



def get_pst_value(piece_type, square, board):
    if piece_type == chess.PAWN:
        return PST_PAWN[square]
    elif piece_type == chess.KNIGHT:
        return PST_KNIGHT[square]
    elif piece_type == chess.BISHOP:
        return PST_BISHOP[square]
    elif piece_type == chess.ROOK:
        return PST_ROOK[square]
    elif piece_type == chess.QUEEN:
        return PST_QUEEN[square]
    elif piece_type == chess.KING:
        # Use endgame king PST if the game is in the endgame
        if is_endgame_position(board):
            return PST_KING_ENDGAME[square]
        else:
            return PST_KING[square]
    return 0


def quiescence_search(board, alpha, beta, color, depth):
    if depth == 0:
        return color * evaluate_board(board)

    stand_pat = color * evaluate_board(board)

    if stand_pat >= beta:
        return beta

    if alpha < stand_pat:
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiescence_search(board, -beta, -alpha, -color, depth - 1)
            board.pop()

            if score >= beta:
                return beta

            if score > alpha:
                alpha = score

    return alpha

def mvv_lva_ordering(moves, board):
    def mvv_lva_score(move):
        # MVV-LVA score: Value of the captured piece - Value of the capturing piece
        capturing_piece = board.piece_type_at(move.from_square)
        captured_piece = board.piece_type_at(move.to_square)

        # Handle None values (empty squares)
        capturing_value = PIECE_VALUES.get(capturing_piece, 0)
        captured_value = PIECE_VALUES.get(captured_piece, 0)

        return captured_value - capturing_value


    return sorted(moves, key=mvv_lva_score, reverse=True)


def negamax(board, depth, alpha, beta, color):
    if depth == 0 or board.is_game_over():
       if board.is_capture(board.peek()):
          # Introduce quiescence search for captures
          return quiescence_search(board, alpha, beta, color, 3)

       else:
          return color * evaluate_board(board)


    max_score = float('-inf')
    for move in board.legal_moves:
        board.push(move)
        score = -negamax(board, depth - 1, -beta, -alpha, -color)
        board.pop()

        max_score = max(max_score, score)
        alpha = max(alpha, score)
        if alpha >= beta:
            break

    return max_score


def get_best_move(board, depth):
    for move in board.legal_moves:
        board.push(move)

        # Check if the move results in a checkmate
        if board.is_checkmate():
            board.pop()
            return move

        board.pop()

    # If no immediate checkmate, use the original minimax logic
    best_move = None
    max_score = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    if board.turn == chess.WHITE:
      color = 1
    else:
      color = -1

    for move in board.legal_moves:
        board.push(move)
        score = -negamax(board, depth - 1, -beta, -alpha, -color)
        board.pop()

        if score > max_score:
            max_score = score
            best_move = move

        alpha = max(alpha, score)

    return best_move



def calculateMaxTime(board, remaining_time):
    if board.fullmove_number < 15:
        return remaining_time / 60
    elif board.fullmove_number < 30:
        return remaining_time / 40
    else:
        return remaining_time / 50

def calculateMaxDepth(board):
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
            print("id name Ofish1")
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
                best_move = get_best_move(board, depth)

                # Check if the maximum time has been exceeded
                elapsed_time = time.time() - start_time
                if elapsed_time > calculateMaxTime(board, remainingtime):
                    break

                print(f"info depth {depth} wtime {wtime} btime {btime}")

                # Increase the search depth for the next iteration
                depth += 1


           # Output the final result
           print("bestmove", best_move.uci())

        elif input_line == "quit":
            break


if __name__ == "__main__":
    main()