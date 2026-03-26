# PAWN: <ins>P</ins>iece value <ins>A</ins>nalysis <ins>W</ins>ith <ins>N</ins>eural networks

## Paper

LINK COMING SOON!

## Datasets and Models

We open-source Dataset MC-large and TF along with the best MLP and MLP+CNN model configurations trained for both datasets.

- **Datasets:** [huggingface.co/datasets/ethanjtang/PAWN-piece-value-datasets](https://huggingface.co/datasets/ethanjtang/PAWN-piece-value-datasets)
- **Models:** [huggingface.co/ethanjtang/PAWN-piece-value-predictors](https://huggingface.co/ethanjtang/PAWN-piece-value-predictors)

Both datasets also include many other helpful and unused columns such as:

- FEN + evaluation pairs for anyone wanting to optimize position evaluations for chess engines
- Misc. metadata like side-to-move, material strings, and opening code/name for data analysis/visualization

## Dependencies

### PyTorch and Stuff

```bash
pip install torch torchvision torchaudio scikit-learn
```

### Chess Stuff

```bash
pip install python-chess stockfish
```

### General Utility

```bash
pip install numpy pandas psutil pyarrow tqdm
```

> Please reference shell scripts included in each folder for additional information about how to run each step.

## How to Run This Code

### PGN → PVal

1. Gather a selection of chess games/positions in a single file (using some database like the [Lichess Open Source Games Database](https://database.lichess.org/) or ChessBase).
2. Download [Stockfish](https://stockfishchess.org/) (or some other version of it/another chess engine).
3. Run `python -u pgn_to_piecevals.py`

### PVal Predictor Training

1. Run `python -u pval_train_val_split.py`
2. Run `python -u train_all_models.py`

## Misc. Documentation

- **`./pval_stats`** — contains a helper file used with slurm output files to calculate the number of timeouts per worker (when evaluating positions for calculating piece values).
- **`./pvp_example`** — contains a Jupyter Notebook used to generate figures and piece values used in the main PAWN paper for Figures 1, 3, and 5.
- **`./sample_run`** — includes files + output logs from a sample run completed on the Sol supercomputer using 32 games (`sample_games.pgn`) from GM Garry "Chess" Kasparov's 1985 simul against 32 chess computers (in which he scored 32-0), sourced from: [chessprogramming.org/Kasparov_Simul_vs_32_Micros_Hamburg_1985](https://www.chessprogramming.org/Kasparov_Simul_vs_32_Micros_Hamburg_1985)
