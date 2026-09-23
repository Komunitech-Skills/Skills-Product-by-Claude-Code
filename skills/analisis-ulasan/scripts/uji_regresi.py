#!/usr/bin/env python3
"""Uji regresi olah_ulasan.py. Jalankan: python3 uji_regresi.py  (keluar 0 bila semua lulus)."""
import json
import re
import os
import subprocess
import sys
import tempfile

SINI = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(SINI, "olah_ulasan.py")

# (teks ulasan, tema yang WAJIB ada, tema yang TIDAK boleh ada)
KASUS = [
    ("pesanan diproses lama, 5 hari baru dikirim", ["k_pengiriman"], ["k_respons"]),
    ("chat ga dibales 2 hari", ["k_respons"], []),
    ("brg ga sesuai deskripsi, warnanya beda sama di foto", ["k_tidak_sesuai"], ["k_salah_kirim", "p_sesuai"]),
    ("salah kirim warna, pesen hitam dikirim putih", ["k_salah_kirim"], []),
    ("rasanya ga terlalu manis, pas", [], ["k_rasa"]),
    ("bau apek pas dibuka", ["k_bau"], ["k_rasa"]),
    ("tidak ada yang rusak, semua aman", ["p_kualitas"], ["k_kualitas"]),
    ("kemasan penyok untung isinya aman", ["k_kemasan"], ["k_kualitas"]),
    ("nemu rambut di pastry nya", ["k_kebersihan"], []),
    ("pelayanannya lama banget, nunggu 40 menit", ["k_waktu_tunggu"], ["k_pengiriman"]),
    ("nunggu paket lama banget", ["k_pengiriman"], ["k_waktu_tunggu"]),
    ("parkirnya sempit, toilet kotor", ["k_fasilitas"], []),
    ("tempatnya cozy dan bersih", ["p_suasana", "p_kebersihan"], []),
    ("good quality, fast delivery, will buy again", ["p_kualitas", "p_pengiriman", "p_repeat"], []),
    ("bahannya tebel, ketagihan order", ["p_kualitas"], []),
    ("fast respon, seller ramah", ["p_respons"], ["k_respons"]),
    ("pengiriman cepet, packing rapi pake bubble wrap", ["p_pengiriman", "p_kemasan"], []),
    ("ukurannya kekecilan", ["k_ukuran"], []),
]


def jalankan(args, teks=None):
    r = subprocess.run([sys.executable, SCRIPT] + args, input=teks, capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout, r.stderr


def tema_ulasan(teks, ekstra=None):
    ekstra = ekstra or []
    hasil = set()
    rc, out, err = jalankan(["-"] + ekstra, "3 | " + teks + "\n")
    assert rc == 0, err
    d = json.loads(out)
    for t in d["keluhan_berdasarkan_prioritas"] + d["pujian_terbanyak"]:
        hasil.add(t["id"])
    return hasil, d


def main():
    gagal = 0
    for teks, wajib, larang in KASUS:
        tema, _ = tema_ulasan(teks)
        salah = [w for w in wajib if w not in tema] + [l for l in larang if l in tema]
        if salah:
            gagal += 1
            print("GAGAL: {!r} -> {} (masalah: {})".format(teks, sorted(tema), salah))

    # privasi: email, nomor, nama tidak bocor di kutipan maupun kata teratas
    teks = ("1 | Barang rusak. Hubungi saya di siti.rahma@gmail.com atau 081234567890. Makasih kak Budi Santoso\n"
            "1 | rusak lagi, kak Rina tolong cek. email: budi.x@yahoo.co.id\n")
    rc, out, err = jalankan(["-"], teks)
    for bocor in ("siti", "rahma", "gmail", "0812", "Budi", "Rina", "budi", "yahoo"):
        if re.search(r"\b" + re.escape(bocor.lower()), out.lower()):
            gagal += 1
            print("GAGAL privasi: '{}' muncul di output".format(bocor))

    # angka ribuan tidak terpotong di kutipan
    _, d = tema_ulasan("harga Rp 1.500.000 worth it banget")
    kutipan = [c["kutipan"] for t in d["pujian_terbanyak"] for c in t["contoh"]]
    if not any("1.500.000" in k for k in kutipan):
        gagal += 1
        print("GAGAL: angka Rp terpotong: {}".format(kutipan))

    # kecualikan lewat kamus tambahan & --abaikan-id
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump({"tema": [{"id": "k_kualitas", "kecualikan": ["\\bmati\\W+lampu\\b"]}]}, f)
        kamus = f.name
    try:
        tema, _ = tema_ulasan("pas mati lampu tetap bisa dipakai", ["--kamus-tambahan", kamus])
        if "k_kualitas" in tema:
            gagal += 1
            print("GAGAL: 'kecualikan' tidak bekerja")
    finally:
        os.unlink(kamus)
    rc, out, _ = jalankan(["-", "--abaikan-id", "k_ukuran:1"], "3 | ukurannya kekecilan\n2 | kekecilan\n")
    d = json.loads(out)
    uk = [t for t in d["keluhan_berdasarkan_prioritas"] if t["id"] == "k_ukuran"]
    if not uk or uk[0]["jumlah_ulasan"] != 1:
        gagal += 1
        print("GAGAL: --abaikan-id tidak mengurangi hitungan")

    # input rusak -> exit 2
    for args, teks in ((["-"], ""), (["tidak-ada.csv"], None), (["-", "--abaikan-id", "zzz:1"], "5 | ok\n"),
                       (["-", "--abaikan-id", "k_ukuran:a"], "5 | ok\n")):
        rc, _, err = jalankan(args, teks)
        if rc != 2 or "ERROR" not in err:
            gagal += 1
            print("GAGAL: input rusak {} tidak menghasilkan ERROR kode 2".format(args))

    print("Selesai: {} kasus gagal.".format(gagal) if gagal else "Semua uji regresi lulus.")
    sys.exit(1 if gagal else 0)


if __name__ == "__main__":
    main()
