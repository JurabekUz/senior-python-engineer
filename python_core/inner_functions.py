"""
TOPIC: Inner Functions (Nested Functions)
======================================================

WHAT IS IT?
  - An inner function (also called a nested function) is simply a function
    defined inside another function.
  - The inner function has full access to variables and parameters of its
    enclosing (outer) function — this is the foundation for closures.

RULES / KEY POINTS:
  1. Scope: An inner function is local to the outer function. It cannot be
     called directly from outside the outer function.
  2. Enclosing Scope Access: An inner function can READ variables from the
     outer function's scope freely.
  3. Use Cases: Inner functions are used for:
     - Helper/utility logic that is only relevant to one function.
     - Building closures (returning the inner function as a value).
     - Decorators (which are a special kind of inner function pattern).

COMMON PROBLEMS / PITFALLS:
  - Pitfall 1: Trying to call the inner function from outside the outer function
    raises a NameError — it simply does not exist in the outer scope.
  - Pitfall 2: Confusing inner functions with closures. An inner function becomes
    a closure only when it is RETURNED and CAPTURES a variable from the outer scope.

WHEN TO USE IT:
  - When you have helper logic used only inside one function (encapsulation).
  - When building factory functions (a function that creates and returns another
    function configured with some initial state).

RELATED TOPICS:
  - Closures (closures.py)
  - LEGB Scope Rule (legb_scope.py)
  - Decorators (decorators.py)
"""

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept (Defining & Calling an Inner Function)
# ─────────────────────────────────────────────

def greet(name: str) -> None:
    # This inner function is only accessible inside 'greet'
    def build_message() -> str:
        # Inner function reads 'name' from the enclosing 'greet' scope
        return f"Hello, {name}! Welcome."

    message = build_message()
    print(message)


# ─────────────────────────────────────────────
# SECTION 2 — Advanced / Real-World Usage (Factory Function)
# ─────────────────────────────────────────────

# A factory function creates and returns a configured inner function.
# Each call to the outer function produces a brand new, independent inner function.

def make_multiplier(factor: int):
    """Returns a function that multiplies any number by 'factor'."""
    def multiplier(number: int) -> int:
        return number * factor
    return multiplier  # We return the inner function itself, not its result


def main():
    print("--- Section 1: Basic Inner Function ---")
    greet("Jurabek")
    greet("Python")

    print("\n--- Section 2: Factory Function ---")
    double = make_multiplier(2)   # Creates a 'multiply by 2' function
    triple = make_multiplier(3)   # Creates a 'multiply by 3' function

    print(f"double(5)  = {double(5)}")   # 10
    print(f"triple(5)  = {triple(5)}")   # 15
    print(f"double(10) = {double(10)}")  # 20

    # Proving they are independent function objects
    print(f"\nAre double and triple the same object? {double is triple}")


# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == "__main__":
    main()

# Expected Output:
# --- Section 1: Basic Inner Function ---
# Hello, Jurabek! Welcome.
# Hello, Python! Welcome.
#
# --- Section 2: Factory Function ---
# double(5)  = 10
# triple(5)  = 15
# double(10) = 20
#
# Are double and triple the same object? False
#
# Why:
#   1. 'build_message' is an inner function — it reads 'name' from greet's scope.
#   2. Each call to make_multiplier() creates a FRESH inner 'multiplier' function,
#      capturing the given 'factor'. So 'double' and 'triple' are separate objects.
