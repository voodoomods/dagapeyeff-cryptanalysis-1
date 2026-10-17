#!/usr/bin/env python3
"""
Replicate Hendrick's family-wise p-value computation.
"""
import math
import random
import time
from collections import Counter

import numpy as np

symbol_text = "HAJMNANCICNGMLCGGJLKIBIIGGJACHKJLNHGDKHHHPBDDIBIHMHHCAJOMGBJHGKIDILMCMCMMBJFAKAIIFICBHJICKBJMIBBBGINNLBMLDCMDAQAAMNMNGNFHCDHEDKACGIJLAJCNIPDACLLNKMGNIDFGKKMJKCAFADAKHOFBJJFFKJMLHJIKFLAJKHICHGMIAO"
cells = list(symbol_text)
fixed_positions = [40, 54, 96, 110, 124, 138, 166, 194]

print(f"Total cells: {len(cells)}")
print(f"Fixed positions: {fixed_positions}")

def equal_symbol_share(seq, lag):
    n = len(seq)
    count = sum(1 for i in range(n - lag) if seq[i] == seq[i + lag])
    return count / (n - lag)

def mutual_information(seq, lag):
    n = len(seq)
    pairs = [(seq[i], seq[i + lag]) for i in range(n - lag)]
    pair_counts = Counter(pairs)
    x_counts = Counter()
    y_counts = Counter()
    
    for (x, y), count in pair_counts.items():
        x_counts[x] += count
        y_counts[y] += count
    
    total_pairs = len(pairs)
    mi = 0.0
    for (x, y), count in pair_counts.items():
        p_xy = count / total_pairs
        p_x = x_counts[x] / total_pairs
        p_y = y_counts[y] / total_pairs
        if p_xy > 0:
            mi += p_xy * math.log(p_xy / (p_x * p_y))
    return mi

def distinct_neighbour_pairs(seq):
    pairs = [(seq[i], seq[i + 1]) for i in range(len(seq) - 1)]
    return len(set(pairs))

def repeated_triples(seq):
    n = len(seq)
    triples = [tuple(seq[i:i+3]) for i in range(n - 2)]
    triple_counts = Counter(triples)
    return sum(1 for count in triple_counts.values() if count > 1)

def compute_statistics(seq):
    stats = []
    for lag in range(1, 15):
        stats.append(equal_symbol_share(seq, lag))
    for lag in range(1, 15):
        stats.append(mutual_information(seq, lag))
    stats.append(distinct_neighbour_pairs(seq))
    stats.append(repeated_triples(seq))
    return stats

def permute_fixed(seq, fixed_positions):
    n = len(seq)
    free_positions = [i for i in range(n) if i not in fixed_positions]
    free_symbols = [seq[i] for i in free_positions]
    random.shuffle(free_symbols)
    new_seq = list(seq)
    for pos, symbol in zip(free_positions, free_symbols):
        new_seq[pos] = symbol
    return new_seq

# Generate dealings (null permutations)
n_dealings = 1000  # Hendrick used 20000, but 1000 should give reasonable estimate
print(f"Generating {n_dealings} dealings...")
start = time.time()

dealings_stats = []
for i in range(n_dealings):
    if i % 200 == 0:
        print(f"  {i}...")
    permuted = permute_fixed(cells, fixed_positions)
    dealings_stats.append(compute_statistics(permuted))

dealings_stats = np.array(dealings_stats)
print(f"Generated {n_dealings} dealings in {time.time() - start:.1f}s")

# Add real cells as the first entry
real_stats = compute_statistics(cells)
all_stats = np.vstack([np.array(real_stats).reshape(1, -1), dealings_stats])
n_all = len(all_stats)

print("\nComputing p-values for each sequence against the dealings...")

# For each sequence (including real), compute its 30 p-values against the dealings distribution
p_values_matrix = []
for seq_idx in range(n_all):
    if seq_idx % 200 == 0:
        print(f"  Sequence {seq_idx}/{n_all}...")
    
    seq_stats = all_stats[seq_idx]
    p_values = []
    
    for stat_idx in range(30):
        # Compare this sequence's stat value against all OTHER sequences
        # (Excluding this sequence itself)
        other_indices = [i for i in range(n_all) if i != seq_idx]
        other_vals = all_stats[other_indices, stat_idx]
        
        seq_val = seq_stats[stat_idx]
        
        # Two-sided rank p-value
        if isinstance(seq_val, float):
            rank = np.sum(other_vals >= seq_val) if seq_val >= np.median(other_vals) else np.sum(other_vals <= seq_val)
            p = 2 * min(rank, len(other_vals) - rank) / len(other_vals)
        else:
            rank_below = np.sum(other_vals <= seq_val)
            rank_above = np.sum(other_vals >= seq_val)
            p = 2 * min(rank_below, rank_above) / len(other_vals)
        
        p_values.append(p)
    
    p_values_matrix.append(p_values)

p_values_matrix = np.array(p_values_matrix)

# For each sequence, find its smallest p-value
min_p_values = np.min(p_values_matrix, axis=1)
real_min_p = min_p_values[0]  # Real cells is first
dealings_min_p = min_p_values[1:]  # All dealings

print(f"\nReal cells smallest p-value: {real_min_p:.6f}")
print(f"Dealings smallest p-values: min={np.min(dealings_min_p):.6f}, median={np.median(dealings_min_p):.6f}")

# Family-wise p-value: proportion of dealings whose smallest p ≤ real cells' smallest p
count_as_extreme = np.sum(dealings_min_p <= real_min_p)
family_p = count_as_extreme / len(dealings_min_p)

print(f"\nDealings with min p ≤ {real_min_p:.6f}: {count_as_extreme}/{len(dealings_min_p)}")
print(f"Family-wise p-value: {family_p:.4f}")

# Check which statistic gives the smallest p for real cells
smallest_idx = np.argmin(p_values_matrix[0])
labels = [f"equal lag {i}" for i in range(1, 15)] + [f"info lag {i}" for i in range(1, 15)] + ["distinct pairs", "repeated triples"]
print(f"\nSmallest p for real cells: {p_values_matrix[0, smallest_idx]:.6f} ({labels[smallest_idx]})")

# Save results
import json

results = {
    "real_stats": [float(x) if isinstance(x, float) else int(x) for x in real_stats],
    "real_p_values": p_values_matrix[0].tolist(),
    "real_smallest_p": float(real_min_p),
    "real_smallest_statistic": labels[smallest_idx],
    "family_p": float(family_p),
    "n_dealings": n_dealings,
    "dealings_extreme_count": int(count_as_extreme),
    "dealings_total": len(dealings_min_p)
}
with open("/workspace/research/cipher/dagapeyeff/round9/friedman/familywise_complete.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nResults saved to familywise_complete.json")
print("\nHendrick's reported values:")
print("  Family p (cells): 0.2814")
print("  Smallest p: 0.0138 (info lag 3)")
print("Our replication:")
print(f"  Family p: {family_p:.4f}")
print(f"  Smallest p: {real_min_p:.4f} ({labels[smallest_idx]})")