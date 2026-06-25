"""
TOPIC: Function and Method Overloading
======================================================

WHAT IS IT?
  In statically typed languages (like Java or C++), you can define multiple 
  functions with the same name but different signatures (parameter types or counts).
  In Python, you CANNOT do this natively because the last defined function with 
  a given name simply overwrites any previous definitions.

  However, Python supports overloading patterns through:
    1. Default arguments (`arg=None`) and type checks (`isinstance()`).
    2. `functools.singledispatch` (for function overloading based on the type of the first argument).
    3. `typing.overload` (for static type checker hint definitions only, has no runtime effect).
    4. Third-party libraries like `multipledispatch` (for actual runtime dispatch based on multiple arguments).

RULES / KEY POINTS:
  1. Default Arguments: The most common Pythonic way to handle varying inputs.
  2. `singledispatch`: Transforms a function into a generic function that dispatches
     to type-specific implementations based on the type of the first argument.
  3. `typing.overload`: Used solely for IDE/static type checking assistance. The actual 
     runtime implementation must follow the overloaded signatures and is decorated without `@overload`.
  4. Method Dispatching: For class methods, use `functools.singledispatchmethod`.

COMMON PROBLEMS / PITFALLS:
  - Overwriting functions: Defining `def foo(a)` and then `def foo(a, b)` in the same scope 
    causes the first `foo` to be completely lost.
  - `@typing.overload` at runtime: Forgetting to provide a final non-decorated implementation 
    leads to runtime errors because `@overload` definitions are overridden and do not execute.
  - Type checking overhead: Excessive `isinstance()` checks inside a function can hurt readability 
    and performance.

WHEN TO USE IT:
  - To implement clean APIs that can accept different formats of input (e.g., a database query
    that takes either an `int` ID or a `str` name).
  - To support typing support (mypy) for functions with complex parameter options.

RELATED TOPICS:
  - typing_hints
  - everything_is_object
"""

from functools import singledispatch, singledispatchmethod
from typing import overload, Union

# ─────────────────────────────────────────────
# SECTION 1 — The Classic Pythonic Way (Default Args & Type Checking)
# ─────────────────────────────────────────────

class AreaCalculator:
    def calculate_area(self, radius_or_length: float, width: float = None) -> float:
        """Calculates area. If width is provided, it's a rectangle; otherwise, a circle."""
        if width is None:
            import math
            return math.pi * (radius_or_length ** 2)
        return radius_or_length * width


# ─────────────────────────────────────────────
# SECTION 2 — singledispatch (Functions)
# ─────────────────────────────────────────────

@singledispatch
def format_data(data) -> str:
    """Fallback implementation when no matching type registered."""
    return f"Default representation: {str(data)}"


@format_data.register(str)
def _(data: str) -> str:
    return f"String: '{data}'"


@format_data.register(list)
def _(data: list) -> str:
    items = ", ".join(format_data(item) for item in data)
    return f"List: [{items}]"


@format_data.register(int)
@format_data.register(float)
def _(data: Union[int, float]) -> str:
    return f"Number: {data:.2f}"


# ─────────────────────────────────────────────
# SECTION 3 — singledispatchmethod (Classes)
# ─────────────────────────────────────────────

class DataIngestor:
    def __init__(self):
        self.processed = []

    @singledispatchmethod
    def ingest(self, data):
        raise TypeError("Unsupported data type for ingestion")

    @ingest.register(str)
    def _(self, data: str):
        print(f"  Ingesting string data: {data}")
        self.processed.append(data)

    @ingest.register(list)
    def _(self, data: list):
        print(f"  Ingesting list data with {len(data)} items")
        for item in data:
            self.processed.append(item)


# ─────────────────────────────────────────────
# SECTION 4 — Static Overloading (typing.overload)
# ─────────────────────────────────────────────

class QueryBuilder:
    # Overload signatures for type-checkers (no runtime execution)
    @overload
    def fetch_user(self, identifier: int) -> dict: ...

    @overload
    def fetch_user(self, identifier: str) -> dict: ...

    # The actual runtime implementation (handles both cases)
    def fetch_user(self, identifier: Union[int, str]) -> dict:
        if isinstance(identifier, int):
            return {"id": identifier, "source": "database_lookup_by_id"}
        elif isinstance(identifier, str):
            return {"username": identifier, "source": "database_lookup_by_username"}
        else:
            raise TypeError("Identifier must be an int or a str")


# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("--- Section 1: Classic Pythonic Way ---")
    calc = AreaCalculator()
    print(f"Circle Area (r=5): {calc.calculate_area(5):.2f}")
    print(f"Rectangle Area (5x10): {calc.calculate_area(5, 10):.2f}")

    print("\n--- Section 2: singledispatch (Functions) ---")
    print(format_data("Hello"))
    print(format_data(12.345))
    print(format_data([1, "two", 3.0]))
    print(format_data({"not": "supported"}))

    print("\n--- Section 3: singledispatchmethod (Classes) ---")
    ingestor = DataIngestor()
    ingestor.ingest("UserEvent")
    ingestor.ingest(["Event1", "Event2"])
    try:
        ingestor.ingest(123)
    except TypeError as e:
        print(f"Captured expected error: {e}")

    print("\n--- Section 4: Static Overloading (typing.overload) ---")
    qb = QueryBuilder()
    print(qb.fetch_user(101))
    print(qb.fetch_user("admin_user"))

# Output:
#   --- Section 1: Classic Pythonic Way ---
#   Circle Area (r=5): 78.54
#   Rectangle Area (5x10): 50.00
#
#   --- Section 2: singledispatch (Functions) ---
#   String: 'Hello'
#   Number: 12.35
#   List: [Number: 1.00, String: 'two', Number: 3.00]
#   Default representation: {'not': 'supported'}
#
#   --- Section 3: singledispatchmethod (Classes) ---
#     Ingesting string data: UserEvent
#     Ingesting list data with 2 items
#   Captured expected error: Unsupported data type for ingestion
#
#   --- Section 4: Static Overloading (typing.overload) ---
#   {'id': 101, 'source': 'database_lookup_by_id'}
#   {'username': 'admin_user', 'source': 'database_lookup_by_username'}
# Why:
#   1. Python doesn't support multiple functions with the same name, so the 
#      simplest way is a single method with default args (`width=None`).
#   2. `singledispatch` inspects the type of the first argument at runtime 
#      and routes it to the matching registered function.
#   3. `singledispatchmethod` does the same thing as `singledispatch`, but is
#      designed for methods inside classes, ignoring the `self` or `cls` argument.
#   4. `typing.overload` allows tools like Mypy/VSCode to resolve return types 
#      correctly depending on whether an `int` or `str` is passed, but the actual 
#      runtime code is executed inside the final undecorated `fetch_user` method.
