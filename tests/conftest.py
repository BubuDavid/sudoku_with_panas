import pytest

from models import SudokuBoard


@pytest.fixture
def board_normal_empty():
    return SudokuBoard()


@pytest.fixture
def board_mini_empty():
    return SudokuBoard(
        n_cols=6,
        n_rows=6,
        n_cols_group=3,
        n_rows_group=2,
    )


@pytest.fixture
def board_normal_complete():
    return SudokuBoard(
        board=[
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9],
        ]
    )


@pytest.fixture
def board_normal_incomplete():
    return SudokuBoard(
        board=[
            [5, None, 4, None, 7, None, 9, None, 2],
            [None, 7, None, 1, None, 5, None, 4, None],
            [1, None, 8, None, 4, None, 5, None, 7],
            [None, 5, None, 7, None, 1, None, 2, None],
            [4, None, 6, None, 5, None, 7, None, 1],
            [None, 1, None, 9, None, 4, None, 5, None],
            [9, None, 1, None, 3, None, 2, None, 4],
            [None, 8, None, 4, None, 9, None, 3, None],
            [3, None, 5, None, 8, None, 1, None, 9],
        ]
    )


@pytest.fixture
def board_normal_conflicts():
    return SudokuBoard(
        board=[
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 5],  # Row conflict: 5 appears twice
            [1, 9, 8, 3, 4, 2, 5, 6, 2],  # Row conflict: 2 appears twice
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 3],  # Row conflict: 3 appears twice
            # Column 0 conflict: 3 appears in rows 0 and 8
            # Column 8 conflict: 3 appears in rows 4 and 8
            # Top-right 3x3 region conflict: 2 appears twice (row 0 and row 2)
        ]
    )
