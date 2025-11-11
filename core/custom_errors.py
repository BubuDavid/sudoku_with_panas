from typing import Literal


class OutOfBoundariesError(Exception):
    def __init__(
        self,
        obj_name: Literal["number", "mark"],
        pos_error_type: Literal["row", "column", "both"],
        n_rows: int,
        n_cols: int,
        message: str = "Game object: {obj_name} out of board game boundaries. Out of {pos_error_type}. For board with dimensions {n_rows}x{n_cols}.",
    ) -> None:
        self.obj_name = obj_name
        self.pos_error_type = pos_error_type
        self.n_rows = n_rows
        self.n_cols = n_cols
        message = message.format(
            obj_name=obj_name,
            pos_error_type=pos_error_type,
            n_rows=n_rows,
            n_cols=n_cols,
        )
        super().__init__(message)


class CellNotAvailableError(Exception):
    def __init__(
        self,
        i: int,
        j: int,
        message: str = "You cannot modify cell ({i},{j}) because is a fixed number",
        *args: object,
    ) -> None:
        message.format(i=i, j=j)
        super().__init__(message, *args)


class OutOfLimitsError(Exception):
    def __init__(
        self,
        number: int,
        max_number: int,
        message: str = "Number: {number} out of range 0 < number < {max_number}",
        *args: object,
    ) -> None:
        message.format(number=number, max_number=max_number)
        super().__init__(message, *args)
