# Quicksort Algorithm: Implementation, Analysis, and Randomization

## Overview

This repository contains a comprehensive implementation and analysis of the Quicksort algorithm for **[Your Course Name]**. It includes both deterministic and randomized versions of Quicksort, along with empirical performance analysis across different input distributions.

## Repository Structure

```
├── quicksort.py              # Core implementations (deterministic & randomized)
├── empirical_analysis.py     # Empirical comparison with plot generation
├── report.md                 # Detailed written report with analysis
├── combined_performance.png  # Performance comparison plots
├── speedup_ratio.png         # Speedup ratio visualization
├── bar_comparison.png        # Bar chart comparison at largest input size
├── screenshots/
│   ├── quicksort.png         # Screenshot of quicksort.py execution
│   └── empirical_analysis.png # Screenshot of empirical_analysis.py execution
└── README.md                 # This file
```

## Requirements

- **Python 3.8+**
- **matplotlib** (for generating plots)
- **numpy** (for numerical computations)

Install dependencies:

```bash
python -m pip install matplotlib numpy
```

## How to Run

### 1. Run the Quicksort Demo

Demonstrates both sorting algorithms with correctness verification and a quick performance comparison:

```bash
python quicksort.py
```

### 2. Run the Full Empirical Analysis

Executes comprehensive experiments across multiple input sizes and distributions, then generates performance plots:

```bash
python empirical_analysis.py
```

This will:

- Test input sizes: 500, 1000, 2000, 5000, 8000, 10000
- Test distributions: random, sorted, reverse-sorted
- Run 3 trials per configuration and average the results
- Generate three PNG plot files in the current directory

**Note:** The script increases Python's recursion limit to handle worst-case scenarios with the deterministic version. On very large sorted inputs, the deterministic version may still hit recursion limits or take significant time due to O(n²) behavior.

## Key Findings

| Input Distribution | Deterministic (n=10,000) | Randomized (n=10,000) | Speedup                     |
| ------------------ | ------------------------ | --------------------- | --------------------------- |
| Random             | ~0.009s                  | ~0.012s               | 0.8x (Det. slightly faster) |
| Sorted             | ~2.94s                   | ~0.011s               | **~270x**                   |
| Reverse-Sorted     | ~2.06s                   | ~0.012s               | **~176x**                   |

### Summary

- **Random input**: Both algorithms perform similarly at O(n log n). The deterministic version has a slight edge due to avoiding random number generation overhead.
- **Sorted/Reverse input**: The deterministic version degrades to O(n²) because the last-element pivot creates maximally unbalanced partitions. The randomized version maintains O(n log n) expected time regardless of input distribution.
- **Practical takeaway**: Randomized Quicksort is strongly preferred in production systems where input distributions cannot be guaranteed.

## Algorithm Details

### Deterministic Quicksort

- **Pivot selection**: Last element of the subarray
- **Best/Average case**: O(n log n)
- **Worst case**: O(n²) on sorted/reverse-sorted input
- **Space**: O(log n) average, O(n) worst case

### Randomized Quicksort

- **Pivot selection**: Random element from the subarray
- **Expected time**: O(n log n) for **any** input
- **Worst case**: O(n²) — extremely unlikely
- **Space**: O(log n) expected

## Screenshots

### Running quicksort.py

![Quicksort Demo](screenshots/quicksort.png)

### Running empirical_analysis.py

![Empirical Analysis](screenshots/empirical_analysis.png)

## References

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). _Introduction to Algorithms_ (4th ed.). MIT Press.
- Hoare, C. A. R. (1962). Quicksort. _The Computer Journal_, 5(1), 10–16.

## Author

**[Your Name]**  
[Your Course] — February 2026
