"""
Function arguments (2 or fewer ideally)

A large amount of parameters is usually the sign that a function is doing too much 
(has more than one responsibility). Try to decompose it into smaller functions 
having a reduced set of parameters, ideally less than three.

If the function has a single responsibility, consider if you can bundle some or all 
parameters into a specialized object. This not only reduces parameters but can also 
encapsulate related behavior.
"""

from dataclasses import dataclass
from typing import Dict, Any

# ==========================================
# Bad: Too many arguments
# ==========================================
def create_menu_bad(title: str, body: str, button_text: str, cancellable: bool) -> None:
    """
    Why it's bad:
    - Four parameters make the function signature hard to read.
    - If we need to add another property (e.g., color), we must change the signature everywhere.
    """
    pass


# ==========================================
# Java-esque / Dictionary Config (Better but not ideal in Python)
# ==========================================
class MenuConfigDict:
    def __init__(self, config: Dict[str, Any]):
        """
        Why it's okay but not ideal:
        - It reduces the arguments to 1.
        - However, passing a generic dictionary loses type safety and editor autocomplete.
        - It's hard to know exactly what keys the dictionary should contain without looking at the implementation.
        """
        self.title = config.get("title", "")
        self.body = config.get("body", "")
        self.button_text = config.get("button_text", "OK")
        self.cancellable = config.get("cancellable", False)

menu_dict = MenuConfigDict(
    {
        "title": "My Menu",
        "body": "Something about my menu",
        "button_text": "OK",
        "cancellable": False
    }
)


# ==========================================
# Good (Pythonic): Using Dataclasses
# ==========================================
@dataclass
class MenuConfig:
    """
    Why it's the best (Pythonic):
    - We group the arguments into a single, cohesive data structure.
    - We get full type hints, editor support, and default values natively.
    - If we want to add methods (like validation), we can easily add them to the dataclass.
    """
    title: str
    body: str
    button_text: str = "OK"
    cancellable: bool = False


def create_menu_good(config: MenuConfig) -> None:
    """The function signature is now very clean (1 parameter)."""
    pass


# Usage:
menu_config = MenuConfig(
    title="My Menu",
    body="Something about my menu",
    cancellable=False
)
create_menu_good(menu_config)
