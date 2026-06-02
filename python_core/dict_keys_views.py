"""
TOPIC: Dictionary Keys, Values, and Items Views
======================================================

WHAT IS IT?
  In Python 3, `dict.keys()`, `dict.values()`, and `dict.items()` return view objects instead of lists.
  These views provide a dynamic window on the dictionary's entries, meaning that when the dictionary changes, the view reflects these changes.

RULES / KEY POINTS:
  1. Dictionary views are dynamic (they update when the dict updates).
  2. `keys()` and `items()` views support set-like operations (union, intersection, difference) if values are hashable.
  3. You cannot index into a dictionary view (e.g., `keys[0]` will fail).

COMMON PROBLEMS / PITFALLS:
  - Pitfall 1: Trying to iterate and modify the dictionary at the same time (RuntimeError: dictionary changed size during iteration).
  - Pitfall 2: Trying to index a view. You must convert it to a list first: `list(my_dict.keys())[0]`.

WHEN TO USE IT:
  - When comparing keys of two dictionaries using set operations (e.g., `dict1.keys() & dict2.keys()`).
  - When iterating over large dictionaries efficiently without duplicating memory.

RELATED TOPICS:
  - Dictionaries
  - Sets
"""

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept
# ─────────────────────────────────────────────

person = {"name": "Bob", "age": 30}
keys_view = person.keys()
values_view = person.values()

# Adding a new item
person["city"] = "New York"

# ─────────────────────────────────────────────
# SECTION 2 — Advanced / Real-World Usage
# ─────────────────────────────────────────────

dict_a = {"x": 1, "y": 2, "z": 3}
dict_b = {"y": 20, "z": 30, "w": 40}

# Finding common keys using set intersection
common_keys = dict_a.keys() & dict_b.keys()

# Finding keys unique to dict_a
unique_a = dict_a.keys() - dict_b.keys()

# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print("Keys View:", keys_view)
    print("Common Keys:", common_keys)
    print("Unique to A:", unique_a)

# Output:
#   Keys View: dict_keys(['name', 'age', 'city'])
#   Common Keys: {'z', 'y'}
#   Unique to A: {'x'}
# Why: The keys_view dynamically includes 'city' even though it was created before 'city' was added. The views act like sets, allowing convenient intersections and differences.
