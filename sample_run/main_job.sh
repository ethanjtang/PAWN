#!/bin/bash
#SBATCH -p public ## Partition
#SBATCH -q public  ## QOS
#SBATCH -N 1      ## Number of Sol Nodes
#SBATCH -c 32    ## Number of Cores
#SBATCH --mem=64G  ## Memory (GB)
#SBATCH --time=10000   ## Minutes of compute
#SBATCH -G 1 ## Number of GPUs
#SBATCH --job-name=github-pawn-sample-run
#SBATCH --output=slurm.%j.out  ## job /dev/stdout record (%j expands -> jobid)
#SBATCH --error=slurm.%j.err   ## job /dev/stderr record
#SBATCH --export=NONE          ## keep environment clean
#SBATCH --mail-type=ALL        ## notify <asurite>@asu.edu for any job state change

# Example script

# ------------------------------
# SCRIPT CONFIG
# ------------------------------

echo "=========================================="
echo "PGN->PVal Script"
echo "=========================================="

export PGN_FILE_NAME="sample_games.pgn" # PGN file name
# You can export from a database of your choice, I used the ChessBase Mega Database 2025

export PVP_FILE_NAME="${PGN_FILE_NAME%.pgn}_piecevals.parquet" # PVP - piece val parquet
# Contains piece value entries stored in a DataFrame, saved in a parquet file

export SF_PATH="./stockfish_compiled" # Path to Stockfish
# Your path to Stockfish
# Python script included only works with Stockfish but you could obviously swap engines if you'd like
# (with optional help from your friend Claude)

export NUM_WORKERS="32" # Number of cores (1 core per worker)

# ------------------------------
# SCRIPT SETUP
# ------------------------------

# You may need to create a new mamba environment with:
# module load mamba/latest
# mamba create -n chess-env -c conda-forge python=3.9 pytorch torchvision torchaudio

# Load mamba and activate environment
echo "Loading mamba and activating chess-env..."
module load mamba/latest
source activate chess-env

# Verify Python version (lost sanity over this)
echo "Python version:"
python3 --version

# Install Pytorch and stuff
# Keep in mind some lines (like this) are unnecessary for gathering piece values.
# I combined piece value gathering and predictor training into one script file at first.
# But that is a STUPID idea, please use abstraction and step-by-step architectures whenever you can.
mamba install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y
python3 -m pip install --user torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Check if Python is available (lost sanity over this)
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Install Python dependencies and enable execution for Stockfish (lost sanity over this)
# You probably don't need torchvision/torchaudio but I don't feel like checking anymore
python3 -m pip install torch torchvision torchaudio scikit-learn # ml stuff
python3 -m pip install python-chess stockfish # chess
python3 -m pip install numpy pandas psutil pyarrow tqdm # util
chmod +x ./stockfish_compiled

# ------------------------------
# MAIN PVAL GENERATION SCRIPT
# ------------------------------

echo "------------------------------------------"
echo "PHASE 1: GATHER PVAL DATA"
echo "------------------------------------------"

echo ""
echo "=========================================="
echo "STEP 1: PGNs -> PVal Parquet"
echo "=========================================="

# Check if the parquet file already exists
if [ -f "$PVP_FILE_NAME" ]; then
    echo "Output file $PVP_FILE_NAME already exists, skipping pgn_to_piecevals.py"
    echo "File size: $(du -h "$PVP_FILE_NAME" | cut -f1)"
# Otherwise, run the program to generate the pval parquet
else
    python3 -u pgn_to_piecevals.py

    # Check if pgn_to_piecevals.py completed successfully
    if [ $? -ne 0 ]; then
        echo "Error: pgn_to_piecevals.py failed!"
        exit 1
    fi

    # Check if the output parquet file was created
    if [ ! -f "$PVP_FILE_NAME" ]; then
        echo "Error: Output file $PVP_FILE_NAME was not created!"
        exit 1
    fi
fi

# Check if the temp_piecevals directory exists
# Used to store each individual worker's pval parquet before they are aggregated into the final result
if [ ! -d "temp_piecevals" ]; then
    echo "Warning: temp_piecevals directory not found"
fi

echo ""
echo "=========================================="
echo "PGNs->PVal Parquet Complete!"
echo "Parquet file created: $PVP_FILE_NAME"
echo "File size: $(du -h "$PVP_FILE_NAME" | cut -f1)"
echo "=========================================="
echo ""

echo "------------------------------------------"
echo "PHASE 2: TRAIN PVAL PREDICTORS AND EVALUATE PERFORMANCE"
echo "------------------------------------------"

echo "=========================================="
echo "Pval Predictor Training + Evaluation Script"
echo "=========================================="

# Pval DF in parquet file
INPUT_DATA="${PVP_FILE_NAME}"

# File paths for training/validation pval data
TRAIN_DATA="train.parquet"
VAL_DATA="val.parquet"

# Output directory for trained models
OUTPUT_DIR="./output"

# !!! CHECK THIS BEFORE RUNNING !!!
# Memory and worker configuration - should match SBATCH directives above
NUM_CORES="32"       # Match SBATCH -c value
TOTAL_MEMORY_GB="64" # Match SBATCH --mem value
# !!! CHECK THIS BEFORE RUNNING !!!

# Python path
PYTHON="python3"

# Display configuration
echo "Configuration:"
echo "------------------------------------------"
echo "INPUT_DATA=$INPUT_DATA"
echo "TRAIN_DATA=$TRAIN_DATA"
echo "VAL_DATA=$VAL_DATA"
echo "OUTPUT_DIR=$OUTPUT_DIR"
echo "NUM_CORES=$NUM_CORES"
echo "TOTAL_MEMORY_GB=$TOTAL_MEMORY_GB"
echo "------------------------------------------"

# Verify Python version (lost sanity over this)
echo "Python version:"
python3 --version

# Create output directory if it doesn't exist
mkdir -p "./output"

# Verify required input pval data file exists
echo "Checking for input data file..."
if [ ! -f "$INPUT_DATA" ]; then
    echo "ERROR: Input data file not found: $INPUT_DATA"
    exit 1
fi

echo "Input data file found: $INPUT_DATA"

# ------------------------------
# MAIN PVAL PREDICTOR TRAINING + EVALUATION SCRIPT
# ------------------------------

echo ""
echo "=========================================="
echo "STEP 1: Splitting PVal Data Into Train/Val Sets"
echo "=========================================="

# Check if train and val parquet files already exist
if [ -f "$TRAIN_DATA" ] && [ -f "$VAL_DATA" ]; then
    echo "Found existing split files:"
    echo "  - $TRAIN_DATA"
    echo "  - $VAL_DATA"
    echo "Skipping data splitting step..."
    echo ""
# Split the data if train and val parquet files are not found
else
    echo "Split files not found. Running pval_train_val_split.py..."
    python3 -u pval_train_val_split.py

    # Check exit status
    if [ $? -ne 0 ]; then
        echo ""
        echo "=========================================="
        echo "ERROR: Data splitting failed!"
        echo "Check slurm.*.err for error details"
        echo "=========================================="
        exit 1
    fi

    # Verify split files were created
    if [ ! -f "$TRAIN_DATA" ] || [ ! -f "$VAL_DATA" ]; then
        echo "ERROR: Split files not created successfully"
        echo "Expected: $TRAIN_DATA and $VAL_DATA"
        exit 1
    fi

    echo "Data splitting completed successfully!"
    echo "Training file: $TRAIN_DATA"
    echo "Validation file: $VAL_DATA"
fi

echo ""
echo "=========================================="
echo "STEP 2: Train All Piece Value Prediction Models"
echo "=========================================="
echo "Models to train:"
echo "  - 3 MLP baselines (mlp1, mlp2, chessable2023)"
echo "  - 9 CNN-based models (512d embeddings, 4/6/8 position autoencoder layers, 3/4/5 pval prediction layers)"
echo "Total: 12 models"
echo "=========================================="
echo ""

echo "Running train_all_models.py..."
python3 -u train_all_models.py

# Check exit status
if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "PVAL PREDICTOR TRAINING + EVAL COMPLETED SUCCESSFULLY!"
    echo "=========================================="
    echo "Results saved to: $OUTPUT_DIR"
    echo "Metrics file: $OUTPUT_DIR/all_models_metrics.json"
    echo "=========================================="
else
    echo ""
    echo "=========================================="
    echo "ERROR: Training failed!"
    echo "Check slurm.*.err for error details"
    echo "=========================================="
    exit 1
fi

