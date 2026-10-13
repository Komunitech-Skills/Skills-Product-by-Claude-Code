# Atribusi

## Jalur produksi
**Kurasi (ATM = Amati, Tiru, Modifikasi).** Skill ini mengadaptasi struktur alur empat skill keuangan pribadi berlisensi MIT, lalu ditulis ulang total untuk keluarga/pekerja Indonesia dan dilengkapi script hitung teruji (lihat "Apa yang diubah/ditambahkan").

## Sumber yang diadaptasi
- **Repo:** [openaccountant/skills](https://github.com/openaccountant/skills)
- **Skill sumber:** `personal/debt-payoff`, `personal/zero-based-budget`, `personal/emergency-fund`, `personal/financial-goals`
- **Pembuat:** Open Accountant
- **Lisensi:** MIT — "Copyright (c) 2026 Open Accountant" (dibaca langsung via `git show HEAD:LICENSE`; teks lengkap di `LICENSE-MIT` folder ini, disalin tanpa perubahan)
- **Commit yang dipakai:** `f5abe381f24b5b7d59f1d0b4a825b14494ff2034` (Thu Apr 9 11:03:51 2026 -0400), diperoleh 2026-09-26 lewat `git clone --depth 1 --filter=blob:none --sparse` + `git sparse-checkout set personal/debt-payoff personal/zero-based-budget personal/emergency-fund personal/financial-goals`.
- **Bagian yang dipelajari:** keempat `SKILL.md` di atas (total 257 baris) — alur Avalanche/Snowball dan rumus amortisasi bulanan, konsep zero-based ("setiap dolar diberi tugas") dan patokan 50/30/20, target dana darurat berbasis pengeluaran esensial, serta rumus tabungan bulanan per target.
- **Bagian yang TIDAK dipakai:** seluruh langkah "Wilson Tools" (`transaction_search`, `spending_summary` — alat proprietary milik Open Accountant, butuh akun), rujukan aplikasi/bank AS (YNAB, EveryDollar, Ally, Capital One, NerdWallet, unbury.me), angka dolar & APY AS, dan skill lain di repo tersebut.

## Catatan jujur tentang bukti sumber (Tahap 2 CLAUDE.md)
Sumber ini **tidak memenuhi 3 sinyal bukti penuh**: ±75★/16 fork (di bawah ambang), commit terakhir 2026-04-09 (stagnan ±5 bulan), belum terlihat issue/PR aktif dari komunitas. Yang terpenuhi hanya umur (>3 bulan) dan kualitas isi (rumus benar secara matematis). Hal ini dicatat di catatan riset internal kurator (tidak disertakan dalam paket) sebagai **PERLU REVIEW**, dan **pemilik Komunitech menyetujui pemakaiannya pada 2026-09-26** karena isinya berkualitas dan kategori keuangan pribadi masih kosong — bukan karena sumbernya sangat terbukti. Karena itu nilai skill ini bertumpu pada hitungan & lokalisasi yang kami tulis dan uji sendiri, bukan pada popularitas sumber.

## Audit lisensi & keamanan (Tahap 2–3)
- `LICENSE` root repo sumber dibaca langsung: MIT — mengizinkan modifikasi & penjualan turunan dengan menyertakan pemberitahuan hak cipta dan izin.
- Keempat `SKILL.md` dibaca penuh. Tidak ada script di folder sumber (murni Markdown); tidak ada yang dijalankan.
- `grep` pola mencurigakan (curl, wget, ignore, rm -rf, sudo, eval, base64, http) di seluruh folder hasil sparse-checkout → **nihil**. Tidak ada perintah destruktif, pengiriman data ke luar, permintaan kredensial, instruksi tersembunyi, API key, atau data pribadi.
- Kesimpulan: **lolos audit**.

## Apa yang diubah/ditambahkan (nilai tambah ATM)
1. **Empat skill digabung jadi satu alur keluarga** (anggaran → dana darurat → utang → target) dengan urutan prioritas yang jelas.
2. **Lokalisasi penuh Indonesia:** Rupiah & parsing "1,5jt/750rb/Rp1.500.000"; pos kiriman orang tua, arisan, zakat/perpuluhan/sedekah/dana punia (opsional, tanpa fatwa), kondangan; THR/bonus/gaji ke-13 dibagi 12; e-wallet GoPay/OVO/DANA (top-up bukan pengeluaran); pola realistis 60/20/20 dst. untuk keluarga bertanggungan.
3. **Dana darurat 3–12 bulan per status** (PNS, lajang, menikah, punya anak, pekerja lepas) — sumber hanya 3–6 bulan ala AS.
4. **Utang khas Indonesia:** kartu kredit, KTA, paylater, pinjol legal, leasing; **konversi bunga flat → efektif** (tidak ada di sumber); bunga per hari/bulan/tahun; peringatan batas bunga BI (kartu kredit 1,75%/bulan) & OJK (pinjol konsumtif 0,1%/hari 2026); cek legalitas OJK (situs, 157, WA 081-157-157-157); peringatan gali lubang tutup lubang; deteksi cicilan minimum ≤ bunga (utang tak akan lunas).
5. **Target Indonesia** (DP rumah, pendidikan anak, haji/umrah, pensiun) dengan inflasi & imbal hasil sebagai **asumsi eksplisit**, tanpa rekomendasi produk — sumber memakai pembagian sederhana tanpa inflasi.
6. **Script `scripts/keuangan.py`** (Python standar, Decimal) + **tes regresi `tests/uji_regresi.py`** yang memverifikasi hitungan dengan implementasi Fraction independen (termasuk 40 kasus utang acak) dan memastikan input buruk tidak menghasilkan traceback — sumber tidak punya script sama sekali.
7. Rumus manual lengkap (`references/rumus-manual.md`) agar skill tetap berguna tanpa script; template anggaran & daftar utang; disclaimer bukan nasihat keuangan; batas cakupan terhadap skill usaha di katalog Komunitech.

## Pembagian lisensi bagian ini
- **Alur/struktur yang diadaptasi** (konsep Avalanche/Snowball, zero-based + 50/30/20, dana darurat berbasis pengeluaran esensial, tabungan bulanan per target) di `SKILL.md` dan `references/rumus-manual.md`: turunan dari materi MIT `openaccountant/skills` — tunduk pada ketentuan MIT (lihat `LICENSE-MIT`), sudah ditulis ulang total dalam bahasa Indonesia.
- **Semua bagian lain** — `scripts/`, `tests/`, `references/utang-dan-pinjol.md`, `references/pos-anggaran-indonesia.md`, `templates/`, `examples/`, `README.md` — karya orisinal Komunitech, tidak mengandung materi pihak ketiga.

Penggunaan tunduk pada `LISENSI.txt` dalam paket pembelian, ditambah ketentuan MIT pada bagian yang disebut di atas.

## Riwayat versi
### v1.0.1 (2026-09-26) — revisi dari HASIL-UJI (skor 8), status `draft`
- T-1: satuan bunga wajib jelas. `konversi-flat --bunga-flat` menerima `0,9%/bln`, `10,8%/thn`, `0,9% per bulan` dan opsi `--per bulan|tahun`; angka tanpa satuan < 3 → dua tafsiran + PERINGATAN (tidak lagi diam-diam dibaca per tahun); ≥ 3 → dianggap per tahun dengan catatan. `utang` konsisten: bunga tanpa satuan < 3 ditolak dengan pertanyaan satuan, `--per` tersedia, ≥ 3 diberi peringatan. Efektif 4 desimal untuk disalin ke `utang`.
- T-2: nominal gaji/saldo/pokok/biaya < Rp10.000 (mis. "1.500") → bagian PERINGATAN INPUT.
- T-5: `target --kemampuan` menampilkan bulan ke berapa target tercapai (atau tidak tercapai dalam 60 tahun).
- T-6: catatan take over/refinancing/konsolidasi (bandingkan total bunga sisa vs baru + provisi/admin/penalti) di keluaran `utang`, SKILL.md, dan references — tanpa rekomendasi produk.
- T-8: asumsi minimum kartu kredit tetap disebut di Batasan.
- Angka lama tidak berubah (skenario 02: 10 bulan, bunga Rp4.226.895). Tes regresi 33 → 50.

### v1.0.0 (2026-09-26) — rilis awal, status `draft`
Belum diuji penguji independen (Tahap 6). Tes regresi pembuat: lihat `tests/uji_regresi.py`.
