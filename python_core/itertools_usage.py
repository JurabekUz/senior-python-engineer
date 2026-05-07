"""
TOPIC: Iterators & Itertools
======================================================

WHAT IS IT?
  Iterators are objects that implement the iterator protocol, consisting of 
  __iter__() and __next__(). The `itertools` module provides a set of fast, 
  memory-efficient tools that work with iterators to handle complex iteration.

RULES / KEY POINTS:
  1. An **Iterable** is something you can get an iterator from (e.g., list, str).
  2. An **Iterator** is the object that actually does the traversing.
  3. Iterators are "lazy": they only calculate the next value when requested.
  4. Once an iterator raises `StopIteration`, it is "exhausted" and cannot be reset.
  5. `itertools` functions return iterators, saving memory for large datasets.

COMMON PROBLEMS / PITFALLS:
  - Infinite Iterators: `itertools.count()` or `cycle()` will run forever if not sliced or broken.
  - Consuming Iterators: Calling `list(my_iterator)` consumes it entirely.
  - Nesting: Deeply nested `itertools` chains can become hard to debug.

WHEN TO USE IT:
  - Processing logs or large CSV files line-by-line.
  - Generating combinations/permutations for algorithms.
  - Grouping or windowing data streams.

RELATED TOPICS:
  - Generators (yield)
  - List Comprehensions
  - Dunder methods (__iter__, __next__)
"""

import itertools

# ─────────────────────────────────────────────
# SECTION 1 — Iterator Protocol Basics
# ─────────────────────────────────────────────

class MyCounter:
    """A custom iterator that counts from start to end."""
    def __init__(self, low, high):
        self.current = low
        self.high = high

    def __iter__(self):
        # Must return the iterator object itself
        return self

    def __next__(self):
        # Must return the next value or raise StopIteration
        if self.current > self.high:
            raise StopIteration
        else:
            self.current += 1
            return self.current - 1

def basic_iterator_demo():
    print("--- Section 1: Custom Iterator ---")
    counter = MyCounter(1, 3)
    
    # Manual iteration
    it = iter(counter)
    print(f"First: {next(it)}")
    print(f"Second: {next(it)}")
    print(f"Third: {next(it)}")
    # print(next(it)) # This would raise StopIteration

# ─────────────────────────────────────────────
# SECTION 2 — Itertools Power Tools
# ─────────────────────────────────────────────

def itertools_demo():
    print("\n--- Section 2: Itertools Mastery ---")
    
    # 1. chain: Combine multiple iterables
    combined = itertools.chain([1, 2], "AB", (9, 10))
    print(f"Chain: {list(combined)}")

    # 2. islice: Slice an iterator (very important for infinite ones)
    infinite_count = itertools.count(10, 5) # 10, 15, 20...
    sliced = itertools.islice(infinite_count, 5)
    print(f"iSlice (first 5 of count): {list(sliced)}")

    # 3. cycle: Repeat an iterable indefinitely
    colors = ["Red", "Green"]
    cycled = itertools.islice(itertools.cycle(colors), 5)
    print(f"Cycle: {list(cycled)}")

    # 4. groupby: Group adjacent elements (requires sorting)
    data = [("A", 1), ("A", 2), ("B", 3), ("B", 4), ("A", 5)]
    # Note: Only groups *consecutive* identical keys
    for key, group in itertools.groupby(data, lambda x: x[0]):
        print(f"Group {key}: {list(group)}")

    # 5. product: Cartesian product (nested loops replacement)
    pairs = itertools.product([1, 2], ["A", "B"])
    print(f"Product: {list(pairs)}")

# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == "__main__":
    basic_iterator_demo()
    itertools_demo()

# Output:
#   --- Section 1: Custom Iterator ---
#   First: 1
#   Second: 2
#   Third: 3
#
#   --- Section 2: Itertools Mastery ---
#   Chain: [1, 2, 'A', 'B', 9, 10]
#   iSlice (first 5 of count): [10, 15, 20, 25, 30]
#   Cycle: ['Red', 'Green', 'Red', 'Green', 'Red']
#   Group A: [('A', 1), ('A', 2)]
#   Group B: [('B', 3), ('B', 4)]
#   Group A: [('A', 5)]
#   Product: [(1, 'A'), (1, 'B'), (2, 'A'), (2, 'B')]
#
# Why:
#   - Section 1 shows how __iter__ and __next__ work together to define an iterator.
#   - chain merges different types of iterables into one stream.
#   - islice is used to safely consume only a part of an infinite count() generator.
#   - groupby only groups *consecutive* items, which is why 'A' appears twice in the output.
#   - product avoids multiple nested for-loops, making code cleaner.
