"""
TOPIC: Typing Hints
======================================================

WHAT IS IT?
  Type hints (introduced in PEP 484) allow you to statically indicate the type of a value in Python. 
  They do not enforce types at runtime (Python remains dynamically typed), but they help third-party tools 
  like IDEs and type checkers (e.g., mypy) catch type errors before execution.

RULES / KEY POINTS:
  1. Use `:` to hint variables/arguments, and `->` to hint return types.
  2. Use the `typing` module for more complex types like List, Dict, Union, Optional, Any, Callable (in Python 3.9+, built-in list/dict/etc. can be used).
  3. Type hints have no effect on runtime performance or execution behavior.

COMMON PROBLEMS / PITFALLS:
  - Pitfall 1: Assuming type hints enforce type safety at runtime. `def add(a: int) -> int:` will still accept strings if called with them!
  - Pitfall 2: Over-complicating types. If a type is too complex to read, you might need to rethink your data structure or use a TypeAlias.

WHEN TO USE IT:
  - In almost all modern Python codebases, especially large projects, to improve readability and catch bugs early via static analysis.

RELATED TOPICS:
  - Dataclasses
  - pydantic (runtime type validation)
"""

from typing import List, Dict, Optional, Union, Callable

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept
# ─────────────────────────────────────────────

def greet(name: str) -> str:
    return f"Hello, {name}!"

# Basic variable type hint (Python 3.6+)
age: int = 25
is_active: bool = True

# ─────────────────────────────────────────────
# SECTION 2 — Advanced / Real-World Usage
# ─────────────────────────────────────────────

# Complex nested types
def process_users(users: List[Dict[str, Union[str, int]]]) -> Optional[int]:
    if not users:
        return None
    return len(users)

# Callable for functions passed as arguments
def execute_operation(operation: Callable[[int, int], int], a: int, b: int) -> int:
    return operation(a, b)

# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print(greet("Alice"))
    
    users_data = [{"name": "Bob", "id": 101}]
    print("Processed users:", process_users(users_data))
    
    add_func = lambda x, y: x + y
    print("Operation result:", execute_operation(add_func, 5, 3))

# Output:
#   Hello, Alice!
#   Processed users: 1
#   Operation result: 8
# Why: Standard function execution. Note that the Python interpreter ignores the hints, so the output is identical to unhinted code. Tools like mypy would catch if we passed a string to `execute_operation`.
