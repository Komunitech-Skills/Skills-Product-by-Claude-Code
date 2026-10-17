# SOP Usaha Jadi Cepat, Lengkap dengan Checklist Berparaf

**Ceritakan cara kerja Anda, dapat SOP (Standar Operasional Prosedur: panduan langkah kerja tertulis) lengkap dan checklist harian yang siap dicetak dan ditempel.**

*Diuji AI penguji independen: 7,0 → 8,5 dari 10 (SOP lengkap langsung tampil di chat dan siap cetak, bukan disimpan diam-diam ke file).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Langkah kerja bernomor dengan bahasa super sederhana, mudah dipahami karyawan baru di hari pertama
- ✅ Checklist harian siap cetak dengan kolom centang Senin–Minggu dan paraf
- ✅ Ada panduan "Jika terjadi masalah", jadi karyawan tahu harus berbuat apa dan lapor ke siapa
- ✅ Indikator keberhasilan yang terukur, misalnya "0 salah kirim per minggu"
- ✅ Versi dan riwayat revisi tercatat, sehingga SOP mudah diperbarui

## Cocok untuk siapa
- Pemilik toko, minimarket, kafe, warung makan, dan online shop yang mulai punya karyawan
- Usaha yang membuka cabang baru dan ingin standar kerjanya sama
- Supervisor yang lelah menjelaskan hal yang sama berulang kali

## Contoh sebelum & sesudah
**Sebelum:** Cara closing kasir hanya diajarkan lisan. Selisih uang baru ketahuan di akhir bulan, dan tidak jelas siapa yang bertanggung jawab.

**Sesudah (cukup ketik):** "Bikinin SOP closing kasir buat laundry kiloan aku, Laundry Bersih Wangi di Yogyakarta ... pembayaran ada tunai sama QRIS. Modal laci tiap hari Rp200.000 ..." Cuplikan jawaban asli dari uji pertama di OpenClaw, 1 Okt 2026 (`examples/00-openclaw-sebelum-sesudah.md`; hasil lengkap juga memuat tujuan, penanggung jawab, indikator keberhasilan, dan checklist harian siap cetak):
```
# SOP: Closing Kasir Harian
...
### B. Hitung & Cocokkan Transaksi
6. Hitung uang tunai di laci per pecahan, dari lembar besar ke kecil.
7. Sisihkan modal awal laci Rp200.000 dari total tunai di laci.
8. ⚠️ Bandingkan sisa tunai dengan "Penjualan Tunai" di aplikasi. (Selisih harus ketahuan malam itu juga, bukan besok setelah lupa kejadiannya.)
9. Cocokkan mutasi QRIS di HP dengan "Penjualan QRIS" di aplikasi kasir.
...
## 6. Jika terjadi masalah
| Jika... | Maka... | Lapor ke |
|---|---|---|
| Selisih tunai lebih dari Rp10.000 (usulan) | Hitung ulang, cek foto & laporan aplikasi, tanya kasir | Pemilik, besok pagi |
| Listrik padam saat closing | Hitung manual dengan kalkulator, catat di kertas dulu, pindahkan ke aplikasi setelah listrik nyala | Pemilik |
...
```

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Buat SOP packing pesanan Shopee untuk olshop baju saya"
- "SOP buka toko jam 8 pagi, lengkap checklist-nya"
- "SOP handling komplain pelanggan untuk warung makan"
- "Perbarui SOP ini ke versi 1.1, tambahkan langkah foto paket"

## Instalasi singkat
Salin folder `sop-writer` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

**Hasil uji (angka nyata):**
- **Uji OpenClaw, 1 Oktober 2026** (penguji AI independen; angka dari `examples/00-openclaw-sebelum-sesudah.md`): rata-rata nilai 7,0 tanpa skill menjadi 8,5 dengan skill (skala 10); uji ulang v1.0.4 untuk SOP closing kasir laundry: 6,5 tanpa skill menjadi 8,5 sampai 9 dengan skill. Pembeda: SOP lengkap langsung tampil di chat dan siap cetak (kontrol dokumen, langkah kritis ⚠️ beserta alasannya, tabel "jika … maka …", indikator, checklist berparaf), sedangkan tanpa skill SOP ditulis ke file dan tidak tampil di chat.
- Jujur: untuk aturan dapur yang berisiko, AI biasa sudah menolak praktik berbahaya. Satu penyebutan izin PIRT yang kurang tepat tercatat pada uji; bila SOP dipakai untuk perizinan, cocokkan dengan ketentuan resmi.

**Status uji (jujur):** diuji di OpenClaw (uji otomatis agent) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama).

## Bukti uji di bot Telegram

Diuji di bot Telegram OpenClaw yang asli (grup uji internal Komunitech) pada 17 Oktober 2026, versi 1.0.6, dengan permintaan SOP packing pesanan untuk online shop skincare (sekitar 150 paket per hari dari Shopee dan TikTok Shop, 2 staf packing, dicek admin). Skor kami (skala 10), tanpa skill → dengan skill: **7** → **8,5**, selisih +1,5, **lulus acuan kami**, tepat di batas (artinya skor dengan skill minimal 8 dan selisih minimal 1,5 poin).

Dengan skill, SOP lengkap tampil utuh di chat dalam format baku: langkah kritis ditandai, ada daftar "jika terjadi masalah", target ukur, checklist harian dengan paraf, dan riwayat revisi. Tanpa skill, isinya berupa daftar tips yang praktis, tetapi bukan dokumen SOP resmi.

Catatan jujur: ada beberapa asumsi kecil yang belum ditandai (serum dianggap botol kaca, batas waktu 14.45), ide praktis pencegah salah varian seperti stiker warna per ukuran justru muncul di versi tanpa skill, dan SOP tampil dalam 3 pesan berurutan. Uji sebelumnya: 16 Oktober 2026 (versi 1.0.5), tanpa skill **7** → dengan skill **3**, belum lulus acuan kami karena SOP lengkap tidak sampai ke pembeli (hanya ringkasan); itu diperbaiki di versi 1.0.6.

## FAQ
**Saya belum punya cara kerja yang baku. Tetap bisa?**
Bisa. Skill memakai praktik umum untuk jenis usaha Anda dan menandai langkah yang perlu Anda sesuaikan.

**Bisa dibuat versi poster untuk ditempel?**
Bisa. Minta "versi poster", nanti dibuat 5–7 langkah inti dengan huruf besar.

**Apakah SOP ini cukup untuk sertifikasi (halal, SLHS/sertifikat laik higiene sanitasi, PIRT/izin produksi rumahan, ISO)?**
Belum. SOP ini untuk operasional harian. Untuk sertifikasi, ikuti ketentuan resmi dan konsultasikan ke petugas atau pendamping sertifikasi.

## Riwayat perubahan

Versi terkini: **1.0.6**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
