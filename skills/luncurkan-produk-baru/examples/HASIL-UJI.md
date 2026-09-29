# HASIL UJI - luncurkan-produk-baru v1.0.0

- Tanggal uji: 2026-09-29
- Penguji: agent independen (bukan pembuat), hanya membaca folder skill + CLAUDE.md
- Platform: `claude-code (simulasi agent)` - belum diuji di platform asli
- Berkas uji: `04-uji-skenario-normal.md`, `05-uji-input-kurang-luar-cakupan-data-rusak.md`, `00-pembanding-tanpa-skill.md`, `00-banding-pesaing.md` (contoh pembuat 01-03 dibiarkan)

## 1. Audit keamanan & format
| Butir | Temuan | Status |
|---|---|---|
| Frontmatter | hanya `name` + `description`; nama = folder; deskripsi satu baris, ID+EN | LULUS |
| Script | `jadwal_peluncuran.py` hanya `argparse, csv, io, json, sys, datetime`; tanpa jaringan, tanpa baca/tulis file, tanpa subprocess/eval | LULUS |
| Prompt injection / kredensial / data pribadi | tidak ditemukan; contoh memakai data fiktif | LULUS |
| Lisensi | MIT x2 (marketingskills, phuryn) + Apache-2.0 (product-on-purpose) disertakan di `licenses/`; ATTRIBUTION memuat atribusi, keterangan "file telah diubah", status NOTICE, dan "tidak berafiliasi" | LULUS |
| `scripts/__pycache__/` | ada di folder kerja, tetapi diabaikan git dan dikecualikan `build.py` | OK |
| Skill rujukan | semua skill yang dirujuk ada di repo; `strategi-harga-produk` ada foldernya tetapi belum di catalog.csv (SKILL sudah menulis "bila terpasang") | catatan |

## 2. Verifikasi independen
- **Daftar libur:** 25 tanggal 2026 dan 26 tanggal 2027 di script dicocokkan dengan pengumuman resmi SKB 3 Menteri di setneg.go.id (2026: ditetapkan 19 Sep 2025, 17 libur + 8 cuti; 2027: ditandatangani 15 Sep 2026, 18 libur + 8 cuti). **51/51 cocok.** Catatan "2027 PERLU REVIEW" di script/SKILL/README sekarang bisa dicabut.
  Sumber: https://setneg.go.id/baca/index/inilah_skb_3_menteri_libur_nasional_dan_cuti_bersama_2026 ; https://setneg.go.id/baca/index/inilah_skb_3_menteri_libur_nasional_dan_cuti_bersama_2027
- **Tanggal & pergeseran hari:** verifikator terpisah (daftar libur diketik ulang dari setneg, aturan geser ditulis ulang) dijalankan untuk SETIAP tanggal peluncuran 1 Jan 2026 - 31 Des 2027 (730 tanggal x 42 tugas): **0 selisih** tanggal maupun nama hari.
- **Angka skenario 1** (stok 20x1,3=26; titik pesan ulang 3x2,9=9; laba promo 13.500-8.500-1.080=3.920; diskon 20% -> 2.540) dihitung ulang dengan Python: cocok.
- `tests/uji_regresi.py`: 10 tes OK.

## 3. Vonis per skenario
| # | Skenario | Vonis | Catatan |
|---|---|---|---|
| 1 | Keripik tempe pedas, pangan, T0 Sab 7 Nov 2026 | LULUS | 8 bagian lengkap, 42 tugas benar; teks siap tempel kuat. Celah logika soft launch (bug B1) dan stok tanpa pre-order (B5) |
| 2 | Gamis linen, lintas tahun, Isra Mikraj 2027, libur tambahan | LULUS | geser 5 Jan 2027 -> 4 Jan, 10 Jan -> 8 Jan benar; catatan Natal/Tahun Baru/Imlek benar |
| 3 | Serum kosmetik, 12.12 | LULUS dengan catatan | peringatan 12.12 muncul; kosmetik tidak dapat tugas label/listing (B3) |
| 4 | Input tidak lengkap | LULUS | satu pesan 5 pertanyaan + jalan pintas default 35 hari |
| 5 | Di luar cakupan (SaaS/Product Hunt + valuasi) | LULUS | menolak sopan, arahkan ke profesional, tawarkan bagian relevan |
| - | Data rusak script | LULUS | semua tanggal rusak -> Galat kode 2; libur/tanggal kembar/waktu pendek terdeteksi (bila `--hari-ini` diberikan) |
| A/B | tanpa vs dengan skill | MENANG (33 vs 9 dari 35) | |
| Pesaing | launch (Corey Haines) & product-launch-strategy (Nexscope) | MENANG (37 vs 19 vs 14 dari 40) | |

## 4. Bug & kelemahan
- **B1 (sedang, logika jadwal):** "Tanya 10 pembeli soft launch" di T-7, padahal "Stok fisik sudah di tangan" baru T-2 dan tanggal kirim pre-order tidak diatur. Contoh pembuat 02 sendiri menulis soft launch "kirim mulai 12 Nov" (= T-2) sementara masukan diminta 7 Nov. Pembeli belum menerima barang saat ditanya.
- **B2 (sedang, kegunaan):** tanpa `--hari-ini`, script tidak memberi peringatan waktu <30 hari maupun tanggal lewat, dan perintah utama di SKILL.md langkah 5 tidak memakai `--hari-ini`. Agen yang mengikuti contoh bisa melewatkan peringatan terpenting.
- **B3 (sedang):** `--jenis kosmetik` hanya menambah 1 tugas; tugas label (T-28) dan cek foto listing = label/nomor notifikasi (T-3) hanya untuk pangan.
- **B4 (kecil):** peringatan "tahun tanpa data libur" hanya memeriksa tahun T0; T0 akhir Des 2027 menghasilkan tugas Jan 2028 tanpa peringatan.
- **B5 (kecil, rumus):** rumus stok (pesanan minggu 1 x 1,3) tidak menambahkan unit pre-order soft launch yang juga diambil dari stok; contoh 01 memakai 40 pre-order soft launch sebagai perkiraan minggu 1 sehingga maknanya rancu.
- **B6 (kecil):** peluncuran di sekitar Lebaran hanya dapat peringatan umum; tidak ada peringatan khusus musim mudik (ekspedisi/pemasok libur ±1 minggu, bahan naik).
- **B7 (kecil, tampilan md):** judul tanggal memakai label T tugas pertama; tugas hasil geser tampil di bawah label T yang salah (mis. bazar T-5 di bawah "(T-7)").
- **B8 (kecil):** deskripsi & README menyebut "jasa", tetapi tidak ada `--jenis jasa`; tugas stok/kemasan/uji kirim tidak relevan untuk jasa dan SKILL tidak menyuruh agen membuangnya.

## 5. Skor: **8/10 - LULUS**
Alasan: menang telak di A/B dan banding pesaing; script aman, stdlib, teruji, dan 100% akurat untuk 730 tanggal; data libur 2026-2027 cocok dengan SKB resmi; teks siap tempel, pagar etika WA (opt-in, STOP, tanpa blast), dan pengingat legal sesuai CLAUDE.md. Dikurangi karena celah logika soft launch (B1), peringatan waktu pendek yang bergantung pada flag opsional (B2), dan cakupan kosmetik/jasa yang tidak setara klaimnya (B3, B8).

## 6. Permintaan perbaikan (untuk pembuat)
1. B1: pindahkan tugas umpan balik soft launch ke setelah barang pre-order diterima (mis. tambah tugas "kirim pre-order soft launch" di T-10 hari kerja dan umpan balik di T-5), atau jadikan T-14 pre-order dengan barang yang sudah ada; selaraskan contoh 02.
2. B2: jadikan `--hari-ini` bawaan = `date.today()` (tetap bisa ditimpa), atau tambahkan `--hari-ini` pada perintah di SKILL.md langkah 5 dan contoh SKILL.
3. B3: berlakukan tugas label T-28 dan cek foto listing T-3 untuk `kosmetik` juga (teks disesuaikan: nomor notifikasi BPOM, klaim).
4. B4: periksa semua tahun dalam rentang T-30..T+30 untuk peringatan data libur.
5. B5: ubah rumus stok menjadi (pre-order soft launch + perkiraan pesanan minggu 1) x 1,3, atau jelaskan pemisahannya; perbaiki kalimat contoh 01.
6. B6: tambah peringatan bila T-7..T+7 bersinggungan dengan libur Idulfitri/cuti bersama Lebaran.
7. B7: tampilkan label T per baris tugas (atau per kelompok) di keluaran md.
8. B8: tambahkan `--jenis jasa` (buang tugas stok/kemasan/uji kirim) atau instruksikan agen membuang tugas yang tidak relevan untuk jasa.
9. Cabut label "PERLU REVIEW" data libur 2027 (sudah cocok dengan setneg.go.id per 2026-09-29).
10. (Opsional, pelajaran dari pesaing, tulis ulang sendiri) bedakan skala peluncuran: produk baru vs varian/rasa baru, dengan versi jadwal ringkas untuk varian.

Setelah perbaikan B1-B3, uji ulang oleh penguji independen.
