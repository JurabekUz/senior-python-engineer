"""
TOPIC: collections.deque
======================================================

WHAT IS IT?
  deque (Double-Ended Queue) is a list-like container with fast appends and pops 
  on either end. It is pronounced as "deck".

RULES / KEY POINTS:
  1. Thread-safe: Deques support thread-safe, memory efficient appends and pops.
  2. Performance: O(1) time complexity for appends and pops from both ends (vs O(n) for list.insert(0)).
  3. Max Length: Can be created with a fixed size using `maxlen`.
  4. Indexing: Supports indexing but is slower than lists for random access in the middle (O(n)).

COMMON PROBLEMS / PITFALLS:
  - Random Access: Accessing middle elements (e.g., `d[50]`) is O(n), while lists are O(1).
  - Removing by value: `remove()` is O(n).
  - Slicing: Deques do not support slicing directly (need to convert to list).

WHEN TO USE IT:
  - Implementing Queues (FIFO) or Stacks (LIFO).
  - Maintaining a "Moving Average" or "Recent History" using `maxlen`.
  - Breath-First Search (BFS) algorithms.

RELATED TOPICS:
  - queue.Queue (synchronized for multi-threading)
  - collections.defaultdict
  - list performance
"""

from collections import deque

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept
# ─────────────────────────────────────────────

# Initialization
d = deque(["apple", "banana", "cherry"])
print(f"Initial deque: {d}")

# Appending and Popping from both ends
d.append("date")          # Add to right
d.appendleft("elderberry") # Add to left
print(f"After appends: {d}")

right_item = d.pop()      # Remove from right
left_item = d.popleft()   # Remove from left
print(f"Popped: {right_item} and {left_item}")
print(f"Remaining: {d}")

# ─────────────────────────────────────────────
# SECTION 2 — Rotation and Extension
# ─────────────────────────────────────────────

# Rotate: move n steps to the right (if positive) or left (if negative)
d.rotate(1)
print(f"Rotated 1 step right: {d}")

d.rotate(-2)
print(f"Rotated 2 steps left: {d}")

# Extend and Extendleft
d.extend([1, 2])          # Adds multiple to right
d.extendleft([3, 4])      # Adds multiple to left (Note: reverses order)
print(f"After extensions: {d}")

# ─────────────────────────────────────────────
# SECTION 3 — Limited Size (maxlen)
# ─────────────────────────────────────────────

# A fixed-size deque automatically discards items from the opposite end
history = deque(maxlen=3)
history.append("page1")
history.append("page2")
history.append("page3")
print(f"Full history: {history}")

history.append("page4") # page1 is dropped
print(f"History after new item: {history}")

# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n--- Final Test ---")
    test_d = deque("abc")
    test_d.appendleft("z")
    print(f"Test result: {test_d}")
    
# Output:
#   Initial deque: deque(['apple', 'banana', 'cherry'])
#   After appends: deque(['elderberry', 'apple', 'banana', 'cherry', 'date'])
#   Popped: date and elderberry
#   Remaining: deque(['apple', 'banana', 'cherry'])
#   Rotated 1 step right: deque(['cherry', 'apple', 'banana'])
#   Rotated 2 steps left: deque(['banana', 'cherry', 'apple'])
#   After extensions: deque([4, 3, 'banana', 'cherry', 'apple', 1, 2])
#   Full history: deque(['page1', 'page2', 'page3'], maxlen=3)
#   History after new item: deque(['page2', 'page3', 'page4'], maxlen=3)
#
#   --- Final Test ---
#   Test result: deque(['z', 'a', 'b', 'c'])
# Why:
#   1. appendleft adds to the 0-th index.
#   2. extendleft(iterable) adds items one by one to the left, resulting in reverse order.
#   3. rotate(1) makes the last element the first.
#   4. maxlen ensures the size never exceeds the limit by "pushing out" old items.
