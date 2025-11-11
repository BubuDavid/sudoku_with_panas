from typing import Required, TypedDict


class BoardExpression(TypedDict, total=False):
    board: Required[list[list[int | None]]]
    n_cols: int
    n_rows: int
    n_cols_group: int
    n_rows_group: int
