"""
TOPIC: Everything is an Object
======================================================

WHAT IS IT?
  In Python, literally everything is an object. This includes numbers, strings, functions, modules, and even classes themselves.
  Since they are objects, they can be assigned to variables, passed as arguments, and returned from functions (First-class citizens).

RULES / KEY POINTS:
  1. All objects inherit from the base `object` class.
  2. Functions are objects (instances of the `function` class).
  3. Classes are objects (instances of the `type` class or a custom metaclass).
  4. You can inspect any object using `dir()`, `type()`, and `id()`.

COMMON PROBLEMS / PITFALLS:
  - Pitfall 1: Mutating default arguments (like `def foo(l=[]):`). Since the function is an object created once, its default argument object persists across calls.
  - Pitfall 2: Confusing class attributes with instance attributes, since the class itself is an object that holds its own state.

WHEN TO USE IT:
  - Understanding this is crucial for advanced Python programming, such as writing decorators, metaprogramming, and functional paradigms.

RELATED TOPICS:
  - First-Class Functions
  - Metaclasses
  - Memory Management (Garbage Collection)
"""

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept
# ─────────────────────────────────────────────

def simple_function():
    return "I am a function"

# Functions can be assigned to variables
func_alias = simple_function

# Functions have attributes like any other object
simple_function.custom_attr = "I attached data to a function!"

# ─────────────────────────────────────────────
# SECTION 2 — Advanced / Real-World Usage
# ─────────────────────────────────────────────

# Classes are objects too
class MyClass:
    pass

# We can pass the class itself (not an instance) to a function
def instantiate_class(cls):
    print(f"Instantiating {cls.__name__}...")
    return cls()

obj = instantiate_class(MyClass)

# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print("Function call via alias:", func_alias())
    print("Function custom attribute:", simple_function.custom_attr)
    print("Type of function:", type(simple_function))
    print("Type of MyClass:", type(MyClass))
    print("Type of 42:", type(42))

# Output:
#   Function call via alias: I am a function
#   Function custom attribute: I attached data to a function!
#   Type of function: <class 'function'>
#   Instantiating MyClass...
#   Type of MyClass: <class 'type'>
#   Type of 42: <class 'int'>
# Why: Every entity in Python, whether a primitive number, a function, or a class blueprint, is an instance of some fundamental class (like `int`, `function`, or `type`).
