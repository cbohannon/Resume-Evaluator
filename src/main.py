import argparse
import itertools
import sys
import threading
import time

from parser import parse_docx
from evaluator import evaluate
from reporter import report


def _spinner(message: str, stop_event: threading.Event) -> None:
    for frame in itertools.cycle(r"⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"):
        if stop_event.is_set():
            break
        print(f"\r{message} {frame}", end="", flush=True, file=sys.stderr)
        time.sleep(0.1)
    print(f"\r{message} done.   ", file=sys.stderr)


def _run_with_spinner(message: str, fn):
    stop = threading.Event()
    t = threading.Thread(target=_spinner, args=(message, stop))
    t.start()
    try:
        return fn()
    finally:
        stop.set()
        t.join()


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate a resume using Claude AI."
    )
    parser.add_argument(
        "resume",
        metavar="RESUME",
        help="Path to the resume .docx file",
    )
    parser.add_argument(
        "--output",
        default="console",
        metavar="PATH",
        help='Output destination: "console" (default) or a file path (e.g. report.md)',
    )
    parser.add_argument(
        "--role",
        default="",
        metavar="ROLE",
        help='Target role for evaluation (e.g. "Senior Software Engineer")',
    )

    args = parser.parse_args()

    try:
        print("Parsing resume...", file=sys.stderr)
        resume_text = parse_docx(args.resume)

        evaluation = _run_with_spinner(
            "Sending to Claude for evaluation...",
            lambda: evaluate(resume_text, role=args.role),
        )

        report(evaluation, args.resume, output=args.output, role=args.role)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
