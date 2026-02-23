#!/bin/bash
#SBATCH -p public ## Partition
#SBATCH -q public  ## QOS
#SBATCH -N 1      ## Number of Sol Nodes
#SBATCH -c 128    ## Number of Cores
#SBATCH --mem=256G  ## Memory (GB)
#SBATCH --time=10000   ## Minutes of compute
#SBATCH --job-name=this-is-a-good-use-of-compute-resources
#SBATCH --output=slurm.%j.out  ## job /dev/stdout record (%j expands -> jobid)
#SBATCH --error=slurm.%j.err   ## job /dev/stderr record
#SBATCH --export=NONE          ## keep environment clean
#SBATCH --mail-type=ALL        ## notify <asurite>@asu.edu for any job state change

# This is an example slurm script I used with the Sol supercomputer 
# to gather all piece values in Datasets MC and GM.

# ------------------------------
# SCRIPT CONFIG
# ------------------------------

echo "=========================================="
echo "PGN->PVal Script"
echo "=========================================="

export PGN_FILE_NAME="MY_PGN.pgn" # PGN file name
# You can export from a database of your choice, I used the ChessBase Mega Database 2025

export PVP_FILE_NAME="${PGN_FILE_NAME%.pgn}_piecevals.parquet" # PVal data file name
# Contains piece value entries stored in a DataFrame, saved in a parquet file

export SF_PATH="./THE_BIG_FISH" # Path to Stockfish
# Your path to Stockfish
# Python script included only works with Stockfish but you could obviously swap engines if you'd like
# (with optional help from your friend Claude)

export NUM_WORKERS="128" # Number of cores (1 core per worker)

# ------------------------------
# SCRIPT SETUP
# ------------------------------

# You may need to create a new mambe environment with:
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
# I combined piece value gathering and preditor training into one script file at first.
# But that is a STUPID idea, please use abstraction and step-by-step architectures whenever you can.
mamba install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y
python3 -m pip install --user torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Check if Python is available (lost sanity over this)
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Install Python dependencies and enable execution for Stockfish (lost sanity over this)
python3 -m pip install --user python-chess stockfish numpy pandas psutil pyarrow scikit-learn
chmod +x ./stockfish_compiled

# ------------------------------
# MAIN PVAL GENERATION SCRIPT
# ------------------------------

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

