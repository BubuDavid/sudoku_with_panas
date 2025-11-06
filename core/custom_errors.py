from typing import Literal


class OutOfBoundariesError(Exception):
    def __init__(
        self,
        obj_name: Literal["number", "mark", "annotation"],
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
