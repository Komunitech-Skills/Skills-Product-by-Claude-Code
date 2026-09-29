# Beta Gelombang 1 — Daftar Skill Unggulan (usulan 2026-09-29)

Dasar: `docs/uji-platform.md` (uji platform asli oleh tim) → `docs/program-beta.md` (5–10 member VIP, ±7 hari).
Status di `catalog.csv` baru boleh naik ke `beta` **setelah** uji platform asli lulus (`examples/UJI-PLATFORM.md`).

## Kriteria pemilihan
1. Skor uji internal ≥ 8, tanpa temuan sedang/tinggi yang terbuka.
2. **Tanpa instalasi software pihak ketiga** (cukup Python bawaan) — cocok untuk pembeli awam.
3. Pekerjaan harian/mingguan yang nyata, sehingga bisa dipakai ≥ 3 kali dalam 7 hari.
4. Mewakili 4 paket solusi VIP: toko online, usaha offline, konsultan, klinik.
5. Nilai jual tinggi (ecer Rp 99rb–199rb atau VIP).

## Gelombang 1 — 10 skill

| # | Skill | Skor | Harga usulan | Target beta tester | Tugas nyata selama 7 hari |
|---|---|---|---|---|---|
| 1 | `kasir-lokal` | 9 | Rp 199.000 | Warung/kafe/toko kelontong | Catat penjualan harian, tutup kasir tiap malam |
| 2 | `gaji-umkm` | 9 | Rp 199.000 | Usaha dengan 2–15 karyawan | Hitung gaji + BPJS + PPh 21 satu bulan, cetak slip |
| 3 | `kas-umkm` | 8 | Rp 99.000 | Warung/bengkel/laundry | Buku kas harian + impor mutasi bank, rekap mingguan |
| 4 | `hitung-hpp` | 9 | Rp 99.000 | Produsen makanan/minuman, seller | Hitung HPP 3 produk + harga jual |
| 5 | `riset-harga-kompetitor` | 8 | Rp 99.000 | Seller marketplace | Bandingkan harga 1 produk vs 5–10 pesaing |
| 6 | `laporan-harian-usaha` | 9 | VIP | Pemilik toko/usaha offline | Laporan harian otomatis ke Telegram 21.00 |
| 7 | `crm-wa` | 9 | Rp 149.000 | Sales/reseller/jasa | Catat prospek & jadwal follow-up harian |
| 8 | `pph21-ter` | 9 | Rp 149.000 | Admin keuangan/HR | Hitung PPh 21 TER karyawan 1 bulan |
| 9 | `laporan-klien-konsultan` | 9 | Rp 99.000 | Konsultan/agensi/freelancer | Draf laporan progres mingguan ke klien |
| 10 | `pengingat-pasien-klinik` | 9 | Rp 99.000 | Klinik/praktik mandiri | Buku jadwal kontrol + draf pengingat WA |

**Komposisi beta tester yang disarankan (5–10 orang):** 2 toko online, 3 usaha offline, 2 konsultan/freelancer, 1–2 klinik; campur OpenClaw (mayoritas) + minimal 1 Claude Code/Cursor/Codex; campur Windows & Mac.

## Cadangan / Gelombang 2 (butuh instalasi software lokal — uji setelah gelombang 1)
`frappe-books-usaha`, `hledger-usaha`, `dolibarr-usaha`, `vikunja-tugas`, `pantau-website-toko`, `notebook-riset-lokal`, `pdf-lokal` — butuh panduan instalasi dicoba langsung oleh tim di Windows/Mac dulu.

## Langkah
1. **Tim/pemilik: uji platform asli** tiap skill (±10 menit) sesuai `docs/uji-platform.md`, minimal OpenClaw; catat di `skills/<nama>/examples/UJI-PLATFORM.md`.
2. Yang lulus → Akun B ubah status `beta` di `catalog.csv` + tambahkan platform ke `platform_teruji`.
3. Buat paket per tester: `python3 scripts/build.py --pembeli "Beta - <nama>" --skill <nama> --beta` (hasil di `dist/`, jangan di-commit; catat kode lisensi di sistem penjualan).
4. Kirim formulir masukan (`docs/program-beta.md`) di hari ke-7; rangkum anonim di `skills/<nama>/examples/MASUKAN-BETA.md`.
5. Kriteria `rilis`: ≥ 80% instal tanpa bantuan, rata-rata kegunaan ≥ 4, tidak ada laporan hasil salah yang belum diperbaiki.

## Catatan risiko
- Skill hitungan (gaji, PPh 21, kas) memakai aturan per 2026 dan pembulatan belum dicocokkan dengan Coretax — sampaikan ke tester: hasil diperiksa dulu sebelum dipakai untuk setor/lapor.
- `pengingat-pasien-klinik`: data minimal, tanpa diagnosis; pengingat berupa draf yang dikirim staf (keputusan pemilik).
- `laporan-harian-usaha`: kirim ke Telegram (bot resmi), bukan WhatsApp.
