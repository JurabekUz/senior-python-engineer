"""
TOPIC: global and nonlocal Keywords
======================================================

WHAT IS IT?
  - By default in Python, any assignment inside a function creates a NEW local
    variable. You cannot write to a variable from an outer scope without
    explicitly declaring your intent.
  - `global`   : Declares that a variable inside a function refers to (and
                  can WRITE to) the module-level global variable.
  - `nonlocal` : Declares that a variable inside an inner function refers to
                  (and can WRITE to) the nearest enclosing (outer) function's
                  variable — NOT the global scope.

RULES / KEY POINTS:
  1. Reading is free. Writing requires a declaration (`global` or `nonlocal`).
  2. `global` reaches all the way up to the module level.
  3. `nonlocal` only goes up ONE level at a time to the nearest enclosing scope.
     It cannot reach the global scope.
  4. Best Practice: Avoid `global` in production code. Excessive use of global
     state makes code hard to test and debug. Prefer passing variables as
     arguments and returning new values instead.

COMMON PROBLEMS / PITFALLS:
  - Pitfall 1: Using `global` to share state between many functions. This is a
    design smell — consider using a class or passing the value as an argument.
  - Pitfall 2: Forgetting `nonlocal` inside a closure that needs to modify a
    captured variable, leading to an UnboundLocalError.

WHEN TO USE IT:
  - `global`: Module-level configuration or state that is intentionally shared
    (e.g., a settings flag, a registry dictionary). Use sparingly.
  - `nonlocal`: Inside closures that need to maintain and UPDATE their own
    private state (e.g., counters, accumulators, toggles).

RELATED TOPICS:
  - LEGB Scope Rule (legb_scope.py)
  - Closures (closures.py)
"""

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept (global keyword)
# ─────────────────────────────────────────────

# Module-level global variable
request_count = 0


def handle_request():
    """Simulates incrementing a global request counter."""
    global request_count  # Declare: I want to WRITE to the global 'request_count'
    request_count += 1


def get_count() -> int:
    return request_count  # Reading a global — no 'global' declaration needed


# ─────────────────────────────────────────────
# SECTION 2 — Advanced / Real-World Usage (nonlocal in closures)
# ─────────────────────────────────────────────

# Real-world example: A stateful on/off toggle built with a closure.
# 'nonlocal' allows the inner function to update the 'state' variable
# that lives in the enclosing 'make_toggle' scope.

def make_toggle(initial_state: bool = False):
    """Returns a function that flips a boolean state on each call."""
    state = initial_state

    def toggle() -> bool:
        nonlocal state  # Declare: I want to WRITE to 'state' in the enclosing scope
        state = not state
        return state

    return toggle


# Demonstrating the pitfall: forgetting 'nonlocal'
def make_broken_toggle():
    state = False

    def toggle() -> bool:
        # Without 'nonlocal', Python treats 'state' as a new local variable.
        # Reading it before assignment raises UnboundLocalError.
        try:
            state = not state  # UnboundLocalError!
        except UnboundLocalError as e:
            print(f"  Expected UnboundLocalError: {e}")
        return False

    return toggle


def main():
    print("--- Section 1: global keyword ---")
    print(f"Initial count: {get_count()}")
    handle_request()
    handle_request()
    handle_request()
    print(f"After 3 requests: {get_count()}")

    print("\n--- Section 2: nonlocal in a closure ---")
    dark_mode = make_toggle(initial_state=False)

    print(f"Toggle 1: {dark_mode()}")  # True
    print(f"Toggle 2: {dark_mode()}")  # False
    print(f"Toggle 3: {dark_mode()}")  # True

    # Two independent toggles — each has its own private 'state'
    toggle_a = make_toggle(False)
    toggle_b = make_toggle(True)
    toggle_a()
    print(f"\ntoggle_a after 1 flip: {toggle_a()}")  # False (flipped twice)
    print(f"toggle_b after 0 flips: {toggle_b()}")   # False (flipped once)

    print("\n--- Pitfall: Missing nonlocal ---")
    broken = make_broken_toggle()
    broken()


# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == "__main__":
    main()

# Expected Output:
# --- Section 1: global keyword ---
# Initial count: 0
# After 3 requests: 3
#
# --- Section 2: nonlocal in a closure ---
# Toggle 1: True
# Toggle 2: False
# Toggle 3: True
#
# toggle_a after 1 flip: False
# toggle_b after 0 flips: False
#
# --- Pitfall: Missing nonlocal ---
#   Expected UnboundLocalError: cannot access local variable 'state' before assignment
#
# Why:
#   1. 'global' makes 'request_count' in handle_request() point to the same
#      object as the module-level variable, so the increment is permanent.
#   2. 'nonlocal' makes 'state' in toggle() point to the variable in make_toggle(),
#      allowing it to be mutated. Without it, Python creates a NEW local 'state'.
#   3. toggle_a and toggle_b are independent closures with separate 'state' cells.
