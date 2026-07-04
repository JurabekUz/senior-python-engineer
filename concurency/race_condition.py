from threading import Thread, Lock


# A race condition is a common problem in real-world projects.
# Imagine your function updates a shared variable, file, or database record.
# If multiple threads try to modify it at exactly the same time,
# the final result may become incorrect.
# We use a Lock to prevent this problem.

# Imagine many people want to donate to the same charity event.
donate_amount = 0

# Create a Lock instance.
# This is just Python's syntax for locking shared resources.
#
# To be honest, I didn't like this syntax at first.
# I forgot it many times while learning.
# But it is what it is—you need a Lock object before you can lock anything.
#
# Python uses classes almost everywhere,
# especially for more advanced or complex topics.
lock = Lock()


def donate(batch_of_people: list):
    # donate_amount is a global variable.
    # Since we want to modify it inside this function,
    # we must declare it as global.

    global donate_amount

    for p in batch_of_people:

        # Use the lock with a context manager.
        # Don't forget to create a Lock instance first.
        #
        # While one thread is inside this block,
        # every other thread has to wait.
        with lock:
            donate_amount += p["amount"]
            print(f"{p['name']} donated ${p['amount']}")


batches = (
    # Imagine each list contains thousands of records.
    [{"name": "John", "amount": 200}, {"name": "Musk", "amount": 102}, {"name": "Andre", "amount": 150}],

    # Another batch processed by another thread.
    [{"name": "John", "amount": 200}, {"name": "Musk", "amount": 102}, {"name": "Andre", "amount": 150}],

    # In real projects, these batches are usually much larger.
    [{"name": "John", "amount": 200}, {"name": "Musk", "amount": 102}, {"name": "Andre", "amount": 150}],

    # Every batch will be handled independently.
    [{"name": "John", "amount": 200}, {"name": "Musk", "amount": 102}, {"name": "Andre", "amount": 150}],
)


# Instead of creating each thread manually,
# we can use a for loop (or list comprehension).
threads = [
    Thread(target=donate, args=[batch])
    for batch in batches
]


# Start all threads.
for t in threads:
    t.start()


# Wait until every thread finishes.
for t in threads:
    t.join()


print(f"Total donated amount: ${donate_amount}")

# Without the lock, multiple threads may update donate_amount
# at exactly the same time, and some updates can be lost.
#
# With the lock, only one thread can modify the shared variable
# at any given moment, so the final result is correct.
#
# The syntax is easy.
# The difficult part is recognizing which variables or resources
# are shared between threads and therefore need synchronization.