"""
Search Assignment Starter Code
Implement three search algorithms and benchmark their performance.
"""

import json
import time
import random


# ============================================================================
# PART 1: Linear Search
# ============================================================================

def linear_search(data, target):
    """
    Search for target in data using linear search.

    Linear search checks each element sequentially until finding the target
    or reaching the end of the list.

    Args:
        data (list): List to search (can be sorted or unsorted)
        target: Item to find

    Returns:
        int: Index of target if found, -1 if not found

    Time Complexity: O(n) - must check up to n elements
    Space Complexity: O(1) - uses constant extra space
    """

    for i in range(len(data)):
        if data[i] == target:
            return i

    return -1


# ============================================================================
# PART 2: Binary Search (Iterative)
# ============================================================================

def binary_search_iterative(data, target):
    """
    Search for target in SORTED data using iterative binary search.

    Binary search repeatedly divides the search space in half by comparing
    the target to the middle element.

    Args:
        data (list): SORTED list to search
        target: Item to find

    Returns:
        int: Index of target if found, -1 if not found

    Time Complexity: O(log n) - divides search space in half each iteration
    Space Complexity: O(1) - uses constant extra space

    IMPORTANT: This only works on SORTED data!
    """

    left = 0
    right = len(data) - 1

    while left <= right:
        middle = (left + right) // 2

        if data[middle] == target:
            return middle
        elif data[middle] < target:
            left = middle + 1
        else:
            right = middle - 1

    return -1


# ============================================================================
# PART 3: Binary Search (Recursive)
# ============================================================================

def binary_search_recursive(data, target, left=None, right=None):
    """
    Search for target in SORTED data using recursive binary search.

    This is the recursive version of binary search, which naturally expresses
    the divide-and-conquer approach.

    Args:
        data (list): SORTED list to search
        target: Item to find
        left (int): Left boundary of search space
        right (int): Right boundary of search space

    Returns:
        int: Index of target if found, -1 if not found

    Time Complexity: O(log n)
    Space Complexity: O(log n) - recursion call stack
    """

    # Handle default parameters on first call
    if left is None:
        left = 0
    if right is None:
        right = len(data) - 1

    # Base case: target was not found
    if left > right:
        return -1

    # Find the middle element
    middle = (left + right) // 2

    # Target found
    if data[middle] == target:
        return middle

    # Search the right half
    elif data[middle] < target:
        return binary_search_recursive(data, target, middle + 1, right)

    # Search the left half
    else:
        return binary_search_recursive(data, target, left, middle - 1)


# ============================================================================
# BENCHMARKING & TESTING
# ============================================================================

def load_dataset(filename):
    """Load a dataset from JSON file."""
    with open(f"datasets/{filename}", "r") as f:
        return json.load(f)


def load_test_cases():
    """Load test cases for validation."""
    with open("datasets/test_cases.json", "r") as f:
        return json.load(f)


def test_search_correctness():
    """Test that search functions work correctly."""
    print("=" * 70)
    print("TESTING SEARCH CORRECTNESS")
    print("=" * 70 + "\n")

    # Simple test data
    sorted_data = [1, 3, 5, 7, 9, 11, 13, 15]
    unsorted_data = [7, 2, 9, 1, 5, 13, 3, 11]

    print("Test 1: Linear search on unsorted data")
    result = linear_search(unsorted_data, 9)
    print(f"  linear_search({unsorted_data}, 9) = {result}")
    print(
        f"  Expected: 2, Got: {result}, "
        f"{'✓ PASS' if result == 2 else '✗ FAIL'}"
    )

    print("\nTest 2: Linear search - item not found")
    result = linear_search(unsorted_data, 99)
    print(f"  linear_search({unsorted_data}, 99) = {result}")
    print(
        f"  Expected: -1, Got: {result}, "
        f"{'✓ PASS' if result == -1 else '✗ FAIL'}"
    )

    print("\nTest 3: Binary search iterative on sorted data")
    result = binary_search_iterative(sorted_data, 9)
    print(f"  binary_search_iterative({sorted_data}, 9) = {result}")
    print(
        f"  Expected: 4, Got: {result}, "
        f"{'✓ PASS' if result == 4 else '✗ FAIL'}"
    )

    print("\nTest 4: Binary search iterative - item not found")
    result = binary_search_iterative(sorted_data, 10)
    print(f"  binary_search_iterative({sorted_data}, 10) = {result}")
    print(
        f"  Expected: -1, Got: {result}, "
        f"{'✓ PASS' if result == -1 else '✗ FAIL'}"
    )

    print("\nTest 5: Binary search recursive on sorted data")
    result = binary_search_recursive(sorted_data, 13)
    print(f"  binary_search_recursive({sorted_data}, 13) = {result}")
    print(
        f"  Expected: 6, Got: {result}, "
        f"{'✓ PASS' if result == 6 else '✗ FAIL'}"
    )

    print("\nTest 6: Binary search recursive - item not found")
    result = binary_search_recursive(sorted_data, 8)
    print(f"  binary_search_recursive({sorted_data}, 8) = {result}")
    print(
        f"  Expected: -1, Got: {result}, "
        f"{'✓ PASS' if result == -1 else '✗ FAIL'}"
    )


def benchmark_algorithm(search_func, data, targets):
    """
    Benchmark a search algorithm on given data with multiple targets.

    Args:
        search_func: The search function to test
        data: The dataset to search
        targets: List of items to search for

    Returns:
        float: Average time per search in seconds
    """
    start = time.time()

    for target in targets:
        search_func(data, target)

    end = time.time()
    return (end - start) / len(targets)


def benchmark_all_datasets():
    """Benchmark all search algorithms on all datasets."""
    print("\n" + "=" * 70)
    print("BENCHMARKING SEARCH ALGORITHMS")
    print("=" * 70 + "\n")

    datasets = {
        "customer_ids.json": "Unsorted Customer IDs (100K)",
        "product_catalog.json": "Pre-sorted Product Catalog (50K)",
        "config_settings.json": "Small Config Settings (500)",
        "dictionary_words.json": "Dictionary Words (10K)"
    }

    test_cases = load_test_cases()

    for filename, description in datasets.items():
        print(f"Dataset: {description}")
        print("-" * 70)

        data = load_dataset(filename)
        dataset_key = filename.replace(".json", "")

        # Get targets to search for
        targets = (
            test_cases[dataset_key]["present"][:50]
            + test_cases[dataset_key]["absent"][:50]
        )
        random.shuffle(targets)

        # Benchmark linear search
        linear_time = benchmark_algorithm(linear_search, data, targets)
        print(
            f"  Linear Search:              "
            f"{linear_time * 1000:.4f} ms per search"
        )

        # For unsorted data, sort it first for binary search
        if (
            "unsorted" in description.lower()
            or "small config" in description.lower()
        ):
            sorted_data = sorted(data)

            sort_start = time.time()
            sorted(data)
            sort_time = time.time() - sort_start

            print(
                f"  Time to sort data:          "
                f"{sort_time * 1000:.2f} ms (one-time cost)"
            )
        else:
            sorted_data = data
            sort_time = 0

        # Benchmark binary search iterative
        binary_iter_time = benchmark_algorithm(
            binary_search_iterative, sorted_data, targets
        )

        print(
            f"  Binary Search (Iterative):  "
            f"{binary_iter_time * 1000:.4f} ms per search"
        )

        # Benchmark binary search recursive
        binary_rec_time = benchmark_algorithm(
            binary_search_recursive, sorted_data, targets
        )

        print(
            f"  Binary Search (Recursive):  "
            f"{binary_rec_time * 1000:.4f} ms per search"
        )

        # Calculate speedup
        if binary_iter_time > 0:
            speedup = linear_time / binary_iter_time
            print(
                f"  Binary speedup:             "
                f"{speedup:.2f}x faster than linear"
            )

        print()


def analyze_preprocessing_costs():
    """Analyze when sorting overhead is worth it."""
    print("=" * 70)
    print("PREPROCESSING COST ANALYSIS")
    print("=" * 70 + "\n")

    # Use customer IDs dataset
    data = load_dataset("customer_ids.json")
    test_cases = load_test_cases()
    targets = test_cases["customer_ids"]["present"][:100]

    # Measure sort time
    sort_start = time.time()
    sorted_data = sorted(data)
    sort_time = time.time() - sort_start

    # Measure search times
    linear_time = benchmark_algorithm(
        linear_search, data, targets[:10]
    )

    binary_time = benchmark_algorithm(
        binary_search_iterative, sorted_data, targets[:10]
    )

    print("Dataset: Customer IDs (100,000 unsorted entries)")
    print(f"One-time sort cost: {sort_time * 1000:.2f} ms")
    print(f"Linear search time: {linear_time * 1000:.4f} ms per search")
    print(f"Binary search time: {binary_time * 1000:.4f} ms per search")
    print(
        f"Time saved per search: "
        f"{(linear_time - binary_time) * 1000:.4f} ms\n"
    )

    # Calculate break-even point
    time_saved_per_search = linear_time - binary_time

    if time_saved_per_search > 0:
        searches_to_break_even = sort_time / time_saved_per_search

        print(
            f"Break-even point: "
            f"{int(searches_to_break_even)} searches"
        )

        print(
            f"After {int(searches_to_break_even)} searches, "
            f"sorting + binary search becomes faster\n"
        )


if __name__ == "__main__":
    print("SEARCH ASSIGNMENT - STARTER CODE")
    print("Implement the search functions above, then run tests.\n")

    # Test the search functions
    test_search_correctness()

    # Leave these commented for now.
    # We will run them after confirming the tests pass.

    benchmark_all_datasets()
    analyze_preprocessing_costs()