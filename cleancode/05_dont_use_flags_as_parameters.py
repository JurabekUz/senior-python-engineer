"""
Don't use flags as function parameters

Flags tell your user that this function does more than one thing. 
Functions should do one thing. Split your functions if they are 
following different code paths based on a boolean.
"""

from tempfile import gettempdir
from pathlib import Path

# ==========================================
# Bad: Using a boolean flag
# ==========================================
def create_file_bad(name: str, temp: bool) -> None:
    """
    Why it's bad:
    - The `temp` boolean flag clearly shows that this function does two different things.
    - It creates two separate code paths inside the function.
    """
    if temp:
        (Path(gettempdir()) / name).touch()
    else:
        Path(name).touch()


# ==========================================
# Good: Splitting into separate functions
# ==========================================
def create_file(name: str) -> None:
    """
    Why it's good:
    - This function does exactly one thing: creates a file in the current directory.
    - The function name and signature are extremely clear.
    """
    Path(name).touch()


def create_temp_file(name: str) -> None:
    """
    Why it's good:
    - This function does exactly one thing: creates a temporary file.
    - We eliminated the boolean flag and made the API simpler.
    """
    (Path(gettempdir()) / name).touch()
