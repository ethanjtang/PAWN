"""
This file pval_train_val_split.py is used to split our initially gathered piece value dataset
(formatted as a DataFrame and saved as a parquet) into separate training and validation sets
based on the original game the piece value entry came from.

A single game is assigned a game ID and has X many positions.
Each of these X positions will have Y number of piece value entries.

We assign every collection of X*Y piece values from a unique game to either the
training or validation set to prevent overfitting inconsistencies we saw when testing
a train/val split based on individual rows.

This is necessary mostly to prevent overfitting for our CNN autoencoder we use to derive 
intermediate position representations. By splitting by game ID, the CNN autoencoder should not
encounter most of the validation positions during training unlike when we used a row-level split.

Configuration:
- INPUT_FILE: Source parquet file with all piece value data
- TRAIN_FILE: Output file for training data (~80% of rows)
- VAL_FILE: Output file for validation data (~20% of rows)
- RANDOM_SEED: Random seed for reproducibility
- TRAIN_SPLIT: Training set proportion (0.8 = 80%)

Usage:
    python pval_train_val_split.py
"""

# imports
import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path

# ==============
# CONFIG
# ==============

# Input pval data
# INPUT_FILE = "carlsen_full_piecevals.parquet" # change this as needed
INPUT_FILE = r"2023_gm_games_piecevals.parquet"

# Output train/val data
TRAIN_FILE = "train.parquet"
VAL_FILE = "val.parquet"

# Split configuration
TRAIN_SPLIT = 0.8  # 80% training, 20% validation
RANDOM_SEED = 14   # 14

# ==============
# MAIN
# ==============

def main():
    print("="*80)
    print("SPLITTING DATASET INTO TRAIN/VALIDATION SETS")
    print("="*80)
    print(f"Input file: {INPUT_FILE}")
    print(f"Train file: {TRAIN_FILE}")
    print(f"Validation file: {VAL_FILE}")
    print(f"Split ratio: {TRAIN_SPLIT:.0%} train / {1-TRAIN_SPLIT:.0%} validation (by game)")
    print(f"Random seed: {RANDOM_SEED}")
    print("="*80)
    print()

    # Load the data
    print("Loading pval data...")
    input_path = Path(INPUT_FILE)
    if not input_path.exists():
        print(f"ERROR: Input file not found: {INPUT_FILE}")
        return 1

    # Read pval DF in from parquet
    df = pd.read_parquet(INPUT_FILE)
    print(f"Loaded {len(df):,} rows")
    print(f"Columns: {list(df.columns)}")
    print()

    # Print basic statistics
    print("Dataset statistics:")
    print(f"  Total rows: {len(df):,}")
    print(f"  Unique games: {df['game_id'].nunique():,}")
    print(f"  Unique positions: {df['fen'].nunique():,}")
    print(f"  Piece value range: [{df['piece_value'].min()}, {df['piece_value'].max()}]")
    print(f"  Piece value mean: {df['piece_value'].mean():.2f}")
    print(f"  Piece value std: {df['piece_value'].std():.2f}")
    print()

    # Cap piece values at 5x their base value based on piece type
    # Piece values: pawn=1, knight/bishop=3, rook=5, queen=10
    # Caps: pawn=±5, knight/bishop=±15, rook=±25, queen=±50
    print("Capping piece values at 5x their base value by piece type...")

    # Create copy of pval data
    original_values = df['piece_value'].copy()

    # Define caps for each piece type (in centipawns - cp)
    piece_caps = {
        'p': 500,      # 5 * 100 cp
        'k': 1500,   # 5 * 300 cp
        'b': 1500,   # 5 * 300 cp
        'r': 2500,     # 5 * 500 cp
        'q': 5000,    # 5 * 1000 cp
        'k': 0       # Kings have no material value
    }

    # Apply caps based on piece type
    for piece_type, cap in piece_caps.items():
        mask = df['piece_type'].str.lower() == piece_type.lower() # handle case sensitive piece types
        if mask.any():
            df.loc[mask, 'piece_value'] = df.loc[mask, 'piece_value'].clip(-cap, cap)
            capped_in_type = ((original_values[mask] != df.loc[mask, 'piece_value']).sum())
            if capped_in_type > 0:
                print(f"  {piece_type.capitalize()}: capped {capped_in_type:,} values (cap=±{cap})")

    # Print out summary stats for total number of piece values capped
    total_capped = (original_values != df['piece_value']).sum()
    print(f"  Total capped: {total_capped:,} values ({total_capped/len(df)*100:.2f}%)")
    print(f"  New piece value range: [{df['piece_value'].min()}, {df['piece_value'].max()}]")
    print()

    # Split pval data at the game level (based on game ID)
    # Important to note that there will still be duplicate FENs/positions between the train and val set because different games may play the same openings/positions
    # But this removes a lot of the problems with overfitting from using a row level split for piece value data
    print(f"Splitting data {TRAIN_SPLIT:.0%}/{1-TRAIN_SPLIT:.0%} by game ID...")
    print("  (All positions from a game stay in the same split)")

    # Get unique game IDs and split them
    unique_games = df['game_id'].unique()
    print(f"  Total unique games: {len(unique_games):,}")
    
    # Create train/val game ID split
    train_games, val_games = train_test_split(
        unique_games,
        train_size=TRAIN_SPLIT,
        random_state=RANDOM_SEED,
        shuffle=True
    )

    # Print number of train/val games
    print(f"  Training games: {len(train_games):,}")
    print(f"  Validation games: {len(val_games):,}")

    # Create train/val DataFrames based on game-level split
    train_game_set = set(train_games)
    val_game_set = set(val_games)

    train_df = df[df['game_id'].isin(train_game_set)].copy()
    val_df = df[df['game_id'].isin(val_game_set)].copy()

    print(f"\nTraining set: {len(train_df):,} rows ({len(train_df)/len(df):.1%})")
    print(f"Validation set: {len(val_df):,} rows ({len(val_df)/len(df):.1%})")

    # Verify amount of FEN overlap b/w train/val set
    # (Some overlap is expected due to shared openings among different games) 
    train_fens = set(train_df['fen'].unique())
    val_fens = set(val_df['fen'].unique())
    overlapping_fens = train_fens & val_fens
    print(f"\nData leakage check:")
    print(f"  Unique FENs in train: {len(train_fens):,}")
    print(f"  Unique FENs in val: {len(val_fens):,}")
    print(f"  Overlapping FENs: {len(overlapping_fens):,} ({len(overlapping_fens)/len(val_fens)*100:.1f}% of val FENs)")
    print(f"  Note: Some FEN overlap is expected from common openings between different games.")
    print()

    # Print train split statistics
    print("Training set statistics:")
    print(f"  Unique games: {train_df['game_id'].nunique():,}")
    print(f"  Unique positions: {train_df['fen'].nunique():,}")
    print(f"  Piece value range: [{train_df['piece_value'].min()}, {train_df['piece_value'].max()}]")
    print(f"  Piece value mean: {train_df['piece_value'].mean():.2f}")
    print()

    # Print val split statistics
    print("Validation set statistics:")
    print(f"  Unique games: {val_df['game_id'].nunique():,}")
    print(f"  Unique positions: {val_df['fen'].nunique():,}")
    print(f"  Piece value range: [{val_df['piece_value'].min()}, {val_df['piece_value'].max()}]")
    print(f"  Piece value mean: {val_df['piece_value'].mean():.2f}")
    print()

    # Save train split
    print("Saving training set...")
    train_df.to_parquet(TRAIN_FILE, compression='lz4', index=False, engine='pyarrow')
    print(f"Saved to {TRAIN_FILE}")

    # Save val split
    print("Saving validation set...")
    val_df.to_parquet(VAL_FILE, compression='lz4', index=False, engine='pyarrow')
    print(f"Saved to {VAL_FILE}")
    print()

    # Print confirmation message and stats
    print("="*80)
    print("SPLIT COMPLETE!")
    print("="*80)
    print(f"Training data: {TRAIN_FILE} ({len(train_df):,} rows)")
    print(f"Validation data: {VAL_FILE} ({len(val_df):,} rows)")
    print("="*80)

    # return(return)
    return 0

# main(main)
if __name__ == "__main__":
    exit(main())