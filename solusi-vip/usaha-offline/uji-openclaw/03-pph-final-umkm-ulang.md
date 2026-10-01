# Uji ulang 03 — PPh Final UMKM 0,5% (pph-final-umkm 1.0.3)

Tanggal uji ulang: 2026-10-01 (Asia/Jakarta) · Penguji independen (bukan pembuat skill) · OpenClaw lokal (`openclaw agent --local`), model router Komunitech `ninerouter/komunitech` (jawaban dilayani `claude-sonnet-5`). Home baru `sol2-usaha-offline` (paket skill solusi, dibuat ulang lewat script reset sebelum skenario). Hanya sisi SESUDAH. Pesan member **identik** dengan uji pertama ([03-pph-final-umkm.md](03-pph-final-umkm.md)). Balasan disalin utuh tanpa suntingan. Semua angka dihitung ulang penguji dengan Python. Argumen tool call tidak dapat diaudit (hanya nama tool dari JSON keluaran).

## Pesan member
> Saya punya warung makan, atas nama pribadi, NPWP dari 2021. Omzet 2026: Jan 48jt, Feb 45jt, Mar 52jt, Apr 70jt, Mei 55jt, Jun 50jt, Jul 53jt, Agu 58jt, Sep 61jt. Okt kira2 60jt. Pajak 0,5% nya tiap bulan berapa dan setornya kapan? Ada yg telat ga?

Alat: `read, exec` (23 dtk). Skill terpakai.

## Balasan (utuh)
> Berikut hasil hitungnya (warung atas nama pribadi, NPWP 2021):
>
> ## PPh Final UMKM 0,5% - Tahun 2026 (Orang pribadi)
>
> | Bulan | Omzet | Kumulatif | Kena pajak | PPh 0,5% | Setor paling lambat |
> |---|---:|---:|---:|---:|---|
> | Jan | 48jt | 48jt | 0 | Rp0 | - |
> | Feb | 45jt | 93jt | 0 | Rp0 | - |
> | Mar | 52jt | 145jt | 0 | Rp0 | - |
> | Apr | 70jt | 215jt | 0 | Rp0 | - |
> | Mei | 55jt | 270jt | 0 | Rp0 | - |
> | Jun | 50jt | 320jt | 0 | Rp0 | - |
> | Jul | 53jt | 373jt | 0 | Rp0 | - |
> | Agu | 58jt | 431jt | 0 | Rp0 | - |
> | Sep | 61jt | 492jt | 0 | Rp0 | - |
> | Okt (estimasi) | 60jt | 552jt | **52jt** | **Rp 260.000** | **16 Nov 2026** (15 Nov jatuh Minggu, jadi mundur ke Senin) |
>
> **Intinya:**
> - Jan–Sep: omzet kumulatif masih di bawah Rp500 juta → **tidak ada pajak yang perlu disetor**, jadi tidak ada yang "telat" karena memang belum wajib setor.
> - **Oktober** jadi bulan pertama kena pajak, karena kumulatif tembus Rp552 juta (lewat Rp500 juta). Tapi hanya selisihnya yang kena: Rp552jt − Rp500jt = **Rp52 juta** × 0,5% = **Rp260.000**.
> - Batas setornya **16 November 2026** (belum lewat, jadi aman — tidak ada yang telat sejauh ini).
>
> **Catatan penting:**
> - Batas Rp500 juta ini untuk total omzet semua usaha Anda (bukan cuma warung ini), kalau ada usaha lain jumlahkan juga.
> - NPWP terdaftar 2021 → tarif 0,5% berlaku sampai tahun pajak **2027** menurut aturan lama (PP 55/2022, 7 tahun untuk orang pribadi). Ada kabar PP 20/2026 mengubah batas ini tapi **belum saya verifikasi** — cek ke DJP (Kring Pajak 1500200) sebelum 2027.
> - Ini dihitung dari omzet (bukan laba), dan masih estimasi untuk Oktober (60jt) — nanti sesuaikan kalau angka final beda.
>
> Perlu saya bantu buatkan pengingat otomatis tiap tanggal 15 biar tidak kelewat ke depannya?

## Verifikasi independen
Kumulatif (Python): 48, 93, 145, 215, 270, 320, 373, 431, 492, 552 jt ✔. Jan–Sep Rp0 ✔. Okt: (552 − 500) × 0,5% = **Rp260.000** ✔. 15 Nov 2026 = Minggu, 16 Nov 2026 = Senin (bukan libur nasional) → batas setor **16 Nov 2026** sesuai PMK 81/2024 ✔. NPWP 2021 + 7 tahun pajak (PP 55/2022 Ps. 59) → s.d. 2027 ✔. Tidak ada yang telat ✔.

## Penilaian
- **Cacat lama hilang: YA, keduanya.** (1) *"16 Nov 2026 (15 Nov jatuh Minggu, jadi mundur ke Senin)"*. (2) *"tarif 0,5% berlaku sampai tahun pajak 2027 menurut aturan lama (PP 55/2022, 7 tahun untuk orang pribadi). Ada kabar PP 20/2026 mengubah batas ini tapi belum saya verifikasi"*.
- **Regresi:** tidak ada. Tabel per bulan lebih jelas dari versi lama. Disclaimer "bukan nasihat pajak" tidak eksplisit di balasan (ada rujukan Kring Pajak). Kecil.
- **Skor: 9/10** (uji pertama SESUDAH: 7).
