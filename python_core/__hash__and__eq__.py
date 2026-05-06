"""
TOPIC: __hash__ and __eq__
======================================================

WHAT IS IT?
  Python uses __hash__ and __eq__ together to determine
  object identity in sets and dict keys.

  __eq__   → defines what "equal" means between two objects
  __hash__ → returns an integer used as a "bucket address"
              in hash tables (dict, set)

RULES / KEY POINTS:
  1. If __eq__ is defined, Python sets __hash__ = None by default.
     You MUST also define __hash__ manually, or the object becomes
     unhashable (cannot be used in set/dict).

  2. Objects that are equal MUST have the same hash.
     (a == b) → hash(a) == hash(b)   ← REQUIRED

  3. Objects with the same hash do NOT need to be equal.
     hash(a) == hash(b) → a == b is NOT guaranteed (hash collision)

  4. __hash__ should be based on immutable fields only.
     If you hash by a mutable field and it changes → bugs in dict/set.

  5. Default __hash__ (when not overriding) uses object's memory address (id).

COMMON PROBLEMS / PITFALLS:
  - Pitfall 1: Defining __eq__ but forgetting __hash__
      → TypeError: unhashable type when used in set/dict
  - Pitfall 2: Mutable objects in hash (e.g., list as field)
      → Never hash mutable fields, use tuple/frozenset instead
  - Pitfall 3: Relying on default __hash__ when you changed __eq__
      → Two "equal" objects end up in different dict buckets

WHEN TO USE IT:
  - Custom ORM models compared by ID
  - Caching objects by value (e.g. Product, User, Config)
  - Using custom objects as dict keys or in sets

RELATED TOPICS:
  - __eq__, __ne__
  - set, frozenset, dict internals
  - dataclasses (auto-generate hash)
"""


# ─────────────────────────────────────────────
# SECTION 1 — Default behavior (no overrides)
# ─────────────────────────────────────────────

class Product:
    """No __eq__ or __hash__ defined — uses Python defaults."""

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


p1 = Product("apple", 1.5)
p2 = Product("apple", 1.5)

# Even though p1 and p2 have identical data, they are different objects.
# Python compares by memory address (id) by default.
print(p1 == p2)       # False — different objects in memory
print(hash(p1))       # some integer based on id(p1)
print(hash(p2))       # different integer based on id(p2)

# Output:
#   False
#   <some number>
#   <different number>
# Why: No __eq__ defined → Python uses identity (is), not value equality.


# ─────────────────────────────────────────────
# SECTION 2 — Only __eq__ defined (BROKEN state)
# ─────────────────────────────────────────────

class BrokenProduct:
    """
    Defines __eq__ but NOT __hash__.
    Python automatically sets __hash__ = None.
    This makes the object UNHASHABLE.
    """

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __eq__(self, other: "BrokenProduct") -> bool:
        return self.name == other.name and self.price == other.price


bp1 = BrokenProduct("banana", 0.5)
bp2 = BrokenProduct("banana", 0.5)

print(bp1 == bp2)     # True — __eq__ works fine

# Trying to hash a BrokenProduct → TypeError
try:
    print(hash(bp1))
except TypeError as e:
    print(f"Error: {e}")

# Trying to use it in a set → TypeError
try:
    product_set = {bp1, bp2}
except TypeError as e:
    print(f"Set Error: {e}")

# Output:
#   True
#   Error: unhashable type: 'BrokenProduct'
#   Set Error: unhashable type: 'BrokenProduct'
# Why: When __eq__ is overridden, Python sets __hash__ = None as a safety
#      measure to prevent broken hashing behavior.


# ─────────────────────────────────────────────
# SECTION 3 — Correct: __eq__ + __hash__ together
# ─────────────────────────────────────────────

class FixedProduct:
    """
    Correctly implements both __eq__ and __hash__.
    Now works in set and dict.
    """

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __eq__(self, other: "FixedProduct") -> bool:
        # Two products are equal if name AND price match
        return self.name == other.name and self.price == other.price

    def __hash__(self) -> int:
        # Hash must be consistent with __eq__.
        # Use a tuple of the same fields used in __eq__.
        return hash((self.name, self.price))

    def __repr__(self) -> str:
        return f"Product({self.name!r}, {self.price})"


fp1 = FixedProduct("cherry", 2.0)
fp2 = FixedProduct("cherry", 2.0)
fp3 = FixedProduct("mango", 3.5)

print(fp1 == fp2)           # True — same name and price
print(fp1 == fp3)           # False — different products
print(hash(fp1) == hash(fp2))  # True — equal objects must have equal hash

# Now works in sets and dicts
product_set = {fp1, fp2, fp3}
print(len(product_set))     # 2 — fp1 and fp2 are "same" in set

product_price = {fp1: "cheap", fp3: "expensive"}
print(product_price[fp2])   # "cheap" — fp2 == fp1, same hash → same key

# Output:
#   True
#   False
#   True
#   2
#   cheap
# Why: __hash__ uses the same fields as __eq__, so Python correctly
#      identifies fp1 and fp2 as the same key in set/dict.


# ─────────────────────────────────────────────
# SECTION 4 — Real-world: User model comparison
# ─────────────────────────────────────────────

class User:
    """
    Compare users by email only.
    Two User objects with same email = same user.
    """

    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

    def __eq__(self, other: "User") -> bool:
        # Business rule: same email → same user (even different usernames)
        return self.email == other.email

    def __hash__(self) -> int:
        return hash(self.email)  # only email matters

    def __repr__(self) -> str:
        return f"User({self.username!r})"


alice1 = User("alice", "alice@example.com")
alice2 = User("ALICE", "alice@example.com")   # different username, same email
bob   = User("bob",   "bob@example.com")

# Deduplication using a set
users = {alice1, alice2, bob}
print(users)           # {User('alice'), User('bob')} — alice deduplicated
print(len(users))      # 2

# Lookup in dict
cache = {alice1: "cached_data"}
print(cache[alice2])   # "cached_data" — alice2 resolves same key as alice1

# Output:
#   {User('alice'), User('bob')}
#   2
#   cached_data
# Why: hash(alice1) == hash(alice2) and alice1 == alice2 → treated as one key.


# ─────────────────────────────────────────────
# TESTS — Edge cases and verification
# ─────────────────────────────────────────────

print("\n" + "=" * 50)
print("TESTS")
print("=" * 50)

# Test 1: Hash consistency — hash must not change over time
u = User("test", "test@example.com")
h1 = hash(u)
h2 = hash(u)
assert h1 == h2, "Hash must be stable across calls"
print(f"Test 1 PASSED — hash stable: {h1}")

# Test 2: Equal objects must have equal hash (fundamental rule)
u1 = User("a", "same@example.com")
u2 = User("b", "same@example.com")
assert u1 == u2, "Equal users failed"
assert hash(u1) == hash(u2), "Equal objects must have same hash"
print("Test 2 PASSED — equal objects have equal hash")

# Test 3: Set deduplication
u3 = User("x", "unique@example.com")
u4 = User("y", "unique@example.com")
result = len({u3, u4})
assert result == 1, f"Expected 1 unique user, got {result}"
print(f"Test 3 PASSED — set deduplication works, size={result}")

# Test 4: Dict key lookup using equivalent object
u5 = User("original", "key@example.com")
u6 = User("copy",     "key@example.com")
d = {u5: "value"}
assert d[u6] == "value", "Dict lookup by equivalent key failed"
print("Test 4 PASSED — dict lookup by equivalent key works")

# Test 5: Unhashable when only __eq__ defined
class OnlyEq:
    def __eq__(self, other): return True

obj = OnlyEq()
try:
    hash(obj)
    print("Test 5 FAILED — should have raised TypeError")
except TypeError:
    print("Test 5 PASSED — unhashable when only __eq__ defined")
