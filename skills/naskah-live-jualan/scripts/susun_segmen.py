#!/usr/bin/env python3
"""Susun rundown (jadwal segmen) live jualan agar semua produk kebagian waktu dan penonton baru
selalu mendapat rekap.

Pola per produk:
- normal (11 menit): Hook 1 | Demo 4 | Harga & promo 2 | CTA & cara checkout 2 | Tanya-jawab 2
- ringkas (7 menit) dipakai otomatis bila durasi tidak cukup: Hook 1 | Demo 2 | Harga 1 | CTA 2 | Tanya-jawab 1
Pembukaan 3 menit, penutup 3 menit (2 menit bila live < 30 menit). Rekap 1 menit untuk penonton baru
disisipkan setiap ±15 menit. Sisa waktu diisi putaran ulang produk atau "Tanya-jawab bebas & rekap".

Hanya library standar Python 3.8+. Contoh:
  python3 susun_segmen.py --durasi 60 --produk "Hijab Voal,Pashmina Kaos,Inner Ninja" --mulai 19:00
"""
import argparse
import json
import sys
from datetime import datetime, timedelta

# Windows: pastikan teks Indonesia/emoji tercetak tanpa error encoding
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

NORMAL = [("Hook", 1), ("Demo produk", 4), ("Harga & promo", 2), ("CTA & cara checkout", 2), ("Tanya-jawab", 2)]
RINGKAS = [("Hook", 1), ("Demo produk", 2), ("Harga & promo", 1), ("CTA & cara checkout", 2), ("Tanya-jawab", 1)]
JEDA_REKAP = 15


def galat(pesan):
    print("ERROR: " + pesan, file=sys.stderr)
    sys.exit(1)


def total(pola):
    return sum(m for _, m in pola)


def susun(durasi, produk):
    buka = 3
    tutup = 3 if durasi >= 30 else 2
    tersedia = durasi - buka - tutup
    n = len(produk)
    if tersedia >= n * total(NORMAL):
        pola, jenis = NORMAL, "normal"
    elif tersedia >= n * total(RINGKAS):
        pola, jenis = RINGKAS, "ringkas"
    else:
        minimal = n * total(RINGKAS) + buka + tutup
        galat("Durasi {} menit terlalu pendek untuk {} produk. Minimal {} menit, atau kurangi jumlah produk.".format(
            durasi, n, minimal))

    segmen = []
    t = 0

    def tambah(nama, menit, produk_nama="-", putaran=0):
        nonlocal t
        segmen.append({"mulai_menit": t, "selesai_menit": t + menit, "durasi": menit,
                       "segmen": nama, "produk": produk_nama, "putaran": putaran})
        t += menit

    tambah("Pembukaan: sapa, hook besar, janji promo live", buka)
    rekap_terakhir = 0
    batas_isi = durasi - tutup
    putaran = 1
    idx = 0
    while True:
        nama = produk[idx % n]
        if idx and idx % n == 0:
            putaran += 1
        butuh = total(pola)
        perlu_rekap = (t - rekap_terakhir) >= JEDA_REKAP and t + butuh + 1 <= batas_isi
        if t + butuh > batas_isi:
            break
        if perlu_rekap:
            tambah("Rekap untuk penonton baru (promo & produk yang sudah dibahas)", 1)
            rekap_terakhir = t
        for bag, m in pola:
            tambah(bag, m, nama, putaran)
        idx += 1
    sisa = batas_isi - t
    if sisa > 0:
        tambah("Tanya-jawab bebas & rekap semua produk", sisa)
    tambah("Penutup: rekap promo, pengingat checkout, jadwal live berikutnya", tutup)
    return segmen, jenis, idx


def jam(mulai, menit):
    return (mulai + timedelta(minutes=menit)).strftime("%H:%M") if mulai else None


def main():
    p = argparse.ArgumentParser(description="Susun rundown segmen live jualan.")
    p.add_argument("--durasi", type=int, required=True, help="durasi live dalam menit (15–480)")
    p.add_argument("--produk", required=True, help="nama produk dipisah koma, urut dari produk andalan")
    p.add_argument("--mulai", help="jam mulai HH:MM (opsional), mis. 19:00")
    p.add_argument("--json", action="store_true", help="keluarkan JSON")
    a = p.parse_args()

    if not 15 <= a.durasi <= 480:
        galat("Durasi harus 15 sampai 480 menit.")
    produk = [x.strip() for x in a.produk.split(",") if x.strip()]
    if not produk:
        galat("Isi minimal 1 produk di --produk.")
    mulai = None
    if a.mulai:
        try:
            mulai = datetime.strptime(a.mulai.strip().replace(".", ":"), "%H:%M")
        except ValueError:
            galat("Format --mulai harus HH:MM, mis. 19:00.")

    segmen, jenis, jumlah_blok = susun(a.durasi, produk)
    for s in segmen:
        s["jam_mulai"] = jam(mulai, s["mulai_menit"])
        s["jam_selesai"] = jam(mulai, s["selesai_menit"])
    hasil = {"durasi": a.durasi, "jumlah_produk": len(produk), "pola_per_produk": jenis,
             "blok_produk_terjadwal": jumlah_blok, "segmen": segmen}
    if a.json:
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
        return
    print("Rundown live {} menit, {} produk (pola {}).".format(a.durasi, len(produk), jenis))
    print("| Waktu | Menit | Segmen | Produk |")
    print("|---|---|---|---|")
    for s in segmen:
        waktu = "{}–{}".format(s["jam_mulai"], s["jam_selesai"]) if mulai else "{}–{}".format(
            s["mulai_menit"], s["selesai_menit"])
        print("| {} | {} | {} | {} |".format(waktu, s["durasi"], s["segmen"], s["produk"]))


if __name__ == "__main__":
    main()
