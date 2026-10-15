# Riwayat perubahan — broadcast-wa

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.13 (2026-10-15)
- Tindak lanjut verifikasi rujukan aturan (dicek 15 Oktober 2026; sumber: Kebijakan WhatsApp Business https://www.whatsapp.com/legal/business-policy diperbarui 23 Sep 2026, UU 27/2022 PDP di JDIH BPK, PP 33/2026 di peraturan.go.id). Cara kerja skill dan script tidak berubah.
- README: bagian baru "Yang perlu Anda tahu (jujur)" — **mode Copilot** (AI menyiapkan draf & tautan wa.me, pemilik mengirim satu per satu; bukan auto-blast), kirim hanya ke pelanggan yang sudah setuju (opt-in) dan permintaan berhenti dihormati, serta beda **daftar tautan wa.me** dengan **WhatsApp Business Platform (API)** resmi untuk promo massal (bukan WhatsApp Web/kanal WhatsApp di OpenClaw). FAQ kirim otomatis ikut menunjuk jalur resmi itu.
- `references/aturan-pdp-wa.md`: sumber utama UU PDP diganti tautan resmi JDIH BPK (hukumonline jadi sumber sekunder); dasar pemrosesan dirujuk Pasal 20; pemberitahuan kebocoran ditulis "3 × 24 jam (72 jam), tertulis, Pasal 46 ayat (1)"; catatan PP pelaksana "BELUM TERVERIFIKASI" diganti PP 33/2026 (diundangkan 16 Juli 2026, berlaku 16 Januari 2027); bagian kebijakan WhatsApp diberi sumber resmi + tanggal, dan beda tautan wa.me vs WhatsApp Business Platform.
- Perbaikan setelah pemeriksaan independen: README tidak lagi menyebut "biaya per pesan" untuk WhatsApp Business Platform (kini "ada biaya, cek harga terbaru di penyedia", sama dengan referensi); `references/aturan-pdp-wa.md` menulis "lembaga yang disebut UU PDP" (bukan "lembaga pengawas") dan PP 33/2026 cukup disebut "peraturan pelaksana UU 27/2022".

## Catatan revisi 1.0.12 (2026-10-13)
- Rujukan UU PDP ditulis lengkap: UU 27/2022 tentang Pelindungan Data Pribadi (tanpa perubahan cara kerja).

## Catatan revisi 1.0.11 (2026-10-13)
- Rujukan ke skill arsip diganti: `caption-sosmed-umkm`, `kalender-konten-30hari` diganti `konten-mingguan` (SKILL.md, bagian Kapan TIDAK digunakan).

## Catatan revisi 1.0.10 (2026-10-03)
- ATURAN WAJIB baru: draf teks pada jalur penolakan (tanpa file kontak) juga wajib lolos `cek_fakta.py`; klaim/urgensi karangan ("Hari ini ada promo", "Khusus hari ini", "sebelum kehabisan") dilarang.
- `cek_fakta.py` menambah deteksi "hari ini ada promo", "promo hari ini", "mumpung promo"; tes regresi ditambah.

## Catatan revisi 1.0.9 (2026-10-01)
- Cek fakta kini **otomatis di dalam perintah utama** (`siapkan_broadcast.py`) dan tidak bisa dilewati: klaim yang tidak disebut pemilik ("Khusus hari ini", "sebelum kehabisan", "promo terakhir", "buruan", "jangan sampai ketinggalan", "waktu terbatas", "stok terbatas", dst.) membuat script **GAGAL** dan tidak menghasilkan file siap kirim, dengan atau tanpa `--fakta-file`.
- Daftar frasa urgensi di `cek_fakta.py` diperluas; tes regresi ditambah.

## Catatan revisi 1.0.8 (2026-10-01)
- Kolom **Sapaan/Panggilan** di file kontak kini dipakai ("Bu Siti", "Pak Fajar"), tidak lagi diganti "Kak".
- Versi daftar siaran (tanpa nama) dipisah jelas dan ditolak bila masuk ke daftar kirim personal.
- Pemeriksaan anti-karang: klaim seperti "stok terbatas", "terlaris", "halal" ditolak bila tidak disebut pemilik (`--fakta-file`).
- Kolom "Setuju Promo" dikenali otomatis sebagai kolom persetujuan.
