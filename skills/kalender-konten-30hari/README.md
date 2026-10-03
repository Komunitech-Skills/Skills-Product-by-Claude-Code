# Kalender Konten Sebulan, Tinggal Posting

**Sebut jenis usahamu, dapat rencana konten 30 hari lengkap dengan ide, hook, dan momen lokal.**

## Manfaat
- ✅ 30 hari terisi: tanggal, hari, ide konten, kalimat pembuka (hook), dan ajakan (CTA) — tidak ada lagi "hari ini posting apa ya?"
- ✅ Momen lokal otomatis: gajian, tanggal tua, tanggal kembar 10.10–12.12, Harbolnas, Hari Batik, Sumpah Pemuda, Hari Ibu, dan lainnya
- ✅ Seimbang: konten jualan dijaga sekitar 20–30%, sisanya edukasi, bukti, dan hiburan supaya pengikut tidak bosan
- ✅ Langsung tempel ke Google Sheets atau Excel (tersedia versi CSV)
- ✅ Tanggal dan nama hari dihitung otomatis, jadi tidak salah hari

## Cocok untuk siapa
- Pemilik UMKM yang mengurus Instagram, TikTok, dan WA Status sendiri
- Admin sosmed yang harus menyerahkan rencana konten bulanan ke atasan
- Usaha yang bersiap menghadapi 11.11, 12.12, Ramadan, atau ulang tahun toko

## Contoh sebelum & sesudah
**Sebelum:** Posting kalau sempat, sering bolong seminggu, dan baru ingat Hari Batik setelah lewat.

**Sesudah (cukup ketik):** "Bikinin kalender konten Oktober buat kedai kopi di Malang, tanggal 17 ulang tahun kedai, promo beli 2 gratis 1"
→ Tabel 30 hari: 2 Okt konten Hari Batik, 10 Okt momen 10.10, 17 Okt promo ulang tahun, 25 Okt promo gajian, plus file CSV untuk spreadsheet.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Buatin content plan TikTok & IG bulan depan buat toko hijab online"
- "Jadwal konten WA Status 30 hari buat toko sembako, versi CSV buat Excel"
- "Kalender konten Desember buat laundry kiloan, fokus 12.12 dan libur akhir tahun"

## Instalasi singkat
Salin folder `kalender-konten-30hari` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Apakah tanggal Ramadan dan Lebaran otomatis?**
Tidak ditebak, karena tanggal resminya ditetapkan pemerintah setiap tahun. Sebutkan tanggalnya, atau AI akan memberi label "perkiraan — cek SKB 3 Menteri".

**Bisa kalau saya cuma sanggup posting 3 kali seminggu?**
Bisa. Sebutkan kemampuanmu, nanti jadwalnya disesuaikan.

**File CSV-nya berantakan di Excel?**
Minta "CSV pakai titik koma" untuk Excel berbahasa Indonesia, atau "pakai koma" untuk Google Sheets.

## Catatan revisi 1.0.8 (2026-10-03)
- Kemampuan produksi dihitung per minggu kalender (Senin-Minggu): `--maks-video-minggu N` menandai minggu yang kelebihan video.
- Label "Ramadan H-22" ditolak; yang benar "Ramadan hari ke-22".

## Catatan revisi 1.0.7 (2026-10-03)
- "Aturan wajib" di awal SKILL.md: fakta produk/harga/klaim hanya dari kamu, selebihnya `[isi: ...]`; hasil default ringkas (tabel 30 baris + tips + asumsi) agar balasan cepat; file hanya di folder kerja.
- Cek fakta kini wajib: finalisasi tanpa salinan pesanmu dianggap GAGAL, jadi karangan tentang produk tidak lolos.

## Catatan revisi 1.0.6 (2026-10-01)
- Lebih ringan dan andal di Telegram/OpenClaw: AI cukup menjalankan script 2 kali (kerangka + finalisasi). Satu perintah finalisasi `--selesai` langsung menyimpan file CSV + tabel lengkap, mencetak tabel ringkas untuk chat (1 baris per hari, Hook & CTA 3 hari pertama), dan sekaligus cek-silang tanggal & fakta. Isian ditulis sebagai teks sederhana `No | Format | Ide | Hook | CTA`, bukan JSON besar.
- Caption lengkap hanya ditulis bila Anda minta (maks. 3–5 hari per balasan).
- Cek fakta diperluas: rasa/tekstur ("isi nanasnya padat", "renyah", "lumer"), cara buat ("dicetak satu-satu"), janji kirim ("besok dikirim"), dan jadwal toko ("pre-order dibuka", "sudah buka lagi") yang tidak Anda sebut ditandai GAGAL. Kalimat tips ("biar tetap renyah") tidak dianggap klaim.
- Platform yang tidak Anda sebut dicatat di Asumsi.

## Catatan revisi 1.0.5 (2026-10-01)
- Ramadan, Idulfitri, dan Imlek kini diisi otomatis oleh script dari tabel perkiraan (berlabel "perkiraan"): tiap hari Ramadan diberi "Ramadan hari ke-N", plus Nuzulul Qur'an, 10 malam terakhir, batas THR ±H-7, Lebaran & H+1, dan pasca-Lebaran. Tidak ada lagi "Tanggal tua" di tengah Ramadan.
- Cek-silang baru `--cek-teks`: tanggal hari besar yang disebut di tips/catatan harus sama dengan tabel (mis. Idulfitri 10 Mar 2027, bukan "19–20 Mar"); jawaban untuk periode Ramadan wajib menyebut Ramadan.
- Langkah wajib "Fakta dari pengguna" + `--fakta`: layanan/promo yang tidak Anda sebut (mis. "antar-jemput gratis") ditandai GAGAL.

## Catatan revisi 1.0.4 (2026-10-01)
- Tanggal hari besar (Ramadan, Lebaran, Imlek) diambil dari tabel perkiraan di skill, mis. awal Ramadan 2027 sekitar 8 Februari 2027 (perkiraan, menunggu sidang isbat), dan tidak pernah diklaim "sudah dicek".
- Urgensi palsu ("stok terbatas", "hari terakhir") dilarang kecuali faktanya Anda berikan.
