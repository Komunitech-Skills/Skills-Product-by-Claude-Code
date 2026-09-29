#!/usr/bin/env python3
"""Jalankan SATU putaran (tick) bot sesuai aturan member. Dipanggil manual atau terjadwal
(OpenClaw `automations add --command-argv ...`, lihat references/openclaw-jadwal.md).

Urutan pengaman di setiap putaran:
  1. konfigurasi valid & batas risiko lengkap          (kalau tidak: tidak ada order)
  2. ada file STOP (folder bot, folder konfigurasi, atau global
     ~/.komunitech/bot-trading-kripto/STOP-<id> / STOP-SEMUA)?  -> berhenti (tombol berhenti)
  3. bot sudah berstatus berhenti?                       -> diam sampai member melanjutkan
  4. mode live? wajib --izinkan-live + KONFIRMASI-LIVE.json cocok + sudah pernah disimulasikan
  5. kunci milik member (testnet/live) + cek izin kunci (live Binance: tolak bila ada withdraw)
  6. harga dari bursa (gagal -> tidak ada order)
  7. stop-loss global & batas rugi harian (tanggal tidak pernah mundur walau jam komputer mundur)
  8. aturan strategi -> niat order -> cek batas per order/total/order terbuka -> eksekusi
Semua kejadian ditulis ke bot/audit.jsonl (kunci disamarkan) & transaksi ke bot/transaksi.csv.

Keluaran: pesan siap kirim ke member, atau `NO_REPLY` bila tidak ada kejadian.
Kode keluar: 0 tenang, 2 ada transaksi/kejadian, 3 bot berhenti, 1 error konfigurasi/tak terduga.
Dengan --openclaw: SELALU keluar 0 (Gateway OpenClaw menganggap kode bukan-0 sebagai job gagal).

Pakai:
  python3 jalankan_bot.py --konfigurasi bot/konfigurasi.json
  python3 jalankan_bot.py --konfigurasi bot/konfigurasi.json --openclaw
  (uji: --harga 1500000000 untuk mode paper tanpa jaringan; --sekarang 2026-09-29T08:00:00+07:00)
"""

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inti import (D, DISCLAIMER, NOL, WIB, KonfigurasiTidakValid, Penyamar, ambil_buku, angka,  # noqa: E402
                  catat_niat_berhasil, cek_niat, cek_risiko_awal, cek_tombol_berhenti, ekuitas, hentikan,
                  folder_stop_global, hash_konfigurasi, muat_konfigurasi, muat_state, pasang_buku, rencanakan,
                  rp, segel_konfirmasi, sidik_jari_penuh, sidik_jari_strategi, simpan_json_atomik, teks,
                  terapkan_isi, tulis_audit)
from datetime import timedelta  # noqa: E402
from bursa import ErrorBursa, ErrorKunci, StatusTidakPasti, buat_adapter, muat_kunci  # noqa: E402

FOLDER_SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LABEL = {"paper": "[SIMULASI - bukan uang asli]", "testnet": "[TESTNET - uang mainan]",
         "live": "[LIVE - UANG ASLI]"}
KOLOM_TRANSAKSI = ["waktu", "mode", "bursa", "pasangan", "sisi", "jumlah_koin", "harga", "bruto",
                   "fee", "pajak_pph", "bersih", "realized_pl", "alasan", "order_id", "sumber_angka", "catatan"]
FRASA_LIVE = "LIVE {kode} SAYA TANGGUNG RISIKONYA"
# Syarat bukti simulasi sebelum live: putaran paper dengan harga ASLI dari bursa & jam asli
# (bukan --harga/--sekarang/--url-uji), minimal sekian putaran dan rentang sekian jam.
MIN_PAPER_PUTARAN = 3
MIN_PAPER_JAM = 24
KEDALUWARSA_KUNCI_PUTARAN = 600
# KONFIRMASI-LIVE.json SEKALI PAKAI: wajib dipakai (putaran live pertama) dalam 24 jam sejak dibuat.
KEDALUWARSA_KONFIRMASI = timedelta(hours=24)


def bukti_paper(state, sj):
    """Kembalikan (cukup: bool, keterangan) untuk bukti simulasi aturan dengan sidik `sj`."""
    b = (state.get("paper_nyata_per_sidik") or {}).get(sj) or {}
    n = int(b.get("jumlah", 0))
    jam = 0.0
    if b.get("pertama") and b.get("terakhir"):
        jam = (datetime.fromisoformat(b["terakhir"]) - datetime.fromisoformat(b["pertama"])).total_seconds() / 3600
    cukup = n >= MIN_PAPER_PUTARAN and jam >= MIN_PAPER_JAM
    ket = (f"{n} putaran paper dengan harga asli selama {jam:.1f} jam "
           f"(syarat: minimal {MIN_PAPER_PUTARAN} putaran dalam rentang minimal {MIN_PAPER_JAM} jam)")
    return cukup, ket


def ambil_kunci_putaran(p_kunci, sekarang_iso):
    """Kunci putaran ATOMIK (O_CREAT|O_EXCL) supaya dua putaran tidak jalan bersamaan.
    Kunci basi (> 10 menit, mis. proses sebelumnya mati) dihapus lalu dicoba sekali lagi."""
    for _ in range(2):
        try:
            fd = os.open(p_kunci, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            try:
                if time.time() - os.path.getmtime(p_kunci) < KEDALUWARSA_KUNCI_PUTARAN:
                    return False
                os.remove(p_kunci)
            except OSError:
                return False
            continue
        with os.fdopen(fd, "w") as f:
            f.write(sekarang_iso)
        return True
    return False


def tulis_transaksi(path, baris):
    baru = not os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=KOLOM_TRANSAKSI)
        if baru:
            w.writeheader()
        w.writerow(baris)


def periksa_konfirmasi_live(cfg, state, folder_bot, sekarang=None):
    """Kembalikan None bila semua syarat live terpenuhi, atau pesan penolakan.
    Konfirmasi SEKALI PAKAI: dipakai pada putaran live pertama -> menjadi `sesi_live` yang terikat ke hash
    konfigurasi persis. Sesi batal bila mode berganti atau konfigurasi berubah; konfirmasi yang sama tidak
    bisa dipakai lagi (id-nya dicatat di state & file ditandai `dipakai`)."""
    sekarang = sekarang or datetime.now(WIB)
    sj = sidik_jari_strategi(cfg)
    if int(state.get("tick_paper_per_sidik", {}).get(sj, 0)) < 1:
        return ("Mode live ditolak: aturan yang SAMA persis belum pernah dijalankan di mode simulasi (paper). "
                "Jalankan dulu dengan \"mode\": \"paper\" minimal satu putaran, lalu siapkan live lagi.")
    cukup, ket = bukti_paper(state, sj)
    if not cukup:
        return (f"Mode live ditolak: bukti simulasi belum cukup -- baru {ket}. Biarkan jadwal paper berjalan "
                "dulu dengan aturan yang sama, lalu siapkan live lagi.")
    path = os.path.join(folder_bot, "KONFIRMASI-LIVE.json")
    try:
        with open(path, encoding="utf-8") as f:
            k = json.load(f)
    except (OSError, json.JSONDecodeError):
        return ("Mode live ditolak: KONFIRMASI-LIVE.json belum ada/rusak. Jalankan scripts/siapkan_live.py "
                "dan ikuti langkah konfirmasinya.")
    if not isinstance(k, dict):
        k = {}
    hash_cfg = hash_konfigurasi(cfg)
    kode = sidik_jari_penuh(cfg)
    sesi = state.get("sesi_live")
    if sesi and sesi.get("hash_konfigurasi") != hash_cfg:
        state["sesi_live"] = sesi = None          # konfigurasi berubah -> sesi live batal
    if k.get("kode") != kode or k.get("frasa") != FRASA_LIVE.format(kode=kode):
        return ("Mode live ditolak: konfigurasi berubah sejak konfirmasi terakhir (kode tidak cocok). "
                "Ulangi scripts/siapkan_live.py supaya Anda meninjau aturan yang baru.")
    if k.get("pernyataan_kunci_tanpa_withdraw") is not True or k.get("daftar_periksa_withdraw_selesai") is not True:
        return ("Mode live ditolak: daftar periksa 'kunci tanpa izin withdraw' belum diselesaikan member "
                "(siapkan_live.py --saya-sudah-cek-tanpa-withdraw).")
    idk, waktu_k = k.get("id"), k.get("waktu")
    if (not idk or not waktu_k or k.get("hash_konfigurasi") != hash_cfg
            or k.get("segel") != segel_konfirmasi(idk, hash_cfg, waktu_k)):
        return ("Mode live ditolak: KONFIRMASI-LIVE.json tidak terikat ke konfigurasi ini (format lama, disunting, "
                "atau disalin). Ulangi scripts/siapkan_live.py.")
    if sesi and sesi.get("id") == idk:
        return None                                # sesi live yang sama masih berlaku
    dipakai = state.setdefault("konfirmasi_live_dipakai", [])
    if idk in dipakai or k.get("dipakai"):
        return ("Mode live ditolak: konfirmasi live ini SUDAH DIPAKAI (sekali pakai). Konfirmasi batal setiap kali "
                "mode berganti atau konfigurasi berubah. Tinjau lagi posisi & batas risiko, lalu ulangi "
                "scripts/siapkan_live.py.")
    try:
        t_k = datetime.fromisoformat(waktu_k)
        if t_k.tzinfo is None:
            t_k = t_k.replace(tzinfo=WIB)
    except (TypeError, ValueError):
        return "Mode live ditolak: waktu di KONFIRMASI-LIVE.json rusak. Ulangi scripts/siapkan_live.py."
    if sekarang - t_k > KEDALUWARSA_KONFIRMASI or t_k - sekarang > timedelta(minutes=10):
        return ("Mode live ditolak: konfirmasi live kedaluwarsa (wajib dipakai dalam 24 jam sejak dibuat). "
                "Ulangi scripts/siapkan_live.py.")
    # pakai konfirmasi: sekali pakai, terikat hash konfigurasi + waktu
    state["sesi_live"] = {"id": idk, "hash_konfigurasi": hash_cfg, "waktu": waktu_k,
                          "mulai": sekarang.isoformat(timespec="seconds")}
    dipakai.append(idk)
    del dipakai[:-50]
    k["dipakai"] = sekarang.isoformat(timespec="seconds")
    try:
        simpan_json_atomik(path, k)
    except OSError:
        pass                                       # id sudah tercatat di state -> tetap sekali pakai
    return None


def satu_putaran(args):
    cfg = muat_konfigurasi(args.konfigurasi)
    folder_bot = os.path.abspath(args.folder_bot or os.path.dirname(os.path.abspath(args.konfigurasi)))
    p_state = os.path.join(folder_bot, "state.json")
    p_audit = os.path.join(folder_bot, "audit.jsonl")
    p_trx = os.path.join(folder_bot, "transaksi.csv")
    sekarang = datetime.fromisoformat(args.sekarang) if args.sekarang else datetime.now(WIB)
    if sekarang.tzinfo is None:
        sekarang = sekarang.replace(tzinfo=WIB)
    mode, kut, label = cfg["mode"], cfg["kutipan"], LABEL[cfg["mode"]]
    if (args.harga or args.sekarang) and mode != "paper":
        raise KonfigurasiTidakValid("--harga/--sekarang hanya untuk uji di mode paper.")
    penyamar = Penyamar()

    def audit(peristiwa, data):
        tulis_audit(p_audit, peristiwa, data, penyamar, sekarang)

    # kunci putaran (cegah dua putaran bersamaan) -- atomik
    p_kunci = os.path.join(folder_bot, ".sedang-jalan")
    os.makedirs(folder_bot, exist_ok=True)
    if not ambil_kunci_putaran(p_kunci, sekarang.isoformat()):
        return 0, "NO_REPLY"
    try:
        state = muat_state(p_state, cfg)
        pesan_awal = []
        mode_lama = state.get("mode")
        if mode_lama != mode:
            # Ganti mode: buku TIAP MODE terpisah & disimpan. Buku mode lama disimpan di buku_per_mode,
            # buku mode baru dipulihkan (bila pernah ada). Buku LIVE (posisi, modal terpakai, patokan rugi)
            # tidak pernah di-reset oleh ganti mode. Bukti simulasi, waktu_terakhir (pengaman jam), dan
            # status berhenti berada di luar buku sehingga ikut terbawa.
            bpm = state.get("buku_per_mode")
            if not isinstance(bpm, dict):
                bpm = {}
            if mode_lama is not None:
                audit("ganti_mode", {"dari": mode_lama, "ke": mode})
                bpm[mode_lama] = ambil_buku(state)
                if mode_lama == "live" and D(state.get("posisi_koin") or "0") > 0:
                    pesan_awal.append(
                        f"PERHATIAN: mode diganti dari LIVE ke {mode}. Posisi live ({teks(D(state['posisi_koin']))} "
                        f"{cfg['koin']}, modal terpakai {rp(D(state['biaya_perolehan']), cfg['kutipan'])}) TETAP "
                        "tercatat di buku live dan tetap dihitung dalam batas modal total bila kembali ke live. "
                        "Posisi itu TIDAK dipantau stop-loss selama mode bukan live -- cek di aplikasi bursa.")
            pasang_buku(state, cfg, bpm.pop(mode, None))
            state["buku_per_mode"] = bpm
            if state.get("sesi_live"):
                audit("konfirmasi_live_batal", {"alasan": "ganti mode", "id": state["sesi_live"].get("id")})
            state["sesi_live"] = None                     # ganti mode membatalkan konfirmasi live
            state["mode"] = mode
        sj = sidik_jari_strategi(cfg)
        if state.get("sidik_jari_strategi") != sj:
            if D(state["posisi_koin"]) > 0:
                hentikan(state, "Aturan/konfigurasi berubah saat bot masih memegang koin. Tinjau, lalu "
                                "jalankan berhenti.py --lanjutkan bila perubahan disengaja.")
            else:
                state["grid_slot"], state["tp_sl_status"] = {}, "menunggu_masuk"
                state["sidik_jari_strategi"] = sj
            audit("aturan_berubah", {"sidik_baru": sj})

        pesan = pesan_awal

        def selesai(kode):
            simpan_json_atomik(p_state, state)
            if not pesan:
                return kode, "NO_REPLY"
            return kode, "\n".join([f"Bot kripto {label} {cfg['pasangan']}"] + pesan + ["", DISCLAIMER])

        aktif = cek_tombol_berhenti(args.konfigurasi, folder_bot)
        if aktif and not state.get("berhenti"):
            hentikan(state, "Tombol berhenti (file STOP) aktif: " + ", ".join(aktif))
            audit("tombol_berhenti", {"file": aktif})
        if state.get("berhenti"):
            if not state.get("notif_berhenti_terkirim"):
                state["notif_berhenti_terkirim"] = True
                pesan.append(f"BOT BERHENTI. Alasan: {state['alasan_berhenti']}")
                pesan.append("Tidak ada order baru. Untuk melanjutkan, tinjau dulu lalu minta agen menjalankan "
                             "berhenti.py --lanjutkan.")
                return selesai(3)
            return selesai(0)

        kunci = None
        if mode == "live":
            if not args.izinkan_live:
                hentikan(state, "Mode live dipanggil tanpa --izinkan-live.")
                audit("live_ditolak", {"alasan": "tanpa --izinkan-live"})
                pesan.append("Mode live ditolak: perintah tidak memuat --izinkan-live.")
                return selesai(3)
            tolak = periksa_konfirmasi_live(cfg, state, folder_bot, sekarang)
            if tolak:
                hentikan(state, tolak)
                audit("live_ditolak", {"alasan": tolak})
                pesan.append(tolak)
                return selesai(3)
        if mode in ("testnet", "live"):
            try:
                kunci = muat_kunci(cfg, FOLDER_SKILL)
            except ErrorKunci as e:
                hentikan(state, f"Masalah kunci API: {e}")
                audit("kunci_bermasalah", {"pesan": str(e)})
                pesan.append(f"Masalah kunci API: {e}")
                return selesai(3)
            penyamar.rahasia = [r for r in kunci.rahasia() if len(r) >= 6]

        adapter = buat_adapter(cfg, kunci, D(args.harga) if args.harga else None, args.url_uji)
        try:
            if hasattr(adapter, "sinkron_waktu") and mode != "paper":
                adapter.sinkron_waktu()
            if mode != "paper" and state.get("izin_kunci_dicek_hari") != sekarang.astimezone(WIB).date().isoformat():
                izin = adapter.cek_izin_kunci()
                audit("cek_izin_kunci", izin)
                if izin.get("lolos") is False:
                    alasan = "Kunci API tidak lolos pemeriksaan: " + "; ".join(izin.get("masalah") or [izin.get("catatan", "")])
                    hentikan(state, alasan)
                    pesan.append(alasan)
                    return selesai(3)
                state["izin_kunci_dicek_hari"] = sekarang.astimezone(WIB).date().isoformat()
            aturan = adapter.aturan_simbol()
            harga = adapter.harga()
            if not harga.is_finite() or harga <= 0:
                raise ErrorBursa(f"harga tidak wajar ({harga})")
        except (ErrorBursa, KeyError, IndexError, ValueError, TypeError, ArithmeticError) as e:
            audit("gagal_data", {"pesan": str(e)})
            if not state.get("gagal_data_dilaporkan"):
                state["gagal_data_dilaporkan"] = True
                pesan.append(f"Tidak bisa mengambil data bursa: {str(e).rstrip('.')}. Tidak ada order dijalankan putaran ini.")
                return selesai(2)
            return selesai(0)
        if state.pop("gagal_data_dilaporkan", False):
            pesan.append("Data bursa sudah bisa diambil lagi.")
        if aturan.get("status") not in (None, "TRADING"):
            audit("pasar_tidak_aktif", aturan)
            pesan.append(f"Pasar {cfg['pasangan']} sedang tidak aktif ({aturan.get('status')}). Tidak ada order.")
            return selesai(2)
        ds = cfg["_d"]
        if "langkah_jumlah" in aturan:
            ds["langkah_jumlah"] = max(ds["langkah_jumlah"], aturan["langkah_jumlah"])
        if "min_nilai_order" in aturan:
            ds["min_nilai_order"] = max(ds["min_nilai_order"], aturan["min_nilai_order"])

        state["jumlah_tick"] = int(state.get("jumlah_tick", 0)) + 1
        if mode == "paper":
            b = state.setdefault("tick_paper_per_sidik", {})
            b[sj] = int(b.get(sj, 0)) + 1
            if not (args.harga or args.sekarang or args.url_uji):
                bn = state.setdefault("paper_nyata_per_sidik", {}).setdefault(sj, {"jumlah": 0})
                bn["jumlah"] = int(bn.get("jumlah", 0)) + 1
                bn.setdefault("pertama", sekarang.isoformat(timespec="seconds"))
                if bn.get("terakhir") is None or sekarang.isoformat() > bn["terakhir"]:
                    bn["terakhir"] = sekarang.isoformat(timespec="seconds")
        audit("putaran", {"mode": mode, "harga": teks(harga), "sidik": sj})

        alasan_henti, paksa = cek_risiko_awal(cfg, state, harga, sekarang)
        if state.get("jam_mundur_terdeteksi"):
            audit("jam_mundur", {"jam_komputer": sekarang.isoformat(), "dipakai": state.get("waktu_terakhir")})
            if state.get("peringatan_jam_mundur") != state.get("hari"):
                state["peringatan_jam_mundur"] = state.get("hari")
                pesan.append(f"PERINGATAN: jam komputer mundur (sekarang {sekarang.isoformat(timespec='minutes')}, "
                             f"putaran terakhir {state.get('waktu_terakhir')}). Batas rugi harian tetap dihitung "
                             f"untuk tanggal {state.get('hari')} (tidak di-reset). Periksa pengaturan jam/NTP mesin bot.")
        daftar = [paksa] if paksa else ([] if alasan_henti else rencanakan(cfg, state, harga, sekarang))
        paparan = None
        if mode == "live":
            # Rekonsiliasi dengan SALDO BURSA (baca-saja): koin milik bot = saldo sekarang - saldo awal
            # (dicatat di buku live pada putaran live pertama). Modal terpakai = max(buku bot, saldo bursa).
            try:
                saldo = adapter.saldo_koin()
                if state.get("saldo_koin_awal_bursa") in (None, ""):
                    state["saldo_koin_awal_bursa"] = teks(max(NOL, saldo - D(state["posisi_koin"])))
                    audit("saldo_awal_live", {"saldo_koin_awal_bursa": state["saldo_koin_awal_bursa"]})
                paparan = max(NOL, saldo - D(state["saldo_koin_awal_bursa"])) * harga
            except (ErrorBursa, KeyError, ValueError, TypeError, ArithmeticError) as e:
                audit("saldo_bursa_gagal", {"pesan": str(e)})
                if any(n["sisi"] == "beli" for n in daftar):
                    pesan.append("Saldo bursa tidak bisa dicek untuk batas modal total; order BELI dilewati "
                                 "putaran ini (tidak ada pembelian tanpa pengecekan).")
                daftar = [n for n in daftar if n["sisi"] != "beli"]
        order_terbuka = adapter.jumlah_order_terbuka() if daftar else 0
        for niat in daftar:
            status, ket = cek_niat(cfg, state, niat, harga, order_terbuka, paparan)
            if status == "lewati":
                audit("niat_dilewati", {"niat": niat, "alasan": ket})
                continue
            if status == "berhenti":
                alasan_henti = ket
                audit("batas_risiko", {"niat": niat, "alasan": ket})
                break
            try:
                if niat["sisi"] == "beli":
                    isi = adapter.order_pasar("beli", nilai_kutipan=niat["nilai_kutipan"], langkah=ds["langkah_jumlah"])
                else:
                    isi = adapter.order_pasar("jual", jumlah_koin=niat["jumlah_koin"], langkah=ds["langkah_jumlah"])
            except StatusTidakPasti as e:
                alasan_henti = f"STATUS ORDER TIDAK PASTI: {e}"
                audit("order_tidak_pasti", {"niat": niat, "pesan": str(e)})
                break
            except ErrorBursa as e:
                alasan_henti = f"Order ditolak bursa: {e}"
                audit("order_ditolak", {"niat": niat, "pesan": str(e)})
                break
            pl = terapkan_isi(state, isi, kut)
            if paparan is not None and isi["sisi"] == "beli":
                paparan += isi["bersih"]          # saldo bursa di atas diambil sebelum order ini
            catat_niat_berhasil(state, niat, isi, sekarang)
            tulis_transaksi(p_trx, {
                "waktu": sekarang.isoformat(timespec="seconds"), "mode": mode, "bursa": cfg["bursa"],
                "pasangan": cfg["pasangan"], "sisi": isi["sisi"], "jumlah_koin": teks(isi["jumlah"]),
                "harga": teks(isi["harga"]), "bruto": teks(isi["bruto"]), "fee": teks(isi["fee"]),
                "pajak_pph": teks(isi["pajak"]), "bersih": teks(isi["bersih"]),
                "realized_pl": teks(pl) if isi["sisi"] == "jual" else "", "alasan": niat["alasan"],
                "order_id": isi.get("order_id", ""), "sumber_angka": isi.get("sumber_angka", ""),
                "catatan": isi.get("catatan", "")})
            audit("transaksi", {k: (teks(v) if hasattr(v, "quantize") else v) for k, v in isi.items()})
            kata = "BELI" if isi["sisi"] == "beli" else "JUAL"
            baris = (f"{kata} {teks(isi['jumlah'])} {cfg['koin']} @ {rp(isi['harga'], kut)} | "
                     f"{'bayar' if isi['sisi'] == 'beli' else 'terima bersih'} {rp(isi['bersih'], kut)} "
                     f"(fee {rp(isi['fee'], kut)}" + (f", PPh {rp(isi['pajak'], kut)}" if isi["pajak"] else "") + ")")
            baris += f"\n  Aturan Anda: {niat['alasan']}"
            if isi["sisi"] == "jual":
                baris += f"\n  Untung/rugi transaksi ini: {rp(pl, kut)}"
            if cfg["_jenis"] == "grid" and isi["sisi"] == "jual":
                baris += ("\n  Catatan: untung/rugi dihitung dari harga rata-rata SEMUA koin bot, bukan harga beli "
                          "slot ini saja (slot yang dijual di atas harga belinya bisa tercatat rugi).")
            if isi.get("sumber_angka") == "estimasi":
                baris += "\n  Catatan: angka ESTIMASI, cocokkan dengan riwayat di aplikasi bursa."
            pesan.append(baris)
            if niat.get("alasan") == "stop-loss global":
                break
        if alasan_henti:
            hentikan(state, alasan_henti)
            state["notif_berhenti_terkirim"] = True
            audit("bot_berhenti", {"alasan": alasan_henti})
            pesan.append(f"BOT BERHENTI. Alasan: {alasan_henti}")
            pesan.append("Tidak ada order baru sampai Anda meninjau dan melanjutkan (berhenti.py --lanjutkan).")
        if pesan:
            e = ekuitas(state, harga)
            pesan.append(f"Ringkasan bot: kas {rp(D(state['kas']), kut)}, koin {teks(D(state['posisi_koin']))} "
                         f"{cfg['koin']}, nilai total {rp(e, kut)} (harga {rp(harga, kut)}), untung/rugi terealisasi "
                         f"{rp(D(state['realized_pl']), kut)}.")
        return selesai(3 if alasan_henti else (2 if pesan else 0))
    finally:
        try:
            os.remove(p_kunci)
        except OSError:
            pass


def main(argv=None):
    ap = argparse.ArgumentParser(description="Jalankan satu putaran bot trading kripto (aturan milik member).")
    ap.add_argument("--konfigurasi", required=True)
    ap.add_argument("--folder-bot", help="default: folder file konfigurasi. Tombol berhenti tetap dicek juga di "
                                         "folder konfigurasi & " + folder_stop_global())
    ap.add_argument("--openclaw", action="store_true", help="selalu exit 0 (untuk jadwal OpenClaw)")
    ap.add_argument("--izinkan-live", action="store_true", help="wajib untuk mode live")
    ap.add_argument("--harga", help="UJI: harga manual (hanya mode paper)")
    ap.add_argument("--sekarang", help="UJI: waktu ISO 8601")
    ap.add_argument("--url-uji", help="UJI: server tiruan lokal (hanya localhost)")
    args = ap.parse_args(argv)
    try:
        if args.harga:
            angka(args.harga, "--harga")
        kode, keluaran = satu_putaran(args)
    except KonfigurasiTidakValid as e:
        kode, keluaran = 1, f"Bot kripto: konfigurasi bermasalah, TIDAK ada order dijalankan.\n{e}"
    except ValueError as e:
        kode, keluaran = 1, f"Bot kripto: input bermasalah, TIDAK ada order dijalankan.\n{e}"
    except Exception as e:  # noqa: BLE001 -- jangan pernah mengirim traceback ke member/OpenClaw
        kode, keluaran = 1, (f"Bot kripto: kesalahan tak terduga ({type(e).__name__}), TIDAK ada order dijalankan "
                             "putaran ini. Periksa konfigurasi & bot/audit.jsonl; bila berulang, hentikan bot "
                             "(berhenti.py) dan hubungi dukungan Komunitech.")
    print(Penyamar()(keluaran))
    return 0 if args.openclaw else kode


if __name__ == "__main__":
    sys.exit(main())
