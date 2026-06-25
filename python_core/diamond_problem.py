"""
TOPIC: The Diamond Problem
======================================================

WHAT IS IT?
  The "diamond problem" occurs when a class inherits from two classes that
  share a common ancestor, forming a diamond-shaped inheritance graph:

          A          ← common ancestor
         / \\
        B   C        ← both inherit from A
         \\ /
          D          ← inherits from B AND C

  The question: when D calls a method, which path does it take?
  Does A.__init__() run once or twice?

  Python solves this with C3 Linearization (MRO). Every class in the
  diamond is visited EXACTLY ONCE, in a deterministic order.

RULES / KEY POINTS:
  1. Without `super()`: A's __init__ would run TWICE (once via B, once via C).
     This causes double initialization bugs.
  2. With `super()`: Python follows the MRO → A's __init__ runs exactly ONCE.
  3. C3 rule: a class is never visited before ALL of its subclasses.
  4. MRO for D(B, C) with common ancestor A: D → B → C → A → object.
  5. In B, `super()` goes to C (next in D's MRO), NOT to A.
  6. Cooperative `super()` + `**kwargs` is the standard solution.

COMMON PROBLEMS / PITFALLS:
  - Calling `Parent.__init__(self)` directly instead of `super().__init__()`
    → breaks the MRO chain, causes double-init in diamonds.
  - Not using `**kwargs` → TypeError when unexpected args arrive from
    a sibling class in the MRO chain.
  - Assuming `super()` goes to "my parent" — it goes to "next in MRO".
  - Mutable state (lists, dicts) initialized in a common ancestor may get
    reset if __init__ runs twice due to non-cooperative calls.

WHEN TO USE IT:
  - Mixin-heavy designs (logging + serialization + validation + base model).
  - Framework classes (Django: multiple model mixins, DRF: generic views).
  - Understanding why `super()` is essential in Python OOP.

RELATED TOPICS:
  - inheritance_mro (previous topic — MRO fundamentals)
  - abc_abstract
  - class_attributes
"""

# ─────────────────────────────────────────────
# SECTION 1 — The Diamond Shape
# ─────────────────────────────────────────────

#        Animal
#        /    \
#    Flyer   Swimmer
#        \    /
#       FlyingFish

class Animal:
    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)  # Cooperative: forward remaining kwargs
        self.name = name
        print(f"  Animal.__init__(name={name!r})")

    def breathe(self) -> str:
        return f"{self.name} breathes"


class Flyer(Animal):
    def __init__(self, max_altitude: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.max_altitude = max_altitude
        print(f"  Flyer.__init__(max_altitude={max_altitude})")

    def fly(self) -> str:
        return f"{self.name} flies up to {self.max_altitude}m"


class Swimmer(Animal):
    def __init__(self, max_depth: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.max_depth = max_depth
        print(f"  Swimmer.__init__(max_depth={max_depth})")

    def swim(self) -> str:
        return f"{self.name} dives to {self.max_depth}m"


class FlyingFish(Flyer, Swimmer):
    def __init__(self, name: str, max_altitude: int, max_depth: int):
        print("  FlyingFish.__init__()")
        # One super() call → entire MRO chain runs, each class takes its kwargs
        super().__init__(
            name=name,
            max_altitude=max_altitude,
            max_depth=max_depth,
        )

# MRO: FlyingFish → Flyer → Swimmer → Animal → object
# Init order: FlyingFish → Flyer → Swimmer → Animal → object
# Animal.__init__ runs EXACTLY ONCE ✅


# ─────────────────────────────────────────────
# SECTION 2 — The BROKEN Way (without super)
# ─────────────────────────────────────────────

class BaseLogger:
    init_count = 0

    def __init__(self):
        BaseLogger.init_count += 1
        print(f"  BaseLogger.__init__() — call #{BaseLogger.init_count}")


class FileLogger(BaseLogger):
    def __init__(self):
        BaseLogger.__init__(self)  # ❌ Direct call, not super()
        print("  FileLogger.__init__()")


class DBLogger(BaseLogger):
    def __init__(self):
        BaseLogger.__init__(self)  # ❌ Direct call, not super()
        print("  DBLogger.__init__()")


class DualLogger(FileLogger, DBLogger):
    def __init__(self):
        FileLogger.__init__(self)  # ❌ Direct call
        DBLogger.__init__(self)    # ❌ Direct call
        print("  DualLogger.__init__()")

# Result: BaseLogger.__init__ runs TWICE! (once via FileLogger, once via DBLogger)


# ─────────────────────────────────────────────
# SECTION 3 — The FIXED Way (cooperative super)
# ─────────────────────────────────────────────

class BaseLoggerFixed:
    init_count = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        BaseLoggerFixed.init_count += 1
        print(f"  BaseLoggerFixed.__init__() — call #{BaseLoggerFixed.init_count}")


class FileLoggerFixed(BaseLoggerFixed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # ✅ Cooperative
        print("  FileLoggerFixed.__init__()")


class DBLoggerFixed(BaseLoggerFixed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # ✅ Cooperative
        print("  DBLoggerFixed.__init__()")


class DualLoggerFixed(FileLoggerFixed, DBLoggerFixed):
    def __init__(self):
        super().__init__()  # ✅ One call → full MRO chain
        print("  DualLoggerFixed.__init__()")

# Result: BaseLoggerFixed.__init__ runs ONCE ✅
# MRO: DualLoggerFixed → FileLoggerFixed → DBLoggerFixed → BaseLoggerFixed → object


# ─────────────────────────────────────────────
# SECTION 4 — Method Resolution in the Diamond
# ─────────────────────────────────────────────

class A:
    def greet(self):
        return "Hello from A"

class B(A):
    def greet(self):
        return "Hello from B"

class C(A):
    def greet(self):
        return "Hello from C"

class D(B, C):
    pass  # No override — which greet() does D use?

# MRO: D → B → C → A → object
# D().greet() calls B.greet() — leftmost parent wins


class D2(B, C):
    def greet(self):
        # Access ALL versions explicitly
        return {
            "D2": "Hello from D2",
            "B": B.greet(self),      # Explicit, bypasses MRO
            "C": C.greet(self),      # Explicit
            "A": A.greet(self),      # Explicit
            "super": super().greet() # MRO: goes to B
        }


# ─────────────────────────────────────────────
# SECTION 5 — Real-World: Django-Style Mixins
# ─────────────────────────────────────────────

class View:
    """Base view (like Django's View)."""
    def dispatch(self, request: str) -> str:
        return f"View.dispatch({request})"


class LoginRequiredMixin(View):
    """Checks auth before dispatching."""
    def dispatch(self, request: str) -> str:
        print(f"  🔒 LoginRequiredMixin: checking auth for '{request}'")
        if request == "anonymous":
            return "403 Forbidden"
        return super().dispatch(request)  # → next in MRO


class PermissionMixin(View):
    """Checks permissions before dispatching."""
    def dispatch(self, request: str) -> str:
        print(f"  🛡️ PermissionMixin: checking permissions for '{request}'")
        if request == "readonly":
            return "403 No Permission"
        return super().dispatch(request)  # → next in MRO


class ProtectedView(LoginRequiredMixin, PermissionMixin, View):
    """Both auth AND permissions checked before the view runs."""
    def dispatch(self, request: str) -> str:
        print(f"  📄 ProtectedView.dispatch({request})")
        return super().dispatch(request)

# MRO: ProtectedView → LoginRequiredMixin → PermissionMixin → View → object
# dispatch chain: ProtectedView → LoginRequired → Permission → View


# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("--- Section 1: Diamond with Cooperative super() ---")
    fish = FlyingFish("Nemo", max_altitude=50, max_depth=100)
    print(f"\n{fish.breathe()}")
    print(fish.fly())
    print(fish.swim())
    print(f"MRO: {' → '.join(c.__name__ for c in FlyingFish.__mro__)}")

    print("\n--- Section 2: BROKEN — Double Init ---")
    BaseLogger.init_count = 0
    broken = DualLogger()
    print(f"BaseLogger.__init__ called {BaseLogger.init_count} time(s) ❌")

    print("\n--- Section 3: FIXED — Single Init ---")
    BaseLoggerFixed.init_count = 0
    fixed = DualLoggerFixed()
    print(f"BaseLoggerFixed.__init__ called {BaseLoggerFixed.init_count} time(s) ✅")

    print("\n--- Section 4: Method Resolution ---")
    d = D()
    print(f"D().greet() = '{d.greet()}'  (B wins — leftmost parent)")
    print(f"D2 all versions: {D2().greet()}")

    print("\n--- Section 5: Django-Style Mixin Chain ---")
    view = ProtectedView()
    print("Request from 'admin':")
    print(f"  Result: {view.dispatch('admin')}")
    print("\nRequest from 'anonymous':")
    print(f"  Result: {view.dispatch('anonymous')}")
    print("\nRequest from 'readonly':")
    print(f"  Result: {view.dispatch('readonly')}")

# Output:
#   --- Section 1: Diamond with Cooperative super() ---
#     FlyingFish.__init__()
#     Animal.__init__(name='Nemo')
#     Swimmer.__init__(max_depth=100)
#     Flyer.__init__(max_altitude=50)
#
#   Nemo breathes
#   Nemo flies up to 50m
#   Nemo dives to 100m
#   MRO: FlyingFish → Flyer → Swimmer → Animal → object
#
#   --- Section 2: BROKEN — Double Init ---
#     BaseLogger.__init__() — call #1
#     FileLogger.__init__()
#     BaseLogger.__init__() — call #2
#     DBLogger.__init__()
#     DualLogger.__init__()
#   BaseLogger.__init__ called 2 time(s) ❌
#
#   --- Section 3: FIXED — Single Init ---
#     BaseLoggerFixed.__init__() — call #1
#     DBLoggerFixed.__init__()
#     FileLoggerFixed.__init__()
#     DualLoggerFixed.__init__()
#   BaseLoggerFixed.__init__ called 1 time(s) ✅
#
#   --- Section 4: Method Resolution ---
#   D().greet() = 'Hello from B'  (B wins — leftmost parent)
#   D2 all versions: {'D2': 'Hello from D2', 'B': ..., 'C': ..., ...}
#
#   --- Section 5: Django-Style Mixin Chain ---
#   Request from 'admin':
#     📄 ProtectedView.dispatch(admin)
#     🔒 LoginRequiredMixin: checking auth for 'admin'
#     🛡️ PermissionMixin: checking permissions for 'admin'
#     Result: View.dispatch(admin)
#
#   Request from 'anonymous':
#     📄 ProtectedView.dispatch(anonymous)
#     🔒 LoginRequiredMixin: checking auth for 'anonymous'
#     Result: 403 Forbidden
#
#   Request from 'readonly':
#     📄 ProtectedView.dispatch(readonly)
#     🔒 LoginRequiredMixin: checking auth for 'readonly'
#     🛡️ PermissionMixin: checking permissions for 'readonly'
#     Result: 403 No Permission
# Why:
#   1. Cooperative super() + **kwargs → Animal.__init__ runs ONCE even
#      though both Flyer and Swimmer inherit from it.
#   2. Direct calls (Parent.__init__) bypass MRO → BaseLogger inits TWICE.
#   3. super().__init__() follows MRO → BaseLoggerFixed inits ONCE.
#   4. D(B, C): leftmost parent B wins for method resolution.
#   5. Django mixin pattern: each mixin's dispatch() does its check, then
#      calls super().dispatch() to pass control to the next mixin in MRO.
#      If a check fails, it short-circuits and returns early.
