# 00 — Uji banding pesaing

Penguji: agent penguji independen (simulasi, Claude Code), 2026-09-24. Skill/produk pesaing hanya dibaca dari dokumentasi publik untuk dinilai; tidak ada kode pihak ketiga yang dijalankan atau disalin.

## 1. Pencarian skill agent sejenis (SKILL.md)
| Sumber | Kata kunci | Hasil |
|---|---|---|
| ClawHub (clawhub.ai/skills?q=pos) | pos, cashier, kasir, receipt | Tidak ada skill kasir/POS toko. |
| VoltAgent/awesome-openclaw-skills (README) | point of sale, pos, cashier, kasir, cash register, receipt | Tidak ada (satu hasil "Polygon PoS" = blockchain, tidak relevan). |
| VoltAgent/awesome-agent-skills (README) | idem | Tidak ada (hanya "chat … receipts" Azure). |
| Pencarian web GitHub "SKILL.md" + kasir/point of sale | idem | Hanya aplikasi POS biasa (bukan skill); `fdocr/clawshier` = pencatat foto struk belanja ke Google Sheets (pengeluaran, bukan kasir penjualan). |

**Kesimpulan:** tidak ditemukan pesaing sebanding dalam bentuk agent skill. Pembanding yang relevan adalah **aplikasi POS open-source lokal/self-host** dan **SaaS kasir Indonesia**.

## 2. Pembanding aplikasi POS open-source (dinilai dari dokumentasi resmi, tidak diinstal)
| | **kasir-lokal** (kita) | **OSPOS** — github.com/opensourcepos/opensourcepos | **Frappe Books** — github.com/frappe/books | **NexoPOS** — github.com/blair2004/NexoPOS |
|---|---|---|---|---|
| Lisensi | Proprietary Komunitech | MIT + wajib pertahankan footer | AGPL-3.0 | GPL-3.0 |
| Popularitas | baru | ±4,4k bintang | ±5k bintang | ±1,3k bintang |
| Instalasi untuk awam | Salin folder + Python 3 (tanpa server) | PHP 8.2 + MySQL/MariaDB + Apache (atau Docker) — berat untuk awam | Installer desktop (Win/Mac/Linux), SQLite lokal — mudah | PHP/Laravel + MySQL — berat |
| Cara pakai | Chat bahasa sehari-hari ("dua kopi susu, bayar qris") | Layar kasir web, klik/scan barcode | Aplikasi desktop, form | Layar kasir web |
| Bahasa Indonesia | Asli (istilah & angka lokal "100rb", "1,5jt") | Ada terjemahan | Ada terjemahan | Terbatas |
| Buka/tutup kasir + selisih | Ya | Ya (cash-up) | Tidak menonjol (fokus akuntansi) | Ya (register) |
| Struk thermal 58/80 | HTML siap cetak dari browser | Ya, + barcode | Tidak disebut di README | Ya |
| Diskon bertingkat, bayar campuran | Ya | Ya | Terbatas | Ya |
| Pajak Indonesia (PPN 12% DPP 11/12, pembulatan) | Ya, sesuai PMK 131/2024 | Pajak generik (%), perlu diatur manual; DPP nilai lain tidak ada | Pajak generik | Pajak generik |
| PBJT/PB1 restoran | **Belum** | Bisa diatur sebagai pajak % generik | Pajak % generik | Pajak % generik |
| Stok | Opsional / via skill buku-stok | Lengkap | Lengkap + akuntansi | Lengkap |
| Laporan | Rekap harian/bulanan/tahunan teks + CSV; omzet PPh final | Banyak laporan | Laporan akuntansi lengkap | Dasbor |
| Kecepatan antrean ramai | Lambat (konfirmasi tiap nota lewat chat) | Cepat (scan) | Sedang | Cepat |
| Dioperasikan AI agent / Telegram | **Ya (inti produk)** | Tidak | Tidak | Tidak (ada API) |

### Skenario 01 dijalankan "dengan instruksi pesaing"
Tidak dapat dijalankan secara jujur: pesaing adalah aplikasi GUI yang memerlukan instalasi server (OSPOS/NexoPOS) atau aplikasi desktop (Frappe Books), dan aturan repo melarang memasang dependensi dari sumber luar tanpa izin pemilik. Penilaian di bawah berbasis fitur terdokumentasi, bukan output nyata.

## 3. Penilaian berdampingan untuk UMKM awam Indonesia (1–10)
| Kriteria | kasir-lokal | OSPOS | Frappe Books | NexoPOS |
|---|:-:|:-:|:-:|:-:|
| Kemudahan mulai (awam) | 8 | 3 | 7 | 3 |
| Kesesuaian konteks Indonesia (bahasa, Rupiah, PPN 11/12, PPh final) | 9 | 5 | 5 | 4 |
| Akurasi hitung (terverifikasi di uji ini) | 10 | n/a | n/a | n/a |
| Kecepatan kasir ramai | 4 | 9 | 6 | 9 |
| Kelengkapan fitur POS | 6 | 9 | 7 | 9 |
| Siap pakai via chat/Telegram | 10 | 1 | 1 | 2 |
| **Kesan keseluruhan untuk target (warung/toko kecil, pemilik awam, dioperasikan agent)** | **8** | 5 | 6 | 5 |

Skill kita **tidak kalah** untuk target pasarnya (UMKM satu outlet yang ingin dioperasikan lewat chat); kalah jelas pada kecepatan antrean dan kelengkapan fitur POS klasik — hal ini sudah diakui jujur di README ("bukan kasir supermarket").

## 4. Dibanding SaaS Moka / Majoo (fitur dasar yang belum ada)
- **Pajak restoran PBJT/PB1** (mode tarif daerah, mis. 10%) + service charge — fitur standar kasir F&B di Indonesia. **Paling penting** karena kedai/kafe adalah target utama.
- Scan barcode / pencarian cepat produk di layar; mode antrean cepat tanpa konfirmasi per nota.
- Modifier/topping & varian harga (less sugar, extra shot +Rp 5.000), open bill / simpan pesanan meja, split bill.
- Laporan per kasir/shift dan hak akses karyawan (PIN kasir), laporan laba kotor (HPP) — kasir-lokal tidak menyimpan harga beli.
- Pelanggan/member & poin; struk dikirim otomatis ke WhatsApp/email.
- Aplikasi di HP/tablet & multi-outlet (sengaja di luar cakupan).
- Integrasi QRIS dinamis/EDC (sengaja di luar cakupan; hanya dicatat).

## 5. Yang bisa dipelajari (ide, bukan salinan)
1. Dari OSPOS/NexoPOS: konsep "register/cash-up" per shift dengan denominasi pecahan uang (hitung lembar 100rb/50rb/…) untuk membantu kasir menghitung uang fisik.
2. Dari SaaS F&B: mode pajak daerah + service charge dengan urutan hitung yang jelas di struk (Subtotal → Service → PB1).
3. Dari Frappe Books: laporan laba kotor dengan HPP per produk (bisa ditarik dari buku-stok yang sudah menyimpan harga beli).
4. Modifier sederhana ("+shot", "less sugar") sebagai item tambahan bernilai Rp 0/berbayar.

## Sumber
- https://github.com/opensourcepos/opensourcepos (MIT + footer, ±4,4k bintang, PHP 8.2 + MySQL)
- https://github.com/frappe/books (AGPL-3.0, ±5k bintang, Electron + SQLite, POS mode)
- https://github.com/blair2004/NexoPOS (GPL-3.0, ±1,3k bintang, Laravel)
- https://clawhub.ai/skills?q=pos ; https://github.com/VoltAgent/awesome-openclaw-skills ; https://github.com/VoltAgent/awesome-agent-skills ; https://github.com/fdocr/clawshier
</content>
</invoke>
