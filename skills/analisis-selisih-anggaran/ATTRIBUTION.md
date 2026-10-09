# Atribusi

## Jalur produksi
**Kurasi (ATM = Amati, Tiru, Modifikasi).** Skill ini mengambil kerangka jenis selisih dan alur analisis dari skill publik berlisensi Apache-2.0, lalu ditulis ulang total dalam Bahasa Indonesia untuk UMKM (Rupiah, pos usaha kecil) dengan script hitung baru.

## Sumber yang diadaptasi
- **Repo:** [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) (pembuat: Anthropic)
- **Skill sumber:** `finance/skills/variance-analysis/SKILL.md` (nama skill sumber: `variance-analysis`; 266 baris; tanpa script/file pendukung). URL: https://github.com/anthropics/knowledge-work-plugins/tree/main/finance/skills/variance-analysis
- **Lisensi:** Apache License 2.0. Teks lengkap di `LICENSE-APACHE`, disalin dari `finance/LICENSE` repo sumber (202 baris, bersih; SHA-256 `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`, diambil 2026-10-05). Pemegang hak cipta tidak disebut (lampiran lisensi masih placeholder `[yyyy] [name of copyright owner]`).
- **NOTICE:** repo sumber **tidak memiliki berkas NOTICE** (`finance/NOTICE` dan `NOTICE` di root: 404, dicek 2026-10-05). Berkas `NOTICE` di folder ini milik Komunitech untuk karya turunan.
- **Cara pengambilan:** `raw.githubusercontent.com` dibaca 2026-10-05 (tanpa clone, tanpa menjalankan kode). SHA-256 `SKILL.md` sumber: `467db7de3fb118550d013409254e2d4a9f87385a661e154655bf3431919b0ba1`.
- **Bagian yang dipelajari (kerangka):** jenis pemecahan selisih (harga/volume, bauran, jumlah orang/tarif untuk biaya tenaga kerja, pengelompokan biaya); ambang materialitas "rupiah atau persen, salah satu terlampaui"; urutan prioritas pemeriksaan (rupiah terbesar, persen terbesar, arah tak terduga, selisih baru, selisih berulang); ciri penjelasan selisih yang baik dan pola yang harus dihindari; jembatan (waterfall) dari angka rencana ke realisasi dengan syarat jumlahnya cocok.
- **Bagian yang TIDAK dipakai:** perbandingan anggaran-forecast-realisasi tiga arah dan akurasi forecast (MAPE), tren varians, ambang 10/15/20% gaya korporat, contoh dolar/ARR/SaaS (churn, ekspansi, FX), dan field frontmatter `argument-hint`.

## Audit keamanan (Tahap 3 CLAUDE.md), 2026-10-05
- Dibaca penuh: `SKILL.md` sumber (266 baris) dan `finance/LICENSE`. Folder skill sumber tidak berisi script; tidak ada yang dijalankan.
- Diperiksa (manual + pencarian pola curl/wget/eval/base64/rm/ssh/token/api key/password/secret/ignore): perintah destruktif, pengiriman data ke luar, pembacaan kredensial, kode ter-obfuscate, instruksi tersembunyi/prompt injection, API key tertanam. **Nihil.** Sumber memuat disclaimer "bukan nasihat keuangan, perlu ditinjau profesional" — semangatnya dipertahankan.
- Kesimpulan: **lolos audit**. Catatan lengkap: `research/sources/knowledge-work-plugins-2026-10-05.md` (bagian skill ini) di repo kurator.

## Pernyataan perubahan (Apache-2.0 bagian 4b: berkas telah diubah)
Materi asal **telah diubah** oleh Komunitech:
1. Ditulis ulang total ke Bahasa Indonesia untuk pemilik UMKM; istilah "favorable/unfavorable" menjadi menguntungkan/merugikan dengan aturan arah pendapatan vs biaya yang eksplisit.
2. Ambang materialitas diganti default UMKM (Rp500.000 atau 5%, bisa diubah, opsi "keduanya").
3. Pemecahan harga/volume/bauran diformulasikan ulang memakai harga rata-rata = nilai ÷ unit, dengan komponen sisa sehingga jumlahnya selalu persis sama dengan total selisih; pemecahan tenaga kerja disederhanakan menjadi efek jumlah (orang/jam) vs tarif.
4. Narasi selisih diubah menjadi rekap 1 layar, tabel 3 kolom, daftar pemeriksaan berbentuk pertanyaan, tindakan, dan pesan WA/Telegram ke tim.

## Nilai tambah Komunitech (karya orisinal)
1. **Script baru `scripts/selisih.py`** (Decimal, Python standar): membaca tabel tempel/markdown/CSV `;`/`,`/tab/ekspor Excel, angka gaya Indonesia (`4,5jt`, `Rp 4.500.000`) maupun Inggris (`45,000,000`), menebak jenis pos, melewati baris total/laba lalu mencocokkannya, penyesuaian biaya variabel terhadap volume penjualan (anggaran fleksibel), ranking material, jembatan laba, penanganan data rusak (kode 2 + saran). 53 uji regresi (`tests/uji_selisih.py`) dengan angka pembanding dihitung terpisah.
2. Daftar pemeriksaan penyebab per pos UMKM (penjualan, HPP, gaji/lembur, sewa, listrik, iklan, ongkir, komisi marketplace/ojol, kemasan) dalam bentuk pertanyaan, bukan tuduhan (`references/rumus-dan-pemeriksaan.md`).
3. Pola penolakan memoles/mengubah/menggeser angka realisasi untuk investor/bank, tetap disertai analisis jujur.
4. Contoh kasus lokal fiktif (kafe, toko hijab online, jasa kebersihan, laundry) dan README pembeli.

Bagian turunan (kerangka jenis selisih, ambang, urutan prioritas di `SKILL.md` dan `references/rumus-dan-pemeriksaan.md` bagian 1) tunduk pada `LICENSE-APACHE`. Bagian orisinal (`scripts/`, `tests/`, `examples/`, `references/rumus-dan-pemeriksaan.md` bagian 2-3, `README.md`) adalah karya Komunitech dan tunduk pada `LISENSI.txt` paket pembelian.
