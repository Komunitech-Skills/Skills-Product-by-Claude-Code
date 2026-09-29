#!/usr/bin/env python3
"""Persiapan mode LIVE (uang asli) -- konfirmasi bertahap.

Langkah 1 (ringkasan & kode):
  python3 siapkan_live.py --konfigurasi bot/konfigurasi.json
  -> cek syarat, tampilkan ringkasan aturan + batas risiko + kode konfirmasi + frasa yang
     HARUS DIKETIK SENDIRI oleh member di chat.
Langkah 2 (cek kunci, butuh internet; tanpa menampilkan isi kunci):
  python3 siapkan_live.py --konfigurasi bot/konfigurasi.json --cek-kunci
Langkah 3 (tulis konfirmasi -- HANYA dengan frasa yang diketik member sendiri, SETELAH member
menyelesaikan DAFTAR PERIKSA izin withdraw di layar bursa):
  python3 siapkan_live.py --konfigurasi bot/konfigurasi.json \
     --frasa "LIVE <kode> SAYA TANGGUNG RISIKONYA" --saya-sudah-cek-tanpa-withdraw
Setiap perubahan konfigurasi mengubah kode -> konfirmasi lama tidak berlaku.
Indodax: izin withdraw TIDAK diperiksa lewat API (skill sengaja tidak memanggil metode withdraw apa
pun, termasuk yang baca-saja) -> daftar periksa manual WAJIB. Binance live: selain daftar periksa,
izin diperiksa otomatis lewat GET /sapi/v1/account/apiRestrictions (endpoint baca-saja).
"""

import argparse
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inti import (D, WIB, KonfigurasiTidakValid, muat_konfigurasi, muat_state, rp, sidik_jari_penuh,  # noqa: E402
                  sidik_jari_strategi, simpan_json_atomik, teks, tulis_audit, SUMBER_PAJAK)
from jalankan_bot import FRASA_LIVE, bukti_paper  # noqa: E402

DAFTAR_PERIKSA = {
    "indodax": [
        "Login ke indodax.com (situs asli, cek alamatnya), buka menu Pengaturan API / API Trade.",
        "Cari API key yang dipakai bot ini (cocokkan beberapa karakter awalnya; JANGAN tempel ke chat).",
        "Pastikan izin 'withdraw' / 'tarik dana' TIDAK dicentang. Yang boleh aktif hanya 'view' dan 'trade'.",
        "Bila izin withdraw ternyata aktif: hapus kunci itu, buat kunci baru tanpa withdraw, simpan ulang file kunci.",
        "Tidak ada kunci lain berizin withdraw yang disimpan di komputer bot.",
    ],
    "binance": [
        "Login ke binance.com, buka API Management.",
        "Pastikan 'Enable Withdrawals' TIDAK dicentang; aktifkan hanya 'Enable Reading' dan 'Enable Spot & Margin Trading'.",
        "Margin, futures, universal transfer TIDAK aktif; batasi IP ke IP mesin bot bila bisa.",
        "Bot juga memeriksa ini otomatis (endpoint baca-saja apiRestrictions) dan menolak kunci ber-withdraw.",
    ],
}


def teks_daftar_periksa(bursa):
    return "\n".join(f"  [ ] {i}. {t}" for i, t in enumerate(DAFTAR_PERIKSA[bursa], 1))

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
         f"Fee dipakai: {teks(ds['fee_persen'])}% | PPh jual: {teks(ds['tarif_pph'] * 100)}%"
         + (f" | PPh beli (swap kripto-kripto): {teks(ds['tarif_pph_beli'] * 100)}%" if ds.get("tarif_pph_beli") else "")
         + f" ({SUMBER_PAJAK})",
         "Order yang dipakai: MARKET (harga saat eksekusi bisa berbeda dari harga terakhir)."]
    if cfg["_jenis"] == "grid":
        b.append("Catatan grid: stop-loss global dihitung dari harga rata-rata SEMUA slot, jadi bisa terpicu "
                 "saat harga masih di dalam rentang grid; untung/rugi per jual memakai rata-rata semua koin.")
    return "\n".join(b)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Persiapan mode live bot kripto (konfirmasi bertahap)")
    ap.add_argument("--konfigurasi", required=True)
    ap.add_argument("--folder-bot")
    ap.add_argument("--cek-kunci", action="store_true")
    ap.add_argument("--frasa")
    ap.add_argument("--saya-sudah-cek-tanpa-withdraw", action="store_true",
                    help="member SENDIRI sudah menyelesaikan daftar periksa izin withdraw di layar bursa")
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
    cukup_paper, ket_paper = bukti_paper(st, sj)
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
        except (ErrorKunci, ErrorBursa, ValueError) as e:
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
        print(f"\nBukti simulasi aturan yang sama: {ket_paper}."
              + ("" if cukup_paper else " BELUM CUKUP -> biarkan jadwal paper berjalan dulu. Live belum bisa aktif."))
        print(f"\nDAFTAR PERIKSA WAJIB (dikerjakan MEMBER SENDIRI di layar {cfg['bursa']}, bukan oleh agent):")
        print(teks_daftar_periksa(cfg["bursa"]))
        print(f"\nKode konfirmasi: {kode}")
        print("Agar live aktif, MEMBER SENDIRI harus mengetik persis kalimat ini di chat:")
        print(f"  {frasa_benar}")
        print("dan menyatakan sudah menyelesaikan SEMUA butir daftar periksa di atas (izin withdraw MATI).")
        return 0 if cukup_paper else 2

    if n_sim < 1 or not cukup_paper:
        print(f"Ditolak: bukti simulasi belum cukup ({ket_paper}).")
        return 2
    if a.frasa.strip() != frasa_benar:
        print("Ditolak: frasa tidak persis sama (kode mungkin berubah karena konfigurasi diubah). "
              "Jalankan langkah 1 lagi.")
        return 2
    if not a.saya_sudah_cek_tanpa_withdraw:
        print("Ditolak: daftar periksa izin withdraw belum dinyatakan selesai oleh member "
              "(--saya-sudah-cek-tanpa-withdraw). Daftar periksa:")
        print(teks_daftar_periksa(cfg["bursa"]))
        return 2
    sekarang = datetime.now(WIB)
    simpan_json_atomik(os.path.join(folder, "KONFIRMASI-LIVE.json"), {
        "kode": kode, "frasa": frasa_benar, "pernyataan_kunci_tanpa_withdraw": True,
        "daftar_periksa_withdraw_selesai": True, "daftar_periksa": DAFTAR_PERIKSA[cfg["bursa"]],
        "cek_izin_otomatis": cfg["bursa"] == "binance",
        "waktu": sekarang.isoformat(timespec="seconds"), "ringkasan": ringkasan(cfg)})
    tulis_audit(os.path.join(folder, "audit.jsonl"), "konfirmasi_live", {"kode": kode}, None, sekarang)
    print(f"Konfirmasi live tersimpan (kode {kode}). Jadwal/perintah live wajib memakai --izinkan-live.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
