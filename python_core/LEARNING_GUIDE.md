# Python Core — Learning Guide

## File Template (used for every topic)

Each `.py` file follows this exact structure:

```
"""
TOPIC: <Topic Name>
======================================================

WHAT IS IT?
  Brief explanation of the concept.

RULES / KEY POINTS:
  1. Rule one
  2. Rule two
  3. ...

COMMON PROBLEMS / PITFALLS:
  - Pitfall 1: what goes wrong and why
  - Pitfall 2: ...

WHEN TO USE IT:
  - Real-world scenario

RELATED TOPICS:
  - Related concept 1
  - Related concept 2
"""

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept
# ─────────────────────────────────────────────

... code with inline comments ...

# ─────────────────────────────────────────────
# SECTION 2 — Advanced / Real-World Usage
# ─────────────────────────────────────────────

... code ...

# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

... test code ...

# Output:
#   <actual console output>
# Why: <explanation of why this output appears>
```

---

## Topic List & Progress

### Group 1 — Dunder (Magic) Methods
| # | File | Status |
|---|------|--------|
| 1 | `__hash__and__eq__.py` | ✅ Done |
| 2 | `__str__and__repr__.py` | ⬜ |
| 3 | `__call__.py` | ⬜ |
| 4 | `__getattr__and__setattr__.py` | ⬜ |
| 5 | `itertools_usage.py` | ✅ Done |
| 6 | `__new__.py` | ⬜ |
| 7 | `__add__and__sub__.py` | ⬜ |
| 8 | `__gt__and__lt__.py` | ⬜ |
| 9 | `__dict__.py` | ⬜ |
| 10 | `__dir__.py` | ⬜ |

### Group 2 — Functions & Scope
| # | File | Status |
|---|------|--------|
| 11 | `args_and_kwargs.py` | ⬜ |
| 12 | `decorators.py` | ✅ Done |
| 13 | `closures.py` | ⬜ |
| 14 | `inner_functions.py` | ⬜ |
| 15 | `legb_scope.py` | ⬜ |
| 16 | `global_and_nonlocal.py` | ⬜ |
| 17 | `generators.py` | ⬜ |
| 18 | `filter_map_reduce.py` | ⬜ |

### Group 3 — OOP Concepts
| # | File | Status |
|---|------|--------|
| 19 | `abc_abstract.py` | ⬜ |
| 20 | `property.py` | ⬜ |
| 21 | `class_attributes.py` | ⬜ |
| 22 | `inheritance_mro.py` | ⬜ |
| 23 | `diamond_problem.py` | ⬜ |
| 24 | `duck_typing.py` | ⬜ |
| 25 | `overloading.py` | ⬜ |

### Group 4 — Data Structures & Built-ins
| # | File | Status |
|---|------|--------|
| 26 | `collections_namedtuple.py` | ✅ Done |
| 27 | `enum.py` | ⬜ |
| 28 | `copy_shallow_deep.py` | ⬜ |
| 29 | `dict_keys_views.py` | ⬜ |
| 30 | `enumerate_zip.py` | ⬜ |
| 31 | `itertools_usage.py` | ✅ Done |
| 32 | `collections_counter.py` | ✅ Done |
| 33 | `collections_deque.py` | ✅ Done |
| 34 | `collections_defaultdict.py` | ✅ Done |

### Group 5 — Advanced Patterns
| # | File | Status |
|---|------|--------|
| 35 | `context_manager.py` | ⬜ |
| 36 | `typing_hints.py` | ⬜ |
| 37 | `dataclasses_core.py` | ✅ Done |
| 38 | `everything_is_object.py` | ⬜ |
| 39 | `assert.py` | ⬜ |

---

## Learning Workflow (per topic)

1. **Read** — understand what the concept is (5 min)
2. **Write** — create the `.py` file using the template above
3. **Run** — execute and verify console output matches comments
4. **Explain** — can you explain it in plain English? ✅ = you learned it
5. **Mark** — update status in this file

---

## Naming Convention

- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_CASE`
