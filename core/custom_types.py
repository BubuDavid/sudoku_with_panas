from typing import TypedDict

COORD = tuple[int, int]
CoordNum = dict[COORD, int]


class ConflictDict(TypedDict):
    """Object that identifies conflicts between the numbers in the sudoku"""

    rows: dict[int, CoordNum]
    cols: dict[int, CoordNum]
    regions: dict[int, int]
