"""
TOPIC: Inheritance & MRO (Method Resolution Order)
======================================================

WHAT IS IT?
  Inheritance lets a child class reuse and extend the behavior of a parent class.
  MRO is the ORDER in which Python searches for methods when you call one.
  Python uses the C3 Linearization algorithm to compute a deterministic,
  monotonic MRO — you can inspect it with `ClassName.__mro__` or `ClassName.mro()`.

RULES / KEY POINTS:
  1. Single inheritance: Child → Parent → object.
  2. Multiple inheritance: Python resolves via C3 Linearization (left-to-right,
     depth-first, but skips classes already visited).
  3. `super()` follows the MRO — it does NOT always call the direct parent.
     In a diamond, `super()` calls the NEXT class in the MRO chain.
  4. `isinstance(obj, cls)` checks the entire MRO (including parents).
  5. `issubclass(A, B)` checks if B appears anywhere in A's MRO.
  6. Every class eventually inherits from `object` — it's always last in MRO.
  7. `super().__init__()` must be called to ensure parent initialization runs.

COMMON PROBLEMS / PITFALLS:
  - Forgetting `super().__init__()` → parent state is never initialized.
  - In multiple inheritance, `super()` doesn't go to "the parent" — it goes
    to the NEXT class in MRO. This surprises people from Java/C++.
  - Inconsistent MRO → Python raises TypeError at class definition time
    if C3 linearization cannot find a valid order.
  - Method shadowing: a child method hides the parent method completely;
    use `super().method()` to extend rather than replace.

WHEN TO USE IT:
  - Code reuse: factor common logic into a base class.
  - Polymorphism: treat different subclasses through a common interface.
  - Framework extension: override specific hooks (e.g., Django views).
  - Mixins: small, focused classes that add behavior via multiple inheritance.

RELATED TOPICS:
  - diamond_problem (next topic — deep-dive into diamond shape)
  - abc_abstract
  - class_attributes
  - duck_typing
"""

# ─────────────────────────────────────────────
# SECTION 1 — Basic Single Inheritance
# ─────────────────────────────────────────────

class Vehicle:
    def __init__(self, brand: str, year: int):
        self.brand = brand
        self.year = year

    def start(self) -> str:
        return f"{self.brand} engine started"

    def info(self) -> str:
        return f"{self.brand} ({self.year})"


class Car(Vehicle):
    def __init__(self, brand: str, year: int, doors: int):
        super().__init__(brand, year)  # ← Calls Vehicle.__init__
        self.doors = doors

    def info(self) -> str:
        # EXTEND parent method, don't replace
        return f"{super().info()}, {self.doors} doors"


class ElectricCar(Car):
    def __init__(self, brand: str, year: int, doors: int, battery_kwh: float):
        super().__init__(brand, year, doors)
        self.battery_kwh = battery_kwh

    def start(self) -> str:
        # OVERRIDE completely — no engine sound
        return f"{self.brand} silently powers on ({self.battery_kwh} kWh)"

    def info(self) -> str:
        return f"{super().info()}, {self.battery_kwh} kWh battery"


# MRO: ElectricCar → Car → Vehicle → object


# ─────────────────────────────────────────────
# SECTION 2 — MRO Inspection
# ─────────────────────────────────────────────

def show_mro(cls):
    """Helper to display MRO in a readable format."""
    names = [c.__name__ for c in cls.__mro__]
    return " → ".join(names)


# ─────────────────────────────────────────────
# SECTION 3 — Multiple Inheritance & Mixins
# ─────────────────────────────────────────────

class LoggerMixin:
    """Mixin: adds logging capability. No __init__ needed."""
    def log(self, message: str):
        print(f"  [LOG {type(self).__name__}] {message}")


class SerializerMixin:
    """Mixin: adds JSON serialization."""
    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}


class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def greet(self) -> str:
        return f"Hello, I'm {self.name}"


class AdminUser(LoggerMixin, SerializerMixin, User):
    """Multiple inheritance: AdminUser gets logging, serialization, AND user behavior."""
    def __init__(self, name: str, email: str, level: int):
        super().__init__(name, email)  # Follows MRO → calls User.__init__
        self.level = level

    def promote(self):
        self.level += 1
        self.log(f"Promoted to level {self.level}")  # From LoggerMixin

# MRO: AdminUser → LoggerMixin → SerializerMixin → User → object


# ─────────────────────────────────────────────
# SECTION 4 — super() Follows MRO, Not Parent
# ─────────────────────────────────────────────

class A:
    def who(self):
        print("  A.who() called — next in MRO after A")

class B(A):
    def who(self):
        print("  B.who() called")
        super().who()  # Goes to NEXT in MRO, not necessarily A

class C(A):
    def who(self):
        print("  C.who() called")
        super().who()  # Goes to NEXT in MRO

class D(B, C):
    def who(self):
        print("  D.who() called")
        super().who()  # Goes to B (next in MRO)

# MRO: D → B → C → A → object
# So D.who() → B.who() → C.who() → A.who()
# Notice: B.super() goes to C, NOT to A! Because C is next in D's MRO.


# ─────────────────────────────────────────────
# SECTION 5 — isinstance & issubclass
# ─────────────────────────────────────────────

# isinstance checks the entire inheritance chain
# issubclass checks if one class is in another's MRO


# ─────────────────────────────────────────────
# SECTION 6 — Cooperative Multiple Inheritance (__init__ chain)
# ─────────────────────────────────────────────

class Base:
    def __init__(self, **kwargs):
        # Catch-all: absorb remaining kwargs so the chain doesn't break
        print(f"  Base.__init__(kwargs={kwargs})")
        super().__init__()  # Ends at object.__init__()

class Left(Base):
    def __init__(self, left_val, **kwargs):
        print(f"  Left.__init__(left_val={left_val})")
        self.left_val = left_val
        super().__init__(**kwargs)  # Pass remaining kwargs down the MRO

class Right(Base):
    def __init__(self, right_val, **kwargs):
        print(f"  Right.__init__(right_val={right_val})")
        self.right_val = right_val
        super().__init__(**kwargs)

class Bottom(Left, Right):
    def __init__(self, left_val, right_val, bottom_val):
        print(f"  Bottom.__init__(bottom_val={bottom_val})")
        self.bottom_val = bottom_val
        super().__init__(left_val=left_val, right_val=right_val)

# MRO: Bottom → Left → Right → Base → object
# __init__ chain: Bottom → Left → Right → Base → object
# Each class takes what it needs from kwargs, passes the rest along.


# ─────────────────────────────────────────────
# SECTION 7 — Invalid MRO (TypeError)
# ─────────────────────────────────────────────

# Uncommenting this would raise TypeError at class definition time:
#
# class X: pass
# class Y(X): pass
# class Z(X, Y): pass  # ← TypeError: Cannot create a consistent MRO
#
# Why? C3 requires that X comes before Y (from Z(X, Y) left-to-right),
# but Y inherits from X, so X must come AFTER Y. Contradiction → error.


# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("--- Section 1: Single Inheritance ---")
    tesla = ElectricCar("Tesla", 2024, 4, 75.0)
    print(tesla.info())
    print(tesla.start())

    print("\n--- Section 2: MRO Inspection ---")
    print(f"ElectricCar MRO: {show_mro(ElectricCar)}")
    print(f"AdminUser MRO:   {show_mro(AdminUser)}")
    print(f"D MRO:           {show_mro(D)}")

    print("\n--- Section 3: Multiple Inheritance & Mixins ---")
    admin = AdminUser("Jurabek", "jurabek@mail.com", 1)
    print(admin.greet())          # From User
    print(admin.to_dict())        # From SerializerMixin
    admin.promote()               # Uses LoggerMixin.log()

    print("\n--- Section 4: super() Follows MRO ---")
    print("Calling D().who():")
    D().who()
    # Notice the chain: D → B → C → A (not D → B → A!)

    print("\n--- Section 5: isinstance & issubclass ---")
    print(f"isinstance(tesla, Car)?       {isinstance(tesla, Car)}")
    print(f"isinstance(tesla, Vehicle)?   {isinstance(tesla, Vehicle)}")
    print(f"isinstance(tesla, object)?    {isinstance(tesla, object)}")
    print(f"issubclass(ElectricCar, Car)?     {issubclass(ElectricCar, Car)}")
    print(f"issubclass(ElectricCar, Vehicle)? {issubclass(ElectricCar, Vehicle)}")
    print(f"issubclass(Car, ElectricCar)?     {issubclass(Car, ElectricCar)}")

    print("\n--- Section 6: Cooperative __init__ Chain ---")
    print("Creating Bottom(left_val=10, right_val=20, bottom_val=30):")
    b = Bottom(left_val=10, right_val=20, bottom_val=30)
    print(f"Result: left={b.left_val}, right={b.right_val}, bottom={b.bottom_val}")

    print("\n--- Section 7: Invalid MRO ---")
    try:
        # Dynamically create the invalid hierarchy to show the error
        X = type("X", (), {})
        Y = type("Y", (X,), {})
        Z = type("Z", (X, Y), {})  # ← Will fail
    except TypeError as e:
        print(f"TypeError: {e}")

# Output:
#   --- Section 1: Single Inheritance ---
#   Tesla (2024), 4 doors, 75.0 kWh battery
#   Tesla silently powers on (75.0 kWh)
#
#   --- Section 2: MRO Inspection ---
#   ElectricCar MRO: ElectricCar → Car → Vehicle → object
#   AdminUser MRO:   AdminUser → LoggerMixin → SerializerMixin → User → object
#   D MRO:           D → B → C → A → object
#
#   --- Section 3: Multiple Inheritance & Mixins ---
#   Hello, I'm Jurabek
#   {'name': 'Jurabek', 'email': 'jurabek@mail.com', 'level': 1}
#   [LOG AdminUser] Promoted to level 2
#
#   --- Section 4: super() Follows MRO ---
#   Calling D().who():
#     D.who() called
#     B.who() called
#     C.who() called
#     A.who() called — next in MRO after A
#
#   --- Section 5: isinstance & issubclass ---
#   isinstance(tesla, Car)?       True
#   isinstance(tesla, Vehicle)?   True
#   isinstance(tesla, object)?    True
#   issubclass(ElectricCar, Car)?     True
#   issubclass(ElectricCar, Vehicle)? True
#   issubclass(Car, ElectricCar)?     False
#
#   --- Section 6: Cooperative __init__ Chain ---
#   Creating Bottom(left_val=10, right_val=20, bottom_val=30):
#     Bottom.__init__(bottom_val=30)
#     Left.__init__(left_val=10)
#     Right.__init__(right_val=20)
#     Base.__init__(kwargs={})
#   Result: left=10, right=20, bottom=30
#
#   --- Section 7: Invalid MRO ---
#   TypeError: Cannot create a consistent method resolution order (MRO)...
# Why:
#   1. Single inheritance MRO is simple: child → parent → grandparent → object.
#   2. In multiple inheritance, C3 linearization goes left-to-right, depth-first,
#      but never visits a class before all its subclasses are visited.
#   3. super() follows the MRO of the ACTUAL object's class, not the class
#      where super() is written. So B.super() in a D instance goes to C, not A.
#   4. Cooperative __init__ uses **kwargs to pass unrecognized args down the chain.
#      Each class takes what it needs and forwards the rest.
#   5. Invalid MRO happens when C3 finds contradictory ordering requirements.
