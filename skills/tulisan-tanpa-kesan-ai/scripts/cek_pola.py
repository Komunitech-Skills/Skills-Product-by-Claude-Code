#!/usr/bin/env python3
"""Alat bantu skill tulisan-tanpa-kesan-ai: mendeteksi pola tulisan "berbau AI" khas
Bahasa Indonesia pada sebuah draf, dan menghitung skor kebersihan (0-100, makin tinggi
makin bersih dari pola).

Hanya memakai pustaka standar Python (3.7+). Tidak ada akses jaringan.
Jalankan dengan `python3` (Windows: `python` atau `py`).

PENTING: ini alat bantu HEURISTIK (pencocokan kata/frasa), bukan pendeteksi AI dan bukan
penentu akhir. Selalu baca ulang temuannya sendiri — lihat SKILL.md & references/pola-ai-indonesia.md
untuk penjelasan tiap pola dan contoh perbaikan.

Contoh:
  python3 cek_pola.py --teks "Di era digital ini, mari kita simak tips berikut. Semoga bermanfaat!"
  python3 cek_pola.py --file draf.txt
  python3 cek_pola.py --file draf.txt --format json
"""
import argparse
import json
import re
import sys

# ---------------------------------------------------------------------------
# Daftar pola: (id, nama, bobot per kemunculan, daftar regex)
# Bobot lebih besar = pola lebih mencolok/berisiko (lihat "Catatan skor & prioritas"
# di references/pola-ai-indonesia.md). Regex case-insensitive.
# ---------------------------------------------------------------------------

POLA = [
    ("pembuka-basa-basi", "Pembuka basa-basi", 6, [
        r"di era digital ini", r"di era modern ini", r"dalam dunia yang terus berkembang",
        r"seiring perkembangan zaman", r"di tengah persaingan yang semakin ketat",
        r"dalam artikel ini (kita )?akan membahas",
    ]),
    ("kontras-biner", "Kontras biner palsu", 5, [
        r"bukan hanya\b.{0,60}\btetapi juga", r"tidak hanya\b.{0,60}\btetapi juga",
        r"bukan sekadar\b.{0,60}\bmelainkan",
    ]),
    ("ajakan-generik", "Ajakan generik", 4, [
        r"mari kita simak", r"yuk simak", r"yuk kita bahas", r"simak (ulasan|penjelasan) berikut",
    ]),
    ("menjadi-kunci", "Menjadi kunci / peran penting", 5, [
        r"menjadi kunci", r"memainkan peran (penting|vital)", r"menjadi faktor penentu",
        r"menjadi solusi terbaik",
    ]),
    ("tak-dipungkiri", "Tak bisa dipungkiri / sangat penting untuk", 4, [
        r"tak bisa dipungkiri", r"tidak dapat dipungkiri", r"sangat penting untuk\b",
        r"perlu diketahui bahwa",
    ]),
    ("tiga-serangkai", "Tiga-serangkai berulang", 5, [
        r"cepat,\s*mudah,\s*dan\s*terpercaya", r"murah,\s*berkualitas,\s*dan\s*tahan\s*lama",
        r"profesional,\s*ramah,\s*dan\s*berpengalaman",
    ]),
    ("emdash-berlebihan", "Em-dash berlebihan", 2, [
        r"—.{0,80}—.{0,80}—",  # 3+ tanda pisah dalam satu rentang teks
    ]),
    ("emoji-berderet", "Emoji berderet", 2, [
        r"([\U0001F300-\U0001FAFF☀-➿]){3,}",
    ]),
    ("penutup-klise", "Pembuka/penutup klise", 5, [
        r"semoga bermanfaat", r"semoga informasi ini bermanfaat", r"sekian dan terima kasih",
        r"demikian informasi yang dapat kami sampaikan", r"terima kasih sudah membaca sampai",
        r"semoga email ini menemukan anda dalam keadaan baik",
    ]),
    ("klaim-superlatif", "Klaim superlatif tanpa bukti", 8, [
        r"solusi terbaik", r"nomor satu\b", r"\brevolusioner\b", r"terobosan terbaru",
        r"wajib coba", r"dijamin puas", r"terbukti ampuh",
    ]),
    ("insight-palsu", "Insight palsu / analisis dangkal", 5, [
        r"yang menarik adalah", r"hal ini menunjukkan bahwa", r"ini membuktikan betapa",
    ]),
    ("dramatis-terpotong", "Kalimat dramatis terpotong", 4, [
        r"bayangkan jika\b", r"pernahkah kamu berpikir", r"ini bukan sekadar\b.{0,40}\bini adalah",
    ]),
    ("sok-tahu", "Sok tahu isi hati pembaca", 4, [
        r"sering dilewatkan orang", r"kebanyakan orang (nggak|tidak) tahu",
        r"rahasia yang jarang dibagikan",
    ]),
    ("kesimpulan-berlebihan", "Penutup kesimpulan berlebihan", 4, [
        r"^kesimpulannya", r"\bkesimpulannya,", r"jadi,\s*intinya", r"secara keseluruhan,",
    ]),
    ("weasel-attribution", "Klaim tanpa sumber", 7, [
        r"banyak orang percaya", r"penelitian menunjukkan(?! ini bagian dari)",
        r"menurut para ahli",
    ]),
]

# Kata/frasa tunggal yang dihitung terpisah (bukan pola kalimat) — dianggap "kata pengisi"
KATA_PENGISI = [
    "sesungguhnya", "pada dasarnya", "pada hakikatnya",
]


def _baca_teks(args):
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return f.read()
    if args.teks:
        return args.teks
    return sys.stdin.read()


def deteksi(teks):
    """Kembalikan list temuan: {id, nama, kutipan, bobot}."""
    temuan = []
    kalimat_list = re.split(r"(?<=[.!?])\s+|\n+", teks)
    for pola_id, nama, bobot, daftar_regex in POLA:
        for rgx in daftar_regex:
            for m in re.finditer(rgx, teks, flags=re.IGNORECASE | re.MULTILINE):
                # cari kalimat yang memuat kecocokan untuk kutipan yang lebih enak dibaca
                kutipan = None
                for kal in kalimat_list:
                    if m.group(0).lower() in kal.lower():
                        kutipan = kal.strip()
                        break
                if not kutipan:
                    kutipan = m.group(0)
                temuan.append({"id": pola_id, "nama": nama, "kutipan": kutipan, "bobot": bobot})
    return temuan


def hitung_skor(temuan):
    total_potongan = sum(t["bobot"] for t in temuan)
    return max(0, 100 - total_potongan)


def cetak_teks(teks, temuan, skor):
    print(f"Skor kebersihan pola: {skor}/100 (makin tinggi makin bersih)")
    print("Catatan: heuristik pencocokan kata, bukan pendeteksi AI — baca ulang sendiri.\n")
    if not temuan:
        print("Tidak ada pola dari daftar references/pola-ai-indonesia.md yang terdeteksi.")
        return
    for i, t in enumerate(temuan, 1):
        print(f"{i}. Pola: {t['nama']} ({t['id']})")
        print(f"   Kutipan: \"{t['kutipan']}\"")
    print(f"\nTotal temuan: {len(temuan)}")


def main():
    ap = argparse.ArgumentParser(description="Deteksi pola tulisan berbau AI (Bahasa Indonesia).")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--teks", help="Teks draf langsung (dalam tanda kutip).")
    src.add_argument("--file", help="Path file .txt berisi draf.")
    ap.add_argument("--format", choices=["teks", "json"], default="teks")
    args = ap.parse_args()

    teks = _baca_teks(args)
    if not teks or not teks.strip():
        print("ERROR: draf kosong. Tempel teks lewat --teks, --file, atau stdin.", file=sys.stderr)
        sys.exit(1)

    temuan = deteksi(teks)
    skor = hitung_skor(temuan)

    if args.format == "json":
        print(json.dumps({"skor": skor, "temuan": temuan}, ensure_ascii=False, indent=2))
    else:
        cetak_teks(teks, temuan, skor)


if __name__ == "__main__":
    main()
