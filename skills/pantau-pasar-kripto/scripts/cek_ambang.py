#!/usr/bin/env python3
"""Cek harga kripto vs ambang yang ditetapkan member, tanpa API key.

Sumber data publik (tanpa kunci):
- CoinGecko `simple/price`  https://docs.coingecko.com/reference/simple-price
  Endpoint: https://api.coingecko.com/api/v3/simple/price
  Dipakai untuk harga USD/IDR + persentase perubahan 24 jam (field bawaan API).
- Indodax `ticker/<pair>`   https://github.com/btcid/indodax-official-api-docs/blob/master/Public-REST-API.md
  Endpoint: https://indodax.com/api/ticker/<pair>idr
  Dipakai sebagai harga pasar lokal (Rupiah) opsional, TANPA field perubahan 24 jam
  (Indodax tidak menyediakannya di endpoint publik ini) -- karena itu ambang persen untuk
  sumber Indodax HANYA bisa dihitung kalau member menetapkan `harga_acuan` sendiri di
  konfigurasi (lihat README/SKILL.md), bukan otomatis dari 24 jam terakhir.

ATURAN KERAS: skrip ini TIDAK PERNAH mengarang harga. Kalau sumber gagal dan tidak ada
data cache yang tersimpan, koin itu ditandai "gagal_total" dan tidak diberi angka apa pun.
Kalau memakai data cache (karena sumber hidup gagal), itu ditandai jelas sebagai data basi
lengkap dengan jam datanya.

Mode:
- Online (default): mengambil harga langsung dari CoinGecko/Indodax lewat urllib (stdlib saja).
- Offline uji (`--harga-file`): membaca harga dari file JSON lokal, tanpa jaringan sama sekali.
  Format file harga (per kunci "<coingecko_id_atau_kode>_<mata_uang>"):
  {
    "bitcoin_idr": {"harga": 1500000000, "perubahan_24jam_persen": -2.3,
                     "jam_data": "2026-09-24T10:00:00+07:00", "sumber": "coingecko"},
    "ethereum_usd": {"harga": 2650.5, "perubahan_24jam_persen": 1.2,
                      "jam_data": "2026-09-24T10:00:00+07:00", "sumber": "coingecko"}
  }
  Koin yang TIDAK ada di file ini dianggap "sumber gagal" untuk uji skenario itu.

Keluaran: satu objek JSON ke stdout, termasuk field `pesan_singkat` siap tempel/kirim, dan
kode keluar (exit code) yang berbeda supaya automation OpenClaw tahu kapan harus memanggil
agent:
  0 = sukses, TIDAK ada ambang yang terlewati
  2 = sukses, ADA ambang yang terlewati (automation sebaiknya memanggil agent/mengumumkan)
  3 = sukses sebagian: ada koin yang gagal total (tanpa cache) -- tetap cek koin lain
  1 = error input/konfigurasi (file tidak ada, JSON rusak, kolom wajib kurang)
"""

import argparse
import json
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
    return f"US$ {nilai:,.2f}"


def format_persen(nilai):
    if nilai is None:
        return "-"
    tanda = "+" if nilai >= 0 else ""
    return f"{tanda}{bulat_setengah_ke_atas(nilai, 2):.2f}%"


def kunci_koin(cfg_koin):
    dasar = cfg_koin.get("coingecko_id") or cfg_koin.get("kode", "").lower()
    return f"{dasar}_{cfg_koin['mata_uang'].lower()}"


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


# ---------------------------------------------------------------------------
# Muat file
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
        ada_ambang = any(
            k.get(f) is not None
            for f in ("ambang_naik_persen", "ambang_turun_persen",
                       "ambang_harga_di_atas", "ambang_harga_di_bawah")
        )
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

def _ambil_url_json(url, timeout, percobaan):
    kesalahan_terakhir = None
    for i in range(max(1, percobaan)):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "komunitech-pantau-pasar-kripto/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as e:
            kesalahan_terakhir = e
            if i < percobaan - 1:
                time.sleep(min(2 ** i, 4))
    raise RuntimeError(str(kesalahan_terakhir))


def ambil_harga_coingecko(coingecko_id, mata_uang, timeout, percobaan):
    url = (
        f"{COINGECKO_URL}?ids={coingecko_id}&vs_currencies={mata_uang.lower()}"
        "&include_24hr_change=true&include_last_updated_at=true"
    )
    data = _ambil_url_json(url, timeout, percobaan)
    if coingecko_id not in data or mata_uang.lower() not in data[coingecko_id]:
        raise RuntimeError(f"CoinGecko tidak mengembalikan data untuk '{coingecko_id}'/{mata_uang}.")
    d = data[coingecko_id]
    ts = d.get(f"last_updated_at")
    jam_data = (
        datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(WIB).isoformat()
        if ts else waktu_wib_sekarang().isoformat()
    )
    return {
        "harga": d[mata_uang.lower()],
        "perubahan_24jam_persen": d.get(f"{mata_uang.lower()}_24h_change"),
        "jam_data": jam_data,
        "sumber": "coingecko",
    }


def ambil_harga_indodax(pair, timeout, percobaan):
    url = INDODAX_URL_TMPL.format(pair=pair)
    data = _ambil_url_json(url, timeout, percobaan)
    if "ticker" not in data or "last" not in data["ticker"]:
        raise RuntimeError(f"Indodax tidak mengembalikan data ticker untuk pair '{pair}'.")
    t = data["ticker"]
    ts = t.get("server_time")
    jam_data = (
        datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(WIB).isoformat()
        if ts else waktu_wib_sekarang().isoformat()
    )
    return {
        "harga": float(t["last"]),
        "perubahan_24jam_persen": None,  # Indodax ticker publik tidak menyediakan ini
        "jam_data": jam_data,
        "sumber": "indodax",
    }


def ambil_harga_online(cfg_koin, timeout, percobaan):
    sumber = cfg_koin.get("sumber")
    mata_uang = cfg_koin["mata_uang"].lower()
    if sumber == "indodax" or (sumber is None and mata_uang == "idr" and cfg_koin.get("indodax_pair")):
        pair = cfg_koin.get("indodax_pair") or f"{cfg_koin['kode'].lower()}idr"
        return ambil_harga_indodax(pair, timeout, percobaan)
    coingecko_id = cfg_koin.get("coingecko_id") or cfg_koin["kode"].lower()
    return ambil_harga_coingecko(coingecko_id, mata_uang, timeout, percobaan)


# ---------------------------------------------------------------------------
# Evaluasi ambang
# ---------------------------------------------------------------------------

def evaluasi_ambang(cfg_koin, harga_sekarang, persen_perubahan):
    detail = []
    terlewati = False

    naik = cfg_koin.get("ambang_naik_persen")
    turun = cfg_koin.get("ambang_turun_persen")
    if persen_perubahan is not None:
        if naik is not None and persen_perubahan >= naik:
            terlewati = True
            detail.append(f"Naik {format_persen(persen_perubahan)} (ambang naik {naik}%).")
        if turun is not None and persen_perubahan <= -abs(turun):
            terlewati = True
            detail.append(f"Turun {format_persen(persen_perubahan)} (ambang turun {turun}%).")
    elif naik is not None or turun is not None:
        detail.append(
            "Ambang persen tidak bisa dicek: tidak ada dasar pembanding "
            "(sumber ini tidak punya data 24 jam, dan 'harga_acuan' belum diisi di konfigurasi)."
        )

    di_atas = cfg_koin.get("ambang_harga_di_atas")
    di_bawah = cfg_koin.get("ambang_harga_di_bawah")
    if di_atas is not None and harga_sekarang >= di_atas:
        terlewati = True
        detail.append(f"Harga sudah >= ambang atas {di_atas}.")
    if di_bawah is not None and harga_sekarang <= di_bawah:
        terlewati = True
        detail.append(f"Harga sudah <= ambang bawah {di_bawah}.")

    return terlewati, detail


# ---------------------------------------------------------------------------
# Proses satu koin
# ---------------------------------------------------------------------------

def proses_koin(cfg_koin, sekarang, harga_file_data, state, timeout, percobaan, usia_basi_jam):
    kk = kunci_koin(cfg_koin)
    hasil = {
        "kode": cfg_koin["kode"],
        "mata_uang": cfg_koin["mata_uang"].upper(),
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
        "detail_pemicu": [],
        "peringatan": [],
    }

    data_baru = None
    kesalahan = None
    if harga_file_data is not None:
        data_baru = harga_file_data.get(kk)
        if data_baru is None:
            kesalahan = f"Tidak ada entri '{kk}' di --harga-file (disimulasikan sebagai sumber gagal)."
    else:
        try:
            data_baru = ambil_harga_online(cfg_koin, timeout, percobaan)
        except Exception as e:  # noqa: BLE001 - semua kegagalan jaringan ditangani sama
            kesalahan = f"Gagal mengambil harga langsung: {e}"

    if data_baru is not None:
        hasil["status"] = "hidup"
        hasil["harga"] = data_baru["harga"]
        hasil["sumber"] = data_baru["sumber"]
        hasil["jam_data"] = data_baru["jam_data"]
        hasil["perubahan_24jam_persen"] = data_baru.get("perubahan_24jam_persen")
        hasil["usia_data_jam"] = round(usia_jam(data_baru["jam_data"], sekarang) or 0, 2)
        state[kk] = {
            "harga_terakhir": data_baru["harga"],
            "jam_data_terakhir": data_baru["jam_data"],
            "sumber_terakhir": data_baru["sumber"],
        }
    else:
        cache = state.get(kk)
        if cache:
            hasil["status"] = "cache"
            hasil["harga"] = cache["harga_terakhir"]
            hasil["sumber"] = f"{cache['sumber_terakhir']} (cache)"
            hasil["jam_data"] = cache["jam_data_terakhir"]
            usia = usia_jam(cache["jam_data_terakhir"], sekarang)
            hasil["usia_data_jam"] = round(usia, 2) if usia is not None else None
            hasil["peringatan"].append(
                f"DATA BASI: {kesalahan} Menampilkan harga cache dari {cache['jam_data_terakhir']} "
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
        hasil["harga_format"] = (
            format_rupiah(hasil["harga"]) if hasil["mata_uang"] == "IDR" else format_usd(hasil["harga"])
        )
        acuan = cfg_koin.get("harga_acuan")
        if acuan:
            hasil["persen_vs_acuan"] = hitung_persen_perubahan(hasil["harga"], acuan)
            persen_pakai = hasil["persen_vs_acuan"]
        else:
            persen_pakai = hasil["perubahan_24jam_persen"]
        terlewati, detail = evaluasi_ambang(cfg_koin, hasil["harga"], persen_pakai)
        hasil["ambang_terlewati"] = terlewati
        hasil["detail_pemicu"] = detail

    return hasil


# ---------------------------------------------------------------------------
# Pesan singkat
# ---------------------------------------------------------------------------

def susun_pesan_singkat(daftar_hasil, sekarang):
    baris = [f"Pantau harga kripto -- {sekarang.strftime('%d %b %Y %H:%M')} WIB"]
    ada_pemicu = False
    for h in daftar_hasil:
        if h["status"] == "gagal_total":
            baris.append(f"- {h['kode']}: gagal ambil data, tidak ada cache. {h['peringatan'][0]}")
            continue
        tanda = " ⚠️" if h["status"] == "cache" else ""
        perubahan = h["perubahan_24jam_persen"]
        teks_perubahan = f" ({format_persen(perubahan)} / 24 jam)" if perubahan is not None else ""
        baris.append(f"- {h['kode']}: {h['harga_format']}{teks_perubahan}{tanda}")
        if h["ambang_terlewati"]:
            ada_pemicu = True
            for d in h["detail_pemicu"]:
                baris.append(f"  >> AMBANG TERLEWATI: {d}")
    if not ada_pemicu:
        baris.append("Tidak ada ambang yang terlewati saat ini.")
    baris.append("Sumber & jam data ada di rincian JSON. Informasi, bukan nasihat investasi.")
    return "\n".join(baris)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description="Cek harga kripto vs ambang member (tanpa API key).")
    ap.add_argument("--konfigurasi", required=True, help="Path ke konfigurasi.json (daftar koin & ambang).")
    ap.add_argument("--state", required=True, help="Path ke state.json (cache harga terakhir, dibuat otomatis).")
    ap.add_argument("--harga-file", default=None,
                     help="Mode offline/uji: path JSON berisi harga simulasi, tanpa jaringan sama sekali.")
    ap.add_argument("--timeout", type=float, default=8.0, help="Timeout per permintaan (detik). Default 8.")
    ap.add_argument("--percobaan", type=int, default=2, help="Jumlah percobaan per sumber. Default 2.")
    ap.add_argument("--usia-basi-jam", type=float, default=6.0,
                     help="Cache lebih tua dari ini (jam) diberi peringatan tambahan. Default 6.")
    ap.add_argument("--keluaran", choices=["json", "teks"], default="json",
                     help="json = satu objek JSON (default, untuk automation/agent). "
                          "teks = hanya pesan_singkat ke stdout.")
    args = ap.parse_args(argv)

    try:
        cfg = muat_json(args.konfigurasi, wajib=True, nama="Konfigurasi")
        daftar_koin = validasi_konfigurasi(cfg)
        state = muat_json(args.state, wajib=False, nama="State")
        if not isinstance(state, dict):
            raise KesalahanInput("State rusak: isinya harus objek JSON (dict), bukan daftar/nilai lain.")
        harga_file_data = None
        if args.harga_file:
            harga_file_data = muat_json(args.harga_file, wajib=True, nama="File harga (--harga-file)")
            if not isinstance(harga_file_data, dict):
                raise KesalahanInput("--harga-file rusak: isinya harus objek JSON (dict).")
    except KesalahanInput as e:
        print(json.dumps({"status": "error", "pesan": str(e)}, ensure_ascii=False, indent=2))
        return 1

    sekarang = waktu_wib_sekarang()
    daftar_hasil = []
    for k in daftar_koin:
        daftar_hasil.append(
            proses_koin(k, sekarang, harga_file_data, state, args.timeout, args.percobaan, args.usia_basi_jam)
        )

    try:
        with open(args.state, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except OSError as e:
        for h in daftar_hasil:
            h["peringatan"].append(f"Gagal menyimpan cache state: {e}")

    pesan_singkat = susun_pesan_singkat(daftar_hasil, sekarang)

    ada_terlewati = any(h["ambang_terlewati"] for h in daftar_hasil)
    ada_gagal_total = any(h["status"] == "gagal_total" for h in daftar_hasil)

    keluaran = {
        "status": "ok",
        "jam_cek": sekarang.isoformat(),
        "ambang_terlewati": ada_terlewati,
        "ada_koin_gagal_total": ada_gagal_total,
        "koin": daftar_hasil,
        "pesan_singkat": pesan_singkat,
        "disclaimer": "Informasi, bukan nasihat investasi. Keputusan & risiko sepenuhnya milik Anda.",
    }

    if args.keluaran == "teks":
        print(pesan_singkat)
    else:
        print(json.dumps(keluaran, ensure_ascii=False, indent=2))

    if ada_terlewati:
        return 2
    if ada_gagal_total:
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
