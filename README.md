# PAWN
Piece value Analysis With Neural networks

## Dependencies and other things

### Machine Learning
pip install torch torchvision torchaudio scikit-learn 
### Chess Specific
pip install python-chess stockfish
### General Utility
pip install numpy pandas psutil pyarrow tqdm

### Please reference shell scripts included in each folder for additional information about how to run each step.

## How to run this code

### PGN -> PVal

1. Gather a selection of chess games/positions in a single file (using some database like the Lichess Open Source Games Database or ChessBase).
2. Download Stockfish (or some other version of it/another chess engine).
3. Run python -u pgn_to_piecevals.py
   
### PVal Predictor Training

1. Run python -u pval_train_val_split.py
2. Run python -u train_all_models.py
