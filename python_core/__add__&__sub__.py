"""
TOPIC: Magic Methods - __add__ & __sub__ (and the dir() Function)
==================================================================

WHAT IS IT?
  - `__add__` and `__sub__` are magic (dunder) methods in Python that define how
    objects of a custom class behave when used with the addition (+) and
    subtraction (-) operators.
  - Python's built-in `dir()` function returns a list (directory) of all valid
    attributes and methods of an object.

RULES / KEY POINTS:
  1. No Automatic Arithmetic: Arithmetic magic methods like `__add__`, `__sub__`
     are NOT defined automatically in user-defined classes.
  2. Implicit object Inheritance: Every custom class implicitly inherits from the
     base `object` class. This base class provides default implementations for
     essential lifecycle/introspection methods (like `__init__`, `__dict__`, and `__dir__`).
  3. dir() Abbreviation: The name `dir` stands for "directory". It serves as an
     index/catalog listing all attributes and methods of an object.
  4. Type Consistency: Typically, operators like `__add__` should return a new
     instance of the class rather than mutating the existing ones.
  5. In-place Operators: `__iadd__` (+=) and `__isub__` (-=) are used for in-place
     mutations and should return `self`.

COMMON PROBLEMS / PITFALLS:
  - Pitfall 1: Attempting arithmetic operations on a class without defining its
    respective magic method results in: `TypeError: unsupported operand type(s)`.
  - Pitfall 2: Forgetting to return `self` from in-place magic methods like
    `__iadd__` or `__isub__`. If you do not return `self`, the object becomes `None`
    after the assignment (e.g., `x += y` makes `x` become `None`).

WHEN TO USE IT:
  - Use mathematical magic methods when building classes that represent numerical,
    geometric, or physical quantities (e.g., Vectors, Points, Complex Numbers, Matrices).

RELATED TOPICS:
  - `__mul__`, `__truediv__`, `__floordiv__`
  - `__dict__` and `__dir__`
  - Base `object` class and inheritance
"""

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept (Implicit Inheritance & dir())
# ─────────────────────────────────────────────

# In this section, we examine a simple class without custom mathematical operators.
# We will see that standard methods exist via the base 'object' class, but adding
# two instances together fails with a TypeError.

class Range:
    def __init__(self, min_value: int, max_value: int):
        self.min_value: int = min_value
        self.max_value: int = max_value

# Instantiate Range objects
range_obj1 = Range(1, 10)
range_obj2 = Range(11, 20)

# 1. Introspection via __dict__ (Inherited from base 'object')
print("Range object dict:", range_obj1.__dict__)

# 2. Introspection via dir() (Stands for "directory", inherited from base 'object')
print("All dir() attributes of Range:", dir(range_obj1))

# 3. Attempting addition (+) will raise a TypeError because __add__ is not defined
try:
    result = range_obj1 + range_obj2
except TypeError as e:
    print(f"Expected Error: {e}")


# ─────────────────────────────────────────────
# SECTION 2 — Advanced / Real-World Usage (Implementing Point Arithmetic)
# ─────────────────────────────────────────────

# Here, we explicitly implement __add__, __sub__, __iadd__, and __isub__
# to enable seamless arithmetic operations for our custom Point objects.

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"<Point x:{self.x},y:{self.y}>"

    # Addition (+): Returns a NEW Point instance
    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    # Subtraction (-): Returns a NEW Point instance
    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    # In-place Addition (+=): Mutates the current instance and returns self
    def __iadd__(self, other: "Point") -> "Point":
        self.x += other.x
        self.y += other.y
        return self

    # In-place Subtraction (-=): Mutates the current instance and returns self
    def __isub__(self, other: "Point") -> "Point":
        self.x -= other.x
        self.y -= other.y
        return self


def main():
    print("\n--- Point Arithmetic Test ---")
    p1 = Point(10, 20)
    p2 = Point(30, 30)
    print(f"Initial Points: p1 = {p1}, p2 = {p2}")

    # Standard Addition
    p3 = p1 + p2
    print(f"p1 + p2 = {p3}")

    # Standard Subtraction
    p4 = p2 - p1
    print(f"p2 - p1 = {p4}")

    # In-place Addition
    p1 += p2
    print(f"After p1 += p2: p1 = {p1}")


# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == "__main__":
    main()

# Expected Output:
# Range object dict: {'min_value': 1, 'max_value': 10}
# All dir() attributes of Range: ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'max_value', 'min_value']
# Expected Error: unsupported operand type(s) for +: 'Range' and 'Range'
#
# --- Point Arithmetic Test ---
# Initial Points: p1 = <Point x:10,y:20>, p2 = <Point x:30,y:30>
# p1 + p2 = <Point x:40,y:50>
# p2 - p1 = <Point x:20,y:10>
# After p1 += p2: p1 = <Point x:40,y:50>
#
# Why: 
#   1. The 'Range' class doesn't define '__add__', so adding instances causes a TypeError.
#   2. The standard dunder methods (like '__dict__' and '__dir__') are inherited from 'object' by default.
#   3. 'dir' stands for "directory" because it catalogues the names of the attributes/methods.
#   4. The 'Point' class defines custom '__add__', '__sub__', and '__iadd__' methods, allowing it to seamlessly handle + and += operations.
