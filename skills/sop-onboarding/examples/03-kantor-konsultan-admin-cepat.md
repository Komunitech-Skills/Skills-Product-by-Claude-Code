# Uji 03 — Kantor Konsultan, Staf Admin, Mode "Cepat Saja"

Penguji independen (Tahap 6), 25 September 2026.

## Input pengguna
> "Staf admin baru mulai Senin 12 Oktober 2026 di kantor konsultan pajak saya, Senin–Jumat. Cepat saja ya,
> saya cuma butuh pesan sambutan WA sama jadwal 30-60-90."

Agent mengikuti Langkah 1 (buat bagian yang diminta saja) dan aturan "cepat": tidak bertanya ulang.
Jenis hubungan kerja tidak disebut → script dijalankan dengan default `pkwtt` dan asumsi ditulis tegas.

## Perintah script
```bash
python3 scripts/jadwal_onboarding.py --mulai "12 Oktober 2026" --hari-kerja 5 --jenis pkwtt \
  --nama "Staf Admin" --libur libur-nasional-2026-2027.csv --format markdown
```
Exit code 0.

---

## Pesan sambutan WA
```
Halo [Nama]! 🎉

Selamat bergabung di [Nama Kantor] sebagai Staf Admin. Kami senang kamu akan mulai bekerja
pada Senin, 12 Oktober 2026 pukul [isi: jam masuk].

Info untuk hari pertama:
📍 Lokasi: [isi: alamat kantor]
👤 Yang akan menyambut: [isi: nama & jabatan]
👕 Pakaian: [isi: mis. kemeja rapi]
📄 Bawa: KTP asli, nomor rekening, NPWP bila ada

Kalau ada pertanyaan sebelum hari-H, langsung chat saya ya.
Sampai jumpa Senin!

Salam,
[Nama pengirim], [Jabatan]
```

## Jadwal 30-60-90
| Tahap | Tanggal target | Tanggal disesuaikan | Digeser? | Penanggung jawab | Kegiatan |
|---|---|---|---|---|---|
| Hari pertama (H1) | 12 Oktober 2026 | 12 Oktober 2026 | Tidak | Pemilik/Atasan langsung | Penyambutan, serah terima perangkat & akun, penjelasan buku saku karyawan |
| Akhir minggu 1 | 18 Oktober 2026 | 19 Oktober 2026 | Ya | Buddy/rekan pendamping | Cek pemahaman tugas dasar & SOP harian, tanya kendala |
| Evaluasi 30 hari | 10 November 2026 | 10 November 2026 | Tidak | Atasan langsung | Evaluasi checklist tugas dasar; beri umpan balik tertulis singkat |
| Evaluasi 60 hari | 10 Desember 2026 | 10 Desember 2026 | Tidak | Atasan langsung | Evaluasi kemandirian kerja & kepatuhan SOP |
| Evaluasi 90 hari / akhir orientasi | 9 Januari 2027 | 11 Januari 2027 | Ya | Pemilik/Atasan | Evaluasi akhir masa orientasi (isi formulir evaluasi) |
| Akhir masa percobaan (batas hukum) | 11 Januari 2027 | 11 Januari 2027 | Tidak | Pemilik/Atasan | Keputusan lanjut sebagai karyawan tetap atau tidak (evaluasi disarankan selesai paling lambat hari kerja ini, SEBELUM tanggal hukum berakhir) |

Target admin kantor konsultan (sesuaikan):
- **Hari 30:** paham alur surat masuk/keluar, arsip dokumen klien, jadwal tenggat klien; akun email & aplikasi aktif.
- **Hari 60:** mandiri mengelola agenda & tagihan klien; menjaga kerahasiaan data klien (NDA ditandatangani).
- **Hari 90:** menjalankan administrasi harian tanpa pendampingan; bisa melatih admin berikutnya untuk tugas dasar.

**Asumsi:** staf ini karyawan tetap (PKWTT) dengan masa percobaan 3 bulan yang tertulis di perjanjian
kerja. Bila **kontrak (PKWT)**, baris "Akhir masa percobaan" dihapus — PKWT dilarang memakai masa percobaan
(UU 13/2003 Pasal 58 jo. UU 6/2023). Bila PKWTT tanpa masa percobaan tertulis, baris itu juga tidak berlaku.

Catatan singkat: jangan lupa daftarkan BPJS Ketenagakerjaan & Kesehatan (wajib, paling lambat 30 hari).
Butuh checklist dokumen, buku saku, atau NDA klien? Tinggal bilang — bagian itu bisa saya lanjutkan.
Disclaimer: alat bantu administrasi, bukan nasihat hukum (dasar aturan dicek 25 September 2026).

---
## Penilaian penguji
| Kriteria | Hasil |
|---|---|
| Hanya bagian yang diminta | ✅ ringkas, bagian lain ditawarkan |
| Tanggal cocok verifikasi mandiri | ✅ (12 Okt + 89 = 9 Jan 2027 Sabtu → Senin 11 Jan; percobaan 12 Okt→11 Jan 2027) |
| Asumsi disebut | ✅ tetapi asumsi "pakai masa percobaan" muncul karena default script `--jenis pkwtt` langsung menambah baris percobaan. SKILL.md tidak mengatur default jenis bila pengguna tidak menyebut. |
| Temuan | Evaluasi 90 hari (Senin 11 Jan) jatuh **tepat pada** hari terakhir masa percobaan — tidak ada jeda untuk menyampaikan hasil. Bila pengguna hanya melihat baris "Evaluasi 90 hari / akhir orientasi (isi formulir evaluasi)", ia bisa terlambat. |
| Kasus lain | Bila tanggal mulai tidak diberikan di mode cepat, SKILL.md tidak menjelaskan fallback (tanggal relatif H+29 dst. atau wajib tanya). |
