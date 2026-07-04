# This approach is commonly used in real projects.
# On top of that, it's very easy to use.

from concurrent.futures import ThreadPoolExecutor
import time


# Imagine this is a resource-intensive function.
def heavy_function(name_of_arg):
    print("Starting...")

    time.sleep(5)
    print(name_of_arg)

    print("Finished.")


# We usually use ThreadPoolExecutor with a context manager.
#
# You'll see this pattern a lot in Python:
# create a class instance and use it with "with".
#
# To be honest, I liked this syntax from the beginning,
#
# ThreadPoolExecutor is a class.
# max_workers specifies how many threads can run at the same time.
with ThreadPoolExecutor(max_workers=5) as executor:
    # map() schedules the function for every item in the iterable.
    # The first argument is the function.
    # The second argument is an iterable of values passed to the function.
    executor.map(
        heavy_function, 
        range(1, 500)
    )


# In my opinion, this approach is easier to remember
# and much cleaner than creating Thread objects manually.
#
# The workflow is simple:
# 1. Write a function.
# 2. Create a ThreadPoolExecutor.
# 3. Call map() with the function and an iterable.
#
# That's it.
