"""
Clean Code - Topic 2: Use Searchable Names & Avoid Mental Mapping

We will read more code than we will ever write. It's important that
the code we do write is readable and searchable. Make your names searchable
and don't force the reader to translate what a variable means.
"""

# ============================================================
# PART 1: Use Searchable Names
# ============================================================
#
# By NOT naming variables that end up being meaningful for
# understanding our program, we hurt our readers.
# Make your names searchable.

# ❌ BAD
import time

# What is the number 86400 for again?
time.sleep(86400)


# ✅ GOOD
import time

# Declare them in the global namespace for the module.
SECONDS_IN_A_DAY = 60 * 60 * 24
time.sleep(SECONDS_IN_A_DAY)

# Why is this better?
#  - You can search for SECONDS_IN_A_DAY across the entire codebase.
#  - The magic number 86400 is invisible to grep/search.
#  - The constant name makes the intent self-documenting.


# ============================================================
# PART 2: Avoid Mental Mapping
# ============================================================
#
# Don't force the reader of your code to translate what the
# variable means. Explicit is better than implicit.

# ❌ BAD
seq = ("Austin", "New York", "San Francisco")

for item in seq:
    # do_stuff()
    # do_some_other_stuff()

    # Wait, what's `item` again?
    print(item)


# ✅ GOOD
locations = ("Austin", "New York", "San Francisco")

for location in locations:
    # do_stuff()
    # do_some_other_stuff()
    # ...
    print(location)

# Why is this better?
#  - `locations` and `location` make the intent immediately clear.
#  - The reader doesn't need to scroll back up to remember what `seq` or `item` was.
#  - Explicit names eliminate the mental overhead of translation.


# ============================================================
# 📌 Summary
# ============================================================
#
#  1. Use searchable names — avoid magic numbers and single-letter
#     variables. Name constants at the module level so they can be
#     found and understood across the codebase.
#
#  2. Avoid mental mapping — don't make readers translate vague
#     names like `seq` or `item` into what they actually represent.
#     Explicit is always better than implicit.
# ============================================================
