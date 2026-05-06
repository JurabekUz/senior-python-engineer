"""
TOPIC: Decorators
======================================================

WHAT IS IT?
  A decorator is a design pattern that allows you to modify the behavior of a 
  function or class without permanently modifying its source code. They are 
  represented by the `@decorator_name` syntax.

RULES / KEY POINTS:
  1. High-Order Functions: Decorators are functions that take another function 
     as an argument and return a new function.
  2. Syntactic Sugar: `@dec` is just a shortcut for `fn = dec(fn)`.
  3. wraps: Always use `functools.wraps` to preserve the original function's 
     metadata (name, docstring, etc.).
  4. Order: If multiple decorators are used, they are applied from bottom to top.

COMMON PROBLEMS / PITFALLS:
  - Lost Metadata: Without `@wraps`, the decorated function loses its `__name__`.
  - Arguments: Forgetting to handle `*args` and `**kwargs` inside the wrapper 
    will break functions that take parameters.
  - Performance: Overusing decorators can add overhead, especially in tight loops.

WHEN TO USE IT:
  - Logging and timing (e.g., measuring execution time).
  - Authentication and authorization.
  - Caching (memoization).
  - Input validation.

RELATED TOPICS:
  - closures
  - inner_functions
  - functools.wraps
"""

import time
from functools import wraps

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept (The "Timer" example)
# ─────────────────────────────────────────────

def timer(fn):
    @wraps(fn) # Preserves metadata
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        end = time.perf_counter()
        print(f"Function {fn.__name__!r} took {end - start:.4f}s")
        return result
    return wrapper

@timer
def heavy_computation(n):
    """Simulates a heavy task."""
    time.sleep(n)
    return f"Done with {n}"

# ─────────────────────────────────────────────
# SECTION 2 — Decorators with Arguments
# ─────────────────────────────────────────────

def repeat(num_times):
    """A decorator factory that returns a decorator."""
    def decorator_repeat(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = fn(*args, **kwargs)
            return result
        return wrapper
    return decorator_repeat

@repeat(num_times=3)
def greet(name):
    print(f"Hello {name}")

# ─────────────────────────────────────────────
# SECTION 3 — Multiple Decorators
# ─────────────────────────────────────────────

def bold(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return f"<b>{fn(*args, **kwargs)}</b>"
    return wrapper

def italic(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return f"<i>{fn(*args, **kwargs)}</i>"
    return wrapper

@bold
@italic
def format_text(text):
    return text

# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("--- Section 1: Timer ---")
    print(heavy_computation(1))
    print(f"Function name preserved? {heavy_computation.__name__ == 'heavy_computation'}")

    print("\n--- Section 2: Repeat ---")
    greet("Jurabek")

    print("\n--- Section 3: Multiple ---")
    print(format_text("Hello World"))

# Output:
#   --- Section 1: Timer ---
#   Function 'heavy_computation' took 1.000...s
#   Done with 1
#   Function name preserved? True
#
#   --- Section 2: Repeat ---
#   Hello Jurabek
#   Hello Jurabek
#   Hello Jurabek
#
#   --- Section 3: Multiple ---
#   <b><i>Hello World</i></b>
# Why:
#   1. @wraps(fn) ensures the decorated function keeps its original identity.
#   2. Decorators with arguments require 3 levels of nesting: factory -> decorator -> wrapper.
#   3. Multiple decorators stack: bold(italic(format_text)). The bottom one runs first.
