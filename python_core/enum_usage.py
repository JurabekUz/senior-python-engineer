"""
TOPIC: Enums (Enumerations)
======================================================

WHAT IS IT?
  An enumeration is a set of symbolic names (members) bound to unique, constant values.
  In Python, the `enum` module provides a way to define enumerations.

RULES / KEY POINTS:
  1. Enum members are singletons, meaning you can compare them with `is`.
  2. Enums are iterable, and you can loop through their members.
  3. Enums are immutable; you cannot add, remove, or change members after creation.

COMMON PROBLEMS / PITFALLS:
  - Pitfall 1: Trying to compare an Enum member directly to an integer or string (unless you use IntEnum or StrEnum).
  - Pitfall 2: Attempting to modify an Enum member's value after it's defined (raises AttributeError).

WHEN TO USE IT:
  - When you have a fixed set of options (e.g., Status, Directions, Roles) and want to avoid "magic strings" or "magic numbers."

RELATED TOPICS:
  - Dataclasses
  - Constants
"""

from enum import Enum, IntEnum, auto

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept
# ─────────────────────────────────────────────

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# Basic usage
my_color = Color.RED

# ─────────────────────────────────────────────
# SECTION 2 — Advanced / Real-World Usage
# ─────────────────────────────────────────────

class Status(IntEnum):
    PENDING = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()

def check_status(status: Status):
    if status is Status.COMPLETED:
        return "All done!"
    elif status == 2:  # Possible because it's IntEnum
        return "Still working on it."
    return "Not started."

# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print(Color.RED.name)
    print(Color.RED.value)
    
    print(Status.IN_PROGRESS.value)
    print(check_status(Status.COMPLETED))

# Output:
#   RED
#   1
#   2
#   All done!
# Why: `name` gets the member's name as a string, `value` gets the assigned value. auto() assigns 1, 2, 3 sequentially. IntEnum allows comparison with integers.
