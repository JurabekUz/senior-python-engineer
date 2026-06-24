"""
TOPIC: Class Attributes vs Instance Attributes
======================================================

WHAT IS IT?
  Python classes have TWO kinds of attributes:
    • CLASS attributes — defined in the class body, shared by ALL instances.
    • INSTANCE attributes — defined on `self`, unique to each object.

  When you read `obj.x`, Python looks up the MRO chain:
    instance.__dict__  →  class.__dict__  →  parent class.__dict__  →  ...

  When you WRITE `obj.x = val`, it ALWAYS creates/updates an instance attribute
  — it NEVER touches the class attribute. This is the #1 source of confusion.

RULES / KEY POINTS:
  1. Class attrs live in `ClassName.__dict__`, instance attrs in `self.__dict__`.
  2. Reading `obj.x` falls back to the class attr if no instance attr exists.
  3. Writing `obj.x = val` ALWAYS creates an instance attr → shadows the class attr.
  4. Mutating a MUTABLE class attr (list, dict) via `obj.x.append()` modifies
     the shared object — it does NOT create an instance attr.
  5. Use `ClassName.x` to explicitly read/write the class attr.
  6. `type(self).x` is the same as `ClassName.x` but works with inheritance.
  7. `@classmethod` and `@staticmethod` relate to class-level behavior.

COMMON PROBLEMS / PITFALLS:
  - Mutable default class attrs (lists, dicts) are shared across ALL instances.
    One instance mutating `self.items.append(x)` affects every other instance.
  - Shadowing: `self.x = val` hides the class attr — the class attr still exists.
  - Using `self.counter += 1` creates an instance attr instead of incrementing
    the shared class counter. Use `ClassName.counter += 1` instead.

WHEN TO USE IT:
  - Class attrs: constants, defaults, counters, caches shared across instances.
  - Instance attrs: per-object state (name, age, config, data).
  - @classmethod: factory methods, alternative constructors.
  - @staticmethod: utility functions that don't need self or cls.

RELATED TOPICS:
  - __dict__
  - property
  - inheritance_mro
  - __getattr__and__setattr__
"""

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept: Class vs Instance
# ─────────────────────────────────────────────

class Dog:
    species = "Canis familiaris"  # CLASS attribute — shared by all dogs
    count = 0                     # CLASS attribute — tracks total dogs

    def __init__(self, name: str, age: int):
        self.name = name  # INSTANCE attribute — unique per dog
        self.age = age    # INSTANCE attribute
        Dog.count += 1    # Modify via ClassName, NOT self

    def info(self) -> str:
        # Reading `self.species` works — falls back to class attr
        return f"{self.name} ({self.species}), age {self.age}"


# ─────────────────────────────────────────────
# SECTION 2 — The Shadowing Trap
# ─────────────────────────────────────────────

class Config:
    """Demonstrates how `self.x = val` shadows the class attribute."""
    debug = False  # Class-level default

    def enable_debug(self):
        # ❌ This creates an INSTANCE attribute, doesn't change the class attr
        self.debug = True

    def enable_debug_globally(self):
        # ✅ This changes the CLASS attribute for everyone
        Config.debug = True


# ─────────────────────────────────────────────
# SECTION 3 — Mutable Class Attr Trap (The Big Gotcha)
# ─────────────────────────────────────────────

class BrokenTaskList:
    """❌ BAD: Mutable class attr shared across all instances."""
    tasks = []  # SHARED list — every instance sees the same list

    def add(self, task: str):
        self.tasks.append(task)  # Mutates the shared list, no shadowing!


class CorrectTaskList:
    """✅ GOOD: Initialize mutable data in __init__."""

    def __init__(self):
        self.tasks = []  # INSTANCE attribute — unique per object

    def add(self, task: str):
        self.tasks.append(task)


# ─────────────────────────────────────────────
# SECTION 4 — __dict__ Inspection
# ─────────────────────────────────────────────

class Point:
    dimensions = 2  # class attr

    def __init__(self, x: float, y: float):
        self.x = x  # instance attr
        self.y = y   # instance attr


# ─────────────────────────────────────────────
# SECTION 5 — @classmethod and @staticmethod
# ─────────────────────────────────────────────

class Employee:
    raise_percent = 1.05  # 5% raise — class-level policy
    _count = 0

    def __init__(self, name: str, salary: float):
        self.name = name
        self.salary = salary
        Employee._count += 1

    def apply_raise(self):
        """Uses class attr for raise percentage."""
        self.salary *= type(self).raise_percent  # type(self) respects inheritance

    @classmethod
    def set_raise_percent(cls, percent: float):
        """@classmethod — receives the CLASS as first arg, not an instance.
        Use for: factory methods, modifying class state."""
        cls.raise_percent = percent

    @classmethod
    def from_string(cls, emp_str: str) -> "Employee":
        """Factory method — alternative constructor."""
        name, salary = emp_str.split("-")
        return cls(name, float(salary))

    @classmethod
    def headcount(cls) -> int:
        return cls._count

    @staticmethod
    def is_valid_salary(salary: float) -> bool:
        """@staticmethod — no self, no cls. Just a namespaced utility.
        Use for: helper functions that logically belong to the class."""
        return salary > 0


# ─────────────────────────────────────────────
# SECTION 6 — Instance Counter (Real-World Pattern)
# ─────────────────────────────────────────────

class Connection:
    """Tracks active connections using a class attribute."""
    _active = 0
    _history = []  # Mutable, but intentionally shared (this is a feature!)

    def __init__(self, host: str):
        self.host = host
        Connection._active += 1
        Connection._history.append(f"OPEN: {host}")

    def close(self):
        Connection._active -= 1
        Connection._history.append(f"CLOSE: {self.host}")

    @classmethod
    def active_count(cls) -> int:
        return cls._active

    @classmethod
    def get_history(cls) -> list:
        return cls._history.copy()


# ─────────────────────────────────────────────
# SECTION 7 — Inheritance and Class Attrs
# ─────────────────────────────────────────────

class Animal:
    sound = "..."

class Cat(Animal):
    sound = "Meow"  # Overrides in Cat's __dict__, Animal.sound unchanged

class Kitten(Cat):
    pass  # Inherits Cat.sound → "Meow"


# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("--- Section 1: Class vs Instance ---")
    d1 = Dog("Rex", 5)
    d2 = Dog("Buddy", 3)
    print(d1.info())
    print(d2.info())
    print(f"Total dogs: {Dog.count}")
    print(f"Same species object? {d1.species is d2.species}")

    print("\n--- Section 2: Shadowing Trap ---")
    c1 = Config()
    c2 = Config()
    c1.enable_debug()  # Only creates instance attr on c1
    print(f"c1.debug = {c1.debug}")  # True (instance attr)
    print(f"c2.debug = {c2.debug}")  # False (still reads class attr)
    print(f"Config.debug = {Config.debug}")  # False (class attr untouched)
    print(f"'debug' in c1.__dict__? {'debug' in c1.__dict__}")  # True
    print(f"'debug' in c2.__dict__? {'debug' in c2.__dict__}")  # False

    print("\n--- Section 3: Mutable Trap ---")
    bad1 = BrokenTaskList()
    bad2 = BrokenTaskList()
    bad1.add("Buy milk")
    print(f"bad1.tasks = {bad1.tasks}")
    print(f"bad2.tasks = {bad2.tasks}")  # ❌ Also has "Buy milk"!
    print(f"Same list? {bad1.tasks is bad2.tasks}")

    good1 = CorrectTaskList()
    good2 = CorrectTaskList()
    good1.add("Buy milk")
    print(f"good1.tasks = {good1.tasks}")
    print(f"good2.tasks = {good2.tasks}")  # ✅ Empty
    print(f"Same list? {good1.tasks is good2.tasks}")

    print("\n--- Section 4: __dict__ Inspection ---")
    p = Point(3, 4)
    print(f"Instance __dict__: {p.__dict__}")
    print(f"Class __dict__ keys: {[k for k in Point.__dict__ if not k.startswith('_')]}")
    print(f"'dimensions' in instance? {'dimensions' in p.__dict__}")
    print(f"p.dimensions = {p.dimensions}")  # Falls back to class

    print("\n--- Section 5: classmethod & staticmethod ---")
    e1 = Employee("Alice", 100_000)
    e2 = Employee.from_string("Bob-80000")  # Factory method
    print(f"{e1.name}: ${e1.salary:,.0f}")
    print(f"{e2.name}: ${e2.salary:,.0f}")
    print(f"Headcount: {Employee.headcount()}")

    Employee.set_raise_percent(1.10)  # 10% raise for everyone
    e1.apply_raise()
    print(f"{e1.name} after raise: ${e1.salary:,.0f}")
    print(f"Valid salary? {Employee.is_valid_salary(50000)}")
    print(f"Valid salary? {Employee.is_valid_salary(-100)}")

    print("\n--- Section 6: Connection Counter ---")
    conn1 = Connection("db-server-1")
    conn2 = Connection("db-server-2")
    print(f"Active: {Connection.active_count()}")
    conn1.close()
    print(f"Active after close: {Connection.active_count()}")
    print(f"History: {Connection.get_history()}")

    print("\n--- Section 7: Inheritance ---")
    print(f"Animal.sound = '{Animal.sound}'")
    print(f"Cat.sound = '{Cat.sound}'")
    print(f"Kitten.sound = '{Kitten.sound}'")
    print(f"'sound' in Kitten.__dict__? {'sound' in Kitten.__dict__}")

# Output:
#   --- Section 1: Class vs Instance ---
#   Rex (Canis familiaris), age 5
#   Buddy (Canis familiaris), age 3
#   Total dogs: 2
#   Same species object? True
#
#   --- Section 2: Shadowing Trap ---
#   c1.debug = True
#   c2.debug = False
#   Config.debug = False
#   'debug' in c1.__dict__? True
#   'debug' in c2.__dict__? False
#
#   --- Section 3: Mutable Trap ---
#   bad1.tasks = ['Buy milk']
#   bad2.tasks = ['Buy milk']
#   Same list? True
#   good1.tasks = ['Buy milk']
#   good2.tasks = []
#   Same list? False
#
#   --- Section 4: __dict__ Inspection ---
#   Instance __dict__: {'x': 3, 'y': 4}
#   Class __dict__ keys: ['dimensions']
#   'dimensions' in instance? False
#   p.dimensions = 2
#
#   --- Section 5: classmethod & staticmethod ---
#   Alice: $100,000
#   Bob: $80,000
#   Headcount: 2
#   Alice after raise: $110,000
#   Valid salary? True
#   Valid salary? False
#
#   --- Section 6: Connection Counter ---
#   Active: 2
#   Active after close: 1
#   History: ['OPEN: db-server-1', 'OPEN: db-server-2', 'CLOSE: db-server-1']
#
#   --- Section 7: Inheritance ---
#   Animal.sound = '...'
#   Cat.sound = 'Meow'
#   Kitten.sound = 'Meow'
#   'sound' in Kitten.__dict__? False
# Why:
#   1. Class attrs are shared — `d1.species is d2.species` is True (same object).
#   2. `self.debug = True` creates an instance attr that shadows the class attr.
#      c2 never got an instance attr, so it still reads from Config.debug (False).
#   3. Mutable class attrs (lists) are THE classic Python OOP bug.
#      `self.tasks.append()` mutates in-place — no new instance attr is created.
#   4. `p.__dict__` only has instance attrs. `dimensions` lives in Point.__dict__.
#   5. @classmethod gets `cls` → can create instances, modify class state.
#      @staticmethod gets nothing → pure utility, just namespaced under the class.
#   6. `_active` and `_history` are intentionally class-level — tracking global state.
#   7. Kitten inherits `sound` from Cat. `'sound' in Kitten.__dict__` is False
#      because it's found in Cat.__dict__ via MRO lookup.
