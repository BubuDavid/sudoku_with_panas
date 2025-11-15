from typing import Literal

from controllers import GameController
from core import CellNotAvailableError, OutOfBoundariesError, OutOfLimitsError


def play_game(gc: GameController):
    """Interactive gameplay loop"""
    print("\n=== Sudoku Game ===")
    print("Commands:")
    print("  <row> <col> <num>   - Add number to cell (e.g., '0 0 5')")
    print("  r <row> <col>       - Remove number from cell")
    print("  u                   - Undo movement")
    print("  reset               - Reset board to start")
    print("  quit                - Exit game")
    print()

    while True:
        gc.display_cli()
        if gc.is_solved():
            print("\n🎉 Congratulations! You solved the puzzle!")
            print(f"Total moves: {gc.get_move_count()}")
            break

        print(f"\nMoves: {gc.get_move_count()}")
        user_input = input("Enter command: ").strip().lower()

        if not user_input:
            continue

        if user_input in {"quit", "exit", "exit()", "q", ":q"}:
            print("Thanks for playing!")
            break

        if user_input == "reset":
            gc.reset_board()
            print("Board reset!")
            continue

        try:
            parts = user_input.split()
            if len(parts) == 3 and parts[0] not in {"u", "r"}:
                # Add number: <row> <col> <num>
                row, col, num = map(int, parts)
                gc.toggle_number(row, col, num)

            elif len(parts) == 3 and parts[0] == "r":
                # Remove number: r <row> <col>
                row, col = map(int, parts[1:])
                gc.remove_number(row, col)
            elif len(parts) == 1 and parts[0] == "u":
                gc.undo_move()
            else:
                print("Invalid command format")

        except ValueError:
            print("Invalid input. Please use numbers.")
        except (
            OutOfBoundariesError,
            CellNotAvailableError,
            OutOfLimitsError,
        ) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


def main(
    board_type: Literal["normal", "mini"],
    difficulty: Literal["easy", "medium", "hard", "gifted"],
):
    gc = GameController.load_board(f"./premade_boards/{board_type}.json")
    gc.randomize(difficulty)
    play_game(gc)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Entrypoint for the sudoku-with-panas gameplay",
    )
    parser.add_argument(
        "type",
        nargs="?",
        type=str,
        default="normal",
        help="Kind of board, for now only supporting: 'mini' and 'normal'",
    )
    parser.add_argument(
        "--diff",
        type=str,
        nargs="?",
        default="easy",
        help="'gifted','easy', 'medium' or 'hard'",
    )

    args = parser.parse_args()

    if args.type not in {"normal", "mini"}:
        raise ValueError("Only supporting 'normal' and 'mini'")

    if args.diff not in {"easy", "medium", "hard", "gifted"}:
        raise ValueError("Only supporting: 'easy', 'medium' or 'hard'")

    main(board_type=args.type, difficulty=args.diff)
