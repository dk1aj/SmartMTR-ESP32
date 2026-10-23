"""Generate the two user manuals and two one-page Quick Start PDFs.

Run from the repository root after installing ReportLab and Pillow:
    python docs/generate_documentation_pdfs.py
"""

from __future__ import annotations

import html
import re
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
COLLAGE = ROOT / "output" / "images" / "SmartMTR-ESP32_UI_Collage.png"
PDF_DIR = ROOT / "output" / "pdf"

INK = colors.HexColor("#152233")
BLUE = colors.HexColor("#087EA4")
CYAN = colors.HexColor("#34C7E8")
PALE = colors.HexColor("#EAF7FB")
YELLOW = colors.HexColor("#F6C344")
MUTED = colors.HexColor("#586778")
GRID = colors.HexColor("#B8C8D2")


def register_fonts() -> tuple[str, str, str]:
    candidates = [
        (Path("C:/Windows/Fonts/segoeui.ttf"), Path("C:/Windows/Fonts/segoeuib.ttf"), Path("C:/Windows/Fonts/seguisb.ttf")),
        (Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"), Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"), Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")),
    ]
    for regular, bold, semi in candidates:
        if regular.exists() and bold.exists() and semi.exists():
            pdfmetrics.registerFont(TTFont("DocRegular", str(regular)))
            pdfmetrics.registerFont(TTFont("DocBold", str(bold)))
            pdfmetrics.registerFont(TTFont("DocSemi", str(semi)))
            return "DocRegular", "DocBold", "DocSemi"
    return "Helvetica", "Helvetica-Bold", "Helvetica-Bold"


REGULAR, BOLD, SEMI = register_fonts()


def clean_text(value: str) -> str:
    return value.replace("–", "-").replace("—", "-").replace("‑", "-").replace("×", "x")


def inline(value: str) -> str:
    value = html.escape(clean_text(value.strip()))
    value = re.sub(r"`([^`]+)`", lambda match: f"<font name='{SEMI}'>{match.group(1)}</font>", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", value)
    value = re.sub(r"\[([^]]+)\]\(([^)]+)\)", r"<u>\1</u>", value)
    return value


def styles(compact: bool = False):
    base = getSampleStyleSheet()
    body_size = 7.1 if compact else 9.1
    leading = 8.6 if compact else 12.0
    return {
        "title": ParagraphStyle("title", parent=base["Title"], fontName=BOLD, fontSize=24 if compact else 30, leading=28 if compact else 34, textColor=INK, alignment=TA_CENTER, spaceAfter=5 * mm),
        "subtitle": ParagraphStyle("subtitle", parent=base["Normal"], fontName=REGULAR, fontSize=10.2, leading=13, textColor=MUTED, alignment=TA_CENTER),
        "h1": ParagraphStyle("h1", parent=base["Heading1"], fontName=BOLD, fontSize=12 if compact else 16, leading=14 if compact else 19, textColor=BLUE, spaceBefore=3 * mm, spaceAfter=1.5 * mm, keepWithNext=True),
        "h2": ParagraphStyle("h2", parent=base["Heading2"], fontName=SEMI, fontSize=9.4 if compact else 12, leading=11 if compact else 14, textColor=INK, spaceBefore=2 * mm, spaceAfter=1 * mm, keepWithNext=True),
        "body": ParagraphStyle("body", parent=base["BodyText"], fontName=REGULAR, fontSize=body_size, leading=leading, textColor=INK, spaceAfter=1.3 * mm),
        "bullet": ParagraphStyle("bullet", parent=base["BodyText"], fontName=REGULAR, fontSize=body_size, leading=leading, leftIndent=4 * mm, firstLineIndent=-3 * mm, textColor=INK, spaceAfter=0.6 * mm),
        "note": ParagraphStyle("note", parent=base["BodyText"], fontName=REGULAR, fontSize=7.6 if compact else 8.5, leading=9.2 if compact else 11, textColor=INK, leftIndent=3 * mm, rightIndent=3 * mm, borderColor=CYAN, borderWidth=0.8, borderPadding=4, backColor=PALE, spaceAfter=2 * mm),
        "caption": ParagraphStyle("caption", parent=base["BodyText"], fontName=REGULAR, fontSize=8.2, leading=10, textColor=MUTED, alignment=TA_CENTER, spaceBefore=2 * mm),
        "cell": ParagraphStyle("cell", parent=base["BodyText"], fontName=REGULAR, fontSize=6.7 if compact else 7.8, leading=8.0 if compact else 9.4, textColor=INK),
        "cellhead": ParagraphStyle("cellhead", parent=base["BodyText"], fontName=BOLD, fontSize=6.9 if compact else 8, leading=8.2 if compact else 9.6, textColor=colors.white),
    }


class NumberedDoc(BaseDocTemplate):
    def __init__(self, filename: Path, title: str, compact: bool = False):
        margin = 12 * mm if compact else 17 * mm
        super().__init__(str(filename), pagesize=A4, leftMargin=margin, rightMargin=margin, topMargin=14 * mm if compact else 18 * mm, bottomMargin=12 * mm if compact else 17 * mm, title=title, author="SmartMTR-ESP32 project")
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="normal")
        self.addPageTemplates(PageTemplate(id="main", frames=[frame], onPage=self.decorate))
        self.compact = compact

    def decorate(self, canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(CYAN)
        canvas.setLineWidth(0.6)
        canvas.line(doc.leftMargin, A4[1] - 10 * mm, A4[0] - doc.rightMargin, A4[1] - 10 * mm)
        canvas.setFont(REGULAR, 7.2)
        canvas.setFillColor(MUTED)
        canvas.drawString(doc.leftMargin, 7 * mm, "SmartMTR-ESP32")
        canvas.drawRightString(A4[0] - doc.rightMargin, 7 * mm, str(doc.page))
        canvas.restoreState()


def fitted_image(path: Path, max_w: float, max_h: float) -> Image:
    with PILImage.open(path) as im:
        w, h = im.size
    scale = min(max_w / w, max_h / h)
    return Image(str(path), width=w * scale, height=h * scale)


def table_flow(rows: list[list[str]], st, widths=None) -> Table:
    data = []
    for ri, row in enumerate(rows):
        style = st["cellhead"] if ri == 0 else st["cell"]
        data.append([Paragraph(inline(cell), style) for cell in row])
    if widths is None:
        cols = max(len(r) for r in rows)
        widths = [176 * mm / cols] * cols
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("GRID", (0, 0), (-1, -1), 0.35, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F8FA")]),
    ]))
    return table


def markdown_blocks(path: Path, st, manual: bool) -> list:
    lines = path.read_text(encoding="utf-8").splitlines()
    story: list = []
    i = 0
    first_h1 = True
    while i < len(lines):
        raw = lines[i].rstrip()
        if not raw:
            i += 1
            continue
        if raw.startswith("!["):
            if manual:
                i += 1
                continue
            story.extend([fitted_image(COLLAGE, 112 * mm, 78 * mm), Spacer(1, 1.5 * mm)])
            i += 1
            continue
        if raw.startswith("# "):
            if first_h1:
                first_h1 = False
            else:
                story.append(Paragraph(inline(raw[2:]), st["h1"]))
            i += 1
            continue
        if raw.startswith("## "):
            heading = raw[3:]
            if manual and heading in {"UI-Übersicht", "UI overview"}:
                caption = "Quelltextbasierte UI-Darstellungen, keine Hardware-Fotos." if "Übersicht" in heading else "Source-based UI renderings, not hardware photographs."
                story.extend([PageBreak(), Paragraph(inline(heading), st["h1"]), Spacer(1, 2 * mm), fitted_image(COLLAGE, 176 * mm, 180 * mm), Paragraph(inline(caption), st["caption"]), PageBreak()])
                i += 1
                while i < len(lines) and (not lines[i].strip() or lines[i].startswith("![") or lines[i].startswith("*Source-") or lines[i].startswith("*Quelltext")):
                    i += 1
                continue
            story.append(Paragraph(inline(heading), st["h1"]))
            i += 1
            continue
        if raw.startswith("### "):
            story.append(Paragraph(inline(raw[4:]), st["h2"]))
            i += 1
            continue
        if raw.startswith("> "):
            story.append(Paragraph(inline(raw[2:]), st["note"]))
            i += 1
            continue
        if raw.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[ |:\-]+\|$", lines[i + 1]):
            rows = [[c.strip() for c in raw.strip("|").split("|")]]
            i += 2
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip("|").split("|")])
                i += 1
            story.extend([table_flow(rows, st), Spacer(1, 1.5 * mm)])
            continue
        if re.match(r"^(?:[-*]|\d+\.)\s+", raw):
            numbered = bool(re.match(r"^\d+\.\s+", raw))
            marker, text_value = re.split(r"\s+", raw, maxsplit=1)
            prefix = marker if numbered else "•"
            story.append(Paragraph(f"{prefix} {inline(text_value)}", st["bullet"]))
            i += 1
            continue
        if raw.startswith("```"):
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            story.append(Paragraph("<font name='Courier'>" + html.escape("<br/>".join(code)) + "</font>", st["note"]))
            continue
        para = [raw]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|>|\||```|[-*]\s|\d+\.\s)", lines[i]):
            para.append(lines[i].strip())
            i += 1
        story.append(Paragraph(inline(" ".join(para)), st["body"]))
    return story


def build_manual(source: str, output: str, language: str):
    st = styles()
    title = "SmartMTR-ESP32\nBedienungsanleitung" if language == "de" else "SmartMTR-ESP32\nUser Manual"
    subtitle = "Praxisanleitung für AetherSDR und FlexRadio" if language == "de" else "Practical guide for AetherSDR and FlexRadio"
    doc = NumberedDoc(PDF_DIR / output, title.replace("\n", " "))
    cover = [Spacer(1, 28 * mm), Paragraph(title.replace("\n", "<br/>"), st["title"]), Paragraph(subtitle, st["subtitle"]), Spacer(1, 15 * mm), fitted_image(COLLAGE, 150 * mm, 112 * mm), Spacer(1, 8 * mm), Paragraph("Source-based documentation - Repository version 2026-10-23", st["caption"]), PageBreak()]
    doc.build(cover + markdown_blocks(ROOT / source, st, manual=True))


def build_quick(source: str, output: str, language: str):
    st = styles(compact=True)
    title = "SmartMTR-ESP32 - Quick Start" if language == "de" else "SmartMTR-ESP32 Quick Start"
    doc = NumberedDoc(PDF_DIR / output, title, compact=True)
    blocks = markdown_blocks(ROOT / source, st, manual=False)
    blocks = [flowable for flowable in blocks if not isinstance(flowable, Image)]
    story = [Paragraph(title, st["title"]), fitted_image(COLLAGE, 112 * mm, 78 * mm)] + blocks
    doc.build(story)


def main():
    if not COLLAGE.is_file():
        raise FileNotFoundError(COLLAGE)
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    build_manual("docs/BEDIENUNGSANLEITUNG_DE.md", "SmartMTR-ESP32_Bedienungsanleitung_DE.pdf", "de")
    build_manual("docs/USER_MANUAL_EN.md", "SmartMTR-ESP32_User_Manual_EN.pdf", "en")
    build_quick("docs/QUICK_START_DE.md", "SmartMTR-ESP32_Quick_Start_DE.pdf", "de")
    build_quick("docs/QUICK_START_EN.md", "SmartMTR-ESP32_Quick_Start_EN.pdf", "en")


if __name__ == "__main__":
    main()
