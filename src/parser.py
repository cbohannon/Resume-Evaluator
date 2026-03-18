import zipfile
from pathlib import Path
from xml.etree import ElementTree

from docx import Document
from docx.oxml.ns import qn

_APP_NS = "http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"


def _extract_paragraph_text(p_elem) -> str:
    """Extract text from a paragraph element, using ' — ' as a tab separator."""
    parts = []
    for node in p_elem.iter():
        if node.tag == qn("w:t"):
            parts.append(node.text or "")
        elif node.tag == qn("w:tab"):
            parts.append("  —  ")
    return "".join(parts).strip()


def get_page_count(path: str) -> int | None:
    """Read the page count Word stored in docProps/app.xml, or None if unavailable."""
    try:
        with zipfile.ZipFile(path) as z:
            with z.open("docProps/app.xml") as f:
                tree = ElementTree.parse(f)
                pages = tree.find(f"{{{_APP_NS}}}Pages")
                if pages is not None and pages.text:
                    return int(pages.text)
    except Exception:
        pass
    return None


def parse_docx(path: str) -> str:
    """Extract text content from a Word (.docx) file, preserving document order."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if p.suffix.lower() != ".docx":
        raise ValueError(f"Expected a .docx file, got: {p.suffix}")

    doc = Document(str(p))
    lines = []

    for child in doc.element.body:
        if child.tag == qn("w:p"):
            text = _extract_paragraph_text(child)
            if text:
                lines.append(text)
        elif child.tag == qn("w:tbl"):
            seen = set()
            for row in child.iter(qn("w:tr")):
                cells = []
                for cell in row.iter(qn("w:tc")):
                    cell_text = "".join(node.text or "" for node in cell.iter(qn("w:t"))).strip()
                    if cell_text and cell_text not in seen:
                        seen.add(cell_text)
                        cells.append(cell_text)
                if cells:
                    lines.append(", ".join(cells))

    return "\n".join(lines)
