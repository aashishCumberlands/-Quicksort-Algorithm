"""
Empirical Analysis: Deterministic vs Randomized Quicksort
==========================================================
This script performs a comprehensive empirical comparison of both
Quicksort variants across different input sizes and distributions.
It generates performance plots saved as PNG images.

Author: [Your Name]
Course: [Your Course]
Date: February 2026
"""

import sys
import time
import random
import copy
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving plots
import matplotlib.pyplot as plt
import numpy as np

from quicksort import (
    quicksort, randomized_quicksort,
    generate_test_data, measure_time
)

# Increase recursion limit for worst-case scenarios
sys.setrecursionlimit(50000)


def run_experiments(sizes, distributions, num_trials=3):
    """
    Run sorting experiments across multiple sizes, distributions, and trials.
    
    Parameters:
        sizes (list): List of input sizes to test
        distributions (list): List of distribution types
        num_trials (int): Number of trials per configuration (results averaged)
    
    Returns:
        dict: Nested dictionary of results
              results[distribution][algorithm] = list of avg times per size
    """
    results = {}
    
    for dist in distributions:
        results[dist] = {"Deterministic": [], "Randomized": []}
        
        for size in sizes:
            det_times = []
            rand_times = []
            
            for trial in range(num_trials):
                arr = generate_test_data(size, dist)
                
                # Deterministic Quicksort
                try:
                    det_time = measure_time(quicksort, arr)
                    det_times.append(det_time)
                except RecursionError:
                    det_times.append(float('nan'))
                
                # Randomized Quicksort
                try:
                    rand_time = measure_time(randomized_quicksort, arr)
                    rand_times.append(rand_time)
                except RecursionError:
                    rand_times.append(float('nan'))
            
            avg_det = np.nanmean(det_times) if det_times else float('nan')
            avg_rand = np.nanmean(rand_times) if rand_times else float('nan')
            
            results[dist]["Deterministic"].append(avg_det)
            results[dist]["Randomized"].append(avg_rand)
            
            print(f"  Size={size:<6} Dist={dist:<15} "
                  f"Det={avg_det:.6f}s  Rand={avg_rand:.6f}s")
    
    return results


def plot_results(sizes, results, output_dir="."):
    """
    Generate comparison plots for the empirical analysis.
    
    Creates:
        1. Individual plots per distribution
        2. A combined overview plot
        3. A speedup ratio plot
    """
    distributions = list(results.keys())
    colors = {"Deterministic": "#E74C3C", "Randomized": "#2ECC71"}
    
    # --- Plot 1: Combined overview (2x2 grid) ---
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Quicksort Performance: Deterministic vs Randomized",
                 fontsize=16, fontweight='bold', y=0.98)
    
    for idx, dist in enumerate(distributions):
        row, col = idx // 2, idx % 2
        ax = axes[row][col]
        
        det_times = results[dist]["Deterministic"]
        rand_times = results[dist]["Randomized"]
        
        ax.plot(sizes, det_times, 'o-', color=colors["Deterministic"],
                label="Deterministic", linewidth=2, markersize=6)
        ax.plot(sizes, rand_times, 's-', color=colors["Randomized"],
                label="Randomized", linewidth=2, markersize=6)
        
        ax.set_title(f'{dist.replace("_", " ").title()} Input', fontsize=13, fontweight='bold')
        ax.set_xlabel('Input Size (n)', fontsize=11)
        ax.set_ylabel('Time (seconds)', fontsize=11)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.tick_params(labelsize=10)
    
    # If fewer than 4 distributions, hide extra subplot
    if len(distributions) < 4:
        axes[1][1].set_visible(False)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    combined_path = f"{output_dir}/combined_performance.png"
    plt.savefig(combined_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\nSaved: {combined_path}")
    
    # --- Plot 2: Speedup ratio ---
    fig, ax = plt.subplots(figsize=(10, 6))
    markers = ['o', 's', '^', 'D']
    dist_colors = ['#3498DB', '#E74C3C', '#2ECC71', '#9B59B6']
    
    for idx, dist in enumerate(distributions):
        det_times = np.array(results[dist]["Deterministic"])
        rand_times = np.array(results[dist]["Randomized"])
        
        # Speedup: how many times faster is randomized vs deterministic
        # Values > 1 mean randomized is faster
        with np.errstate(divide='ignore', invalid='ignore'):
            speedup = det_times / rand_times
            speedup = np.where(np.isfinite(speedup), speedup, np.nan)
        
        ax.plot(sizes, speedup, f'{markers[idx]}-', color=dist_colors[idx],
                label=dist.replace("_", " ").title(), linewidth=2, markersize=7)
    
    ax.axhline(y=1, color='gray', linestyle='--', alpha=0.7, label='Equal Performance')
    ax.set_title('Speedup Ratio: Deterministic Time / Randomized Time',
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('Input Size (n)', fontsize=12)
    ax.set_ylabel('Speedup Ratio', fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    speedup_path = f"{output_dir}/speedup_ratio.png"
    plt.savefig(speedup_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {speedup_path}")
    
    # --- Plot 3: Bar chart for specific size comparison ---
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Use the largest size for comparison
    x = np.arange(len(distributions))
    width = 0.35
    
    det_final = [results[d]["Deterministic"][-1] for d in distributions]
    rand_final = [results[d]["Randomized"][-1] for d in distributions]
    
    bars1 = ax.bar(x - width/2, det_final, width, label='Deterministic',
                   color=colors["Deterministic"], alpha=0.85, edgecolor='white')
    bars2 = ax.bar(x + width/2, rand_final, width, label='Randomized',
                   color=colors["Randomized"], alpha=0.85, edgecolor='white')
    
    ax.set_title(f'Performance at Largest Input Size (n={sizes[-1]})',
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('Input Distribution', fontsize=12)
    ax.set_ylabel('Time (seconds)', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels([d.replace("_", " ").title() for d in distributions])
    ax.legend(fontsize=11)
    ax.grid(True, axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        if not np.isnan(height):
            ax.annotate(f'{height:.4f}s', xy=(bar.get_x() + bar.get_width()/2, height),
                       xytext=(0, 3), textcoords="offset points",
                       ha='center', va='bottom', fontsize=9)
    for bar in bars2:
        height = bar.get_height()
        if not np.isnan(height):
            ax.annotate(f'{height:.4f}s', xy=(bar.get_x() + bar.get_width()/2, height),
                       xytext=(0, 3), textcoords="offset points",
                       ha='center', va='bottom', fontsize=9)
    
    bar_path = f"{output_dir}/bar_comparison.png"
    plt.savefig(bar_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {bar_path}")
    
    return [combined_path, speedup_path, bar_path]


def print_summary_table(sizes, results):
    """Print a formatted summary table of all results."""
    distributions = list(results.keys())
    
    print("\n" + "=" * 80)
    print("SUMMARY TABLE: Average Execution Times (seconds)")
    print("=" * 80)
    print(f"{'Size':<8}", end="")
    for dist in distributions:
        print(f"{'|  ' + dist.title():<22}", end="")
    print()
    print(f"{'':8}", end="")
    for _ in distributions:
        print(f"{'|  Det':>11}{'Rand':>11}", end="")
    print()
    print("-" * 80)
    
    for i, size in enumerate(sizes):
        print(f"{size:<8}", end="")
        for dist in distributions:
            det = results[dist]["Deterministic"][i]
            rand = results[dist]["Randomized"][i]
            det_str = f"{det:.5f}" if not np.isnan(det) else "N/A"
            rand_str = f"{rand:.5f}" if not np.isnan(rand) else "N/A"
            print(f"|  {det_str:>9} {rand_str:>9}", end="")
        print()
    print("=" * 80)


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EMPIRICAL ANALYSIS: Deterministic vs Randomized Quicksort")
    print("=" * 60)
    
    # Configuration
    SIZES = [500, 1000, 2000, 5000, 8000, 10000]
    DISTRIBUTIONS = ["random", "sorted", "reverse"]
    NUM_TRIALS = 3
    
    print(f"\nInput sizes: {SIZES}")
    print(f"Distributions: {DISTRIBUTIONS}")
    print(f"Trials per config: {NUM_TRIALS}")
    print(f"\nRunning experiments...\n")
    
    # Run experiments
    results = run_experiments(SIZES, DISTRIBUTIONS, NUM_TRIALS)
    
    # Print summary
    print_summary_table(SIZES, results)
    
    # Generate plots
    print("\nGenerating plots...")
    plot_files = plot_results(SIZES, results, output_dir=".")
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print("\nKey Observations:")
    print("  1. On RANDOM input, both algorithms perform similarly (O(n log n)).")
    print("  2. On SORTED/REVERSE input, deterministic Quicksort degrades to O(n^2)")
    print("     due to unbalanced partitions (pivot is always min or max).")
    print("  3. Randomized Quicksort maintains O(n log n) expected performance")
    print("     regardless of input distribution, as random pivot selection")
    print("     prevents consistently unbalanced partitions.")
    print("  4. The speedup ratio shows randomized version's advantage grows")
    print("     with input size on adversarial (sorted/reverse) inputs.")