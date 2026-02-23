"""
FILE OVERALL SUMMARY
"""

# chess imports
import chess
import chess.pgn
from stockfish import Stockfish
from program_timer import start_timer
from eco_codes import ECO_CODES, eco_code_to_opening_name

# general imports
import os
import sys
import time
import pandas as pd
import multiprocessing
import traceback
from io import StringIO

# race condition imports
from multiprocessing import cpu_count, Process

PGN_FILE_NAME = os.environ.get("PGN_FILE_NAME", None) # PGN file with N games
PVP_FILE_NAME = os.environ.get("PVP_FILE_NAME", None) # Final aggregate piece val parquet
SF_PATH = os.environ.get("SF_PATH", None) # the big fish
NUM_WORKERS = int(os.environ.get("NUM_WORKERS", min(cpu_count(), 1))) # number of cores

env_var_list = [PGN_FILE_NAME, PVP_FILE_NAME, SF_PATH] # for checking in main()

# Stockfish config
STOCKFISH_DEPTH = 20
STOCKFISH_TIMEOUT = 300 # seconds

# Function to get material string for a given color in a given position
# ex) 3 pawns, 1 queen, 1 king = 'pppQK'
def get_material_string(board, color):
    """
    Function to get material string for a given color in a given position
    ex) 3 pawns, 1 queen, 1 king = 'pppQK'
    Note that formatting of material strings is diff. from 'piece_type' which uses White - PNBRQ, Black - pnbrq
    Also note that this information is implictly present in FEN strings
    """
    # Check that board and color are not empty
    if board is None:
        print(f"Error: Board is empty - board={board}")
        return ""
    if color is None:
        print(f"Error: No color provided - color={color}")
        return ""

    piece_symbols = {
        chess.PAWN: 'p',
        chess.KNIGHT: 'N',
        chess.BISHOP: 'B',
        chess.ROOK: 'R',
        chess.QUEEN: 'Q',
        chess.KING: 'K'
    }
    material = []

    # Populate material list
    for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]:
        squares = board.pieces(piece_type, color)
        for _ in squares:
            material.append(piece_symbols[piece_type])

    return ''.join(material)

# Read all games from PGN file and convert to strings for distribution
def load_games_from_pgn(pgn_file_name):
    """
    Load all games from PGN file and convert each to a string.
    Returns a list of (game_index, game_pgn_string, eco_code) tuples.
    """
    print(f"Loading games from {pgn_file_name}")
    games = []

    # Open PGN file and read games
    with open(pgn_file_name, encoding="utf-8", errors="ignore") as pgn:
        game_index = 0
        # Continue reading games as long as there are more games to read
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break

            # Extract ECO code from game headers
            eco_code = game.headers.get("ECO", "")

            # Convert game to string for serialization
            exporter = chess.pgn.StringExporter(headers=True, variations=False, comments=False)
            game_str = game.accept(exporter)

            # Add (game_index, game_pgn_string, eco_code) to list of games
            games.append((game_index, game_str, eco_code))
            game_index += 1

            if game_index % 1000 == 0:
                print(f"Loaded {game_index} games from PGN file")

    print(f"Finished loading {len(games)} games from {pgn_file_name}")
    return games

# Module-level worker function for Stockfish evaluation (some Windows shenanigans)
def _eval_worker(result_queue, stockfish_path, fen, depth):
    """Worker function to run Stockfish in separate process"""
    try:
        sf = Stockfish(path=stockfish_path)
        sf._set_option("Threads", 1)
        sf.set_depth(depth_value=depth)
        # Evaluate current position given in FEN and store eval in result_queue
        sf.set_fen_position(fen)
        eval_result = sf.get_evaluation()
        result_queue.put({'eval_result': eval_result})
    except Exception as e:
        result_queue.put({'error': str(e)})

# Helper function to run Stockfish evaluation with timeout
def evaluate_with_timeout(stockfish, fen, timeout=60):
    """
    Evaluate position with Stockfish with a timeout of X seconds.
    Returns centipawn evaluation for non-static positions (valid, non-solved/mate positions)
    Returns None for mate positions/timeout/error
    """

    # This is very convoluted but basically you need to do this messiness of storing results in a separate queue to run multiprocessing on Windows
    result_queue = multiprocessing.Queue()
    # Get stockfish path with multiple attributes to handle different versions
    if hasattr(stockfish, 'path'):
        stockfish_path = stockfish.path
    elif hasattr(stockfish, '_path'):
        stockfish_path = stockfish._path
    else:
        # Fallback to name-mangled attribute for older versions
        stockfish_path = getattr(stockfish, '_Stockfish__stockfish_path', None)
        if stockfish_path is None:
            raise AttributeError("Could not find stockfish path attribute")

    # Start process to evaluate a FEN (position) at X depth using SF
    eval_process = multiprocessing.Process(
        target=_eval_worker,
        args=(result_queue, stockfish_path, fen, STOCKFISH_DEPTH)
    )
    eval_process.start()
    eval_process.join(timeout=timeout)

    # Check if process is still alive after attempt to join
    if eval_process.is_alive():
        # Timeout occurred, end process
        eval_process.terminate()
        eval_process.join()
        return None

    # Get result from eval process worker
    try:
        result = result_queue.get_nowait()
        if 'error' in result:
            # Timeout occurred
            return None

        eval_result = result['eval_result']
        if eval_result["type"] == "mate":
            # Static/invalid position
            return None
        else:
            # Valid eval of position with value that we can actually use
            return eval_result["value"]
    except:
        return None

# Function to check if board is valid
def is_board_valid(board):
    """Check if board is valid (a live game with a non-static eval) for piece value calculation"""
    if not board.is_valid():
        return False
    if board.is_checkmate() or board.is_stalemate():
        return False
    if board.legal_moves.count() == 0:
        return False
    return True

# Worker function that processes a slice of games
def process_games_worker(worker_id, games_slice, output_file, sf_path):
    """
    Each worker:
    1. Receives a slice of games to process
    2. For each game, processes all positions
    3. For each position, calculates piece values by removing each piece from the position and calculates its value as the change in SF evaluation from the og position
    4. Writes results to its own parquet file

    Piece value data collected per piece:
    - game_id: String format "w{worker_id}_g{game_num}"
    - fen: FEN string
    - move_number: Move number in the game
    - side_to_move: White or Black ('w' or 'b')
    - eco_code: ECO code
    - opening: Opening name from ECO code
    - white_material: Material string for white
    - black_material: Material string for black
    - piece_type: Piece symbol (White - PNBRQ, Black - pnbrq)
    - rank: Rank (0-7)
    - file: File (0-7)
    - original_eval: Stockfish eval of position with piece present (original position)
    - eval_without_piece: Stockfish eval of position with piece removed (position with piece removed)
    - piece_value: Difference between two evals (original_eval - eval_without_piece)
    """
    print(f"Worker {worker_id}: Starting with {len(games_slice)} games, Stockfish depth={STOCKFISH_DEPTH}, timeout={STOCKFISH_TIMEOUT}s")

    # Initialize Stockfish for this worker
    stockfish = Stockfish(path=sf_path)
    stockfish._set_option("Threads", 1)
    stockfish.set_depth(depth_value=STOCKFISH_DEPTH)

    # Vars to store various stats that are useful
    all_piece_data = []
    processed_games = 0
    total_positions = 0
    total_pieces = 0
    timeouts = 0

    # For each game to be processed...
    for game_num, (original_game_index, game_pgn_str, game_eco_code) in enumerate(games_slice):
        # Set unique id based on what worker was assigned to it
        game_id = f"w{worker_id}_g{game_num}"
        print(f"Worker {worker_id}: Starting game {game_id} (original index {original_game_index})")

        try:
            # Parse the PGN string into a game object
            pgn_io = StringIO(game_pgn_str)
            game = chess.pgn.read_game(pgn_io)

            # Flee if there is no game
            if game is None:
                continue

            # Get game's opening name from ECO code
            opening = eco_code_to_opening_name(game_eco_code)

            # Create board object to flick through game moves one by one
            board = game.board()
            move_no = 0

            # For each unique game position (for each position after making a move)...
            for move in game.mainline_moves():
                board.push(move)
                move_no += 1
                
                # Get current position as FEN
                fen = board.fen()

                # Get side to move ('w' or 'b')
                side_to_move = 'w' if board.turn == chess.WHITE else 'b'

                # Get material strings
                white_material = get_material_string(board, chess.WHITE)
                black_material = get_material_string(board, chess.BLACK)

                # Get og position's SF evaluation (used in all pval calcs for each unique non-K piece)
                og_eval = evaluate_with_timeout(stockfish, fen, timeout=STOCKFISH_TIMEOUT)

                # Check if position is static/non-static
                if og_eval is None:
                    # Timeout or mate position - skip this position entirely
                    timeouts += 1
                    continue

                total_positions += 1
                position_pieces = 0

                # For each square in the current position...
                for square in chess.SQUARES:
                    # Check if there is a piece at the current square being processed
                    piece = board.piece_at(square)
                    if not piece:
                        continue

                    # Skip kings
                    if piece.symbol().upper() == 'K':
                        continue
                    
                    # If there is a piece at the current square of interest...
                    # Create position with piece of interest removed
                    board_rm = board.copy()
                    board_rm.remove_piece_at(square)

                    # Check and skip if removing piece causes an illegal position
                    if not is_board_valid(board_rm):
                        continue
                    
                    # Get position with removed piece as FEN
                    fen_rm = board_rm.fen()

                    # Get new SF evaluation of position without piece of interest
                    rm_eval = evaluate_with_timeout(stockfish, fen_rm, timeout=STOCKFISH_TIMEOUT)

                    # Check if evaluating new position was successful
                    if rm_eval is None:
                        # Timeout or invalid position
                        timeouts += 1
                        continue

                    # Calculate piece value
                    piece_value = og_eval - rm_eval

                    # Get rank and file (0-7)
                    rank = chess.square_rank(square)
                    file = chess.square_file(square)

                    # Create pval data entry (a row)
                    piece_data = {
                        'game_id': game_id,
                        'fen': fen,
                        'move_number': move_no,
                        'side_to_move': side_to_move,
                        'eco_code': game_eco_code,
                        'opening': opening,
                        'white_material': white_material,
                        'black_material': black_material,
                        'piece_type': piece.symbol(),
                        'rank': rank,
                        'file': file,
                        'original_eval': og_eval,
                        'eval_without_piece': rm_eval,
                        'piece_value': piece_value,
                    }

                    # Add new pval entry to aggregate pval data
                    all_piece_data.append(piece_data)
                    total_pieces += 1
                    position_pieces += 1

                # Print message after processing position
                # print(f"Worker {worker_id}: Finished position (move {move_no}), evaluated {position_pieces} pieces")
            
            # Print confirmation message for a worker after finishing each game with piece count
            processed_games += 1
            print(f"Worker {worker_id}: Finished game {game_id}, found {len([d for d in all_piece_data if d['game_id'] == game_id])} pieces")

            # Print confirmation message for worker every X games processed
            if processed_games % 50 == 0:
                print(f"Worker {worker_id}: Processed {processed_games}/{len(games_slice)} games, {total_positions} positions, {total_pieces} pieces, {timeouts} timeouts")

        except Exception as e:
            print(f"Worker {worker_id}: Error processing game {game_id}: {e}")
            continue
    
    # Print confirmation message after worker finishes processing all games with stats
    print(f"Worker {worker_id}: Finished processing all games. Writing to {output_file}")
    print(f"Worker {worker_id}: Stats - {processed_games} games, {total_positions} positions, {total_pieces} pieces, {timeouts} timeouts")

    # Write results to worker's parquet file
    if all_piece_data:
        df = pd.DataFrame(all_piece_data)
        df.to_parquet(output_file, compression='lz4', index=False, engine='pyarrow')
        print(f"Worker {worker_id}: Wrote {len(df)} piece values to {output_file}")
    else:
        print(f"Worker {worker_id}: No piece data to write")

def main():
    # Validate env variables
    print("Checking all env variables are valid")
    for var in env_var_list:
        if var is None:
            print(f"Error: At least one environment variable is None. Exiting immediately my liege!")
            sys.exit(1)

    # Validate NUM_WORKERS
    if NUM_WORKERS < 1:
        print(f"Error: NUM_WORKERS must be >= 1, got {NUM_WORKERS}")
        sys.exit(1)

    # CONFIG
    print(f"=== Configuration ===")
    print(f"Workers: {NUM_WORKERS}")
    print(f"Stockfish depth: {STOCKFISH_DEPTH}")
    print(f"Stockfish timeout: {STOCKFISH_TIMEOUT}s")
    print(f"Stockfish threads per instance: 1")
    print(f"PGN file: {PGN_FILE_NAME}")
    print(f"Output file: {PVP_FILE_NAME}")
    print("=" * 20)

    # Start program timer
    print("Starting program timer thread for pgn_to_piecevals.py")
    start_timer(thread_update_time_secs=60)

    print(f"Starting conversion from PGN->PieceVals from {PGN_FILE_NAME}->{PVP_FILE_NAME}")

    # Convert PGNs to PVal data
    try:
        # Load all games from PGN file
        games = load_games_from_pgn(pgn_file_name=PGN_FILE_NAME)

        # Check that there are games to process
        if not games:
            print("No games found in PGN file!")
            sys.exit(1)

        # Split games evenly across workers
        total_games = len(games)
        games_per_worker = total_games // NUM_WORKERS
        remainder = total_games % NUM_WORKERS

        print(f"\n=== Game Distribution ===")
        print(f"Total games: {total_games}")
        print(f"Games per worker (base): {games_per_worker}")
        print(f"Extra games to distribute: {remainder}")
        print("=" * 20)

        # Create game slices for each worker
        game_slices = []
        start_idx = 0
        for i in range(NUM_WORKERS):
            # Give one extra game to first 'remainder' workers
            slice_size = games_per_worker + (1 if i < remainder else 0)
            end_idx = start_idx + slice_size
            game_slices.append(games[start_idx:end_idx])
            print(f"Worker {i}: {slice_size} games (indices {start_idx}-{end_idx-1})")
            start_idx = end_idx

        # Create directory for temp worker output files
        temp_dir = "temp_piecevals"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        print(f"\nWorker outputs directory: {temp_dir}")

        # Initialize worker processes
        workers = []
        worker_output_files = []
        start_time = time.time()

        # Create temp worker output files
        for i in range(NUM_WORKERS):
            output_file = os.path.join(temp_dir, f"worker_{i}.parquet")
            worker_output_files.append(output_file)
            # Start workers
            p = Process(target=process_games_worker,
                       args=(i, game_slices[i], output_file, SF_PATH))
            p.start()
            workers.append(p)
        print(f"\nStarted {NUM_WORKERS} workers")

        # Wait for all workers to finish
        print("\nWaiting for workers to complete...")
        for i, worker in enumerate(workers):
            worker.join()
            if worker.exitcode == 0:
                print(f"Worker {i} completed successfully")
            else:
                print(f"Worker {i} exited with code {worker.exitcode}")

        # Print time stats
        elapsed_time = time.time() - start_time
        print(f"\nAll workers finished in {elapsed_time:.1f} seconds")

        # Merge all worker parquet files
        print("\n=== Merging worker outputs ===")
        all_dfs = []
        total_pieces = 0

        # Append individual worker files to final PVal DF array
        for i, output_file in enumerate(worker_output_files):
            if os.path.exists(output_file):
                df = pd.read_parquet(output_file)
                all_dfs.append(df)
                # Track total pvals gathered
                total_pieces += len(df)
                print(f"Worker {i}: {len(df)} piece values")
            else:
                print(f"Worker {i}: No output file found")

        # Check that final pval DF array is not empty
        if not all_dfs:
            print("ERROR: No piece data collected from any worker!")
            sys.exit(1)

        # Concatenate all worker DFs
        print("\nConcatenating all dataframes...")
        final_df = pd.concat(all_dfs, ignore_index=True)
        print(f"Total piece values: {len(final_df)}")

        # Save final parquet file
        print(f"\nSaving final output to {PVP_FILE_NAME}")
        final_df.to_parquet(PVP_FILE_NAME, compression='lz4', index=False, engine='pyarrow')
        print(f"Saved {len(final_df)} piece values to {PVP_FILE_NAME}")

        # Print column info and data sample
        print(f"\nColumns: {final_df.columns.tolist()}")
        print(f"\nSample data:")
        print(final_df.head())

        # Print statistics
        print("\n=== Statistics ===")
        print(f"Unique games: {final_df['game_id'].nunique()}")
        print(f"Unique positions (FENs): {final_df['fen'].nunique()}")
        print(f"Total piece values: {len(final_df)}")
        if 'piece_type' in final_df.columns: # this check is schizo
            print(f"\nPiece type distribution:")
            print(final_df['piece_type'].value_counts())
        print("=" * 20)

        # Print final summary statements, keep worker output files
        print(f"\nWorker output files saved in: {temp_dir}")
        print(f"\nFinished converting games from {PGN_FILE_NAME} to piece values in {PVP_FILE_NAME}")
        print(f"Total processing time: {elapsed_time:.1f} seconds")
        
        # nothing went wrong so exit normally
        sys.exit(0)

    # something has gone wrong
    except Exception as e:
        print(f"Error during PGN->PVals processing: {e}")
        traceback.print_exc()
        sys.exit(1)

# main (main)
if __name__ == "__main__":
    main()