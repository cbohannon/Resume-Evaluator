from pathlib import Path

from docx import Document


def parse_docx(path: str) -> str:
    """Extract text content from a Word (.docx) file."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if p.suffix.lower() != ".docx":
        raise ValueError(f"Expected a .docx file, got: {p.suffix}")

    doc = Document(str(p))
    lines = []

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if text:
            lines.append(text)

    # Also extract text from tables (skills tables, etc.)
    for table in doc.tables:
        for row in table.rows:
            row_text = "  |  ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
            if row_text:
                lines.append(row_text)

    return "\n".join(lines)
