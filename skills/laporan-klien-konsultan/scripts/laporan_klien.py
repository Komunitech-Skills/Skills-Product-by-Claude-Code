#!/usr/bin/env python3
"""laporan-klien-konsultan (Komunitech) - log kerja lokal + draf laporan progres per klien.

Untuk konsultan/freelancer (pajak, hukum, IT, desain, marketing, dst.) yang harus rutin
mengirim laporan progres ke klien. Semua data disimpan di SATU file CSV lokal (tidak ada
database eksternal, tidak ada akun, tidak ada kirim data ke mana pun). Hanya library
standar Python 3.8+, lintas OS (Windows: `python`/`py`).

Skema kolom log (satu baris = satu pekerjaan yang dicatat):
  tanggal,klien,proyek,pekerjaan,jam,status,kendala,butuh_dari_klien
  - tanggal: YYYY-MM-DD
  - status: selesai | berjalan | terkendala
  - jam: opsional, boleh kosong (mis. konsultasi tanpa hitungan jam)
  - kendala: hambatan di pihak konsultan (opsional)
  - butuh_dari_klien: sesuatu yang perlu klien berikan/putuskan (opsional)

Lokasi file log (urutan prioritas):
  1. --file PATH
  2. ENV KOMUNITECH_LAPORAN_KLIEN_FILE
  3. default: log-kerja-klien.csv (folder kerja saat ini)

Perintah tulis (`catat`) langsung menambah baris (auto-membuat file+header bila belum ada).
Perintah baca (`laporan`, `daftar-klien`) tidak pernah mengubah file.

Contoh:
  python3 laporan_klien.py catat --klien "PT Maju Jaya" --proyek "Pembukuan bulanan" \\
      --pekerjaan "Rekonsiliasi bank September" --jam 2.5 --status selesai
  python3 laporan_klien.py catat --klien "PT Maju Jaya" --proyek "Pembukuan bulanan" \\
      --pekerjaan "Susun draf SPT Masa PPN" --status berjalan \\
      --butuh-klien "Faktur pajak masukan Oktober belum dikirim"
  python3 laporan_klien.py laporan --klien "PT Maju Jaya" --periode mingguan \\
      --rencana "Selesaikan draf SPT Masa;Jadwalkan review dengan klien" --json

Kode keluar: 0 = normal. 1 = input/file tidak valid. 2 = argumen salah tulis.
3 = draf berhasil dibuat TAPI ada pola mirip data pribadi/rahasia terdeteksi di salah satu
    kolom teks -- lihat pesan di stderr, TINJAU ULANG sebelum dikirim ke klien (lihat SKILL.md).
"""
import argparse
import csv
import json
import os
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

APLIKASI = "laporan-klien-konsultan"
VERSI = "1.0.0"
SKEMA = 1

KOLOM = ["tanggal", "klien", "proyek", "pekerjaan", "jam", "status", "kendala", "butuh_dari_klien"]
STATUS_VALID = ("selesai", "berjalan", "terkendala")
LABEL_STATUS = {"selesai": "Selesai", "berjalan": "Berjalan", "terkendala": "Terkendala"}

BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
         "Agustus", "September", "Oktober", "November", "Desember"]
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

# Pola deteksi data pribadi/rahasia klien -- deteksi saja (tidak memblokir), sama seperti
# skill laporan-otomatis-terjadwal. Batas kata (\b) supaya tidak salah kena kata yang cuma
# "kebetulan mengandung" polanya (mis. "unik" tidak kena "nik").
POLA_SENSITIF = [
    ("NIK", re.compile(r"\bnik\b", re.IGNORECASE)),
    ("nomor KTP", re.compile(r"\b(no\.?\s*ktp|nomor\s*ktp|ktp)\b", re.IGNORECASE)),
    ("nomor HP/telepon (angka)", re.compile(
        r"(?<![\w+\-/#])\(?(\+62|62|0)[\s.\-]?8\d{1,3}\)?(?:[\s.\-]?\d){6,10}(?![\w])")),
    ("email pribadi", re.compile(r"\b[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}\b")),
    ("kata sandi/kredensial", re.compile(
        r"\b(password|kata\s*sandi|kredensial|api\s*key|access\s*token|secret\s*key)\b",
        re.IGNORECASE)),
    ("dokumen rahasia disebut eksplisit", re.compile(r"\brahasia\b", re.IGNORECASE)),
]


class Gagal(Exception):
    def __init__(self, pesan, **detail):
        super().__init__(pesan)
        self.pesan = pesan
        self.detail = detail


# ---------------------------------------------------------------------------
# Util umum
# ---------------------------------------------------------------------------

def cari_file(arg_file):
    if arg_file:
        return Path(arg_file).expanduser()
    env = os.environ.get("KOMUNITECH_LAPORAN_KLIEN_FILE")
    if env:
        return Path(env).expanduser()
    return Path("log-kerja-klien.csv")


def aman_csv(teks):
    """Cegah formula injection bila file dibuka di Excel/Sheets (=, +, -, @ di awal sel)."""
    teks = "" if teks is None else str(teks)
    if teks[:1] in ("=", "+", "-", "@"):
        return "'" + teks
    return teks


def baca_tanggal(teks, acuan=None):
    acuan = acuan or date.today()
    if teks is None:
        return acuan
    t = teks.strip().lower()
    if t in ("", "hari-ini", "hariini", "today"):
        return acuan
    if t in ("kemarin", "yesterday"):
        return acuan - timedelta(days=1)
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(teks.strip(), fmt).date()
        except ValueError:
            continue
    raise Gagal(f"Tanggal '{teks}' tidak dikenali. Pakai format YYYY-MM-DD (mis. 2026-09-24), "
                "'hari-ini', atau 'kemarin'.")


def parse_jam(teks):
    if teks is None or str(teks).strip() == "":
        return None
    t = str(teks).strip().replace(",", ".")
    try:
        nilai = float(t)
    except ValueError:
        raise Gagal(f"Jam '{teks}' bukan angka. Contoh yang benar: 2 atau 2.5 (atau 2,5).")
    if nilai < 0:
        raise Gagal("Jam tidak boleh negatif.")
    if nilai > 24:
        raise Gagal(f"Jam '{nilai}' tidak masuk akal untuk satu pekerjaan (>24 jam). "
                     "Pecah jadi beberapa baris `catat` bila memang lintas hari.")
    return nilai


def format_jam(nilai):
    if nilai is None:
        return "-"
    if float(nilai).is_integer():
        return f"{int(nilai)} jam"
    return f"{nilai:.1f}".rstrip("0").rstrip(".").replace(".", ",") + " jam"


def normalisasi_status(teks):
    t = (teks or "berjalan").strip().lower()
    alias = {
        "selesai": "selesai", "done": "selesai", "tuntas": "selesai", "beres": "selesai",
        "berjalan": "berjalan", "progress": "berjalan", "in progress": "berjalan",
        "sedang berjalan": "berjalan", "ongoing": "berjalan",
        "terkendala": "terkendala", "kendala": "terkendala", "stuck": "terkendala",
        "blocked": "terkendala", "tertunda": "terkendala",
    }
    if t not in alias:
        raise Gagal(f"Status '{teks}' tidak dikenali. Pakai salah satu: {', '.join(STATUS_VALID)}.")
    return alias[t]


def tanggal_indo(d):
    return f"{HARI[d.weekday()]}, {d.day} {BULAN[d.month - 1]} {d.year}"


def format_periode_label(d1, d2):
    if d1 == d2:
        return tanggal_indo(d1)
    return f"{d1.day} {BULAN[d1.month - 1]} {d1.year} - {d2.day} {BULAN[d2.month - 1]} {d2.year}"


def rentang_periode(nama, acuan):
    nama = (nama or "minggu-ini").strip().lower()
    if nama in ("mingguan",):
        nama = "minggu-ini"
    if nama in ("bulanan",):
        nama = "bulan-ini"
    if nama == "minggu-ini":
        a = acuan - timedelta(days=acuan.weekday())
        return "Minggu ini", a, a + timedelta(days=6)
    if nama == "minggu-lalu":
        a = acuan - timedelta(days=acuan.weekday() + 7)
        return "Minggu lalu", a, a + timedelta(days=6)
    if nama == "bulan-ini":
        a = acuan.replace(day=1)
        akhir_bulan = (a.replace(month=a.month % 12 + 1, day=1) if a.month != 12
                       else a.replace(year=a.year + 1, month=1, day=1)) - timedelta(days=1)
        return f"Bulan {BULAN[a.month - 1]} {a.year}", a, akhir_bulan
    if nama == "bulan-lalu":
        pertama_bulan_ini = acuan.replace(day=1)
        akhir_bulan_lalu = pertama_bulan_ini - timedelta(days=1)
        a = akhir_bulan_lalu.replace(day=1)
        return f"Bulan {BULAN[a.month - 1]} {a.year}", a, akhir_bulan_lalu
    raise Gagal("--periode harus salah satu: mingguan, bulanan, minggu-ini, minggu-lalu, "
                "bulan-ini, bulan-lalu (atau pakai --dari/--sampai).")


def deteksi_sensitif(teks, sumber, temuan_keluar):
    if not teks:
        return
    for nama_pola, pola in POLA_SENSITIF:
        if pola.search(teks):
            temuan_keluar.append(
                f"{sumber} berisi '{teks}' -- mengandung pola mirip {nama_pola}. Sesuai UU PDP "
                "(UU 27/2022), catat seperlunya saja dan tinjau ulang sebelum draf ini dikirim "
                "ke klien atau disimpan lebih lama dari perlu."
            )


# ---------------------------------------------------------------------------
# Baca/tulis log
# ---------------------------------------------------------------------------

def pastikan_file(path):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(KOLOM)
        return True
    return False


def baca_log(path):
    if not path.exists():
        raise Gagal(f"File log '{path}' tidak ditemukan. Catat pekerjaan dulu dengan perintah "
                    "`catat`, atau jalankan `init` untuk membuat file kosong.")
    try:
        with path.open(newline="", encoding="utf-8-sig") as f:
            r = csv.DictReader(f)
            if r.fieldnames is None:
                return []
            hilang = [k for k in KOLOM if k not in r.fieldnames]
            if hilang:
                raise Gagal(f"File log '{path}' tidak berkolom {hilang} -- pastikan header persis: "
                            f"{','.join(KOLOM)}.")
            baris = list(r)
    except csv.Error as e:
        raise Gagal(f"File log '{path}' tidak bisa dibaca sebagai CSV: {e}")
    hasil = []
    for i, b in enumerate(baris, start=2):
        try:
            tgl = baca_tanggal(b.get("tanggal", ""))
        except Gagal as e:
            raise Gagal(f"Baris {i} '{path.name}': {e.pesan}")
        try:
            status = normalisasi_status(b.get("status", ""))
        except Gagal as e:
            raise Gagal(f"Baris {i} '{path.name}': {e.pesan}")
        jam = None
        if (b.get("jam") or "").strip() != "":
            try:
                jam = parse_jam(b.get("jam"))
            except Gagal as e:
                raise Gagal(f"Baris {i} '{path.name}': {e.pesan}")
        hasil.append({
            "tanggal": tgl, "klien": (b.get("klien") or "").strip(),
            "proyek": (b.get("proyek") or "").strip(), "pekerjaan": (b.get("pekerjaan") or "").strip(),
            "jam": jam, "status": status, "kendala": (b.get("kendala") or "").strip(),
            "butuh_dari_klien": (b.get("butuh_dari_klien") or "").strip(),
        })
    return hasil


def tulis_baris(path, entri):
    baru = pastikan_file(path)
    with path.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([aman_csv(entri[k]) if k != "jam" else ("" if entri[k] is None else entri[k])
                    for k in KOLOM])
    return baru


# ---------------------------------------------------------------------------
# Perintah
# ---------------------------------------------------------------------------

def cmd_init(args):
    path = cari_file(args.file)
    if path.exists() and not args.paksa:
        raise Gagal(f"File '{path}' sudah ada. Pakai --paksa untuk menimpanya dengan file kosong "
                    "baru (isi lama akan hilang -- cadangkan dulu bila perlu).")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(KOLOM)
    hasil = {"dibuat": str(path)}
    if args.json:
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
    else:
        print(f"File log baru dibuat: {path}")
    return 0


def cmd_catat(args):
    path = cari_file(args.file)
    klien = (args.klien or "").strip()
    proyek = (args.proyek or "").strip()
    pekerjaan = (args.pekerjaan or "").strip()
    if not klien:
        raise Gagal("--klien wajib diisi (nama klien/perusahaan).")
    if not proyek:
        raise Gagal("--proyek wajib diisi (nama proyek/layanan, mis. 'Pembukuan bulanan').")
    if not pekerjaan:
        raise Gagal("--pekerjaan wajib diisi (apa yang dikerjakan, dalam satu kalimat).")
    tgl = baca_tanggal(args.tanggal)
    jam = parse_jam(args.jam)
    status = normalisasi_status(args.status)
    kendala = (args.kendala or "").strip()
    butuh = (args.butuh_klien or "").strip()

    peringatan = []
    deteksi_sensitif(pekerjaan, "Kolom pekerjaan", peringatan)
    deteksi_sensitif(kendala, "Kolom kendala", peringatan)
    deteksi_sensitif(butuh, "Kolom butuh_dari_klien", peringatan)

    entri = {"tanggal": tgl.isoformat(), "klien": klien, "proyek": proyek, "pekerjaan": pekerjaan,
             "jam": jam, "status": status, "kendala": kendala, "butuh_dari_klien": butuh}
    file_baru = tulis_baris(path, entri)

    hasil = {"skema": SKEMA, "dicatat": {**entri, "jam": jam}, "file": str(path),
             "file_baru_dibuat": file_baru, "peringatan": peringatan}
    if args.json:
        print(json.dumps(hasil, ensure_ascii=False, indent=2, default=str))
    else:
        print(f"Tercatat: [{LABEL_STATUS[status]}] {klien} / {proyek} -- {pekerjaan} "
              f"({tgl.isoformat()}{', ' + format_jam(jam) if jam is not None else ''})")
        if file_baru:
            print(f"(File log baru dibuat di: {path})")
    if peringatan:
        for p in peringatan:
            print("PERINGATAN: " + p, file=sys.stderr)
        return 3
    return 0


def cmd_daftar_klien(args):
    path = cari_file(args.file)
    entri = baca_log(path)
    klien = sorted({e["klien"] for e in entri if e["klien"]})
    if args.json:
        print(json.dumps({"file": str(path), "klien": klien}, ensure_ascii=False, indent=2))
    else:
        if not klien:
            print(f"Belum ada catatan di '{path}'.")
        else:
            print(f"Klien tercatat di '{path}':")
            for k in klien:
                print(f"- {k}")
    return 0


def _dedup_urut(items):
    dilihat = set()
    hasil = []
    for it in items:
        if it and it not in dilihat:
            dilihat.add(it)
            hasil.append(it)
    return hasil


def susun_laporan(entri_periode, klien, label_periode, awal, akhir, rencana_manual, catatan):
    selesai = [e for e in entri_periode if e["status"] == "selesai"]
    berjalan = [e for e in entri_periode if e["status"] == "berjalan"]
    terkendala = [e for e in entri_periode if e["status"] == "terkendala"]

    berjam = [e for e in entri_periode if e["jam"] is not None]
    tanpa_jam = len(entri_periode) - len(berjam)
    total_jam = round(sum(e["jam"] for e in berjam), 2) if berjam else 0.0
    per_proyek = {}
    for e in berjam:
        per_proyek[e["proyek"]] = round(per_proyek.get(e["proyek"], 0.0) + e["jam"], 2)

    kendala = _dedup_urut(e["kendala"] for e in entri_periode)
    butuh = _dedup_urut(e["butuh_dari_klien"] for e in entri_periode)

    if rencana_manual:
        rencana = [r.strip() for r in rencana_manual if r.strip()]
    else:
        rencana = [f"Lanjutkan: {e['pekerjaan']} ({e['proyek']})" for e in berjalan]
        if not rencana:
            rencana = []

    if not entri_periode:
        catatan.append(
            f"Tidak ada catatan pekerjaan untuk '{klien}' pada periode {label_periode.lower()} "
            f"({awal.isoformat()} s/d {akhir.isoformat()}). Laporan di bawah kosong -- jangan "
            "mengarang isi; catat dulu pekerjaannya dengan perintah `catat`."
        )
    if tanpa_jam:
        catatan.append(
            f"{tanpa_jam} dari {len(entri_periode)} entri tidak mencatat jam -- total jam di "
            "bawah TIDAK termasuk entri tersebut (bukan dianggap 0)."
        )

    bagian = {
        "selesai": selesai, "berjalan": berjalan, "terkendala": terkendala,
        "kendala": kendala, "butuh_dari_klien": butuh, "rencana": rencana,
        "total_jam": total_jam, "entri_tanpa_jam": tanpa_jam, "per_proyek": per_proyek,
        "jumlah_entri": len(entri_periode),
    }

    ringkasan = (
        f"Periode {label_periode.lower()} ({format_periode_label(awal, akhir)}): "
        f"{len(selesai)} pekerjaan selesai, {len(berjalan)} sedang berjalan"
        + (f", {len(terkendala)} terkendala" if terkendala else "")
        + f". Total jam tercatat: {format_jam(total_jam) if berjam else 'tidak ada jam dicatat'}."
    )
    bagian["ringkasan"] = ringkasan
    return bagian


def _baris_kerja(e, dengan_tanggal=True):
    inti = f"{e['pekerjaan']} ({e['proyek']}"
    if dengan_tanggal:
        inti += f", {e['tanggal'].isoformat()}"
    if e["jam"] is not None:
        inti += f", {format_jam(e['jam'])}"
    inti += ")"
    return inti


def buat_markdown(klien, label_periode, awal, akhir, b):
    L = []
    L.append(f"# Laporan Progres -- {klien}")
    L.append(f"**Periode:** {label_periode} ({format_periode_label(awal, akhir)})\n")
    L.append("## Ringkasan")
    L.append(b["ringkasan"] + "\n")
    L.append("## Yang Selesai")
    L += [f"- {_baris_kerja(e)}" for e in b["selesai"]] or ["- (tidak ada pekerjaan selesai pada periode ini)"]
    L.append("")
    L.append("## Yang Sedang Berjalan")
    L += [f"- {_baris_kerja(e)}" for e in b["berjalan"]] or ["- (tidak ada pekerjaan berjalan)"]
    L.append("")
    if b["terkendala"]:
        L.append("## Terkendala")
        L += [f"- {_baris_kerja(e)}" for e in b["terkendala"]]
        L.append("")
    L.append("## Butuh dari Klien")
    L += [f"- {x}" for x in b["butuh_dari_klien"]] or ["- Tidak ada yang dibutuhkan saat ini."]
    L.append("")
    L.append("## Kendala Saat Ini")
    L += [f"- {x}" for x in b["kendala"]] or ["- Tidak ada kendala berarti."]
    L.append("")
    L.append("## Rencana Berikutnya")
    L += [f"- {x}" for x in b["rencana"]] or ["- (isi rencana berikutnya sebelum mengirim)"]
    L.append("")
    L.append("## Total Jam")
    if b["per_proyek"]:
        L.append(f"**Total: {format_jam(b['total_jam'])}**" +
                  (f" (dari {b['jumlah_entri'] - b['entri_tanpa_jam']} entri berjam; "
                   f"{b['entri_tanpa_jam']} entri tanpa jam tidak dihitung)" if b["entri_tanpa_jam"] else ""))
        for p, j in sorted(b["per_proyek"].items()):
            L.append(f"- {p}: {format_jam(j)}")
    else:
        L.append("Tidak ada jam yang dicatat pada periode ini.")
    L.append("\n---")
    L.append("_Draf disusun otomatis dari catatan kerja lokal. Tinjau sebelum dikirim ke klien._")
    return "\n".join(L)


def buat_teks_email(klien, label_periode, awal, akhir, b):
    L = []
    L.append(f"Subjek: Laporan Progres {label_periode} -- {klien} ({format_periode_label(awal, akhir)})\n")
    L.append(f"Yth. Bapak/Ibu {klien},\n")
    L.append(f"Berikut laporan progres untuk periode {format_periode_label(awal, akhir)}.\n")
    L.append(f"Ringkasan: {b['ringkasan']}\n")
    L.append("Yang sudah selesai:")
    L += [f"- {_baris_kerja(e, dengan_tanggal=False)}" for e in b["selesai"]] or ["- (belum ada yang selesai pada periode ini)"]
    L.append("\nYang sedang berjalan:")
    L += [f"- {_baris_kerja(e, dengan_tanggal=False)}" for e in b["berjalan"]] or ["- (tidak ada pekerjaan berjalan)"]
    if b["terkendala"]:
        L.append("\nTerkendala:")
        L += [f"- {_baris_kerja(e, dengan_tanggal=False)}" for e in b["terkendala"]]
    if b["butuh_dari_klien"]:
        L.append("\nMohon bantuan/keputusan dari Bapak/Ibu untuk:")
        L += [f"- {x}" for x in b["butuh_dari_klien"]]
    if b["rencana"]:
        L.append("\nRencana berikutnya:")
        L += [f"- {x}" for x in b["rencana"]]
    L.append("\nDemikian laporan ini kami sampaikan. Silakan hubungi kami bila ada pertanyaan.\n")
    L.append("Hormat kami,\n[Nama Anda]")
    return "\n".join(L)


def buat_teks_wa(klien, label_periode, awal, akhir, b):
    L = []
    L.append(f"*Laporan Progres -- {klien}*")
    L.append(f"_{label_periode}, {format_periode_label(awal, akhir)}_\n")
    L.append(b["ringkasan"] + "\n")
    L.append("*Selesai:*")
    L += [f"- {_baris_kerja(e, dengan_tanggal=False)}" for e in b["selesai"]] or ["- Belum ada"]
    L.append("\n*Berjalan:*")
    L += [f"- {_baris_kerja(e, dengan_tanggal=False)}" for e in b["berjalan"]] or ["- Tidak ada"]
    if b["terkendala"]:
        L.append("\n*Terkendala:*")
        L += [f"- {_baris_kerja(e, dengan_tanggal=False)}" for e in b["terkendala"]]
    if b["butuh_dari_klien"]:
        L.append("\n*Butuh dari Bapak/Ibu:*")
        L += [f"- {x}" for x in b["butuh_dari_klien"]]
    if b["rencana"]:
        L.append("\n*Rencana berikutnya:*")
        L += [f"- {x}" for x in b["rencana"]]
    return "\n".join(L)


def cmd_laporan(args):
    path = cari_file(args.file)
    klien = (args.klien or "").strip()
    if not klien:
        raise Gagal("--klien wajib diisi.")
    semua = baca_log(path)

    acuan = baca_tanggal(args.tanggal_acuan) if args.tanggal_acuan else date.today()
    if args.dari or args.sampai:
        if not (args.dari and args.sampai):
            raise Gagal("--dari dan --sampai harus diisi berdua.")
        awal = baca_tanggal(args.dari)
        akhir = baca_tanggal(args.sampai)
        if akhir < awal:
            raise Gagal("--sampai lebih awal dari --dari.")
        label_periode = "Periode kustom"
    else:
        label_periode, awal, akhir = rentang_periode(args.periode, acuan)

    cocok_klien = [e for e in semua if e["klien"].strip().lower() == klien.lower()]
    if not cocok_klien and semua:
        klien_ada = sorted({e["klien"] for e in semua})
        raise Gagal(f"Tidak ada catatan untuk klien '{klien}' di '{path}'. Klien yang tercatat: "
                    f"{', '.join(klien_ada) if klien_ada else '(kosong)'}.")
    entri_periode = [e for e in cocok_klien if awal <= e["tanggal"] <= akhir]
    entri_periode.sort(key=lambda e: e["tanggal"])

    catatan = []
    peringatan = []
    b = susun_laporan(entri_periode, klien, label_periode, awal, akhir, args.rencana, catatan)

    for e in entri_periode:
        deteksi_sensitif(e["pekerjaan"], f"Baris {e['tanggal'].isoformat()} (pekerjaan)", peringatan)
        deteksi_sensitif(e["kendala"], f"Baris {e['tanggal'].isoformat()} (kendala)", peringatan)
        deteksi_sensitif(e["butuh_dari_klien"], f"Baris {e['tanggal'].isoformat()} (butuh_dari_klien)",
                          peringatan)

    markdown = buat_markdown(klien, label_periode, awal, akhir, b)
    teks_email = buat_teks_email(klien, label_periode, awal, akhir, b)
    teks_wa = buat_teks_wa(klien, label_periode, awal, akhir, b)

    hasil = {
        "skema": SKEMA, "klien": klien, "periode": {
            "label": label_periode, "awal": awal.isoformat(), "akhir": akhir.isoformat(),
        },
        "jumlah_entri": b["jumlah_entri"], "total_jam": b["total_jam"],
        "jam_per_proyek": b["per_proyek"], "entri_tanpa_jam": b["entri_tanpa_jam"],
        "selesai": [e["pekerjaan"] for e in b["selesai"]],
        "berjalan": [e["pekerjaan"] for e in b["berjalan"]],
        "terkendala": [e["pekerjaan"] for e in b["terkendala"]],
        "kendala": b["kendala"], "butuh_dari_klien": b["butuh_dari_klien"],
        "rencana_berikutnya": b["rencana"], "ringkasan": b["ringkasan"],
        "teks_email": teks_email, "teks_wa": teks_wa, "markdown": markdown,
        "catatan": catatan, "peringatan": peringatan,
        "catatan_internal": "Draf ini untuk ditinjau KONSULTAN sebelum dikirim ke klien -- "
                             "skill ini tidak pernah mengirim apa pun secara otomatis.",
    }

    if args.json:
        print(json.dumps(hasil, ensure_ascii=False, indent=2, default=str))
    else:
        print("=== VERSI EMAIL ===\n")
        print(teks_email)
        print("\n=== VERSI WA/TELEGRAM ===\n")
        print(teks_wa)
        print("\n=== VERSI MARKDOWN (dokumen) ===\n")
        print(markdown)
        if catatan:
            print("\n--- CATATAN ---")
            for c in catatan:
                print("- " + c)
    if peringatan:
        print("\n--- PERINGATAN: pola mirip data pribadi/rahasia (lihat SKILL.md) ---", file=sys.stderr)
        for p in peringatan:
            print("PERINGATAN: " + p, file=sys.stderr)
        return 3
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser():
    ap = argparse.ArgumentParser(prog="laporan_klien.py", description=__doc__.splitlines()[0])
    ap.add_argument("--file", help="Path file log CSV (default: log-kerja-klien.csv atau "
                                     "ENV KOMUNITECH_LAPORAN_KLIEN_FILE)")
    sub = ap.add_subparsers(dest="perintah", required=True)

    p_init = sub.add_parser("init", help="Buat file log kosong")
    p_init.add_argument("--paksa", action="store_true", help="Timpa file yang sudah ada")
    p_init.add_argument("--json", action="store_true")
    p_init.set_defaults(func=cmd_init)

    p_catat = sub.add_parser("catat", help="Catat satu pekerjaan")
    p_catat.add_argument("--klien", required=True)
    p_catat.add_argument("--proyek", required=True)
    p_catat.add_argument("--pekerjaan", required=True)
    p_catat.add_argument("--tanggal", help="YYYY-MM-DD, 'hari-ini' (default), atau 'kemarin'")
    p_catat.add_argument("--jam", help="Jam kerja, mis. 2 atau 2,5 (opsional)")
    p_catat.add_argument("--status", default="berjalan",
                          help="selesai | berjalan (default) | terkendala")
    p_catat.add_argument("--kendala", default="", help="Hambatan di pihak konsultan (opsional)")
    p_catat.add_argument("--butuh-klien", dest="butuh_klien", default="",
                          help="Yang perlu diberikan/diputuskan klien (opsional)")
    p_catat.add_argument("--json", action="store_true")
    p_catat.set_defaults(func=cmd_catat)

    p_daftar = sub.add_parser("daftar-klien", help="Lihat daftar klien yang tercatat")
    p_daftar.add_argument("--json", action="store_true")
    p_daftar.set_defaults(func=cmd_daftar_klien)

    p_lap = sub.add_parser("laporan", help="Susun draf laporan progres satu klien")
    p_lap.add_argument("--klien", required=True)
    p_lap.add_argument("--periode", default="minggu-ini",
                        help="mingguan/bulanan, minggu-ini (default)/minggu-lalu/bulan-ini/bulan-lalu")
    p_lap.add_argument("--dari", help="Tanggal awal kustom YYYY-MM-DD (butuh --sampai)")
    p_lap.add_argument("--sampai", help="Tanggal akhir kustom YYYY-MM-DD (butuh --dari)")
    p_lap.add_argument("--tanggal-acuan", dest="tanggal_acuan",
                        help="Anggap hari ini = tanggal ini (default: hari ini sungguhan; "
                             "berguna untuk menguji jadwal Jumat)")
    p_lap.add_argument("--rencana", action="append",
                        help="Satu butir rencana berikutnya (bisa diulang). Tanpa ini, rencana "
                             "diturunkan dari pekerjaan berstatus 'berjalan'.")
    p_lap.add_argument("--json", action="store_true")
    p_lap.set_defaults(func=cmd_laporan)

    return ap


def main(argv=None):
    ap = build_parser()
    args = ap.parse_args(argv)
    try:
        return args.func(args) or 0
    except Gagal as e:
        print(f"Error: {e.pesan}", file=sys.stderr)
        return 1
    except (OSError, UnicodeDecodeError) as e:
        print(f"Error file: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
