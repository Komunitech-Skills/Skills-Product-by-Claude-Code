#!/usr/bin/env python3
"""Tombol berhenti (kill switch), status, dan melanjutkan bot.

  python3 berhenti.py --konfigurasi bot/konfigurasi.json                 # BERHENTI SEKARANG (buat file STOP)
  python3 berhenti.py --konfigurasi bot/konfigurasi.json --batalkan-order  # + batalkan order terbuka di bursa
  python3 berhenti.py --konfigurasi bot/konfigurasi.json --status          # lihat status tanpa mengubah apa pun
  python3 berhenti.py --konfigurasi bot/konfigurasi.json --lanjutkan --saya-sudah-cek
  python3 berhenti.py --semua                                            # hentikan SEMUA bot di komputer ini
  python3 berhenti.py --cabut-semua --saya-sudah-cek                     # cabut tombol "hentikan semua"

Lokasi file STOP (bot berhenti bila SATU saja ada, apa pun --folder-bot yang dipakai jadwal):
  - <folder bot>/STOP dan <folder file konfigurasi>/STOP
  - ~/.komunitech/bot-trading-kripto/STOP-<id konfigurasi>   (global, khusus bot ini)
  - ~/.komunitech/bot-trading-kripto/STOP-SEMUA              (global, semua bot)
  (Windows: ~ = C:\\Users\\<nama>)

Tombol berhenti TIDAK butuh konfigurasi valid: bila konfigurasi rusak, file STOP tetap dibuat.
Berhenti tidak menjual koin yang dipegang (supaya tidak ada transaksi tak terduga); jual
manual di aplikasi bursa bila Anda mau. `--lanjutkan` hanya dijalankan atas perintah
eksplisit member setelah meninjau alasan berhenti.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inti import (D, WIB, KonfigurasiTidakValid, Penyamar, daftar_file_stop, folder_stop_global,  # noqa: E402
                  muat_konfigurasi, muat_state, rp, sidik_jari_strategi, simpan_json_atomik, teks, tulis_audit)

FOLDER_SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Tombol berhenti / status / lanjutkan bot kripto", allow_abbrev=False)
    ap.add_argument("--konfigurasi")
    ap.add_argument("--semua", action="store_true", help="hentikan SEMUA bot (file STOP-SEMUA global)")
    ap.add_argument("--cabut-semua", action="store_true", help="hapus STOP-SEMUA (wajib --saya-sudah-cek)")
    ap.add_argument("--folder-bot")
    ap.add_argument("--batalkan-order", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--lanjutkan", action="store_true")
    ap.add_argument("--saya-sudah-cek", action="store_true")
    ap.add_argument("--alasan", default="diminta member")
    ap.add_argument("--url-uji")
    a = ap.parse_args(argv)
    sekarang = datetime.now(WIB)
    p_semua = os.path.join(folder_stop_global(), "STOP-SEMUA")

    if a.cabut_semua:
        if not a.saya_sudah_cek:
            print("Ditolak: tambahkan --saya-sudah-cek (hanya setelah member meninjau & menyetujui).")
            return 1
        if os.path.exists(p_semua):
            os.remove(p_semua)
        print("Tombol 'hentikan semua bot' dicabut. Bot yang sudah berhenti TETAP berhenti sampai masing-masing "
              "dilanjutkan dengan --konfigurasi ... --lanjutkan --saya-sudah-cek.")
        return 0
    if a.semua and not a.lanjutkan and not a.status:
        os.makedirs(folder_stop_global(), exist_ok=True)
        with open(p_semua, "w", encoding="utf-8") as f:
            f.write(f"STOP-SEMUA {sekarang.isoformat(timespec='seconds')} - {a.alasan}\n")
        print(f"Tombol berhenti SEMUA bot AKTIF ({p_semua}). Tidak ada bot yang membuat order baru mulai "
              "putaran berikutnya. Koin yang dipegang TIDAK dijual otomatis.")
        if not a.konfigurasi:
            return 0
    if not a.konfigurasi:
        print("Isi --konfigurasi <file konfigurasi bot>, atau pakai --semua untuk menghentikan semua bot.")
        return 1
    folder = os.path.abspath(a.folder_bot or os.path.dirname(os.path.abspath(a.konfigurasi)))
    p_state, p_audit = (os.path.join(folder, n) for n in ("state.json", "audit.jsonl"))
    semua_stop = daftar_file_stop(a.konfigurasi, folder)
    stop_bot_ini = [p for p in semua_stop if p != p_semua]

    if a.status:
        try:
            cfg = muat_konfigurasi(a.konfigurasi)
            st = muat_state(p_state, cfg)
        except KonfigurasiTidakValid as e:
            print(f"Konfigurasi bermasalah: {e}")
            return 1
        kut = cfg["kutipan"]
        print(f"Bot {cfg['pasangan']} mode {cfg['mode']} | strategi {cfg['_jenis']}")
        aktif = [p for p in semua_stop if os.path.exists(p)]
        print(f"Status: {'BERHENTI - ' + str(st['alasan_berhenti']) if st.get('berhenti') else 'aktif'}"
              f"{' | file STOP aktif: ' + ', '.join(aktif) if aktif else ''}")
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
        if os.path.exists(p_semua):
            print("Ditolak: tombol 'hentikan SEMUA bot' masih aktif. Bila member setuju, cabut dulu dengan "
                  "berhenti.py --cabut-semua --saya-sudah-cek, lalu ulangi.")
            return 1
        st = muat_state(p_state, cfg)
        alasan_lama = st.get("alasan_berhenti")
        # Catatan: waktu_terakhir (pengaman jam mundur) TIDAK di-reset, KECUALI tercatat jauh di masa
        # depan (jam komputer pernah lompat maju); itu hanya diperbaiki lewat --lanjutkan yang ditinjau member.
        catatan_jam = ""
        wt = st.get("waktu_terakhir")
        try:
            if wt and datetime.fromisoformat(wt) > sekarang + timedelta(hours=1):
                catatan_jam = (f" Catatan: putaran terakhir tercatat {wt}, lebih maju dari jam komputer sekarang; "
                               "patokan waktu diatur ulang ke sekarang. Pastikan jam/NTP mesin bot benar.")
                st["waktu_terakhir"] = sekarang.isoformat(timespec="seconds")
        except ValueError:
            st["waktu_terakhir"] = sekarang.isoformat(timespec="seconds")
        st.update(berhenti=False, alasan_berhenti=None, notif_berhenti_terkirim=False,
                  sidik_jari_strategi=sidik_jari_strategi(cfg), hari=None, ekuitas_awal_hari=None,
                  ekuitas_terakhir=None, buku_rugi_harian={}, jejak_ekuitas=[])
        simpan_json_atomik(p_state, st)
        for p in stop_bot_ini:
            if os.path.exists(p):
                os.remove(p)
        tulis_audit(p_audit, "dilanjutkan", {"alasan_berhenti_sebelumnya": alasan_lama}, None, sekarang)
        print(f"Bot dilanjutkan. Alasan berhenti sebelumnya: {(alasan_lama or '-').rstrip('.')}. "
              "Batas rugi harian dihitung ulang dari sekarang." + catatan_jam)
        return 0

    # tulis STOP di SEMUA lokasi milik bot ini (folder bot, folder konfigurasi, global di home),
    # supaya bot berhenti apa pun --folder-bot yang dipakai jadwal.
    dibuat, gagal = [], []
    for p in stop_bot_ini:
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(f"STOP {sekarang.isoformat(timespec='seconds')} - {a.alasan}\n")
            dibuat.append(p)
        except OSError as e:
            gagal.append(f"{p} ({type(e).__name__})")
    if not dibuat:
        print("GAGAL membuat file STOP di mana pun: " + "; ".join(gagal) +
              ". Hentikan jadwal bot di OpenClaw sekarang dan batalkan order manual di aplikasi bursa.")
        return 2
    try:
        tulis_audit(p_audit, "tombol_berhenti_ditekan", {"alasan": a.alasan, "file": dibuat}, None, sekarang)
    except OSError:
        pass
    print("Tombol berhenti AKTIF (file STOP dibuat di: " + ", ".join(dibuat) + "). "
          "Bot tidak akan membuat order baru mulai putaran berikutnya.")
    if gagal:
        print("Catatan: sebagian lokasi gagal ditulis: " + "; ".join(gagal))
    if a.batalkan_order:
        try:
            cfg = muat_konfigurasi(a.konfigurasi)
            if cfg["mode"] == "paper":
                print("Mode simulasi: tidak ada order di bursa.")
                return 0
            from bursa import buat_adapter, muat_kunci, ErrorBursa, ErrorKunci, StatusTidakPasti
            kunci = muat_kunci(cfg, FOLDER_SKILL)
            ad = buat_adapter(cfg, kunci, None, a.url_uji)
            if hasattr(ad, "sinkron_waktu"):
                ad.sinkron_waktu()   # cegah error -1021 (jam melenceng) di Binance
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
