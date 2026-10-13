# Uji OpenClaw SEBELUM vs SESUDAH: kas-umkm

**Sumber (ada di paket VIP):** `solusi-vip/usaha-offline/UJI-OPENCLAW.md` (tabel skor skenario 04, bagian "Cacat per skill" dan "Uji ulang 2026-10-01 (keuangan)") dengan rincian per skenario di `solusi-vip/usaha-offline/uji-openclaw/04-rekap-kas-harian.md` dan `04-rekap-kas-harian-ulang.md`.
**Tanggal uji:** 2026-10-01 (Asia/Jakarta).
**Versi skill saat uji:** uji pertama kira-kira 1.0.10 (disimpulkan dari riwayat `catalog.csv` sebelum perbaikan pasca-uji; berkas sumber tidak menyebut versi), uji ulang = 1.0.11. Versi di katalog saat ini: 1.0.12.
**Penguji (agent):** agent penguji independen (bukan pembuat skill); uji ulang oleh penguji independen lain.

> Berkas ini ringkasan yang disalin dari catatan uji solusi VIP Usaha Offline (uji dilakukan per solusi, bukan per skill). Angka disalin apa adanya dari sumber.

## Cara uji
- OpenClaw lokal (`openclaw agent --local`, satu giliran per panggilan, tanpa Telegram/gateway). Model: router Komunitech `ninerouter/komunitech` (dilayani `claude-sonnet-5`), sama dengan bot member.
- **SEBELUM** = home OpenClaw tanpa skill. **SESUDAH** = home berisi paket skill usaha-offline (24 skill, termasuk `kas-umkm`). Pesan identik; file fiktif `catatan-kas-1okt.txt` disalin identik ke kedua workspace.
- Uji ulang hanya mengulang sisi SESUDAH; skor SEBELUM dipakai ulang dari uji pertama. Angka dihitung ulang penguji dengan Python.

**Pesan member (skenario 04):** "Ini catatan kas warung hari ini ada di file catatan-kas-1okt.txt. Tolong rekap: pemasukan, pengeluaran, untung hari ini berapa, dan uang di laci harusnya berapa? Kok kayaknya kurang ya"

## Skor

| Skenario | Versi skill | Skor tanpa skill | Skor dengan skill | Pembeda (satu kalimat) |
|---|---|:-:|:-:|---|
| 04 Rekap kas harian dan selisih laci dari file catatan, uji pertama | ±1.0.10 | 9 | 9 | Skill tidak terpicu (hanya ditawarkan di akhir jawaban), kedua sisi menghitung sendiri dengan benar (pemasukan Rp3.825.000, beban Rp958.500, laba kas Rp2.866.500, laci seharusnya Rp2.581.500, kurang Rp1.500) sehingga tidak ada pembeda. |
| 04, uji ulang (hanya sisi SESUDAH) | 1.0.11 | 9 (dari uji pertama) | 9 | Skill kini terpakai (rekap per baris, asumsi "laba kas sehari, belum laba akuntansi" disebut, tawaran simpan ke buku kas permanen) dengan angka yang sama. |
| **Rata-rata skenario ini** (skenario tunggal) | | **9** | **9** (uji pertama dan uji ulang) | Selisih 0 pada kedua putaran. |

Rata-rata seluruh solusi usaha-offline (5 skenario, skill berbeda) di uji pertama: 7,8 → 7,8. Itu skor solusi, bukan skor skill ini.

## Verdik
**LULUS uji ulang (skor 9, 1.0.11), tanpa selisih skor terhadap model tanpa skill pada skenario ini.**

## Catatan jujur
- Tidak ada pembeda skor yang terukur: untuk rekap sekali-jalan dari file teks, model tanpa skill sudah benar semua (termasuk memisahkan kasbon dan prive dari beban, serta QRIS dan listrik transfer dari laci). Sumber menyatakan paket skill tidak memberi nilai tambah di rekap sekali-jalan.
- Nilai utama `kas-umkm` (buku kas tersimpan, saldo per akun, opname laci, laporan terjadwal) tidak diuji di skenario ini karena agent tidak memakai skill pada uji pertama; setelah uji pertama skill diperbaiki (sumber menyarankan kata pemicu di `description` dan alur impor catatan harian), dan pada uji ulang skill terpakai.
- Kedua sisi menjalankan `find /` ke seluruh disk pada uji pertama; pada uji ulang tidak terlihat dari daftar alat, tetapi argumen tool call tidak dapat diaudit.
- Versi 1.0.12 (kategori "operasional", 2 Okt 2026) berasal dari uji gabungan paket kantor-manajemen (catatan internal kurator, tidak disertakan dalam paket, bagian 12), bukan dari skenario ini.
- Satu skenario saja.
