"""
TOPIC: Duck Typing (Dynamic Typing)
======================================================

WHAT IS IT?
  Duck Typing is a programming concept where an object's suitability for a 
  given role is determined by the presence of certain methods and properties, 
  rather than its actual type/inheritance hierarchy. 
  "If it walks like a duck and quacks like a duck, then it's a duck."

RULES / KEY POINTS:
  1. No Type Enforcement: We do not check `isinstance(obj, ExpectedClass)`.
  2. Interface over Inheritance: Different classes can satisfy the same interface
     without sharing a common base class.
  3. LBYL vs EAFP: Python favors "Easier to Ask for Forgiveness than Permission" 
     (try/except) over "Look Before You Leap" (checking hasattr/type).
  4. typing.Protocol (PEP 544): Allows static type checkers (like mypy) to perform
     structural subtyping (static duck typing).

COMMON PROBLEMS / PITFALLS:
  - AttributeError: If an object doesn't implement a method called at runtime.
  - Inadvertent interface matching: An object might happen to have a method 
    with the same name but completely different semantics (e.g., `run()` on a
    `Database` vs `Runner`).
  - Lacking documentation: Duck typing can make code harder to read if the
    expected interface is not documented or hinted with `Protocol`.

WHEN TO USE IT:
  - To allow highly decoupled and flexible plugins/components.
  - Mocking/testing: Easily pass fake objects that mimic the real interface.
  - Generic algorithms (e.g., a function that works on any object with a `.read()` method).

RELATED TOPICS:
  - abc_abstract (nominal interfaces)
  - typing.Protocol (structural subtyping)
  - __getattr__and__setattr__
"""

from typing import Protocol

# ─────────────────────────────────────────────
# SECTION 1 — Classic Duck Typing
# ─────────────────────────────────────────────

class Duck:
    def quack(self) -> str:
        return "Quack!"

    def fly(self) -> str:
        return "Flap flap!"


class Person:
    def quack(self) -> str:
        return "I am acting like a duck: Quack!"

    def fly(self) -> str:
        return "I am waving my arms: Flap!"


def make_it_quack_and_fly(thing) -> None:
    # We don't check `isinstance(thing, Duck)`!
    # We just call the methods we expect to be there.
    print(f"  Quack: {thing.quack()}")
    print(f"  Fly:   {thing.fly()}")


# ─────────────────────────────────────────────
# SECTION 2 — EAFP (Pythonic) vs LBYL
# ─────────────────────────────────────────────

class SafeQuacker:
    def quack(self) -> str:
        return "Safe Quack!"


def process_quacker_lbyl(thing) -> None:
    """Look Before You Leap: check before calling."""
    if hasattr(thing, "quack") and callable(getattr(thing, "quack")):
        print(f"  LBYL: {thing.quack()}")
    else:
        print("  LBYL: This thing cannot quack!")


def process_quacker_eafp(thing) -> None:
    """Easier to Ask Forgiveness than Permission: try and handle exception."""
    try:
        print(f"  EAFP: {thing.quack()}")
    except (AttributeError, TypeError):
        print("  EAFP: Failed to quack!")


# ─────────────────────────────────────────────
# SECTION 3 — Static Duck Typing: typing.Protocol
# ─────────────────────────────────────────────

class Quacker(Protocol):
    """A Protocol defines a structural contract for static type checkers."""
    def quack(self) -> str:
        ...


def strict_quack(q: Quacker) -> str:
    """Mypy knows `q` must have a `quack` method, even if classes don't inherit from Quacker."""
    return q.quack()


class ToyDuck:
    # No explicit inheritance from Quacker, but fits the Protocol structurally!
    def quack(self) -> str:
        return "Squeak!"


# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("--- Section 1: Classic Duck Typing ---")
    donald = Duck()
    john = Person()
    
    print("Donald:")
    make_it_quack_and_fly(donald)
    print("John:")
    make_it_quack_and_fly(john)

    print("\n--- Section 2: EAFP vs LBYL ---")
    sq = SafeQuacker()
    number = 42
    
    print("Processing SafeQuacker:")
    process_quacker_lbyl(sq)
    process_quacker_eafp(sq)
    
    print("Processing integer (cannot quack):")
    process_quacker_lbyl(number)
    process_quacker_eafp(number)

    print("\n--- Section 3: Static Duck Typing (Protocol) ---")
    toy = ToyDuck()
    print(f"Strict quack on ToyDuck: {strict_quack(toy)}")

# Output:
#   --- Section 1: Classic Duck Typing ---
#   Donald:
#     Quack: Quack!
#     Fly:   Flap flap!
#   John:
#     Quack: I am acting like a duck: Quack!
#     Fly:   I am waving my arms: Flap!
#
#   --- Section 2: EAFP vs LBYL ---
#   Processing SafeQuacker:
#     LBYL: Safe Quack!
#     EAFP: Safe Quack!
#   Processing integer (cannot quack):
#     LBYL: This thing cannot quack!
#     EAFP: Failed to quack!
#
#   --- Section 3: Static Duck Typing (Protocol) ---
#   Strict quack on ToyDuck: Squeak!
# Why:
#   1. Both Duck and Person can be passed to `make_it_quack_and_fly` because 
#      they implement `quack` and `fly` (Classic Duck Typing).
#   2. EAFP is standard in Python: we try calling the method directly, catching
#      AttributeError if it fails, which avoids redundant checks (LBYL).
#   3. ToyDuck matches the Quacker Protocol because it has the `quack` method, 
#      satisfying the static check without subclass inheritance.
