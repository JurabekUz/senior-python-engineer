# FAANG Interview Internals: Python Namespaces, Memory Optimization & Autocomplete Customization

When interviewing for Senior, Staff, or Principal Engineer roles at FAANG/Big Tech companies, interviews rarely test rote memorization of Python built-ins. Instead, they evaluate your **deep understanding of Python internals** to solve real-world scale, performance, and architecture problems.

This guide explores the internal mechanics of `__dict__` vs `dir()`, how they are tested in high-level engineering interviews, and how to use them for memory optimization and dynamic system design.

---

## 1. Deep Dive: `__dict__` vs `dir()`

Understanding how Python represents objects under the hood is fundamental to high-performance programming.

| Criterion | `__dict__` (and `vars()`) | `dir()` (and `__dir__()`) |
| :--- | :--- | :--- |
| **What is it?** | A dictionary (`dict`) storing the object's writable namespace. | A built-in function returning a sorted list of all accessible attribute/method names. |
| **Data Type** | `dict` (or `mappingproxy` for classes). | `list` of strings. |
| **Content** | Only **direct instance attributes** and their values (`key: value`). | **All** names available on the object (instance attributes, class attributes, methods, and inherited magic methods). |
| **Scope** | Local to the instance. Does not show inherited class methods unless overridden. | Global to the object's hierarchy. Shows all inherited methods from parent classes and the base `object`. |
| **Mutability** | **Mutable** for instances. You can write directly to it to dynamically assign attributes. | **Immutable**. It is a temporary list; modifying the list does not affect the object. |
| **Memory footprint** | High (creates a hash table for every single instance). | None (generated dynamically on-demand). |
| **`__slots__` Exception** | Disappeared/non-existent if `__slots__` is defined. | Still works perfectly and includes slot variables in the returned list. |

### Visual Representation of Object Namespace Resolution
When you request `obj.attribute`, CPython resolves it in the following conceptual path:
```
[Access obj.attribute]
         │
         ├───> 1. Search in Instance Namespace: obj.__dict__['attribute'] (If exists -> Return)
         │
         ├───> 2. Search in Class Namespace: obj.__class__.__dict__['attribute'] (If exists -> Return)
         │
         └───> 3. Search in Base Classes (MRO): Parent.__dict__['attribute'] (If exists -> Return)
                 │
                 └───> Otherwise: Raise AttributeError
```

---

## 2. FAANG Interview Scenario 1: Extreme Memory Optimization (`__slots__`)

### The Interview Problem
> *"We have a high-throughput Python service running in production that processes millions of `UserCoordinate` objects simultaneously. The service is running out of memory (OOM), and our infrastructure costs are skyrocketing. How would you optimize the memory footprint of these objects at the Python language level?"*

### The Architectural Solution
By default, Python is highly dynamic, creating a `__dict__` dictionary for every user-defined class instance. A Python dictionary is a hash table that requires significant memory overhead (minimum 100-200 bytes per object just to maintain the dictionary hash structure, even when empty).

If we define `__slots__` on our class, CPython stores instance variables in a highly optimized, fixed-size flat array instead of a dictionary. This **completely eliminates the `__dict__` attribute** for the instance, saving up to 50-60% of RAM.

### Implementation and Measurement Demo

```python
import sys

# Standard dynamic class (Creates __dict__ for every instance)
class DynamicUser:
    def __init__(self, user_id: int, username: str):
        self.user_id = user_id
        self.username = username

# Memory-optimized class (No __dict__ created)
class OptimizedUser:
    __slots__ = ('user_id', 'username')  # Pre-allocates memory for these attributes only

    def __init__(self, user_id: int, username: str):
        self.user_id = user_id
        self.username = username


def run_memory_demo():
    u_dynamic = DynamicUser(101, "jurabek")
    u_optimized = OptimizedUser(101, "jurabek")

    # 1. Inspect namespace differences
    print("Dynamic User Namespace:", u_dynamic.__dict__)
    try:
        print("Optimized User Namespace:", u_optimized.__dict__)
    except AttributeError:
        print("Optimized User has NO __dict__ attribute! Memory is saved.")

    # 2. Compare RAM overhead
    # Note: sys.getsizeof() only measures the base object size.
    # For a dynamic object, we must add the size of its __dict__ namespace dictionary.
    dynamic_size = sys.getsizeof(u_dynamic) + sys.getsizeof(u_dynamic.__dict__)
    optimized_size = sys.getsizeof(u_optimized)

    print(f"Dynamic Object Memory Footprint: {dynamic_size} bytes")
    print(f"Optimized Object Memory Footprint: {optimized_size} bytes")
    print(f"Memory Saved per Object: {((dynamic_size - optimized_size) / dynamic_size) * 100:.1f}%")

if __name__ == '__main__':
    run_memory_demo()
```

---

## 3. FAANG Interview Scenario 2: Dynamic API & ORM Design (Customizing `__dir__`)

### The Interview Problem
> *"We are building a custom ORM (Object-Relational Mapper) or an API Gateway client that fetches fields dynamically from a remote database/service. When developers work with our objects in an interactive environment (like a Jupyter Notebook or a Python REPL), they want tab-completion (autocomplete) to show all the dynamically available fields, even though they aren't standard class attributes. How do you implement this?"*

### The Architectural Solution
Built-in autocomplete tools, debuggers, and REPLs use the `dir()` function to discover available attributes of an object. Under the hood, calling `dir(obj)` triggers `obj.__dir__()`.

By overriding the `__dir__()` magic method, we can combine our static class attributes/methods with **dynamic keys** (e.g., columns fetched from a database schema) and return a unified list. This provides a premium developer experience with fully functional autocomplete!

### Implementation Demo

```python
class DynamicModel:
    def __init__(self, db_schema: list, db_values: dict):
        self._schema = db_schema  # Dynamic attributes allowed
        self._values = db_values  # Actual data stored

    # 1. Custom attribute lookup (How we fetch dynamic values)
    def __getattr__(self, name):
        if name in self._schema:
            return self._values.get(name, None)
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")

    # 2. Custom directory discovery (How we customize autocomplete!)
    def __dir__(self):
        # Start with standard attributes & methods defined in the class
        standard_attributes = list(super().__dir__())
        # Append our dynamic schema fields
        return standard_attributes + self._schema


def run_orm_demo():
    # Suppose we fetch this schema and data from a database dynamically
    columns = ['id', 'email', 'joined_date', 'is_active']
    record = {'id': 99, 'email': 'jurabek@example.com', 'is_active': True}

    user_model = DynamicModel(db_schema=columns, db_values=record)

    # Autocomplete / Directory discovery works flawlessly!
    discovered_names = dir(user_model)
    print("\nAre dynamic columns discoverable via dir()?")
    print("  'email' in dir():", 'email' in discovered_names)
    print("  'is_active' in dir():", 'is_active' in discovered_names)

    # Accessing them works dynamically too!
    print("\nDynamic Access:")
    print("  User ID:", user_model.id)
    print("  User Email:", user_model.email)

if __name__ == '__main__':
    run_orm_demo()
```

---

## 4. Key Takeaways for Senior Engineers

1. **Understand Python's Internal Resolvers:** `__dict__` is the storage engine; `dir()` is the discovery map.
2. **Be Mindful of Overhead:** Keep objects simple. If you are creating millions of small record-like objects, always define `__slots__`.
3. **Control Introspection:** Customize developer tools, SDKs, and ORMs by overriding `__dir__()` so they feel clean and supportive to work with.
