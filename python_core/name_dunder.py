"""
TOPIC: The __name__ Variable
======================================================

WHAT IS IT?
  `__name__` is a built-in variable in Python that evaluates to the name of the 
  current module. However, if a module is being run directly, `__name__` is 
  set to the string "__main__".

RULES / KEY POINTS:
  1. If you run a file directly: `__name__ == "__main__"`.
  2. If you import a file: `__name__ == "filename"`.
  3. The `if __name__ == "__main__":` block is used to prevent code from 
     executing when the file is imported as a module.

COMMON PROBLEMS / PITFALLS:
  - Forgetting the block: Code like database connections or API calls might 
    trigger unexpectedly when you just wanted to import a single function.
  - Typo in "__main__": If you type `"_main_"` (one underscore), it won't work.

WHEN TO USE IT:
  - To provide a script entry point (the 'start' of your app).
  - To include tests or example usage inside a module file.
  - To make a file both a reusable module and a runnable script.

RELATED TOPICS:
  - Modules and Packages
  - Import System
  - Entry Points
"""

# ─────────────────────────────────────────────
# SECTION 1 — Basic Concept
# ─────────────────────────────────────────────

def say_hello():
    print("Hello from name_dunder.py!")

print(f"Module level print: My name is {__name__}")

if __name__ == "__main__":
    print("--- Execution started directly ---")
    say_hello()
    print("This code ONLY runs if you execute this file directly.")
else:
    print(f"--- Execution started via IMPORT in {__name__} ---")

# ─────────────────────────────────────────────
# SECTION 2 — Practical Demonstration
# ─────────────────────────────────────────────

# To see this in action, we need another file. 
# I will create 'name_importer.py' which imports this file.

# ─────────────────────────────────────────────
# TESTS — Expected output explained
# ─────────────────────────────────────────────

# If run directly (python name_dunder.py):
# Output:
#   Module level print: My name is __main__
#   --- Execution started directly ---
#   Hello from name_dunder.py!
#   This code ONLY runs if you execute this file directly.

# If imported (import name_dunder):
# Output:
#   Module level print: My name is name_dunder
#   --- Execution started via IMPORT in name_dunder ---
