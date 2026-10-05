#!/usr/bin/env python3
"""Ubah teks Markdown sederhana (hasil skill) menjadi file Word .docx.

Karya asli Komunitech. Hanya Python standar (zipfile + XML), lintas OS, tanpa paket tambahan.
Mendukung: judul (#, ##, ###, ####), kutipan (> teks, tampil miring berindentasi), miring (*teks*), daftar (- / * / 1.), tabel bergaris tegak (| a | b |),
tebal (**teks**), garis pemisah (--- jadi paragraf kosong), dan penanda halaman baru
"<<HALAMAN BARU>>" (dipakai untuk memisahkan Kunci Jawaban guru dari lembar siswa).

Pakai:
    python3 buat_docx.py masukan.md keluaran.docx
(Windows: python atau py). Keluaran: pesan singkat; kode 0 bila berhasil, 1 bila gagal.
"""
from __future__ import annotations

import os
import re
import sys
import zipfile
from xml.sax.saxutils import escape

PAGE_BREAK = "<<HALAMAN BARU>>"
NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'


_TOKEN = re.compile(r"(\*\*.+?\*\*|(?<![*\w])\*(?!\s)[^*]+?(?<!\s)\*(?![*\w]))")


def _runs(text: str, bold_all: bool = False, italic_all: bool = False) -> str:
    out = []
    for part in _TOKEN.split(text):
        if part == "":
            continue
        b, it = bold_all, italic_all
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            part, b = part[2:-2], True
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            part, it = part[1:-1], True
        rpr = ("<w:b/>" if b else "") + ("<w:i/>" if it else "")
        rpr = f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
        out.append(f'<w:r>{rpr}<w:t xml:space="preserve">{escape(part)}</w:t></w:r>')
    return "".join(out)


def _para(text: str, style: str | None = None, bold: bool = False, indent: bool = False,
          quote: bool = False) -> str:
    ppr = ""
    if style:
        ppr += f'<w:pStyle w:val="{style}"/>'
    if indent:
        ppr += '<w:ind w:left="360" w:hanging="240"/>'
    if quote:
        ppr += ('<w:pBdr><w:left w:val="single" w:sz="12" w:space="6" w:color="808080"/></w:pBdr>'
                '<w:ind w:left="567"/>')
    ppr = f"<w:pPr>{ppr}</w:pPr>" if ppr else ""
    return f"<w:p>{ppr}{_runs(text, bold, quote)}</w:p>"


def _table(rows: list[list[str]]) -> str:
    border = "".join(
        f'<w:{s} w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        for s in ("top", "left", "bottom", "right", "insideH", "insideV")
    )
    xml = [f"<w:tbl><w:tblPr><w:tblW w:w=\"0\" w:type=\"auto\"/><w:tblBorders>{border}</w:tblBorders></w:tblPr>"]
    for ri, row in enumerate(rows):
        xml.append("<w:tr>")
        for cell in row:
            xml.append(f"<w:tc><w:tcPr/>{_para(cell, bold=(ri == 0))}</w:tc>")
        xml.append("</w:tr>")
    xml.append("</w:tbl><w:p/>")
    return "".join(xml)


def markdown_ke_body(md: str) -> str:
    body: list[str] = []
    table: list[list[str]] = []
    prev_blank = False

    def flush():
        nonlocal table
        if table:
            body.append(_table(table))
            table = []

    for raw in md.replace("\r\n", "\n").split("\n"):
        line = raw.rstrip()
        s = line.strip()
        if s.startswith("|") and s.endswith("|") and len(s) > 1:
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                continue  # baris pemisah header tabel
            table.append(cells)
            continue
        flush()
        if s == "":
            if not prev_blank:
                body.append("<w:p/>")
            prev_blank = True
            continue
        prev_blank = False
        if s == PAGE_BREAK:
            body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
        elif re.fullmatch(r"[-─_*]{3,}", s):
            continue
        elif (m := re.match(r"(#{1,4})\s+(.*)", s)):
            body.append(_para(m.group(2), f"Heading{len(m.group(1))}"))
        elif (m := re.match(r">\s?(.*)", s)):
            body.append(_para(m.group(1), quote=True))
        elif (m := re.match(r"[-*•]\s+(.*)", s)):
            body.append(_para("• " + m.group(1), indent=True))
        elif (m := re.match(r"(\d+[.)])\s+(.*)", s)):
            body.append(_para(f"{m.group(1)} {m.group(2)}", indent=True))
        else:
            body.append(_para(s))
    flush()
    return "".join(body)


def _styles() -> str:
    def h(n, size):
        return (f'<w:style w:type="paragraph" w:styleId="Heading{n}"><w:name w:val="heading {n}"/>'
                f'<w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>'
                f'<w:pPr><w:keepNext/><w:spacing w:before="240" w:after="80"/><w:outlineLvl w:val="{n-1}"/></w:pPr>'
                f'<w:rPr><w:b/><w:sz w:val="{size}"/></w:rPr></w:style>')
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles {NS}>'
            '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>'
            '<w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>'
            '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>'
            '<w:qFormat/><w:pPr><w:spacing w:after="80"/></w:pPr></w:style>'
            + h(1, 32) + h(2, 28) + h(3, 24) + h(4, 22) + '</w:styles>')


def buat_docx(md: str, path: str) -> None:
    document = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {NS}><w:body>'
                + markdown_ke_body(md) +
                '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
                '<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="708" w:footer="708" w:gutter="0"/>'
                '</w:sectPr></w:body></w:document>')
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
          '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
          '</Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '</Relationships>')
    drels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
             '</Relationships>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", document)
        z.writestr("word/styles.xml", _styles())
        z.writestr("word/_rels/document.xml.rels", drels)


def main(argv: list[str]) -> int:
    if len(argv) != 3 or not argv[2].lower().endswith(".docx"):
        print("Pakai: python3 buat_docx.py masukan.md keluaran.docx")
        return 1
    try:
        with open(argv[1], encoding="utf-8") as f:
            md = f.read()
    except (OSError, UnicodeDecodeError) as e:
        print(f"GAGAL membaca {argv[1]}: {e}")
        return 1
    if not md.strip():
        print("GAGAL: file masukan kosong.")
        return 1
    try:
        buat_docx(md, argv[2])
    except OSError as e:
        print(f"GAGAL menulis {argv[2]}: {e}")
        return 1
    print(f"OK: file ditulis di {os.path.abspath(argv[2])} . Buka dengan Word/Google Docs/LibreOffice dan periksa sebelum dicetak.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
