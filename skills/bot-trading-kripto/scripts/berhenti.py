#!/usr/bin/env python3
"""Tombol berhenti (kill switch), status, dan melanjutkan bot.

  python3 berhenti.py --konfigurasi bot/konfigurasi.json                 # BERHENTI SEKARANG (buat file bot/STOP)
  python3 berhenti.py --konfigurasi bot/konfigurasi.json --batalkan-order  # + batalkan order terbuka di bursa
  python3 berhenti.py --konfigurasi bot/konfigurasi.json --status          # lihat status tanpa mengubah apa pun
  python3 berhenti.py --konfigurasi bot/konfigurasi.json --lanjutkan --saya-sudah-cek

Tombol berhenti TIDAK butuh konfigurasi valid: bila konfigurasi rusak, file STOP tetap dibuat.
Berhenti tidak menjual koin yang dipegang (supaya tidak ada transaksi tak terduga); jual
manual di aplikasi bursa bila Anda mau. `--lanjutkan` hanya dijalankan atas perintah
eksplisit member setelah meninjau alasan berhenti.
"""

import argparse
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inti import (D, WIB, KonfigurasiTidakValid, Penyamar, muat_konfigurasi, muat_state, rp,  # noqa: E402
                  sidik_jari_strategi, simpan_json_atomik, teks, tulis_audit)

FOLDER_SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Tombol berhenti / status / lanjutkan bot kripto")
    ap.add_argument("--konfigurasi", required=True)
    ap.add_argument("--folder-bot")
    ap.add_argument("--batalkan-order", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--lanjutkan", action="store_true")
    ap.add_argument("--saya-sudah-cek", action="store_true")
    ap.add_argument("--alasan", default="diminta member")
    ap.add_argument("--url-uji")
    a = ap.parse_args(argv)
    folder = os.path.abspath(a.folder_bot or os.path.dirname(os.path.abspath(a.konfigurasi)))
    p_stop, p_state, p_audit = (os.path.join(folder, n) for n in ("STOP", "state.json", "audit.jsonl"))
    sekarang = datetime.now(WIB)

    if a.status:
        try:
            cfg = muat_konfigurasi(a.konfigurasi)
            st = muat_state(p_state, cfg)
        except KonfigurasiTidakValid as e:
            print(f"Konfigurasi bermasalah: {e}")
            return 1
        kut = cfg["kutipan"]
        print(f"Bot {cfg['pasangan']} mode {cfg['mode']} | strategi {cfg['_jenis']}")
        print(f"Status: {'BERHENTI - ' + str(st['alasan_berhenti']) if st.get('berhenti') else 'aktif'}"
              f"{' | file STOP ada' if os.path.exists(p_stop) else ''}")
        print(f"Kas bot {rp(D(st['kas']), kut)} | koin {teks(D(st['posisi_koin']))} {cfg['koin']} | "
              f"modal terpakai {rp(D(st['biaya_perolehan']), kut)} | untung/rugi terealisasi {rp(D(st['realized_pl']), kut)}")
        print(f"Total fee {rp(D(st['total_fee']), kut)} | PPh {rp(D(st['total_pajak']), kut)} | "
              f"transaksi {st.get('jumlah_transaksi', 0)} | putaran {st.get('jumlah_tick', 0)}")
        return 0

    if a.lanjutkan:
        if not a.saya_sudah_cek:
            print("Ditolak: tambahkan --saya-sudah-cek (hanya setelah member meninjau alasan berhenti & menyetujui).")
            return 1
        try:
            cfg = muat_konfigurasi(a.konfigurasi)
        except KonfigurasiTidakValid as e:
            print(f"Tidak bisa melanjutkan, konfigurasi bermasalah: {e}")
            return 1
        st = muat_state(p_state, cfg)
        alasan_lama = st.get("alasan_berhenti")
        st.update(berhenti=False, alasan_berhenti=None, notif_berhenti_terkirim=False,
                  sidik_jari_strategi=sidik_jari_strategi(cfg), hari=None, ekuitas_awal_hari=None, ekuitas_terakhir=None)
        simpan_json_atomik(p_state, st)
        if os.path.exists(p_stop):
            os.remove(p_stop)
        tulis_audit(p_audit, "dilanjutkan", {"alasan_berhenti_sebelumnya": alasan_lama}, None, sekarang)
        print(f"Bot dilanjutkan. Alasan berhenti sebelumnya: {(alasan_lama or '-').rstrip('.')}. "
              "Batas rugi harian dihitung ulang dari sekarang.")
        return 0

    os.makedirs(folder, exist_ok=True)
    with open(p_stop, "w", encoding="utf-8") as f:
        f.write(f"STOP {sekarang.isoformat(timespec='seconds')} - {a.alasan}\n")
    tulis_audit(p_audit, "tombol_berhenti_ditekan", {"alasan": a.alasan}, None, sekarang)
    print("Tombol berhenti AKTIF (file STOP dibuat). Bot tidak akan membuat order baru mulai putaran berikutnya.")
    if a.batalkan_order:
        try:
            cfg = muat_konfigurasi(a.konfigurasi)
            if cfg["mode"] == "paper":
                print("Mode simulasi: tidak ada order di bursa.")
                return 0
            from bursa import buat_adapter, muat_kunci, ErrorBursa, ErrorKunci, StatusTidakPasti
            kunci = muat_kunci(cfg, FOLDER_SKILL)
            ad = buat_adapter(cfg, kunci, None, a.url_uji)
            n = ad.batalkan_semua()
            tulis_audit(p_audit, "order_dibatalkan", {"jumlah": n}, Penyamar(kunci.rahasia()), sekarang)
            print(f"Order terbuka yang dibatalkan: {n}.")
        except Exception as e:  # tetap berhenti walau pembatalan gagal
            print(f"PERHATIAN: pembatalan order gagal ({type(e).__name__}: {e}). Batalkan manual di aplikasi bursa.")
            return 2
    print("Koin yang sudah dibeli bot TIDAK dijual otomatis. Cek posisi di aplikasi bursa.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
