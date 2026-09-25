#!/usr/bin/env python3
"""Alat bantu skill pesan-prospek-wa: memeriksa draf pesan pembuka WhatsApp
dan membangun tautan wa.me dengan normalisasi nomor Indonesia.

Hanya memakai pustaka standar Python (3.7+). Tidak ada akses jaringan.
Jalankan dengan `python3` (Windows: `python` atau `py`).

Contoh:
  # Periksa draf pesan (jam kirim opsional, format 24 jam)
  python3 cek_pesan.py cek --pesan "Selamat siang Pak Andi, perkenalkan saya Rian dari Toko Berkah..." --jam-kirim 19:30

  # Periksa dari file teks
  python3 cek_pesan.py cek --file draf_pesan.txt

  # Bangun tautan wa.me dari nomor + pesan
  python3 cek_pesan.py wa --nomor "0812-3456-7890" --pesan "Selamat siang Pak Andi, ..."

Catatan: pemeriksaan kata pemicu spam & "asal kontak" bersifat heuristik
(pencocokan kata kunci) — bukan pengecekan makna. Selalu baca ulang pesan
sendiri sebelum mengirim; skrip ini alat bantu, bukan pengganti penilaian.
"""
import argparse
import re
import sys
from urllib.parse import quote

# ---------------------------------------------------------------------------
# Batas & daftar kata kunci
# ---------------------------------------------------------------------------

BATAS_KARAKTER_DISARANKAN = 500   # kira-kira muat 1 layar HP tanpa banyak scroll
BATAS_KARAKTER_MAKS = 700
BATAS_KATA_PER_KALIMAT = 25       # kalimat lebih panjang dari ini terasa berat dibaca di HP
JAM_MULAI_WAJAR = 8               # 08.00
JAM_SELESAI_WAJAR = 20            # 20.00 (batas akhir, > jam ini dianggap terlalu malam)

# Singkatan umum yang boleh huruf besar semua tanpa dianggap "teriak"
SINGKATAN_AMAN = {
    "WA", "CS", "PT", "CV", "UD", "QRIS", "COD", "ID", "RT", "RW", "KTP",
    "NPWP", "SD", "SMP", "SMA", "SMK", "UMKM", "BPOM", "IG", "FB", "TT",
    "STOP", "OK", "SIM", "AC", "TV",
}

# Frasa/kata pemicu kesan spam atau berlebihan (huruf kecil, dicocokkan case-insensitive)
KATA_PEMICU_SPAM = [
    "gratis!!!", "gratis!!", "100% dijamin", "dijamin 100%", "auto cuan",
    "buruan sebelum kehabisan", "jangan sampai ketinggalan", "no php",
    "no tipu", "bukan tipu", "join sekarang juga", "klik link ini sekarang",
    "limited banget", "harga gila", "diskon gila", "promo gila",
    "cepetan daftar", "auto kaya", "modal receh untung gede",
    "tanpa modal", "kerja santai gaji besar", "wa admin sekarang juga",
]

# Kata kunci yang menandai pesan MENYEBUT asal kontak (heuristik)
KATA_KUNCI_ASAL_KONTAK = [
    "dapat nomor", "dapat kontak", "dapat kontaknya", "dapat nomornya",
    "nomor bapak/ibu saya dapat", "kontak ini saya dapat", "dari rekomendasi",
    "direkomendasikan oleh", "referensi dari", "dikasih tahu oleh",
    "dari teman", "dari kenalan", "dari grup", "dari pameran",
    "dari google maps", "dari instagram", "dari ig", "dari facebook",
    "dari marketplace", "lihat dari", "melihat profil", "melihat usaha bapak/ibu",
    "kontak dari", "nomor dari", "dari bapak", "dari ibu", "izin menghubungi",
]

# Kata kunci yang menandai ada opsi keluar / berhenti yang sopan (heuristik)
KATA_KUNCI_OPSI_KELUAR = [
    "boleh diabaikan", "maaf mengganggu", "balas stop", "balas berhenti",
    "mohon maaf bila", "kalau tidak berkenan", "kalau belum berminat",
    "jika tidak relevan", "tidak perlu dibalas", "abaikan saja pesan ini",
    "silakan abaikan", "boleh diabaikan bila", "maaf sebelumnya",
]


class InputSalah(Exception):
    pass


# ---------------------------------------------------------------------------
# Bagian: normalisasi nomor & tautan wa.me
# ---------------------------------------------------------------------------

def normalisasi_nomor_wa(nomor):
    """Ubah nomor HP Indonesia ke format 62xxxxxxxxxx (tanpa '+', tanpa spasi/strip)."""
    if nomor is None or not str(nomor).strip():
        raise InputSalah("nomor WhatsApp kosong")
    bersih = re.sub(r"[\s\-().]", "", str(nomor).strip())
    if bersih.startswith("+"):
        bersih = bersih[1:]
    if not re.fullmatch(r"\d{8,15}", bersih):
        raise InputSalah(
            f"nomor {nomor!r} tidak terlihat seperti nomor HP yang valid "
            "(harus angka, 8-15 digit setelah tanda dibuang)"
        )
    if bersih.startswith("0"):
        bersih = "62" + bersih[1:]
    elif bersih.startswith("8"):
        bersih = "62" + bersih
    elif not bersih.startswith("62"):
        raise InputSalah(
            f"nomor {nomor!r}: awali dengan 08xx, 8xx, atau 62xx (kode negara Indonesia)"
        )
    return bersih


def bangun_tautan_wa(nomor, pesan=""):
    nomor_bersih = normalisasi_nomor_wa(nomor)
    tautan = f"https://wa.me/{nomor_bersih}"
    if pesan and pesan.strip():
        tautan += f"?text={quote(pesan.strip())}"
    return tautan


# ---------------------------------------------------------------------------
# Bagian: pemeriksaan draf pesan
# ---------------------------------------------------------------------------

def pisah_kalimat(teks):
    potongan = re.split(r"(?<=[.!?])\s+", teks.strip())
    return [p.strip() for p in potongan if p.strip()]


def hitung_kata(teks):
    return len(re.findall(r"\S+", teks))


def cek_kalimat_panjang(teks):
    hasil = []
    for kalimat in pisah_kalimat(teks):
        n = hitung_kata(kalimat)
        if n > BATAS_KATA_PER_KALIMAT:
            cuplikan = kalimat if len(kalimat) <= 80 else kalimat[:77] + "..."
            hasil.append(f"{n} kata: \"{cuplikan}\"")
    return hasil


def cek_kapital_berlebihan(teks):
    kata_kapital = []
    for kata in re.findall(r"[A-Za-z]+", teks):
        if len(kata) >= 3 and kata.isupper() and kata.upper() not in SINGKATAN_AMAN:
            kata_kapital.append(kata)
    return kata_kapital


def cek_kata_pemicu_spam(teks):
    rendah = teks.lower()
    ditemukan = [frasa for frasa in KATA_PEMICU_SPAM if frasa in rendah]
    if re.search(r"[!?]{3,}", teks):
        ditemukan.append("tanda seru/tanya berulang (!!! atau ???)")
    return ditemukan


def hitung_link(teks):
    return len(re.findall(r"https?://\S+|www\.\S+", teks, flags=re.IGNORECASE))


def cek_kata_kunci(teks, daftar):
    rendah = teks.lower()
    return any(kunci in rendah for kunci in daftar)


def cek_jam_kirim(jam_teks):
    """jam_teks format 'HH:MM'. Return (jam_int, wajar_bool) atau None jika tidak diisi."""
    if not jam_teks:
        return None
    if not re.fullmatch(r"([01]?\d|2[0-3]):[0-5]\d", jam_teks.strip()):
        raise InputSalah(f"format --jam-kirim harus HH:MM (24 jam), diberi {jam_teks!r}")
    jam = int(jam_teks.split(":")[0])
    wajar = JAM_MULAI_WAJAR <= jam < JAM_SELESAI_WAJAR
    return jam, wajar


def periksa_pesan(teks, jam_kirim=None):
    if not teks or not teks.strip():
        raise InputSalah("pesan kosong")

    jumlah_karakter = len(teks.strip())
    jumlah_kata = hitung_kata(teks)
    jumlah_baris = len(teks.strip().splitlines())

    kalimat_panjang = cek_kalimat_panjang(teks)
    kata_kapital = cek_kapital_berlebihan(teks)
    pemicu_spam = cek_kata_pemicu_spam(teks)
    jumlah_link = hitung_link(teks)
    sebut_asal_kontak = cek_kata_kunci(teks, KATA_KUNCI_ASAL_KONTAK)
    ada_opsi_keluar = cek_kata_kunci(teks, KATA_KUNCI_OPSI_KELUAR)
    info_jam = cek_jam_kirim(jam_kirim)

    peringatan = []
    if jumlah_karakter > BATAS_KARAKTER_MAKS:
        peringatan.append(
            f"Pesan {jumlah_karakter} karakter — lebih dari {BATAS_KARAKTER_MAKS}, "
            "kemungkinan kepanjangan untuk pesan pembuka. Pertimbangkan versi 'singkat'."
        )
    elif jumlah_karakter > BATAS_KARAKTER_DISARANKAN:
        peringatan.append(
            f"Pesan {jumlah_karakter} karakter — di atas {BATAS_KARAKTER_DISARANKAN}, "
            "mungkin perlu scroll di layar HP. Masih boleh, tapi cek dulu."
        )
    if kalimat_panjang:
        peringatan.append(
            f"{len(kalimat_panjang)} kalimat lebih dari {BATAS_KATA_PER_KALIMAT} kata (berat dibaca di HP): "
            + "; ".join(kalimat_panjang)
        )
    if kata_kapital:
        peringatan.append(
            "Kata huruf kapital semua terdeteksi (bisa terkesan teriak/spam): "
            + ", ".join(sorted(set(kata_kapital)))
        )
    if pemicu_spam:
        peringatan.append(
            "Frasa berisiko terkesan spam/berlebihan terdeteksi: " + "; ".join(pemicu_spam)
        )
    if jumlah_link > 1:
        peringatan.append(f"Ada {jumlah_link} link — pesan pembuka sebaiknya maksimal 1 link (atau tanpa link).")
    if not sebut_asal_kontak:
        peringatan.append(
            "Tidak terdeteksi kalimat yang menyebutkan dari mana nomor/kontak didapat "
            "(referral, Google Maps, IG, grup, pameran, dll). Ini penting untuk pesan pertama "
            "agar tidak terkesan spam/penipuan — cek manual, heuristik ini bisa salah deteksi."
        )
    if not ada_opsi_keluar:
        peringatan.append(
            "Tidak terdeteksi opsi keluar yang sopan (mis. 'boleh diabaikan bila tidak relevan', "
            "'maaf mengganggu'). Cek manual, heuristik ini bisa salah deteksi."
        )
    if info_jam is not None:
        jam, wajar = info_jam
        if not wajar:
            peringatan.append(
                f"Jam kirim {jam_kirim} di luar rentang wajar {JAM_MULAI_WAJAR:02d}.00–{JAM_SELESAI_WAJAR:02d}.00 "
                "waktu setempat penerima — pertimbangkan menjadwalkan ulang."
            )

    return {
        "jumlah_karakter": jumlah_karakter,
        "jumlah_kata": jumlah_kata,
        "jumlah_baris": jumlah_baris,
        "jumlah_link": jumlah_link,
        "sebut_asal_kontak": sebut_asal_kontak,
        "ada_opsi_keluar": ada_opsi_keluar,
        "jam_kirim_wajar": info_jam[1] if info_jam is not None else None,
        "peringatan": peringatan,
    }


def cetak_hasil_periksa(hasil):
    print(f"Jumlah karakter : {hasil['jumlah_karakter']}")
    print(f"Jumlah kata     : {hasil['jumlah_kata']}")
    print(f"Jumlah baris    : {hasil['jumlah_baris']}")
    print(f"Jumlah link     : {hasil['jumlah_link']}")
    print(f"Sebut asal kontak terdeteksi : {'Ya' if hasil['sebut_asal_kontak'] else 'Tidak'}")
    print(f"Opsi keluar terdeteksi       : {'Ya' if hasil['ada_opsi_keluar'] else 'Tidak'}")
    if hasil["jam_kirim_wajar"] is not None:
        print(f"Jam kirim wajar (08.00-20.00) : {'Ya' if hasil['jam_kirim_wajar'] else 'Tidak'}")
    print()
    if hasil["peringatan"]:
        print(f"[PERIKSA DULU] {len(hasil['peringatan'])} hal perlu dicek:")
        for p in hasil["peringatan"]:
            print(f"  - {p}")
    else:
        print("[OK] Tidak ada masalah yang terdeteksi oleh pemeriksaan otomatis ini.")
        print("      (Tetap baca ulang sendiri sebelum kirim — ini bukan jaminan.)")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Alat bantu pesan-prospek-wa: cek draf pesan & bangun tautan wa.me"
    )
    sub = ap.add_subparsers(dest="perintah", required=True)

    p_cek = sub.add_parser("cek", help="Periksa draf pesan (panjang, spam, asal kontak, opsi keluar, jam kirim)")
    grup = p_cek.add_mutually_exclusive_group(required=True)
    grup.add_argument("--pesan", help="Teks pesan langsung")
    grup.add_argument("--file", help="Path file teks berisi pesan")
    p_cek.add_argument("--jam-kirim", default=None, help="Jam rencana kirim, format 24 jam HH:MM, mis. 19:30")

    p_wa = sub.add_parser("wa", help="Bangun tautan wa.me dari nomor + pesan")
    p_wa.add_argument("--nomor", required=True, help="Nomor WhatsApp, mis. 0812xxxxxxx atau 62812xxxxxxx")
    p_wa.add_argument("--pesan", default="", help="Isi pesan yang otomatis terisi saat tombol WA diklik")

    args = ap.parse_args(argv)

    try:
        if args.perintah == "cek":
            if args.file:
                try:
                    with open(args.file, "r", encoding="utf-8") as f:
                        teks = f.read()
                except OSError as e:
                    raise InputSalah(f"tidak bisa membaca file {args.file!r}: {e}")
            else:
                teks = args.pesan
            hasil = periksa_pesan(teks, jam_kirim=args.jam_kirim)
            cetak_hasil_periksa(hasil)
            return 0
        elif args.perintah == "wa":
            print(bangun_tautan_wa(args.nomor, args.pesan))
            return 0
    except InputSalah as e:
        print(f"Input tidak valid: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
