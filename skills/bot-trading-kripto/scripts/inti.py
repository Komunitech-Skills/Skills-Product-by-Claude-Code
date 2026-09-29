#!/usr/bin/env python3
"""Inti bot-trading-kripto: konfigurasi, aturan strategi MILIK MEMBER, batas risiko,
akuntansi (Decimal), pajak/fee, log audit, dan tombol berhenti.

Modul ini TIDAK menyentuh jaringan. Semua keputusan beli/jual berasal dari aturan yang
ditulis member di konfigurasi (DCA terjadwal, grid, take-profit/stop-loss, rebalancing).
Tidak ada indikator, prediksi, atau sinyal dari Komunitech.

Hanya Python standar. Semua angka uang memakai Decimal (bukan float).
"""

import hashlib
import json
import os
import re
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation, ROUND_DOWN, ROUND_HALF_UP

D = Decimal
WIB = timezone(timedelta(hours=7))
NOL = D("0")

MODE = ("paper", "testnet", "live")
BURSA = ("binance", "indodax")
JENIS_STRATEGI = ("dca", "grid", "tp_sl", "rebalancing")

# Tarif PPh Pasal 22 final atas penjualan aset kripto -- PMK 50/2025, berlaku 1 Agustus 2025.
# Sumber: https://www.pajak.go.id/index.php/en/node/118105 (dibaca 2026-09-29).
TARIF_PPH = {"domestik": D("0.0021"), "luar_negeri": D("0.01"), "tidak_dihitung": NOL}
SUMBER_PAJAK = ("PMK 50/2025 (berlaku 1 Agustus 2025): PPh 22 final 0,21% (PAKD dalam negeri) "
                "/ 1% (platform luar negeri) dari nilai jual, dipungut dari penjual. "
                "Dicek 2026-09-29 di pajak.go.id. Pembulatan belum dicocokkan dengan Coretax.")

# Fee bawaan bila member tidak mengisi (asumsi, WAJIB disebut ke member):
# Indodax btc_idr taker 0,2% (dari https://indodax.com/api/pairs, dibaca 2026-09-29);
# Binance spot standar 0,1%.
FEE_BAWAAN = {"indodax": D("0.2"), "binance": D("0.1")}
PAJAK_BAWAAN = {"indodax": "domestik", "binance": "luar_negeri"}

DISCLAIMER = ("Bot ini hanya menjalankan aturan yang ANDA tetapkan. Bukan nasihat investasi, "
              "bukan sinyal, tanpa jaminan untung. Aset kripto berisiko tinggi; Anda bisa "
              "kehilangan seluruh modal. Keputusan & risiko sepenuhnya milik Anda.")


class KonfigurasiTidakValid(Exception):
    """Pesan selalu Bahasa Indonesia, siap ditunjukkan ke member."""


# ---------------------------------------------------------------------------- angka

def angka(nilai, nama, positif=True, boleh_nol=False):
    """Ubah ke Decimal. Terima str/int (float ditolak supaya tidak ada galat biner diam-diam
    -- tulis angka sebagai teks di JSON, mis. "100000")."""
    if isinstance(nilai, bool) or nilai is None:
        raise KonfigurasiTidakValid(f"'{nama}' wajib diisi angka.")
    if isinstance(nilai, float):
        raise KonfigurasiTidakValid(
            f"'{nama}' tulis sebagai teks, mis. \"{nilai}\" (pakai tanda kutip) supaya presisi terjaga.")
    s = str(nilai).strip().replace("_", "")
    try:
        x = D(s)
    except InvalidOperation:
        raise KonfigurasiTidakValid(f"'{nama}' = {nilai!r} bukan angka (pakai titik untuk desimal, tanpa pemisah ribuan).")
    if not x.is_finite():
        raise KonfigurasiTidakValid(f"'{nama}' harus angka biasa.")
    if positif and (x < 0 or (x == 0 and not boleh_nol)):
        raise KonfigurasiTidakValid(f"'{nama}' harus lebih dari 0 (sekarang {nilai}).")
    return x


def bulat_bawah(x, langkah):
    """Bulatkan ke bawah ke kelipatan `langkah` (mis. lot size bursa)."""
    if langkah <= 0:
        return x
    return (x / langkah).to_integral_value(rounding=ROUND_DOWN) * langkah


def bulat_uang(x, kutipan):
    """Rupiah -> rupiah terdekat. Mata uang lain (USDT) -> 8 desimal."""
    q = D("1") if kutipan == "IDR" else D("0.00000001")
    return x.quantize(q, rounding=ROUND_HALF_UP)


def bulat_pajak(x, kutipan):
    """PPh dibulatkan ke BAWAH (tidak pernah memungut melebihi tarif)."""
    q = D("1") if kutipan == "IDR" else D("0.00000001")
    return x.quantize(q, rounding=ROUND_DOWN)


def teks(x):
    """Decimal -> teks tanpa notasi ilmiah."""
    if x == x.to_integral_value():
        return str(x.quantize(D("1")))
    return format(x.normalize(), "f")


def rp(x, kutipan="IDR"):
    if kutipan == "IDR":
        n = int(bulat_uang(x, "IDR"))
        tanda = "-" if n < 0 else ""
        return f"{tanda}Rp{abs(n):,}".replace(",", ".")
    return f"{teks(bulat_uang(x, kutipan))} {kutipan}"


# ---------------------------------------------------------------------------- konfigurasi

def _wajib(d, kunci, konteks):
    if kunci not in d or d[kunci] in (None, ""):
        raise KonfigurasiTidakValid(f"{konteks}: '{kunci}' wajib diisi.")
    return d[kunci]


def normalisasi_konfigurasi(cfg):
    """Validasi & lengkapi konfigurasi. Kembalikan dict baru (angka tetap teks di JSON,
    tetapi field `_d` berisi Decimal siap pakai)."""
    if not isinstance(cfg, dict):
        raise KonfigurasiTidakValid("Konfigurasi harus objek JSON.")
    mode = cfg.get("mode", "paper")
    if mode not in MODE:
        raise KonfigurasiTidakValid(f"'mode' harus salah satu {MODE} (sekarang {mode!r}).")
    bursa = _wajib(cfg, "bursa", "konfigurasi")
    if bursa not in BURSA:
        raise KonfigurasiTidakValid(f"'bursa' harus salah satu {BURSA} (sekarang {bursa!r}).")
    pasangan = str(_wajib(cfg, "pasangan", "konfigurasi"))
    if bursa == "indodax":
        m = re.fullmatch(r"([a-z0-9]{2,15})_idr", pasangan)
        if not m:
            raise KonfigurasiTidakValid("Indodax: 'pasangan' ditulis huruf kecil berakhiran _idr, mis. \"btc_idr\".")
        koin, kutipan = m.group(1).upper(), "IDR"
    else:
        koin = str(_wajib(cfg, "koin", "Binance")).upper()
        kutipan = str(_wajib(cfg, "kutipan", "Binance")).upper()
        if pasangan != koin + kutipan or not re.fullmatch(r"[A-Z0-9]{5,20}", pasangan):
            raise KonfigurasiTidakValid(f"Binance: 'pasangan' harus = koin+kutipan, mis. \"BTCUSDT\" (sekarang {pasangan!r}).")
    if mode == "live" and bursa == "binance" and cfg.get("saya_paham_binance_bukan_pakd_ojk") is not True:
        raise KonfigurasiTidakValid(
            "Mode live di Binance global ditolak: Binance global tidak tercantum di daftar PAKD berizin OJK "
            "(cek ojk.go.id) dan PPh-nya 1%. Pakai Indodax (PAKD berizin) untuk live, atau tambahkan "
            "\"saya_paham_binance_bukan_pakd_ojk\": true bila Anda tetap memilihnya dengan sadar.")

    st = cfg.get("strategi")
    if not isinstance(st, dict):
        raise KonfigurasiTidakValid("'strategi' wajib diisi (objek dengan 'jenis').")
    jenis = st.get("jenis")
    if jenis not in JENIS_STRATEGI:
        raise KonfigurasiTidakValid(f"strategi.jenis harus salah satu {JENIS_STRATEGI} (sekarang {jenis!r}).")

    br = cfg.get("batas_risiko")
    if not isinstance(br, dict):
        raise KonfigurasiTidakValid(
            "'batas_risiko' WAJIB diisi: modal_maks_per_order, modal_maks_total, stop_loss_persen, "
            "rugi_harian_maks, order_terbuka_maks. Bot tidak mau jalan tanpa batas risiko.")
    ds = {}
    for k in ("modal_maks_per_order", "modal_maks_total", "stop_loss_persen", "rugi_harian_maks"):
        ds[k] = angka(_wajib(br, k, "batas_risiko"), f"batas_risiko.{k}")
    if not (D("0") < ds["stop_loss_persen"] < D("100")):
        raise KonfigurasiTidakValid("batas_risiko.stop_loss_persen harus di antara 0 dan 100.")
    if ds["modal_maks_per_order"] > ds["modal_maks_total"]:
        raise KonfigurasiTidakValid("batas_risiko.modal_maks_per_order tidak boleh lebih besar dari modal_maks_total.")
    oto = br.get("order_terbuka_maks")
    if not isinstance(oto, int) or isinstance(oto, bool) or not 1 <= oto <= 50:
        raise KonfigurasiTidakValid("batas_risiko.order_terbuka_maks wajib bilangan bulat 1-50.")
    ds["order_terbuka_maks"] = oto

    if jenis == "dca":
        ds["nominal"] = angka(_wajib(st, "nominal_per_beli", "strategi dca"), "strategi.nominal_per_beli")
        ij = angka(_wajib(st, "interval_jam", "strategi dca"), "strategi.interval_jam")
        if ij < 1:
            raise KonfigurasiTidakValid("strategi.interval_jam minimal 1.")
        ds["interval_jam"] = ij
        if st.get("take_profit_persen") not in (None, ""):
            ds["tp"] = angka(st["take_profit_persen"], "strategi.take_profit_persen")
        if ds["nominal"] > ds["modal_maks_per_order"]:
            raise KonfigurasiTidakValid("nominal_per_beli melebihi batas_risiko.modal_maks_per_order.")
    elif jenis == "grid":
        ds["bawah"] = angka(_wajib(st, "harga_bawah", "strategi grid"), "strategi.harga_bawah")
        ds["atas"] = angka(_wajib(st, "harga_atas", "strategi grid"), "strategi.harga_atas")
        n = st.get("jumlah_grid")
        if not isinstance(n, int) or isinstance(n, bool) or not 2 <= n <= 100:
            raise KonfigurasiTidakValid("strategi.jumlah_grid wajib bilangan bulat 2-100.")
        ds["jumlah_grid"] = n
        ds["nominal"] = angka(_wajib(st, "nominal_per_grid", "strategi grid"), "strategi.nominal_per_grid")
        if ds["bawah"] >= ds["atas"]:
            raise KonfigurasiTidakValid("strategi.harga_bawah harus lebih kecil dari harga_atas.")
        if ds["nominal"] > ds["modal_maks_per_order"]:
            raise KonfigurasiTidakValid("nominal_per_grid melebihi batas_risiko.modal_maks_per_order.")
        if ds["nominal"] * n > ds["modal_maks_total"]:
            raise KonfigurasiTidakValid(
                f"jumlah_grid x nominal_per_grid ({n} x {teks(ds['nominal'])}) melebihi modal_maks_total. "
                "Kurangi jumlah grid/nominal atau naikkan modal total secara sadar.")
    elif jenis == "tp_sl":
        ds["nominal"] = angka(_wajib(st, "nominal_beli", "strategi tp_sl"), "strategi.nominal_beli")
        ds["tp"] = angka(_wajib(st, "take_profit_persen", "strategi tp_sl"), "strategi.take_profit_persen")
        ds["sl"] = angka(_wajib(st, "stop_loss_persen", "strategi tp_sl"), "strategi.stop_loss_persen")
        if not ds["sl"] < 100:
            raise KonfigurasiTidakValid("strategi.stop_loss_persen harus < 100.")
        if st.get("harga_masuk_maks") not in (None, ""):
            ds["harga_masuk_maks"] = angka(st["harga_masuk_maks"], "strategi.harga_masuk_maks")
        if ds["nominal"] > ds["modal_maks_per_order"]:
            raise KonfigurasiTidakValid("nominal_beli melebihi batas_risiko.modal_maks_per_order.")
    else:  # rebalancing
        ds["target"] = angka(_wajib(st, "target_persen_koin", "strategi rebalancing"), "strategi.target_persen_koin")
        ds["ambang"] = angka(_wajib(st, "ambang_deviasi_persen", "strategi rebalancing"), "strategi.ambang_deviasi_persen")
        if not D("0") < ds["target"] < D("100"):
            raise KonfigurasiTidakValid("strategi.target_persen_koin harus di antara 0 dan 100.")

    biaya = cfg.get("biaya") or {}
    ds["fee_persen"] = angka(biaya.get("fee_persen", str(FEE_BAWAAN[bursa])), "biaya.fee_persen", boleh_nol=True)
    if ds["fee_persen"] >= 5:
        raise KonfigurasiTidakValid("biaya.fee_persen tidak wajar (>= 5%). Periksa lagi.")
    pajak = biaya.get("pajak", PAJAK_BAWAAN[bursa])
    if pajak not in TARIF_PPH:
        raise KonfigurasiTidakValid(f"biaya.pajak harus salah satu {tuple(TARIF_PPH)}.")
    if mode == "live" and pajak == "tidak_dihitung":
        raise KonfigurasiTidakValid("Mode live: biaya.pajak tidak boleh 'tidak_dihitung'.")
    ds["tarif_pph"] = TARIF_PPH[pajak]
    ds["langkah_jumlah"] = angka(cfg.get("langkah_jumlah", "0.00000001"), "langkah_jumlah")
    ds["min_nilai_order"] = angka(cfg.get("min_nilai_order", "10000" if kutipan == "IDR" else "5"),
                                  "min_nilai_order", boleh_nol=True)

    if mode in ("testnet", "live"):
        kunci = cfg.get("kunci")
        if not isinstance(kunci, dict) or not (kunci.get("file") or kunci.get("env") is True):
            raise KonfigurasiTidakValid(
                f"Mode {mode} butuh 'kunci': {{\"file\": \"<path file kunci milik Anda>\"}} atau {{\"env\": true}}. "
                "Kunci dibuat & disimpan SENDIRI oleh Anda (lihat references/keamanan-kunci-api.md).")

    out = dict(cfg)
    out.update({"mode": mode, "koin": koin, "kutipan": kutipan})
    out["_d"] = ds
    out["_jenis"] = jenis
    return out


def muat_konfigurasi(path):
    try:
        with open(path, encoding="utf-8-sig") as f:
            cfg = json.load(f)
    except FileNotFoundError:
        raise KonfigurasiTidakValid(f"File konfigurasi '{path}' tidak ditemukan.")
    except json.JSONDecodeError as e:
        raise KonfigurasiTidakValid(f"File konfigurasi bukan JSON valid (baris {e.lineno}): {e.msg}")
    return normalisasi_konfigurasi(cfg)


def _kanonik(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=True, separators=(",", ":"))


def sidik_jari_strategi(cfg):
    """Sidik jari aturan (tanpa mode & kunci) -- dipakai membuktikan aturan yang SAMA
    sudah pernah disimulasikan sebelum live."""
    inti = {k: cfg.get(k) for k in ("bursa", "pasangan", "strategi", "batas_risiko", "biaya")}
    return hashlib.sha256(_kanonik(inti).encode()).hexdigest()[:16]


def sidik_jari_penuh(cfg):
    bersih = {k: v for k, v in cfg.items() if not k.startswith("_")}
    return hashlib.sha256(_kanonik(bersih).encode()).hexdigest()[:12]


# ---------------------------------------------------------------------------- state

def state_awal(cfg):
    ds = cfg["_d"]
    return {
        "versi": 1,
        "sidik_jari_strategi": sidik_jari_strategi(cfg),
        "kas": teks(ds["modal_maks_total"]),   # kas "virtual" bot = anggaran member
        "posisi_koin": "0",
        "biaya_perolehan": "0",                # total kutipan yang dibayar utk posisi terbuka (incl fee)
        "realized_pl": "0",
        "total_fee": "0",
        "total_pajak": "0",
        "jumlah_transaksi": 0,
        "terakhir_beli_dca": None,
        "grid_slot": {},
        "tp_sl_status": "menunggu_masuk",
        "hari": None,
        "ekuitas_awal_hari": None,
        "berhenti": False,
        "alasan_berhenti": None,
        "notif_berhenti_terkirim": False,
        "jumlah_tick": 0,
        "tick_paper_per_sidik": {},
    }


def muat_state(path, cfg):
    if not os.path.exists(path):
        return state_awal(cfg)
    try:
        with open(path, encoding="utf-8") as f:
            st = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        raise KonfigurasiTidakValid(f"File state '{path}' rusak ({e}). Jangan dihapus diam-diam: "
                                    "periksa audit.jsonl, lalu pindahkan file itu bila ingin mulai ulang.")
    dasar = state_awal(cfg)
    dasar.update(st)
    return dasar


def simpan_json_atomik(path, data):
    folder = os.path.dirname(os.path.abspath(path))
    os.makedirs(folder, exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


# ---------------------------------------------------------------------------- log audit

class Penyamar:
    """Menyamarkan kunci/secret dari teks apa pun sebelum ditulis ke log/keluaran."""

    def __init__(self, rahasia=()):
        self.rahasia = [r for r in rahasia if r and len(r) >= 6]

    def __call__(self, s):
        s = str(s)
        for r in self.rahasia:
            s = s.replace(r, "***DISAMARKAN***")
        # Jaga-jaga: tanda tangan & parameter sensitif di URL
        s = re.sub(r"(signature=)[0-9a-fA-F]{16,}", r"\1***", s)
        s = re.sub(r"(?i)(X-MBX-APIKEY|\bKey|\bSign)(['\"]?\s*[:=]\s*['\"]?)[A-Za-z0-9\-]{8,}", r"\1\2***", s)
        return s


def tulis_audit(path, peristiwa, data, penyamar=None, sekarang=None):
    """Tambah satu baris JSON ke log audit lokal (append-only)."""
    sekarang = sekarang or datetime.now(WIB)
    baris = {"waktu": sekarang.isoformat(timespec="seconds"), "peristiwa": peristiwa, "data": data}
    s = json.dumps(baris, ensure_ascii=False, default=str)
    if penyamar:
        s = penyamar(s)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(s + "\n")


# ---------------------------------------------------------------------------- akuntansi

def ekuitas(state, harga):
    return D(state["kas"]) + D(state["posisi_koin"]) * harga


def harga_rata(state):
    pos = D(state["posisi_koin"])
    return D(state["biaya_perolehan"]) / pos if pos > 0 else None


def simulasi_isi(cfg, sisi, harga, nilai_kutipan=None, jumlah_koin=None):
    """Model isi order untuk paper/backtest (dan estimasi untuk live).
    Beli: total bayar (harga*jumlah + fee) <= nilai_kutipan. Jual: jumlah_koin dijual.
    Kembalikan dict angka Decimal, atau None bila jumlah jadi 0 setelah pembulatan lot."""
    ds, kut = cfg["_d"], cfg["kutipan"]
    f = ds["fee_persen"] / D("100")
    if sisi == "beli":
        jumlah = bulat_bawah((nilai_kutipan / (D("1") + f)) / harga, ds["langkah_jumlah"])
        if jumlah <= 0:
            return None
        bruto = jumlah * harga
        fee = bulat_uang(bruto * f, kut)
        total = bulat_uang(bruto, kut) + fee
        if total > nilai_kutipan:  # jaga-jaga efek pembulatan rupiah
            jumlah = bulat_bawah(jumlah - ds["langkah_jumlah"], ds["langkah_jumlah"])
            if jumlah <= 0:
                return None
            bruto = jumlah * harga
            fee = bulat_uang(bruto * f, kut)
            total = bulat_uang(bruto, kut) + fee
        return {"sisi": "beli", "harga": harga, "jumlah": jumlah, "bruto": bulat_uang(bruto, kut),
                "fee": fee, "pajak": NOL, "bersih": total}
    jumlah = bulat_bawah(jumlah_koin, ds["langkah_jumlah"])
    if jumlah <= 0:
        return None
    bruto = bulat_uang(jumlah * harga, kut)
    fee = bulat_uang(bruto * f, kut)
    pajak = bulat_pajak(bruto * ds["tarif_pph"], kut)
    return {"sisi": "jual", "harga": harga, "jumlah": jumlah, "bruto": bruto,
            "fee": fee, "pajak": pajak, "bersih": bruto - fee - pajak}


def terapkan_isi(state, isi, kutipan):
    """Perbarui state bot dari satu isi order. Metode rata-rata tertimbang."""
    kas, pos, bp = D(state["kas"]), D(state["posisi_koin"]), D(state["biaya_perolehan"])
    if isi["sisi"] == "beli":
        kas -= isi["bersih"]
        pos += isi["jumlah"]
        bp += isi["bersih"]
        pl = NOL
    else:
        porsi = bp * isi["jumlah"] / pos if pos > 0 else NOL
        porsi = bulat_uang(porsi, kutipan)
        pl = isi["bersih"] - porsi
        kas += isi["bersih"]
        pos -= isi["jumlah"]
        bp = NOL if pos <= 0 else bp - porsi
        state["realized_pl"] = teks(D(state["realized_pl"]) + pl)
    state["kas"], state["posisi_koin"], state["biaya_perolehan"] = teks(kas), teks(pos), teks(bp)
    state["total_fee"] = teks(D(state["total_fee"]) + isi["fee"])
    state["total_pajak"] = teks(D(state["total_pajak"]) + isi["pajak"])
    state["jumlah_transaksi"] = int(state.get("jumlah_transaksi", 0)) + 1
    return pl


# ---------------------------------------------------------------------------- strategi

def level_grid(ds):
    langkah = (ds["atas"] - ds["bawah"]) / D(ds["jumlah_grid"])
    return [ds["bawah"] + langkah * i for i in range(ds["jumlah_grid"] + 1)]


def rencanakan(cfg, state, harga, sekarang):
    """Terjemahkan ATURAN MEMBER -> daftar niat order. Tidak ada penilaian pasar."""
    ds, jenis = cfg["_d"], cfg["_jenis"]
    niat = []
    pos = D(state["posisi_koin"])
    rata = harga_rata(state)
    if jenis == "dca":
        if "tp" in ds and pos > 0 and rata and harga >= rata * (1 + ds["tp"] / 100):
            niat.append({"sisi": "jual", "jumlah_koin": pos,
                         "alasan": f"take-profit DCA {teks(ds['tp'])}% dari harga rata-rata tercapai"})
        tb = state.get("terakhir_beli_dca")
        jatuh_tempo = tb is None or sekarang >= datetime.fromisoformat(tb) + timedelta(hours=float(ds["interval_jam"]))
        if jatuh_tempo:
            niat.append({"sisi": "beli", "nilai_kutipan": ds["nominal"],
                         "alasan": f"DCA terjadwal tiap {teks(ds['interval_jam'])} jam", "dca": True})
    elif jenis == "grid":
        lv = level_grid(ds)
        slot = state.setdefault("grid_slot", {})
        for i in range(ds["jumlah_grid"]):
            kunci = str(i)
            if kunci in slot and harga >= lv[i + 1]:
                niat.append({"sisi": "jual", "jumlah_koin": D(slot[kunci]), "slot": kunci,
                             "alasan": f"grid: harga >= level {i + 1} ({teks(lv[i + 1])})"})
        for i in range(ds["jumlah_grid"]):
            kunci = str(i)
            # beli di slot i hanya bila harga di pita [lv_i, lv_i+1) -- satu slot per tick
            if kunci not in slot and lv[i] <= harga < lv[i + 1]:
                niat.append({"sisi": "beli", "nilai_kutipan": ds["nominal"], "slot": kunci,
                             "alasan": f"grid: harga di pita level {i} ({teks(lv[i])}-{teks(lv[i + 1])})"})
    elif jenis == "tp_sl":
        status = state.get("tp_sl_status", "menunggu_masuk")
        if status == "menunggu_masuk" and pos == 0:
            if "harga_masuk_maks" not in ds or harga <= ds["harga_masuk_maks"]:
                niat.append({"sisi": "beli", "nilai_kutipan": ds["nominal"], "alasan": "tp_sl: masuk sesuai aturan", "tp_sl_masuk": True})
        elif pos > 0 and rata:
            if harga >= rata * (1 + ds["tp"] / 100):
                niat.append({"sisi": "jual", "jumlah_koin": pos, "alasan": f"take-profit {teks(ds['tp'])}% tercapai", "tp_sl_selesai": True})
            elif harga <= rata * (1 - ds["sl"] / 100):
                niat.append({"sisi": "jual", "jumlah_koin": pos, "alasan": f"stop-loss strategi {teks(ds['sl'])}% tersentuh", "tp_sl_selesai": True})
    else:  # rebalancing
        e = ekuitas(state, harga)
        if e > 0:
            nilai_koin = pos * harga
            persen = nilai_koin / e * 100
            if abs(persen - ds["target"]) >= ds["ambang"]:
                selisih = e * ds["target"] / 100 - nilai_koin
                nilai = min(abs(selisih), ds["modal_maks_per_order"])
                if selisih > 0:
                    niat.append({"sisi": "beli", "nilai_kutipan": min(nilai, D(state["kas"])),
                                 "alasan": f"rebalancing: porsi koin {teks(persen.quantize(D('0.01')))}% < target {teks(ds['target'])}%"})
                else:
                    niat.append({"sisi": "jual", "jumlah_koin": nilai / harga,
                                 "alasan": f"rebalancing: porsi koin {teks(persen.quantize(D('0.01')))}% > target {teks(ds['target'])}%"})
    return niat


# ---------------------------------------------------------------------------- risiko

def cek_tombol_berhenti(folder_bot):
    return os.path.exists(os.path.join(folder_bot, "STOP"))


def cek_risiko_awal(cfg, state, harga, sekarang):
    """Dipanggil SEBELUM strategi. Kembalikan (alasan_berhenti|None, niat_paksa|None).
    - stop-loss global: harga <= rata-rata x (1 - SL%) -> jual semua lalu berhenti
    - rugi harian: ekuitas turun > rugi_harian_maks sejak awal hari (WIB) -> berhenti"""
    ds = cfg["_d"]
    hari = sekarang.astimezone(WIB).date().isoformat()
    if state.get("hari") != hari or state.get("ekuitas_awal_hari") is None:
        state["hari"] = hari
        state["ekuitas_awal_hari"] = teks(ekuitas(state, harga))
    pos = D(state["posisi_koin"])
    rata = harga_rata(state)
    if pos > 0 and rata and harga <= rata * (1 - ds["stop_loss_persen"] / 100):
        return (f"STOP-LOSS: harga {teks(harga)} <= {teks(ds['stop_loss_persen'])}% di bawah harga rata-rata "
                f"{teks(bulat_uang(rata, cfg['kutipan']))}. Posisi dijual & bot berhenti.",
                {"sisi": "jual", "jumlah_koin": pos, "alasan": "stop-loss global"})
    rugi = D(state["ekuitas_awal_hari"]) - ekuitas(state, harga)
    if rugi > ds["rugi_harian_maks"]:
        return (f"BATAS RUGI HARIAN: turun {rp(rugi, cfg['kutipan'])} hari ini (batas "
                f"{rp(ds['rugi_harian_maks'], cfg['kutipan'])}). Bot berhenti, tidak ada order baru.", None)
    return None, None


def cek_niat(cfg, state, niat, harga, jumlah_order_terbuka):
    """Periksa satu niat terhadap batas risiko. Kembalikan (status, pesan):
    'ok' | 'lewati' (terlalu kecil / kas kurang, tidak berbahaya) | 'berhenti' (batas dilanggar)."""
    ds, kut = cfg["_d"], cfg["kutipan"]
    if jumlah_order_terbuka >= ds["order_terbuka_maks"]:
        return "berhenti", (f"BATAS ORDER TERBUKA: ada {jumlah_order_terbuka} order terbuka di bursa "
                            f"(batas {ds['order_terbuka_maks']}). Bot berhenti; cek manual di aplikasi bursa.")
    if niat["sisi"] == "beli":
        nilai = niat["nilai_kutipan"]
        if nilai > ds["modal_maks_per_order"]:
            return "berhenti", f"BATAS MODAL PER ORDER: {rp(nilai, kut)} > {rp(ds['modal_maks_per_order'], kut)}. Bot berhenti."
        if D(state["biaya_perolehan"]) + nilai > ds["modal_maks_total"]:
            return "berhenti", (f"BATAS MODAL TOTAL: modal terpakai {rp(D(state['biaya_perolehan']), kut)} + order "
                                f"{rp(nilai, kut)} > {rp(ds['modal_maks_total'], kut)}. Bot berhenti membeli.")
        if nilai > D(state["kas"]):
            return "lewati", f"kas bot tersisa {rp(D(state['kas']), kut)} < order {rp(nilai, kut)}"
        if nilai < ds["min_nilai_order"]:
            return "lewati", f"nilai order {rp(nilai, kut)} di bawah minimum {rp(ds['min_nilai_order'], kut)}"
    else:
        if niat["jumlah_koin"] > D(state["posisi_koin"]):
            niat["jumlah_koin"] = D(state["posisi_koin"])
        if niat["jumlah_koin"] <= 0:
            return "lewati", "tidak ada koin milik bot untuk dijual"
        if niat["jumlah_koin"] * harga < ds["min_nilai_order"]:
            return "lewati", f"nilai jual di bawah minimum {rp(ds['min_nilai_order'], kut)}"
    return "ok", ""


def hentikan(state, alasan):
    if not state.get("berhenti"):
        state["berhenti"] = True
        state["alasan_berhenti"] = alasan
        state["notif_berhenti_terkirim"] = False


def catat_niat_berhasil(state, niat, isi, sekarang):
    if niat.get("dca"):
        state["terakhir_beli_dca"] = sekarang.isoformat()
    if "slot" in niat:
        if isi["sisi"] == "beli":
            state["grid_slot"][niat["slot"]] = teks(isi["jumlah"])
        else:
            state["grid_slot"].pop(niat["slot"], None)
    if niat.get("tp_sl_masuk"):
        state["tp_sl_status"] = "dalam_posisi"
    if niat.get("tp_sl_selesai"):
        state["tp_sl_status"] = "selesai"
