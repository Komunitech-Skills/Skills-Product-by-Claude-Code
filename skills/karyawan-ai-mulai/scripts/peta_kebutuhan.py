#!/usr/bin/env python3
"""Cocokkan jawaban wawancara singkat ke rekomendasi skill dari library Komunitech.

Tujuan: hasil rekomendasi KONSISTEN (tidak dikira-kira ulang tiap kali), sesuai
`references/peta-skill.md`. Hanya memakai library Python standar (Python 3.8+).

Pakai:
    python3 scripts/peta_kebutuhan.py --tugas "bikin caption" --tugas "rekap penjualan" \
        --tugas "balas chat pelanggan" --industri "toko retail" --json

Windows: ganti `python3` dengan `python` atau `py`.

Keluaran: JSON berisi skill yang cocok per tugas (maks. 1 skill per tugas, yang paling
relevan) dan skill fallback per industri bila kata kunci tugas tidak cocok apa pun.
Kalau tidak ada Python yang bisa dijalankan, cocokkan MANUAL dengan tabel di
`references/peta-skill.md` — jangan menebak nama skill di luar tabel itu.
"""
import argparse
import json
import sys
import unicodedata

# (kata kunci yang dicari di dalam jawaban pengguna, huruf kecil) -> nama skill
# Urutan penting: kata kunci lebih spesifik ditaruh lebih dulu agar tidak tertimpa
# oleh kata kunci umum (mis. "ulasan" sebelum "chat").
PEMETAAN = [
    (["rekap ulasan", "banyak ulasan", "ratusan ulasan", "analisis ulasan", "sentiment"], "analisis-ulasan"),
    (["balas ulasan", "balas review", "reply review", "rating jelek", "bintang 1"], "balas-ulasan-pelanggan"),
    (["balas chat", "auto reply", "customer service", "cs pelanggan", "quick reply", "faq pelanggan"], "balas-chat-cs"),
    (["arus kas", "cash flow", "proyeksi kas", "uang cukup sampai", "cash runway"], "arus-kas-13minggu"),
    (["laporan keuangan", "laba rugi", "neraca", "sak emkm"], "laporan-keuangan-emkm"),
    (["rekonsiliasi", "cocokkan mutasi", "rekening koran", "cek transfer masuk"], "rekonsiliasi-bank"),
    (["rekap penjualan", "rekap omzet", "laporan penjualan", "sales report", "omzet harian"], "rekap-penjualan-csv"),
    (["nota", "struk", "faktur", "ocr", "input struk"], "ekstrak-nota-faktur"),
    (["kalender konten", "jadwal posting", "content plan", "content calendar", "rencana konten"], "kalender-konten-30hari"),
    (["caption", "copywriting", "konten sosmed", "posting instagram", "posting tiktok"], "caption-sosmed-umkm"),
    (["promo", "diskon", "flash sale", "campaign", "kampanye"], "promo-kalender"),
    (["follow up", "follow-up", "prospek belum balas", "chasing lead", "ghosting"], "follow-up-prospek"),
    (["tagih", "piutang", "belum bayar", "telat bayar", "debt collection", "overdue"], "tagih-piutang"),
    (["invoice", "kuitansi", "billing", "nota tagihan"], "buat-invoice"),
    (["penawaran harga", "sph", "quotation", "price quote"], "surat-penawaran-harga"),
    (["broadcast", "blast wa", "bulk message", "wa marketing"], "broadcast-wa"),
    (["notulen", "notula", "risalah rapat", "meeting notes", "rangkum rapat"], "notulen-rapat"),
    (["surat resmi", "surat dinas", "surat undangan", "surat keterangan", "formal letter"], "surat-resmi"),
    (["sop", "prosedur kerja", "checklist harian", "standard operating"], "sop-writer"),
    (["lowongan", "loker", "rekrut karyawan", "job posting", "hiring"], "lowongan-kerja"),
    (["surat peringatan", "sp1", "sp2", "sp3", "surat teguran karyawan"], "surat-peringatan-karyawan"),
    (["slip gaji", "payroll", "potongan bpjs", "hitung gaji"], "slip-gaji-bpjs"),
    (["pph 21", "pajak karyawan", "withholding tax", "ter "], "pph21-ter"),
    (["thr", "holiday allowance"], "hitung-thr"),
    (["pph final", "pajak umkm", "0,5%", "0.5%", "pph umkm"], "pph-final-umkm"),
    (["ppn", "vat", "pajak pertambahan nilai"], "hitung-ppn"),
    (["hpp", "modal per pcs", "break even", "bep", "unit cost"], "hitung-hpp"),
    (["harga jual marketplace", "potongan marketplace", "untung bersih per produk", "seller fee"], "harga-jual-marketplace"),
    (["listing", "judul produk", "deskripsi produk", "marketplace seo"], "listing-marketplace"),
    (["foto produk", "shot list", "product photography"], "foto-produk-brief"),
    (["live selling", "live jualan", "livestream shopping", "rundown live"], "naskah-live-jualan"),
    (["reseller", "dropship", "agen", "tier pricing"], "katalog-reseller"),
    (["proposal kerjasama", "proposal kemitraan", "sponsorship", "partnership proposal"], "proposal-kerjasama"),
    (["perjanjian", "kontrak", "mou", "nda"], "perjanjian-sederhana"),
    (["kur", "pinjaman usaha", "business loan", "cicilan"], "pengajuan-kur"),
]

# Industri/peran -> paket default (dipakai bila pengguna minta cepat/pakai default)
PAKET_INDUSTRI = {
    "toko": ["rekap-penjualan-csv", "balas-chat-cs", "caption-sosmed-umkm"],
    "retail": ["rekap-penjualan-csv", "balas-chat-cs", "caption-sosmed-umkm"],
    "f&b": ["rekap-penjualan-csv", "balas-chat-cs", "caption-sosmed-umkm"],
    "kuliner": ["rekap-penjualan-csv", "balas-chat-cs", "caption-sosmed-umkm"],
    "jasa": ["surat-penawaran-harga", "follow-up-prospek", "buat-invoice"],
    "konsultasi": ["surat-penawaran-harga", "follow-up-prospek", "buat-invoice"],
    "freelance": ["surat-penawaran-harga", "follow-up-prospek", "buat-invoice"],
    "kantor": ["notulen-rapat", "surat-resmi", "sop-writer"],
    "admin": ["notulen-rapat", "surat-resmi", "sop-writer"],
    "keuangan": ["laporan-keuangan-emkm", "rekonsiliasi-bank", "arus-kas-13minggu"],
    "akuntansi": ["laporan-keuangan-emkm", "rekonsiliasi-bank", "arus-kas-13minggu"],
    "hr": ["slip-gaji-bpjs", "pph21-ter", "lowongan-kerja"],
    "sdm": ["slip-gaji-bpjs", "pph21-ter", "lowongan-kerja"],
    "manufaktur": ["hitung-hpp", "arus-kas-13minggu", "rekap-penjualan-csv"],
    "produksi": ["hitung-hpp", "arus-kas-13minggu", "rekap-penjualan-csv"],
    "kesehatan": ["sop-writer", "surat-resmi", "notulen-rapat"],
    "klinik": ["sop-writer", "surat-resmi", "notulen-rapat"],
    "properti": ["surat-penawaran-harga", "follow-up-prospek", "proposal-kerjasama"],
}

PAKET_UMUM = ["rekap-penjualan-csv", "balas-chat-cs", "surat-resmi"]


def normalisasi(teks):
    teks = teks.lower().strip()
    teks = unicodedata.normalize("NFKD", teks)
    return teks


def cocokkan_tugas(tugas):
    t = normalisasi(tugas)
    for kata_kunci_list, skill in PEMETAAN:
        for kk in kata_kunci_list:
            if kk in t:
                return skill
    return None


def cocokkan_industri(industri):
    ind = normalisasi(industri)
    for kunci, paket in PAKET_INDUSTRI.items():
        if kunci in ind:
            return paket
    return None


def main():
    ap = argparse.ArgumentParser(description="Cocokkan jawaban wawancara ke rekomendasi skill")
    ap.add_argument("--tugas", action="append", default=[], help="Tugas yang menyita waktu (bisa diulang, maks. dipakai 3)")
    ap.add_argument("--industri", default="", help="Industri/peran pengguna")
    ap.add_argument("--json", action="store_true", help="Output JSON (default: teks)")
    args = ap.parse_args()

    if not args.tugas and not args.industri:
        print("Error: isi minimal --tugas atau --industri.", file=sys.stderr)
        sys.exit(1)

    rekomendasi = []
    tugas_tanpa_cocok = []
    dipakai = set()
    for tugas in args.tugas[:3]:
        skill = cocokkan_tugas(tugas)
        if skill and skill not in dipakai:
            rekomendasi.append({"tugas": tugas, "skill": skill})
            dipakai.add(skill)
        elif not skill:
            tugas_tanpa_cocok.append(tugas)

    paket_industri = cocokkan_industri(args.industri) if args.industri else None
    if not rekomendasi:
        # Tidak ada tugas yang cocok kata kunci: pakai paket industri, lalu paket umum.
        fallback = paket_industri or PAKET_UMUM
        for skill in fallback:
            rekomendasi.append({"tugas": None, "skill": skill})

    hasil = {
        "rekomendasi": rekomendasi[:3],
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
