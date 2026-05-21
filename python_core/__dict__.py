"""
TOPIC: Namespace Introspection - The __dict__ Attribute (and vars() Function)
=============================================================================

WHAT IS IT?
  - In Python, `__dict__` is a dictionary (or dictionary-like mapping) that stores 
    an object's writable attributes.
  - Every user-defined class instance, class itself, and module in Python typically 
    has a `__dict__` attribute representing its namespace.
  - The built-in `vars()` function returns the `__dict__` attribute of any object 
    that has one.

RULES / KEY POINTS:
  1. Attribute Lookup: When you access an attribute (`obj.attr`), Python resolves 
     this under the hood by looking up `'attr'` in the `obj.__dict__` dictionary.
  2. Direct Mutation: You can add, modify, or delete instance attributes by directly 
     manipulating `instance.__dict__` (e.g., `obj.__dict__['x'] = 10` is equivalent to `obj.x = 10`).
  3. Class vs. Instance `__dict__`:
     - An **instance `__dict__`** is a standard, mutable Python `dict` containing 
       instance-specific variables.
     - A **class `__dict__`** is a read-only `mappingproxy` object containing class 
       variables, methods, and descriptors.
  4. vars() Function: Using `vars(obj)` is the official, Pythonic equivalent to `obj.__dict__`.
  5. The Slots Exception: If a class defines `__slots__`, its instances will not 
     have a `__dict__` attribute, saving memory by preventing dynamic attribute creation.

COMMON PROBLEMS / PITFALLS:
  - Pitfall 1: Attempting to modify class `__dict__` directly (e.g., `MyClass.__dict__['x'] = 5`) 
    will raise `TypeError: 'mappingproxy' object does not support item assignment`. 
    You must use `setattr(MyClass, 'x', 5)` or `MyClass.x = 5`.
  - Pitfall 2: Assuming every object has a `__dict__`. Built-in types (like `list`, `dict`, `str`) 
    and classes using `__slots__` do not have a `__dict__`.

WHEN TO USE IT:
  - Debugging: Instantly inspect all attributes and their current values.
  - Serialization: Easily convert an object's instance state into a dictionary for JSON serialization.
  - Dynamic Configuration: Hydrating objects from external data sources (e.g., databases, JSON configs) 
    by writing directly to the `__dict__`.

RELATED TOPICS:
  - `setattr()`, `getattr()`, `hasattr()`, `delattr()`
  - `__slots__` optimization
  - The built-in `vars()` function
"""

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept (Instance vs. Class Namespaces)
# ─────────────────────────────────────────────

class Product:
    category = "Electronics"  # Class-level attribute

    def __init__(self, name: str, price: float):
        self.name = name        # Instance-level attribute
        self.price = price      # Instance-level attribute

    def get_details(self) -> str:
        return f"{self.name}: ${self.price}"


def demonstrate_basic_namespaces():
    print("--- Section 1: Basic Concept ---")
    p1 = Product("Laptop", 999.99)
    p2 = Product("Smartphone", 599.99)

    # 1. View Instance __dict__ using direct access and vars()
    print("p1 dict:", p1.__dict__)
    print("p2 dict (via vars):", vars(p2))

    # 2. View Class __dict__ (stores class variables, methods, etc.)
    # Note: It returns a 'mappingproxy', not a regular dict!
    print("Product Class dict type:", type(Product.__dict__))
    print("Product Class category in dict:", Product.__dict__['category'])


# ─────────────────────────────────────────────
# SECTION 2 — Advanced Usage (Dynamic Mutation & Optimization)
# ─────────────────────────────────────────────

# Custom dynamic config loader example using __dict__
class Config:
    def __init__(self, **kwargs):
        # Directly update the instance namespace with external options
        self.__dict__.update(kwargs)


# Memory-optimized class using __slots__ (No __dict__ created)
class OptimizedPoint:
    __slots__ = ('x', 'y')  # Restricts attributes to 'x' and 'y'

    def __init__(self, x, y):
        self.x = x
        self.y = y


def demonstrate_advanced_namespaces():
    print("\n--- Section 2: Advanced Usage ---")
    
    # 1. Dynamic attribute modification via __dict__
    p = Product("Tablet", 299.99)
    print("Before dynamic update:", p.price)
    
    # Mutating attribute by directly writing to the dictionary namespace
    p.__dict__['price'] = 249.99
    # Dynamically adding a brand attribute
    p.__dict__['brand'] = "Pear"

    print("After dynamic update (price):", p.price)
    print("After dynamic update (brand):", p.brand)
    print("Final p dict:", p.__dict__)

    # 2. Attempting to write to Class __dict__ directly raises a TypeError
    try:
        Product.__dict__['category'] = "Smart Home"
    except TypeError as e:
        print(f"Expected Error when mutating class dict: {e}")

    # Correct way to mutate class attribute
    Product.category = "Smart Home"
    print("Updated category:", Product.category)

    # 3. Dynamic Configuration Loading
    settings = {"theme": "dark", "volume": 80, "debug": True}
    config = Config(**settings)
    print("Config volume:", config.volume)
    print("Config dict:", config.__dict__)

    # 4. Slots optimization (No __dict__ available)
    op = OptimizedPoint(10, 20)
    print("OptimizedPoint x, y:", op.x, op.y)
    try:
        print("op __dict__:", op.__dict__)
    except AttributeError as e:
        print(f"Expected Attribute Error with slots: {e}")


def main():
    demonstrate_basic_namespaces()
    demonstrate_advanced_namespaces()


# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == '__main__':
    main()

# Expected Output:
# --- Section 1: Basic Concept ---
# p1 dict: {'name': 'Laptop', 'price': 999.99}
# p2 dict (via vars): {'name': 'Smartphone', 'price': 599.99}
# Product Class dict type: <class 'mappingproxy'>
# Product Class category in dict: Electronics
#
# --- Section 2: Advanced Usage ---
# Before dynamic update: 299.99
# After dynamic update (price): 249.99
# After dynamic update (brand): Pear
# Final p dict: {'name': 'Tablet', 'price': 249.99, 'brand': 'Pear'}
# Expected Error when mutating class dict: 'mappingproxy' object does not support item assignment
# Updated category: Smart Home
# Config volume: 80
# Config dict: {'theme': 'dark', 'volume': 80, 'debug': True}
# OptimizedPoint x, y: 10 20
# Expected Attribute Error with slots: 'OptimizedPoint' object has no attribute '__dict__'
#
# Why:
#   1. Instance attributes are stored in a regular dictionary ('__dict__') which is mutable.
#   2. The class attributes and methods are stored in a read-only 'mappingproxy' to maintain integrity.
#   3. Using '__slots__' disables the automatic creation of '__dict__', reducing memory usage 
#      and preventing dynamic creation of new attributes.
