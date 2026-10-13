# Uji OpenClaw SEBELUM vs SESUDAH — notulen-rapat

## Uji ulang v1.0.4 (2026-10-13, penguji independen)

**Cara uji:** OpenClaw 2026.10.2 lokal (`openclaw agent --local`, tanpa Telegram/gateway), model router Komunitech yang sama dengan bot member (`ninerouter/komunitech`, jawaban `claude-sonnet-5`). Home bersih per sisi dan sesi baru. SEBELUM = tanpa skill; SESUDAH = hanya skill ini (v1.0.4), bukan paket. Agent dijalankan terisolasi (repo dan folder lain tidak terlihat). Tanggal sistem agent 14 Okt 2026 (WIB), sedangkan pesan menyebut "tadi pagi" dan "1/10". Kedua sisi memakai 1 Okt 2026 sebagai tanggal rapat.

**Skenario (pesan identik, satu giliran, data fiktif):** sama persis dengan uji 2026-10-01, yaitu catatan rapat mingguan 1/10 yang berantakan ("sales sept 2,1M target 2,5M", "jumat depan", "sebelum rabu", "besok", "forklift 2 rusak", "hendra ajukan sewa forklift … pak budi setuju", rapat berikutnya "kamis depan").

**Verifikasi kalender (Python, independen):** 1 Okt 2026 = Kamis; besok = Jumat 2 Okt; Senin = 5 Okt; sebelum Rabu = sebelum 7 Okt; Kamis depan = 8 Okt; "Jumat depan" bisa Jumat 2 Okt atau Jumat 9 Okt (ambigu). Nama hari di jawaban SESUDAH semuanya benar.

| Sisi | Skor | Alasan |
|---|---|---|
| SEBELUM (tanpa skill) | 6 | Struktur rapi dan peserta lengkap. Namun "2,1M" ditulis "Rp2,1 juta" tanpa tanda ragu, "forklift 2 rusak" dibaca sebagai "2 unit forklift rusak", dan tanggal relatif tidak dikonversi ("Jumat depan", "Sebelum Rabu", "Besok"). Tabel tugas juga menambah tenggat karangan untuk sewa forklift ("Senin (saat teknisi datang)"), dan tidak ada daftar hal yang perlu dikonfirmasi maupun pesan WA. |
| SESUDAH (v1.0.4) | 9 | Tanggal dihitung script: sebelum Rabu 7 Okt, besok Jumat 2 Okt, rapat berikutnya Kamis 8 Okt. "Jumat depan" ditandai ambigu (2 atau 9 Okt) di tabel dan di pesan WA (90 kata), satuan "M" diberi `[cek: …]`, dan "Forklift 2" ditulis sebagai nomor unit. Perbaikan v1.0.4 terbukti: tidak ada lagi tugas tambahan untuk Hendra, karena sewa forklift hanya dicatat sebagai keputusan yang disetujui Pak Budi, dan harga palet tidak lagi masuk Keputusan. Minus kecil: pemimpin rapat diisi "Pak Budi — disimpulkan dari jabatan" (memang ditandai untuk dikonfirmasi, tetapi SKILL.md meminta `[isi]`). |
| **Selisih** | **+3,0** | |

**Verdik: LULUS** (sesudah 9 ≥ 8 dan selisih 3,0 ≥ 1,5).

**Pembeda (hanya muncul saat skill aktif):** tanggal relatif dikonversi pasti lewat script, dan yang ambigu ("Jumat depan" = 2 atau 9 Okt) ditanyakan. Tanpa skill, tanggal dibiarkan relatif, "2,1M" berubah menjadi Rp2,1 juta, dan forklift nomor 2 dibaca sebagai 2 unit.

Proses: sisi SESUDAH membaca SKILL.md, lalu menjalankan `scripts/tanggal_relatif.py` 4 kali lewat path skill langsung (tanpa `find /` dan tanpa instalasi paket), selesai dalam ±4 menit. Sisi SEBELUM tidak memakai alat (±1,5 menit).

Cuplikan jawaban:
> **SEBELUM:** - Realisasi September: Rp2,1 juta dari target Rp2,5 juta.
> **SEBELUM:** - 2 unit forklift rusak; teknisi dijadwalkan datang Senin.
> **SEBELUM:** | 2 | Sewa forklift sementara 3 hari | Hendra | Senin (saat teknisi datang) |
> **SEBELUM:** | 3 | Daftar piutang & draft tagihan | Bu Sari | Sebelum Rabu |
>
> **SESUDAH:** - Penjualan September tercatat Rp 2,1 M dari target Rp 2,5 M ⚠️ `[cek: satuan "M" dimaksud miliar atau juta?]`
> **SESUDAH:** - Forklift 2 (nomor unit) rusak; teknisi datang Senin, 5 Oktober 2026
> **SESUDAH:** 2. Sewa forklift sementara (3 hari, Rp 450.000/hari) disetujui Pak Budi.   ← bagian Keputusan
> **SESUDAH:** | 2 | Kirim daftar prospek | Tono | Jumat, 2 atau 9 Oktober 2026 ("paling lambat Jumat depan") ⚠️ ambigu | Belum mulai |
> **SESUDAH:** | 3 | Buat daftar piutang & draft tagihan | Bu Sari | Sebelum Rabu, 7 Oktober 2026 | Belum mulai |
> **SESUDAH (pesan WA):** • @Tono: kirim daftar prospek — tenggat *Jumat 2 Okt* atau *9 Okt* (❓ mohon dipastikan)

---

## Riwayat — uji 2026-10-01 (sebelum uji ulang di atas)

Sumber (ada di paket VIP): `solusi-vip/kantor-manajemen/UJI-OPENCLAW.md` (rincian: `solusi-vip/kantor-manajemen/uji-openclaw/01-notulen-rapat-catatan-berantakan.md` dan `01-notulen-rapat-ulang3.md`). Tanggal uji: 2026-10-01 (Asia/Jakarta). Versi skill saat uji: uji pertama tidak dicatat di sumber (sebelum revisi 1.0.3); uji ulang ke-3 = 1.0.3 (versi katalog saat ini 1.0.4). Penguji: agent penguji independen (bukan pembuat skill).

Berkas ini hanya menyalin ringkasan dari catatan uji internal di atas; balasan utuh kedua sisi ada di berkas sumber.

## Cara uji
- OpenClaw lokal (`openclaw agent --local`, tanpa Telegram/gateway), model router Komunitech yang sama dengan bot member (`ninerouter/komunitech`, jawaban `claude-sonnet-5`).
- SEBELUM = home tanpa skill; SESUDAH = home dengan paket skill Kantor & Manajemen. Kedua home dibuat ulang bersih sebelum skenario.
- Pesan member: catatan rapat mingguan 1/10 yang berantakan (peserta, "sales sept 2,1M target 2,5M", "jumat depan", "sebelum rabu", "besok", "forklift 2 rusak", rapat berikutnya "kamis depan").
- Kalender dicek penguji dengan Python (1 Okt 2026 = Kamis).

## Skor (skala 10)

| # | Skenario | Tanpa skill | Dengan skill (uji pertama) | Dengan skill (uji ulang ke-3, v1.0.3) | Pembeda satu kalimat |
|---|---|---|---|---|---|
| 1 | Notulen dari catatan rapat berantakan (tanggal relatif, satuan angka) | 6 | 8,5 | 9 | Tanpa skill "2,1M" ditulis Rp2.100.000, tanggal relatif tidak dikonversi, dan satu tugas dikarang; dengan skill tanggal dihitung script ("Sebelum Rabu, 7 Oktober 2026"), satuan "M" ditandai untuk dikonfirmasi, dan ada ringkasan siap tempel ke grup. |
| | **Rata-rata** (satu skenario) | **6** | **8,5** | **9** | |

## Verdik
**LULUS uji ulang ke-3** (9). Sumber menempatkan skenario ini sebagai salah satu pembeda nyata paket Kantor & Manajemen (tanggal relatif dikonversi pasti).

## Catatan jujur
- Satu skenario saja di OpenClaw; sisi tanpa skill tidak diulang pada uji ulang.
- Cacat uji pertama sisi dengan skill yang hilang pada uji ulang ke-3: script tidak mengenali "sebelum rabu"; "forklift 2 rusak" ditafsirkan 2 unit (kesalahan yang sama juga terjadi di sisi tanpa skill); tawaran "Mau saya tanyakan ke Tono dulu?".
- Temuan uji ulang ke-3: muncul tugas tambahan "Proses sewa forklift sementara - Hendra" yang tidak ada di catatan (ditandai peringatan "belum ada tenggat", tetapi melampaui catatan); sel tenggat Tono menulis 9 Okt padahal ditandai ambigu; "harga palet maksimal Rp85.000" ditaruh di bagian Keputusan (tafsir ringan). README skill mencatat perbaikan tugas tambahan di 1.0.4; tidak ada catatan uji ulang OpenClaw untuk 1.0.4 di sumber.
- Uji pertama: satuan "M" juga ditandai ambigu oleh sisi dengan skill (aman, tetapi agak berlebihan).
