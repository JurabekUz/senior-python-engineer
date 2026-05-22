"""
TOPIC: Magic Method - __dir__ (and the dir() Function)
======================================================

WHAT IS IT?
  - `__dir__` is a magic method in Python that is implicitly called when the 
    built-in `dir()` function is invoked on an object.
  - By defining custom `__dir__()` behavior, a class can explicitly control the 
    sorted list of attribute names that are returned by `dir()`.

RULES / KEY POINTS:
  1. Default Behavior: By default, `dir()` retrieves all accessible instance variables, 
     class variables, methods, and parent-class dunder methods via inheritance.
  2. Customizing Discovery: Defining `__dir__(self)` must return a sequence (like a `list` 
     or `tuple`) of strings representing the names of the attributes/methods.
  3. Autocomplete Integration: Popular interactive shells, REPLs, and IDEs use `dir()` 
     under the hood for autocompletion (tab-completion).
  4. Complete Freedom: The names returned by `__dir__()` do not strictly have to exist 
     as physical attributes on the object—they can be dynamic or virtual fields.

COMMON PROBLEMS / PITFALLS:
  - Pitfall 1: Returning non-string elements. The sequence returned by `__dir__()` 
    must consist entirely of strings; otherwise, `dir()` raises a `TypeError`.
  - Pitfall 2: Over-filtering. If you implement `__dir__()` and forget to include 
    standard properties or class methods (like `super().__dir__()`), developers 
    will lose autocomplete for standard, valid methods.

WHEN TO USE IT:
  - Dynamic Proxies: When delegating attribute lookups to another object (e.g., in a 
    Wrapper or Proxy pattern) and wanting the proxy to advertise the wrapped object's attributes.
  - Custom ORMs / JSON Models: When attributes are fetched dynamically from a database schema 
    or external API payload, and you want them to be discoverable by IDE autocomplete tools.

RELATED TOPICS:
  - The built-in `dir()` and `vars()` functions
  - Attribute access methods: `__getattr__`, `__getattribute__`
  - Dynamic developer experiences (DX)
"""

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept (Customizing dir() Output)
# ─────────────────────────────────────────────

# In this section, we build a simple class that overrides __dir__ to return a 
# custom list of names. This shows how dir() calls __dir__() internally.

class SimpleCustomDirectory:
    def __init__(self, key: str, val: str):
        self.key = key
        self.val = val

    # Control what dir(instance) returns
    def __dir__(self) -> list:
        # We can return an arbitrary list of strings!
        return ["custom_attribute_1", "custom_attribute_2", "key", "val"]


# ─────────────────────────────────────────────
# SECTION 2 — Advanced / Real-World Usage (Dynamic Autocomplete for ORM Model)
# ─────────────────────────────────────────────

# Here, we create an ORM-like DynamicRecord class.
# It holds database schema keys and values in a private dictionary.
# We override __getattr__ to resolve dynamic field access.
# We override __dir__ to merge standard class attributes with the dynamic schema keys,
# giving IDE autocomplete tools a seamless discoverability experience.

class DynamicRecord:
    def __init__(self, schema_fields: list, data: dict):
        self._fields = schema_fields
        self._data = data

    # 1. Catch-all for dynamic attribute access (e.g., record.email)
    def __getattr__(self, name: str):
        if name in self._fields:
            return self._data.get(name, None)
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")

    # 2. Custom __dir__ merging standard class metadata with dynamic keys
    def __dir__(self) -> list:
        # Get standard class attributes (like __init__, __getattr__, self._fields, etc.)
        standard_attrs = list(super().__dir__())
        # Return standard attributes combined with our dynamic database fields
        return standard_attrs + self._fields


def main():
    # --- Testing Section 1: Custom Directory ---
    print("--- Section 1: Simple Custom __dir__ ---")
    simple_obj = SimpleCustomDirectory("username", "jurabek")
    
    # Normally dir() would return standard methods like __init__, __class__, etc.
    # But now it returns exactly what we defined in __dir__()!
    print("dir() on simple_obj:", dir(simple_obj))
    print("Has physical 'custom_attribute_1'? :", hasattr(simple_obj, "custom_attribute_1"))

    # --- Testing Section 2: Dynamic ORM Autocomplete ---
    print("\n--- Section 2: Dynamic ORM Autocomplete ---")
    columns = ["id", "email", "role", "is_verified"]
    row_data = {"id": 42, "email": "jurabek@faang.com", "role": "Senior Engineer"}

    user_record = DynamicRecord(schema_fields=columns, data=row_data)

    # 1. Introspection via dir()
    available_names = dir(user_record)
    print("Is dynamic column 'email' discoverable via dir()? :", "email" in available_names)
    print("Is dynamic column 'role' discoverable via dir()? :", "role" in available_names)
    print("Is dynamic column 'is_verified' discoverable via dir()? :", "is_verified" in available_names)

    # 2. Dynamic access works seamlessly
    print("\nDynamic Property Access:")
    print(f"  User ID: {user_record.id}")
    print(f"  User Email: {user_record.email}")
    print(f"  User Role: {user_record.role}")
    print(f"  Is Verified: {user_record.is_verified}")


# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == '__main__':
    main()

# Expected Output:
# --- Section 1: Simple Custom __dir__ ---
# dir() on simple_obj: ['custom_attribute_1', 'custom_attribute_2', 'key', 'val']
# Has physical 'custom_attribute_1'? : False
#
# --- Section 2: Dynamic ORM Autocomplete ---
# Is dynamic column 'email' discoverable via dir()? : True
# Is dynamic column 'role' discoverable via dir()? : True
# Is dynamic column 'is_verified' discoverable via dir()? : True
#
# Dynamic Property Access:
#   User ID: 42
#   User Email: jurabek@faang.com
#   User Role: Senior Engineer
#   Is Verified: None
#
# Why:
#   1. In Section 1, calling dir() directly executed 'SimpleCustomDirectory.__dir__()',
#      returning our exact custom list, overriding standard dunder introspection.
#   2. In Section 2, the 'user_record' object holds dynamic properties inside its schema.
#      By combining super().__dir__() with 'self._fields' inside our custom '__dir__()',
#      the dynamic database attributes are successfully advertised to autocomplete systems.
#   3. '__getattr__' intercepts calls to 'user_record.email', pulling the value 
#      directly from 'self._data'.
