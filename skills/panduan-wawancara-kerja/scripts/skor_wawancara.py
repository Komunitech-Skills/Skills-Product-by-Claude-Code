#!/usr/bin/env python3
"""Hitung skor wawancara beberapa kandidat dari beberapa pewawancara, dan bagi waktu wawancara.

Pemakaian (Windows: ganti python3 dengan python atau py):
  python3 scripts/skor_wawancara.py data.json                     (ringkasan teks)
  python3 scripts/skor_wawancara.py data.json --format json       (untuk diproses lebih lanjut)
  python3 scripts/skor_wawancara.py --alur 45 --kompetensi 5      (bagi waktu wawancara)

Format data.json: lihat references/format-skor.md dan templates/skor-contoh.json.
Hanya Python standar. Tidak memakai jaringan, tidak menulis berkas, tidak mengubah masukan.

Aturan hitung (persis, tanpa pembulatan selera):
  - Skor valid: angka 1 sampai 5 (koma desimal "4,5" diterima). Kosong dilewati; di luar 1-5 atau bukan angka
    diabaikan dan dilaporkan sebagai peringatan.
  - Rata-rata per kompetensi = rata-rata skor valid dari semua pewawancara.
  - Total = jumlah (rata-rata kompetensi x bobot) / jumlah bobot, memakai rata-rata TIDAK dibulatkan;
    dibulatkan SEKALI ke 2 desimal (setengah ke atas). Bobot yang jumlahnya bukan 100 dinormalkan.
  - Selisih antar pewawancara pada satu kompetensi (skor tertinggi dikurangi terendah) lebih dari 1,5 poin
    ditandai "perlu dibahas".
  - Kandidat yang punya skor kosong/diabaikan/belum lengkap: "Belum bisa disimpulkan" (tanpa rekomendasi, tanpa peringkat).
  - Kompetensi terkuat/terlemah yang seri atau sedang diperselisihkan tidak dipilih ("seri - putuskan setelah pembahasan").
"""
import argparse
import json
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from fractions import Fraction
from pathlib import Path

MAKS_BYTE = 2_000_000
BATAS_SELISIH = Fraction(3, 2)        # lebih dari 1,5 poin = perlu dibahas
BATAS_LANJUT = Fraction(7, 2)         # total >= 3,5 = disarankan lanjut
BATAS_CADANGAN = Fraction(11, 4)      # total >= 2,75 = pertimbangkan (cadangan)
LANTAI_KOMPETENSI = Fraction(5, 2)    # rata-rata kompetensi < 2,5 = di bawah standar
LANTAI_KRITIS = Fraction(3)           # kompetensi kritis < 3,0 = di bawah standar
VERSI = "1.0.3"
KOSONG = {"", "-", "–", "—", "n/a", "na", "null", "none", "belum", "kosong", "tidak ada"}

S_LANJUT = "Disarankan lanjut"
S_PERTIMBANGKAN = "Pertimbangkan (cadangan)"
S_BELUM_SESUAI = "Belum sesuai saat ini"
S_BELUM_SIMPULAN = "Belum bisa disimpulkan"
S_BELUM_DINILAI = "Belum dinilai"


class Galat(Exception):
    """Kesalahan masukan yang harus diperbaiki pengguna (pesan dalam Bahasa Indonesia)."""


# ---------- util angka ----------
def rapikan(s):
    return " ".join(s.split()) if isinstance(s, str) else ""


def kunci(s):
    return rapikan(s).casefold()


def ke_angka(nilai, persen=False):
    """Ubah ke Fraction. Lempar ValueError bila bukan angka hingga (bool, NaN, tak hingga ditolak)."""
    if nilai is None or isinstance(nilai, bool):
        raise ValueError("bukan angka")
    if isinstance(nilai, (int, float)):
        teks = repr(nilai)
    elif isinstance(nilai, str):
        teks = nilai.strip().replace(",", ".")
        if persen and teks.endswith("%"):
            teks = teks[:-1].strip()
    else:
        raise ValueError("bukan angka")
    try:
        d = Decimal(teks)
    except InvalidOperation:
        raise ValueError("bukan angka") from None
    if not d.is_finite() or (d != 0 and abs(d.adjusted()) > 30):
        raise ValueError("bukan angka")
    return Fraction(d)


def bulat2(fr):
    d = Decimal(fr.numerator) / Decimal(fr.denominator)
    return d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def f2(fr):
    """Dua desimal, koma Indonesia: 3,85."""
    return str(bulat2(fr)).replace(".", ",")


def fp(fr):
    """Desimal secukupnya (maks. 2), koma Indonesia: 2 atau 1,5 atau 3,25."""
    s = str(bulat2(fr))
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s.replace(".", ",")


def angka_json(fr):
    return float(bulat2(fr))


# ---------- baca & validasi masukan ----------
def baca_kompetensi(daftar, peringatan):
    if not isinstance(daftar, list) or not daftar:
        raise Galat("'kompetensi' harus berupa daftar berisi minimal satu kompetensi (nama dan bobot).")
    hasil, terlihat = [], set()
    for i, k in enumerate(daftar, 1):
        if isinstance(k, str):
            k = {"nama": k}
        if not isinstance(k, dict):
            raise Galat(f"Kompetensi nomor {i} harus berupa objek dengan 'nama' dan 'bobot'.")
        nama = rapikan(k.get("nama"))
        if not nama:
            raise Galat(f"Kompetensi nomor {i} belum punya 'nama'.")
        if kunci(nama) in terlihat:
            raise Galat(f"Nama kompetensi '{nama}' muncul dua kali. Beri nama yang berbeda.")
        terlihat.add(kunci(nama))
        bobot = None
        if k.get("bobot") not in (None, ""):
            try:
                bobot = ke_angka(k["bobot"], persen=True)
            except ValueError:
                raise Galat(f"Bobot kompetensi '{nama}' bukan angka: {k['bobot']!r}.") from None
            if bobot <= 0:
                raise Galat(f"Bobot kompetensi '{nama}' harus lebih dari 0.")
        kritis = k.get("kritis")
        kritis = kritis is True or (isinstance(kritis, str) and kritis.strip().casefold() in {"ya", "true", "1"})
        hasil.append({"nama": nama, "bobot": bobot, "kritis": kritis})
    tanpa = [x["nama"] for x in hasil if x["bobot"] is None]
    if len(tanpa) == len(hasil):
        for x in hasil:
            x["bobot"] = Fraction(1)
        peringatan.append("Bobot tidak diisi: semua kompetensi dianggap sama penting.")
    elif tanpa:
        raise Galat("Bobot belum lengkap untuk: " + ", ".join(tanpa) + ". Isi bobot semua kompetensi atau kosongkan semuanya.")
    else:
        jumlah = sum(x["bobot"] for x in hasil)
        if jumlah != 100:
            peringatan.append(f"Jumlah bobot {fp(jumlah)}, bukan 100. Bobot dinormalkan: tiap bobot dibagi {fp(jumlah)} lalu dikali 100%.")
    jumlah = sum(x["bobot"] for x in hasil)
    for x in hasil:
        x["persen"] = x["bobot"] / jumlah * 100
    return hasil


def baca_skor_kandidat(label, skor, komp_index, peringatan):
    """Kembalikan ({pewawancara: {nama_kompetensi: Fraction}}, [skor yang diabaikan]) untuk satu kandidat."""
    if skor in (None, {}):
        return {}, []
    if not isinstance(skor, dict):
        raise Galat(f"'skor' kandidat {label} harus berupa objek, bukan {type(skor).__name__}.")
    nilai_dict = [isinstance(v, dict) for v in skor.values()]
    if all(nilai_dict):
        per_pw = skor
    elif not any(nilai_dict):
        per_pw = {"Pewawancara 1": skor}
    else:
        raise Galat(f"'skor' kandidat {label} campur: sebagian per pewawancara, sebagian langsung per kompetensi. Pilih satu bentuk.")
    hasil, diabaikan = {}, []
    for pw_raw, isi in per_pw.items():
        pw = rapikan(str(pw_raw)) or "Pewawancara"
        hasil.setdefault(pw, {})
        for nama_raw, nilai in isi.items():
            k = kunci(str(nama_raw))
            if k not in komp_index:
                peringatan.append(f"{label} / {pw}: kompetensi '{rapikan(str(nama_raw))}' tidak dikenal, diabaikan (cek ejaan).")
                diabaikan.append(f"{pw} / '{rapikan(str(nama_raw))}' (nama kompetensi tidak dikenal)")
                continue
            nama = komp_index[k]
            if nilai is None or (isinstance(nilai, str) and kunci(nilai) in KOSONG):
                peringatan.append(f"{label} / {pw} / {nama}: skor kosong, dilewati.")
                diabaikan.append(f"{pw} / {nama} (kosong)")
                continue
            try:
                angka = ke_angka(nilai)
            except ValueError:
                peringatan.append(f"{label} / {pw} / {nama}: skor {nilai!r} bukan angka, diabaikan.")
                diabaikan.append(f"{pw} / {nama} (bukan angka)")
                continue
            if not 1 <= angka <= 5:
                peringatan.append(f"{label} / {pw} / {nama}: skor {rapikan(str(nilai))} di luar 1-5, diabaikan.")
                diabaikan.append(f"{pw} / {nama} (di luar 1-5)")
                continue
            hasil[pw][nama] = angka
    return hasil, diabaikan


def baca_data(data, batas):
    if not isinstance(data, dict):
        raise Galat("Isi berkas harus berupa objek JSON dengan 'kompetensi' dan 'kandidat'.")
    peringatan = []
    komp = baca_kompetensi(data.get("kompetensi"), peringatan)
    komp_index = {kunci(k["nama"]): k["nama"] for k in komp}
    calon = data.get("kandidat")
    if not isinstance(calon, list) or not calon:
        raise Galat("'kandidat' harus berupa daftar berisi minimal satu kandidat.")
    kandidat, kode_terlihat, pewawancara = [], set(), []
    for i, c in enumerate(calon, 1):
        if not isinstance(c, dict):
            raise Galat(f"Kandidat nomor {i} harus berupa objek dengan 'kode', 'nama', dan 'skor'.")
        kode = rapikan(c.get("kode")) or f"C{i}"
        if kunci(kode) in kode_terlihat:
            raise Galat(f"Kode kandidat '{kode}' dipakai dua kali.")
        kode_terlihat.add(kunci(kode))
        nama = rapikan(c.get("nama"))
        label = f"{kode} {nama}".strip()
        skor, diabaikan = baca_skor_kandidat(label, c.get("skor"), komp_index, peringatan)
        for pw in skor:
            if pw not in pewawancara:
                pewawancara.append(pw)
        kandidat.append({"kode": kode, "nama": nama, "label": label, "skor": skor, "diabaikan": diabaikan})
    return {"posisi": rapikan(data.get("posisi")) or None, "kompetensi": komp, "kandidat": kandidat,
            "pewawancara": pewawancara, "peringatan": peringatan, "batas": batas}


# ---------- hitung ----------
def ekstrem(ada, terbesar):
    """Kompetensi terkuat/terlemah. Bila seri, atau kompetensinya sedang diperselisihkan, jangan memilih satu."""
    if not ada:
        return None
    nilai = max(b["rata"] for b in ada) if terbesar else min(b["rata"] for b in ada)
    kena = [b for b in ada if b["rata"] == nilai]
    return {"nama": [b["nama"] for b in kena], "rata": nilai, "seri": len(kena) > 1,
            "tunda": len(kena) > 1 or kena[0]["dibahas"]}


def kalimat_ekstrem(label, e):
    rinci = ", ".join(e["nama"])
    if e["seri"]:
        return f"{label}: seri \u2014 putuskan setelah pembahasan ({rinci}, {f2(e['rata'])})"
    if e["tunda"]:
        return f"{label}: {rinci} ({f2(e['rata'])}) sedang diperselisihkan \u2014 putuskan setelah pembahasan"
    return f"{label} {rinci} ({f2(e['rata'])})"


def hitung_kandidat(k, komp, batas):
    total_bobot = sum(x["bobot"] for x in komp)
    baris, bobot_terisi, jumlah_tertimbang = [], Fraction(0), Fraction(0)
    for x in komp:
        per_pw = {pw: s[x["nama"]] for pw, s in k["skor"].items() if x["nama"] in s}
        rata = sum(per_pw.values()) / len(per_pw) if per_pw else None
        selisih = (max(per_pw.values()) - min(per_pw.values())) if len(per_pw) >= 2 else None
        if rata is not None:
            bobot_terisi += x["bobot"]
            jumlah_tertimbang += rata * x["bobot"]
        baris.append({"nama": x["nama"], "kritis": x["kritis"], "bobot": x["bobot"], "skor": per_pw, "rata": rata,
                      "selisih": selisih, "dibahas": selisih is not None and selisih > batas["selisih"]})
    ada = [b for b in baris if b["rata"] is not None]
    kosong = [b["nama"] for b in baris if b["rata"] is None]
    total = jumlah_tertimbang / bobot_terisi if bobot_terisi else None
    lemah = [b for b in ada if Fraction(bulat2(b["rata"])) < (LANTAI_KRITIS if b["kritis"] else batas["lantai"])]
    lengkap = not kosong
    diabaikan = k["diabaikan"]
    siap = lengkap and not diabaikan
    dibahas = [b for b in baris if b["dibahas"]]
    alasan = []
    lengkapi = [f"{n} (belum dinilai)" for n in kosong] + diabaikan
    if total is None:
        saran = S_BELUM_DINILAI
        alasan.append("belum ada skor yang valid")
    elif not siap:
        saran = S_BELUM_SIMPULAN
    else:
        t2 = Fraction(bulat2(total))
        if t2 >= batas["lanjut"] and not lemah:
            saran = S_LANJUT
        elif t2 >= batas["cadangan"]:
            saran = S_PERTIMBANGKAN
            if lemah:
                alasan.append("ada kompetensi di bawah standar: " + ", ".join(f"{b['nama']} {f2(b['rata'])}" for b in lemah))
        else:
            saran = S_BELUM_SESUAI
    if dibahas:
        alasan.append("bahas dulu perbedaan penilaian antar pewawancara: " + ", ".join(b["nama"] for b in dibahas))
    saran_teks = saran
    if total is not None and not siap:
        saran_teks = f"{saran} \u2014 lengkapi skor: " + "; ".join(lengkapi)
    elif total is None and diabaikan:
        alasan.append("lengkapi skor: " + "; ".join(lengkapi))
    return {"kode": k["kode"], "nama": k["nama"], "label": k["label"], "kompetensi": baris, "total": total,
            "lengkap": lengkap, "cakupan": bobot_terisi / total_bobot, "kosong": kosong, "lemah": lemah,
            "dibahas": dibahas, "saran": saran, "saran_teks": saran_teks, "alasan": alasan,
            "siap": siap, "diabaikan": diabaikan, "lengkapi": lengkapi,
            "terkuat": ekstrem(ada, True), "terlemah": ekstrem(ada, False),
            "peringkat": None, "seri": False}


def beri_peringkat(hasil_kandidat, komp):
    """Peringkat memakai total yang sudah dibulatkan; seri dipecah dengan skor kompetensi berbobot terbesar."""
    dinilai = [h for h in hasil_kandidat if h["total"] is not None]
    dasar = [h for h in dinilai if h["siap"]]
    sementara = not dasar
    if sementara:
        dasar = dinilai
    urutan_bobot = sorted(range(len(komp)), key=lambda i: (-komp[i]["bobot"], i))

    def kunci_urut(h):
        rata2 = tuple(bulat2(h["kompetensi"][i]["rata"]) if h["kompetensi"][i]["rata"] is not None else Decimal(0)
                      for i in urutan_bobot)
        return (-bulat2(h["total"]),) + tuple(-r for r in rata2)

    dasar.sort(key=kunci_urut)
    i = 0
    while i < len(dasar):
        j = i
        while j < len(dasar) and bulat2(dasar[j]["total"]) == bulat2(dasar[i]["total"]):
            j += 1
        grup = dasar[i:j]
        sengketa = len(grup) > 1 and any(h["dibahas"] for h in grup)
        sebelumnya, posisi = None, i + 1
        for m, h in enumerate(grup):
            kk = kunci_urut(h)
            if sengketa:
                posisi = i + 1            # total sama dan ada penilaian yang diperselisihkan: jangan dipisahkan
            elif kk != sebelumnya:
                posisi = i + m + 1
            h["peringkat"] = posisi
            sebelumnya = kk
        i = j
    jumlah = {}
    for h in dasar:
        jumlah[h["peringkat"]] = jumlah.get(h["peringkat"], 0) + 1
    for h in dasar:
        h["seri"] = jumlah[h["peringkat"]] > 1
        if h["seri"]:
            h["alasan"].append("seri dengan kandidat lain \u2014 putuskan setelah pembahasan")
    return dasar, sementara


def hitung(data, batas_selisih=BATAS_SELISIH, batas_lanjut=BATAS_LANJUT, batas_cadangan=BATAS_CADANGAN,
           lantai=LANTAI_KOMPETENSI):
    batas = {"selisih": batas_selisih, "lanjut": batas_lanjut, "cadangan": batas_cadangan, "lantai": lantai}
    d = baca_data(data, batas)
    hasil = [hitung_kandidat(k, d["kompetensi"], batas) for k in d["kandidat"]]
    dasar, sementara = beri_peringkat(hasil, d["kompetensi"])
    tunggal = len(d["kandidat"]) == 1
    if tunggal:
        for h in hasil:
            h["peringkat"], h["seri"] = None, False
    urut = sorted(dasar, key=lambda h: h["peringkat"]) if not tunggal else []
    dipakai = {id(h) for h in urut}
    sisa = [h for h in hasil if id(h) not in dipakai]
    return {"posisi": d["posisi"], "kompetensi": d["kompetensi"], "pewawancara": d["pewawancara"],
            "kandidat": urut + sisa, "peringatan": d["peringatan"], "peringkat_sementara": sementara and bool(dasar),
            "tunggal": tunggal, "batas": batas}


# ---------- keluaran ----------
def teks_hasil(h):
    b = h["batas"]
    out = ["HASIL SKOR WAWANCARA"]
    kepala = [f"Posisi: {h['posisi']}"] if h["posisi"] else []
    kepala += [f"Kandidat: {len(h['kandidat'])}", f"Pewawancara: {len(h['pewawancara'])}"
               + (f" ({', '.join(h['pewawancara'])})" if h["pewawancara"] else "")]
    out.append(" | ".join(kepala))
    out.append("Bobot: " + "; ".join(f"{x['nama']} {fp(x['persen'])}%" + (" (kritis)" if x["kritis"] else "") for x in h["kompetensi"]))
    if h["peringatan"]:
        out += ["", "PERINGATAN"] + [f"- {p}" for p in h["peringatan"]]
    if h["tunggal"]:
        k = h["kandidat"][0]
        out += ["", "PERINGKAT", "- Hanya satu kandidat: tidak ada peringkat. Dinilai terhadap standar (3 = memenuhi standar), bukan terhadap kandidat lain.",
                f"- {k['label']}: " + (f"total {f2(k['total'])} dari 5. {k['saran_teks']}" if k["total"] is not None else "belum dinilai")]
    else:
        out += ["", "PERINGKAT" + (" (SEMENTARA: belum ada kandidat yang skornya lengkap dan terkonfirmasi)" if h["peringkat_sementara"] else "")]
        for k in h["kandidat"]:
            if k["total"] is None:
                out.append(f"- {k['label']}: belum dinilai.")
            elif k["peringkat"] is None:
                out.append(f"- Belum diperingkat: {k['label']}: total sementara {f2(k['total'])} dari 5. {k['saran_teks']}")
            else:
                out.append(f"{k['peringkat']}. {k['label']}: total {f2(k['total'])} dari 5. {k['saran']}" + (". Seri \u2014 putuskan setelah pembahasan" if k["seri"] else ""))
    out += ["", "RATA-RATA PER KOMPETENSI (1-5)"]
    for k in h["kandidat"]:
        bagian = []
        for x in k["kompetensi"]:
            bagian.append(f"{x['nama']} {f2(x['rata']) if x['rata'] is not None else 'belum dinilai'}"
                          + (" (perlu dibahas)" if x["dibahas"] else ""))
        out.append(f"- {k['label']}: " + "; ".join(bagian))
    dibahas = [(k, x) for k in h["kandidat"] for x in k["dibahas"]]
    out += ["", f"PERLU DIBAHAS (selisih antar pewawancara lebih dari {fp(b['selisih'])} poin)"]
    if dibahas:
        for k, x in dibahas:
            rinci = ", ".join(f"{pw} {fp(s)}" for pw, s in x["skor"].items())
            out.append(f"- {k['label']}, {x['nama']}: {rinci} (selisih {fp(x['selisih'])})")
    else:
        out.append("- Tidak ada." if len(h["pewawancara"]) >= 2 else "- Tidak bisa dicek: hanya satu pewawancara.")
    out += ["", "RINGKASAN KEPUTUSAN"]
    for k in h["kandidat"]:
        if k["total"] is None:
            out.append(f"- {k['label']}: belum ada skor valid.")
            continue
        kalimat = f"- {k['label']}: total {f2(k['total'])} dari 5"
        if k["terkuat"] and k["terlemah"] and k["terkuat"]["rata"] != k["terlemah"]["rata"]:
            kalimat += "; " + kalimat_ekstrem("terkuat", k["terkuat"]) + "; " + kalimat_ekstrem("terlemah", k["terlemah"])
        kalimat += f". Saran: {k['saran_teks']}"
        if k["alasan"]:
            kalimat += "; " + "; ".join(k["alasan"])
        out.append(kalimat + ".")
    out += ["", f"Aturan saran: lanjut bila total >= {fp(b['lanjut'])} dan tidak ada kompetensi di bawah {fp(b['lantai'])} "
                f"(kompetensi kritis: di bawah {fp(LANTAI_KRITIS)}); cadangan bila total >= {fp(b['cadangan'])}. "
                "Saran adalah alat bantu; keputusan tetap di pemilik/tim."]
    return "\n".join(out)


def ekstrem_json(e):
    if e is None:
        return None
    return {"kompetensi": e["nama"], "rata_rata": angka_json(e["rata"]), "seri": e["seri"],
            "putuskan_setelah_pembahasan": e["tunda"]}


def json_hasil(h):
    return {
        "posisi": h["posisi"], "pewawancara": h["pewawancara"], "peringkat_sementara": h["peringkat_sementara"],
        "kandidat_tunggal": h["tunggal"], "peringatan": h["peringatan"],
        "kompetensi": [{"nama": x["nama"], "bobot_persen": angka_json(x["persen"]), "kritis": x["kritis"]} for x in h["kompetensi"]],
        "kandidat": [{
            "kode": k["kode"], "nama": k["nama"], "peringkat": k["peringkat"], "seri": k["seri"],
            "total": angka_json(k["total"]) if k["total"] is not None else None, "lengkap": k["lengkap"],
            "cakupan_persen": angka_json(k["cakupan"] * 100), "saran": k["saran"], "alasan": k["alasan"],
            "siap_diputuskan": k["siap"], "lengkapi_skor": k["lengkapi"],
            "belum_dinilai": k["kosong"],
            "terkuat": ekstrem_json(k["terkuat"]), "terlemah": ekstrem_json(k["terlemah"]),
            "kompetensi": [{"nama": x["nama"], "rata_rata": angka_json(x["rata"]) if x["rata"] is not None else None,
                            "skor": {pw: angka_json(s) for pw, s in x["skor"].items()},
                            "selisih": angka_json(x["selisih"]) if x["selisih"] is not None else None,
                            "perlu_dibahas": x["dibahas"]} for x in k["kompetensi"]],
        } for k in h["kandidat"]],
    }


# ---------- bagi waktu ----------
def bulat_int(x):
    return int(Decimal(x).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def bagi_waktu(durasi, n_kompetensi, tes=None):
    """Kembalikan (daftar (bagian, menit), peringatan). Jumlah menit selalu sama dengan durasi."""
    if not 15 <= durasi <= 240:
        raise Galat("Durasi wawancara harus antara 15 dan 240 menit.")
    if not 1 <= n_kompetensi <= 8:
        raise Galat("Jumlah kompetensi harus antara 1 dan 8 (disarankan 4-6).")
    pembuka = max(3, bulat_int(Decimal(durasi) * Decimal("0.10")))
    tanya = max(3, bulat_int(Decimal(durasi) * Decimal("0.10")))
    penutup = max(2, bulat_int(Decimal(durasi) * Decimal("0.05")))
    if tes is None:
        tes = min(20, bulat_int(Decimal(durasi) * Decimal("0.20")))
    if tes < 0 or tes > durasi // 2:
        raise Galat("Waktu tes praktik harus 0 sampai setengah durasi wawancara.")
    sisa = durasi - (pembuka + tanya + penutup + tes)
    peringatan = []
    if sisa < n_kompetensi:
        raise Galat("Durasi terlalu singkat untuk jumlah kompetensi ini. Tambah durasi atau kurangi kompetensi.")
    dasar, lebih = divmod(sisa, n_kompetensi)
    if dasar < 3:
        peringatan.append(f"Waktu per kompetensi kurang dari 3 menit. Kurangi kompetensi menjadi {max(1, sisa // 3)} atau tambah durasi.")
    daftar = [("Pembuka dan perkenalan", pembuka)]
    if tes:
        daftar.append(("Tes praktik", tes))
    for i in range(n_kompetensi):
        daftar.append((f"Kompetensi {i + 1}", dasar + (1 if i < lebih else 0)))
    daftar += [("Pertanyaan dari kandidat", tanya), ("Penutup", penutup)]
    assert sum(m for _, m in daftar) == durasi
    return daftar, peringatan


def teks_waktu(daftar, peringatan, durasi):
    out = [f"ALUR WAKTU WAWANCARA ({durasi} menit)"]
    out += [f"- {bagian}: {menit} menit" for bagian, menit in daftar]
    out.append(f"Total: {sum(m for _, m in daftar)} menit")
    out += [f"Peringatan: {p}" for p in peringatan]
    return "\n".join(out)


# ---------- CLI ----------
def angka_arg(teks, nama, kecil=1, besar=5):
    try:
        v = ke_angka(teks)
    except ValueError:
        raise Galat(f"{nama} harus berupa angka, bukan {teks!r}.") from None
    if not kecil <= v <= besar:
        raise Galat(f"{nama} harus antara {kecil} dan {besar}.")
    return v


def main(argv=None):
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description=f"Hitung skor wawancara atau bagi waktu wawancara (v{VERSI}).")
    ap.add_argument("berkas", nargs="?", help="berkas JSON berisi kompetensi, kandidat, dan skor")
    ap.add_argument("--format", choices=["ringkas", "json"], default="ringkas")
    ap.add_argument("--batas-selisih", default="1.5", help="selisih antar pewawancara yang ditandai (default 1.5)")
    ap.add_argument("--batas-lanjut", default="3.5", help="total minimal untuk 'disarankan lanjut' (default 3.5)")
    ap.add_argument("--batas-cadangan", default="2.75", help="total minimal untuk 'cadangan' (default 2.75)")
    ap.add_argument("--batas-bawah", default="2.5", help="rata-rata kompetensi di bawah ini = di bawah standar (default 2.5)")
    ap.add_argument("--alur", type=int, help="durasi wawancara (menit) untuk dibagi per bagian")
    ap.add_argument("--kompetensi", type=int, help="jumlah kompetensi (untuk --alur)")
    ap.add_argument("--tes", type=int, help="menit tes praktik (untuk --alur; 0 = tanpa tes)")
    args = ap.parse_args(argv)
    try:
        if args.alur is not None:
            if args.berkas or args.kompetensi is None:
                raise Galat("Pakai: --alur DURASI --kompetensi JUMLAH [--tes MENIT] (tanpa berkas).")
            daftar, peringatan = bagi_waktu(args.alur, args.kompetensi, args.tes)
            print(teks_waktu(daftar, peringatan, args.alur))
            return 0
        if not args.berkas:
            raise Galat("Beri nama berkas JSON, atau pakai --alur. Lihat references/format-skor.md.")
        jalur = Path(args.berkas)
        if not jalur.is_file():
            raise Galat(f"Berkas '{args.berkas}' tidak ditemukan.")
        if jalur.stat().st_size > MAKS_BYTE:
            raise Galat("Berkas terlalu besar (lebih dari 2 MB).")
        try:
            data = json.loads(jalur.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError as e:
            raise Galat(f"Berkas bukan JSON yang valid (baris {e.lineno}, kolom {e.colno}): {e.msg}.") from None
        except UnicodeDecodeError:
            raise Galat("Berkas harus berupa teks UTF-8.") from None
        h = hitung(data, angka_arg(args.batas_selisih, "--batas-selisih", 0, 4), angka_arg(args.batas_lanjut, "--batas-lanjut"),
                   angka_arg(args.batas_cadangan, "--batas-cadangan"), angka_arg(args.batas_bawah, "--batas-bawah"))
        print(json.dumps(json_hasil(h), ensure_ascii=False, indent=2) if args.format == "json" else teks_hasil(h))
        return 0
    except Galat as e:
        print(f"Galat: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
