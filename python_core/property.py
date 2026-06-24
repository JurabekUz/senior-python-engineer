"""
TOPIC: @property — Managed Attributes
======================================================

WHAT IS IT?
  `@property` turns a method into a "getter" so you can access it like an
  attribute (no parentheses). Combined with `@name.setter` and `@name.deleter`,
  it gives you full control over reading, writing, and deleting an attribute —
  while the outside world still uses simple `obj.name` syntax.

  Under the hood, `property` is a DESCRIPTOR — an object that implements
  `__get__`, `__set__`, and/or `__delete__`.

RULES / KEY POINTS:
  1. `@property` defines the GETTER — `obj.x` calls this method.
  2. `@x.setter` defines the SETTER — `obj.x = val` calls this method.
  3. `@x.deleter` defines the DELETER — `del obj.x` calls this method.
  4. Without a setter, the property is READ-ONLY → assignment raises AttributeError.
  5. The backing attribute is conventionally prefixed with `_` (e.g., `self._name`).
  6. `property()` can also be used as a plain function: `x = property(get, set, del, doc)`.

COMMON PROBLEMS / PITFALLS:
  - Infinite recursion: using `self.name` inside the getter for `name` instead
    of `self._name` → calls itself forever → RecursionError.
  - Forgetting @setter: the property becomes read-only, and assignment silently
    raises AttributeError — confusing if unintended.
  - In `__init__`, `self.name = value` triggers the SETTER if a property named
    `name` exists — this is a feature (validation on init), not a bug.
  - Decorator order: `@property` must come FIRST, then `@name.setter`.

WHEN TO USE IT:
  - Input validation (type checking, range clamping, format enforcement).
  - Computed / derived attributes (e.g., `full_name` from first + last).
  - Lazy loading / caching expensive computations.
  - Migrating from public attributes to managed ones WITHOUT breaking API.
  - Read-only attributes that should never be set from outside.

RELATED TOPICS:
  - abc_abstract (abstract properties)
  - __getattr__and__setattr__
  - descriptors (the protocol behind property)
  - dataclasses (field validation via __post_init__)
"""

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept: Getter + Setter + Deleter
# ─────────────────────────────────────────────

class User:
    """Demonstrates the full property lifecycle: get, set, delete."""

    def __init__(self, name: str, age: int):
        # These assignments go through the SETTERS below!
        self.name = name
        self.age = age

    @property
    def name(self) -> str:
        """Getter — called when you read `user.name`."""
        return self._name

    @name.setter
    def name(self, value: str):
        """Setter — called when you write `user.name = 'Alice'`."""
        if not isinstance(value, str):
            raise TypeError(f"Name must be str, got {type(value).__name__}")
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()

    @name.deleter
    def name(self):
        """Deleter — called when you do `del user.name`."""
        print(f"Deleting name '{self._name}'")
        self._name = "DELETED"

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f"Age must be int, got {type(value).__name__}")
        if value < 0 or value > 150:
            raise ValueError(f"Age must be 0-150, got {value}")
        self._age = value


# ─────────────────────────────────────────────
# SECTION 2 — Computed / Derived Properties
# ─────────────────────────────────────────────

class Rectangle:
    """Properties that compute values from other attributes."""

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    @property
    def area(self) -> float:
        """Read-only — no setter defined."""
        return self._width * self._height

    @property
    def perimeter(self) -> float:
        return 2 * (self._width + self._height)

    @property
    def is_square(self) -> bool:
        return self._width == self._height

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float):
        if value <= 0:
            raise ValueError("Width must be positive")
        self._width = value

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float):
        if value <= 0:
            raise ValueError("Height must be positive")
        self._height = value


# ─────────────────────────────────────────────
# SECTION 3 — Read-Only Properties
# ─────────────────────────────────────────────

class DatabaseRecord:
    """Once created, `record_id` can never be changed."""

    def __init__(self, record_id: int, data: str):
        self._record_id = record_id  # Direct assignment — bypasses property
        self.data = data

    @property
    def record_id(self) -> int:
        """No setter → read-only. Assignment raises AttributeError."""
        return self._record_id

    @property
    def data(self) -> str:
        return self._data

    @data.setter
    def data(self, value: str):
        self._data = value


# ─────────────────────────────────────────────
# SECTION 4 — Cached / Lazy Property
# ─────────────────────────────────────────────

import time

class ExpensiveResource:
    """Demonstrates lazy loading — compute once, cache the result."""

    def __init__(self, name: str):
        self.name = name
        self._report = None  # Cache slot

    @property
    def report(self) -> str:
        """Computed on first access, cached for subsequent calls."""
        if self._report is None:
            print(f"  ⏳ Computing report for '{self.name}'... (slow)")
            time.sleep(0.1)  # Simulate expensive work
            self._report = f"Report<{self.name}: 42 items, all OK>"
        return self._report

    def invalidate_cache(self):
        """Force recomputation on next access."""
        self._report = None


# ─────────────────────────────────────────────
# SECTION 5 — property() as a Function (Old Style)
# ─────────────────────────────────────────────

class Temperature:
    """Shows that @property is just syntactic sugar for property()."""

    def __init__(self, celsius: float):
        self._celsius = celsius

    def _get_fahrenheit(self) -> float:
        return self._celsius * 9 / 5 + 32

    def _set_fahrenheit(self, value: float):
        self._celsius = (value - 32) * 5 / 9

    # Equivalent to @property + @setter, just using the function form
    fahrenheit = property(
        fget=_get_fahrenheit,
        fset=_set_fahrenheit,
        doc="Temperature in Fahrenheit"
    )

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float):
        self._celsius = value


# ─────────────────────────────────────────────
# SECTION 6 — The Infinite Recursion Trap
# ─────────────────────────────────────────────

class BadExample:
    """DO NOT DO THIS — included to show the classic mistake."""

    @property
    def value(self):
        # ❌ WRONG: `self.value` calls THIS getter again → infinite loop
        # return self.value  # Would cause RecursionError
        # ✅ CORRECT: use the backing attribute
        return self._value

    @value.setter
    def value(self, val):
        self._value = val


# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("--- Section 1: Getter + Setter + Deleter ---")
    user = User("  Jurabek  ", 25)
    print(f"Name: '{user.name}'")  # Stripped by setter
    print(f"Age: {user.age}")

    try:
        user.name = ""
    except ValueError as e:
        print(f"Validation: {e}")

    try:
        user.age = 200
    except ValueError as e:
        print(f"Validation: {e}")

    del user.name
    print(f"After delete: '{user.name}'")

    print("\n--- Section 2: Computed Properties ---")
    rect = Rectangle(5, 3)
    print(f"Area: {rect.area}")
    print(f"Perimeter: {rect.perimeter}")
    print(f"Is square: {rect.is_square}")
    rect.width = 3
    print(f"After resize → Is square: {rect.is_square}")

    try:
        rect.area = 100  # No setter → read-only
    except AttributeError as e:
        print(f"Read-only: {e}")

    print("\n--- Section 3: Read-Only ---")
    record = DatabaseRecord(42, "important stuff")
    print(f"ID: {record.record_id}")
    try:
        record.record_id = 99
    except AttributeError as e:
        print(f"Cannot set: {e}")

    print("\n--- Section 4: Cached Property ---")
    res = ExpensiveResource("Sales")
    print("First access:")
    print(f"  {res.report}")
    print("Second access (cached):")
    print(f"  {res.report}")
    res.invalidate_cache()
    print("After invalidation:")
    print(f"  {res.report}")

    print("\n--- Section 5: property() Function ---")
    temp = Temperature(100)
    print(f"{temp.celsius}°C = {temp.fahrenheit}°F")
    temp.fahrenheit = 32
    print(f"{temp.fahrenheit}°F = {temp.celsius}°C")

# Output:
#   --- Section 1: Getter + Setter + Deleter ---
#   Name: 'Jurabek'
#   Age: 25
#   Validation: Name cannot be empty
#   Validation: Age must be 0-150, got 200
#   Deleting name 'Jurabek'
#   After delete: 'DELETED'
#
#   --- Section 2: Computed Properties ---
#   Area: 15
#   Perimeter: 16
#   Is square: False
#   After resize → Is square: True
#   Read-only: property 'area' of 'Rectangle' object has no setter
#
#   --- Section 3: Read-Only ---
#   ID: 42
#   Cannot set: property 'record_id' of 'DatabaseRecord' object has no setter
#
#   --- Section 4: Cached Property ---
#   First access:
#     ⏳ Computing report for 'Sales'... (slow)
#     Report<Sales: 42 items, all OK>
#   Second access (cached):
#     Report<Sales: 42 items, all OK>
#   After invalidation:
#     ⏳ Computing report for 'Sales'... (slow)
#     Report<Sales: 42 items, all OK>
#
#   --- Section 5: property() Function ---
#   100°C = 212.0°F
#   32°F = 0.0°C
# Why:
#   1. `self.name = "  Jurabek  "` in __init__ triggers the setter → strips whitespace.
#   2. Validation fires on both init and reassignment — properties guard invariants.
#   3. `del user.name` triggers the deleter — we set it to "DELETED" instead of removing.
#   4. `area` has no setter → assigning to it raises AttributeError (read-only).
#   5. Cached property computes only once; ⏳ only prints on first access (and after invalidation).
#   6. `property(fget, fset)` is the non-decorator equivalent of @property + @setter.
