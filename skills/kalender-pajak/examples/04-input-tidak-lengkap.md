# Uji 04 (Input tidak lengkap) — "kapan bayar pajak?"

> Penguji independen, 2026-09-25.

## Permintaan pengguna
> "kapan bayar pajak?"

## Perilaku agent sesuai SKILL.md
Profil wajib dan tidak bisa ditebak → tanya **sekali**, satu pesan bernomor, maks. 4 pertanyaan (bagian "Input"):

> Supaya tanggalnya pas dengan usaha Anda, saya perlu 4 info singkat:
> 1. Orang pribadi atau badan (PT/CV/koperasi)?
> 2. Pakai PPh final 0,5% (UMKM) atau pembukuan/tarif umum?
> 3. Sudah PKP (memungut PPN)?
> 4. Punya karyawan, atau membayar jasa/sewa yang dipotong PPh 23/4(2)?
>
> Kalau mau cepat, saya pakai asumsi paling umum: **orang pribadi UMKM 0,5%, belum PKP, tanpa karyawan**.

## Bila pengguna menjawab "cepat aja"
```bash
python3 scripts/kalender_pajak.py --profil op-umkm --hari-ini 2026-09-25 --rentang 31
```
Output (apa adanya):
## Tenggat pajak 31 hari ke depan (Jumat, 25 September 2026 s.d. Senin, 26 Oktober 2026) - op-umkm

| Sisa | Tanggal | Kegiatan | Keterangan |
|---|---|---|---|
| 20 hari lagi | Kamis, 15 Oktober 2026 | SETOR PPh Final UMKM 0,5% (PP 55/2022) masa Sep 2026 | - |

_Bukan nasihat pajak. Dasar: PMK 81/2024 (berlaku 1 Jan 2025), PP 55/2022 jo. PP 20/2026, PER-2/PJ/2024, SKB 3 Menteri libur nasional & cuti bersama; dicek 2026-09-25 dari sumber sekunder (naskah resmi belum dibaca langsung). DJP kadang memundurkan tenggat lewat pengumuman khusus - cek pengumuman DJP terbaru (pajak.go.id, Kring Pajak 1500200). Pembulatan/perhitungan pajak tidak dilakukan skill ini dan belum dicocokkan dengan Coretax. Untuk kasus Anda, konsultasikan dengan konsultan pajak atau Account Representative (AR)._

Jawaban agent: "Dengan asumsi Anda orang pribadi UMKM 0,5% belum PKP: setor PPh final masa September paling lambat **Kamis 15 Oktober 2026**. Setoran yang sudah tervalidasi dianggap sudah lapor. Hanya perlu setor bila omzet Anda tahun ini sudah melewati Rp500 juta. Kalau asumsi ini salah, kabari saya profil Anda."

## Uji ketahanan: bila agent langsung memanggil script tanpa profil
```
$ python3 scripts/kalender_pajak.py --tahun 2026
ERROR: isi --profil, mis. --profil op-umkm atau --profil badan-pkp,pemberi-kerja
(kode keluar 2)
```
## Penilaian penguji
- Pertanyaan sekali, ≤4, bahasa awam, default + asumsi disebut → sesuai prinsip "instan".
- Script menolak dengan pesan jelas, tanpa traceback.
- Hasil: **LULUS**.
