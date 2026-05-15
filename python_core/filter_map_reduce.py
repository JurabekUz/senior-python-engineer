"""
TOPIC: Functional Programming: lambda, map, filter, reduce
======================================================

WHAT IS IT?
  Python provides several tools that support a functional programming style. 
  These allow you to process data collections concisely without explicit loops.

RULES / KEY POINTS:
  1. **lambda**: Anonymous functions used for short, one-time tasks.
  2. **map(func, iter)**: Transforms every item in the iterable using `func`.
  3. **filter(func, iter)**: Keeps only items where `func(item)` is True.
  4. **reduce(func, iter)**: Progressively "reduces" a collection to a single 
     value (e.g., sum or product). Must be imported from `functools`.
  5. `map` and `filter` return **iterators**, so they are memory-efficient.

COMMON PROBLEMS / PITFALLS:
  - Readability: Overusing lambdas can make code cryptic.
  - Performance: For simple operations, List Comprehensions are often faster 
    and more "Pythonic" than map/filter.
  - Iterator Exhaustion: Results of map/filter can only be iterated once.

WHEN TO USE IT:
  - Data cleaning and transformation.
  - Applying a consistent operation to a stream of data.
  - Creating quick callback functions for sorting or UI events.

RELATED TOPICS:
  - List Comprehensions
  - Iterators
  - Functools module
"""

from functools import reduce

# ─────────────────────────────────────────────
# SECTION 1 — Lambda, Map, and Filter
# ─────────────────────────────────────────────

def basics_demo():
    print("--- Section 1: Lambda, Map, Filter ---")
    
    numbers = [1, 2, 3, 4, 5, 6]
    
    # 1. Lambda: A quick squaring function
    # Syntax: lambda arguments: expression
    square = lambda x: x ** 2  # noqa: E731
    print(f"Lambda square(5): {square(5)}")

    # 2. Map: Square all numbers
    squared_nums = map(lambda x: x ** 2, numbers)
    print(f"Map (Squared): {list(squared_nums)}")

    # 3. Filter: Keep only even numbers
    even_nums = filter(lambda x: x % 2 == 0, numbers)
    print(f"Filter (Evens): {list(even_nums)}")

# ─────────────────────────────────────────────
# SECTION 2 — Reduce and Real-World Comparison
# ─────────────────────────────────────────────

def advanced_demo():
    print("\n--- Section 2: Reduce & Alternatives ---")
    
    prices = [100, 250, 400, 50]
    
    # 1. Reduce: Calculate total sum
    total = reduce(lambda x, y: x + y, prices)
    print(f"Reduce (Total Price): {total}")

    # 2. Map + Filter combined (Functional Pipeline)
    # Goal: Get 10% discount on prices over 100
    expensive_items = filter(lambda p: p > 100, prices)
    discounted = map(lambda p: p * 0.9, expensive_items)
    print(f"Discounted expensive items: {list(discounted)}")

    # 3. The Pythonic Way: List Comprehension
    # (Usually preferred over map/filter for readability)
    pythonic = [p * 0.9 for p in prices if p > 100]
    print(f"List Comp (Same result): {pythonic}")

# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == "__main__":
    basics_demo()
    advanced_demo()

