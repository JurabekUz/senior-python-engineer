"""
TOPIC: Enumerate and Zip
======================================================

WHAT IS IT?
  `enumerate()` is a built-in function that adds a counter to an iterable and returns it as an enumerate object.
  `zip()` is a built-in function that aggregates elements from two or more iterables, returning an iterator of tuples.

RULES / KEY POINTS:
  1. `enumerate(iterable, start=0)` allows you to specify the starting index.
  2. `zip()` stops when the shortest input iterable is exhausted.
  3. `itertools.zip_longest()` can be used if you want to zip up to the longest iterable.
  4. Both return iterators, so you can loop over them directly or convert them to a list.

COMMON PROBLEMS / PITFALLS:
  - Pitfall 1: Expecting `zip` to pad uneven lists automatically. It simply truncates instead.
  - Pitfall 2: Reusing a `zip` or `enumerate` iterator (they are single-pass iterators and will be exhausted after one iteration).

WHEN TO USE IT:
  - `enumerate`: When you need both the value and the index during a loop.
  - `zip`: When iterating over multiple related sequences simultaneously.

RELATED TOPICS:
  - Iterators
  - Generators
  - itertools
"""

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept
# ─────────────────────────────────────────────

names = ["Alice", "Bob", "Charlie"]
scores = [85, 92]

# enumerate
enum_result = list(enumerate(names, start=1))

# zip
zip_result = list(zip(names, scores))

# ─────────────────────────────────────────────
# SECTION 2 — Advanced / Real-World Usage
# ─────────────────────────────────────────────

# Creating a dictionary from two lists
headers = ["id", "name", "role"]
values = [101, "Alice", "Admin"]
user_dict = dict(zip(headers, values))

# Iterating over both lists with an index
for index, (name, score) in enumerate(zip(names, scores)):
    pass # we can access index, name, score all together

# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print("Enumerate:", enum_result)
    print("Zip:", zip_result)
    print("User Dict:", user_dict)

# Output:
#   Enumerate: [(1, 'Alice'), (2, 'Bob'), (3, 'Charlie')]
#   Zip: [('Alice', 85), ('Bob', 92)]
#   User Dict: {'id': 101, 'name': 'Alice', 'role': 'Admin'}
# Why: `enumerate` assigns indexes starting from 1. `zip` pairs elements but stops after 'Bob' because `scores` only has 2 elements. `dict(zip(...))` is a common idiom to map keys to values.
