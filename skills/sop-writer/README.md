# SOP Usaha Jadi dalam Menit, Karyawan Langsung Paham

**Ceritakan cara kerjamu, dapat SOP lengkap dan checklist harian yang siap dicetak dan ditempel.**

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

**Sesudah (cukup ketik):** "Bikinin SOP closing kasir minimarket saya, 2 shift, ada QRIS dan tunai"
→ SOP 13 langkah (siapkan, hitung, serah terima), tabel penanganan selisih kas, indikator keberhasilan, dan checklist per shift siap cetak.

**Hasil uji (OpenClaw, uji otomatis agent, 2026-10-01):** rata-rata nilai 7,0 tanpa skill menjadi 8,5 dengan skill (skala 10); uji ulang v1.0.4 untuk SOP closing kasir laundry: 6,5 tanpa skill menjadi 8,5 sampai 9 dengan skill. Pembeda: SOP lengkap langsung tampil di chat dan siap cetak (kontrol dokumen, langkah kritis ⚠️ beserta alasannya, tabel "jika … maka …", indikator, checklist berparaf), sedangkan tanpa skill SOP ditulis ke file dan tidak tampil di chat. Jujur: untuk aturan dapur yang berisiko, AI biasa sudah menolak praktik berbahaya. Rincian: `examples/00-openclaw-sebelum-sesudah.md`.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Buat SOP packing pesanan Shopee untuk olshop baju saya"
- "SOP buka toko jam 8 pagi, lengkap checklist-nya"
- "SOP handling komplain pelanggan untuk warung makan"
- "Perbarui SOP ini ke versi 1.1, tambahkan langkah foto paket"

## Instalasi singkat
Salin folder `sop-writer` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Saya belum punya cara kerja yang baku. Tetap bisa?**
Bisa. Skill memakai praktik umum untuk jenis usahamu dan menandai langkah yang perlu kamu sesuaikan.

**Bisa dibuat versi poster untuk ditempel?**
Bisa. Minta "versi poster", nanti dibuat 5–7 langkah inti dengan huruf besar.

**Apakah SOP ini cukup untuk sertifikasi (halal, SLHS, PIRT, ISO)?**
Belum. SOP ini untuk operasional harian. Untuk sertifikasi, ikuti ketentuan resmi dan konsultasikan ke petugas atau pendamping sertifikasi.

## Catatan revisi 1.0.4 (2026-10-01)
- SOP lengkap (semua bagian, termasuk checklist harian) **wajib tampil di balasan chat**, siap salin — tidak lagi hanya disimpan ke file dengan ringkasan di chat. File hanya tambahan bila diminta/di folder proyek. Penting untuk pengguna Telegram/WhatsApp.

## Catatan revisi 1.0.3 (2026-10-01)
- Alur uang SOP kas konsisten: modal laci dipisah **satu kali** saja, ada baris rumus "uang seharusnya = modal + penjualan tunai; setoran = uang di laci − modal", dan aturan "satu tindakan hanya muncul sekali" di panduan bahasa.
- Izin usaha makanan diperbaiki: warung/rumah makan memakai **Sertifikat Laik Higiene Sanitasi (SLHS)** (atau label pengawasan untuk risiko rendah) dari Dinas Kesehatan (Permenkes 14/2021); PIRT/SPP-IRT hanya untuk pangan olahan kemasan.

