"""
TOPIC: Generators
======================================================

WHAT IS IT?
  Generators are functions that act like iterators. They use the `yield` 
  keyword to pause execution and return a value, maintaining their state 
  to resume exactly where they left off when the next value is requested.

RULES / KEY POINTS:
  1. A function with `yield` returns a generator object, not the actual values.
  2. Generators follow the iterator protocol (__iter__ and __next__).
  3. They are "Lazy": values are computed only when requested (on-demand).
  4. Memory Efficient: They don't store the entire sequence in memory.
  5. Once a generator reaches the end or a `return`, it raises `StopIteration`.

COMMON PROBLEMS / PITFALLS:
  - Exhaustion: You cannot iterate over a generator twice.
  - Return values: `return` inside a generator terminates it (StopIteration).
  - List conversion: `list(my_generator)` defeats the memory-saving purpose.

WHEN TO USE IT:
  - Processing large files line-by-line.
  - Generating infinite sequences (like mathematical series).
  - Streaming data from a database or API.

RELATED TOPICS:
  - Iterators (__iter__, __next__)
  - List Comprehensions
  - Memory Management
"""

import sys

# ─────────────────────────────────────────────
# SECTION 1 — Generator Functions
# ─────────────────────────────────────────────

def simple_generator(limit):
    """A basic generator function using yield."""
    print("--- Generator Started ---")
    current = 0
    while current < limit:
        yield current
        current += 1
    print("--- Generator Finished ---")

def generator_function_demo():
    print("--- Section 1: Generator Function ---")
    gen = simple_generator(3)
    
    # Values are produced one by one
    print(f"Next 1: {next(gen)}")
    print(f"Next 2: {next(gen)}")
    print(f"Next 3: {next(gen)}")
    
    # Trying next(gen) again would raise StopIteration

# ─────────────────────────────────────────────
# SECTION 2 — Generator Expressions & Memory
# ─────────────────────────────────────────────

def memory_comparison_demo():
    print("\n--- Section 2: Memory & Expressions ---")
    
    # List comprehension (Immediate, uses memory)
    my_list = [i for i in range(10000)]
    print(f"List size: {sys.getsizeof(my_list)} bytes")
    
    # Generator expression (Lazy, saves memory)
    my_gen = (i for i in range(10000))
    print(f"Generator size: {sys.getsizeof(my_gen)} bytes")
    
    # Fibonacci Generator (Infinite sequence example)
    def fibonacci():
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

    fib = fibonacci()
    print("First 5 Fibonacci numbers:")
    for _ in range(5):
        print(next(fib), end=" ")
    print()

# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == "__main__":
    generator_function_demo()
    memory_comparison_demo()

# Output:
#   --- Section 1: Generator Function ---
#   --- Generator Started ---
#   Next 1: 0
#   Next 2: 1
#   Next 3: 2
#   --- Generator Finished --- (This actually prints if we consumed it via loop)
#
#   --- Section 2: Memory & Expressions ---
#   List size: 85176 bytes (approx)
#   Generator size: 104 bytes (approx)
#   First 5 Fibonacci numbers:
#   0 1 1 2 3
#
# Why:
#   - In Section 1, the print "Generator Started" only happens when first value is requested.
#   - Section 2 shows the massive memory difference. A list stores all 10k items, 
#     while a generator only stores the logic and current state.
#   - The Fibonacci generator demonstrates how we can represent infinite data 
#     without crashing the computer.
