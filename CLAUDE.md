# Resume Evaluator — Claude Context

## Project Overview
A Python CLI tool that evaluates a resume Word document using the Claude API and produces a scored markdown report.

## Architecture

```
resume.docx → src/parser.py → src/evaluator.py → src/reporter.py → console or .md file
```

## Key Files
| File | Purpose |
|------|---------|
| `src/main.py` | CLI entry point (`argparse`), wires pipeline together |
| `src/parser.py` | Extracts text from `.docx` files via `python-docx` |
| `src/evaluator.py` | Sends resume text to Claude API, returns `dict` with `scores` and `evaluation` keys |
| `src/reporter.py` | Builds scorecard table, adds header, routes output to console or file |

## Usage
```
python src/main.py resume.docx
python src/main.py resume.docx --role "Senior Software Engineer"
python src/main.py resume.docx --output report.md
```

## Evaluation Sections & Score Keys
| Score Key    | Section Label          |
|--------------|------------------------|
| `summary`    | Summary / Objective    |
| `experience` | Experience             |
| `education`  | Education              |
| `skills`     | Skills                 |
| `formatting` | Formatting & ATS       |
| `overall`    | Overall                |

## Important Notes
- `python-docx` extracts paragraph text and table cell text; table rows are joined with `  |  ` separators
- Claude returns `{"scores": {...}, "evaluation": "..."}` — `_parse_response()` in `evaluator.py` handles fallback if JSON parsing fails
- `max_tokens=4096` — needed for complete evaluations
- All progress messages go to `stderr`; report content goes to `stdout`
- `--role` injects a role context line at the top of the user message (not the system prompt)

## Environment
- Python 3.12
- Key dependencies: `anthropic`, `python-docx`, `python-dotenv`
- API key in `.env` as `ANTHROPIC_API_KEY`
- Model: `claude-opus-4-6`
- No virtual environment — packages installed globally
