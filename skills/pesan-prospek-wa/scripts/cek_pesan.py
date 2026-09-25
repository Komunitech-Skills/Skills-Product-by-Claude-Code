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
BATAS_EMOJI_DISARANKAN = 3        # > 3 emoji dianggap berlebihan untuk pesan pembuka (v1.0.1 B7)
JAM_MULAI_WAJAR = 8               # 08.00
JAM_SELESAI_WAJAR = 20            # 20.00 (batas akhir, > jam ini dianggap terlalu malam)

# Nomor seluler Indonesia (format 08xx) biasanya 10-13 digit TERMASUK angka 0 di
# depan. Setelah "0" diganti kode negara "62" (2 digit), sisa digit (mis. 8xx...)
# harus 9-12 digit -> total nomor berkode negara 11-14 digit. (v1.0.1 B2)
PANJANG_MIN_SISA_SELULER = 9
PANJANG_MAKS_SISA_SELULER = 12

# Singkatan umum yang boleh huruf besar semua tanpa dianggap "teriak".
# Fokus istilah B2B/UMKM Indonesia yang lazim ditulis kapital. (v1.0.1 B3)
SINGKATAN_AMAN = {
    "WA", "CS", "PT", "CV", "UD", "QRIS", "COD", "ID", "RT", "RW", "KTP",
    "NPWP", "SD", "SMP", "SMA", "SMK", "UMKM", "BPOM", "IG", "FB", "TT",
    "STOP", "OK", "SIM", "AC", "TV",
    # Tambahan v1.0.1 (temuan B3 — istilah B2B/UMKM Indonesia lazim kapital)
    "HRD", "GA", "PPN", "PPH", "SPT", "NIB", "PKP", "SOP", "BPJS",
    "CEO", "CFO", "COO", "GM", "B2B", "B2C", "ISO", "HACCP",
    "HIPMI", "KADIN", "APINDO", "JNE", "JNT", "PDF", "API", "SEO",
    "SDM", "OJK", "NIK", "SIUP", "TDP", "HAKI", "DP", "PO", "PIC",
    "FAQ", "ATM", "KUR", "UKM", "BUMN",
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

# Kata kunci yang menandai pesan MENYEBUT asal kontak (heuristik).
# v1.0.1 (temuan B1): daftar ini diturunkan langsung dari SETIAP pola di
# references/pola-pembuka.md (referral, pameran/expo/bazar, Google Maps/ulasan,
# Instagram/IG/TikTok/postingan, grup/komunitas, website/situs resmi) supaya
# script tidak lagi bertentangan dengan referensinya sendiri. "dari bapak"/
# "dari ibu" SENGAJA tidak dipakai lagi sendirian (dulu memicu salah-positif
# pada kalimat seperti "resep warisan dari ibu saya" yang bukan asal kontak).
KATA_KUNCI_ASAL_KONTAK = [
    # 1. Referral / rekomendasi orang lain
    "dapat nomor", "dapat kontak", "dapat kontaknya", "dapat nomornya",
    "nomor bapak/ibu saya dapat", "kontak ini saya dapat", "dari rekomendasi",
    "direkomendasikan oleh", "rekomendasi dari", "referensi dari",
    "dikasih tahu oleh", "menyarankan saya menghubungi", "dari teman",
    "dari kenalan", "izin menghubungi", "kontak dari", "nomor dari",
    "nomor bapak dari", "nomor ibu dari",
    # 2. Pameran / bazar / acara networking
    "di pameran", "dari pameran", "pameran umkm", "di bazar", "dari bazar",
    "di expo", "dari expo", "acara networking", "di acara", "bertukar kontak",
    "tukar kontak", "tukar kartu nama", "bertemu di", "ketemu di",
    "sempat mengobrol", "mengobrol di",
    # 3. Google Maps / listing bisnis publik
    "google maps", "di maps", "ulasan google", "listing bisnis",
    # 4. Instagram / media sosial usaha
    "akun instagram", "di instagram", "dari instagram", "dari ig", "di ig",
    "akun ig", "di tiktok", "dari tiktok", "lihat postingan", "melihat postingan",
    "dari postingan", "unggahan", "dari facebook",
    # 5. Grup komunitas / WhatsApp Group bisnis
    "anggota grup", "sama-sama anggota", "di grup", "dari grup",
    "grup whatsapp", "grup komunitas",
    # Website / situs resmi (sumber sah lain yang disebut dasar-hukum-wa.md)
    "di website", "dari website", "situs resmi", "website resmi", "di situs",
    # Kontak lama yang dingin kembali & sumber umum lain
    "sempat kontak", "kontak lama", "dari marketplace", "lihat dari",
    "melihat profil", "melihat usaha bapak/ibu", "melihat usaha ibu/bapak",
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
    """Ubah nomor HP Indonesia ke format 62xxxxxxxxxx (tanpa '+', tanpa spasi/strip).

    v1.0.1 (temuan B2):
    - Membuang awalan internasional "00" (mis. "0062..." -> "62...").
    - Mengoreksi salah ketik umum "+62 0812..." (kebiasaan menulis "0" dari
      format lokal setelah kode negara) -> "62812...".
    - Hanya menerima digit ASCII 0-9 (bukan digit Unicode full-width/Arab-Indik,
      yang dulu lolos lewat `\\d` dan memicu pesan error menyesatkan).
    - Memvalidasi panjang & pola nomor seluler Indonesia: setelah kode negara
      "62", sisanya harus diawali "8" dan berjumlah 9-12 digit (nomor 08xx
      Indonesia lazimnya 10-13 digit termasuk "0" di depan). Nomor 14+ digit
      (atau bukan pola 8xx, mis. nomor telepon rumah) ditolak dengan pesan jelas.
    """
    if nomor is None or not str(nomor).strip():
        raise InputSalah("nomor WhatsApp kosong")
    bersih = re.sub(r"[\s\-().]", "", str(nomor).strip())
    if bersih.startswith("+"):
        bersih = bersih[1:]
    if bersih.startswith("00") and len(bersih) > 2:
        bersih = bersih[2:]
    if not re.fullmatch(r"[0-9]{8,15}", bersih):
        raise InputSalah(
            f"nomor {nomor!r} tidak terlihat seperti nomor HP yang valid "
            "(harus angka biasa 0-9, 8-15 digit setelah spasi/tanda/awalan 00 dibuang)"
        )
    if bersih.startswith("620") and len(bersih) > 3:
        # Salah ketik umum: "+62 0812..." -> buang "0" ekstra setelah kode negara.
        bersih = "62" + bersih[3:]
    elif bersih.startswith("0"):
        bersih = "62" + bersih[1:]
    elif bersih.startswith("8"):
        bersih = "62" + bersih
    elif not bersih.startswith("62"):
        raise InputSalah(
            f"nomor {nomor!r}: awali dengan 08xx, 8xx, atau 62xx (kode negara Indonesia)"
        )
    sisa = bersih[2:]
    if not sisa.startswith("8") or not (
        PANJANG_MIN_SISA_SELULER <= len(sisa) <= PANJANG_MAKS_SISA_SELULER
    ):
        raise InputSalah(
            f"nomor {nomor!r} (dinormalisasi jadi {bersih!r}) panjang/polanya tidak wajar "
            "untuk nomor seluler Indonesia. Nomor 08xx biasanya 10-13 digit termasuk '0' "
            "di depan (jadi 62 + 9-12 digit setelah itu, diawali '8'). Periksa lagi — bisa "
            "jadi salah ketik, atau ini bukan nomor seluler (mis. telepon rumah/kantor)."
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
    # v1.0.1 (temuan B8): juga pisah di baris baru, supaya daftar poin bergaya
    # "✅ ... \n✅ ..." (tanpa titik) tidak dihitung sebagai satu kalimat raksasa.
    potongan = re.split(r"(?<=[.!?])\s+|\n+", teks.strip())
    return [p.strip() for p in potongan if p.strip()]


def hitung_kata(teks):
    return len(re.findall(r"\S+", teks))


# Rentang Unicode emoji/simbol piktograf yang umum dipakai di pesan WA.
# (v1.0.1 B7 — bukan daftar lengkap seluruh emoji, tapi cukup untuk kasus wajar.)
_POLA_EMOJI = re.compile(
    "["
    "\U0001F300-\U0001F5FF"
    "\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\U0001F700-\U0001F77F"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FAFF"
    "\U00002600-\U000026FF"
    "\U00002700-\U000027BF"
    "]"
)


def hitung_emoji(teks):
    return len(_POLA_EMOJI.findall(teks))


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
    """jam_teks format 'HH:MM', 'HH.MM', atau 4 digit 'HHMM'.
    Return (jam_int, wajar_bool) atau None jika tidak diisi.

    v1.0.1 (temuan B4): dulu HANYA menerima 'HH:MM', padahal SKILL.md &
    checklist sendiri menulis jam dengan titik (mis. "08.00-20.00") — orang
    Indonesia hampir selalu mengetik titik, bukan titik dua.
    """
    if not jam_teks:
        return None
    teks = jam_teks.strip()
    cocok = re.fullmatch(r"([01]?[0-9]|2[0-3])[:.]([0-5][0-9])", teks)
    if not cocok:
        cocok = re.fullmatch(r"([01][0-9]|2[0-3])([0-5][0-9])", teks)  # mis. "1930"
    if not cocok:
        raise InputSalah(
            "format --jam-kirim harus HH:MM atau HH.MM (24 jam, mis. 19:30 atau 19.30; "
            f"boleh juga 4 digit tanpa pemisah, mis. 1930), diberi {jam_teks!r}"
        )
    jam = int(cocok.group(1))
    wajar = JAM_MULAI_WAJAR <= jam < JAM_SELESAI_WAJAR
    return jam, wajar


ZONA_WAKTU_VALID = ("WIB", "WITA", "WIT")


def periksa_pesan(teks, jam_kirim=None, zona=None):
    if not teks or not teks.strip():
        raise InputSalah("pesan kosong")
    if zona is not None and zona.strip().upper() not in ZONA_WAKTU_VALID:
        raise InputSalah(
            f"--zona {zona!r} tidak dikenal, pakai salah satu: {', '.join(ZONA_WAKTU_VALID)}"
        )
    zona = zona.strip().upper() if zona else None

    jumlah_karakter = len(teks.strip())
    jumlah_kata = hitung_kata(teks)
    jumlah_baris = len(teks.strip().splitlines())
    jumlah_emoji = hitung_emoji(teks)

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
    if jumlah_emoji > BATAS_EMOJI_DISARANKAN:
        peringatan.append(
            f"Ada {jumlah_emoji} emoji — lebih dari {BATAS_EMOJI_DISARANKAN}, bisa terkesan "
            "berlebihan/spam untuk pesan pertama (checklist anti-blokir menyarankan sewajarnya, idealnya 1)."
        )
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
        label_zona = f" {zona}" if zona else " (zona waktu tidak disebutkan lewat --zona)"
        if not wajar:
            peringatan.append(
                f"Jam kirim {jam_kirim} di luar rentang wajar {JAM_MULAI_WAJAR:02d}.00–{JAM_SELESAI_WAJAR:02d}.00"
                f"{label_zona} — ingat, jam ini harus waktu SETEMPAT PENERIMA (WIB/WITA/WIT), "
                "bukan waktu pengirim. Pertimbangkan menjadwalkan ulang."
            )
        elif not zona:
            peringatan.append(
                "Jam kirim wajar, tapi zona waktu tidak disebutkan lewat --zona. Pastikan jam ini "
                "sudah dalam waktu SETEMPAT PENERIMA (WIB/WITA/WIT), bukan waktu kamu sendiri."
            )

    return {
        "jumlah_karakter": jumlah_karakter,
        "jumlah_kata": jumlah_kata,
        "jumlah_baris": jumlah_baris,
        "jumlah_link": jumlah_link,
        "jumlah_emoji": jumlah_emoji,
        "sebut_asal_kontak": sebut_asal_kontak,
        "ada_opsi_keluar": ada_opsi_keluar,
        "jam_kirim_wajar": info_jam[1] if info_jam is not None else None,
        "zona": zona,
        "peringatan": peringatan,
    }


def cetak_hasil_periksa(hasil):
    print(f"Jumlah karakter : {hasil['jumlah_karakter']}")
    print(f"Jumlah kata     : {hasil['jumlah_kata']}")
    print(f"Jumlah baris    : {hasil['jumlah_baris']}")
    print(f"Jumlah link     : {hasil['jumlah_link']}")
    print(f"Jumlah emoji    : {hasil['jumlah_emoji']}")
    print(f"Sebut asal kontak terdeteksi : {'Ya' if hasil['sebut_asal_kontak'] else 'Tidak'}")
    print(f"Opsi keluar terdeteksi       : {'Ya' if hasil['ada_opsi_keluar'] else 'Tidak'}")
    if hasil["jam_kirim_wajar"] is not None:
        zona_cetak = hasil["zona"] or "?"
        print(f"Jam kirim wajar (08.00-20.00 waktu {zona_cetak} SETEMPAT PENERIMA) : {'Ya' if hasil['jam_kirim_wajar'] else 'Tidak'}")
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
    p_cek.add_argument(
        "--jam-kirim", default=None,
        help="Jam rencana kirim, WAKTU SETEMPAT PENERIMA, format 24 jam HH:MM atau HH.MM "
        "(mis. 19:30 / 19.30 / 1930)",
    )
    p_cek.add_argument(
        "--zona", default=None, choices=list(ZONA_WAKTU_VALID) + [z.lower() for z in ZONA_WAKTU_VALID],
        help="Zona waktu SETEMPAT PENERIMA untuk --jam-kirim: WIB, WITA, atau WIT (opsional, tapi disarankan)",
    )

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
            hasil = periksa_pesan(teks, jam_kirim=args.jam_kirim, zona=args.zona)
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
