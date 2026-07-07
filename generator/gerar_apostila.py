#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gerador da apostila do Modulo Python Avancado.

Padrao visual: capa em canvas + conteudo paginado com header/footer.
Fontes DejaVu Sans (UTF-8 completo PT-BR) + DejaVu Mono para codigo.
Rodape "N / total" via build em duas passagens (NumberedCanvas).
"""

import re
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as canvasmod
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    Table, TableStyle, Preformatted, PageBreak, KeepTogether, Flowable,
    NextPageTemplate,
)

# --------------------------------------------------------------------------
# Identidade visual
# --------------------------------------------------------------------------
ACCENT      = colors.HexColor("#336791")   # azul Python/PostgreSQL
ACCENT_DARK = colors.HexColor("#1f3f57")
INK         = colors.HexColor("#1b1b1b")
MUTED       = colors.HexColor("#666666")
CODE_BG     = colors.HexColor("#f4f6f8")
CODE_BORDER = colors.HexColor("#d7dde3")
CODE_INK    = colors.HexColor("#22313f")
KEYWORD     = colors.HexColor("#0b6fb8")
NOTE_BG     = colors.HexColor("#eef4f9")
NOTE_BAR    = ACCENT
WARN_BG     = colors.HexColor("#fdf4e3")
WARN_BAR    = colors.HexColor("#d9962a")
ZEBRA       = colors.HexColor("#f2f6fa")
EX_BG       = colors.HexColor("#eef7f0")
EX_BAR      = colors.HexColor("#3a9d5d")

TITLE   = "Modulo Python Avancado"
SUBTITLE= "Programacao Assincrona, Concorrencia, TDD e Algoritmos"
COURSE  = "Desenvolvedor Full Stack Python"
AUTHOR  = "Willians  |  github.com/Willsmt"
OUTPUT  = "../docs/modulo_python_avancado.pdf"

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("DejaVu",      f"{FONT_DIR}/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", f"{FONT_DIR}/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Obl",  f"{FONT_DIR}/DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Mono", f"{FONT_DIR}/DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-MonoBold", f"{FONT_DIR}/DejaVuSansMono-Bold.ttf"))

PAGE_W, PAGE_H = A4
MARGIN_L = 2.0 * cm
MARGIN_R = 2.0 * cm
MARGIN_T = 2.3 * cm
MARGIN_B = 2.0 * cm

# --------------------------------------------------------------------------
# Estilos
# --------------------------------------------------------------------------
st_chapter_eyebrow = ParagraphStyle(
    "eyebrow", fontName="DejaVu-Bold", fontSize=9, leading=11,
    textColor=ACCENT, spaceAfter=2, tracking=1,
)
st_chapter = ParagraphStyle(
    "chapter", fontName="DejaVu-Bold", fontSize=19, leading=23,
    textColor=ACCENT_DARK, spaceBefore=0, spaceAfter=4,
)
st_h2 = ParagraphStyle(
    "h2", fontName="DejaVu-Bold", fontSize=12.5, leading=16,
    textColor=ACCENT, spaceBefore=13, spaceAfter=4,
)
st_h3 = ParagraphStyle(
    "h3", fontName="DejaVu-Bold", fontSize=10.5, leading=14,
    textColor=ACCENT_DARK, spaceBefore=9, spaceAfter=3,
)
st_body = ParagraphStyle(
    "body", fontName="DejaVu", fontSize=9.7, leading=15,
    textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6,
)
st_bullet = ParagraphStyle(
    "bullet", parent=st_body, leftIndent=15, bulletIndent=3, spaceAfter=3,
)
st_note = ParagraphStyle(
    "note", fontName="DejaVu", fontSize=9.2, leading=13.5, textColor=INK,
    alignment=TA_LEFT,
)
st_note_title = ParagraphStyle(
    "notetitle", fontName="DejaVu-Bold", fontSize=9.2, leading=13,
    textColor=ACCENT_DARK, spaceAfter=2,
)
st_warn_title = ParagraphStyle(
    "warntitle", fontName="DejaVu-Bold", fontSize=9.2, leading=13,
    textColor=WARN_BAR, spaceAfter=2,
)
st_ex_title = ParagraphStyle(
    "extitle", fontName="DejaVu-Bold", fontSize=9.5, leading=13,
    textColor=EX_BAR, spaceAfter=3,
)
st_code = ParagraphStyle(
    "code", fontName="DejaVu-Mono", fontSize=8.1, leading=11.3, textColor=CODE_INK,
)
st_tbl = ParagraphStyle(
    "tbl", fontName="DejaVu", fontSize=8.6, leading=11.5, textColor=INK,
)
st_tbl_h = ParagraphStyle(
    "tblh", fontName="DejaVu-Bold", fontSize=8.7, leading=11.5, textColor=colors.white,
)
st_toc = ParagraphStyle(
    "toc", fontName="DejaVu", fontSize=10, leading=18, textColor=INK,
)
st_toc_b = ParagraphStyle(
    "tocb", fontName="DejaVu-Bold", fontSize=10, leading=18, textColor=ACCENT_DARK,
)

# --------------------------------------------------------------------------
# Helpers de conteudo
# --------------------------------------------------------------------------
PY_KEYWORDS = {
    "async", "await", "def", "return", "import", "from", "for", "while", "if",
    "elif", "else", "in", "not", "and", "or", "is", "None", "True", "False",
    "with", "as", "class", "try", "except", "finally", "raise", "yield",
    "global", "lambda", "pass", "break", "continue", "assert",
}

def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def highlight_line(line: str) -> str:
    """Realca palavras-chave Python; trata comentario apos '#'."""
    if "#" in line:
        idx = line.index("#")
        code_part, comment = line[:idx], line[idx:]
    else:
        code_part, comment = line, ""
    out = []
    for tok in re.split(r"(\W+)", code_part):
        if tok in PY_KEYWORDS:
            out.append(f'<font color="#0b6fb8"><b>{esc(tok)}</b></font>')
        else:
            out.append(esc(tok))
    result = "".join(out)
    if comment:
        result += f'<font color="#7a8894"><i>{esc(comment)}</i></font>'
    return result

class CodeBlock(Flowable):
    """Bloco de codigo com fundo, borda e barra de acento a esquerda."""
    def __init__(self, snippet, width=None):
        super().__init__()
        self.lines = snippet.strip("\n").split("\n")
        self.width = width
        self.pad = 7
        self.bar = 3
        self.lh = st_code.leading

    def wrap(self, availW, availH):
        self.width = self.width or availW
        self.height = len(self.lines) * self.lh + 2 * self.pad
        return self.width, self.height

    def draw(self):
        c = self.canv
        h = self.height
        c.setFillColor(CODE_BG)
        c.setStrokeColor(CODE_BORDER)
        c.roundRect(0, 0, self.width, h, 3, stroke=1, fill=1)
        c.setFillColor(ACCENT)
        c.rect(0, 0, self.bar, h, stroke=0, fill=1)
        y = h - self.pad - self.lh + 3
        for line in self.lines:
            p = Paragraph(highlight_line(line) or "&nbsp;", st_code)
            p.wrapOn(c, self.width - 2 * self.pad - self.bar, self.lh)
            p.drawOn(c, self.pad + self.bar, y)
            y -= self.lh

def code(snippet):
    return KeepTogether([CodeBlock(snippet), Spacer(1, 6)])

def para(text, style=st_body):
    return Paragraph(text, style)

def bullets(items):
    return [Paragraph(f"•&nbsp;&nbsp;{it}", st_bullet) for it in items]

def _callout(title, body_flowables, bg, bar, title_style):
    inner = []
    if title:
        inner.append(Paragraph(title, title_style))
    inner.extend(body_flowables)
    t = Table([[inner]], colWidths=[PAGE_W - MARGIN_L - MARGIN_R - 0.7 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LINEBEFORE", (0, 0), (0, -1), 3, bar),
    ]))
    return KeepTogether([t, Spacer(1, 8)])

def nota(text, title="Nota"):
    body = [Paragraph(text, st_note)] if isinstance(text, str) else text
    return _callout(title, body, NOTE_BG, NOTE_BAR, st_note_title)

def atencao(text, title="Atencao"):
    body = [Paragraph(text, st_note)] if isinstance(text, str) else text
    return _callout(title, body, WARN_BG, WARN_BAR, st_warn_title)

def exercicio(items, title="Exercicio para fazer a mao"):
    body = [Paragraph(f"{i+1}.&nbsp;&nbsp;{it}", st_note) for i, it in enumerate(items)]
    return _callout(title, body, EX_BG, EX_BAR, st_ex_title)

def tabela(header, rows, col_widths=None):
    avail = PAGE_W - MARGIN_L - MARGIN_R
    if col_widths is None:
        col_widths = [avail / len(header)] * len(header)
    data = [[Paragraph(esc(h), st_tbl_h) for h in header]]
    for r in rows:
        data.append([Paragraph(esc(str(c)), st_tbl) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, CODE_BORDER),
        ("LINEBELOW", (0, 0), (-1, 0), 1, ACCENT_DARK),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), ZEBRA))
    t.setStyle(TableStyle(style))
    return KeepTogether([t, Spacer(1, 8)])

def chapter(eyebrow, title):
    rule = Table([[""]], colWidths=[4 * cm], rowHeights=[3])
    rule.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), ACCENT)]))
    return [
        PageBreak(),
        Paragraph(eyebrow.upper(), st_chapter_eyebrow),
        Paragraph(title, st_chapter),
        rule,
        Spacer(1, 12),
    ]

# --------------------------------------------------------------------------
# Canvas numerado (rodape N / total) + header
# --------------------------------------------------------------------------
class NumberedCanvas(canvasmod.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved = []

    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved)
        for state in self._saved:
            self.__dict__.update(state)
            if self._pageNumber > 1:
                self._draw_footer(total)
                self._draw_header()
            super().showPage()
        super().save()

    def _draw_footer(self, total):
        self.setFont("DejaVu", 8)
        self.setFillColor(MUTED)
        self.drawCentredString(
            PAGE_W / 2, 1.15 * cm, f"{self._pageNumber} / {total}"
        )
        self.setStrokeColor(CODE_BORDER)
        self.setLineWidth(0.5)
        self.line(MARGIN_L, 1.5 * cm, PAGE_W - MARGIN_R, 1.5 * cm)

    def _draw_header(self):
        self.setFont("DejaVu", 8)
        self.setFillColor(MUTED)
        self.drawString(MARGIN_L, PAGE_H - 1.3 * cm, TITLE)
        self.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 1.3 * cm, COURSE)
        self.setStrokeColor(CODE_BORDER)
        self.setLineWidth(0.5)
        self.line(MARGIN_L, PAGE_H - 1.5 * cm, PAGE_W - MARGIN_R, PAGE_H - 1.5 * cm)

# --------------------------------------------------------------------------
# Capa
# --------------------------------------------------------------------------
def draw_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(ACCENT)
    canvas.rect(0, PAGE_H - 9 * cm, PAGE_W, 9 * cm, stroke=0, fill=1)
    canvas.setFillColor(ACCENT_DARK)
    canvas.rect(0, PAGE_H - 9 * cm, PAGE_W, 0.35 * cm, stroke=0, fill=1)

    canvas.setFillColor(colors.white)
    canvas.setFont("DejaVu-Bold", 11)
    canvas.drawString(MARGIN_L, PAGE_H - 2.2 * cm, COURSE.upper())

    canvas.setFont("DejaVu-Bold", 30)
    canvas.drawString(MARGIN_L, PAGE_H - 4.7 * cm, "Python")
    canvas.drawString(MARGIN_L, PAGE_H - 6.0 * cm, "Avancado")

    canvas.setFont("DejaVu", 12)
    canvas.drawString(MARGIN_L, PAGE_H - 7.6 * cm, SUBTITLE)

    # Cartoes de specs
    specs = [
        ("Concorrencia", "async / threads / processos"),
        ("Testes", "TDD com pytest"),
        ("Algoritmos", "Big O / Binary / Bubble"),
        ("Projeto", "Web scraping assincrono"),
    ]
    card_w = (PAGE_W - MARGIN_L - MARGIN_R - 0.6 * cm) / 2
    card_h = 2.0 * cm
    x0, y0 = MARGIN_L, PAGE_H - 13.4 * cm
    for i, (t, sub) in enumerate(specs):
        col, row = i % 2, i // 2
        x = x0 + col * (card_w + 0.6 * cm)
        y = y0 - row * (card_h + 0.5 * cm)
        canvas.setFillColor(colors.HexColor("#f4f6f8"))
        canvas.setStrokeColor(CODE_BORDER)
        canvas.roundRect(x, y, card_w, card_h, 6, stroke=1, fill=1)
        canvas.setFillColor(ACCENT)
        canvas.rect(x, y, 0.12 * cm, card_h, stroke=0, fill=1)
        canvas.setFillColor(ACCENT_DARK)
        canvas.setFont("DejaVu-Bold", 12)
        canvas.drawString(x + 0.5 * cm, y + card_h - 0.85 * cm, t)
        canvas.setFillColor(MUTED)
        canvas.setFont("DejaVu", 9.5)
        canvas.drawString(x + 0.5 * cm, y + 0.55 * cm, sub)

    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(2)
    canvas.line(MARGIN_L, 2.6 * cm, PAGE_W - MARGIN_R, 2.6 * cm)
    canvas.setFillColor(MUTED)
    canvas.setFont("DejaVu", 9.5)
    canvas.drawString(MARGIN_L, 2.0 * cm, AUTHOR)
    canvas.drawRightString(
        PAGE_W - MARGIN_R, 2.0 * cm, date.today().strftime("%d/%m/%Y")
    )
    canvas.restoreState()

def build(story):
    doc = BaseDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=MARGIN_L, rightMargin=MARGIN_R,
        topMargin=MARGIN_T, bottomMargin=MARGIN_B,
        title=TITLE, author="Willians",
    )
    frame = Frame(
        MARGIN_L, MARGIN_B, PAGE_W - MARGIN_L - MARGIN_R,
        PAGE_H - MARGIN_T - MARGIN_B, id="body",
    )
    cover_frame = Frame(0, 0, PAGE_W, PAGE_H, id="cover")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=draw_cover),
        PageTemplate(id="body", frames=[frame]),
    ])
    doc.build(story, canvasmaker=NumberedCanvas)

if __name__ == "__main__":
    from conteudo import build_story
    build(build_story())
    print(f"Apostila gerada em {OUTPUT}")
