#!/usr/bin/env python3
"""Rekap pesanan WhatsApp/DM: hitung per pesanan + rekap harian + serah-terima kurir + CSV.

Python standar saja (tanpa paket tambahan), lintas OS.
Jalankan: python3 scripts/rekap_pesanan.py PESANAN [--katalog katalog.csv] [--tanggal 2026-10-06]
          [--mulai 1] [--format teks|json]
Windows: ganti `python3` dengan `python` atau `py`.

PESANAN = file .json atau file teks sederhana (lihat references/format-input.md).
KATALOG = CSV dengan kolom minimal `nama,harga`; opsional `kode`, `alias` (dipisah |), `stok`.

Aturan hitung (rupiah bulat):
  total baris = qty x harga
  subtotal    = jumlah total baris
  diskon      = persen x subtotal (dibulatkan ke rupiah terdekat, .5 ke atas) atau nominal;
                tidak boleh melebihi subtotal
  setelah diskon = subtotal - diskon
  total       = setelah diskon + ongkir
Harga/ongkir yang tidak diketahui TIDAK dikarang: total ditandai belum lengkap.
Script ini hanya membaca file yang diberikan; tidak ada akses jaringan dan tidak menulis file.
"""
import argparse
import csv
import io
import json
import re
import sys
from datetime import date
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from pathlib import Path

KURIR_BAKU = [
    (r"\bj\s*&\s*t\b|\bjnt\b|\bj&t\b|\bj ?and ?t\b", "J&T"),
    (r"\bjne\b", "JNE"),
    (r"\bsi ?cepat\b", "SiCepat"),
    (r"\banter ?aja\b", "AnterAja"),
    (r"\bpos\b|\bpos indonesia\b", "Pos Indonesia"),
    (r"\bgo ?send\b|\bgojek\b", "GoSend"),
    (r"\bgrab ?express\b|\bgrab\b", "GrabExpress"),
    (r"\bambil sendiri\b|\bpickup\b|\bdiambil\b", "Ambil sendiri"),
]

KUNCI = {
    "kode": "kode", "pelanggan": "pelanggan", "nama": "pelanggan", "panggilan": "pelanggan",
    "item": "item", "items": "item", "barang": "item", "pesanan": "item", "order": "item",
    "diskon": "diskon", "potongan": "diskon", "ongkir": "ongkir", "ongkos kirim": "ongkir",
    "kurir": "kurir", "ekspedisi": "kurir", "layanan": "layanan", "bayar": "bayar",
    "metode": "bayar", "pembayaran": "bayar", "status": "status", "dibayar": "dibayar",
    "sudah bayar": "dibayar", "penerima": "penerima", "hp": "hp", "wa": "hp", "no hp": "hp",
    "telp": "hp", "telepon": "hp", "alamat": "alamat", "catatan": "catatan", "note": "catatan",
}


class InputRusak(Exception):
    pass


def rupiah(n):
    if n is None:
        return None
    tanda = "-" if n < 0 else ""
    return f"{tanda}Rp{abs(int(n)):,}".replace(",", ".")


def bulat(d):
    return int(Decimal(d).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def parse_rupiah(nilai):
    """'85rb' / '85.000' / 'Rp85.000' / '85k' / '1,5jt' / 85000 -> int. None bila kosong/tidak terbaca."""
    if nilai is None:
        return None
    if isinstance(nilai, bool):
        return None
    if isinstance(nilai, (int, float)):
        return bulat(Decimal(str(nilai)))
    s = str(nilai).strip().lower().replace("rp", "").replace(" ", "")
    if s in {"", "-", "?", "[isian]"} or s.startswith("[isian"):
        return None
    if s in {"gratis", "free", "0"}:
        return 0
    kali = Decimal(1)
    for akhiran, k in (("juta", 1000000), ("jt", 1000000), ("ribu", 1000), ("rb", 1000), ("k", 1000)):
        if s.endswith(akhiran):
            s, kali = s[: -len(akhiran)], Decimal(k)
            break
    if kali != 1:
        s = s.replace(",", ".")
        if s.count(".") > 1:
            return None
    else:
        # 85.000 / 85,000 / 1.250.000 -> pemisah ribuan
        if re.fullmatch(r"\d{1,3}([.,]\d{3})+", s):
            s = re.sub(r"[.,]", "", s)
        elif re.fullmatch(r"\d+[.,]\d{1,2}", s):
            s = s.replace(",", ".")
    try:
        d = Decimal(s) * kali
    except InvalidOperation:
        return None
    if d < 0:
        return None
    return bulat(d)


def parse_qty(nilai):
    if isinstance(nilai, bool):
        return None
    if isinstance(nilai, int):
        return nilai if nilai > 0 else None
    if isinstance(nilai, float):
        return int(nilai) if nilai > 0 and nilai == int(nilai) else None
    s = str(nilai).strip().lower().replace("pcs", "").replace("buah", "").replace("bh", "").strip()
    if re.fullmatch(r"\d+", s) and int(s) > 0:
        return int(s)
    return None


def norm(s):
    return re.sub(r"\s+", " ", str(s or "").strip().lower())


def baku_kurir(teks):
    t = norm(teks)
    if not t:
        return None, ""
    for pola, nama in KURIR_BAKU:
        if re.search(pola, t):
            sisa = re.sub(pola, "", t).strip(" -/")
            return nama, sisa.upper() if sisa else ""
    return str(teks).strip(), ""


# ---------- katalog ----------

def baca_katalog(path):
    katalog = {}
    if not path:
        return katalog, []
    catatan = []
    teks = Path(path).read_text(encoding="utf-8-sig")
    contoh = teks[:2000]
    pemisah = ";" if contoh.count(";") > contoh.count(",") else ","
    rd = csv.DictReader(io.StringIO(teks), delimiter=pemisah)
    if not rd.fieldnames:
        raise InputRusak("katalog kosong")
    kolom = {norm(k): k for k in rd.fieldnames if k}
    k_nama = next((kolom[k] for k in ("nama", "produk", "nama produk", "barang") if k in kolom), None)
    k_harga = next((kolom[k] for k in ("harga", "harga jual", "harga satuan") if k in kolom), None)
    if not k_nama or not k_harga:
        raise InputRusak("katalog wajib punya kolom 'nama' dan 'harga'")
    for no, b in enumerate(rd, start=2):
        nama = (b.get(k_nama) or "").strip()
        if not nama:
            continue
        harga = parse_rupiah(b.get(k_harga))
        if harga is None:
            catatan.append(f"katalog baris {no} ({nama}): harga tidak terbaca, dilewati")
            continue
        stok_raw = (b.get(kolom.get("stok", ""), "") or "").strip() if "stok" in kolom else ""
        stok = int(stok_raw) if re.fullmatch(r"\d+", stok_raw) else None
        isi = {"nama": nama, "harga": harga, "stok": stok}
        kunci = [norm(nama)]
        if "kode" in kolom and (b.get(kolom["kode"]) or "").strip():
            kunci.append(norm(b[kolom["kode"]]))
        if "alias" in kolom and (b.get(kolom["alias"]) or "").strip():
            kunci += [norm(a) for a in b[kolom["alias"]].split("|") if a.strip()]
        for k in kunci:
            if k in katalog and katalog[k]["nama"] != nama:
                catatan.append(f"katalog: '{k}' dipakai lebih dari satu produk; yang pertama dipakai")
                continue
            katalog.setdefault(k, isi)
    return katalog, catatan


# ---------- pesanan ----------

POLA_ITEM = re.compile(
    r"^(?:(?P<qd>\d+)\s*(?:x|pcs|buah)?\s+(?P<n1>.+?)|(?P<n2>.+)\s*[x\*×]\s*(?P<qb>\d+)(?:\s*(?:pcs|buah))?)"
    r"(?:\s*@\s*(?P<h>.+))?$", re.I)


def parse_item_teks(s):
    s = s.strip()
    if not s:
        return None
    m = POLA_ITEM.match(s)
    if not m:
        return {"nama": s, "qty": None, "harga": None, "_mentah": s}
    nama = (m.group("n1") or m.group("n2") or "").strip()
    qty = m.group("qd") or m.group("qb")
    return {"nama": nama, "qty": qty, "harga": m.group("h"), "_mentah": s}


def baca_teks(teks):
    tanggal = None
    blok, sekarang = [], {}
    for baris in teks.splitlines():
        b = baris.strip()
        if not b or b.startswith("//"):
            continue
        if re.fullmatch(r"-{3,}|#\s*pesanan.*", b, re.I):
            if sekarang:
                blok.append(sekarang)
            sekarang = {}
            continue
        if ":" not in b:
            if "item" in sekarang:  # lanjutan daftar item di baris baru
                sekarang["item"] += "; " + b.lstrip("-• ")
            continue
        k, v = b.split(":", 1)
        k = norm(k)
        if k == "tanggal":
            tanggal = v.strip()
            continue
        kk = KUNCI.get(k)
        if not kk:
            continue
        if kk == "item" and "item" in sekarang:
            sekarang["item"] += "; " + v.strip()
        else:
            sekarang[kk] = v.strip()
    if sekarang:
        blok.append(sekarang)
    pesanan = []
    for p in blok:
        items = [parse_item_teks(x) for x in re.split(r"[;\n]", p.get("item", ""))]
        p["item"] = [i for i in items if i]
        pesanan.append(p)
    return tanggal, pesanan


def baca_pesanan(path):
    teks = Path(path).read_text(encoding="utf-8-sig")
    if not teks.strip():
        raise InputRusak("file pesanan kosong")
    if teks.lstrip().startswith(("{", "[")):
        try:
            data = json.loads(teks)
        except json.JSONDecodeError as e:
            raise InputRusak(f"JSON tidak valid: {e}")
        if isinstance(data, list):
            data = {"pesanan": data}
        if not isinstance(data, dict) or not isinstance(data.get("pesanan"), list):
            raise InputRusak("JSON wajib berisi daftar 'pesanan'")
        kat = data.get("katalog") if isinstance(data.get("katalog"), list) else []
        hasil = []
        for p in data["pesanan"]:
            if not isinstance(p, dict):
                continue
            q = {KUNCI.get(norm(k), norm(k)): v for k, v in p.items()}
            items = q.get("item") or []
            if isinstance(items, str):
                items = [parse_item_teks(x) for x in re.split(r"[;\n]", items)]
            q["item"] = [i if isinstance(i, dict) else parse_item_teks(str(i)) for i in items if i]
            hasil.append(q)
        return data.get("tanggal"), hasil, kat
    tgl, ps = baca_teks(teks)
    return tgl, ps, []


def cek_alamat(alamat):
    a = str(alamat or "").strip()
    if not a:
        return ["alamat belum ada"]
    kurang = []
    if len(a) < 20 or len(a.split()) < 4:
        kurang.append("alamat terlalu singkat (perlu jalan/no, kel/kec, kota)")
    if not re.search(r"\b\d{5}\b", a):
        kurang.append("kode pos belum ada")
    return kurang


def cek_hp(hp):
    d = re.sub(r"\D", "", str(hp or ""))
    if not d:
        return None, "nomor HP penerima belum ada"
    if d.startswith("62"):
        d = "0" + d[2:]
    if not d.startswith("08") or not 10 <= len(d) <= 13:
        return d, "nomor HP penerima tampak tidak lengkap/salah"
    return d, None


def proses(pesanan, katalog, tanggal, mulai):
    tgl_kode = tanggal.strftime("%Y%m%d")
    hasil, ganda, sidik_ada = [], [], {}
    urut = mulai
    for idx, p in enumerate(pesanan, start=1):
        pel = str(p.get("pelanggan") or "").strip() or f"Pelanggan {idx}"
        items, masalah = [], []
        for it in p.get("item") or []:
            nama_in = str(it.get("nama") or "").strip()
            qty = parse_qty(it.get("qty"))
            k = katalog.get(norm(nama_in))
            harga = parse_rupiah(it.get("harga")) if it.get("harga") not in (None, "") else None
            sumber = "pengguna" if harga is not None else None
            if it.get("harga") not in (None, "") and (harga is None or harga <= 0):
                masalah.append(f"harga '{nama_in}' dari chat tidak terbaca atau tidak wajar ('{it.get('harga')}'); " + ("dipakai harga katalog" if k else "belum diketahui"))
                harga, sumber = None, None
            if harga is None and k:
                harga, sumber = k["harga"], "katalog"
            nama = k["nama"] if k else nama_in
            if not nama:
                masalah.append(f"ada item tanpa nama: '{it.get('_mentah', '')}'")
                continue
            if qty is None:
                masalah.append(f"jumlah '{nama}' tidak jelas ('{it.get('qty')}')")
            if harga is None:
                masalah.append(f"harga '{nama}' belum diketahui" + ("" if k else " (tidak ada di katalog)"))
            items.append({"nama": nama, "qty": qty, "harga": harga, "sumber_harga": sumber,
                          "total_baris": qty * harga if (qty is not None and harga is not None) else None})
        if not items:
            masalah.append("tidak ada item pesanan")

        sidik = (norm(pel), tuple(sorted((norm(i["nama"]), i["qty"] or 0) for i in items)))
        hp_sidik = re.sub(r"\D", "", str(p.get("hp") or ""))[-9:]
        sama = [s for s in sidik_ada.get(sidik, []) if not s[1] or not hp_sidik or s[1] == hp_sidik]
        if items and sama:
            ganda.append({"pelanggan": pel, "sama_dengan": sama[0][0]})
            continue

        lengkap = bool(items) and all(i["total_baris"] is not None for i in items)
        subtotal = sum(i["total_baris"] for i in items) if lengkap else None
        # diskon
        dsk_raw = p.get("diskon")
        diskon, dsk_label = 0, ""
        if dsk_raw not in (None, "", 0, "0"):
            s = str(dsk_raw).strip()
            m = re.fullmatch(r"(\d+(?:[.,]\d+)?)\s*%", s)
            if m:
                pct = Decimal(m.group(1).replace(",", "."))
                dsk_label = f"{m.group(1)}%"
                if pct > 100:
                    masalah.append("diskon lebih dari 100% diabaikan")
                    pct, dsk_label = Decimal(0), ""
                diskon = bulat(Decimal(subtotal) * pct / 100) if subtotal is not None else None
            else:
                diskon = parse_rupiah(s)
                if diskon is None:
                    masalah.append(f"diskon '{s}' tidak terbaca, dianggap 0")
                    diskon = 0
        if subtotal is not None and diskon is not None and diskon > subtotal:
            masalah.append("diskon melebihi subtotal, dibatasi sebesar subtotal")
            diskon = subtotal
        setelah = subtotal - diskon if (subtotal is not None and diskon is not None) else None

        kurir, layanan_kurir = baku_kurir(p.get("kurir"))
        layanan = str(p.get("layanan") or "").strip().upper() or layanan_kurir
        ambil = kurir == "Ambil sendiri"
        ongkir = 0 if ambil else parse_rupiah(p.get("ongkir"))
        if ongkir is None and not ambil:
            masalah.append("ongkir belum diketahui")
        total = setelah + ongkir if (setelah is not None and ongkir is not None) else None

        bayar = norm(p.get("bayar"))
        status_raw = norm(p.get("status"))
        cod = "cod" in bayar or "cod" in status_raw or str(p.get("cod")).lower() in {"true", "ya", "1"}
        dibayar = parse_rupiah(p.get("dibayar")) if p.get("dibayar") not in (None, "") else None
        if status_raw in {"lunas", "sudah bayar", "sudah transfer", "paid", "dibayar"} and dibayar is None:
            dibayar = total
            status_bayar = "lunas"
        elif cod:
            status_bayar = "COD (bayar saat terima)"
        elif dibayar is not None and total is not None and dibayar >= total:
            status_bayar = "lunas"
        elif dibayar:
            status_bayar = "dibayar sebagian"
        else:
            status_bayar = "belum bayar"
        sisa = (total - (dibayar or 0)) if (total is not None and status_bayar != "lunas") else (0 if status_bayar == "lunas" else None)
        if dibayar is not None and total is not None and dibayar > total:
            masalah.append(f"pembayaran {rupiah(dibayar)} melebihi total {rupiah(total)} (lebih {rupiah(dibayar - total)})")

        hp, hp_masalah = cek_hp(p.get("hp"))
        kurang_kirim = []
        if not ambil:
            kurang_kirim = cek_alamat(p.get("alamat"))
            if hp_masalah:
                kurang_kirim.append(hp_masalah)
            if not kurir:
                kurang_kirim.append("kurir belum dipilih")

        kode = str(p.get("kode") or "").strip() or f"{tgl_kode}-{urut:02d}"
        if not str(p.get("kode") or "").strip():
            urut += 1
        sidik_ada.setdefault(sidik, []).append((kode, hp_sidik))
        hasil.append({
            "kode": kode, "pelanggan": pel, "item": items,
            "subtotal": subtotal, "diskon": diskon, "diskon_label": dsk_label,
            "setelah_diskon": setelah, "ongkir": ongkir, "total": total,
            "lengkap": total is not None,
            "kurir": kurir or "", "layanan": layanan, "cod": cod,
            "nilai_cod": total if cod else None,
            "status_bayar": status_bayar, "dibayar": dibayar, "sisa_tagihan": sisa,
            "penerima": str(p.get("penerima") or "").strip() or pel,
            "hp": hp or "", "alamat": str(p.get("alamat") or "").strip(),
            "catatan": str(p.get("catatan") or "").strip(),
            "masalah": masalah, "data_kirim_kurang": kurang_kirim,
            "isi_paket": ", ".join(f"{i['nama']} x{i['qty'] if i['qty'] else '?'}" for i in items),
        })
    return hasil, ganda


def rekap_harian(hasil, katalog):
    lengkap = [h for h in hasil if h["lengkap"]]
    omzet = sum(h["setelah_diskon"] for h in lengkap)
    tagihan = sum(h["total"] for h in lengkap)
    ongkir = sum(h["ongkir"] for h in lengkap)
    terjual = {}
    for h in hasil:
        for i in h["item"]:
            if i["qty"]:
                terjual[i["nama"]] = terjual.get(i["nama"], 0) + i["qty"]
    terlaris = sorted(terjual.items(), key=lambda x: (-x[1], x[0]))[:5]
    belum = [{"kode": h["kode"], "pelanggan": h["pelanggan"], "status": h["status_bayar"],
              "sisa": h["sisa_tagihan"]} for h in hasil if h["status_bayar"] in {"belum bayar", "dibayar sebagian"}]
    cod = [{"kode": h["kode"], "pelanggan": h["pelanggan"], "nilai_cod": h["nilai_cod"]} for h in hasil if h["cod"]]
    stok_kurang = []
    stok_dicek = {}
    for v in katalog.values():
        stok_dicek[v["nama"]] = v["stok"]
    for nama, q in terjual.items():
        s = stok_dicek.get(nama)
        if s is not None and q > s:
            stok_kurang.append({"nama": nama, "dipesan": q, "stok": s, "kurang": q - s})
    return {
        "jumlah_pesanan": len(hasil),
        "pesanan_angka_lengkap": len(lengkap),
        "pesanan_belum_lengkap": [h["kode"] for h in hasil if not h["lengkap"]],
        "omzet_barang": omzet, "total_ongkir": ongkir, "total_tagihan": tagihan,
        "terlaris": [{"nama": n, "qty": q} for n, q in terlaris],
        "belum_bayar": belum,
        "total_belum_bayar": sum(b["sisa"] for b in belum if b["sisa"] is not None),
        "cod": cod,
        "stok_kurang": stok_kurang,
    }


def serah_terima(hasil):
    grup = {}
    for h in hasil:
        if h["kurir"] == "Ambil sendiri":
            continue
        grup.setdefault(h["kurir"] or "Kurir belum dipilih", []).append(
            {"kode": h["kode"], "penerima": h["penerima"], "layanan": h["layanan"],
             "isi": h["isi_paket"], "cod": h["cod"], "nilai_cod": h["nilai_cod"]})
    return grup


def blok_csv(hasil, tanggal):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["kode", "tanggal", "pelanggan", "isi_pesanan", "jumlah_barang", "subtotal", "diskon",
                "ongkir", "total", "kurir", "layanan", "cod", "status_bayar", "sisa_tagihan"])
    for h in hasil:
        w.writerow([h["kode"], tanggal.isoformat(), h["pelanggan"], h["isi_paket"],
                    sum(i["qty"] or 0 for i in h["item"]),
                    *["" if h[k] is None else h[k] for k in ("subtotal", "diskon", "ongkir", "total")],
                    h["kurir"], h["layanan"], "ya" if h["cod"] else "tidak", h["status_bayar"],
                    "" if h["sisa_tagihan"] is None else h["sisa_tagihan"]])
    return buf.getvalue()


def rp_atau_isian(n, isian):
    return rupiah(n) if n is not None else f"[isian: {isian}]"


def cetak_teks(out):
    L = []
    t = out["tanggal"]
    L.append(f"=== REKAP PESANAN {t} ===")
    for h in out["pesanan"]:
        L.append("")
        L.append(f"[{h['kode']}] {h['pelanggan']}")
        for i in h["item"]:
            q = i["qty"] if i["qty"] else "?"
            hg = rupiah(i["harga"]) if i["harga"] is not None else "[isian: harga]"
            tb = rupiah(i["total_baris"]) if i["total_baris"] is not None else "[isian]"
            L.append(f"  - {i['nama']} x{q} @ {hg} = {tb}")
        L.append(f"  Subtotal      : {rp_atau_isian(h['subtotal'], 'subtotal')}")
        if h["diskon"]:
            lab = f" ({h['diskon_label']})" if h["diskon_label"] else ""
            L.append(f"  Diskon{lab:<8}: -{rp_atau_isian(h['diskon'], 'diskon')}")
        L.append(f"  Ongkir        : {rp_atau_isian(h['ongkir'], 'ongkir')}")
        L.append(f"  TOTAL         : {rp_atau_isian(h['total'], 'total, menunggu ' + ('harga' if h['subtotal'] is None else 'ongkir'))}")
        if h["dibayar"] and h["status_bayar"] != "lunas":
            L.append(f"  Sudah dibayar : {rupiah(h['dibayar'])} | Sisa: {rp_atau_isian(h['sisa_tagihan'], 'sisa')}")
        L.append(f"  Bayar         : {h['status_bayar']}")
        L.append(f"  Kirim         : {h['kurir'] or '[isian: kurir]'} {h['layanan']}".rstrip())
        for m in h["masalah"]:
            L.append(f"  ! {m}")
        for m in h["data_kirim_kurang"]:
            L.append(f"  ? {m}")
    if out["pesanan_ganda"]:
        L.append("")
        L.append("PESANAN GANDA (tidak dihitung dua kali):")
        for g in out["pesanan_ganda"]:
            L.append(f"  - {g['pelanggan']}: sama dengan {g['sama_dengan']}")
    r = out["rekap_harian"]
    L.append("")
    L.append("=== REKAP HARIAN (tanpa HP & alamat) ===")
    L.append(f"Jumlah pesanan       : {r['jumlah_pesanan']} ({r['pesanan_angka_lengkap']} angka lengkap)")
    if r["pesanan_belum_lengkap"]:
        L.append(f"Belum lengkap angka  : {', '.join(r['pesanan_belum_lengkap'])} (tidak masuk omzet)")
    L.append(f"Omzet barang         : {rupiah(r['omzet_barang'])}")
    L.append(f"Ongkir ditagihkan    : {rupiah(r['total_ongkir'])}")
    L.append(f"Total tagihan        : {rupiah(r['total_tagihan'])}")
    L.append("Terlaris             : " + (", ".join(f"{x['nama']} ({x['qty']})" for x in r["terlaris"]) or "-"))
    L.append(f"Belum bayar          : {len(r['belum_bayar'])} pesanan, {rupiah(r['total_belum_bayar'])}")
    for b in r["belum_bayar"]:
        L.append(f"  - {b['kode']} {b['pelanggan']}: {rp_atau_isian(b['sisa'], 'nominal')} ({b['status']})")
    if r["cod"]:
        L.append(f"COD                  : {len(r['cod'])} paket")
        for c in r["cod"]:
            L.append(f"  - {c['kode']} {c['pelanggan']}: {rp_atau_isian(c['nilai_cod'], 'nilai COD')}")
    for s in r["stok_kurang"]:
        L.append(f"! Stok kurang: {s['nama']} dipesan {s['dipesan']}, stok {s['stok']} (kurang {s['kurang']})")
    L.append("")
    L.append("=== SERAH-TERIMA KURIR ===")
    for kurir, daftar in out["serah_terima_kurir"].items():
        L.append(f"{kurir} - {len(daftar)} paket")
        for n, d in enumerate(daftar, 1):
            cod = f" | COD {rp_atau_isian(d['nilai_cod'], 'nilai COD')}" if d["cod"] else " | non-COD"
            L.append(f"  {n}. {d['kode']} | {d['penerima']} | {d['layanan'] or '-'} | {d['isi']}{cod} | resi: [isian: resi]")
    L.append("")
    L.append("=== LABEL (berisi alamat & HP: hanya untuk ditempel di paket) ===")
    for h in out["pesanan"]:
        if h["kurir"] == "Ambil sendiri":
            continue
        L.append(f"[{h['kode']}] Penerima: {h['penerima']} | HP: {h['hp'] or '[isian: HP]'}")
        alamat = h["alamat"] or "[isian: alamat lengkap]"
        if h["alamat"] and any(m.startswith(("alamat", "kode pos")) for m in h["data_kirim_kurang"]):
            alamat += " [isian: lengkapi alamat/kode pos]"
        L.append(f"  Alamat: {alamat}")
        L.append(f"  Isi: {h['isi_paket']} | {h['kurir'] or '[isian: kurir]'} {h['layanan']}".rstrip())
        L.append(f"  {'COD ' + rp_atau_isian(h['nilai_cod'], 'nilai COD') if h['cod'] else 'NON-COD'}"
                 + (f" | Catatan: {h['catatan']}" if h["catatan"] else ""))
    L.append("")
    L.append("=== CSV (tanpa HP & alamat) ===")
    L.append(out["csv"].rstrip("\n"))
    for c in out["catatan"]:
        L.append(f"catatan: {c}")
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Rekap pesanan WA: total, rekap harian, serah-terima kurir")
    ap.add_argument("pesanan", help="file pesanan (.json atau teks sederhana)")
    ap.add_argument("--katalog", help="CSV katalog (kolom nama,harga; opsional kode,alias,stok)")
    ap.add_argument("--tanggal", help="tanggal pesanan YYYY-MM-DD (default: dari file atau hari ini)")
    ap.add_argument("--mulai", type=int, default=1, help="nomor urut pertama kode pesanan (default 1)")
    ap.add_argument("--format", choices=["teks", "json"], default="teks")
    a = ap.parse_args(argv)
    try:
        tgl_file, pesanan, kat_json = baca_pesanan(a.pesanan)
        katalog, catatan = baca_katalog(a.katalog)
        for k in kat_json:
            if isinstance(k, dict) and k.get("nama") and parse_rupiah(k.get("harga")) is not None:
                isi = {"nama": str(k["nama"]).strip(), "harga": parse_rupiah(k["harga"]),
                       "stok": k.get("stok") if isinstance(k.get("stok"), int) else None}
                katalog.setdefault(norm(isi["nama"]), isi)
                for al in [k.get("kode")] + list(k.get("alias") or []):
                    if al:
                        katalog.setdefault(norm(al), isi)
        tgl_s = a.tanggal or tgl_file
        try:
            tanggal = date.fromisoformat(str(tgl_s).strip()) if tgl_s else date.today()
        except ValueError:
            raise InputRusak(f"tanggal '{tgl_s}' bukan format YYYY-MM-DD")
        if a.mulai < 1:
            raise InputRusak("--mulai minimal 1")
        if not pesanan:
            raise InputRusak("tidak ada pesanan yang terbaca")
        hasil, ganda = proses(pesanan, katalog, tanggal, a.mulai)
    except InputRusak as e:
        msg = {"ok": False, "galat": str(e)}
        print(json.dumps(msg, ensure_ascii=False) if a.format == "json" else f"GALAT: {e}")
        return 2
    except (OSError, UnicodeDecodeError) as e:
        msg = {"ok": False, "galat": f"file tidak bisa dibaca: {e}"}
        print(json.dumps(msg, ensure_ascii=False) if a.format == "json" else f"GALAT: {msg['galat']}")
        return 2
    out = {
        "ok": True, "tanggal": tanggal.isoformat(), "pesanan": hasil, "pesanan_ganda": ganda,
        "rekap_harian": rekap_harian(hasil, katalog), "serah_terima_kurir": serah_terima(hasil),
        "csv": blok_csv(hasil, tanggal), "catatan": catatan,
    }
    if a.format == "json":
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(cetak_teks(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
