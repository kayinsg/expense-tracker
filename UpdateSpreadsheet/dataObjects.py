from typing import NamedTuple

class FontProfile(NamedTuple):
    name       : str
    size       : int | float
    boldToggle : bool
