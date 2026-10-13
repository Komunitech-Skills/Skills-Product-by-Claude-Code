# Tagih Piutang Sopan, Tegas, dan Aman Hukum

**Pelanggan telat bayar? Dapat pesan penagihan bertahap sampai surat teguran resmi, dengan hitungan keterlambatan yang pasti.**

## Manfaat
- ✅ Pesan penagihan 6 tahap: pengingat sebelum jatuh tempo, hari H, lewat 7, 14, sampai 30 hari (surat teguran resmi)
- ✅ Hari keterlambatan, sisa tagihan, dan denda dihitung otomatis dan pasti benar
- ✅ Denda hanya dihitung jika memang tertulis di kontrak atau PO, lengkap dengan dasar pasalnya
- ✅ Rekap umur piutang dari daftar tagihan (CSV): tahu siapa yang harus ditagih duluan
- ✅ Bebas ancaman dan kata-kata mempermalukan yang bisa berbalik jadi masalah hukum

## Cocok untuk siapa
- Supplier, distributor, dan grosir yang memberi tempo pembayaran ke toko atau perusahaan
- Penyedia jasa (katering langganan, desain, konsultan, kontraktor) dengan pembayaran termin
- Pemilik usaha yang sungkan menagih pelanggan lama tapi arus kasnya terganggu

## Contoh sebelum & sesudah
**Sebelum:** Sungkan menagih, pesan cuma "Pak, gimana pembayarannya?" dan tidak ada kabar selama sebulan.

**Sesudah (cukup ketik):** "CV Sinar Abadi invoice 12,5 juta jatuh tempo 24 Agustus, baru bayar 2,5 juta. Di PO ada denda 0,1% per hari setelah 3 hari, maksimal 5%"
→ Ringkasan: terlambat 30 hari, sisa Rp 10.000.000, denda Rp 270.000 sesuai PO. Plus surat teguran resmi yang tegas, sopan, dan menyebut dasar dendanya.

**Hasil uji (OpenClaw, uji otomatis agent, 10 Oktober 2026, v1.0.6):** rata-rata nilai 6,4 tanpa skill menjadi 8,0 dengan skill (skala 10); uji ulang versi terbaru pada 3 skenario: 6,7 menjadi 8,3. Contoh dari uji: 10 nota piutang toko bangunan yang berantakan menghasilkan total belum lunas Rp 157.540.000 dengan Rp 142.540.000 sudah lewat jatuh tempo (7 nota), dan nota yang sudah lunas tidak ikut ditagih. Permintaan "sebarkan ke grup dan hubungi istri atau atasan" ditolak dengan alasan hukum, lalu surat teguran yang sah tetap dibuatkan. Rincian: `examples/00-openclaw-sebelum-sesudah.md`.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Ingatkan pelanggan katering, tagihan 6,3 juta jatuh tempo Jumat ini"
- "Buat semua tahap penagihan untuk invoice INV-0801 Warung Bu Tini"
- "Ini file piutangku, urutkan mana yang harus ditagih dulu"

## Instalasi singkat
Salin folder `tagih-piutang` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

## FAQ
**Boleh saya tambahkan denda keterlambatan?**
Boleh, jika denda itu sudah disepakati tertulis (di kontrak, PO, atau syarat invoice). Jika tidak ada, skill akan mengingatkan agar denda tidak dicantumkan.

**Bolehkah saya mengumumkan nama pelanggan yang menunggak di grup atau media sosial?**
Jangan. Itu bisa melanggar UU ITE dan UU Pelindungan Data Pribadi. Skill ini hanya membuat pesan yang ditujukan langsung ke pelangganmu.

**Apakah surat teguran ini sama dengan bantuan pengacara?**
Tidak. Surat ini membantu menagih secara resmi. Jika tetap tidak dibayar atau nilainya besar, konsultasikan ke advokat.

> **Catatan penting:** alat bantu menyusun pesan dan surat penagihan, bukan nasihat hukum atau keuangan dan bukan pengganti advokat. Denda hanya dihitung bila disepakati tertulis. Dasar hukum yang dirujuk (ringkasan per 23 September 2026): KUHPerdata Pasal 1238 dan 1243 (pernyataan lalai/somasi dan ganti rugi), UU ITE (UU 1/2024) Pasal 27A dan 27B, serta UU PDP (UU 27/2022). Ringkasan hukum ini belum ditinjau advokat, jadi cek ulang bila aturan berubah; sengketa atau gugatan bernilai besar sebaiknya dibawa ke advokat.

## Catatan revisi 1.0.5 (2026-10-01)
- Temuan uji ulang OpenClaw: pesan menulis "kami lampirkan surat" padahal tidak ada file.
- Kini lampiran hanya disebut bila pengguna menyatakan ada; selain itu ditulis `[lampirkan: …]` dengan catatan pengguna yang membuat/melampirkan. Catatan pemilik di luar blok pesan.

## Catatan revisi 1.0.4 (2026-10-01)
Perbaikan dari uji OpenClaw asli (paket kantor-manajemen, konsultan, usaha-offline):
- File piutang dengan judul kolom umum langsung terbaca: `no_faktur`, `nilai_faktur`, `sudah_dibayar`, `customer`, `due_date`, `amount`, `paid`, kolom `sisa`/`outstanding`, judul berkurung seperti "Nilai Faktur (Rp)". Kolom lain (no. WA, tanggal faktur) diabaikan. Angka format Indonesia dan tanggal "25 Sep 2026" diterima. Bila kolom tidak dikenali, pesan error menyebut nama kolom yang diterima dan kolom yang ada di file.
- Rekap kini menampilkan total yang sudah lewat jatuh tempo.
- Script menulis kalimat jadwal yang jelas (tenggat bayar + kapan tahap berikutnya). Opsi `--hubungan dekat` (tetangga/kenalan/keluarga) memakai jeda 14 hari dan menyarankan bicara langsung dulu. Tidak ada lagi saran naik ke tahap tegas dalam 2 hari.
- Rincian yang diberikan pengguna (per bulan/per invoice) wajib masuk ke pesan tagihan.
- UU ITE/UU PDP hanya disebut bila relevan, dengan alasannya. Bila pengguna minta tahap 5 lewat WA: versi WA singkat + saran surat resmi.
- Path script ditulis jelas (subfolder `scripts/` di folder skill); agent dilarang mencari ke seluruh disk.
