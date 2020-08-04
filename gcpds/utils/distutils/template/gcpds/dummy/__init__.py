from .dummy import Dumb
from typing import Union


# ----------------------------------------------------------------------
def dumber(n: Union[int, float], m: Union[int, float]) -> Union[int, float]:
    """Dumper way to add two numbers."""
    dumb = Dumb(n)
    return dumb.add_m(m)

