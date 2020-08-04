""".. include:: ../_notebooks/01-dummy.rst"""

from typing import Union


########################################################################
class Dumb:
    """Dumb Class"""

    # ----------------------------------------------------------------------
    def __init__(self, n: Union[int, float]) -> None:
        """Constructor"""

        self.n = n

    # ----------------------------------------------------------------------
    def add_m(self, m: Union[int, float]) -> Union[int, float]:
        """Add `m` to my `n`."""
        return self.n + m

