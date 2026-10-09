#!/usr/bin/env python3
"""Uji mundur (backtest) aturan member pada data harga CSV milik member.

Memakai mesin aturan & batas risiko yang SAMA dengan bot sungguhan (inti.py), dengan
model isi sederhana: setiap baris = satu putaran, order terisi di harga PENUTUPAN baris
itu, fee & PPh sesuai konfigurasi. Hasil = fakta historis, BUKAN prediksi.

CSV: header wajib memuat kolom waktu (`tanggal`/`waktu`/`time`/`Time`, format YYYY-MM-DD,
YYYY-MM-DD HH:MM, atau detik unix) dan kolom harga penutupan (`close`/`Close`/`tutup`/`harga`).
Pemisah koma atau titik-koma. Baris rusak dilaporkan, tidak menghentikan proses.

  python3 backtest.py --konfigurasi bot/konfigurasi.json --csv data/btcidr-harian.csv
  python3 backtest.py ... --keluaran teks
"""

import argparse
import csv
import io
import json
import os
import re
import sys
from datetime import datetime, timezone
from decimal import InvalidOperation

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inti import (D, DISCLAIMER, NOL, WIB, KonfigurasiTidakValid, SUMBER_PAJAK, catat_niat_berhasil, cek_niat,  # noqa: E402
                  cek_risiko_awal, ekuitas, hentikan, muat_konfigurasi, rencanakan, rp, simulasi_isi,
                  state_awal, teks, terapkan_isi, bulat_uang)

K_WAKTU = ("tanggal", "waktu", "time", "date", "timestamp")
K_HARGA = ("close", "tutup", "harga", "harga_penutupan", "price")


def parse_waktu(s):
    s = s.strip()
    if s.isdigit():
        n = int(s)
        if n > 10 ** 11:
            n //= 1000
        return datetime.fromtimestamp(n, tz=timezone.utc).astimezone(WIB)
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=WIB)
        except ValueError:
            pass
    raise ValueError(f"waktu '{s}' tidak dikenali (pakai YYYY-MM-DD)")


# "38.000" / "1.500" / "1,500": satu pemisah + tepat 3 angka -> bisa ribuan ATAU desimal, tergantung gaya
_AMBIGU = re.compile(r"[1-9]\d{0,2}[.,]\d{3}")


def _bersihkan(s):
    s = re.sub(r"(?i)^\s*(rp|idr)\.?", "", str(s).strip())
    return s.replace(" ", "").replace("\u00a0", "").lstrip("+")


def gaya_angka(s):
    """Tebak gaya satu nilai harga: 'id' (titik ribuan, koma desimal), 'intl' (titik desimal gaya
    bursa), 'ambigu' ('38.000' bisa 38000 atau 38), 'polos' (bilangan bulat), atau None (bukan angka)."""
    v = _bersihkan(s).lstrip("-")
    if re.fullmatch(r"\d+", v):
        return "polos"
    if _AMBIGU.fullmatch(v):
        return "ambigu"
    if re.fullmatch(r"[1-9]\d{0,2}(\.\d{3})+(,\d+)?|\d+,\d+", v):
        return "id"
    if re.fullmatch(r"\d+\.\d+|[1-9]\d{0,2}(,\d{3})+(\.\d+)?", v):
        return "intl"
    return None


def parse_harga(s, gaya=None):
    """Baca harga penutupan dari CSV.

    gaya='intl' = format bursa (titik desimal: '114311.97', '38000.5', '38.000' = 38).
    gaya='id'   = format spreadsheet Indonesia (titik ribuan, koma desimal: '38.000' = 38000,
                  '1.908.238.000', '38.000,50', 'Rp38.000').
    gaya=None   = tebak per nilai; bentuk ambigu ('38.000', '1.500') DITOLAK, tidak ditebak diam-diam.
    baca_csv() menentukan gaya satu kolom penuh sebelum memanggil fungsi ini."""
    asli = str(s).strip()
    v = _bersihkan(asli)
    negatif = v.startswith("-")
    v = v.lstrip("-")
    g = gaya_angka(v)
    if g is None:
        raise ValueError(f"harga '{asli}' bukan angka")
    if g == "ambigu":
        if gaya is None:
            raise ValueError(f"harga '{asli}' ambigu: pemisahnya bisa berarti ribuan ({re.sub('[.,]', '', v)}) atau desimal. "
                             "Simpan CSV tanpa pemisah ribuan (mis. 38000) atau pakai format asli bursa.")
        g = gaya
    elif g not in ("polos", gaya) and gaya is not None:
        raise ValueError(f"harga '{asli}' formatnya berbeda dengan nilai lain di kolom yang sama")
    if g == "id":
        v = v.replace(".", "").replace(",", ".")
    elif g == "intl":
        v = v.replace(",", "")
    try:
        x = D(v)
    except InvalidOperation:
        raise ValueError(f"harga '{asli}' bukan angka")
    if negatif or not x.is_finite() or x <= 0:
        raise ValueError("harga harus > 0")
    return x


def tentukan_gaya(nilai):
    """Satu gaya untuk seluruh kolom harga. Kolom yang hanya berisi bentuk ambigu ('38.000')
    dan bilangan bulat tidak bisa dipastikan -> KonfigurasiTidakValid dengan pesan jelas."""
    ada = {gaya_angka(v) for v in nilai}
    if "id" in ada and "intl" in ada:
        raise KonfigurasiTidakValid(
            "Kolom harga mencampur format Indonesia (38.000,50) dan format bursa (38000.50). "
            "Samakan formatnya, sebaiknya angka polos tanpa pemisah ribuan.")
    if "id" in ada:
        return "id"
    if "intl" in ada:
        return "intl"
    if "ambigu" in ada:
        contoh = next(v for v in nilai if gaya_angka(v) == "ambigu")
        raise KonfigurasiTidakValid(
            f"Harga di CSV ambigu, mis. '{str(contoh).strip()}': titik bisa berarti ribuan (gaya Indonesia, "
            "pasangan IDR) atau desimal (gaya bursa). Simpan ulang CSV tanpa pemisah ribuan (mis. 38000 atau "
            "38000.5), atau unduh ulang data asli dari bursa.")
    return None


def baca_csv(path):
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        isi = f.read()
    if not isi.strip():
        raise KonfigurasiTidakValid("File CSV kosong.")
    pemisah = ";" if isi.splitlines()[0].count(";") > isi.splitlines()[0].count(",") else ","
    r = csv.DictReader(io.StringIO(isi), delimiter=pemisah)
    kolom = {c.strip().lower(): c for c in (r.fieldnames or [])}
    kw = next((kolom[k] for k in K_WAKTU if k in kolom), None)
    kh = next((kolom[k] for k in K_HARGA if k in kolom), None)
    if not kw or not kh:
        raise KonfigurasiTidakValid(f"CSV wajib punya kolom waktu {K_WAKTU} dan harga penutupan {K_HARGA}. "
                                    f"Kolom yang ada: {r.fieldnames}")
    baris = list(r)
    gaya = tentukan_gaya([b[kh] or "" for b in baris])
    data, rusak = [], []
    for no, b in enumerate(baris, start=2):
        try:
            data.append((parse_waktu(b[kw] or ""), parse_harga(b[kh] or "", gaya)))
        except Exception as e:  # noqa: BLE001 -- baris rusak dicatat, tidak menghentikan
            rusak.append({"baris": no, "alasan": str(e) or type(e).__name__})
    data.sort(key=lambda x: x[0])
    return data, rusak


def jalankan(cfg, data):
    cfg = dict(cfg)
    cfg["_d"] = dict(cfg["_d"])
    kut = cfg["kutipan"]
    st = state_awal(cfg)
    transaksi, kejadian = [], []
    puncak, dd_maks = None, NOL
    for waktu, harga in data:
        if st["berhenti"]:
            break
        alasan, paksa = cek_risiko_awal(cfg, st, harga, waktu)
        daftar = [paksa] if paksa else ([] if alasan else rencanakan(cfg, st, harga, waktu))
        for niat in daftar:
            status, ket = cek_niat(cfg, st, niat, harga, 0)
            if status == "lewati":
                continue
            if status == "berhenti":
                alasan = ket
                break
            isi = simulasi_isi(cfg, niat["sisi"], harga, niat.get("nilai_kutipan"), niat.get("jumlah_koin"))
            if isi is None:
                continue
            pl = terapkan_isi(st, isi, kut)
            catat_niat_berhasil(st, niat, isi, waktu)
            transaksi.append({"waktu": waktu.date().isoformat(), "sisi": isi["sisi"], "harga": teks(harga),
                              "jumlah_koin": teks(isi["jumlah"]), "bersih": teks(isi["bersih"]),
                              "fee": teks(isi["fee"]), "pph": teks(isi["pajak"]),
                              "realized_pl": teks(pl) if isi["sisi"] == "jual" else "", "alasan": niat["alasan"]})
        if alasan:
            hentikan(st, alasan)
            kejadian.append({"waktu": waktu.date().isoformat(), "bot_berhenti": alasan})
        e = ekuitas(st, harga)
        puncak = e if puncak is None or e > puncak else puncak
        if puncak > 0:
            dd_maks = max(dd_maks, (puncak - e) / puncak * 100)
    harga_akhir = data[-1][1]
    modal = cfg["_d"]["modal_maks_total"]
    e_akhir = ekuitas(st, harga_akhir)
    # pembanding faktual: seluruh modal dibelikan sekali di baris pertama, dipegang sampai akhir
    bh = simulasi_isi(cfg, "beli", data[0][1], modal)
    bh_akhir = (modal - bh["bersih"]) + bh["jumlah"] * harga_akhir if bh else modal
    return {
        "periode": f"{data[0][0].date()} s.d. {data[-1][0].date()}", "jumlah_baris": len(data),
        "modal_awal_bot": teks(modal), "ekuitas_akhir": teks(bulat_uang(e_akhir, kut)),
        "hasil_persen": teks(((e_akhir - modal) / modal * 100).quantize(D("0.01"))),
        "untung_rugi_terealisasi": teks(bulat_uang(D(st["realized_pl"]), kut)),
        "koin_tersisa": teks(D(st["posisi_koin"])), "kas_tersisa": teks(bulat_uang(D(st["kas"]), kut)),
        "total_fee": teks(D(st["total_fee"])), "total_pph": teks(D(st["total_pajak"])),
        "jumlah_transaksi": len(transaksi), "penurunan_maks_persen": teks(dd_maks.quantize(D("0.01"))),
        "bot_berhenti": st["alasan_berhenti"],
        "pembanding_beli_sekali_tahan": {"ekuitas_akhir": teks(bulat_uang(bh_akhir, kut)),
                                         "hasil_persen": teks(((bh_akhir - modal) / modal * 100).quantize(D("0.01")))},
        "transaksi": transaksi, "kejadian": kejadian, "kutipan": kut, "disclaimer": DISCLAIMER,
        "catatan": ["Hasil masa lalu tidak menjamin hasil masa depan.",
                    "Order diasumsikan terisi di harga penutupan tiap baris; slippage & likuiditas tidak dimodelkan.",
                    "Pembanding 'beli sekali & tahan' hanya fakta historis, bukan rekomendasi.",
                    SUMBER_PAJAK],
    }


def teks_laporan(h, cfg):
    kut = h["kutipan"]
    r = [f"UJI MUNDUR (backtest) {cfg['pasangan']} - strategi {cfg['_jenis']} - {h['periode']} ({h['jumlah_baris']} baris)",
         f"Modal bot: {rp(D(h['modal_awal_bot']), kut)} -> akhir {rp(D(h['ekuitas_akhir']), kut)} ({h['hasil_persen']}%)",
         f"Untung/rugi terealisasi: {rp(D(h['untung_rugi_terealisasi']), kut)} | koin tersisa {h['koin_tersisa']} {cfg['koin']}",
         f"Transaksi: {h['jumlah_transaksi']} | total fee {rp(D(h['total_fee']), kut)} | PPh {rp(D(h['total_pph']), kut)}",
         f"Penurunan terdalam (drawdown): {h['penurunan_maks_persen']}%",
         f"Bot berhenti: {h['bot_berhenti'] or 'tidak'}",
         f"Pembanding faktual beli sekali & tahan: {rp(D(h['pembanding_beli_sekali_tahan']['ekuitas_akhir']), kut)} "
         f"({h['pembanding_beli_sekali_tahan']['hasil_persen']}%)"]
    if h.get("baris_rusak"):
        r.append(f"Baris CSV dilewati: {len(h['baris_rusak'])} (lihat keluaran JSON)")
    r += ["Catatan: " + c for c in h["catatan"]]
    r += ["", "DISCLAIMER: " + DISCLAIMER]
    return "\n".join(r)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Backtest aturan member pada CSV harga")
    ap.add_argument("--konfigurasi", required=True)
    ap.add_argument("--csv", required=True)
    ap.add_argument("--keluaran", choices=("json", "teks"), default="json")
    a = ap.parse_args(argv)
    try:
        cfg = muat_konfigurasi(a.konfigurasi)
        data, rusak = baca_csv(a.csv)
        if len(data) < 2:
            raise KonfigurasiTidakValid(
                f"Data valid hanya {len(data)} baris; butuh minimal 2. Baris rusak: "
                + (", ".join(f"{r['baris']} ({r['alasan']})" for r in rusak[:10]) or "-"))
    except KonfigurasiTidakValid as e:
        print(json.dumps({"status": "error", "pesan": str(e)}, ensure_ascii=False) if a.keluaran == "json" else f"Error: {e}")
        return 1
    except FileNotFoundError:
        print(f"File CSV '{a.csv}' tidak ditemukan.")
        return 1
    h = jalankan(cfg, data)
    h["baris_rusak"] = rusak
    if a.keluaran == "json":
        print(json.dumps({"status": "ok", **h}, ensure_ascii=False, indent=2))
    else:
        print(teks_laporan(h, cfg))
    return 0


if __name__ == "__main__":
    sys.exit(main())
