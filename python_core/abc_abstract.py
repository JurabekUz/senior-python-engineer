"""
TOPIC: ABC — Abstract Base Classes
======================================================

WHAT IS IT?
  The `abc` module provides tools to define Abstract Base Classes (ABCs).
  An ABC is a class that CANNOT be instantiated directly — it exists only
  to define a contract (interface) that subclasses MUST implement.
  Python uses ABCs to bring formal interfaces to a duck-typed language.

RULES / KEY POINTS:
  1. Inherit from `ABC` (or use `metaclass=ABCMeta`) to create an abstract class.
  2. Mark methods with `@abstractmethod` — subclasses MUST override them.
  3. You CANNOT instantiate a class that has unimplemented abstract methods.
  4. ABC CAN have concrete (non-abstract) methods — they are inherited as-is.
  5. `@abstractmethod` must be the INNERMOST decorator when stacking.
  6. `register()` lets you declare a class as a "virtual subclass" without
     inheriting — it passes `isinstance()` but gets NO method inheritance.
  7. `__subclasshook__` lets you define custom rules for `issubclass()`.

COMMON PROBLEMS / PITFALLS:
  - Forgetting to implement ALL abstract methods → TypeError at instantiation.
  - Decorator order: `@property` + `@abstractmethod` → `@property` must be
    outer, `@abstractmethod` must be inner. Wrong order silently breaks.
  - Virtual subclasses (register) do NOT inherit anything — they just pass
    `isinstance()` checks. Calling an unimplemented method will crash.
  - ABC enforcement happens at instantiation, NOT at class definition.
    The class body itself can be defined without errors.

WHEN TO USE IT:
  - Plugin / driver systems where every plugin must implement certain methods.
  - Framework base classes (e.g., Django views, serializers).
  - When you want to enforce a contract across a team in a large codebase.
  - When duck typing alone isn't safe enough (you need early crash, not late).

RELATED TOPICS:
  - duck_typing
  - property
  - inheritance_mro
  - typing.Protocol (structural subtyping alternative)
"""

from abc import ABC, abstractmethod, ABCMeta

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept: Defining an ABC
# ─────────────────────────────────────────────

class PaymentProcessor(ABC):
    """Every payment processor MUST implement `charge` and `refund`."""

    @abstractmethod
    def charge(self, amount: float) -> str:
        """Charge a customer. Must return a transaction ID."""
        ...  # No implementation — subclass must provide one

    @abstractmethod
    def refund(self, transaction_id: str) -> bool:
        """Refund a transaction. Must return True/False."""
        ...

    # Concrete method — inherited by ALL subclasses automatically
    def format_amount(self, amount: float) -> str:
        return f"${amount:,.2f}"


class StripeProcessor(PaymentProcessor):
    """Implements ALL abstract methods → CAN be instantiated."""

    def charge(self, amount: float) -> str:
        return f"stripe_txn_{id(self)}_{amount}"

    def refund(self, transaction_id: str) -> bool:
        print(f"Refunding {transaction_id} via Stripe")
        return True


class BrokenProcessor(PaymentProcessor):
    """Implements only `charge`, forgets `refund` → CANNOT be instantiated."""

    def charge(self, amount: float) -> str:
        return "partial_txn"
    # `refund` is NOT implemented → TypeError on instantiation


# ─────────────────────────────────────────────
# SECTION 2 — Abstract Properties
# ─────────────────────────────────────────────

class Animal(ABC):
    """Demonstrates abstract properties — subclass must provide them."""

    @property
    @abstractmethod  # ← MUST be innermost decorator
    def sound(self) -> str:
        """Every animal must define what sound it makes."""
        ...

    @property
    @abstractmethod
    def legs(self) -> int:
        ...

    def describe(self) -> str:
        return f"I have {self.legs} legs and go '{self.sound}'"


class Dog(Animal):
    @property
    def sound(self) -> str:
        return "Woof"

    @property
    def legs(self) -> int:
        return 4


class Snake(Animal):
    @property
    def sound(self) -> str:
        return "Hiss"

    @property
    def legs(self) -> int:
        return 0


# ─────────────────────────────────────────────
# SECTION 3 — ABCMeta (the old-style way)
# ─────────────────────────────────────────────

# `class Foo(ABC)` is just a shortcut for `class Foo(metaclass=ABCMeta)`.
# They are 100% equivalent. The ABC class itself uses ABCMeta under the hood.

class OldStyleBase(metaclass=ABCMeta):
    @abstractmethod
    def execute(self):
        ...

class OldStyleImpl(OldStyleBase):
    def execute(self):
        return "executed via ABCMeta style"


# ─────────────────────────────────────────────
# SECTION 4 — register() — Virtual Subclasses
# ─────────────────────────────────────────────

class Serializer(ABC):
    @abstractmethod
    def serialize(self, data: dict) -> str:
        ...

# Normal subclass — inherits and implements
class JsonSerializer(Serializer):
    def serialize(self, data: dict) -> str:
        import json
        return json.dumps(data)


# Virtual subclass — does NOT inherit, just passes isinstance() check
class ThirdPartySerializer:
    """Imagine this comes from a library you don't control."""
    def serialize(self, data: dict) -> str:
        return str(data)

Serializer.register(ThirdPartySerializer)  # ← "Trust me, it's a Serializer"

# WARNING: If ThirdPartySerializer did NOT have `serialize`, it would
# still pass isinstance() — but crash when you call .serialize()!


# ─────────────────────────────────────────────
# SECTION 5 — __subclasshook__ (Custom Rules)
# ─────────────────────────────────────────────

class Drawable(ABC):
    """Any class with a `draw()` method is considered Drawable — duck typing
    enforced by the ABC itself via __subclasshook__."""

    @abstractmethod
    def draw(self):
        ...

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Drawable:
            # If the class has a `draw` attribute, accept it
            if any("draw" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented  # ← Let normal checks continue


class Circle:
    """Never inherits from Drawable, but HAS a `draw` method."""
    def draw(self):
        return "Drawing a circle"

class Square:
    """Also has `draw` — also considered Drawable."""
    def draw(self):
        return "Drawing a square"

class Rock:
    """No `draw` method — NOT Drawable."""
    pass


# ─────────────────────────────────────────────
# SECTION 6 — Real-World: Plugin System
# ─────────────────────────────────────────────

class NotificationPlugin(ABC):
    """Base class for a notification plugin system."""

    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        ...

    @abstractmethod
    def validate_recipient(self, recipient: str) -> bool:
        ...

    def send_if_valid(self, recipient: str, message: str) -> str:
        """Template Method pattern — concrete method calls abstract ones."""
        if not self.validate_recipient(recipient):
            return f"Invalid recipient: {recipient}"
        success = self.send(recipient, message)
        return "Sent!" if success else "Failed to send"


class EmailPlugin(NotificationPlugin):
    def send(self, recipient: str, message: str) -> bool:
        print(f"📧 Email to {recipient}: {message}")
        return True

    def validate_recipient(self, recipient: str) -> bool:
        return "@" in recipient


class SMSPlugin(NotificationPlugin):
    def send(self, recipient: str, message: str) -> bool:
        print(f"📱 SMS to {recipient}: {message}")
        return True

    def validate_recipient(self, recipient: str) -> bool:
        return recipient.startswith("+") and len(recipient) >= 10


# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("--- Section 1: Basic ABC ---")
    stripe = StripeProcessor()
    print(stripe.charge(99.99))
    print(stripe.format_amount(99.99))  # Inherited concrete method

    try:
        broken = BrokenProcessor()
    except TypeError as e:
        print(f"Cannot instantiate: {e}")

    print("\n--- Section 2: Abstract Properties ---")
    dog = Dog()
    snake = Snake()
    print(dog.describe())
    print(snake.describe())

    print("\n--- Section 3: ABCMeta ---")
    impl = OldStyleImpl()
    print(impl.execute())
    print(f"Is ABC equivalent? {issubclass(type(OldStyleBase), type(ABC))}")

    print("\n--- Section 4: register() ---")
    tp = ThirdPartySerializer()
    print(f"isinstance check: {isinstance(tp, Serializer)}")
    print(f"issubclass check: {issubclass(ThirdPartySerializer, Serializer)}")
    print(f"Actual base classes: {ThirdPartySerializer.__bases__}")
    # Note: __bases__ does NOT include Serializer — it's virtual only

    print("\n--- Section 5: __subclasshook__ ---")
    print(f"Circle is Drawable? {issubclass(Circle, Drawable)}")
    print(f"Square is Drawable? {issubclass(Square, Drawable)}")
    print(f"Rock is Drawable?   {issubclass(Rock, Drawable)}")
    print(f"isinstance(Circle(), Drawable)? {isinstance(Circle(), Drawable)}")

    print("\n--- Section 6: Plugin System ---")
    email = EmailPlugin()
    sms = SMSPlugin()
    print(email.send_if_valid("user@example.com", "Hello!"))
    print(sms.send_if_valid("+1234567890", "Hey!"))
    print(sms.send_if_valid("123", "Bad number"))

# Output:
#   --- Section 1: Basic ABC ---
#   stripe_txn_<id>_99.99
#   $99.99
#   Cannot instantiate: Can't instantiate abstract class BrokenProcessor with abstract method refund
#
#   --- Section 2: Abstract Properties ---
#   I have 4 legs and go 'Woof'
#   I have 0 legs and go 'Hiss'
#
#   --- Section 3: ABCMeta ---
#   executed via ABCMeta style
#   Is ABC equivalent? True
#
#   --- Section 4: register() ---
#   isinstance check: True
#   issubclass check: True
#   Actual base classes: (<class 'object'>,)
#
#   --- Section 5: __subclasshook__ ---
#   Circle is Drawable? True
#   Square is Drawable? True
#   Rock is Drawable?   False
#   isinstance(Circle(), Drawable)? True
#
#   --- Section 6: Plugin System ---
#   📧 Email to user@example.com: Hello!
#   Sent!
#   📱 SMS to +1234567890: Hey!
#   Sent!
#   Invalid recipient: 123
# Why:
#   1. BrokenProcessor fails because it didn't implement `refund` — ABC
#      enforcement triggers at instantiation time, not at class definition.
#   2. Abstract properties use @property + @abstractmethod (property outer,
#      abstractmethod inner). Subclasses must redefine them as @property.
#   3. ABCMeta is the old-style equivalent of inheriting from ABC.
#   4. register() makes ThirdPartySerializer pass isinstance/issubclass
#      but __bases__ still shows (object,) — no real inheritance occurs.
#   5. __subclasshook__ makes Circle/Square "Drawable" via structural
#      check (duck typing enforced by ABC) — no inheritance needed.
#   6. Template Method pattern: concrete method `send_if_valid` calls
#      abstract `validate_recipient` and `send` — subclasses fill in the blanks.
