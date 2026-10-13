# Atribusi

## Jalur produksi
**Kurasi (ATM = Amati, Tiru, Modifikasi).** Skill ini mengadaptasi kerangka triase tiket dan eskalasi dari dua skill publik berlisensi Apache-2.0, ditulis ulang total dalam Bahasa Indonesia untuk penjual online, kafe, dan usaha jasa yang menerima keluhan lewat WhatsApp, marketplace (Shopee, Tokopedia, TikTok Shop), Instagram, dan ulasan Google/GoFood.

## Sumber yang diadaptasi
- **Repo:** [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) (pembuat: Anthropic)
- **Skill sumber:** `customer-support/skills/ticket-triage/SKILL.md` (nama skill sumber: `ticket-triage`; 275 baris) dan `customer-support/skills/customer-escalation/SKILL.md` (`customer-escalation`; 248 baris). Kedua folder hanya berisi `SKILL.md`, tanpa script.
- **Lisensi:** Apache License 2.0. Teks lengkap di `LICENSE-APACHE`, disalin dari `customer-support/LICENSE` repo sumber (diambil 2026-10-05; 202 baris, tanpa tambahan teks lain; pemegang hak cipta tidak disebut di repo sumber, bagian lampiran lisensi masih berupa placeholder).
- **NOTICE:** repo sumber **tidak memiliki berkas NOTICE** (`customer-support/NOTICE` mengembalikan 404, dicek 2026-10-05), jadi tidak ada NOTICE asli untuk diteruskan. Berkas `NOTICE` di folder ini milik Komunitech untuk karya turunan.
- **Cara pengambilan:** `raw.githubusercontent.com` dibaca pada 2026-10-05 (tanpa clone, tanpa menjalankan kode apa pun). SHA-256 `ticket-triage/SKILL.md` saat dibaca: `d0e5e95443e358ad2a74811b196071d10807ca95aa20351ab5760feeecee1294`; `customer-escalation/SKILL.md`: `90c33574a41371e8e116aaf40237141adcd6075ef8bcb9de993de2b543867b3e`.
- **Bagian yang dipelajari:** (1) alur membaca keluhan: inti masalah, gejala, konteks pelanggan, sinyal urgensi, keadaan emosi; (2) kategori berdasarkan **penyebab utama**, bukan gejala; (3) kerangka prioritas bertingkat dengan kriteria dan target waktu respons, serta pemicu menaikkan prioritas (menunggu melewati batas, banyak pelapor, pelanggan mengancam naik ke atasan, solusi sementara gagal, cakupan melebar); (4) saran "ragu pilih tingkat lebih tinggi"; (5) deteksi duplikat dan pola; (6) kerangka rute eskalasi (dari frontline, ke tim teknis, ke produk, ke keamanan, ke pimpinan) dan kapan ditangani sendiri versus dinaikkan; (7) isi ringkasan eskalasi (dampak, apa yang sudah dicoba, keputusan yang dibutuhkan, tenggat); (8) tahap kabar lanjutan dan penurunan eskalasi bila akar masalah sudah ketemu; (9) draf balasan awal per kategori.
- **Bagian yang TIDAK dipakai:** semua konektor (platform dukungan, basis pengetahuan, pelacak proyek, CRM, obrolan tim), empat tingkat prioritas P1-P4 dengan SLA korporat, kategori khusus perangkat lunak (SSO, API, integrasi, bug, data), rute tim engineering/produk/keamanan, templat langkah reproduksi bug, dan hitungan pendapatan berulang tahunan (ARR).

## Audit keamanan (Tahap 3 CLAUDE.md), 2026-10-05
- Dibaca penuh: kedua `SKILL.md` sumber dan `customer-support/LICENSE`. Tidak ada script dan tidak ada file pendukung di folder skill sumber. Tidak ada yang dijalankan.
- Diperiksa: perintah destruktif, pengiriman data ke server luar, pembacaan kredensial/SSH key/data browser, pengunduh-lalu-eksekusi otomatis, kode ter-obfuscate, instruksi tersembunyi (mengabaikan pengguna, mengirim file, menonaktifkan konfirmasi), API key/token tertanam, dan prompt injection. **Nihil.** Yang ada hanya penanda konektor (`~~support platform`, `~~CRM`) dan tawaran langkah lanjutan; keduanya tidak dibawa.
- Catatan: kedua frontmatter sumber memuat `argument-hint` (tidak dibawa; frontmatter di sini hanya `name` dan `description`). Bagian yang tidak dibawa tidak memengaruhi keamanan.
- Kesimpulan: **lolos audit**, aman diadaptasi.
- Lihat juga catatan riset internal kurator (tidak disertakan dalam paket) (bagian skill ini) di repo kurator.

## Pernyataan perubahan (Apache-2.0 bagian 4b: berkas telah diubah)
Materi asal **telah diubah** oleh Komunitech:
1. Diterjemahkan dan ditulis ulang total ke Bahasa Indonesia; seluruh pembungkus konektor, perintah `/ticket-triage`, dan orientasi tim dukungan perangkat lunak (SaaS) dibuang.
2. Tingkat prioritas dipangkas dari P1-P4 menjadi P1-P3 dengan aturan baru yang cocok untuk usaha kecil: ancaman lapor/ulasan buruk, keamanan, tenggat platform marketplace, nilai pesanan, dan pelanggan yang mengulang.
3. Kategori sumber (bug, how-to, fitur, tagihan, akun, integrasi, keamanan, data, kinerja) diganti kategori keluhan toko dan jasa: barang rusak/tidak sesuai, belum sampai/kurir, salah kirim/kurang, COD gagal/ditolak, komplain layanan, retur/refund, bukan keluhan. Prinsip "kategori menurut penyebab" dipertahankan.
4. Rute eskalasi diganti ke pemilik, ekspedisi, platform, pemasok, dan ahli hukum/BPSK.
5. Kanal diganti ke chat marketplace/WhatsApp/Instagram dan ulasan publik; balasan disiapkan untuk dikirim manusia satu per satu (mode copilot, tidak ada kirim otomatis).

## Nilai tambah Komunitech (karya orisinal)
1. Keluaran: daftar kerja berurutan, tindakan pertama, draf balasan WA/ulasan siap kirim per keluhan, daftar keputusan pemilik, dan rekap aman tanpa data pribadi (sumber hanya satu templat triase untuk satu tiket).
2. Aturan prioritas eksplisit untuk konteks lokal, termasuk tenggat platform marketplace dan batas "nilai besar" yang bisa disesuaikan (`references/dasar-hukum-dan-platform.md`, dicek 2026-10-05).
3. Dasar hukum Indonesia untuk keluhan konsumen (UU 8/1999 Pasal 4, 7, 8, 18, 19; BPSK; UU 27/2022) dan penanganan ulasan publik tanpa menekan pelanggan.
4. Larangan keras: menghapus/membungkam ulasan, imbalan agar mengganti bintang, memakai data pelanggan untuk akun lain, menuduh pelanggan, menjanjikan kompensasi sebelum pemilik memutuskan.
5. **Script baru `scripts/triase.py`** (Python standar; membaca CSV ekspor dengan nama kolom fleksibel, kategori dan prioritas berbasis kata kunci Indonesia, pola, penyamaran nomor HP/email) + 30 uji regresi (`tests/uji_regresi.py`).
6. Templat balasan, contoh kasus lokal (fiktif), README pembeli.

Bagian turunan (alur, kerangka kategori-prioritas-eskalasi di `SKILL.md` dan `references/kategori-dan-tindakan.md`) tunduk pada `LICENSE-APACHE`. Bagian orisinal (`scripts/`, `tests/`, `templates/`, `references/dasar-hukum-dan-platform.md`, `examples/`, `README.md`) adalah karya Komunitech dan tunduk pada `LISENSI.txt` paket pembelian.
