# Presentasi Rapi, Tanpa PowerPoint, Tanpa Ribet

**Cukup ceritakan usaha Anda, langsung jadi presentasi siap kirim — buka di HP pun bisa.**

*Diuji AI penguji independen di OpenClaw: 6,0 → 8,5 dari 10 pada uji ulang v1.1.5 (13 Okt 2026; uji pertama 6,0 → 8,25) (tanpa skill, slide ke bank memuat angka cicilan dan klaim rasio 65% "wajar" tanpa peringatan; dengan skill, angka yang belum pasti ditandai `[isi]` dan peringatan cicilan terlalu berat disampaikan ke Anda secara pribadi, bukan ditaruh di slide).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Tidak perlu install PowerPoint/Canva atau bikin akun apa pun — hasilnya satu file HTML (file halaman web yang dibuka di browser) yang langsung bisa dibuka.
- ✅ Bisa dibuka tanpa internet, di laptop maupun HP, dan tinggal dicetak ke PDF (Print → Save as PDF) untuk dikirim lewat email/WA atau dicetak.
- ✅ Sudah ada 7 kerangka slide siap pakai untuk konteks Indonesia: pitch investor (presentasi untuk meyakinkan calon investor), proposal ke perusahaan lain, pengajuan KUR (Kredit Usaha Rakyat)/bank, laporan bulanan, profil perusahaan, penawaran ke reseller, dan materi pelatihan karyawan, lengkap dengan kartu angka, tabel rapi, timeline, dan kutipan siap pakai.
- ✅ Angka Rupiah ditulis dengan format yang benar (`Rp 1.250.000`) dan diambil dari data Anda atau skill hitung lain Komunitech (mis. skill **Pengajuan KUR**, skill **Rekap Penjualan CSV**) — angka yang belum pasti ditandai `[isi]`, bukan ditebak.
- ✅ Bisa dibuka & dicetak jadi PDF rapi satu slide per halaman, dirancang agar tidak terpotong; di HP tegak akan diingatkan untuk memutar ke posisi mendatar (bisa ditutup lewat tombol "Tetap lihat"). Ada mode edit teks langsung di browser (tombol "Edit") — menyimpan hasil edit (Ctrl+S/Cmd+S) hanya bisa di laptop/komputer, di HP minta AI yang mengubah teksnya.

## Cocok untuk siapa
- Pemilik UMKM yang mau mengajukan KUR (Kredit Usaha Rakyat) ke bank tapi tidak punya desainer.
- Pencari investor/mitra yang butuh pitch deck (presentasi singkat untuk calon investor) cepat dan rapi.
- Tim kantor yang bikin laporan bulanan ke atasan setiap bulan.
- Bisnis yang mau menawarkan produknya ke reseller/agen baru.
- Siapa saja yang butuh presentasi bagus tapi tidak mau ribet buka PowerPoint.

## Contoh sebelum & sesudah
**Sebelum:** Bikin sendiri di PowerPoint/Canva — buka aplikasi, cari template, atur
posisi teks satu-satu, bingung warna apa yang pas, hasilnya kadang berantakan kalau
dibuka di HP.

**Sesudah (cukup ketik):** "Mau ajukan KUR ke BRI bulan depan, butuh presentasi buat ketemu mantri/analisnya. Usaha: bengkel motor "Maju Jaya Motor" di Sidoarjo, jalan 5 tahun, 3 mekanik. Omzet rata2 Rp 42.500.000 per bulan, ..."
→ Satu file HTML berisi 10 slide: sampul, profil, layanan, kinerja, aset, penggunaan dana, rencana pengembalian, proyeksi, legalitas, dan penutup. Balasan aslinya dari uji simulasi agen penguji, 23 Sep 2026, data fiktif (contoh lengkap: `examples/02-pengajuan-kur-bengkel.md`):
```
Presentasi Pengajuan KUR - Bengkel Maju Jaya Motor sudah jadi: kur-maju-jaya-motor.html (10 slide)

Cara pakai:
- Buka file-nya dua kali klik, bisa dibuka di laptop maupun HP, tanpa internet.
- Navigasi: panah kiri/kanan, geser jari di HP, atau tombol ‹ ›.
- Cetak jadi PDF: Ctrl+P / Cmd+P → Simpan sebagai PDF → orientasi Lanskap.

Asumsi yang dipakai: palet "Hijau Amanah"; cicilan dihitung dengan bunga 6% efektif per tahun (anuitas) sebagai perkiraan — angka resmi mengikuti tabel angsuran bank.
Bagian yang masih perlu Anda lengkapi: alamat usaha, layanan tambahan, perkiraan kenaikan omzet setelah dana cair + asumsinya, status bukti sewa tempat.
Catatan: presentasi ini pelengkap, bukan pengganti formulir resmi KUR — cek syarat terbaru ke bank/penyalur KUR (kur.ekon.go.id).
```
(Anuitas = cicilan tetap tiap bulan.)

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Buatkan pitch deck untuk cari investor, usaha saya jasa laundry kiloan."
- "Tolong buatkan presentasi profil perusahaan, [nama usaha], bidang konveksi."
- "Buatkan laporan bulanan penjualan bulan ini untuk dipresentasikan ke owner."
- "Buatkan presentasi penawaran produk ke calon reseller."

## Instalasi singkat
Salin folder `presentasi-instan` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):**
- **Uji OpenClaw, 1 Oktober 2026** (penguji AI independen; angka dari `examples/00-openclaw-sebelum-sesudah.md`): rata-rata nilai 6,0 tanpa skill menjadi 8,25 dengan skill (skala 10). Pada skenario pengajuan KUR, slide buatan AI tanpa skill memuat klaim "rasio di bawah 70% umumnya dianggap wajar" (tanpa sumber) dan tidak memperingatkan bahwa rasio cicilan ±65% itu berat; dengan skill, angka yang belum pasti ditandai `[isi]` dan peringatan rasio berat disampaikan ke Anda secara pribadi, tidak ditaruh di slide.
- Jujur: pada skenario pitch investor, kedua sisi sama-sama menghasilkan presentasi yang layak (nilai 7 tanpa skill vs 8 dengan skill). Tanpa skill, AI di uji ini langsung membuat file PDF (dan file PowerPoint pada skenario KUR), sedangkan skill menghasilkan file HTML dan memandu Anda mencetak PDF sendiri.
- **Uji ulang v1.1.5, 13 Okt 2026** (OpenClaw 2026.10.2, penguji independen, pesan identik dengan uji pertama): tanpa skill **6,0** → dengan skill **8,5** (LULUS). Tanpa skill, rincian dana Rp250 juta dan klaim "profitable/terbukti" dikarang sebagai fakta; dengan skill semua angka yang belum pasti ditandai `[isi]` dan validator lolos. Catatan jujur: isi chat memuat urutan judul, angka kunci, dan asumsi, bukan teks lengkap tiap slide.
- Tampilan di HP dan cetak PDF diuji lewat peramban Chromium di komputer penguji (`examples/HASIL-UJI.md`), bukan di HP atau printer sungguhan.

**Status uji (jujur):** diuji di OpenClaw (uji otomatis agent) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech, 17 Okt 2026, versi 1.1.6) dengan pesan yang sama: "Halo, tolong bikinin pitch deck buat ketemu investor minggu depan. Usahaku laundry kiloan namanya Bersih Kilat, udah 2 outlet di Depok sejak 2023. Omzet gabungan sekarang sekitar Rp 38 juta sebulan, pelanggan aktif 620 orang,…". Tanpa skill skor **6,5** → dengan skill skor **8** (selisih +1,5, lulus acuan kami). Dengan skill, Anda menerima berkas presentasi 13 slide yang langsung bisa dibuka di HP atau laptop dan dicetak ke PDF, dan data yang belum Anda berikan dikosongkan untuk diisi, bukan dikarang. Tanpa skill, Anda hanya mendapat teks di chat dengan rincian dana dan target yang dikarang. Catatan jujur: deck masih menyisakan kolom [isi] (ukuran pasar, pesaing, rincian dana, proyeksi) yang perlu Anda lengkapi sendiri, satu angka di slide Masalah ("2–3 jam/minggu") bukan dari Anda dan belum diberi label perkiraan, valuasi sebelum pendanaan (Rp2,55 miliar) tidak disebut, dan bot sempat mengirim satu pesan tambahan berisi kalimat proses yang tidak perlu. Uji sebelumnya: 16 Okt 2026 (versi 1.1.5) tanpa skill 6,9 → dengan skill 7,5; saat itu berkas deck belum ikut terkirim ke chat.

## FAQ
**Hasilnya file apa? Bisa dibuka pakai apa?**
Hasilnya satu file `.html`. Buka dengan dua kali klik atau tarik ke jendela browser
(Chrome, Edge, Safari, atau browser HP) — tidak perlu internet, tidak perlu aplikasi
tambahan.

**Bisa dijadikan PDF atau file PowerPoint?**
Untuk PDF: bisa, tinggal buka file lalu Ctrl+P / Cmd+P, pilih "Simpan sebagai PDF",
margin "Tidak ada", dan centang "Grafis latar" — halaman otomatis pas, tidak perlu
pilih ukuran kertas atau orientasi manual.
Untuk `.pptx` (PowerPoint asli): skill ini tidak menghasilkan format itu — kalau Anda
butuh file PowerPoint yang bisa diedit di Microsoft Office, gunakan alat pembuat
`.pptx` terpisah.

**Kalau saya belum tahu isi presentasinya harus apa saja, apa tetap bisa dibantu?**
Bisa. Cukup sebutkan presentasi ini untuk keperluan apa (misalnya "pitch investor" atau
"pengajuan KUR"), nanti kerangka slide dan contoh isinya dibuatkan otomatis — bagian
yang perlu Anda lengkapi sendiri (seperti data usaha) akan ditandai jelas.

## Riwayat perubahan

Versi terkini: **1.1.6**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.

- **1.1.6 (16 Okt 2026):** di Telegram/WhatsApp, file presentasi kini ikut dikirim sebagai dokumen, dan balasan memakai bahasa sehari-hari (tanpa istilah teknis atau nama skill internal).
