# Uji Pembuat 01 — Kasir Baru Toko Bangunan (PKWTT, 6 hari kerja)

Uji cepat oleh pembuat skill (bukan pengujian independen Tahap 6 — itu dilakukan agent/sesi terpisah).

## Input pengguna
"Tolong buatin paket onboarding buat kasir baru namanya Sinta di toko bangunan saya di Sidoarjo, mulai
kerja Senin 28 September 2026, kontraknya PKWTT langsung (tanpa masa percobaan tidak, pakai masa
percobaan biasa), buddy-nya Rina (kasir senior), toko buka 6 hari seminggu."

## Perintah script yang dijalankan
```bash
python3 scripts/jadwal_onboarding.py --mulai "28 September 2026" --hari-kerja 6 --jenis pkwtt \
  --nama "Sinta" --format markdown
```

## Output script (disalin persis)
```
# Jadwal Onboarding — Sinta

Mulai kerja: **Senin, 28 September 2026**  |  Hari kerja/minggu: **6**  |  Jenis: **PKWTT**

| Tahap | Tanggal target | Tanggal disesuaikan | Digeser? | Penanggung jawab | Kegiatan |
|---|---|---|---|---|---|
| Hari pertama (H1) | 28 September 2026 | 28 September 2026 | Tidak | Pemilik/Atasan langsung | Penyambutan, serah terima perangkat & akun, penjelasan buku saku karyawan |
| Akhir minggu 1 | 4 Oktober 2026 | 5 Oktober 2026 | Ya | Buddy/rekan pendamping | Cek pemahaman tugas dasar & SOP harian, tanya kendala |
| Evaluasi 30 hari | 27 Oktober 2026 | 27 Oktober 2026 | Tidak | Atasan langsung | Evaluasi checklist tugas dasar; beri umpan balik tertulis singkat |
| Evaluasi 60 hari | 26 November 2026 | 26 November 2026 | Tidak | Atasan langsung | Evaluasi kemandirian kerja & kepatuhan SOP |
| Evaluasi 90 hari / akhir orientasi | 26 Desember 2026 | 26 Desember 2026 | Tidak | Pemilik/Atasan | Evaluasi akhir masa orientasi (isi formulir evaluasi) |
| Akhir masa percobaan (batas hukum) | 27 Desember 2026 | 26 Desember 2026 | Ya | Pemilik/Atasan | Keputusan lanjut sebagai karyawan tetap atau tidak (evaluasi disarankan selesai paling lambat hari kerja ini, SEBELUM tanggal hukum berakhir) |

- **Akhir masa percobaan (batas hukum)**: Masa percobaan maks. 3 bulan, upah selama percobaan tidak
  boleh di bawah upah minimum (UU 13/2003 Pasal 60 jo. UU 6/2023). Tanggal ini TIDAK digeser walau libur;
  hanya tanggal evaluasi yang disarankan dimajukan.
```
Verifikasi manual: 28 September 2026 + 3 bulan = 28 Desember 2026; dikurangi 1 hari = 27 Desember 2026
(Minggu, hari libur karena `--hari-kerja 6` hanya menganggap Minggu libur) → digeser mundur ke Sabtu 26
Desember 2026 untuk tanggal evaluasi disarankan. Cocok dengan output script.

## Ringkasan bagian lain yang dihasilkan agent (dipersingkat)
1. **Checklist pra-hari-pertama**: KTP, NPWP/NIK, rekening, dan mengingatkan pendaftaran BPJS
   Ketenagakerjaan & Kesehatan sebagai wajib (bukan opsional); mengarahkan kontrak PKWTT (dengan atau
   tanpa masa percobaan, sesuai pilihan pemilik) di luar cakupan skill ini.
2. **Pesan sambutan WA** untuk Sinta (versi santai, cocok toko) + pengumuman ke tim menyebut Rina sebagai
   buddy.
3. **Buku saku karyawan** dengan bagian jam kerja, seragam, dan SOP kasir ditandai `[isi: ...]` karena
   pemilik belum memberi detail jam operasional — agent bertanya balik sebelum menuntaskan bagian ini.
4. **Formulir evaluasi** dengan tanggal evaluasi diisi 26 Desember 2026 dari tabel di atas, dan catatan
   bahwa keputusan tidak lanjut perlu konsultasi ahli hukum/Disnaker.

## Catatan hasil uji pembuat
- Jenis usaha "toko bangunan" dipetakan ke varian **Toko/retail** di `references/varian-jenis-usaha.md`.
- Script mengembalikan kode keluar 0 dan tabel Markdown valid; tidak ada `[isi: ...]` yang tertinggal di
  jadwal karena semua tanggal dihitung otomatis.
- Bagian buku saku correctly ditandai `[isi: ...]` untuk data yang tidak diberikan pengguna (jam kerja,
  cuti) — sesuai aturan "jangan mengarang" di SKILL.md.
