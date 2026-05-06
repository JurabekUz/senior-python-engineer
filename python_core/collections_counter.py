"""
TOPIC: collections.Counter
======================================================

WHAT IS IT?
  Counter is a dict subclass for counting hashable objects. It is a collection where 
  elements are stored as dictionary keys and their counts are stored as dictionary values.

RULES / KEY POINTS:
  1. Counts can be any integer value including zero or negative counts.
  2. Accessing a missing key returns 0 instead of raising a KeyError.
  3. It is part of the 'collections' module (standard library).
  4. Most common use cases: counting frequency of items in a list or characters in a string.

COMMON PROBLEMS / PITFALLS:
  - Memory: Counting extremely large datasets in-memory can consume a lot of RAM.
  - Type: It only works for hashable objects (keys must be hashable).
  - Subtle Difference: `update()` adds counts, while `subtract()` decreases them.

WHEN TO USE IT:
  - Analyzing word frequency in text.
  - Finding the most frequent items in a dataset.
  - Comparing two sets of items for equality in terms of frequency.

RELATED TOPICS:
  - collections.defaultdict
  - itertools.chain
  - dictionary methods
"""

from collections import Counter

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept
# ─────────────────────────────────────────────

# Initialization
chars = Counter("abracadabra")
print(f"Character counts: {chars}")

words = Counter(["apple", "banana", "apple", "orange", "banana", "apple"])
print(f"Word counts: {words}")

# Accessing values (no KeyError)
print(f"Count of 'apple': {words['apple']}")
print(f"Count of 'pear' (missing): {words['pear']}")

# ─────────────────────────────────────────────
# SECTION 2 — Useful Methods
# ─────────────────────────────────────────────

# most_common(n) - Returns a list of the n most common elements
print(f"Top 2 words: {words.most_common(2)}")

# elements() - Returns an iterator over elements repeating each as many times as its count
data = Counter(a=2, b=1, c=0, d=-1)
print(f"Elements in {data}: {list(data.elements())}") # Note: ignores 0 and negative counts

# update() vs subtract()
c1 = Counter(a=3, b=1)
c1.update(a=1, b=2)   # Adds counts
print(f"After update: {c1}")

c1.subtract(a=2, b=1) # Subtracts counts
print(f"After subtract: {c1}")

# ─────────────────────────────────────────────
# SECTION 3 — Arithmetic Operations
# ─────────────────────────────────────────────

a = Counter(a=3, b=1)
b = Counter(a=1, b=2)

print(f"Addition (a + b): {a + b}")         # Keeps positive counts only
print(f"Subtraction (a - b): {a - b}")      # Keeps positive counts only
print(f"Intersection (a & b): {a & b}")     # Min of counts
print(f"Union (a | b): {a | b}")            # Max of counts

# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # Test instance
    test_counter = Counter("mississippi")
    print("\n--- Final Test ---")
    print(f"Most common 2 in 'mississippi': {test_counter.most_common(2)}")
    
# Output:
#   Character counts: Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})
#   Word counts: Counter({'apple': 3, 'banana': 2, 'orange': 1})
#   Count of 'apple': 3
#   Count of 'pear' (missing): 0
#   Top 2 words: [('apple', 3), ('banana', 2)]
#   Elements in Counter({'a': 2, 'b': 1, 'c': 0, 'd': -1}): ['a', 'a', 'b']
#   After update: Counter({'a': 4, 'b': 3})
#   After subtract: Counter({'a': 2, 'b': 2})
#   Addition (a + b): Counter({'a': 4, 'b': 3})
#   Subtraction (a - b): Counter({'a': 2})
#   Intersection (a & b): Counter({'a': 1, 'b': 1})
#   Union (a | b): Counter({'a': 3, 'b': 2})
#
#   --- Final Test ---
#   Most common 2 in 'mississippi': [('i', 4), ('s', 4)]
# Why: 
#   1. Initial counts are calculated correctly.
#   2. Missing keys return 0.
#   3. elements() skips non-positive values.
#   4. Arithmetic operations automatically strip non-positive results.
