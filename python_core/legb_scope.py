"""
TOPIC: LEGB Scope Rule
======================================================

WHAT IS IT?
  - LEGB is Python's variable lookup order. When you use a variable name,
    Python searches for it in this exact sequence and stops at the first match:
      L — Local      : Inside the current function
      E — Enclosing  : Inside any enclosing (outer) function (for closures)
      G — Global     : At the top level of the current module/file
      B — Built-in   : Python's built-in namespace (len, print, range, etc.)
  - If the name is not found in any of these layers, Python raises a NameError.

RULES / KEY POINTS:
  1. LEGB is READ-only by default. You can read variables from outer scopes,
     but you cannot WRITE to them without `global` or `nonlocal`.
  2. Shadowing: A variable in an inner scope can "shadow" (hide) a variable
     with the same name in an outer scope. The outer variable is unaffected.
  3. Built-in Shadowing (Danger!): You CAN accidentally shadow built-in names
     like `list`, `len`, or `input` by creating local variables with the same
     name. This is a common source of confusing bugs.
  4. Module-level = Global: The 'Global' in LEGB means the top-level of the
     current .py file — NOT the entire program.

COMMON PROBLEMS / PITFALLS:
  - Pitfall 1: Assigning to a variable inside a function makes Python treat it
    as LOCAL throughout the entire function — even before the assignment line.
    This causes an UnboundLocalError if you try to read it before assignment.
  - Pitfall 2: Shadowing a built-in (e.g., `list = [1,2,3]`) breaks the
    original built-in for the rest of that scope.

WHEN TO USE IT:
  - Understanding LEGB is essential every time you debug a NameError or an
    unexpected variable value — it tells you exactly WHERE Python found (or
    failed to find) the name you used.

RELATED TOPICS:
  - global and nonlocal keywords (global_and_nonlocal.py)
  - Closures and Enclosing scope (closures.py)
"""

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept (L, G, B layers)
# ─────────────────────────────────────────────

# G — Global scope
language = "Python"


def demonstrate_lgb():
    # L — Local scope
    version = 3.12

    # Reads 'version' from L (local) — found immediately
    print(f"Local  'version': {version}")

    # Reads 'language' from G (global) — not in local, goes up one level
    print(f"Global 'language': {language}")

    # Reads 'len' from B (built-in) — not local, not global, found in built-ins
    print(f"Built-in 'len': {len([1, 2, 3])}")


# ─────────────────────────────────────────────
# SECTION 2 — Advanced / Real-World Usage (E layer + Shadowing Pitfalls)
# ─────────────────────────────────────────────

# E — Enclosing scope (the 'E' in LEGB only applies inside nested functions)
def outer():
    message = "I am in the enclosing scope"  # Enclosing variable

    def inner():
        # 'message' is not Local here, so Python looks at Enclosing → found!
        print(f"Enclosing 'message': {message}")

    inner()


def demonstrate_shadowing():
    """Shows how a local variable shadows an outer one."""
    language = "JavaScript"  # This shadows the global 'language' inside this function
    print(f"Inside function, 'language' = {language}")  # Reads LOCAL copy


def demonstrate_builtin_shadowing():
    """Shows the danger of accidentally shadowing a built-in name."""
    # BAD PRACTICE: We shadow the built-in 'len' with a local variable
    len = "oops, I broke len!"
    print(f"len is now: {len}")
    try:
        len([1, 2, 3])  # Calling 'len' as a function now fails!
    except TypeError as e:
        print(f"Expected Error after shadowing built-in: {e}")


def demonstrate_unbound_pitfall():
    """Shows the UnboundLocalError caused by LEGB's assignment rule."""
    x = 10  # Global x

    def bad_function():
        # Because we ASSIGN to 'x' below, Python marks 'x' as LOCAL for the
        # ENTIRE function body. Reading it before assignment causes an error.
        try:
            print(x)  # UnboundLocalError: 'x' referenced before assignment
        except UnboundLocalError as e:
            print(f"Expected UnboundLocalError: {e}")
        x = 20  # This assignment makes Python treat 'x' as local everywhere

    bad_function()


def main():
    print("--- Section 1: L, G, B Layers ---")
    demonstrate_lgb()

    print("\n--- Section 2: E Layer (Enclosing) ---")
    outer()

    print("\n--- Shadowing: Local hides Global ---")
    print(f"Global 'language' before call: {language}")
    demonstrate_shadowing()
    print(f"Global 'language' after call: {language}")  # Unchanged!

    print("\n--- Pitfall: Built-in Shadowing ---")
    demonstrate_builtin_shadowing()

    print("\n--- Pitfall: UnboundLocalError ---")
    demonstrate_unbound_pitfall()


# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == "__main__":
    main()

# Expected Output:
# --- Section 1: L, G, B Layers ---
# Local  'version': 3.12
# Global 'language': Python
# Built-in 'len': 3
#
# --- Section 2: E Layer (Enclosing) ---
# Enclosing 'message': I am in the enclosing scope
#
# --- Shadowing: Local hides Global ---
# Global 'language' before call: Python
# Inside function, 'language' = JavaScript
# Global 'language' after call: Python
#
# --- Pitfall: Built-in Shadowing ---
# len is now: oops, I broke len!
# Expected Error after shadowing built-in: 'str' object is not callable
#
# --- Pitfall: UnboundLocalError ---
# Expected UnboundLocalError: cannot access local variable 'x' before assignment
#
# Why:
#   1. Python searches L -> E -> G -> B in order and stops at the first match.
#   2. Shadowing creates a NEW variable in the inner scope; the outer one is untouched.
#   3. Any assignment in a function body makes that name LOCAL for the entire function.
