# Uji banding pesaing — skill sumber (ATM) `internal-comms` vs `laporan-status-kantor`

## Sumber yang dibandingkan
- **Pesaing utama (wajib, karena ini ATM)**: `internal-comms` — Anthropic, PBC.
  URL: https://github.com/anthropics/skills/tree/main/skills/internal-comms
  Lisensi: Apache License 2.0. Dibaca via `git clone --depth 1` ke `/tmp/anthropic-skills`
  (read-only, tidak dijalankan). Isi hanya dibaca untuk dinilai, tidak disalin ke file ini.
- **Pencarian pesaing publik lain**: kata kunci "`SKILL.md` weekly status report",
  "laporan mingguan bahasa indonesia SKILL.md", `manairalabs/bicara-skills`,
  `alvinindra/bahasa-skills` (via WebSearch).
  - `manairalabs/bicara-skills`: fokus ekstraksi invoice & balasan CS WhatsApp UMKM
    Indonesia — **tidak ada** skill laporan status/komunikasi internal. Tidak relevan.
  - `alvinindra/bahasa-skills`: fokus kualitas penulisan Bahasa Indonesia (diksi, EYD,
    marketing/SEO/UX writing) — **tidak ada** skill format laporan status/3P/pengumuman
    internal. Tidak relevan.
  - `zayan-work/skill-weekly-report` (ditemukan via pencarian umum): skill personal,
    **hardcoded** untuk satu orang ("Zayan") melapor ke satu atasan ("Rengan") dari commit
    git di 4 repo spesifik (`reservato-*`). Bukan template umum yang bisa dipakai kantor
    lain, dan berbasis aktivitas git (developer-only), bukan chat/catatan bebas seperti
    target skill kita. **Tidak sebanding** sebagai pesaing umum, hanya dicatat sebagai
    temuan pencarian.
  - Tidak ditemukan pesaing publik lain yang sebanding (menyusun laporan kantor Indonesia
    dari bahan mentah bebas, multi-jenis komunikasi, siap format WA).

**Kesimpulan pencarian**: satu-satunya pesaing yang benar-benar sebanding adalah skill
sumber ATM (`internal-comms`) itu sendiri.

## Skenario S1 (3P toko bangunan) — berdampingan

**Instruksi sumber diikuti** (dari `examples/3p-updates.md` sumber, generik, tanpa
template audiens/kanal terpisah):

```
🧱 Toko Bangunan Jaya Makmur (Cabang Ciputat) (21-25 Sep 2026)
Progress: Sales this week reached approximately Rp 45 million.
Plans: Preparing a wall paint promotion for next month, timed with the start of dry season.
Problems: Cement stock has been out since Wednesday and hasn't been restocked yet;
warehouse is also short-staffed since Thursday because Budi is on sick leave through
Monday.
```
*(Catatan: skill sumber tidak punya instruksi bahasa — ditulis default Inggris karena
audience/frontmatter aslinya berbahasa Inggris; jika "diterjemahkan" agar setara, hasilnya
tetap TANPA `*bold*` WA karena format sumber tidak menyebutkan sintaks tebal sama sekali,
dan TANPA pertimbangan privasi nama karyawan — sumber tidak membahas ini sama sekali.)*

**Output skill kita** (lihat `examples/01-3p-toko-bangunan.md` lengkap):
```
🧱 *Toko Bangunan Jaya Makmur (Cabang Ciputat)* — Laporan ke Bapak/Ibu Pemilik, 21–25 Sep 2026
*Progres:* Penjualan minggu ini tercatat sekitar Rp45 juta.
*Rencana:* Menyiapkan promo cat tembok untuk bulan depan, menyesuaikan mulai musim kemarau.
*Kendala:* Stok semen habis sejak Rabu dan belum direstok — mohon persetujuan Bapak/Ibu
untuk PO ke supplier. Selain itu, tim gudang kekurangan 1 orang sejak Kamis karena ada
staf yang izin sakit, sehingga proses bongkar-muat sedikit lebih lambat dari biasanya.
```

## Skenario S2 (update tim + versi klien) — berdampingan

**Sumber**: tidak punya template khusus audiens klien sama sekali. Instruksi 3P sumber
ditujukan untuk "executives, leadership, other teammates" secara umum (satu format untuk
semua penerima internal), dan `general-comms.md` (untuk hal di luar 3P/newsletter/FAQ)
hanya berisi prinsip umum ("clarify audience, tone, purpose") tanpa **larangan eksplisit**
menyertakan info sensitif (resign karyawan, over-budget) ke pihak eksternal seperti klien.
Kalau agen memakai skill sumber apa adanya untuk membuat "versi klien" dari 6 poin di S2,
tidak ada pagar built-in yang mencegah info resign 2 karyawan atau over-budget server ikut
ter-copy ke versi klien — itu murni bergantung pada kehati-hatian agen saat itu, bukan
instruksi skill.

**Skill kita**: `templates/3p-ke-klien.md` punya baris eksplisit **"Jangan pernah
menyertakan: masalah SDM internal, masalah keuangan internal perusahaan sendiri"** — pagar
ini terbukti bekerja di `examples/02-startup-tim-dan-klien.md` (versi klien otomatis bersih
dari 2 poin sensitif tersebut).

## Tabel penilaian (rubrik brief)

| Kriteria | Sumber (`internal-comms`) | Skill kita (`laporan-status-kantor`) |
|---|---|---|
| Kegunaan langsung (siap pakai tanpa edit) | Sedang — perlu diedit manual untuk jadi WA-ready (tambah `*bold*`, hapus gaya Inggris jika target Indonesia) | Tinggi — langsung format WA benar, Bahasa Indonesia |
| Lokalisasi Indonesia | Tidak ada (Inggris, tanpa konteks THR/cuti bersama/format WA) | Penuh (bahasa, WA/Telegram, THR, cuti bersama, dua nada budaya kantor ID) |
| Akurasi/anti-karang | Cukup baik secara prinsip ("data-driven", "ask if no access") tapi tidak ada penanda eksplisit `[isi: ...]` untuk info hilang | Eksplisit: penanda `[isi: ...]`, checklist anti-karang, larangan spesifik per domain (tanggal SKB, nominal THR) |
| Kesiapan kirim WA | Tidak (tidak membahas sintaks `*bold*` WA/Telegram sama sekali, ditulis untuk Slack/email korporat) | Ya, eksplisit jadi default kanal |
| Cakupan jenis komunikasi | 4 jenis (3P, newsletter, FAQ, general) | 9 jenis (3 varian 3P + harian + newsletter + pengumuman + FAQ + memo + insiden) |
| Perlindungan data sensitif (privasi karyawan, kebocoran ke klien) | Tidak dibahas sama sekali | Eksplisit: checklist privasi karyawan + larangan kebocoran versi klien |
| Konteks ketenagakerjaan Indonesia (THR, cuti bersama, SKB 3 Menteri) | Tidak relevan/tidak dibahas (skill AS) | Dibahas eksplisit dengan pagar "jangan mengarang tanggal/nominal" |

## Yang bisa dipelajari dari sumber (ide, bukan salinan teks)
- Kesederhanaan struktur "load file panduan sesuai jenis" tetap dipertahankan di skill
  kita (sudah diadopsi sejak awal, tercatat di ATTRIBUTION.md).
- Penekanan sumber pada "data-driven, matter-of-fact, not prose-heavy" untuk 3P adalah
  prinsip bagus yang sudah konsisten diikuti skill kita juga.
- Tidak ada ide baru dari sumber yang belum diadopsi skill kita; sumber justru lebih
  sempit cakupannya untuk konteks target pembeli (UMKM/kantor kecil Indonesia).

## Kesimpulan
Skill kita **menang jelas** di semua kriteria rubrik untuk kedua skenario yang diuji,
terutama pada 3 hal yang paling berdampak ke pembeli: (1) kesiapan format WA/Telegram yang
benar (sumber tidak membahasnya sama sekali — cacat fungsional bila dipakai langsung di
WA), (2) pagar privasi karyawan & kerahasiaan info ke klien (tidak ada di sumber), dan
(3) lokalisasi konteks ketenagakerjaan Indonesia (THR, cuti bersama). Tidak ditemukan
pesaing publik lain yang sebanding selain skill sumber ATM ini.
