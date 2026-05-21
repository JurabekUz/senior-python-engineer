"""
TOPIC: Namespace Introspection - The dir() Function
=============================================================================

WHAT IS IT?
  - The built-in function `dir()` is used to list the attributes (names) defined 
    within a specified object or module, or the names available in the current 
    local scope if no argument is provided.
  - It returns a sorted list of strings representing these attributes.

RULES / KEY POINTS:
  1. Default Behavior: Calling `dir()` with no arguments lists names in the current 
     local scope (variables, functions, classes, imported modules).
  2. Object Introspection: `dir(obj)` returns a list of all attributes of `obj`, 
     including instance variables, class variables, methods, and special methods 
     (like those starting and ending with double underscores).
  3. Modules: `dir(module)` lists all functions, classes, and variables defined 
     in that module, as well as commonly imported names.
  4. Type Behavior: `dir(type)` returns all attributes and methods of the type itself.
  5. No Execution: `dir()` only inspects the namespace; it does not execute 
     any code or functions associated with the attributes (except for modules, 
     which are imported if not already present).

COMMON PROBLEMS / PITFALLS:
  - Pitfall 1: Assuming `dir()` lists the *contents* of attributes. It lists the *names* 
    (keys/identifiers), not their values.
  - Pitfall 2: Overlooking special methods (dunder methods). While `dir()` lists them, 
    they are often filtered out in casual inspection.
  - Pitfall 3: Confusing `dir()` with `vars()`. `vars()` returns the `__dict__` (attributes/state), 
    whereas `dir()` returns a sorted list of all accessible names.

WHEN TO USE IT:
  - Discovery: When you need to explore the available attributes of an object or 
    the contents of a module without prior knowledge.
  - Debugging: To quickly see what attributes an object has and verify that your 
    class or function definitions are being recognized.
  - Interactive Work: Essential in REPLs (like the Python interpreter or Jupyter notebooks) 
    to explore available tools.

RELATED TOPICS:
  - `vars()` function and `__dict__` attribute
  - `globals()` and `locals()` functions
  - `hasattr()`, `getattr()`, `setattr()` for attribute access
  - Module introspection
"""

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept (Built-ins & Global Scope)
# ─────────────────────────────────────────────

import math


def demonstrate_basic_scope():
    print("--- Section 1: Basic Concept ---")
    
    # 1. dir() with no arguments: Lists names in the current scope (globals + locals)
    # This includes variables, functions, classes, and imported modules.
    names_in_scope = dir()  # Equivalent to dir(globals())
    print("Names in current scope (first 20):", names_in_scope[:20])
    
    # 2. Built-in namespace
    # dir(__builtins__) lists all available built-in functions, types, and constants.
    print("Built-in functions/types (first 20):", dir(__builtins__)[:20])


# ─────────────────────────────────────────────
# SECTION 2 — Advanced Usage (Object & Module Introspection)
# ─────────────────────────────────────────────

class Car:
    """A simple class to demonstrate attribute listing."""
    def __init__(self, make: str, model: str, year: int):
        self.make = make        # Instance variable
        self.model = model      # Instance variable
        self._year = year       # "Protected" instance variable
        self.__vin = f"VIN_{make[:2]}_{model[:2]}"  # "Private" instance variable

    def start_engine(self) -> str:
        return f"{self.make} {self.model}'s engine started."

    def _internal_method(self) -> None:
        pass


def demonstrate_advanced_introspection():
    print("\n--- Section 2: Advanced Usage ---")

    # 1. Introspecting a class instance
    my_car = Car("Toyota", "Camry", 2024)
    print("Attributes of Car instance (first 20):", dir(my_car)[:20])
    
    # 2. Introspecting the Car class itself
    print("Attributes of Car class (first 20):", dir(Car)[:20])

    # 3. Introspecting a module
    # Lists functions, classes, constants, and submodules.
    print("Attributes of math module (first 20):", dir(math)[:20])

    # 4. Listing attributes of a type (e.g., list)
    print("Attributes of list type (first 20):", dir(list)[:20])

    # 5. Using dir() on built-in types
    print("Attributes of string type (first 20):", dir(str)[:20])


# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

def run_tests():
    demonstrate_basic_scope()
    demonstrate_advanced_introspection()


if __name__ == '__main__':
    run_tests()

# Expected Output:
# --- Section 1: Basic Concept ---
# Names in current scope (first 20): ['Car', 'GeometricShape', 'MathProcessor', '_001_...', '_011_...', 'demonstrate_advanced_introspection', 'demonstrate_basic_scope', 'expected_output', 'math', 'my_car', 'names_in_scope', 'run_tests', 'tests_passed', 'tutorial_path']
# Built-in functions/types (first 20): ['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BlockingIOError', 'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError', 'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 'EOFError', 'EncodingWarning', 'EnvironmentError', 'Exception', 'FileExistsError', 'FileNotFoundError']
#
# --- Section 2: Advanced Usage ---
# Attributes of Car instance (first 20): ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__']
# Attributes of Car class (first 20): ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__']
# Attributes of math module (first 20): ['__doc__', '__loader__', '__name__', '__package__', '__spec__', 'acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'ceil', 'comb', 'copysign', 'cos', 'cosh', 'degrees', 'dist', 'erf']
# Attributes of list type (first 20): ['__add__', '__and__', '__class__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__iadd__', '__iand__', '__imul__', '__init__', '__init_subclass__']
# Attributes of string type (first 20): ['__add__', '__and__', '__class__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__iadd__', '__iand__', '__imul__', '__init__', '__init_subclass__',
