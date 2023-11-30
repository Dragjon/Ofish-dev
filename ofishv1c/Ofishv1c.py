import chess
import chess.svg
import time

# Piece values
PIECE_VALUES = {
    chess.PAWN: 90,
    chess.KNIGHT: 202,
    chess.BISHOP: 214,
    chess.ROOK: 373,
    chess.QUEEN: 600,
    chess.KING: 10000,  # The king's value is high to prioritize keeping it safe
}

# highest value 100, lowest value 100
# Piece Square Tables (example values, you should fine-tune these)
PST_PAWN = [
    0,   0,   0,   0,   0,   0,  0,   0,
    60,   60,   55,   55,   55,   50,  60,   60,
    25,   20,   40,   45,   45,   20,  10,   25,
    10,   5,   30,   40,   40,   5,  -5,   10,
    10,   -20,   45,   50,   50,   5,  -20,   10,
    10,   10,   10,   5,   5,   -30,  20,   25,
    5,   5,   5,   -20,   -20,   10,  10,   10,
    0,   0,   0,   0,   0,   0,  0,   0,
]

PST_KNIGHT = [
    10,   -10,   10,   5,   10,   10,  -5,   -30,
    -5,   5,   10,   5,   15,   10,  0,   5,
    5,   20,   30,   50,   50,   30,  10,   10,
    0,   20,   45,   40,   40,   45,  20,   -5,
    -20,   10,   30,   45,   45,   30,  10,   -20,
    -5,   10,   35,   0,   0,   35,  20,   -5,
    5,   0,   5,   10,   10,   5,  5,   15,
    -50,   -30,   -5,   5,   5,   10,  -30,   -50,
]

PST_BISHOP = [
    -5,   -5,   -5,   -5,   -5,   -5,  -5,   -5,
    -5,   5,   0,   5,   5,   0,  5,   5,
    0,   0,   10,   0,   0,   15,  0,   0,
    5,   20,   0,   10,   10,   0,  30,   0,
    25,   5,   30,   10,   10,   25,  0,   20,
    -5,   10,   20,   10,   5,   0,  25,   0,
    5,   20,   35,   20,   20,   5,  20,   20,
    -5,   25,   -20,   0,   0,   -25,  -10,   -5,
]

PST_ROOK = [
    15,   15,   15,   15,   15,   15,  15,   15,
    15,   15,   15,   20,   20,   15,  15,   15,
    0,   5,   5,   10,   10,   5,  5,   0,
    0,   0,   0,   5,   5,   0,  0,   0,
    0,   0,   0,   5,   5,   0,  0,   0,
    0,   0,   0,   5,   5,   0,  0,   0,
    -5,   0,   0,   0,   0,   0,  0,   -5,
    -10,   0,   5,   10,   10,   5,  0,   -10,
]

PST_QUEEN = [
    0,   0,   0,   0,   0,   0,  0,   0,
    0,   5,   0,   0,   0,   0,  0,   0,
    0,   0,   0,   0,   0,   0,  0,   0,
    0,   0,   -5,   5,   5,   0,  0,   0,
    0,   0,   5,   5,   5,   5,  0,   0,
    0,   10,   0,   5,   0,   5,  5,   0,
    0,   0,   5,   5,   10,   0,  0,   0,
    0,   0,   0,   -5,   0,   0,  0,   0,
]

PST_KING = [
    # Standard King PST
    -90,   -80,   -80,   -80,   -80,   -80,  -80,   -90,
    -70,   -70,   -70,   -70,   -70,   -70,  -70,   -70,
    -60,   -60,   -60,   -70,   -70,   -60,  -60,   -50,
    -50,   -50,   -50,   -60,   -60,   -50,  -50,   -50,
    -40,   -40,   -40,   -60,   -60,   -40,  -40,   -40,
    -30,   -30,   -30,   -50,   -50,   -30,  -30,   -30,
   5,   5,   -20,   -20,   -30,   -20,  5,   5,
    -5,   70,   60,   0,   -10,   10,  70,   10,
]

PST_KING_ENDGAME = [
    # King PST for Endgame
    20,   20,   20,   25,   25,   20,  20,   20,
    20,   25,   25,   30,   30,   25,  25,   20,
    15,   20,   40,   50,  50,   40,  20,   15,
    10,   15,   50,   60,   60,   50,  15,   10,
    10,   10,   40,   60,   60,   40,  10,   5,
    5,   10,   35,   40,   40,   35,  10,   5,
    -20,   5,   10,   30,   30,   20,  10,   -10,
    -60,   -50,   -40,   -15,   -15,   -35,  -40,   -50,
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