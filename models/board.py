import functools
from collections import defaultdict
from typing import Any, cast

from core import CellNotAvailableError, OutOfBoundariesError, OutOfLimitsError


def check_out_of_bounds(func):
    @functools.wraps(func)
    def wrapper(self, i: int, j: int, entity: Any = None, *args, **kwargs):
        out_row = i >= self.n_rows or i < 0
        out_col = j >= self.n_cols or j < 0
        if out_row or out_col:
            if out_row and out_col:
                error_type = "both"
            elif out_row:
                error_type = "row"
            else:
                error_type = "column"

            raise OutOfBoundariesError(
                obj_name="number" if isinstance(entity, int) else "mark",
                pos_error_type=error_type,
                n_rows=self.n_rows,
                n_cols=self.n_cols,
            )

        # Only check availability and limits if entity is provided
        if not self.available_cells[i][j] and entity is not None:
            raise CellNotAvailableError(i, j)

        if isinstance(entity, int) and (
            entity > (max_number := max(self.n_cols, self.n_rows))
            or entity <= 0
        ):
            raise OutOfLimitsError(entity, max_number)

        # Call function with or without entity based on whether it was provided
        if entity is not None:
            return func(self, i, j, entity, *args, **kwargs)
        else:
            return func(self, i, j, *args, **kwargs)

    return wrapper


class SudokuBoard:
    def __init__(
        self,
        n_cols: int = 9,
        n_rows: int = 9,
        n_cols_group: int = 3,
        n_rows_group: int = 3,
        board: list[list[int | None]] | None = None,
    ) -> None:
        self.n_cols = n_cols
        self.n_rows = n_rows
        self.board: list[list[int | None]] = []
        self.mark_board: list[list[list[bool]]] = []
        self.available_cells: list[list[bool]] = []
        for i in range(self.n_rows):
            init_row = []
            for j in range(self.n_cols):
                if board is None:
                    init_row.append(None)
                else:
                    init_row.append(board[i][j])
            self.board.append(init_row)
            self.available_cells.append([cell is None for cell in init_row])
            self.mark_board.append(
                [[False for _ in range(n_cols)] for _ in init_row]
            )

        self.n_cols_group = n_cols_group
        self.n_rows_group = n_rows_group

    def region_mapping(self, i: int, j: int) -> int:
        region_row = i // self.n_rows_group
        region_col = j // self.n_cols_group

        n_group_column = self.n_cols // self.n_cols_group

        current_region = n_group_column * region_row + region_col

        return current_region

    def _filter_validations(
        self,
        possible_conflicts: dict[int, dict[int, set[Any]]],
    ):
        # Filter the conflicts
        # TODO: Make this a one-liner i know is possible!
        actual_conflicts = {}
        for entity, di in possible_conflicts.items():
            for n, s in di.items():
                if len(s) > 1:
                    if entity not in actual_conflicts:
                        actual_conflicts[entity] = {}
                    actual_conflicts[entity][n] = s

        return actual_conflicts

    def validate_board(self) -> dict:
        rows: dict[int, dict[int, set[int]]] = defaultdict(
            lambda: defaultdict(set)
        )
        cols: dict[int, dict[int, set[int]]] = defaultdict(
            lambda: defaultdict(set)
        )
        regions: dict[int, dict[int, set[tuple[int, int]]]] = defaultdict(
            lambda: defaultdict(set)
        )

        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if self.board[i][j] is not None:
                    current = cast(int, self.board[i][j])  # Pyright bug?
                    rows[i][current].add(j)
                    cols[j][current].add(i)
                    regions[self.region_mapping(i, j)][current].add((i, j))

        row_conflicts = self._filter_validations(rows)
        col_conflicts = self._filter_validations(cols)
        region_conflicts = self._filter_validations(regions)

        return {
            "rows": row_conflicts,
            "cols": col_conflicts,
            "regions": region_conflicts,
        }

    @check_out_of_bounds
    def get(self, i: int, j: int) -> int | None:
        return self.board[i][j]

    @check_out_of_bounds
    def add_number(self, i: int, j: int, number: int) -> None:
        self.board[i][j] = number

    @check_out_of_bounds
    def remove_number(self, i: int, j: int) -> None:
        self.board[i][j] = None

    @check_out_of_bounds
    def toggle_mark(self, i: int, j: int, number: int) -> int | None:
        self.mark_board[i][j][number - 1] = not self.mark_board[i][j][
            number - 1
        ]

        return number if self.mark_board[i][j][number - 1] else None

    def is_solved(self):
        validation = self.validate_board()
        has_no_conflicts = not any(
            [validation["rows"], validation["cols"], validation["regions"]]
        )
        all_numbers = all([bool(cell) for row in self.board for cell in row])
        return has_no_conflicts and all_numbers
