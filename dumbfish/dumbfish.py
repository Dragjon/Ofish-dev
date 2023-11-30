import chess
import time

# Constants for evaluation weights
MATERIAL_WEIGHT = 1
MOBILITY_WEIGHT = 0.66
CASTLING_WEIGHT = 0.55
KING_SHIELD_WEIGHT = 0.43
PAWN_STRUCTURE_WEIGHT = 0.33

# Evaluate material balance
def evaluate_material(board):
    material_score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
          if piece.color == chess.WHITE:
            material_score += piece_value(piece)
          else:
            material_score -= piece_value(piece)
    return material_score

# Assign values to chess pieces
def piece_value(piece):
    if piece.piece_type == chess.PAWN:
        return 10
    elif piece.piece_type == chess.KNIGHT:
        return 32.5
    elif piece.piece_type == chess.BISHOP:
        return 32.5
    elif piece.piece_type == chess.ROOK:
        return 50
    elif piece.piece_type == chess.QUEEN:
        return 90
    elif piece.piece_type == chess.KING:
        return 0

# Evaluate piece mobility
def evaluate_mobility(board):
    legal_moves = list(board.legal_moves)
    return len(legal_moves)

# Evaluate castling
def evaluate_castling(board):
    castling_score = 0

    # Check if the king has castled
    if board.has_queenside_castling_rights(chess.WHITE) and any(
        move.uci() == "e1c1" for move in board.move_stack
    ):
        castling_score += 1

    if board.has_kingside_castling_rights(chess.WHITE) and any(
        move.uci() == "e1g1" for move in board.move_stack
    ):
        castling_score += 1

    if board.has_queenside_castling_rights(chess.BLACK) and any(
        move.uci() == "e8c8" for move in board.move_stack
    ):
        castling_score -= 1

    if board.has_kingside_castling_rights(chess.BLACK) and any(
        move.uci() == "e8g8" for move in board.move_stack
    ):
        castling_score -= 1

    return castling_score


# Evaluate king pawn shield bonus
def evaluate_king_shield(board):
    king_sq = board.king(chess.WHITE) if board.turn == chess.WHITE else board.king(chess.BLACK)
    king_file, king_rank = chess.square_file(king_sq), chess.square_rank(king_sq)
    
    shield_squares = [
        chess.square(king_file + 1, king_rank),  # East
        chess.square(king_file + 1, king_rank + 1),  # Northeast
        chess.square(king_file + 1, king_rank - 1),  # Northwest
    ]
    
    shield_bonus = sum(
        1 for sq in shield_squares if chess.square_file(sq) in range(8) and chess.square_rank(sq) in range(8) and board.piece_at(sq) == chess.PAWN
    )
    return shield_bonus


# Evaluate pawn structure
def evaluate_pawn_structure(board):
    pawn_structure_score = 0
    for file in range(chess.FILE_NAMES.index('a'), chess.FILE_NAMES.index('h') + 1):
        pawns_on_file = [board.piece_at(chess.square(file, rank)) for rank in range(chess.RANK_NAMES.index('1'), chess.RANK_NAMES.index('8') + 1)]
        if all(p == chess.PAWN for p in pawns_on_file):
            pawn_structure_score += 1
    return pawn_structure_score



# Evaluate the position
def evaluate_position(board):

    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return float('-inf')
        else:
            return float('inf')

    if board.can_claim_draw() or board.is_stalemate() or board.is_insufficient_material():
        return 0

    material_score = evaluate_material(board)
    mobility_score = evaluate_mobility(board)
    castling_score = evaluate_castling(board)
    king_shield_score = evaluate_king_shield(board)
    pawn_structure_score = evaluate_pawn_structure(board)

    position_score = (
        MATERIAL_WEIGHT * material_score +
        MOBILITY_WEIGHT * mobility_score +
        CASTLING_WEIGHT * castling_score +
        KING_SHIELD_WEIGHT * king_shield_score +
        PAWN_STRUCTURE_WEIGHT * pawn_structure_score
    )
    return position_score

# Find the best move using minimax algorithm
def find_best_move(board, depth):
    legal_moves = list(board.legal_moves)
    for move in board.legal_moves:
        board.push(move)

        # Check if the move results in a checkmate
        if board.is_checkmate():
            board.pop()
            return move, 9999

        board.pop()

    best_move = None
    best_eval = float('-inf')

    for move in legal_moves:
        board.push(move)
        eval = -minimax(board, depth - 1)
        if eval > best_eval:
            best_eval = eval
            best_move = move
        board.pop()

    return best_move, eval


# Quiescence search
def quiescence_search(board, alpha, beta, depth):
    stand_pat = evaluate_position(board)
    
    if depth == 0 or board.is_game_over():
        return stand_pat

    legal_captures = [move for move in board.legal_moves if board.is_capture(move)]
    
    for move in legal_captures:
        board.push(move)
        eval = -quiescence_search(board, -beta, -alpha, depth - 1)
        board.pop()

        stand_pat = max(stand_pat, eval)
        alpha = max(alpha, eval)
        if alpha >= beta:
            break  # Alpha-beta pruning

    return stand_pat

# Minimax algorithm with alpha-beta pruning and quiescence search
def minimax(board, depth, alpha=float('-inf'), beta=float('inf')):
    if depth == 0 or board.is_game_over():
        return quiescence_search(board, alpha, beta, 3)

    legal_moves = list(board.legal_moves)

    for move in legal_moves:
        board.push(move)
        eval = -minimax(board, depth - 1, -beta, -alpha)
        board.pop()

        alpha = max(alpha, eval)
        if alpha >= beta:
            break  # Alpha-beta pruning

    return alpha

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
           global checkmate_depth
           checkmate_depth = 1

           # Inside the while loop in uci_loop function
           while depth <= calculateMaxDepth(board):
                best_move, score = find_best_move(board, depth)
                checkmate_depth = depth

                # Check if the maximum time has been exceeded
                elapsed_time = time.time() - start_time
                if elapsed_time > calculateMaxTime(board, remainingtime):
                    break

                print(f"info depth {depth} score cp {score}")

                # Increase the search depth for the next iteration
                depth += 1


           # Output the final result
           print("bestmove", best_move.uci())

        elif input_line == "quit":
            break


if __name__ == "__main__":
    main()
