from typing import Literal

from controllers import GameController


def main(
    board_type: Literal["normal", "mini"],
    difficulty: Literal["easy", "medium", "hard", "gifted"],
):
    gc = GameController.load_board(f"./premade_boards/{board_type}.json")
    gc.randomize(difficulty)
    gc.display_cli()


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
