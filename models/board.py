from core import ConflictDict, CoordNum


class SudokuBoard:
    def __init__(
        self,
        n_cols: int = 9,
        n_rows: int = 9,
        n_cols_group: int = 3,
        n_rows_group: int = 3,
    ) -> None:
        self.n_cols = n_cols
        self.n_rows = n_rows
        self.board = []
        for _ in range(self.n_rows):
            init_row = []
            for _ in range(self.n_cols):
                init_row.append(None)
            self.board.append(init_row)

        self.n_cols_group = n_cols_group
        self.n_rows_group = n_rows_group

    def validate_board(self) -> ConflictDict:
        cols: dict[int, CoordNum] = {}
        rows: dict[int, CoordNum] = {}
        regions: dict[int, int]
