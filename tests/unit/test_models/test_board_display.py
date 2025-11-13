from models import SudokuBoard


def test_display_default(board_normal_empty: SudokuBoard):
    print()
    print(board_normal_empty.display())


def test_display_mini(board_mini_empty: SudokuBoard):
    print()
    print(board_mini_empty.display())


def test_display_complete(board_normal_complete: SudokuBoard):
    print()
    print(board_normal_complete.display())


def test_display_incomplete(board_normal_incomplete: SudokuBoard):
    print()
    print(board_normal_incomplete.display())


def test_display_conflicts(board_normal_conflicts: SudokuBoard):
    print()
    print(board_normal_conflicts.display())
