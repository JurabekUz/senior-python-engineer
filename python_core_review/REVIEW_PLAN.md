# Python Core — Review & Interview Preparation Plan

> **Goal:** Reinforce all 41 completed topics to interview-ready level.
> **Pace:** 15-20 minutes daily (in parallel with concurrency studies).
> **Format:** For each topic — question → think → write code → verify answer.

---

## Review Schedule (3-Week Cycle)

### Week 1 — Dunder Methods + Functions & Scope
| Day | Topics | File |
|-----|--------|------|
| Mon | `__hash__`, `__eq__`, `__str__`, `__repr__` | `week1_day1.py` |
| Tue | `__call__`, `__new__`, `__getattr__`, `__setattr__` | `week1_day2.py` |
| Wed | `__add__`, `__sub__`, `__gt__`, `__lt__`, `__dict__`, `__dir__` | `week1_day3.py` |
| Thu | `decorators`, `closures`, `inner_functions` | `week1_day4.py` |
| Fri | `args_kwargs`, `legb_scope`, `global_nonlocal`, `generators` | `week1_day5.py` |

### Week 2 — OOP Concepts + Data Structures
| Day | Topics | File |
|-----|--------|------|
| Mon | `abc_abstract`, `property`, `class_attributes` | `week2_day1.py` |
| Tue | `inheritance_mro`, `diamond_problem`, `super()` | `week2_day2.py` |
| Wed | `duck_typing`, `overloading`, `descriptors` | `week2_day3.py` |
| Thu | `namedtuple`, `enum`, `counter`, `deque`, `defaultdict` | `week2_day4.py` |
| Fri | `copy_shallow_deep`, `dict_views`, `enumerate_zip`, `itertools` | `week2_day5.py` |

### Week 3 — Advanced Patterns + Mixed Interview
| Day | Topics | File |
|-----|--------|------|
| Mon | `context_manager`, `typing_hints`, `dataclasses` | `week3_day1.py` |
| Tue | `everything_is_object`, `name_dunder`, `assert` | `week3_day2.py` |
| Wed | `filter_map_reduce` + mixed dunder questions | `week3_day3.py` |
| Thu | **Mock Interview #1** — 10 mixed questions (45 min) | `mock_interview_1.py` |
| Fri | **Mock Interview #2** — Real-world design problems | `mock_interview_2.py` |

---

## Question Formats

Each `.py` file contains 3 types of questions:

### 1. 🧠 "What's the Output?" (Output Prediction)
```python
# Read the code and predict the output. Then run it to verify.
class A:
    x = []
a1, a2 = A(), A()
a1.x.append(1)
print(a2.x)  # ???
```

### 2. 🐛 "Find the Bug" (Bug Hunt)
```python
# This code has a bug. Find it and fix it.
class Config:
    def __init__(self):
        self.debug = False
    
    @property
    def debug(self):
        return self.debug  # ← Bug: infinite recursion
```

### 3. 🏗️ "Design It" (Real-World Design)
```
Problem: Build a plugin system.
- Every plugin MUST implement an `execute()` method
- Plugins are registered and run sequentially
- Adding a new plugin should require ZERO changes to existing code
→ Which patterns are needed? ABC? Decorator? Registry?
```

---

## Resources & Question Banks

### 📚 Core Books
| Book | Relevant Chapters | Why |
|------|-------------------|-----|
| **Fluent Python** (Luciano Ramalho, 2nd ed) | Ch 1, 9-13, 15-17, 22-24 | Descriptors, MRO, duck typing, operator overloading — the deepest source |
| **Python Tricks** (Dan Bader) | All (short book) | Each trick = 1 interview question |
| **Effective Python** (Brett Slatkin, 3rd ed) | Items 26-43 (Classes), 36-38 (Generators) | Best practices + antipatterns |

### 🌐 Online Resources
| Resource | Link | How to Use |
|----------|------|-----------|
| **RealPython** | realpython.com | Read articles on `MRO`, `descriptors`, `metaclass`, `super()` |
| **Python docs — Data Model** | docs.python.org/3/reference/datamodel.html | Official dunder methods reference |
| **Python docs — HOWTOs** | docs.python.org/3/howto/descriptor.html | Full descriptor protocol explanation |
| **mCoding (YouTube)** | youtube.com/@mCoding | `super()`, MRO, `__init_subclass__` videos — best explanations |
| **ArjanCodes (YouTube)** | youtube.com/@ArjanCodes | OOP design patterns, SOLID, code smells |

### 💻 Interactive Platforms
| Platform | Why |
|----------|-----|
| **LeetCode** (Python tagged, Medium) | OOP + data structure problems |
| **Exercism — Python track** | Dedicated exercises for each concept |
| **HackerRank — Python domain** | Classes, Closures, Decorators sections |

### 📝 Interview Question Collections
| Resource | Link/Notes |
|----------|-----------|
| **awesome-interview-questions (GitHub)** | github.com/DopplerHQ/awesome-interview-questions#python |
| **python-interview-questions (GitHub)** | github.com/learning-zone/python-interview-questions |
| **Real Python — Interview Questions** | realpython.com/python-interview-problems |

---

## Daily Review Routine (15-20 min)

```
1. [3 min]  — Solve 1 "What's the Output?" question from yesterday's topic
2. [5 min]  — Re-read today's topic .py file (from python_core/)
3. [7 min]  — Solve 2-3 problems from today's review file
4. [3 min]  — Explain to yourself: "What is this concept and when do I use it?"
```

---

## Progress Tracking

### Week 1
| Day | File | Status |
|-----|------|--------|
| Mon | `week1_day1.py` | ⬜ |
| Tue | `week1_day2.py` | ⬜ |
| Wed | `week1_day3.py` | ⬜ |
| Thu | `week1_day4.py` | ⬜ |
| Fri | `week1_day5.py` | ⬜ |

### Week 2
| Day | File | Status |
|-----|------|--------|
| Mon | `week2_day1.py` | ⬜ |
| Tue | `week2_day2.py` | ⬜ |
| Wed | `week2_day3.py` | ⬜ |
| Thu | `week2_day4.py` | ⬜ |
| Fri | `week2_day5.py` | ⬜ |

### Week 3
| Day | File | Status |
|-----|------|--------|
| Mon | `week3_day1.py` | ⬜ |
| Tue | `week3_day2.py` | ⬜ |
| Wed | `week3_day3.py` | ⬜ |
| Thu | `mock_interview_1.py` | ⬜ |
| Fri | `mock_interview_2.py` | ⬜ |

---

## Rules

1. **Don't look at the answer first** — write your solution, then verify
2. **Set a timer** — 3-5 minutes per problem, don't spend more
3. **Explain out loud** — "rubber duck debugging" — say what you understand
4. **Making mistakes is good** — understanding the mistake = learning
5. **Run in parallel with concurrency** — 15 min review before today's new topic
