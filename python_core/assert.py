"""
TOPIC: Assertions (`assert` statement)
======================================================

WHAT IS IT?
  The `assert` statement is a debugging aid that tests a condition. 
  If the condition is True, it does nothing and your program continues to execute. 
  If the condition is False, it raises an `AssertionError` with an optional error message.

RULES / KEY POINTS:
  1. Syntax: `assert condition, "Error message"`
  2. Assertions can be globally disabled by running Python with the `-O` (optimize) flag.
  3. Never use `assert` for data validation (e.g., checking user input) or for handling expected runtime errors.

COMMON PROBLEMS / PITFALLS:
  - Pitfall 1: Using parentheses for a tuple in assert: `assert(False, "Error")`. In Python 3, this evaluates as a tuple which is always True (if not empty), defeating the assert completely.
  - Pitfall 2: Using assert for security checks or business logic validation. If `-O` is used, the check is skipped!

WHEN TO USE IT:
  - For sanity checks, testing internal invariants, and verifying conditions that *should never happen* unless there's a bug in your code.
  - In unit tests (though frameworks like pytest provide richer assertion capabilities).

RELATED TOPICS:
  - Exceptions & Error Handling
  - Unit Testing (pytest)
"""

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept
# ─────────────────────────────────────────────

def calculate_discount(price, discount):
    # Sanity check: price and discount should be reasonable
    assert 0 <= discount <= 1, "Discount must be between 0 and 1"
    return price * (1 - discount)

# ─────────────────────────────────────────────
# SECTION 2 — Advanced / Real-World Usage
# ─────────────────────────────────────────────

class BankAccount:
    def __init__(self, balance):
        self.balance = balance
        
    def withdraw(self, amount):
        # We might use assertions for internal invariant checks
        assert self.balance >= 0, "Account balance somehow went negative!"
        
        if amount > self.balance:
            # Use exceptions for normal validation!
            raise ValueError("Insufficient funds")
            
        self.balance -= amount

# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print("Price after 20% discount:", calculate_discount(100, 0.2))
    
    try:
        calculate_discount(100, 1.5)
    except AssertionError as e:
        print("Assertion caught:", e)
        
    try:
        # Pitfall example: using a tuple always passes because (False, 'message') is a truthy tuple
        assert (False, "This assert never fails!")
        print("Tuple assert passed (this is the pitfall!).")
    except AssertionError:
        print("This won't print.")

# Output:
#   Price after 20% discount: 80.0
#   Assertion caught: Discount must be between 0 and 1
#   Tuple assert passed (this is the pitfall!).
# Why: The first call passes the assert. The second call violates it, triggering AssertionError. The third demonstrates the tuple trap where a non-empty tuple evaluates to True.
