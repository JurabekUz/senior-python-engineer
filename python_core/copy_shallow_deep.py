"""
TOPIC: Shallow vs Deep Copy
======================================================

WHAT IS IT?
  In Python, assignment (`=`) creates a reference, not a copy. The `copy` module provides methods to duplicate objects.
  A shallow copy constructs a new collection and populates it with references to the child objects.
  A deep copy constructs a new collection and recursively populates it with copies of the child objects.

RULES / KEY POINTS:
  1. `copy.copy(obj)` creates a shallow copy.
  2. `copy.deepcopy(obj)` creates a deep copy.
  3. For immutable objects (like strings, integers, tuples containing immutable objects), copying just returns a reference to the original object.

COMMON PROBLEMS / PITFALLS:
  - Pitfall 1: Using a shallow copy for nested lists or dictionaries, and modifying the nested object, inadvertently changing the original object as well.

WHEN TO USE IT:
  - Use shallow copy when you want a new collection but are fine with sharing references to inner objects.
  - Use deep copy when you need an entirely independent clone of a nested data structure.

RELATED TOPICS:
  - References vs Values
  - Mutability
"""

import copy

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept
# ─────────────────────────────────────────────

original_list = [1, 2, [3, 4]]
shallow_copied_list = copy.copy(original_list)
deep_copied_list = copy.deepcopy(original_list)

# Modifying a nested object affects the shallow copy but not the deep copy
original_list[2].append(5)

# ─────────────────────────────────────────────
# SECTION 2 — Advanced / Real-World Usage
# ─────────────────────────────────────────────

class User:
    def __init__(self, name, settings):
        self.name = name
        self.settings = settings
        
user1 = User("Alice", {"theme": "dark", "notifications": True})
# Creating a completely independent user profile to test changes
user_test = copy.deepcopy(user1)
user_test.settings["theme"] = "light"

# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print("Original:", original_list)
    print("Shallow:", shallow_copied_list)
    print("Deep:", deep_copied_list)
    
    print("User1 Theme:", user1.settings["theme"])
    print("UserTest Theme:", user_test.settings["theme"])

# Output:
#   Original: [1, 2, [3, 4, 5]]
#   Shallow: [1, 2, [3, 4, 5]]
#   Deep: [1, 2, [3, 4]]
#   User1 Theme: dark
#   UserTest Theme: light
# Why: Shallow copy references the same inner list as the original, so modifications appear in both. Deep copy recursively duplicates all objects, so they remain independent.
