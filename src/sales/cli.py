"""Command Line Interface (CLI) for Sales Analytics."""

import argparse
import sys
from pathlib import Path

from sales import __version__
from sales.calculator import filter_by_threshold
from sales.reader import read_data
from sales.reporter import generate_report


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="sales",
        description="Process sales CSV logs and generate summary reports.",
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        default=None,
        help="Path to input sales CSV/text file",
    )
    parser.add_argument(
        "-i",
        "--input",
        dest="input_flag",
        help="Path to input sales CSV/text file (alternative to positional argument)",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Path to output report file (defaults to stdout if omitted)",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=float,
        default=None,
        help="Minimum line item total amount to include in calculations",
    )
    parser.add_argument(
        "-d",
        "--discount",
        type=float,
        default=0.0,
        help="Discount percentage [0.0 - 100.0] applied to grand total",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.

    Args:
        argv: Command-line arguments (uses sys.argv[1:] if None).

    Returns:
        Process exit code (0 for success, 1 for error).
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    input_path_str = args.input_flag or args.input_file
    if not input_path_str:
        parser.print_usage(sys.stderr)
        sys.stderr.write("Error: input file must be specified.\n")
        return 1

    try:
        records = read_data(input_path_str)
        if args.threshold is not None:
            records = filter_by_threshold(records, args.threshold)

        report = generate_report(records, discount=args.discount)

        if args.output:
            out_file = Path(args.output)
            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.write_text(report + "\n", encoding="utf-8")
        else:
            sys.stdout.write(report + "\n")

        return 0

    except FileNotFoundError as err:
        sys.stderr.write(f"Error: {err}\n")
        return 1
    except ValueError as err:
        sys.stderr.write(f"Validation error: {err}\n")
        return 1
    except Exception as err:
        sys.stderr.write(f"Unexpected error: {err}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
