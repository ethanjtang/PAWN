# PAWN

[![arXiv](https://img.shields.io/badge/arXiv-2604.15585-b31b1b.svg?style=for-the-badge)](https://arxiv.org/abs/2604.15585) <br>

> <ins>P</ins>iece value <ins>A</ins>nalysis <ins>W</ins>ith <ins>N</ins>eural networks <br>

### TLDR

Incorporating intermediate position representations derived using a CNN autoencoder as additional inputs to MLP-based chess piece relative value prediction systems significantly increases their accuracy.

### TLDR^2

All ♝s on g7 are created equal, but some ♝s on g7 are more equal than others.

## Datasets and Models

We open-source Dataset MC-large and TF along with the best MLP and MLP+CNN model configurations trained for both datasets.

[![HuggingFace](https://img.shields.io/badge/🤗_HuggingFace-Datasets-yellow?style=for-the-badge)](https://huggingface.co/datasets/ethanjtang/PAWN-piece-value-datasets) <br>
[![HuggingFace](https://img.shields.io/badge/🤗_HuggingFace-Models-yellow?style=for-the-badge)](https://huggingface.co/ethanjtang/PAWN-piece-value-predictors) <br>

Both datasets also include many other helpful and unused columns such as:
- FEN + evaluation pairs for anyone wanting to optimize position evaluations for chess engines
- Misc. metadata like side-to-move, material strings, and opening code/name for data analysis/visualization

## Dependencies

### Machine Learning (+400% stock price) Stuff

```bash
pip install torch torchvision torchaudio scikit-learn
```
> torchvision and torchaudio are likely redundant (I was experimenting with graphs/GNNs for piece value prediction but gave up halfway)

### Chess Stuff

```bash
pip install python-chess stockfish
```

### General Utility

```bash
pip install numpy pandas psutil pyarrow tqdm
```

> Please reference shell scripts included in each folder for additional information about how to run each step!

## How to Run This Code

### PGN → Piece Value Dataset

1. Gather a selection of chess games/positions in a single file (using some database like the [Lichess Open Source Games Database](https://database.lichess.org/) or ChessBase).
2. Download [Stockfish](https://stockfishchess.org/) (or some other version of it/another chess engine).
3. Run `python -u pgn_to_piecevals.py`

### Piece Value Predictor Training

1. Run `python -u pval_train_val_split.py`
2. Run `python -u train_all_models.py`

## Miscellaneous Files

- **`./pval_stats`** — contains a helper file used with slurm output files to calculate the number of timeouts per worker (when evaluating positions for calculating piece values).
- **`./pvp_example`** — contains a Jupyter Notebook used to generate figures and piece values used in the main PAWN paper for Figures 1, 3, and 5.
- **`./sample_run`** — contains input/output files from a sample run completed on the Sol supercomputer using 32 games (`sample_games.pgn`) from GM Garry "Chess" Kasparov's 1985 simul against 32 chess computers (in which he scored 32-0), sourced from: [chessprogramming.org/Kasparov_Simul_vs_32_Micros_Hamburg_1985](https://www.chessprogramming.org/Kasparov_Simul_vs_32_Micros_Hamburg_1985)

## Citation

```bibtex
@misc{tang2026pawnpiecevalueanalysis,
      title={PAWN: Piece Value Analysis with Neural Networks}, 
      author={Ethan Tang and Hasan Davulcu and Jia Zou and Zhongju Zhang},
      year={2026},
      eprint={2604.15585},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2604.15585}, 
}
