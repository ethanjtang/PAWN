"""
AI SLOP

Calculate average proportion of timeouts for positions for each worker.

This script parses a SLURM output file to extract:
- Positions processed per worker
- Piece values gathered per worker
- Timeouts per worker

And calculates the percentage of piece values lost to timeouts.
"""

import re
from collections import defaultdict

def parse_slurm_output(filepath):
    """Parse the SLURM output file to extract worker statistics."""

    # Pattern to match final worker stats lines
    # Example: "Worker 107: Stats - 54 games, 5886 positions, 101517 pieces, 1150 timeouts"
    pattern = re.compile(
        r'Worker (\d+): Stats - (\d+) games, (\d+) positions, (\d+) pieces, (\d+) timeouts'
    )

    worker_stats = {}

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                worker_id = int(match.group(1))
                games_total = int(match.group(2))
                positions = int(match.group(3))
                pieces = int(match.group(4))
                timeouts = int(match.group(5))

                worker_stats[worker_id] = {
                    'games': games_total,
                    'positions': positions,
                    'pieces': pieces,
                    'timeouts': timeouts
                }

    return worker_stats

def calculate_statistics(worker_stats):
    """Calculate timeout statistics."""

    total_positions = 0
    total_pieces = 0
    total_timeouts = 0

    # Per-worker timeout proportions
    worker_timeout_proportions = []

    print("=" * 80)
    print("WORKER-LEVEL STATISTICS")
    print("=" * 80)
    print(f"{'Worker':<8} {'Games':<7} {'Positions':<12} {'Pieces':<12} {'Timeouts':<12} {'Timeout %':<12}")
    print("-" * 80)

    for worker_id in sorted(worker_stats.keys()):
        stats = worker_stats[worker_id]
        positions = stats['positions']
        pieces = stats['pieces']
        timeouts = stats['timeouts']
        games = stats['games']

        total_positions += positions
        total_pieces += pieces
        total_timeouts += timeouts

        # Calculate timeout proportion for this worker
        # Timeouts represent piece value calculations that failed
        # (due to tiemout constraints or either position being invalid)
        # Each position has multiple pieces, so timeouts / (pieces processed + timeouts) gives % lost
        total_attempted = pieces + timeouts 
        if total_attempted > 0:
            timeout_pct = (timeouts / total_attempted) * 100
        else:
            timeout_pct = 0

        worker_timeout_proportions.append(timeout_pct)

        print(f"{worker_id:<8} {games:<7} {positions:<12,} {pieces:<12,} {timeouts:<12,} {timeout_pct:<12.2f}%")

    print("=" * 80)
    print("\nAGGREGATE STATISTICS")
    print("=" * 80)

    print(f"\nTotal workers: {len(worker_stats)}")
    print(f"Total positions processed: {total_positions:,}")
    print(f"Total piece values gathered: {total_pieces:,}")
    print(f"Total timeouts: {total_timeouts:,}")

    # Overall timeout percentage
    total_attempted = total_pieces + total_timeouts
    overall_timeout_pct = (total_timeouts / total_attempted) * 100 if total_attempted > 0 else 0

    print(f"\nTotal piece evaluations attempted: {total_attempted:,}")
    print(f"Overall timeout percentage: {overall_timeout_pct:.4f}%")
    print(f"  - Piece values successfully gathered: {total_pieces:,} ({100 - overall_timeout_pct:.4f}%)")
    print(f"  - Piece values lost to timeouts: {total_timeouts:,} ({overall_timeout_pct:.4f}%)")

    # Average pieces per position
    avg_pieces_per_position = total_pieces / total_positions if total_positions > 0 else 0
    print(f"\nAverage pieces per position: {avg_pieces_per_position:.2f}")

    # Worker-level statistics
    if worker_timeout_proportions:
        avg_worker_timeout = sum(worker_timeout_proportions) / len(worker_timeout_proportions)
        min_timeout = min(worker_timeout_proportions)
        max_timeout = max(worker_timeout_proportions)

        print(f"\nPER-WORKER TIMEOUT STATISTICS:")
        print(f"  Average timeout % across workers: {avg_worker_timeout:.4f}%")
        print(f"  Min worker timeout %: {min_timeout:.4f}%")
        print(f"  Max worker timeout %: {max_timeout:.4f}%")
        print()
        print()
        
    return {
        'total_positions': total_positions,
        'total_pieces': total_pieces,
        'total_timeouts': total_timeouts,
        'overall_timeout_pct': overall_timeout_pct,
        'worker_timeout_proportions': worker_timeout_proportions
    }

def main():
    file = "slurm.46942719.out" # CHANGE THIS AS NEEDED

    print(f"Parsing {file}...")
    worker_stats = parse_slurm_output(file)

    if not worker_stats:
        print("No worker statistics found in the file!")
        return

    print(f"Found data for {len(worker_stats)} workers\n")

    results = calculate_statistics(worker_stats)

    print(results)

if __name__ == "__main__":
    main()
