from collections import defaultdict
from typing import Any


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
        self.board = []
        for i in range(self.n_rows):
            init_row = []
            for j in range(self.n_cols):
                if board is None:
                    init_row.append(None)
                else:
                    init_row.append(board[i][j])
            self.board.append(init_row)

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
                    rows[i][self.board[i][j]].add(j)
                    cols[j][self.board[i][j]].add(i)
                    regions[self.region_mapping(i, j)][self.board[i][j]].add(
                        (i, j)
                    )

        row_conflicts = self._filter_validations(rows)
        col_conflicts = self._filter_validations(cols)
        region_conflicts = self._filter_validations(regions)

        return {
            "rows": row_conflicts,
            "cols": col_conflicts,
            "regions": region_conflicts,
        }
