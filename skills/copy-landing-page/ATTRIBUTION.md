# Atribusi

## Jalur produksi
**Kurasi (ATM = Amati, Tiru, Modifikasi).** Skill ini mengadaptasi struktur & prinsip yang terbukti dari skill publik berlisensi MIT, dengan nilai tambah besar untuk pasar Indonesia (lihat bagian "Apa yang diubah/ditambahkan" di bawah).

## Sumber yang diadaptasi
- **Repo:** [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills)
- **Pembuat:** Corey Haines
- **Lisensi:** MIT (dicek langsung di file `LICENSE` repo sumber — lihat `LICENSE-MIT` di folder ini untuk teks lengkapnya)
- **Commit/snapshot yang dipakai:** hasil `git clone --depth 1` pada 2026-09-24 (branch default saat itu; commit sha tidak dicatat karena depth 1 tidak menyertakan riwayat penuh — snapshot README/VERSIONS.md repo menyebut versi skill v2.0.x)
- **Bagian yang dipelajari:** skill `skills/copywriting/SKILL.md`, `skills/cro/SKILL.md`, dan `skills/offers/SKILL.md` (kerangka halaman, prinsip benefit-over-feature, value equation, dan daftar larangan taktik manipulatif/scarcity palsu).
- **Bagian yang TIDAK dipakai:** skill lain di repo tersebut (mis. `pricing`, `signup`, `ads`, `social`) tidak relevan dengan cakupan `copy-landing-page` dan tidak diadaptasi.

## Audit lisensi & keamanan (pedoman kurasi Komunitech)
- File `LICENSE` di root repo sumber dicek langsung: MIT, Copyright (c) 2025 Corey Haines — mengizinkan modifikasi & penjualan turunan.
- Tidak ditemukan file `LICENSE` terpisah per-skill di dalam `skills/*/` — seluruh repo tunduk pada satu `LICENSE` MIT di root.
- Skill `copywriting`, `cro`, dan `offers` tidak memiliki folder `scripts/` — tidak ada kode yang dijalankan dari sumber ini.
- Isi `SKILL.md` ketiga skill tersebut dibaca penuh: tidak ditemukan perintah destruktif, pengiriman data ke server luar, permintaan kredensial/SSH key/data browser, `curl` yang dieksekusi otomatis, kode ter-obfuscate, atau instruksi tersembunyi yang menyuruh agent mengabaikan pengguna/menonaktifkan konfirmasi/mengirim file. Bagian lain repo (mis. `social/references/listening.md`, `public-relations/references/newsjacking.md`) memang berisi contoh perintah `curl` untuk riset publik, tetapi berada di luar cakupan skill ini dan tidak diadaptasi.
- Tidak ditemukan API key, token, atau data pribadi tertanam pada bagian yang diadaptasi.
- Kesimpulan: **lolos audit**, aman diadaptasi.

## Apa yang diubah/ditambahkan (nilai tambah ATM)
Sumber berbahasa Inggris dan generik-global; berikut penambahan besar yang membuat skill ini berbeda, bukan sekadar terjemahan:
1. **100% Bahasa Indonesia natural** dengan pilihan nada (santai/profesional/"bahasa ibu-ibu"), bukan hasil terjemahan mesin.
2. **CTA WhatsApp lokal**: pembuatan tautan `wa.me` dengan encoding pesan otomatis (script `scripts/bangun_tautan_wa.py`), bukan sekadar "tombol CTA" generik.
3. **Kebiasaan pembeli Indonesia**: COD/transfer/QRIS, ongkir, format testimoni dari pembeli lokal.
4. **Kepatuhan hukum Indonesia** (`references/dasar-hukum-klaim.md`): UU Perlindungan Konsumen No. 8/1999 (iklan menyesatkan), Peraturan BPOM No. 18/2024 & No. 27/2025 (klaim kosmetik/kesehatan/pangan), UU No. 33/2014 (sertifikasi halal wajib UMK per 18 Oktober 2026) — tidak ada di skill sumber sama sekali.
5. **Larangan tegas mengarang bukti sosial** (testimoni/rating/angka penjualan palsu) dengan mekanisme placeholder eksplisit.
6. **Ceklis klaim berisiko** yang wajib ditampilkan di setiap output.
7. **Output terstruktur untuk pembeli awam**: versi panjang + versi pendek link-in-bio, 3 variasi headline, meta title/description dengan panjang karakter dihitung persis lewat script (bukan diperkirakan), dan tautan WA siap pakai — sumber aslinya tidak punya format output baku seperti ini.
8. **Script Python teruji** (18 kasus uji, termasuk data rusak: nomor kosong, nomor bukan angka, kode negara asing, nomor kepanjangan) — sumber tidak menyertakan script sama sekali untuk skill ini.
9. **Contoh kasus lokal** (UMKM makanan) dan dokumentasi pembeli (README.md) — tidak ada di repo sumber (repo sumber adalah instruksi agent, bukan produk untuk dijual ke pembeli awam).

## Pembagian lisensi bagian ini
- **Teks kerangka umum yang diadaptasi** (urutan bagian halaman, prinsip benefit-over-feature, larangan taktik manipulatif) di `references/struktur-halaman.md`: turunan dari materi MIT `coreyhaines31/marketingskills` — tunduk pada ketentuan MIT (lihat `LICENSE-MIT`), sudah ditulis ulang dan dilokalkan penuh.
- **Semua bagian lain** — `SKILL.md`, `references/dasar-hukum-klaim.md`, `templates/`, `scripts/`, `examples/`, dan `README.md` — adalah karya orisinal Komunitech, tidak mengandung materi pihak ketiga, dan boleh diperlakukan sebagai proprietary Komunitech.

Penggunaan tunduk pada `LISENSI.txt` yang disertakan dalam paket pembelian, ditambah ketentuan MIT pada bagian yang disebut di atas.
