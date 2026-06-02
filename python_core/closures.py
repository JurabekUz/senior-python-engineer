"""
TOPIC: Closures
======================================================

WHAT IS IT?
  - A closure is an inner function that REMEMBERS the variables from its
    enclosing (outer) function's scope, even after the outer function has
    finished executing and is no longer in memory.
  - In other words, the inner function "closes over" the variables it needs
    and carries them with it wherever it goes.

RULES / KEY POINTS:
  1. Three Conditions for a Closure:
     a) There must be a nested (inner) function.
     b) The inner function must refer to a variable from the outer scope.
     c) The outer function must RETURN the inner function.
  2. Lifetime: The captured variables stay alive as long as the closure
     object itself is alive — even if the outer function is long gone.
  3. Inspection: You can inspect what a closure has captured using the
     `__closure__` attribute and `cell_contents`.
  4. State: Each closure call to the factory function creates an independent
     "memory cell" — closures are a lightweight alternative to classes for
     managing simple state.

COMMON PROBLEMS / PITFALLS:
  - Pitfall 1 (Loop Closures): Creating closures inside a loop that capture
    a loop variable. All closures end up sharing the LAST value of the loop
    variable, not their value at creation time. Fix: use a default argument.
  - Pitfall 2: Trying to modify (write to) a captured variable directly
    raises an UnboundLocalError. Fix: use the `nonlocal` keyword.

WHEN TO USE IT:
  - Maintaining lightweight state without a full class (e.g., counters, caches).
  - Building configurable function factories (e.g., validators, formatters).
  - The foundation of decorators.

RELATED TOPICS:
  - Inner Functions (inner_functions.py)
  - global and nonlocal keywords (global_and_nonlocal.py)
  - Decorators (decorators.py)
"""

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept (A Simple Closure)
# ─────────────────────────────────────────────

def make_counter(start: int = 0):
    """A closure that remembers its own count between calls."""
    count = start  # This variable lives inside the closure's memory

    def increment() -> int:
        nonlocal count  # We need 'nonlocal' to WRITE to the captured variable
        count += 1
        return count

    return increment  # Return the inner function (the closure)


# ─────────────────────────────────────────────
# SECTION 2 — Advanced / Real-World Usage
# ─────────────────────────────────────────────

# Real-world example: A configurable validator factory.
# Instead of a class, we use a closure to create reusable validators.

def make_range_validator(min_val: int, max_val: int):
    """Returns a validator function for a specific numeric range."""
    def validate(value: int) -> bool:
        if not (min_val <= value <= max_val):
            raise ValueError(
                f"Value {value} is out of allowed range [{min_val}, {max_val}]"
            )
        return True
    return validate


# Pitfall Demo: Loop closure trap
def loop_closure_pitfall():
    print("\n-- Pitfall: Loop Closure Trap --")
    # WRONG: All functions capture the same 'i' variable (its final value = 2)
    funcs_wrong = [lambda: i for i in range(3)]
    print("Wrong output:", [f() for f in funcs_wrong])  # [2, 2, 2]

    # CORRECT: Use a default argument to capture the value at creation time
    funcs_correct = [lambda i=i: i for i in range(3)]
    print("Correct output:", [f() for f in funcs_correct])  # [0, 1, 2]


def main():
    print("--- Section 1: Simple Counter Closure ---")
    counter_a = make_counter(0)
    counter_b = make_counter(10)  # Independent closure with its own state

    print(f"counter_a: {counter_a()}")  # 1
    print(f"counter_a: {counter_a()}")  # 2
    print(f"counter_a: {counter_a()}")  # 3
    print(f"counter_b: {counter_b()}")  # 11 — completely independent

    # Inspecting what the closure captured
    print(f"\nCaptured variables in counter_a: {[c.cell_contents for c in counter_a.__closure__]}")

    print("\n--- Section 2: Validator Factory ---")
    validate_age = make_range_validator(0, 120)
    validate_score = make_range_validator(0, 100)

    print(f"Age 25 valid: {validate_age(25)}")
    print(f"Score 85 valid: {validate_score(85)}")

    try:
        validate_age(200)
    except ValueError as e:
        print(f"Expected Error: {e}")

    loop_closure_pitfall()


# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == "__main__":
    main()

# Expected Output:
# --- Section 1: Simple Counter Closure ---
# counter_a: 1
# counter_a: 2
# counter_a: 3
# counter_b: 11
#
# Captured variables in counter_a: [3]
#
# --- Section 2: Validator Factory ---
# Age 25 valid: True
# Score 85 valid: True
# Expected Error: Value 200 is out of allowed range [0, 120]
#
# -- Pitfall: Loop Closure Trap --
# Wrong output: [2, 2, 2]
# Correct output: [0, 1, 2]
#
# Why:
#   1. counter_a and counter_b are independent closures — each captured its OWN
#      'count' variable. Calling one does not affect the other.
#   2. __closure__ reveals the current state of captured variables.
#   3. In the loop pitfall, all lambdas captured the same 'i' reference.
#      By the time they run, i == 2. The default argument fix captures the VALUE.
