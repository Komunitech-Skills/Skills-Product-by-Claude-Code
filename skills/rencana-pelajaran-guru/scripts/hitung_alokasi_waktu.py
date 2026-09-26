#!/usr/bin/env python3
"""Hitung & cocokkan alokasi waktu Modul Ajar/RPP.

Karya asli Komunitech (komunitech.com) — bukan bagian dari materi yang diambil dari
anthropics/k12-teacher-skills. Hanya memakai Python standar (tanpa paket tambahan),
jadi tetap jalan di macOS/Linux/Windows dengan Python 3 biasa.

Kenapa skill ini butuh script (bukan dikira-kira):
- 1 Jam Pelajaran (JP) punya durasi menit berbeda per jenjang (SD 35, SMP 40, SMA/SMK 45).
- Total menit kegiatan (pembukaan + inti + penutup, per pertemuan) HARUS persis sama
  dengan total JP yang diminta guru dikali menit per JP jenjang itu — kalau tidak, jadwal
  pelajaran di sekolah bisa kacau (pelajaran berikutnya telat mulai).

Contoh pakai:
    python3 hitung_alokasi_waktu.py --jenjang smp --jp 3 --pertemuan "10,45,10;5,50,15"

    (dua pertemuan; tiap pertemuan ditulis "pembukaan,inti,penutup" dalam menit,
    dipisah ";" antar pertemuan)

Keluaran (JSON ke stdout) berisi total menit yang diminta (JP x menit/JP x jumlah
pertemuan), total menit yang ditulis di setiap pertemuan, selisihnya, dan status
COCOK/TIDAK COCOK per pertemuan.

Skill tetap bisa dipakai TANPA menjalankan script ini — Langkah Kerja di SKILL.md
meminta menjumlahkan menit secara manual bila Python tidak tersedia.
"""
from __future__ import annotations

import argparse
import json
import sys

MENIT_PER_JP = {
    "sd": 35,
    "mi": 35,
    "smp": 40,
    "mts": 40,
    "sma": 45,
    "smk": 45,
    "ma": 45,
}

JENJANG_VALID = ", ".join(sorted(MENIT_PER_JP))


def parse_pertemuan(teks: str) -> list[tuple[int, int, int]]:
    """Ubah "10,45,10;5,50,15" jadi [(10,45,10), (5,50,15)]. Lempar ValueError yang
    pesannya sudah ramah untuk ditampilkan ke guru bila format salah."""
    hasil = []
    for i, blok in enumerate(teks.split(";"), start=1):
        blok = blok.strip()
        if not blok:
            continue
        bagian = [b.strip() for b in blok.split(",")]
        if len(bagian) != 3:
            raise ValueError(
                f"Pertemuan {i}: harus 3 angka dipisah koma "
                f"(pembukaan,inti,penutup), ditemukan {len(bagian)}: {blok!r}"
            )
        try:
            angka = tuple(int(b) for b in bagian)
        except ValueError:
            raise ValueError(
                f"Pertemuan {i}: semua nilai harus bilangan bulat menit, ditemukan {blok!r}"
            ) from None
        if any(a < 0 for a in angka):
            raise ValueError(f"Pertemuan {i}: menit tidak boleh negatif ({blok!r})")
        hasil.append(angka)
    if not hasil:
        raise ValueError("Tidak ada data pertemuan yang bisa dibaca dari --pertemuan")
    return hasil


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Hitung & cocokkan alokasi waktu Modul Ajar/RPP dengan Jam Pelajaran (JP)."
    )
    ap.add_argument(
        "--jenjang", required=True, choices=sorted(MENIT_PER_JP),
        help=f"Jenjang sekolah ({JENJANG_VALID})",
    )
    ap.add_argument("--jp", required=True, type=int, help="Jumlah JP per pertemuan (mis. 2 atau 3)")
    ap.add_argument(
        "--pertemuan", required=True,
        help='Menit tiap pertemuan, format "pembukaan,inti,penutup" dipisah ";" '
             'untuk banyak pertemuan. Contoh: "10,45,10;5,50,15"',
    )
    args = ap.parse_args()

    if args.jp <= 0:
        print(json.dumps({"error": "--jp harus lebih dari 0"}, ensure_ascii=False, indent=2))
        return 1

    try:
        pertemuan = parse_pertemuan(args.pertemuan)
    except ValueError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False, indent=2))
        return 1

    menit_per_jp = MENIT_PER_JP[args.jenjang]
    target_menit = args.jp * menit_per_jp

    baris = []
    semua_cocok = True
    for i, (pembukaan, inti, penutup) in enumerate(pertemuan, start=1):
        total = pembukaan + inti + penutup
        selisih = total - target_menit
        cocok = selisih == 0
        semua_cocok = semua_cocok and cocok
        baris.append({
            "pertemuan": i,
            "pembukaan_menit": pembukaan,
            "inti_menit": inti,
            "penutup_menit": penutup,
            "total_menit": total,
            "target_menit": target_menit,
            "selisih_menit": selisih,
            "status": "COCOK" if cocok else (
                "KELEBIHAN" if selisih > 0 else "KEKURANGAN"
            ),
        })

    hasil = {
        "jenjang": args.jenjang,
        "menit_per_jp": menit_per_jp,
        "jp_per_pertemuan": args.jp,
        "target_menit_per_pertemuan": target_menit,
        "jumlah_pertemuan": len(pertemuan),
        "total_menit_seluruh_pertemuan": sum(b["total_menit"] for b in baris),
        "target_menit_seluruh_pertemuan": target_menit * len(pertemuan),
        "semua_pertemuan_cocok": semua_cocok,
        "rincian": baris,
    }
    print(json.dumps(hasil, ensure_ascii=False, indent=2))
    return 0 if semua_cocok else 2


if __name__ == "__main__":
    sys.exit(main())
