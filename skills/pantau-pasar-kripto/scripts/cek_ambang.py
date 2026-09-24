#!/usr/bin/env python3
"""Cek harga kripto vs ambang yang ditetapkan member, tanpa API key. (v1.0.1)

Sumber data publik (tanpa kunci):
- CoinGecko `simple/price`  https://docs.coingecko.com/reference/simple-price
  Endpoint: https://api.coingecko.com/api/v3/simple/price
  Dipakai untuk harga USD/IDR + persentase perubahan 24 jam (field bawaan API).
  Semua koin yang sumbernya CoinGecko diambil dalam **satu permintaan batch**
  (`ids=a,b,c&vs_currencies=idr,usd`), bukan satu permintaan per koin -- supaya tidak
  gampang kena batas laju (HTTP 429) saat daftar pantau berisi banyak koin.
- Indodax `ticker/<pair>`   https://github.com/btcid/indodax-official-api-docs/blob/master/Public-REST-API.md
  Endpoint: https://indodax.com/api/ticker/<pair>
  Dipakai sebagai harga pasar lokal (Rupiah) opsional, TANPA field perubahan 24 jam
  (Indodax tidak menyediakannya di endpoint publik ini) -- karena itu ambang persen untuk
  sumber Indodax HANYA bisa dihitung kalau member menetapkan `harga_acuan` sendiri di
  konfigurasi (lihat README/SKILL.md), bukan otomatis dari 24 jam terakhir.

ATURAN KERAS: skrip ini TIDAK PERNAH mengarang harga. Kalau sumber gagal dan tidak ada
data cache yang tersimpan, koin itu ditandai "gagal_total" dan tidak diberi angka apa pun.
Kalau memakai data cache (karena sumber hidup gagal), itu ditandai jelas sebagai data basi
lengkap dengan jam datanya. Data yang BERHASIL diambil tapi ternyata sudah lama (mis. API
belum memperbarui) juga diberi peringatan yang sama, bukan didiamkan begitu saja.

Mode:
- Online (default): mengambil harga langsung dari CoinGecko/Indodax lewat urllib (stdlib saja).
- Offline uji (`--harga-file`): membaca harga dari file JSON lokal, tanpa jaringan sama sekali.
  Format file harga (per kunci "<coingecko_id_atau_kode>_<mata_uang>_<sumber>"; sumber
  disertakan di kunci supaya koin yang sama tidak bentrok cache-nya kalau dipantau dari dua
  sumber berbeda -- lihat `kunci_koin()`):
  {
    "bitcoin_idr_coingecko": {"harga": 1500000000, "perubahan_24jam_persen": -2.3,
                     "jam_data": "2026-09-24T10:00:00+07:00", "sumber": "coingecko"},
    "ethereum_usd_coingecko": {"harga": 2650.5, "perubahan_24jam_persen": 1.2,
                      "jam_data": "2026-09-24T10:00:00+07:00", "sumber": "coingecko"}
  }
  Koin yang TIDAK ada di file ini dianggap "sumber gagal" untuk uji skenario itu.

Konfigurasi (`--konfigurasi`): field ambang/harga (`ambang_naik_persen`,
`ambang_turun_persen`, `ambang_harga_di_atas`, `ambang_harga_di_bawah`, `harga_acuan`)
boleh ditulis sebagai angka ATAU teks, termasuk format Indonesia dan tanda persen, mis.
`"5%"`, `"1.450.000.000"`, `"1.450.000,50"` -- semua dirapikan otomatis (lihat
`_parse_angka_konfigurasi`). Semua ambang & harga_acuan WAJIB lebih besar dari 0.

Keluaran: satu objek JSON ke stdout, termasuk field `pesan_singkat` siap tempel/kirim
(sudah memuat sumber, jam data, dan peringatan data basi per koin), dan kode keluar (exit
code) yang berbeda supaya automation OpenClaw tahu kapan harus memanggil agent/mengirim
pesan (lihat `references/openclaw-jadwal.md` & `scripts/cek_dan_lapor.py`):
  0 = sukses, TIDAK ADA yang perlu dilaporkan sekarang (tidak ada ambang baru terlewati)
  2 = sukses, ADA ambang yang BARU terlewati (atau sudah lama & jeda lapor-ulang habis)
      -- ini yang dipakai automation untuk memutuskan kapan mengumumkan/memanggil agent
  3 = sukses sebagian: ada koin yang gagal total (tanpa cache) -- tetap cek koin lain
  1 = error input/konfigurasi (file konfigurasi tidak ada/rusak, kolom wajib kurang)
Catatan: field JSON `ambang_terlewati` (per koin & ringkasan) selalu menunjukkan fakta apa
adanya (ambang sedang terlampaui atau tidak), TERLEPAS dari apakah sudah pernah dilaporkan.
Field `perlu_lapor` yang membedakan "baru/perlu diumumkan sekarang" dari "sudah pernah
dilaporkan, diredam sementara" (anti-spam, lihat `--jeda-ulang-jam`) -- exit code 2 hanya
mengikuti `perlu_lapor`, bukan `ambang_terlewati` mentah, supaya automation berkala (mis.
tiap jam) tidak mengumumkan hal yang sama berulang-ulang selama kondisi belum berubah.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

WIB = timezone(timedelta(hours=7))

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
INDODAX_URL_TMPL = "https://indodax.com/api/ticker/{pair}"


# ---------------------------------------------------------------------------
# Util angka & format
# ---------------------------------------------------------------------------

def bulat_setengah_ke_atas(nilai, digit=0):
    """Pembulatan matematis biasa (0,5 ke atas), BUKAN pembulatan genap Python.

    Dipakai untuk semua angka Rupiah yang ditampilkan (dibulatkan ke rupiah terdekat,
    sesuai standar CLAUDE.md), dan untuk persentase (dibulatkan 2 desimal untuk tampilan).
    """
    if nilai is None:
        return None
    faktor = 10 ** digit
    from decimal import Decimal, ROUND_HALF_UP
    d = Decimal(str(nilai)) * faktor
    d = d.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    hasil = float(d) / faktor
    if digit <= 0:
        return int(hasil)
    return hasil


def format_rupiah(nilai):
    bulat = bulat_setengah_ke_atas(nilai, 0)
    negatif = bulat < 0
    bulat = abs(bulat)
    s = f"{bulat:,}".replace(",", ".")
    return f"{'-' if negatif else ''}Rp {s}"


def format_usd(nilai):
    s = f"{nilai:,.2f}"
    # gaya Indonesia: titik untuk ribuan, koma untuk desimal
    s = s.replace(",", "@").replace(".", ",").replace("@", ".")
    return f"US$ {s}"


def formatter_untuk(mata_uang):
    return format_rupiah if mata_uang.upper() == "IDR" else format_usd


def format_angka_ringkas(nilai):
    """'5.0' -> '5', '5.5' -> '5,5' -- dipakai untuk menyebut ambang di pesan (ambang
    ditulis apa adanya oleh member, seringnya bilangan bulat; hindari akhiran '.0')."""
    if nilai == int(nilai):
        return str(int(nilai))
    return f"{nilai}".replace(".", ",")


def format_persen(nilai):
    if nilai is None:
        return "-"
    tanda = "+" if nilai >= 0 else ""
    angka = f"{bulat_setengah_ke_atas(nilai, 2):.2f}".replace(".", ",")
    return f"{tanda}{angka}%"


def sumber_efektif(cfg_koin):
    """Tentukan sumber yang akan dipakai untuk koin ini (tanpa jaringan)."""
    sumber = cfg_koin.get("sumber")
    mata_uang = cfg_koin["mata_uang"].lower()
    if sumber == "indodax" or (sumber is None and mata_uang == "idr" and cfg_koin.get("indodax_pair")):
        return "indodax"
    return "coingecko"


def kunci_koin(cfg_koin):
    """Kunci cache/state, MENYERTAKAN sumber -- supaya koin yang sama dipantau dari 2
    sumber berbeda (mis. CoinGecko utk USD & Indodax utk IDR) tidak berbagi/bentrok cache."""
    dasar = cfg_koin.get("coingecko_id") or cfg_koin.get("kode", "").lower()
    return f"{dasar}_{cfg_koin['mata_uang'].lower()}_{sumber_efektif(cfg_koin)}"


def hitung_persen_perubahan(harga_sekarang, harga_acuan):
    if not harga_acuan:
        return None
    return (harga_sekarang - harga_acuan) / harga_acuan * 100.0


def waktu_wib_sekarang():
    return datetime.now(WIB)


def parse_waktu(teks):
    try:
        return datetime.fromisoformat(teks)
    except Exception:
        return None


def usia_jam(jam_data_teks, sekarang):
    t = parse_waktu(jam_data_teks)
    if t is None:
        return None
    if t.tzinfo is None:
        t = t.replace(tzinfo=WIB)
    delta = sekarang - t
    return delta.total_seconds() / 3600.0


def _parse_angka_konfigurasi(nilai, label):
    """Terima angka langsung, atau teks: '5%', '1.450.000.000', '1.450.000,50', '5'.

    Dipakai untuk field ambang & harga_acuan di konfigurasi.json (BUKAN untuk data harga
    dari API/--harga-file, yang selalu murni angka). Selalu mengembalikan float > 0, atau
    melempar KesalahanInput dengan pesan yang menyebut field mana yang bermasalah.
    """
    if isinstance(nilai, (int, float)) and not isinstance(nilai, bool):
        hasil = float(nilai)
    else:
        s = str(nilai).strip()
        if s == "":
            raise KesalahanInput(f"{label}: nilai kosong.")
        s = s.replace("%", "").replace(" ", "")
        s = s.replace("Rp", "").replace("rp", "").replace("US$", "").replace("us$", "")
        try:
            if "," in s and "." in s:
                s = s.replace(".", "").replace(",", ".")
            elif "," in s:
                s = s.replace(",", ".")
            elif "." in s:
                bagian = s.split(".")
                if len(bagian) > 2 or len(bagian[-1]) == 3:
                    s = s.replace(".", "")
            hasil = float(s)
        except ValueError:
            raise KesalahanInput(f"{label}: '{nilai}' bukan angka yang bisa dibaca.")
    if hasil <= 0:
        raise KesalahanInput(f"{label}: harus lebih besar dari 0, dapat {hasil}.")
    return hasil


# ---------------------------------------------------------------------------
# Muat & validasi konfigurasi
# ---------------------------------------------------------------------------

class KesalahanInput(Exception):
    pass


def muat_json(path, wajib=True, nama="file"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        if wajib:
            raise KesalahanInput(f"{nama} tidak ditemukan: {path}")
        return {}
    except json.JSONDecodeError as e:
        raise KesalahanInput(f"{nama} berisi JSON yang rusak ({path}): {e}")


FIELD_ANGKA = ("ambang_naik_persen", "ambang_turun_persen", "ambang_harga_di_atas",
               "ambang_harga_di_bawah", "harga_acuan")


def validasi_konfigurasi(cfg):
    if not isinstance(cfg, dict) or "koin" not in cfg:
        raise KesalahanInput("Konfigurasi tidak valid: field 'koin' (daftar) wajib ada.")
    daftar = cfg["koin"]
    if not isinstance(daftar, list) or not daftar:
        raise KesalahanInput("Konfigurasi tidak valid: 'koin' harus daftar berisi minimal 1 koin.")
    for i, k in enumerate(daftar):
        for wajib in ("kode", "mata_uang"):
            if wajib not in k or not k[wajib]:
                raise KesalahanInput(f"Koin ke-{i+1} kurang field wajib '{wajib}'.")
        if k["mata_uang"].lower() not in ("idr", "usd"):
            raise KesalahanInput(
                f"Koin '{k['kode']}': mata_uang harus 'idr' atau 'usd', dapat '{k['mata_uang']}'."
            )
        for field in FIELD_ANGKA:
            if k.get(field) is not None:
                k[field] = _parse_angka_konfigurasi(k[field], f"Koin '{k['kode']}', field '{field}'")
        ada_ambang = any(k.get(f) is not None for f in FIELD_ANGKA if f != "harga_acuan")
        if not ada_ambang:
            raise KesalahanInput(
                f"Koin '{k['kode']}': tidak ada ambang sama sekali "
                "(isi minimal salah satu: ambang_naik_persen/ambang_turun_persen/"
                "ambang_harga_di_atas/ambang_harga_di_bawah)."
            )
    return daftar


# ---------------------------------------------------------------------------
# Pengambilan harga (online)
# ---------------------------------------------------------------------------

def _tunggu_retry_429(retry_after_header, percobaan_ke):
    """Fungsi murni (tanpa I/O) supaya bisa diuji offline: berapa detik menunggu setelah
    HTTP 429, memakai header Retry-After kalau ada dan masuk akal, atau backoff bertahap."""
    if retry_after_header:
        try:
            nilai = float(retry_after_header)
            if nilai >= 0:
                return min(nilai, 15.0)
        except (TypeError, ValueError):
            pass
    return min(2.0 ** percobaan_ke, 15.0)


def _ambil_url_json(url, timeout, percobaan):
    kesalahan_terakhir = None
    for i in range(max(1, percobaan)):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "komunitech-pantau-pasar-kripto/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            kesalahan_terakhir = e
            if i < percobaan - 1:
                retry_after = e.headers.get("Retry-After") if e.headers else None
                if e.code == 429:
                    time.sleep(_tunggu_retry_429(retry_after, i))
                else:
                    time.sleep(min(2 ** i, 4))
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            kesalahan_terakhir = e
            if i < percobaan - 1:
                time.sleep(min(2 ** i, 4))
    raise RuntimeError(str(kesalahan_terakhir))


def _jam_dari_unix(ts):
    return (
        datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(WIB).isoformat()
        if ts else waktu_wib_sekarang().isoformat()
    )


def ambil_batch_coingecko(coingecko_ids, daftar_mata_uang, timeout, percobaan):
    """Satu permintaan untuk BANYAK koin sekaligus (hemat kuota, menghindari 429)."""
    if not coingecko_ids:
        return {}
    ids = ",".join(sorted(set(coingecko_ids)))
    mu = ",".join(sorted({m.lower() for m in daftar_mata_uang}))
    url = (
        f"{COINGECKO_URL}?ids={ids}&vs_currencies={mu}"
        "&include_24hr_change=true&include_last_updated_at=true"
    )
    return _ambil_url_json(url, timeout, percobaan)


def _bentuk_hasil_dari_batch_coingecko(batch, coingecko_id, mata_uang):
    mata_uang = mata_uang.lower()
    if batch is None or coingecko_id not in batch or mata_uang not in batch[coingecko_id]:
        raise RuntimeError(f"CoinGecko tidak mengembalikan data untuk '{coingecko_id}'/{mata_uang}.")
    d = batch[coingecko_id]
    return {
        "harga": d[mata_uang],
        "perubahan_24jam_persen": d.get(f"{mata_uang}_24h_change"),
        "jam_data": _jam_dari_unix(d.get("last_updated_at")),
        "sumber": "coingecko",
    }


def ambil_harga_coingecko(coingecko_id, mata_uang, timeout, percobaan):
    """Ambil satu koin saja (dipakai bila hanya ada 1 koin CoinGecko, atau utk uji unit)."""
    batch = ambil_batch_coingecko([coingecko_id], [mata_uang], timeout, percobaan)
    return _bentuk_hasil_dari_batch_coingecko(batch, coingecko_id, mata_uang)


def ambil_harga_indodax(pair, timeout, percobaan):
    url = INDODAX_URL_TMPL.format(pair=pair)
    data = _ambil_url_json(url, timeout, percobaan)
    if "ticker" not in data or "last" not in data["ticker"]:
        raise RuntimeError(f"Indodax tidak mengembalikan data ticker untuk pair '{pair}'.")
    t = data["ticker"]
    return {
        "harga": float(t["last"]),
        "perubahan_24jam_persen": None,  # Indodax ticker publik tidak menyediakan ini
        "jam_data": _jam_dari_unix(t.get("server_time")),
        "sumber": "indodax",
    }


def ambil_data_untuk_koin(cfg_koin, harga_file_data, batch_coingecko, batch_error, timeout, percobaan):
    """Kembalikan (data_baru_dict_atau_None, pesan_kesalahan_atau_None). Tidak menyentuh state."""
    if harga_file_data is not None:
        kk = kunci_koin(cfg_koin)
        data = harga_file_data.get(kk)
        if data is None:
            return None, f"Tidak ada entri '{kk}' di --harga-file (disimulasikan sebagai sumber gagal)."
        return data, None

    if sumber_efektif(cfg_koin) == "coingecko":
        coingecko_id = cfg_koin.get("coingecko_id") or cfg_koin["kode"].lower()
        mata_uang = cfg_koin["mata_uang"].lower()
        if batch_coingecko is None:
            return None, f"Gagal mengambil harga (permintaan batch CoinGecko gagal): {batch_error}"
        try:
            return _bentuk_hasil_dari_batch_coingecko(batch_coingecko, coingecko_id, mata_uang), None
        except Exception as e:  # noqa: BLE001
            return None, f"Gagal mengambil harga: {e}"
    else:
        pair = cfg_koin.get("indodax_pair") or f"{cfg_koin['kode'].lower()}idr"
        try:
            return ambil_harga_indodax(pair, timeout, percobaan), None
        except Exception as e:  # noqa: BLE001
            return None, f"Gagal mengambil harga langsung: {e}"


# ---------------------------------------------------------------------------
# Evaluasi ambang
# ---------------------------------------------------------------------------

def evaluasi_ambang(cfg_koin, harga_sekarang, persen_perubahan, mata_uang):
    """Kembalikan (terlewati, detail_terpicu, tidak_bisa_dicek)."""
    fmt = formatter_untuk(mata_uang)
    detail = []
    tidak_bisa = []
    terlewati = False

    naik = cfg_koin.get("ambang_naik_persen")
    turun = cfg_koin.get("ambang_turun_persen")
    if naik is not None or turun is not None:
        if persen_perubahan is not None:
            if naik is not None and persen_perubahan >= naik:
                terlewati = True
                detail.append(f"Naik {format_persen(persen_perubahan)} (ambang naik {format_angka_ringkas(naik)}%).")
            if turun is not None and persen_perubahan <= -abs(turun):
                terlewati = True
                detail.append(f"Turun {format_persen(persen_perubahan)} (ambang turun {format_angka_ringkas(turun)}%).")
        else:
            tidak_bisa.append(
                "ambang naik/turun %: tidak ada dasar pembanding (data dari cache tanpa "
                "perubahan 24 jam, atau sumber Indodax tanpa 'harga_acuan' di konfigurasi)."
            )

    di_atas = cfg_koin.get("ambang_harga_di_atas")
    di_bawah = cfg_koin.get("ambang_harga_di_bawah")
    if di_atas is not None and harga_sekarang >= di_atas:
        terlewati = True
        detail.append(f"Harga sudah {fmt(harga_sekarang)}, >= ambang atas {fmt(di_atas)}.")
    if di_bawah is not None and harga_sekarang <= di_bawah:
        terlewati = True
        detail.append(f"Harga sudah {fmt(harga_sekarang)}, <= ambang bawah {fmt(di_bawah)}.")

    return terlewati, detail, tidak_bisa


def perbarui_status_notifikasi(notif_map, kk_notif, terlewati, sekarang, jeda_ulang_jam):
    """Anti-spam: kembalikan True hanya kalau ambang ini BARU terlewati, atau sudah
    terlewati sejak sebelumnya tapi jeda lapor-ulang (`jeda_ulang_jam`) sudah habis.
    Direset (boleh lapor lagi kapan saja) begitu kondisi kembali normal."""
    entri_lama = notif_map.get(kk_notif) or {}
    prev_terlewati = bool(entri_lama.get("terlewati"))
    prev_pada = entri_lama.get("pada")

    if not terlewati:
        notif_map[kk_notif] = {
            "terlewati": False,
            "pada": sekarang.isoformat() if prev_terlewati else (prev_pada or sekarang.isoformat()),
        }
        return False

    if not prev_terlewati:
        lapor = True
    else:
        usia = usia_jam(prev_pada, sekarang) if prev_pada else None
        lapor = usia is None or usia >= jeda_ulang_jam

    notif_map[kk_notif] = {"terlewati": True, "pada": sekarang.isoformat() if lapor else prev_pada}
    return lapor


# ---------------------------------------------------------------------------
# Proses satu koin
# ---------------------------------------------------------------------------

def proses_koin(cfg_koin, indeks, sekarang, data_baru, kesalahan, state, usia_basi_jam, jeda_ulang_jam):
    kk = kunci_koin(cfg_koin)
    kk_notif = f"{kk}#{indeks}"
    mata_uang = cfg_koin["mata_uang"].upper()
    hasil = {
        "kode": cfg_koin["kode"],
        "mata_uang": mata_uang,
        "status": None,
        "harga": None,
        "harga_format": None,
        "sumber": None,
        "jam_data": None,
        "usia_data_jam": None,
        "perubahan_24jam_persen": None,
        "persen_vs_acuan": None,
        "harga_acuan": cfg_koin.get("harga_acuan"),
        "ambang_terlewati": False,
        "perlu_lapor": False,
        "detail_pemicu": [],
        "ambang_tidak_bisa_dicek": [],
        "peringatan": [],
    }

    entri_cache = state.setdefault(kk, {})

    if data_baru is not None:
        hasil["status"] = "hidup"
        hasil["harga"] = data_baru["harga"]
        hasil["sumber"] = data_baru["sumber"]
        hasil["jam_data"] = data_baru["jam_data"]
        hasil["perubahan_24jam_persen"] = data_baru.get("perubahan_24jam_persen")
        usia = usia_jam(data_baru["jam_data"], sekarang)
        hasil["usia_data_jam"] = round(usia, 2) if usia is not None else 0.0
        if usia is not None and usia > usia_basi_jam:
            hasil["peringatan"].append(
                f"Data ini BERHASIL diambil tapi sudah berumur ±{hasil['usia_data_jam']} jam "
                f"(lebih tua dari batas {usia_basi_jam} jam) -- sumbernya kemungkinan belum "
                "memperbarui harga, jangan dianggap harga saat ini tanpa cek ulang."
            )
        entri_cache["harga_terakhir"] = data_baru["harga"]
        entri_cache["jam_data_terakhir"] = data_baru["jam_data"]
        entri_cache["sumber_terakhir"] = data_baru["sumber"]
    else:
        if entri_cache.get("harga_terakhir") is not None:
            hasil["status"] = "cache"
            hasil["harga"] = entri_cache["harga_terakhir"]
            hasil["sumber"] = f"{entri_cache['sumber_terakhir']} (cache)"
            hasil["jam_data"] = entri_cache["jam_data_terakhir"]
            usia = usia_jam(entri_cache["jam_data_terakhir"], sekarang)
            hasil["usia_data_jam"] = round(usia, 2) if usia is not None else None
            hasil["peringatan"].append(
                f"DATA BASI: {kesalahan} Menampilkan harga cache dari {entri_cache['jam_data_terakhir']} "
                f"(±{hasil['usia_data_jam']} jam lalu)."
            )
            if usia is not None and usia > usia_basi_jam:
                hasil["peringatan"].append(
                    f"Cache sudah lebih tua dari batas {usia_basi_jam} jam -- jangan dianggap harga saat ini."
                )
        else:
            hasil["status"] = "gagal_total"
            hasil["peringatan"].append(f"GAGAL TOTAL, tidak ada cache tersimpan: {kesalahan}")

    if hasil["harga"] is not None:
        hasil["harga_format"] = formatter_untuk(mata_uang)(hasil["harga"])
        acuan = cfg_koin.get("harga_acuan")
        if acuan:
            hasil["persen_vs_acuan"] = hitung_persen_perubahan(hasil["harga"], acuan)
            persen_pakai = hasil["persen_vs_acuan"]
        else:
            persen_pakai = hasil["perubahan_24jam_persen"]
        terlewati, detail, tidak_bisa = evaluasi_ambang(cfg_koin, hasil["harga"], persen_pakai, mata_uang)
        hasil["ambang_terlewati"] = terlewati
        hasil["detail_pemicu"] = detail
        hasil["ambang_tidak_bisa_dicek"] = tidak_bisa

        notif_map = state.setdefault("_notifikasi", {})
        hasil["perlu_lapor"] = perbarui_status_notifikasi(notif_map, kk_notif, terlewati, sekarang, jeda_ulang_jam)

    return hasil


# ---------------------------------------------------------------------------
# Pesan singkat
# ---------------------------------------------------------------------------

def susun_pesan_singkat(daftar_hasil, sekarang, peringatan_global):
    baris = [f"Pantau harga kripto -- {sekarang.strftime('%d %b %Y %H:%M')} WIB"]
    for p in peringatan_global:
        baris.append(f"⚠️ {p}")

    ada_pemicu = False
    koin_bermasalah = []  # (kode, alasan) -- gagal total ATAU ambang % tidak bisa dicek
    koin_normal_aman = []

    for h in daftar_hasil:
        if h["status"] == "gagal_total":
            alasan = h["peringatan"][0] if h["peringatan"] else "tidak diketahui"
            baris.append(f"- {h['kode']}: TIDAK BISA DICEK -- {alasan}")
            koin_bermasalah.append(h["kode"])
            continue

        tanda = " ⚠️ DATA BASI" if h["status"] == "cache" else ""
        perubahan = h["perubahan_24jam_persen"]
        teks_perubahan = f" ({format_persen(perubahan)} / 24 jam)" if perubahan is not None else ""
        baris.append(
            f"- {h['kode']}: {h['harga_format']}{teks_perubahan}{tanda} "
            f"[sumber: {h['sumber']}, data jam {h['jam_data']}]"
        )
        for p in h["peringatan"]:
            baris.append(f"  ⚠️ {p}")

        if h["ambang_terlewati"]:
            ada_pemicu = True
            if h["perlu_lapor"]:
                for d in h["detail_pemicu"]:
                    baris.append(f"  >> AMBANG TERLEWATI: {d}")
            else:
                baris.append(
                    "  (ambang masih terlewati, tapi sudah pernah dilaporkan -- diredam "
                    "sampai jeda lapor-ulang habis, lihat --jeda-ulang-jam)"
                )
        elif h["ambang_tidak_bisa_dicek"]:
            koin_bermasalah.append(h["kode"])
            for t in h["ambang_tidak_bisa_dicek"]:
                baris.append(f"  (tidak bisa dicek: {t})")
        else:
            koin_normal_aman.append(h["kode"])

    if not ada_pemicu:
        if koin_bermasalah:
            baris.append(
                f"Tidak ada ambang yang terlewati untuk koin yang berhasil dicek "
                f"({', '.join(koin_normal_aman) if koin_normal_aman else '-'}); "
                f"TIDAK bisa dicek untuk: {', '.join(koin_bermasalah)}."
            )
        else:
            baris.append("Tidak ada ambang yang terlewati (semua koin berhasil dicek).")

    baris.append("Informasi, bukan nasihat investasi. Keputusan & risiko sepenuhnya milik Anda.")
    return "\n".join(baris)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description="Cek harga kripto vs ambang member (tanpa API key).")
    ap.add_argument("--konfigurasi", required=True, help="Path ke konfigurasi.json (daftar koin & ambang).")
    ap.add_argument("--state", required=True, help="Path ke state.json (cache harga & status notifikasi, dibuat otomatis).")
    ap.add_argument("--harga-file", default=None,
                     help="Mode offline/uji: path JSON berisi harga simulasi, tanpa jaringan sama sekali.")
    ap.add_argument("--timeout", type=float, default=8.0, help="Timeout per permintaan (detik). Default 8.")
    ap.add_argument("--percobaan", type=int, default=2, help="Jumlah percobaan per sumber. Default 2.")
    ap.add_argument("--usia-basi-jam", type=float, default=6.0,
                     help="Data lebih tua dari ini (jam) diberi peringatan tambahan, baik cache maupun data hidup. Default 6.")
    ap.add_argument("--jeda-ulang-jam", type=float, default=6.0,
                     help="Kalau ambang tetap terlewati, tunggu sekian jam sebelum melapor ulang koin yang sama (anti-spam). Default 6.")
    ap.add_argument("--keluaran", choices=["json", "teks"], default="json",
                     help="json = satu objek JSON (default, untuk automation/agent). "
                          "teks = hanya pesan_singkat ke stdout.")
    args = ap.parse_args(argv)

    try:
        cfg = muat_json(args.konfigurasi, wajib=True, nama="Konfigurasi")
        daftar_koin = validasi_konfigurasi(cfg)
        harga_file_data = None
        if args.harga_file:
            harga_file_data = muat_json(args.harga_file, wajib=True, nama="File harga (--harga-file)")
            if not isinstance(harga_file_data, dict):
                raise KesalahanInput("--harga-file rusak: isinya harus objek JSON (dict).")
    except KesalahanInput as e:
        print(json.dumps({"status": "error", "pesan": str(e)}, ensure_ascii=False, indent=2))
        return 1

    peringatan_global = []
    try:
        state = muat_json(args.state, wajib=False, nama="State")
        if not isinstance(state, dict):
            raise KesalahanInput("State bukan objek JSON (dict), melainkan tipe lain.")
    except KesalahanInput as e:
        state = {}
        try:
            if os.path.exists(args.state):
                cadangan = f"{args.state}.rusak-{int(time.time())}"
                os.replace(args.state, cadangan)
                peringatan_global.append(
                    f"State sebelumnya rusak ({e}) -- dicadangkan ke '{cadangan}' dan dimulai ulang "
                    "dari kosong (cache harga & riwayat notifikasi hilang, akan terisi lagi mulai sekarang)."
                )
        except OSError as e2:
            peringatan_global.append(
                f"State sebelumnya rusak ({e}) dan gagal dicadangkan ({e2}) -- dimulai ulang dari kosong."
            )

    sekarang = waktu_wib_sekarang()

    batch_coingecko, batch_error = None, None
    if harga_file_data is None:
        koin_coingecko = [k for k in daftar_koin if sumber_efektif(k) == "coingecko"]
        if koin_coingecko:
            ids = [k.get("coingecko_id") or k["kode"].lower() for k in koin_coingecko]
            mu = [k["mata_uang"] for k in koin_coingecko]
            try:
                batch_coingecko = ambil_batch_coingecko(ids, mu, args.timeout, args.percobaan)
            except Exception as e:  # noqa: BLE001
                batch_coingecko = None
                batch_error = str(e)
        else:
            batch_coingecko = {}

    daftar_hasil = []
    for indeks, k in enumerate(daftar_koin):
        data_baru, kesalahan = ambil_data_untuk_koin(
            k, harga_file_data, batch_coingecko, batch_error, args.timeout, args.percobaan
        )
        daftar_hasil.append(
            proses_koin(k, indeks, sekarang, data_baru, kesalahan, state, args.usia_basi_jam, args.jeda_ulang_jam)
        )

    try:
        with open(args.state, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except OSError as e:
        peringatan_global.append(f"Gagal menyimpan cache state: {e}")

    pesan_singkat = susun_pesan_singkat(daftar_hasil, sekarang, peringatan_global)

    ada_terlewati = any(h["ambang_terlewati"] for h in daftar_hasil)
    ada_perlu_lapor = any(h["ambang_terlewati"] and h["perlu_lapor"] for h in daftar_hasil)
    ada_gagal_total = any(h["status"] == "gagal_total" for h in daftar_hasil)

    keluaran = {
        "status": "ok",
        "jam_cek": sekarang.isoformat(),
        "ambang_terlewati": ada_terlewati,
        "perlu_lapor_sekarang": ada_perlu_lapor,
        "ada_koin_gagal_total": ada_gagal_total,
        "koin": daftar_hasil,
        "peringatan_global": peringatan_global,
        "pesan_singkat": pesan_singkat,
        "disclaimer": "Informasi, bukan nasihat investasi. Keputusan & risiko sepenuhnya milik Anda.",
    }

    if args.keluaran == "teks":
        print(pesan_singkat)
    else:
        print(json.dumps(keluaran, ensure_ascii=False, indent=2))

    if ada_perlu_lapor:
        return 2
    if ada_gagal_total:
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
