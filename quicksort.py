"""
Quicksort Algorithm: Deterministic and Randomized Implementations
=================================================================
This module provides both deterministic and randomized versions of the
Quicksort algorithm, along with utility functions for analysis.

Author: [Your Name]
Course: [Your Course]
Date: February 2026
"""

import random
import time
import copy


# =============================================================================
# DETERMINISTIC QUICKSORT
# =============================================================================

def partition(arr, low, high):
    """
    Partition the array around the last element as pivot.
    
    Elements smaller than the pivot are moved to the left,
    and elements greater are moved to the right.
    
    Parameters:
        arr (list): The array to partition
        low (int): Starting index of the subarray
        high (int): Ending index of the subarray (pivot position)
    
    Returns:
        int: The final position of the pivot element
    """
    pivot = arr[high]  # Choose last element as pivot
    i = low - 1        # Index of the smaller element boundary

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]  # Swap elements

    # Place pivot in its correct sorted position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quicksort(arr, low=None, high=None):
    """
    Deterministic Quicksort using the last element as pivot.
    
    This implementation follows the standard Quicksort algorithm as
    described in CLRS (Cormen et al., 2022). It selects the last element
    as the pivot, partitions the array, and recursively sorts the subarrays.
    
    Parameters:
        arr (list): The array to sort (sorted in-place)
        low (int): Starting index (default: 0)
        high (int): Ending index (default: len(arr) - 1)
    
    Returns:
        list: The sorted array
    
    Time Complexity:
        Best Case:    O(n log n) - balanced partitions
        Average Case: O(n log n) - expected with random input
        Worst Case:   O(n^2)     - already sorted or reverse-sorted input
    
    Space Complexity: O(log n) average, O(n) worst case (recursion stack)
    """
    if low is None:
        low = 0
    if high is None:
        high = len(arr) - 1

    if low < high:
        # Partition and get pivot index
        pivot_index = partition(arr, low, high)
        
        # Recursively sort elements before and after partition
        quicksort(arr, low, pivot_index - 1)
        quicksort(arr, pivot_index + 1, high)

    return arr


# =============================================================================
# RANDOMIZED QUICKSORT
# =============================================================================

def randomized_partition(arr, low, high):
    """
    Partition with a randomly chosen pivot.
    
    A random element from the subarray is selected and swapped with
    the last element, then standard partitioning is applied. This
    randomization helps avoid worst-case behavior on sorted inputs.
    
    Parameters:
        arr (list): The array to partition
        low (int): Starting index of the subarray
        high (int): Ending index of the subarray
    
    Returns:
        int: The final position of the pivot element
    """
    # Choose a random pivot and swap it with the last element
    random_index = random.randint(low, high)
    arr[random_index], arr[high] = arr[high], arr[random_index]
    
    return partition(arr, low, high)


def randomized_quicksort(arr, low=None, high=None):
    """
    Randomized Quicksort with random pivot selection.
    
    This version randomly selects a pivot element from the subarray
    before partitioning. By randomizing the pivot choice, we ensure
    that no specific input distribution consistently triggers worst-case
    behavior, achieving O(n log n) expected time for all inputs.
    
    Parameters:
        arr (list): The array to sort (sorted in-place)
        low (int): Starting index (default: 0)
        high (int): Ending index (default: len(arr) - 1)
    
    Returns:
        list: The sorted array
    
    Time Complexity:
        Expected: O(n log n) for ANY input distribution
        Worst Case: O(n^2) - extremely unlikely with randomization
    
    Space Complexity: O(log n) expected (recursion stack)
    """
    if low is None:
        low = 0
    if high is None:
        high = len(arr) - 1

    if low < high:
        # Partition with random pivot and get pivot index
        pivot_index = randomized_partition(arr, low, high)
        
        # Recursively sort elements before and after partition
        randomized_quicksort(arr, low, pivot_index - 1)
        randomized_quicksort(arr, pivot_index + 1, high)

    return arr


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def generate_test_data(size, distribution="random"):
    """
    Generate test arrays with different distributions.
    
    Parameters:
        size (int): Number of elements
        distribution (str): Type of distribution
            - "random": Random integers
            - "sorted": Already sorted array
            - "reverse": Reverse-sorted array
            - "nearly_sorted": Sorted with ~10% elements swapped
            - "duplicates": Array with many duplicate values
    
    Returns:
        list: Generated array
    """
    if distribution == "random":
        return [random.randint(0, size * 10) for _ in range(size)]
    elif distribution == "sorted":
        return list(range(size))
    elif distribution == "reverse":
        return list(range(size - 1, -1, -1))
    elif distribution == "nearly_sorted":
        arr = list(range(size))
        num_swaps = max(1, size // 10)
        for _ in range(num_swaps):
            i, j = random.randint(0, size - 1), random.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    elif distribution == "duplicates":
        return [random.randint(0, size // 10) for _ in range(size)]
    else:
        raise ValueError(f"Unknown distribution: {distribution}")


def measure_time(sort_func, arr):
    """
    Measure the execution time of a sorting function.
    
    Parameters:
        sort_func (callable): Sorting function to measure
        arr (list): Array to sort (a copy is made to preserve original)
    
    Returns:
        float: Execution time in seconds
    """
    arr_copy = copy.deepcopy(arr)
    start = time.perf_counter()
    sort_func(arr_copy)
    end = time.perf_counter()
    return end - start


def verify_sort(sort_func, test_cases=10, max_size=1000):
    """
    Verify that a sorting function produces correct results.
    
    Parameters:
        sort_func (callable): Sorting function to verify
        test_cases (int): Number of test cases to run
        max_size (int): Maximum array size for test cases
    
    Returns:
        bool: True if all tests pass
    """
    for i in range(test_cases):
        size = random.randint(0, max_size)
        arr = [random.randint(-10000, 10000) for _ in range(size)]
        expected = sorted(arr)
        result = sort_func(arr.copy())
        if result != expected:
            print(f"Test {i+1} FAILED: size={size}")
            return False
    print(f"All {test_cases} tests PASSED for {sort_func.__name__}")
    return True


# =============================================================================
# DEMONSTRATION
# =============================================================================

if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(20000)
    
    print("=" * 60)
    print("QUICKSORT ALGORITHM - DEMONSTRATION")
    print("=" * 60)
    
    # Verify correctness
    print("\n--- Correctness Verification ---")
    verify_sort(quicksort)
    verify_sort(randomized_quicksort)
    
    # Demo with small array
    print("\n--- Sorting Demonstration ---")
    sample = [38, 27, 43, 3, 9, 82, 10]
    print(f"Original array:  {sample}")
    print(f"Deterministic:   {quicksort(sample.copy())}")
    print(f"Randomized:      {randomized_quicksort(sample.copy())}")
    
    # Quick performance comparison
    print("\n--- Quick Performance Comparison ---")
    sizes = [1000, 5000, 10000]
    distributions = ["random", "sorted", "reverse"]
    
    print(f"\n{'Size':<8} {'Distribution':<15} {'Deterministic (s)':<20} {'Randomized (s)':<20}")
    print("-" * 65)
    
    for size in sizes:
        for dist in distributions:
            arr = generate_test_data(size, dist)
            
            # For sorted/reverse with deterministic, use smaller sizes to avoid recursion limit
            if dist in ("sorted", "reverse") and size > 5000:
                det_time = "N/A (recursion)"
            else:
                det_time = f"{measure_time(quicksort, arr):.6f}"
            
            rand_time = f"{measure_time(randomized_quicksort, arr):.6f}"
            print(f"{size:<8} {dist:<15} {det_time:<20} {rand_time:<20}")
    
    print("\n" + "=" * 60)
    print("Run 'python empirical_analysis.py' for full analysis with plots.")
    print("=" * 60)