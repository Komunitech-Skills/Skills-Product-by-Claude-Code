#!/usr/bin/env python3
"""Persiapan mode LIVE (uang asli) -- konfirmasi bertahap.

Langkah 1 (ringkasan & kode):
  python3 siapkan_live.py --konfigurasi bot/konfigurasi.json
  -> cek syarat, tampilkan ringkasan aturan + batas risiko + kode konfirmasi + frasa yang
     HARUS DIKETIK SENDIRI oleh member di chat.
Langkah 2 (cek kunci, butuh internet; tanpa menampilkan isi kunci):
  python3 siapkan_live.py --konfigurasi bot/konfigurasi.json --cek-kunci
Langkah 3 (tulis konfirmasi -- HANYA dengan frasa yang diketik member sendiri):
  python3 siapkan_live.py --konfigurasi bot/konfigurasi.json \
     --frasa "LIVE <kode> SAYA TANGGUNG RISIKONYA" --kunci-tanpa-withdraw
Setiap perubahan konfigurasi mengubah kode -> konfirmasi lama tidak berlaku.
"""

import argparse
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inti import (D, WIB, KonfigurasiTidakValid, muat_konfigurasi, muat_state, rp, sidik_jari_penuh,  # noqa: E402
                  sidik_jari_strategi, simpan_json_atomik, teks, tulis_audit, SUMBER_PAJAK)
from jalankan_bot import FRASA_LIVE  # noqa: E402

FOLDER_SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ringkasan(cfg):
    ds, kut, st = cfg["_d"], cfg["kutipan"], cfg["strategi"]
    b = [f"Bursa: {cfg['bursa']} | pasangan: {cfg['pasangan']} | strategi: {cfg['_jenis']}",
         "Aturan strategi (milik Anda): " + json.dumps({k: v for k, v in st.items() if k != 'jenis'}, ensure_ascii=False),
         f"Batas modal per order: {rp(ds['modal_maks_per_order'], kut)}",
         f"Batas modal total: {rp(ds['modal_maks_total'], kut)}",
         f"Stop-loss global: {teks(ds['stop_loss_persen'])}% di bawah harga rata-rata -> jual semua & berhenti",
         f"Batas rugi harian: {rp(ds['rugi_harian_maks'], kut)} -> berhenti",
         f"Order terbuka maks: {ds['order_terbuka_maks']}",
         f"Fee dipakai: {teks(ds['fee_persen'])}% | PPh jual: {teks(ds['tarif_pph'] * 100)}% ({SUMBER_PAJAK})",
         "Order yang dipakai: MARKET (harga saat eksekusi bisa berbeda dari harga terakhir)."]
    return "\n".join(b)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Persiapan mode live bot kripto (konfirmasi bertahap)")
    ap.add_argument("--konfigurasi", required=True)
    ap.add_argument("--folder-bot")
    ap.add_argument("--cek-kunci", action="store_true")
    ap.add_argument("--frasa")
    ap.add_argument("--kunci-tanpa-withdraw", action="store_true")
    ap.add_argument("--url-uji")
    a = ap.parse_args(argv)
    try:
        cfg = muat_konfigurasi(a.konfigurasi)
    except KonfigurasiTidakValid as e:
        print(f"Konfigurasi bermasalah: {e}")
        return 1
    if cfg["mode"] != "live":
        print("Konfigurasi belum \"mode\": \"live\". Live hanya disiapkan atas permintaan eksplisit member.")
        return 1
    folder = os.path.abspath(a.folder_bot or os.path.dirname(os.path.abspath(a.konfigurasi)))
    st = muat_state(os.path.join(folder, "state.json"), cfg)
    sj = sidik_jari_strategi(cfg)
    n_sim = int(st.get("tick_paper_per_sidik", {}).get(sj, 0))
    kode = sidik_jari_penuh(cfg)
    frasa_benar = FRASA_LIVE.format(kode=kode)

    if a.cek_kunci:
        from bursa import buat_adapter, muat_kunci, ErrorBursa, ErrorKunci
        try:
            kunci = muat_kunci(cfg, FOLDER_SKILL)
            ad = buat_adapter(cfg, kunci, None, a.url_uji)
            if hasattr(ad, "sinkron_waktu"):
                ad.sinkron_waktu()
            hasil = ad.cek_izin_kunci()
        except (ErrorKunci, ErrorBursa) as e:
            print(f"Cek kunci GAGAL: {e}")
            return 2
        if hasil.get("lolos") is False:
            print("Kunci DITOLAK: " + "; ".join(hasil.get("masalah", [])))
            print("Buat kunci baru dengan izin HANYA trading spot (tanpa withdraw), lalu ulangi.")
            return 2
        print("Kunci terbaca (isi tidak ditampilkan). " + (
            "Izin diperiksa otomatis: tanpa withdraw, spot trading aktif." if hasil.get("dicek_otomatis") else ""))
        if hasil.get("catatan"):
            print(hasil["catatan"])
        return 0

    if a.frasa is None:
        print("=== PERSIAPAN MODE LIVE (UANG ASLI) ===")
        print(ringkasan(cfg))
        print(f"\nBukti simulasi aturan yang sama: {n_sim} putaran paper."
              + ("" if n_sim else " BELUM ADA -> jalankan mode paper dulu. Live tidak bisa disiapkan."))
        print(f"\nKode konfirmasi: {kode}")
        print("Agar live aktif, MEMBER SENDIRI harus mengetik persis kalimat ini di chat:")
        print(f"  {frasa_benar}")
        print("dan menyatakan bahwa API key TIDAK punya izin withdraw (tarik dana).")
        return 0 if n_sim else 2

    if n_sim < 1:
        print("Ditolak: aturan ini belum pernah dijalankan di mode paper.")
        return 2
    if a.frasa.strip() != frasa_benar:
        print("Ditolak: frasa tidak persis sama (kode mungkin berubah karena konfigurasi diubah). "
              "Jalankan langkah 1 lagi.")
        return 2
    if not a.kunci_tanpa_withdraw:
        print("Ditolak: pernyataan kunci tanpa izin withdraw (--kunci-tanpa-withdraw) belum diberikan member.")
        return 2
    sekarang = datetime.now(WIB)
    simpan_json_atomik(os.path.join(folder, "KONFIRMASI-LIVE.json"), {
        "kode": kode, "frasa": frasa_benar, "pernyataan_kunci_tanpa_withdraw": True,
        "waktu": sekarang.isoformat(timespec="seconds"), "ringkasan": ringkasan(cfg)})
    tulis_audit(os.path.join(folder, "audit.jsonl"), "konfirmasi_live", {"kode": kode}, None, sekarang)
    print(f"Konfirmasi live tersimpan (kode {kode}). Jadwal/perintah live wajib memakai --izinkan-live.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
