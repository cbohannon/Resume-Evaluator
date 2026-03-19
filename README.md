# Resume Evaluator

A Python CLI tool that evaluates a resume Word document using the Claude API and produces a scored markdown report with actionable feedback.

## Requirements

- Python 3.12+
- An [Anthropic API key](https://console.anthropic.com/)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your API key:
   ```bash
   cp .env.example .env
   # then edit .env and add your key
   ```

## Usage

```bash
# Basic evaluation
python src/main.py resume.docx

# Target a specific role
python src/main.py resume.docx --role "Senior Software Engineer"

# Save report to a file
python src/main.py resume.docx --output report.md

# Combine options
python src/main.py resume.docx --role "Senior Software Engineer" --output report.md
```

## Output

The report includes a scorecard and detailed evaluation across five sections:

| Section | What's evaluated |
|---|---|
| Summary / Objective | Clarity, relevance, hook |
| Experience | Impact statements, quantified achievements, action verbs |
| Education | Relevance, formatting, prominence |
| Skills | Coverage, ATS keyword alignment, gaps |
| Formatting & ATS | Layout, length, parse-friendliness |

Each section is scored 1–10, with an overall score and a **Quick Wins** section highlighting the top 3 changes for immediate impact.

## Roadmap

### V2 — PDF Support
Planned support for `.pdf` resumes using `pdfminer.six` or `pypdf`. The pipeline will remain the same — the parser will detect the file extension and route accordingly, with no changes required to the evaluator or reporter.
