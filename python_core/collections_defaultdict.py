"""
TOPIC: collections.defaultdict
======================================================

WHAT IS IT?
  defaultdict is a dictionary subclass that calls a factory function to supply 
  missing values. It never raises a KeyError for missing keys.

RULES / KEY POINTS:
  1. Default Factory: The first argument must be a callable (e.g., int, list, lambda).
  2. Missing Keys: When a key is accessed that doesn't exist, the factory function 
     is called without arguments to provide a default value.
  3. Storage: The default value is physically added to the dictionary.
  4. Standard dict methods: It supports all regular dictionary methods.

COMMON PROBLEMS / PITFALLS:
  - Unintentional insertions: Simply checking `if d['missing']:` will create the key 
    in the dictionary. Use `if 'key' in d:` or `d.get('key')` to avoid this.
  - Mutable defaults: Using a list as a factory is great, but remember that the 
    factory is called for *each* missing key (they get unique lists).

WHEN TO USE IT:
  - Grouping items (e.g., a dictionary where values are lists of items).
  - Counting items (using `int` as factory starts at 0).
  - Building tree structures or nested dictionaries.

RELATED TOPICS:
  - collections.Counter
  - dict.setdefault()
  - collections.ChainMap
"""

from collections import defaultdict

# ─────────────────────────────────────────────
# SECTION 1 — Basic Types
# ─────────────────────────────────────────────

# 1. Counting with 'int' (default is 0)
counts = defaultdict(int)
text = "apple banana apple orange banana apple"
for word in text.split():
    counts[word] += 1
print(f"Word counts: {dict(counts)}")

# 2. Grouping with 'list' (default is [])
groups = defaultdict(list)
pairs = [("fruit", "apple"), ("fruit", "banana"), ("veg", "carrot")]
for category, item in pairs:
    groups[category].append(item)
print(f"Grouped items: {dict(groups)}")

# ─────────────────────────────────────────────
# SECTION 2 — Custom Factories
# ─────────────────────────────────────────────

# Using lambda for custom defaults
# For example, a default value of "N/A"
user_data = defaultdict(lambda: "N/A")
user_data["name"] = "Jurabek"

print(f"Existing key: {user_data['name']}")
print(f"Missing key: {user_data['age']}") # Returns "N/A" and inserts it
print(f"Dictionary state: {dict(user_data)}")

# ─────────────────────────────────────────────
# SECTION 3 — Nested defaultdict (Advanced)
# ─────────────────────────────────────────────

# A tree-like structure
def tree():
    return defaultdict(tree)

taxonomy = tree()
taxonomy["Animalia"]["Chordata"]["Mammalia"]["Carnivora"]["Canidae"] = "Dog"
print(f"Nested data: {taxonomy['Animalia']['Chordata']['Mammalia']}")

# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n--- Final Test ---")
    test_dict = defaultdict(set)
    test_dict["odd"].add(1)
    test_dict["even"].add(2)
    test_dict["odd"].add(3)
    print(f"Sets result: {dict(test_dict)}")

# Output:
#   Word counts: {'apple': 3, 'banana': 2, 'orange': 1}
#   Grouped items: {'fruit': ['apple', 'banana'], 'veg': ['carrot']}
#   Existing key: Jurabek
#   Missing key: N/A
#   Dictionary state: {'name': 'Jurabek', 'age': 'N/A'}
#   Nested data: defaultdict(<function tree at ...>, {'Carnivora': defaultdict(<function tree at ...>, {'Canidae': 'Dog'})})
#   
#   --- Final Test ---
#   Sets result: {'odd': {1, 3}, 'even': {2}}
# Why:
#   1. int() returns 0, list() returns [], set() returns set().
#   2. defaultdict adds the missing key to the map automatically upon access.
#   3. lambda allows returning any constant or complex object as a default.
#   4. Recursive functions can create arbitrarily deep nested dictionaries.
