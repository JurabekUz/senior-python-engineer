from threading import Thread
from time import sleep


# Imagine this function is resource-intensive and takes a long time to execute.
def heavy_fn(delay, text):
    print("Starting heavy process...")
    sleep(delay)
    print(text)
    print("Heavy process finished.")


# Create thread instances.
# Each thread allows this function to run independently.
# Threads don't execute immediately after creation.
thread1 = Thread(
    target=heavy_fn,
    args=(
        12,  # Wait for 12 seconds
        "Threading is fun to learn. It may not be easy at first, but if you keep writing code, you'll understand it much better.",
    ),
)

thread2 = Thread(
    target=heavy_fn,
    args=(
        5,  # Wait for 5 seconds
        "In real projects, threading becomes much more interesting. Imagine downloading or processing 100 files. You could create 5 threads and let each thread handle 20 files.",
    ),
)

# The threading syntax itself is actually very simple.
# You only need a function (with or without arguments).
#
# Personally, I didn't learn much from examples that only use sleep()
# or print a few messages. They felt too artificial.
#
# Real-world examples are much easier to understand because they solve
# actual problems, and that's where threading becomes useful.
#
# The Thread class mainly needs two arguments:
# - target: the function to execute
# - args: the arguments passed to that function
#
# Overall, the idea is simple:
# 1. Write a function.
# 2. Create one or more Thread objects.
# 3. Pass the target function and its arguments.
# 4. Start the threads.

# Start both threads.
# In Python, creating a thread isn't enough—you must call start().
thread1.start()
thread2.start()

# Wait until both threads finish before continuing.
thread1.join()
thread2.join()

print("Completed.")

# Congratulations! You built your first multithreaded program.
#
# The syntax is actually the easy part.
# The real challenge comes later, when multiple threads share data,
# coordinate with each other, and avoid race conditions.
#
# The best way to learn threading is by writing code that solves
# real problems instead of only reading articles or chatting with AI.