#!/bin/bash
#SBATCH -p public ## Partition
#SBATCH -q public  ## QOS
#SBATCH -N 1      ## Number of Sol Nodes
#SBATCH -c 16    ## Number of Cores
#SBATCH --mem=64G  ## Memory (GB)
#SBATCH --time=10000   ## Minutes of compute
#SBATCH -G 1        ## Number of GPUs
#SBATCH --job-name=chess-pval-2023-gm-games
#SBATCH --output=slurm.%j.out  ## job /dev/stdout record (%j expands -> jobid)
#SBATCH --error=slurm.%j.err   ## job /dev/stderr record
#SBATCH --export=NONE          ## keep environment clean
#SBATCH --mail-type=ALL        ## notify <asurite>@asu.edu for any job state change

# This is an example slurm script I used with the Sol supercomputer 
# to train piece value predictors on Dataset MC and GM.

# ------------------------------
# SCRIPT CONFIG
# ------------------------------

echo "=========================================="
echo "Pval Preditor Training + Evaluation Script"
echo "=========================================="

# Pval DF in parquet file
INPUT_DATA="MY_PVAL_PARQUET.parquet"

# File paths for training/validation pval data
TRAIN_DATA="train.parquet"
VAL_DATA="val.parquet"

# Output directory for trained models
OUTPUT_DIR="./output"

# !!! CHECK THIS BEFORE RUNNING !!!
# Memory and worker configuration - should match SBATCH directives above
NUM_CORES="16"       # Match SBATCH -c value
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
mamba install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y
python3 -m pip install --user torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Check if Python is available (lost sanity over this)
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "./output"

# Verify PyTorch was installed successfully (lost sanity over this)
echo "Verifying PyTorch installation..."
python3 -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda if torch.cuda.is_available() else \"N/A\"}')"
if ! python3 -c "import torch" 2>/dev/null; then
    echo "WARNING: PyTorch installation failed!"
fi

# Install Python ependencies
echo "Installing Python dependencies..."
python3 -m pip install --user python-chess numpy pandas psutil pyarrow scikit-learn tqdm

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


