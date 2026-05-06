"""
TOPIC: collections.namedtuple
======================================================

WHAT IS IT?
  namedtuple is a factory function for creating tuple subclasses with named fields. 
  It allows you to access elements by name (obj.field) as well as by index (obj[0]).

RULES / KEY POINTS:
  1. Immutable: Like regular tuples, you cannot change values after creation.
  2. Memory efficient: They have the same memory footprint as regular tuples (no __dict__).
  3. Access: Supports dot notation, indexing, and unpacking.
  4. Typename: The first argument is the name of the class being created.

COMMON PROBLEMS / PITFALLS:
  - Immutability: Trying to assign a value (e.g., `p.x = 10`) raises an AttributeError.
  - Typename mismatch: The variable name and the typename (1st arg) are usually the same, 
    but they don't have to be. This can be confusing.
  - Field names: Cannot start with a number or be a Python keyword.

WHEN TO USE IT:
  - Returning structured data from functions without the overhead of a full class.
  - Improving code readability over standard tuples where indices like `data[3]` are cryptic.

RELATED TOPICS:
  - typing.NamedTuple (class-based version with type hints)
  - dataclasses.dataclass
  - collections.deque
"""

from collections import namedtuple

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept
# ─────────────────────────────────────────────

# Creation: namedtuple(typename, field_names)
# field_names can be a list of strings or a single space/comma separated string
Point = namedtuple("Point", ["x", "y", "z"])

# Instantiation
p = Point(10, 20, 30)
print(f"Point: {p}")

# Accessing fields
print(f"By name (p.x): {p.x}")
print(f"By index (p[1]): {p[1]}")

# Unpacking
x, y, z = p
print(f"Unpacked: {x}, {y}, {z}")

# ─────────────────────────────────────────────
# SECTION 2 — Advanced Methods
# ─────────────────────────────────────────────

# _make(iterable): Create a new instance from an existing sequence or iterable
data = [100, 200, 300]
p2 = Point._make(data)
print(f"Created via _make: {p2}")

# _asdict(): Returns an OrderedDict (or dict in 3.7+) mapping field names to values
print(f"As dictionary: {p2._asdict()}")

# _replace(**kwargs): Returns a NEW instance with specified fields replaced
p3 = p2._replace(z=999)
print(f"After _replace (original p2 unchanged): {p3}")
print(f"Verify p2 is still: {p2}")

# ─────────────────────────────────────────────
# SECTION 3 — Default Values (Python 3.7+)
# ─────────────────────────────────────────────

# Use the 'defaults' parameter to set default values from the right-most fields
Person = namedtuple("Person", "name age job", defaults=["Unemployed"])
p_default = Person("Jurabek", 25)
print(f"Person with default job: {p_default}")

# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n--- Final Test ---")
    # Demonstrating the "nom" example from playground
    PlayPoint = namedtuple("nom", ["x", "y", "z"])
    pp = PlayPoint(x=1, y=2, z=3)
    print(f"Playground Point (typename='nom'): {pp}")
    print(f"Type of pp: {type(pp).__name__}") # This will be 'nom'

# Output:
#   Point: Point(x=10, y=20, z=30)
#   By name (p.x): 10
#   By index (p[1]): 20
#   Unpacked: 10, 20, 30
#   Created via _make: Point(x=100, y=200, z=300)
#   As dictionary: {'x': 100, 'y': 200, 'z': 300}
#   After _replace (original p2 unchanged): Point(x=100, y=200, z=999)
#   Verify p2 is still: Point(x=100, y=200, z=300)
#   Person with default job: Person(name='Jurabek', age=25, job='Unemployed')
#
#   --- Final Test ---
#   Playground Point (typename='nom'): nom(x=1, y=2, z=3)
#   Type of pp: nom
# Why:
#   1. namedtuples are tuples, so they support indexing and unpacking.
#   2. _replace creates a copy because tuples are immutable.
#   3. defaults are applied from right to left.
#   4. The typename (1st arg) determines the __repr__ and type name.
