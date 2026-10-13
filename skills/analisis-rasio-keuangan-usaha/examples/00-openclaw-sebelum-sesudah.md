# Uji OpenClaw SEBELUM vs SESUDAH — analisis-rasio-keuangan-usaha

## Uji ulang v1.0.5 (2026-10-13, penguji independen)

**Cara uji:** OpenClaw 2026.10.2 lokal (`openclaw agent --local`, tanpa Telegram/gateway), model router Komunitech yang sama dengan bot member (`ninerouter/komunitech`, jawaban `claude-sonnet-5`). Home bersih per sisi dan sesi baru. SEBELUM = tanpa skill; SESUDAH = hanya skill ini (v1.0.5), bukan paket. Agent dijalankan terisolasi (repo dan folder lain tidak terlihat). Tanggal sistem agent: 14 Okt 2026 (WIB).

**Skenario (pesan identik, satu giliran, data fiktif):** sama persis dengan uji 2026-10-01, yaitu neraca 31 Des 2025 + laba rugi 2025 perusahaan dagang (penjualan Rp9,6 M, kas Rp420 jt, utang bank jangka pendek Rp900 jt) dengan permintaan "tolong dicek sehat ga perusahaannya, buat bahan rapat sama komisaris minggu depan".

**Verifikasi angka (Python Decimal, independen dari script skill):** rasio lancar 1,657; cepat 1,066; kas 0,253; modal kerja Rp1,09 M; margin kotor 22,5%; margin usaha 7,40%; margin bersih 3,25%; ROA 5,24%; ROE 12,53%; DER 1,390; DAR 58,15%; cakupan bunga 2,290; umur stok 48,1 hari; lama piutang 51,3 hari; lama bayar pemasok 37,3 hari; siklus kas 62,1 hari; kas ÷ utang bank jangka pendek 46,7%; skala usaha kecil (PP 7/2021). **Di kedua sisi semua angka cocok** setelah pembulatan tampilan.

| Sisi | Skor | Alasan |
|---|---|---|
| SEBELUM (tanpa skill) | 7 | Semua rasio benar dan tersusun rapi, dan cakupan bunga 2,29x ditandai sebagai titik lemah. Namun kas Rp420 jt tidak dibandingkan dengan utang bank jatuh tempo Rp900 jt, sehingga kesimpulan "cukup sehat secara likuiditas", "aman jangka pendek", dan "tidak dalam bahaya" terlalu menenangkan untuk bahan komisaris. Ambang tidak bersumber dan tidak ada disclaimer. |
| SESUDAH (v1.0.5) | 9 | Angka dihitung script dan semuanya cocok. "Pemeriksaan kas vs utang jatuh tempo" menyebut risiko likuiditas SEDANG (kas menutup 47%), rasio kas diturunkan ke kuning, dan saran no. 1 adalah mengurus jadwal/perpanjangan utang bank. Perbaikan v1.0.5 terbukti: muncul baris "**Asumsi:** … jenis usaha dagang … skala kecil menurut penjualan setahun (PP 7/2021)". Minus kecil: ringkasan menulis ambang piutang "≤30–45 hari" sedangkan tabel "≤30 hari", disclaimer menyebut "referensi internal", serta ada bagian kesiapan kredit/bunga KUR yang tidak diminta. |
| **Selisih** | **+2,0** | |

**Verdik: LULUS** (sesudah 9 ≥ 8 dan selisih 2,0 ≥ 1,5).

**Pembeda (hanya muncul saat skill aktif):** kas Rp420 jt dibandingkan langsung dengan utang bank jatuh tempo Rp900 jt, dengan tingkat risiko likuiditas "SEDANG" dan saran mengurus perpanjangan sebelum jatuh tempo. Tanpa skill, laporan menyimpulkan "aman jangka pendek".

Proses: sisi SESUDAH membaca SKILL.md, lalu menjalankan `scripts/rasio.py` lewat path skill langsung (tanpa `find /` dan tanpa instalasi paket), selesai dalam ±4 menit. Sisi SEBELUM tidak memakai alat (±2 menit).

Cuplikan jawaban:
> **SEBELUM:** - Working Capital = 2.750 - 1.660 = **+1.090 juta** → positif, aman jangka pendek
> **SEBELUM:** Perusahaan **cukup sehat secara likuiditas dan neraca masih seimbang** …
> **SEBELUM:** Singkatnya: **tidak dalam bahaya, tapi struktur permodalan agak bertumpu pada utang dan marginnya tipis** …
>
> **SESUDAH:** **Asumsi:** saya pakai ambang jenis usaha **dagang** karena HPP 77,5% dari penjualan dan margin kotor 22,5% … — skala **kecil** menurut penjualan setahun (PP 7/2021).
> **SESUDAH:** 1. **Risiko likuiditas SEDANG** — utang bank jatuh tempo ≤12 bulan (Rp 900 jt) lebih besar dari kas (Rp 420 jt). …
> **SESUDAH:** | Rasio kas | 0,25x | ≥0,20x baik | 🟡 Waspada | Diturunkan karena kas < utang bank jatuh tempo (lihat di bawah). |
> **SESUDAH:** | Lama piutang tertagih | 51,3 hari | ≤30 hari baik | 🔴 Bahaya | Paling bermasalah — piutang terlalu lambat cair. |
> **SESUDAH:** 1. **Amankan utang bank jatuh tempo** — minta jadwal jatuh tempo tertulis dari bank, ajukan perpanjangan/roll-over …

---

## Riwayat — uji 2026-10-01 (sebelum uji ulang di atas)

Sumber (ada di paket VIP): `solusi-vip/kantor-manajemen/UJI-OPENCLAW.md` (rincian: `solusi-vip/kantor-manajemen/uji-openclaw/03-rasio-keuangan-bahan-komisaris.md` dan `03-rasio-keuangan-ulang3.md`). Tanggal uji: 2026-10-01 (Asia/Jakarta). Versi skill saat uji: uji pertama tidak dicatat di sumber (sebelum revisi 1.0.4); uji ulang ke-3 = 1.0.4 (versi katalog saat ini 1.0.5). Penguji: agent penguji independen (bukan pembuat skill).

Berkas ini hanya menyalin ringkasan dari catatan uji internal di atas; balasan utuh kedua sisi ada di berkas sumber.

## Cara uji
- OpenClaw lokal (`openclaw agent --local`, tanpa Telegram/gateway), model router Komunitech yang sama dengan bot member (`ninerouter/komunitech`, jawaban `claude-sonnet-5`).
- SEBELUM = home tanpa skill; SESUDAH = home dengan paket skill Kantor & Manajemen. Kedua home dibuat ulang bersih sebelum skenario.
- Pesan member: neraca 31 Des 2025 dan laba rugi 2025 sebuah perusahaan dagang (penjualan Rp9,6 M, kas Rp420 jt, utang bank jangka pendek Rp900 jt), "dicek sehat ga perusahaannya, buat bahan rapat sama komisaris".
- Semua rasio dihitung ulang penguji dengan Python (rasio lancar 1,657; cepat 1,066; kas 0,253; DER 1,390; cakupan bunga 2,290; margin kotor 22,5%; dan seterusnya).

## Skor (skala 10)

| # | Skenario | Tanpa skill | Dengan skill (uji pertama) | Dengan skill (uji ulang ke-3, v1.0.4) | Pembeda satu kalimat |
|---|---|---|---|---|---|
| 1 | Rasio keuangan neraca + laba rugi untuk bahan rapat komisaris | 8 | 8 | 9 | Uji pertama seri: semua angka benar di kedua sisi, tanpa skill menangkap risiko utang bank jangka pendek (Rp900 jt) melebihi kas (Rp420 jt) sedangkan dengan skill salah menenangkan ("tidak ada risiko gagal bayar jangka pendek", rasio kas hijau); setelah revisi: risiko likuiditas "SEDANG", kas hanya menutup 47% utang bank jangka pendek, rasio kas kuning, semua angka dari script. |
| | **Rata-rata** (satu skenario) | **8** | **8** | **9** | |

## Verdik
**LULUS uji ulang ke-3** (9). Pada uji pertama hasilnya SERI, dan sumber melarang memakai skenario ini sebagai bukti sebelum/sesudah; setelah uji ulang sumber menyebut cuplikan jualan kini layak.

## Catatan jujur
- Selisih terhadap sisi tanpa skill hanya 1,0 poin (9 melawan 8) dan sisi tanpa skill tidak diulang; untuk laporan yang rapi, model tanpa skill sudah pandai menghitung rasio dasar.
- Cacat uji pertama sisi dengan skill: ambang UMKM dipakai untuk perusahaan menengah, rasio kas 0,25 diberi tanda hijau, dan jenis usaha "dagang" diasumsikan tanpa disebut. Dua cacat pertama hilang pada uji ulang ke-3; jenis usaha tertulis di kepala laporan ("Usaha dagang, skala kecil") tetapi belum diberi label asumsi (README skill mencatat perbaikan di 1.0.5; tidak ada catatan uji ulang OpenClaw untuk 1.0.5 di sumber).
- Uji ulang ke-3 mengoreksi laporan uji pertama: omzet Rp9,6 M tergolong usaha kecil menurut PP 7/2021 (bukan menengah).
- Regresi kecil uji ulang: saran no. 3 tumpang tindih dengan saran no. 1, dan label "ROA/ROE disetahunkan" tidak perlu untuk data setahun penuh.
- Hanya satu skenario di OpenClaw.
