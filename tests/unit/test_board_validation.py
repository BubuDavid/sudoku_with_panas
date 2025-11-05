import json

from models import SudokuBoard


class SetEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return list(o)
        return json.JSONEncoder.default(self, o)


def test_board_validation_normal_no_conflicts(
    board_normal_complete: SudokuBoard,
):
    conflicts = board_normal_complete.validate_board()
    assert not conflicts["rows"], "Incorrect row conflicts"
    assert not conflicts["cols"], "Incorrect cols conflicts"
    assert not conflicts["regions"], "Incorrect regions conflicts"


def test_board_validation_normal_no_conflicts_incomplete(
    board_normal_incomplete: SudokuBoard,
):
    conflicts = board_normal_incomplete.validate_board()
    assert not conflicts["rows"], "Incorrect row conflicts"
    assert not conflicts["cols"], "Incorrect cols conflicts"
    assert not conflicts["regions"], "Incorrect regions conflicts"


def test_board_validation_normal_conflicts(
    board_normal_conflicts: SudokuBoard,
):
    conflicts = board_normal_conflicts.validate_board()
    assert conflicts["rows"], "Incorrect row conflicts"
    assert conflicts["cols"], "Incorrect cols conflicts"
    assert conflicts["regions"], "Incorrect regions conflicts"
    print()
    print(json.dumps(conflicts, indent=2, cls=SetEncoder))
