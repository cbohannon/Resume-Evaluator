import sys
from datetime import date
from pathlib import Path

_SCORE_LABELS = [
    ("summary",    "Summary / Objective"),
    ("experience", "Experience"),
    ("education",  "Education"),
    ("skills",     "Skills"),
    ("formatting", "Formatting & ATS"),
]


def _build_scorecard(scores: dict) -> str:
    rows = []
    for key, label in _SCORE_LABELS:
        if key in scores:
            rows.append(f"| {label:<24} | {scores[key]:>2}/10 |")

    return "\n".join([
        "## Scorecard\n",
        f"| {'Section':<24} | Score |",
        f"|{'-'*26}|-------|",
        *rows,
        f"|{'-'*26}|-------|",
        f"| {'Overall':<24} | {scores.get('overall', '?'):>2}/10 |\n",
    ])


def report(evaluation: dict, resume_path: str, output: str = "console", role: str = "") -> None:
    """
    Output the evaluation as a formatted markdown report.

    Args:
        evaluation: Dict with 'scores' and 'evaluation' keys returned by Claude
        resume_path: Path to the source resume file (used in the header)
        output: "console" to print, or a file path to save as markdown
        role: Optional target role (e.g. "Senior Software Engineer")
    """
    content = _build_report(evaluation, resume_path, role=role)

    if output == "console":
        print(content)
    else:
        dest = Path(output)
        dest.write_text(content, encoding="utf-8")
        print(f"Report saved to {dest}", file=sys.stderr)


def _build_report(evaluation: dict, resume_path: str, role: str = "") -> str:
    scores = evaluation.get("scores", {})
    text = evaluation.get("evaluation", "")
    today = date.today().strftime("%B %d, %Y")
    filename = Path(resume_path).name if resume_path else ""

    lines = [
        "# Resume Evaluation",
        "",
        f"**Resume:** {filename}" if filename else "",
        f"**Target Role:** {role}" if role else "",
        f"**Date:** {today}",
        "",
        "---",
        "",
    ]

    lines = [line for line in lines if line is not None]

    if scores:
        lines.append(_build_scorecard(scores))
        lines.append("---\n")

    lines.append(text)
    return "\n".join(lines)
