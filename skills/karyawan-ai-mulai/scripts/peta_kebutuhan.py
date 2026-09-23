#!/usr/bin/env python3
"""Cocokkan jawaban wawancara singkat ke rekomendasi skill dari library Komunitech.

Tujuan: hasil rekomendasi KONSISTEN (tidak dikira-kira ulang tiap kali), sesuai
`references/peta-skill.md`. Hanya memakai library Python standar (Python 3.8+).

Pakai:
    python3 scripts/peta_kebutuhan.py --tugas "bikin caption" --tugas "rekap penjualan" \
        --tugas "balas chat pelanggan" --industri "toko retail" --json

Windows: ganti `python3` dengan `python` atau `py`.

Uji sendiri (20 frasa member nyata, termasuk kasus yang dulu salah cocok):
    python3 scripts/peta_kebutuhan.py --self-test

Keluaran: JSON berisi skill yang cocok per tugas (satu skill per tugas, yang paling
relevan, dicocokkan sebagai KATA/FRASA UTUH — bukan potongan huruf di tengah kata
lain), lalu diisi sampai minimal 3 rekomendasi dari paket industri, lalu paket umum,
tanpa duplikat. Kalau tidak ada Python yang bisa dijalankan, cocokkan MANUAL dengan
tabel di `references/peta-skill.md` — jangan menebak nama skill di luar tabel itu.
"""
import argparse
import json
import re
import sys
import unicodedata

# (kata kunci/frasa yang dicari sebagai KATA UTUH di jawaban pengguna, huruf kecil) -> skill
# Urutan penting: frasa lebih spesifik ditaruh lebih dulu agar tidak tertimpa frasa umum
# (mis. "ulasan" sebelum "chat"). SEMUA kunci dicocokkan dengan batas kata (\b...\b),
# jadi "kur" TIDAK match "kurir", "sop" TIDAK match "sopir", "nota" TIDAK match "notaris".
# Kunci yang terlalu pendek/berisiko ambigu meski sudah dibatasi kata (mis. akronim 2-3
# huruf seperti "kur", "hr", "mou", "nda", atau "ter " dengan spasi) SENGAJA tidak dipakai
# sendirian -- selalu dalam bentuk frasa yang lebih panjang.
PEMETAAN = [
    (["rekap ulasan", "banyak ulasan", "ratusan ulasan", "analisis ulasan", "sentiment", "rangkum ulasan"], "analisis-ulasan"),
    (["balas ulasan", "balas review", "reply review", "rating jelek", "bintang 1", "review pelanggan"], "balas-ulasan-pelanggan"),
    (["balas chat", "bales chat", "bales wa", "balas wa", "auto reply", "autoreply", "customer service",
      "cs pelanggan", "quick reply", "faq pelanggan", "layani pelanggan", "chat pelanggan"], "balas-chat-cs"),
    (["arus kas", "cash flow", "proyeksi kas", "uang cukup sampai", "cash runway", "kas 13 minggu"], "arus-kas-13minggu"),
    (["laporan keuangan", "laba rugi", "neraca", "sak emkm", "untung berapa bulan ini"], "laporan-keuangan-emkm"),
    (["rekonsiliasi", "cocokkan mutasi", "rekening koran", "cek transfer masuk", "mutasi bank"], "rekonsiliasi-bank"),
    (["rekap penjualan", "rekap jualan", "rekap omzet", "laporan penjualan", "laporan jualan",
      "sales report", "omzet harian", "laporan omzet"], "rekap-penjualan-csv"),
    (["laporan otomatis", "kirim laporan otomatis", "jadwalkan laporan", "laporan rutin terjadwal",
      "laporan terjadwal", "scheduled report", "auto-send report", "kirim rekap tiap pagi"], "laporan-otomatis-terjadwal"),
    (["catat stok", "cek stok", "stock opname", "stok opname", "restock", "picking list",
      "potong stok", "buku stok", "inventori toko", "stok menipis"], "buku-stok"),
    (["input struk", "ketik ulang nota", "cek faktur pajak", "rekap nota belanja"], "ekstrak-nota-faktur"),
    (["kalender konten", "jadwal posting", "content plan", "content calendar", "rencana konten 30 hari"], "kalender-konten-30hari"),
    (["bikin caption", "buat caption", "caption sosmed", "copywriting", "konten sosmed",
      "bikin konten", "buat konten", "posting instagram", "posting ig", "posting tiktok"], "caption-sosmed-umkm"),
    (["rencana promo", "diskon aman", "flash sale", "campaign plan", "sale planning"], "promo-kalender"),
    (["follow up", "follow-up", "prospek belum balas", "chasing lead", "ghosting", "klien belum balas"], "follow-up-prospek"),
    (["tagih piutang", "nagih utang", "belum bayar", "telat bayar", "debt collection", "overdue invoice"], "tagih-piutang"),
    (["buat invoice", "bikin invoice", "kuitansi", "billing", "nota tagihan"], "buat-invoice"),
    (["penawaran harga", "surat penawaran", "sph", "quotation", "price quote"], "surat-penawaran-harga"),
    (["broadcast wa", "blast wa", "bulk message", "wa marketing", "pesan massal"], "broadcast-wa"),
    (["notulen", "notula", "risalah rapat", "meeting notes", "rangkum rapat", "rangkum meeting"], "notulen-rapat"),
    (["surat resmi", "surat dinas", "surat undangan", "surat keterangan", "formal letter"], "surat-resmi"),
    (["buat sop", "bikin sop", "prosedur kerja", "checklist harian", "standard operating procedure"], "sop-writer"),
    (["lowongan", "loker", "rekrut karyawan", "job posting", "hiring", "cari karyawan baru"], "lowongan-kerja"),
    (["surat peringatan", "surat sp1", "surat sp2", "surat sp3", "surat teguran karyawan"], "surat-peringatan-karyawan"),
    (["slip gaji", "hitung gaji", "gaji karyawan", "payroll", "potongan bpjs"], "slip-gaji-bpjs"),
    (["pph 21", "pph21", "pajak karyawan", "withholding tax", "metode ter", "tarif efektif rata-rata"], "pph21-ter"),
    (["hitung thr", "thr lebaran", "thr natal", "holiday allowance"], "hitung-thr"),
    (["pph final", "pajak umkm", "pph umkm", "pph 0,5", "pph 0.5"], "pph-final-umkm"),
    (["hitung ppn", "pisahkan ppn", "harga include ppn", "pajak pertambahan nilai"], "hitung-ppn"),
    (["hitung hpp", "modal per pcs", "harga pokok produksi", "break even", "titik impas", "unit cost"], "hitung-hpp"),
    (["harga jual marketplace", "potongan marketplace", "untung bersih per produk", "seller fee"], "harga-jual-marketplace"),
    (["buat listing", "judul produk", "deskripsi produk", "marketplace seo", "optimasi listing"], "listing-marketplace"),
    (["foto produk", "shot list", "product photography"], "foto-produk-brief"),
    (["live selling", "live jualan", "livestream shopping", "rundown live", "naskah live"], "naskah-live-jualan"),
    (["program reseller", "jadi reseller", "buka agen", "jadi agen", "dropship", "dropshipper", "tier pricing"], "katalog-reseller"),
    (["proposal kerjasama", "proposal kemitraan", "sponsorship", "partnership proposal"], "proposal-kerjasama"),
    (["surat perjanjian", "buat kontrak", "draf kontrak", "nda kerahasiaan", "mou kerjasama"], "perjanjian-sederhana"),
    (["ajukan kur", "kur bri", "kur mandiri", "kur bni", "kredit usaha rakyat", "pinjaman usaha", "business loan", "cicilan kur"], "pengajuan-kur"),
]

# Industri/peran -> paket default (dipakai bila pengguna minta cepat/pakai default,
# atau untuk mengisi rekomendasi sampai minimal 3 bila tugas belum cukup cocok).
PAKET_INDUSTRI = {
    "toko": ["rekap-penjualan-csv", "balas-chat-cs", "caption-sosmed-umkm"],
    "retail": ["rekap-penjualan-csv", "balas-chat-cs", "caption-sosmed-umkm"],
    "f&b": ["rekap-penjualan-csv", "balas-chat-cs", "caption-sosmed-umkm"],
    "fnb": ["rekap-penjualan-csv", "balas-chat-cs", "caption-sosmed-umkm"],
    "kuliner": ["rekap-penjualan-csv", "balas-chat-cs", "caption-sosmed-umkm"],
    "restoran": ["rekap-penjualan-csv", "balas-chat-cs", "caption-sosmed-umkm"],
    "rumah makan": ["rekap-penjualan-csv", "balas-chat-cs", "caption-sosmed-umkm"],
    "warung": ["rekap-penjualan-csv", "balas-chat-cs", "caption-sosmed-umkm"],
    "kafe": ["rekap-penjualan-csv", "balas-chat-cs", "caption-sosmed-umkm"],
    "cafe": ["rekap-penjualan-csv", "balas-chat-cs", "caption-sosmed-umkm"],
    "jasa": ["surat-penawaran-harga", "follow-up-prospek", "buat-invoice"],
    "konsultasi": ["surat-penawaran-harga", "follow-up-prospek", "buat-invoice"],
    "konsultan": ["surat-penawaran-harga", "follow-up-prospek", "buat-invoice"],
    "freelance": ["surat-penawaran-harga", "follow-up-prospek", "buat-invoice"],
    "freelancer": ["surat-penawaran-harga", "follow-up-prospek", "buat-invoice"],
    "bengkel": ["surat-penawaran-harga", "buat-invoice", "follow-up-prospek"],
    "kantor": ["notulen-rapat", "surat-resmi", "sop-writer"],
    "admin": ["notulen-rapat", "surat-resmi", "sop-writer"],
    "keuangan": ["laporan-keuangan-emkm", "rekonsiliasi-bank", "arus-kas-13minggu"],
    "akuntansi": ["laporan-keuangan-emkm", "rekonsiliasi-bank", "arus-kas-13minggu"],
    "sdm": ["slip-gaji-bpjs", "pph21-ter", "lowongan-kerja"],
    "kepegawaian": ["slip-gaji-bpjs", "pph21-ter", "lowongan-kerja"],
    "human resources": ["slip-gaji-bpjs", "pph21-ter", "lowongan-kerja"],
    "manufaktur": ["hitung-hpp", "arus-kas-13minggu", "rekap-penjualan-csv"],
    "produksi": ["hitung-hpp", "arus-kas-13minggu", "rekap-penjualan-csv"],
    # Dokter solo: prioritas balas pasien (Copilot -- draf balasan, bukan auto-reply
    # langsung ke pasien) & edukasi, baru SOP/surat. TIDAK ada skrining/diagnosis medis.
    "dokter": ["balas-chat-cs", "sop-writer", "surat-resmi"],
    "klinik": ["balas-chat-cs", "sop-writer", "notulen-rapat"],
    "kesehatan": ["balas-chat-cs", "sop-writer", "notulen-rapat"],
    "properti": ["surat-penawaran-harga", "follow-up-prospek", "proposal-kerjasama"],
}

PAKET_UMUM = ["rekap-penjualan-csv", "balas-chat-cs", "surat-resmi"]

# Uji sendiri: frasa nyata dari persona member + kasus yang dulu salah cocok (regresi).
# (tugas, industri_opsional) -> skill yang DIHARAPKAN, atau None untuk "tidak boleh cocok".
KASUS_UJI = [
    ("input no resi kurir", None, None),          # dulu: salah -> pengajuan-kur
    ("gaji sopir bulan ini", None, None),          # dulu: salah -> sop-writer
    ("catat pendapatan harian", None, None),       # dulu: salah -> perjanjian-sederhana ("nda")
    ("bantu atur agenda saya", None, None),        # dulu: salah -> katalog-reseller ("agen")
    ("urus surat ke notaris", None, None),         # dulu: salah -> ekstrak-nota-faktur ("nota")
    ("hitung amount pembayaran", None, None),      # dulu: salah -> perjanjian-sederhana ("mou")
    ("mau ke dokter dulu", None, None),            # dulu: salah -> pph21-ter ("ter ")
    (None, "shrimp farm", None),                   # dulu: salah -> paket HR ("hr" di "shrimp")
    ("rekap jualan minggu ini", None, "rekap-penjualan-csv"),
    ("bales wa pelanggan", None, "balas-chat-cs"),
    ("bikin konten buat ig", None, "caption-sosmed-umkm"),
    ("posting ig tiap hari", None, "caption-sosmed-umkm"),
    ("laporan omzet bulanan", None, "rekap-penjualan-csv"),
    ("gaji karyawan bulan ini", None, "slip-gaji-bpjs"),
    ("catat stok gudang", None, "buku-stok"),
    ("kirim laporan otomatis tiap senin", None, "laporan-otomatis-terjadwal"),
    ("ajukan kur bri buat modal", None, "pengajuan-kur"),
    ("buat sop packing pesanan", None, "sop-writer"),
    ("ketik ulang nota belanja", None, "ekstrak-nota-faktur"),
    ("hitung thr lebaran", None, "hitung-thr"),
    (None, "restoran padang", "rekap-penjualan-csv"),
    (None, "rumah makan keluarga", "rekap-penjualan-csv"),
    (None, "kafe kopi kecil", "rekap-penjualan-csv"),
    (None, "dokter gigi solo", "balas-chat-cs"),
    (None, "bengkel motor", "surat-penawaran-harga"),
]


def normalisasi(teks):
    teks = teks.lower().strip()
    teks = unicodedata.normalize("NFKD", teks)
    return teks


def _pola_kata_utuh(frasa):
    """Regex kata/frasa UTUH: batas kata di awal & akhir, spasi di tengah fleksibel."""
    bagian = [re.escape(kata) for kata in frasa.split()]
    return re.compile(r"\b" + r"\s+".join(bagian) + r"\b")


# Pra-kompilasi semua pola sekali saja (dipakai berulang oleh cocokkan_tugas/industri).
_POLA_PEMETAAN = [([_pola_kata_utuh(kk) for kk in daftar], skill) for daftar, skill in PEMETAAN]
_POLA_INDUSTRI = {kunci: _pola_kata_utuh(kunci) for kunci in PAKET_INDUSTRI}


def cocokkan_tugas(tugas):
    t = normalisasi(tugas)
    for pola_list, skill in _POLA_PEMETAAN:
        for pola in pola_list:
            if pola.search(t):
                return skill
    return None


def cocokkan_industri(industri):
    ind = normalisasi(industri)
    for kunci, pola in _POLA_INDUSTRI.items():
        if pola.search(ind):
            return PAKET_INDUSTRI[kunci]
    return None


def rekomendasikan(daftar_tugas, industri):
    """Kembalikan (rekomendasi[], tugas_tanpa_cocok[], paket_industri|None).

    rekomendasi selalu diisi sampai MINIMAL 3 skill (bila memungkinkan dari data
    yang ada): dari tugas yang cocok dulu, lalu paket industri, lalu paket umum,
    tanpa duplikat -- sesuai §2 peta-skill.md.
    """
    rekomendasi = []
    tugas_tanpa_cocok = []
    dipakai = set()
    for tugas in daftar_tugas[:3]:
        skill = cocokkan_tugas(tugas)
        if skill and skill not in dipakai:
            rekomendasi.append({"tugas": tugas, "skill": skill})
            dipakai.add(skill)
        elif not skill:
            tugas_tanpa_cocok.append(tugas)

    paket_industri = cocokkan_industri(industri) if industri else None

    for skill in (paket_industri or []):
        if len(rekomendasi) >= 3:
            break
        if skill not in dipakai:
            rekomendasi.append({"tugas": None, "skill": skill})
            dipakai.add(skill)

    for skill in PAKET_UMUM:
        if len(rekomendasi) >= 3:
            break
        if skill not in dipakai:
            rekomendasi.append({"tugas": None, "skill": skill})
            dipakai.add(skill)

    return rekomendasi, tugas_tanpa_cocok, paket_industri


def jalankan_self_test():
    gagal = 0
    for tugas, industri, diharapkan in KASUS_UJI:
        if tugas is not None:
            hasil = cocokkan_tugas(tugas)
            label = f"tugas={tugas!r}"
        else:
            paket = cocokkan_industri(industri)
            hasil = paket[0] if paket else None
            label = f"industri={industri!r}"
        ok = hasil == diharapkan
        status = "OK " if ok else "GAGAL"
        if not ok:
            gagal += 1
        print(f"[{status}] {label} -> {hasil!r} (diharapkan {diharapkan!r})")
    total = len(KASUS_UJI)
    print(f"\n{total - gagal}/{total} kasus lulus.")
    return gagal == 0


def main():
    ap = argparse.ArgumentParser(description="Cocokkan jawaban wawancara ke rekomendasi skill")
    ap.add_argument("--tugas", action="append", default=[], help="Tugas yang menyita waktu (bisa diulang, maks. dipakai 3)")
    ap.add_argument("--industri", default="", help="Industri/peran pengguna")
    ap.add_argument("--json", action="store_true", help="Output JSON (default: teks)")
    ap.add_argument("--self-test", action="store_true", help="Jalankan uji regresi bawaan lalu keluar")
    args = ap.parse_args()

    if args.self_test:
        sukses = jalankan_self_test()
        sys.exit(0 if sukses else 1)

    if not args.tugas and not args.industri:
        print("Error: isi minimal --tugas atau --industri.", file=sys.stderr)
        sys.exit(1)

    rekomendasi, tugas_tanpa_cocok, paket_industri = rekomendasikan(args.tugas, args.industri)

    hasil = {
        "rekomendasi": rekomendasi,
        "tugas_tanpa_padanan": tugas_tanpa_cocok,
        "paket_industri": paket_industri,
        "sumber": "references/peta-skill.md (tabel statis, jangan menebak di luar tabel ini)",
        "catatan": (
            "Tugas tanpa padanan tetap harus dijawab jujur ke pengguna: sebutkan tidak ada "
            "skill khusus, tawarkan skill terdekat bila ada, atau arahkan ke jasa/di luar cakupan."
        ),
    }

    if args.json:
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
    else:
        print("Rekomendasi skill:")
        for r in hasil["rekomendasi"]:
            asal = f" (dari tugas: {r['tugas']})" if r["tugas"] else " (default paket)"
            print(f"  - {r['skill']}{asal}")
        if hasil["tugas_tanpa_padanan"]:
            print("Tugas tanpa padanan di library:")
            for t in hasil["tugas_tanpa_padanan"]:
                print(f"  - {t}")


if __name__ == "__main__":
    main()
