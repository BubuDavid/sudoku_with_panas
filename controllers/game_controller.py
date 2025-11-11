import json
from pathlib import Path
from typing import cast

from models import BoardExpression, SudokuBoard


class GameController:
    def __init__(
        self,
        n_cols=9,
        n_rows=9,
        n_cols_group=3,
        n_rows_group=3,
        board=None,
    ) -> None:
        self.board = SudokuBoard(
            n_cols=n_cols,
            n_rows=n_rows,
            n_cols_group=n_cols_group,
            n_rows_group=n_rows_group,
            board=board,
        )
        self.original_board = self.board
        self.move_history: list[tuple[str, tuple[int, int, int]]] = []

    @classmethod
    def load_board(cls, board_config_or_path: str | Path | BoardExpression):
        if isinstance(board_config_or_path, str) or isinstance(
            board_config_or_path, Path
        ):
            path_config = Path(board_config_or_path)
            with open(path_config, "r") as f:
                config = cast(BoardExpression, json.load(f))
        else:
            config = board_config_or_path

        board_config: BoardExpression = {
            "board": config["board"],
            "n_cols": config.get("n_cols") or len(config["board"][0]),
            "n_rows": config.get("n_rows") or len(config["board"]),
            "n_rows_group": config.get("n_rows_group")
            or len(config["board"]) // 2,
            "n_cols_group": config.get("n_cols_group")
            or len(config["board"][0]) // 2,
        }

        return cls(**board_config)

    def toggle_number(self, i: int, j: int, number: int) -> int | None:
        if self.board.get(i, j) == number:
            self.board.remove_number(i, j)
            self.move_history.append(("remove_number", (i, j, number)))
            return self.board.get(i, j)

        self.board.add_number(i, j, number)
        self.move_history.append(("add_number", (i, j, number)))
        return self.board.get(i, j)

    def toggle_mark(self, i: int, j: int, number: int) -> int | None:
        result = self.board.toggle_mark(i, j, number)
        self.move_history.append(
            ("add_mark", (i, j, number))
            if result
            else ("remove_mark", (i, j, number))
        )

        return result

    def is_solved(self) -> bool:
        assert self.board is not None
        return self.board.is_solved()

    def get_conflicts(self) -> dict:
        return self.board.validate_board()

    def reset_board(self):
        self.move_history = []
        self.board = self.original_board

    def get_move_count(self):
        return len(self.move_history)
