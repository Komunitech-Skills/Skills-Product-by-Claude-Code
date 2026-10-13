# Presentasi Rapi, Tanpa PowerPoint, Tanpa Ribet

**Cukup ceritakan usahamu, langsung jadi presentasi siap kirim — buka di HP pun bisa.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Tidak perlu install PowerPoint/Canva atau bikin akun apa pun — hasilnya satu file HTML yang langsung bisa dibuka.
- ✅ Bisa dibuka tanpa internet, di laptop maupun HP, dan tinggal dicetak ke PDF (Print → Save as PDF) untuk dikirim lewat email/WA atau dicetak.
- ✅ Sudah ada 7 kerangka slide siap pakai untuk konteks Indonesia: pitch investor, proposal ke perusahaan lain, pengajuan KUR/bank, laporan bulanan, profil perusahaan, penawaran ke reseller, dan materi pelatihan karyawan, lengkap dengan kartu angka, tabel rapi, timeline, dan kutipan siap pakai.
- ✅ Angka Rupiah ditulis dengan format yang benar (`Rp 1.250.000`) dan diambil dari data Anda atau skill hitung lain di library ini (mis. `pengajuan-kur`, `rekap-penjualan-csv`) — bukan ditebak.
- ✅ Bisa dibuka & dicetak jadi PDF rapi satu slide per halaman, tidak terpotong; di HP tegak akan diingatkan untuk memutar ke posisi mendatar (bisa ditutup lewat tombol "Tetap lihat"). Ada mode edit teks langsung di browser (tombol "Edit") — menyimpan hasil edit (Ctrl+S/Cmd+S) hanya bisa di laptop/komputer, di HP minta AI yang mengubah teksnya.

## Cocok untuk siapa
- Pemilik UMKM yang mau mengajukan KUR ke bank tapi tidak punya desainer.
- Pencari investor/mitra yang butuh pitch deck cepat dan rapi.
- Tim kantor yang bikin laporan bulanan ke atasan setiap bulan.
- Bisnis yang mau menawarkan produknya ke reseller/agen baru.
- Siapa saja yang butuh presentasi bagus tapi tidak mau ribet buka PowerPoint.

## Contoh sebelum & sesudah
**Sebelum:** Bikin sendiri di PowerPoint/Canva — buka aplikasi, cari template, atur
posisi teks satu-satu, bingung warna apa yang pas, hasilnya kadang berantakan kalau
dibuka di HP.

**Sesudah (cukup ketik):** "Buatkan presentasi pengajuan KUR untuk warung sembako
saya, omzet Rp 35 juta/bulan, mau pinjam Rp 50 juta buat nambah stok dan gerobak
keliling."
→ Dalam beberapa saat, dapat satu file HTML berisi 10 slide rapi (profil usaha, omzet,
aset, tujuan pinjaman, proyeksi, dst.), sudah bisa dibuka di HP dan dicetak jadi PDF.

**Hasil uji (OpenClaw, uji otomatis agent, 2026-10-01):** rata-rata nilai 6,0 tanpa skill menjadi 8,25 dengan skill (skala 10).
Pada skenario pengajuan KUR, slide buatan AI tanpa skill memuat klaim "rasio di bawah 70% umumnya dianggap wajar" (tanpa sumber) dan tidak memperingatkan bahwa rasio cicilan ±65% itu berat;
dengan skill, angka yang belum pasti ditandai `[isi]` dan peringatan rasio berat disampaikan ke Anda secara pribadi, tidak ditaruh di slide.
Jujur: pada uji ini masih ada beberapa kalimat kualitatif karangan di slide; perbaikannya (v1.1.5) belum diuji ulang.
Rincian: `examples/00-openclaw-sebelum-sesudah.md`.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Buatkan pitch deck untuk cari investor, usaha saya jasa laundry kiloan."
- "Tolong buatkan presentasi profil perusahaan, [nama usaha], bidang konveksi."
- "Buatkan laporan bulanan penjualan bulan ini untuk dipresentasikan ke owner."
- "Buatkan presentasi penawaran produk ke calon reseller."

## Instalasi singkat
Salin folder `presentasi-instan` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Hasilnya file apa? Bisa dibuka pakai apa?**
Hasilnya satu file `.html`. Buka dengan dua kali klik atau tarik ke jendela browser
(Chrome, Edge, Safari, atau browser HP) — tidak perlu internet, tidak perlu aplikasi
tambahan.

**Bisa dijadikan PDF atau file PowerPoint?**
Untuk PDF: bisa, tinggal buka file lalu Ctrl+P / Cmd+P, pilih "Simpan sebagai PDF",
margin "Tidak ada", dan centang "Grafis latar" — halaman otomatis pas, tidak perlu
pilih ukuran kertas atau orientasi manual.
Untuk `.pptx` (PowerPoint asli): skill ini tidak menghasilkan format itu — kalau kamu
butuh file PowerPoint yang bisa diedit di Microsoft Office, gunakan alat pembuat
`.pptx` terpisah.

**Kalau saya belum tahu isi presentasinya harus apa saja, apa tetap bisa dibantu?**
Bisa. Cukup sebutkan presentasi ini untuk keperluan apa (misalnya "pitch investor" atau
"pengajuan KUR"), nanti kerangka slide dan contoh isinya dibuatkan otomatis — bagian
yang perlu kamu lengkapi sendiri (seperti data usaha) akan ditandai jelas.

## Riwayat perubahan

Versi terkini: **1.1.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
