"""
TOPIC: Magic Method - __call__
======================================================

WHAT IS IT?
  - The `__call__` magic method allows an instance of a class to be called 
    just like a regular function (e.g., `object()`).
  - Any object that implements the `__call__` method is known as a "callable" 
    and returns `True` when checked with the built-in `callable(object)` function.

RULES / KEY POINTS:
  1. Function-like Syntax: Defining `__call__(self, *args, **kwargs)` enables 
     calling an object directly: `instance(*args, **kwargs)`.
  2. Stateful Behavior: Unlike standard functions, callable objects can retain 
     state between calls across multiple executions since they are class instances.
  3. Signature Flexibility: `__call__` can accept any parameters, including 
     positional arguments (`*args`) and keyword arguments (`**kwargs`).

COMMON PROBLEMS / PITFALLS:
  - Pitfall 1: Attempting to call an instance of a class that does not implement 
    `__call__` will raise a `TypeError: 'MyClass' object is not callable`.
  - Pitfall 2: Overusing `__call__` can lead to unreadable code. If an object performs 
    multiple distinct operations, it is better to use descriptive method names 
    instead of making the object itself callable.

WHEN TO USE IT:
  - Useful for creating decorators that maintain state (e.g., counting function calls, 
    caching/memoization).
  - Used for defining function-like interfaces that require internal state or setup 
    (e.g., event dispatchers, mathematical functions like polynomial solvers).

RELATED TOPICS:
  - The built-in `callable()` function
  - Function decorators and closures
  - Stateful programming
"""

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept (Stateful Callable)
# ─────────────────────────────────────────────

# In this section, we build a simple class that counts how many times its instance 
# has been called. This demonstrates how a callable object can retain state.

class StatefulCounter:
    def __init__(self, increment: int = 1):
        self.increment = increment
        self.call_count = 0

    def __call__(self, *args, **kwargs) -> int:
        # Each time the object is called, we increment the count and return it
        self.call_count += self.increment
        return self.call_count


# ─────────────────────────────────────────────
# SECTION 2 — Advanced / Real-World Usage (Event Dispatcher / Callbacks)
# ─────────────────────────────────────────────

# Here, we create an Event class that inherits from list. 
# It holds a collection of listener/callback functions. 
# Calling the Event object triggers (calls) all the registered callbacks in order.

class Event(list):
    def __call__(self, *args, **kwargs):
        """
        Triggers all registered callbacks in this event list with the 
        provided arguments.
        """
        print(f"\n[Event Dispatcher] Triggering {len(self)} listener(s)...")
        for callback in self:
            callback(*args, **kwargs)


# Listener callbacks to register
def log_to_console(message: str):
    print(f"  [Console Listener] Received message: {message}")

def log_to_file(message: str):
    print(f"  [File Listener] Writing to log file: {message}")


def main():
    # --- Testing Section 1: Stateful Callable ---
    print("--- Section 1: Stateful Counter ---")
    counter = StatefulCounter(increment=5)
    
    # Check if the object is callable
    print(f"Is counter callable? {callable(counter)}")
    
    # Call the object multiple times
    print(f"First call: {counter()}")   # Returns 5
    print(f"Second call: {counter()}")  # Returns 10
    print(f"Third call: {counter()}")   # Returns 15
    print(f"Total times invoked: {counter.call_count // 5}")

    # --- Testing Section 2: Advanced Event Dispatcher ---
    print("\n--- Section 2: Event Dispatcher ---")
    # Instantiate the Event object (which acts as a list)
    user_signup_event = Event()

    # Register listeners by appending them to the event list
    user_signup_event.append(log_to_console)
    user_signup_event.append(log_to_file)

    # Triggering the event is as simple as calling the object!
    user_signup_event("User 'Jurabek' signed up successfully.")


# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == "__main__":
    main()

# Expected Output:
# --- Section 1: Stateful Counter ---
# Is counter callable? True
# First call: 5
# Second call: 10
# Third call: 15
# Total times invoked: 3
#
# --- Section 2: Event Dispatcher ---
#
# [Event Dispatcher] Triggering 2 listener(s)...
#   [Console Listener] Received message: User 'Jurabek' signed up successfully.
#   [File Listener] Writing to log file: User 'Jurabek' signed up successfully.
#
# Why:
#   1. The 'counter' object becomes callable because we implemented the '__call__' method.
#      It retains the count state in 'self.call_count' across calls.
#   2. The 'user_signup_event' object inherits from 'list' and stores callbacks.
#      When 'user_signup_event()' is called, its custom '__call__' method iterates 
#      through itself and invokes each callback function with the passed arguments.
