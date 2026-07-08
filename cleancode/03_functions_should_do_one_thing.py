"""
Functions should do one thing

This is by far the most important rule in software engineering. When functions do more than one thing, 
they are harder to compose, test, and reason about. When you can isolate a function to just one action, 
they can be refactored easily and your code will read much cleaner.

Below are three examples showing the progression from a bad approach to the best approach utilizing generators.
"""

from typing import List, Generator, Iterator


class Client:
    def __init__(self, active: bool):
        self.active = active


def email(client: Client) -> None:
    """Simulates sending an email to a client."""
    pass


# ==========================================
# Bad: Function does more than one thing
# ==========================================
def email_clients_bad(clients: List[Client]) -> None:
    """Filter active clients and send them an email.
    
    Why it's bad: 
    - The function is both filtering and emailing. 
    - It's harder to test just the filtering logic or just the email logic.
    """
    for client in clients:
        if client.active:
            email(client)


# ==========================================
# Good: Separating responsibilities
# ==========================================
def get_active_clients(clients: List[Client]) -> List[Client]:
    """Filter active clients.
    
    Why it's good:
    - We separated the filtering logic from the emailing logic.
    
    Why it can be better:
    - It iterates through all clients and creates a brand new list in memory. 
    - This can be memory-intensive for a very large list of clients.
    """
    return [client for client in clients if client.active]


def email_clients_good(clients: List[Client]) -> None:
    """Send an email to a given list of clients."""
    for client in get_active_clients(clients):
        email(client)


# ==========================================
# Even better: Using Generators
# ==========================================
def active_clients(clients: Iterator[Client]) -> Generator[Client, None, None]:
    """Only active clients, yielded one by one lazily.
    
    Why it's the best:
    - Single Responsibility: It only handles filtering.
    - Memory Efficiency: It yields items lazily. It doesn't create a new list in memory.
    - Faster execution if the pipeline breaks early: We don't evaluate the whole list upfront.
    - Generality: Accepts any Iterator, not just a List.
    """
    return (client for client in clients if client.active)


def email_clients_best(clients: Iterator[Client]) -> None:
    """Send an email to a given list of clients."""
    for client in active_clients(clients):
        email(client)
