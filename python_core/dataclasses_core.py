"""
TOPIC: Dataclasses
======================================================

WHAT IS IT?
  Introduced in Python 3.7, @dataclass is a decorator that 
  automatically generates dunder methods like __init__, __repr__, 
  and __eq__ for classes that primarily store data.

RULES / KEY POINTS:
  1. Fields MUST have type annotations. Without annotations, 
     they are ignored by the dataclass decorator.
  2. Fields with default values must come AFTER fields without 
     default values (just like function arguments).
  3. Use field() for advanced configuration (default_factory, repr=False, etc.).
  4. ClassVar: Used for class-level attributes that shouldn't be 
     treated as instance fields.
  5. InitVar: Fields used only for __init__ and __post_init__, 
     but not stored as instance attributes.

COMMON PROBLEMS / PITFALLS:
  - Pitfall 1: Using mutable defaults like [] or {}.
      → Solution: Use field(default_factory=list).
  - Pitfall 2: Forgetting type hints.
      → Dataclasses skip any attribute that doesn't have a type hint.
  - Pitfall 3: Comparison logic with floats.
      → Dataclasses generate __eq__ by default; be careful comparing float fields.

WHEN TO USE IT:
  - Creating "Data Transfer Objects" (DTOs).
  - Representing database records or API responses.
  - Any class whose main purpose is state rather than behavior.

RELATED TOPICS:
  - NamedTuple
  - Typing hints
  - __init__, __repr__, __eq__
"""

from dataclasses import dataclass, field, InitVar
from typing import ClassVar

# ─────────────────────────────────────────────
# SECTION 1 — Simple Dataclass & Default Values
# ─────────────────────────────────────────────

@dataclass
class User:
    # Simple fields (automatically added to __init__)
    user_id: int
    username: str
    
    # Default value (must come after non-default fields)
    is_active: bool = True
    
    # Mutable default (WRONG: roles: list = [])
    # Correct way: use default_factory to get a fresh list for every instance
    roles: list[str] = field(default_factory=list)

u1 = User(1, "alice")
u2 = User(1, "alice")
u3 = User(2, "bob", roles=["admin"])

print(u1)             # Auto-generated __repr__
print(u1 == u2)       # Auto-generated __eq__ (True based on values)
print(u3.roles)       # ['admin']

# Output:
#   User(user_id=1, username='alice', is_active=True, roles=[])
#   True
#   ['admin']
# Why: Dataclasses generate a readable repr and field-by-field equality check.


# ─────────────────────────────────────────────
# SECTION 2 — ClassVar & InitVar
# ─────────────────────────────────────────────

@dataclass
class Book:
    title: str
    author: str
    
    # ClassVar: Not an instance field, shared by all instances.
    # It is excluded from __init__ and __repr__.
    library_name: ClassVar[str] = "City Central Library"
    
    # InitVar: Passed to __init__ but not stored on the instance.
    # Useful for data needed ONLY during construction (like a config or password).
    discount_code: InitVar[str | None] = None
    price: float = 100.0

    def __post_init__(self, discount_code: str | None):
        """
        Called automatically AFTER __init__.
        It receives any InitVar arguments defined in the class.
        """
        if discount_code == "SAVE10":
            self.price *= 0.9

b1 = Book("Python 101", "Guido", discount_code="SAVE10")
print(f"Price: {b1.price}")
print(f"Library: {b1.library_name}")

# Checking if discount_code is in the instance dictionary
if "discount_code" not in b1.__dict__:
    print("discount_code is NOT in __dict__ (InitVar worked)")
else:
    print("discount_code is in __dict__ (Unexpected!)")

# Output:
#   Price: 90.0
#   Library: City Central Library
#   discount_code is NOT in __dict__ (InitVar worked)
# Why: ClassVar belongs to the class. InitVar is only a parameter for __init__ and __post_init__.


# ─────────────────────────────────────────────
# SECTION 3 — Inheritance & Ordering
# ─────────────────────────────────────────────

@dataclass(order=True)
class Person:
    # order=True generates comparison methods: __lt__, __le__, __gt__, __ge__
    # Comparison is done field-by-field in the order they are defined.
    age: int
    name: str = field(compare=False) # Exclude name from comparison logic

@dataclass(order=True)
class Employee(Person):
    # Inheritance: Employee fields come AFTER Person fields in the generated __init__.
    # Resulting order: (age, name, salary)
    salary: int = 50000

e1 = Employee(age=30, name="Alice", salary=60000)
e2 = Employee(age=25, name="Bob", salary=70000)

# Comparing e1 > e2?
# It first compares 'age'. Since 30 > 25, it returns True immediately.
print(f"e1 > e2? {e1 > e2}") 

# Output:
#   e1 > e2? True
# Why: age is defined first and included in comparison. name is ignored.


# ─────────────────────────────────────────────
# TESTS — Verification
# ─────────────────────────────────────────────

print("\n" + "=" * 50)
print("TESTS")
print("=" * 50)

# Test 1: Immutability (frozen=True)
@dataclass(frozen=True)
class Point:
    x: int
    y: int

p = Point(10, 20)
try:
    p.x = 30
except Exception as e:
    print(f"Test 1 PASSED — frozen works: {type(e).__name__}")

# Test 2: Post Init Validation
@dataclass
class ValidatedUser:
    name: str
    def __post_init__(self):
        if not self.name:
            raise ValueError("Name cannot be empty")

try:
    ValidatedUser("")
except ValueError:
    print("Test 2 PASSED — __post_init__ validation works")

# Test 3: Inheritance field order
# Expected __init__ signature: (priority, name, salary)
@dataclass
class Manager(Employee):
    department: str = "IT"

m = Manager(40, "John", 80000, "HR")
print(f"Test 3 PASSED — Manager: {m.name} in {m.department}")
