"""These tests were in fact vibecoded but reviewed"""

import json
import tempfile
from pathlib import Path

import pytest

from controllers import GameController
from core import CellNotAvailableError, OutOfBoundariesError, OutOfLimitsError
from models import BoardExpression


class TestGameControllerInit:
    def test_init_default(self):
        """Test default initialization creates empty 9x9 board"""
        controller = GameController()
        assert controller.board.n_rows == 9
        assert controller.board.n_cols == 9
        assert controller.board.n_rows_group == 3
        assert controller.board.n_cols_group == 3
        assert len(controller.move_history) == 0

    def test_init_custom_dimensions(self):
        """Test initialization with custom dimensions"""
        controller = GameController(
            n_cols=6, n_rows=6, n_cols_group=3, n_rows_group=2
        )
        assert controller.board.n_rows == 6
        assert controller.board.n_cols == 6
        assert controller.board.n_rows_group == 2
        assert controller.board.n_cols_group == 3

    def test_init_with_board(self):
        """Test initialization with pre-filled board"""
        board = [
            [5, 3, None, None, 7, None, None, None, None],
            [6, None, None, 1, 9, 5, None, None, None],
            [None, 9, 8, None, None, None, None, 6, None],
            [8, None, None, None, 6, None, None, None, 3],
            [4, None, None, 8, None, 3, None, None, 1],
            [7, None, None, None, 2, None, None, None, 6],
            [None, 6, None, None, None, None, 2, 8, None],
            [None, None, None, 4, 1, 9, None, None, 5],
            [None, None, None, None, 8, None, None, 7, 9],
        ]
        controller = GameController(board=board)
        assert controller.board.board[0][0] == 5
        assert controller.board.board[0][2] is None


class TestGameControllerLoadBoard:
    def test_load_from_dict(self):
        """Test loading board from BoardExpression dict"""
        config: BoardExpression = {
            "board": [
                [5, 3, None],
                [6, None, None],
                [None, 9, 8],
            ],
            "n_cols": 3,
            "n_rows": 3,
            "n_cols_group": 1,
            "n_rows_group": 1,
        }
        controller = GameController.load_board(config)
        assert controller.board.n_rows == 3
        assert controller.board.n_cols == 3
        assert controller.board.board[0][0] == 5
        assert controller.board.board[1][1] is None

    def test_load_from_file(self):
        """Test loading board from JSON file"""
        config = {
            "board": [
                [5, 3, None],
                [6, None, None],
                [None, 9, 8],
            ],
            "n_cols": 3,
            "n_rows": 3,
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(config, f)
            temp_path = f.name

        try:
            controller = GameController.load_board(temp_path)
            assert controller.board.n_rows == 3
            assert controller.board.n_cols == 3
            assert controller.board.board[0][0] == 5
        finally:
            Path(temp_path).unlink()

    def test_load_with_inferred_dimensions(self):
        """Test loading board with dimensions inferred from board array"""
        config: BoardExpression = {
            "board": [
                [5, 3, None, 1],
                [6, None, None, 2],
            ]
        }
        controller = GameController.load_board(config)
        assert controller.board.n_rows == 2
        assert controller.board.n_cols == 4
        # Default groups should be half the dimensions
        assert controller.board.n_rows_group == 1
        assert controller.board.n_cols_group == 2


class TestGameControllerToggleNumber:
    def test_toggle_number_add(self):
        """Test adding a number to empty cell"""
        controller = GameController()
        result = controller.toggle_number(0, 0, 5)
        assert result == 5
        assert controller.board.board[0][0] == 5
        assert len(controller.move_history) == 1
        assert controller.move_history[0] == ("add_number", (0, 0, 5))

    def test_toggle_number_remove(self):
        """Test removing a number by toggling same number"""
        controller = GameController()
        controller.toggle_number(0, 0, 5)
        result = controller.toggle_number(0, 0, 5)
        assert result is None
        assert controller.board.board[0][0] is None
        assert len(controller.move_history) == 2
        assert controller.move_history[1] == ("remove_number", (0, 0, 5))

    def test_toggle_number_replace(self):
        """Test replacing one number with another"""
        controller = GameController()
        controller.toggle_number(0, 0, 5)
        result = controller.toggle_number(0, 0, 3)
        assert result == 3
        assert controller.board.board[0][0] == 3
        assert len(controller.move_history) == 2
        assert controller.move_history[1] == ("add_number", (0, 0, 3))

    def test_toggle_number_out_of_bounds(self):
        """Test toggling number with invalid coordinates"""
        controller = GameController()
        with pytest.raises(OutOfBoundariesError):
            controller.toggle_number(10, 0, 5)
        with pytest.raises(OutOfBoundariesError):
            controller.toggle_number(0, 10, 5)
        with pytest.raises(OutOfBoundariesError):
            controller.toggle_number(-1, 0, 5)

    def test_toggle_number_out_of_limits(self):
        """Test toggling number with invalid number value"""
        controller = GameController()
        with pytest.raises(OutOfLimitsError):
            controller.toggle_number(0, 0, 10)
        with pytest.raises(OutOfLimitsError):
            controller.toggle_number(0, 0, 0)
        with pytest.raises(OutOfLimitsError):
            controller.toggle_number(0, 0, -1)

    def test_toggle_number_fixed_cell(self):
        """Test toggling number in a fixed (pre-filled) cell"""
        board = [[5, None], [None, None]]
        controller = GameController(n_rows=2, n_cols=2, board=board)
        # Should raise error when trying to modify fixed cell
        with pytest.raises(CellNotAvailableError):
            controller.toggle_number(0, 0, 3)


class TestGameControllerToggleMark:
    def test_toggle_mark_add(self):
        """Test adding a mark to a cell"""
        controller = GameController()
        result = controller.toggle_mark(0, 0, 5)
        assert result == 5
        assert controller.board.mark_board[0][0][4] is True  # 5 -> index 4
        assert len(controller.move_history) == 1
        assert controller.move_history[0] == ("add_mark", (0, 0, 5))

    def test_toggle_mark_remove(self):
        """Test removing a mark by toggling again"""
        controller = GameController()
        controller.toggle_mark(0, 0, 5)
        result = controller.toggle_mark(0, 0, 5)
        assert result is None
        assert controller.board.mark_board[0][0][4] is False
        assert len(controller.move_history) == 2
        assert controller.move_history[1] == ("remove_mark", (0, 0, 5))

    def test_toggle_mark_multiple(self):
        """Test adding multiple marks to same cell"""
        controller = GameController()
        controller.toggle_mark(0, 0, 1)
        controller.toggle_mark(0, 0, 5)
        controller.toggle_mark(0, 0, 9)
        assert controller.board.mark_board[0][0][0] is True
        assert controller.board.mark_board[0][0][4] is True
        assert controller.board.mark_board[0][0][8] is True
        assert len(controller.move_history) == 3

    def test_toggle_mark_out_of_bounds(self):
        """Test toggling mark with invalid coordinates"""
        controller = GameController()
        with pytest.raises(OutOfBoundariesError):
            controller.toggle_mark(10, 0, 5)

    def test_toggle_mark_fixed_cell(self):
        """Test toggling mark in a fixed cell"""
        board = [[5, None], [None, None]]
        controller = GameController(n_rows=2, n_cols=2, board=board)
        with pytest.raises(CellNotAvailableError):
            controller.toggle_mark(0, 0, 1)


class TestGameControllerSolved:
    def test_is_solved_complete_valid(self, board_normal_complete):
        """Test is_solved returns True for valid complete board"""
        controller = GameController(board=board_normal_complete.board)
        assert controller.is_solved() is True

    def test_is_solved_incomplete(self, board_normal_incomplete):
        """Test is_solved returns False for incomplete board"""
        controller = GameController(board=board_normal_incomplete.board)
        assert controller.is_solved() is False

    def test_is_solved_conflicts(self, board_normal_conflicts):
        """Test is_solved returns False for board with conflicts"""
        controller = GameController(board=board_normal_conflicts.board)
        assert controller.is_solved() is False

    def test_is_solved_empty(self):
        """Test is_solved returns False for empty board"""
        controller = GameController()
        assert controller.is_solved() is False


class TestGameControllerConflicts:
    def test_get_conflicts_none(self, board_normal_complete):
        """Test get_conflicts returns empty for valid board"""
        controller = GameController(board=board_normal_complete.board)
        conflicts = controller.get_conflicts()
        assert not conflicts["rows"]
        assert not conflicts["cols"]
        assert not conflicts["regions"]

    def test_get_conflicts_present(self, board_normal_conflicts):
        """Test get_conflicts detects conflicts"""
        controller = GameController(board=board_normal_conflicts.board)
        conflicts = controller.get_conflicts()
        assert conflicts["rows"]
        assert conflicts["cols"]
        assert conflicts["regions"]


class TestGameControllerReset:
    def test_reset_board(self):
        """Test reset_board restores original state"""
        board = [[None, None, None], [None, None, None], [None, None, None]]
        controller = GameController(n_rows=3, n_cols=3, board=board)

        # Make some moves
        controller.toggle_number(0, 1, 3)
        controller.toggle_number(1, 1, 2)
        controller.toggle_mark(2, 2, 1)

        assert len(controller.move_history) == 3
        assert controller.board.board[0][1] == 3

        # Reset
        controller.reset_board()

        assert len(controller.move_history) == 0
        # Verify board is reset
        assert controller.board.board[0][1] is None
        assert controller.board.board[1][1] is None

    def test_get_move_count(self):
        """Test get_move_count tracks moves correctly"""
        controller = GameController()
        assert controller.get_move_count() == 0

        controller.toggle_number(0, 0, 5)
        assert controller.get_move_count() == 1

        controller.toggle_mark(1, 1, 3)
        assert controller.get_move_count() == 2

        controller.toggle_number(0, 0, 5)  # Remove
        assert controller.get_move_count() == 3


class TestGameControllerMoveHistory:
    def test_move_history_tracks_all_operations(self):
        """Test that move history captures all operations correctly"""
        controller = GameController()

        controller.toggle_number(0, 0, 5)
        controller.toggle_number(0, 1, 3)
        controller.toggle_mark(1, 1, 7)
        controller.toggle_number(0, 0, 5)  # Remove

        expected_history = [
            ("add_number", (0, 0, 5)),
            ("add_number", (0, 1, 3)),
            ("add_mark", (1, 1, 7)),
            ("remove_number", (0, 0, 5)),
        ]

        assert controller.move_history == expected_history
