# Skenario 02 — Kontraktor kecil, tender konstruksi HPS Rp2,4 miliar: jadwal mundur + checklist SBU/SKK

> Uji independen, 2026-09-25 (tanggal "hari ini" disimulasikan 15 Okt 2026 via `--hari-ini`). Output script apa adanya.

## Input pengguna
"CV saya kontraktor kecil, SBU BG001 kualifikasi kecil, KBLI 41012. Lagi pegang 3 proyek jalan. Ikut tender Rehabilitasi Gedung Puskesmas, HPS Rp2,4 miliar, pagu Rp2,5 M. Pengumuman 5/10, penjelasan 12/10, batas unggah 23/10/2026 jam 10.00. Tanggal 20 Oktober libur hari jadi kabupaten. Hari ini tanggal 15. Tolong jadwal & checklist SBU/SKK."

## Perintah
```
python3 scripts/cek_penawaran.py jadwal --batas "23/10/2026 10.00" --pengumuman 2026-10-05 --penjelasan 2026-10-12 --libur 2026-10-20 --hari-ini 2026-10-15 --konstruksi
```
(Tanpa `--jaminan`: HPS Rp2,4 M ≤ Rp10 M → jaminan penawaran umumnya tidak wajib; agent mengingatkan cek LDP.)

## Output script
```
JADWAL MUNDUR PENAWARAN - batas unggah Jumat, 23 Oktober 2026 pukul 10:00
Hari ini: Kamis, 15 Oktober 2026 | sisa hari kerja sebelum hari batas: 5
Hari kerja: Senin-Jumat; libur yang dikecualikan: 2026-10-20

[ ] Pengumuman   Senin, 5 Oktober 2026  [TERLEWAT - kerjakan segera]
      Unduh dokumen pemilihan dari SPSE; baca syarat kualifikasi, KBLI/SBU, metode evaluasi, HPS, jadwal. Putuskan ikut/tidak (cek kelayakan).
[ ] Penjelasan   Senin, 12 Oktober 2026  [TERLEWAT - kerjakan segera]
      Ikuti pemberian penjelasan (aanwijzing) di SPSE; ajukan pertanyaan tertulis sebelum sesi ditutup.
[ ] Penjelasan+1 Selasa, 13 Oktober 2026  [TERLEWAT - kerjakan segera]
      Cek Berita Acara Pemberian Penjelasan & adendum dokumen pemilihan; sesuaikan rencana penawaran.
[ ] H-7          Selasa, 13 Oktober 2026  [TERLEWAT - kerjakan segera]
      Kumpulkan dokumen: NIB & KBLI (OSS), NPWP, status PKP, akta & pengesahan, pengalaman/kontrak, tenaga ahli & peralatan. Cek masa berlaku semua izin/sertifikat. Cek SBU (subklasifikasi & kualifikasi) dan SKK personel, sisa kemampuan paket (SKP).
[ ] H-5          Kamis, 15 Oktober 2026  [HARI INI]
      Susun dokumen teknis: spesifikasi/brosur, metode pelaksanaan, jadwal, surat dukungan (bila diminta). Minta harga tertulis dari pemasok.
[ ] H-3          Senin, 19 Oktober 2026
      Finalisasi harga: jalankan cek_penawaran.py (volume x harga, PPN, total, % HPS, terbilang). Siapkan surat penawaran (masa berlaku sesuai dokumen), tanda tangan pihak berwenang.
[ ] H-2          Rabu, 21 Oktober 2026
      Pemeriksaan silang: checklist administrasi/teknis/harga; cocokkan nama paket, kode tender, nilai angka vs terbilang; cek format & ukuran file.
[ ] H-1          Kamis, 22 Oktober 2026
      UNGGAH penawaran lengkap di SPSE (jangan tunggu hari terakhir). Simpan bukti/tanda terima unggah; cek file terbaca.
[ ] H            Jumat, 23 Oktober 2026
      Batas akhir unggah pukul 10:00. Hanya perbaikan darurat; unggah ulang paling lambat beberapa jam sebelum batas. Pastikan status penawaran 'terkirim'.

Jadwal resmi selalu yang tertera di SPSE (bisa berubah lewat adendum). Cek ulang setiap hari.
```

## Jawaban agent
### Kelayakan: **IKUT DENGAN SYARAT**
| Butir | Status | Catatan |
|---|---|---|
| Paket untuk UMK (pagu ≤ Rp15 M) | ✅ | Pasal 65 Perpres 16/2018 jo. 46/2025 |
| SBU subklasifikasi & kualifikasi | ❓ | BG001 kecil — cocokkan subklasifikasi yang diminta LDK & masa berlaku |
| SKK personel manajerial (PM/PL, K3) | ❓ | Cek jabatan, jenjang & masa berlaku SKK di SIJK/LPJK |
| **SKP = 5 − 3 = 2** | ✅ | Masih boleh ikut (SKP > 0). Jika menang 2 paket lagi, SKP habis |
| Pengalaman | ❓ | Paket ≤ Rp2,5 M: usaha kecil berdiri < 3 th dapat dikecualikan — cek LDK (PERLU REVIEW) |
| Jaminan penawaran | ✅ tidak wajib | HPS ≤ Rp10 M — ikuti LDP |

### Checklist konstruksi tambahan (B1 teknis)
- [ ] SBU sesuai subklasifikasi (scan + nomor registrasi) — H-7 cek masa berlaku
- [ ] SKK personel manajerial sesuai jabatan & jenjang di LDP, tidak dipakai di paket lain yang sedang berjalan
- [ ] Daftar peralatan utama (milik/sewa + bukti)
- [ ] Metode pelaksanaan & jadwal ≤ jangka waktu
- [ ] Rencana Keselamatan Konstruksi (RKK) bila diminta
- [ ] Rincian harga (Daftar Kuantitas & Harga) — volume sama dengan BoQ dokumen, cek dengan `cek_penawaran.py harga`
- [ ] Perhitungan SKP ditulis di isian kualifikasi

### Jadwal — ringkas
Pengumuman, penjelasan, dan H-7 sudah lewat → **kumpulkan dokumen & cek SBU/SKK hari ini juga** bersamaan dengan H-5 (dokumen teknis). H-3 Senin 19/10 finalisasi harga; **20/10 libur (dilewati)**; H-2 Rabu 21/10 cek silang; **H-1 Kamis 22/10 unggah**; batas Jumat 23/10 pukul 10.00 (pagi — jangan rencanakan unggah di hari H).

Asumsi: tidak ada libur nasional lain 15–23 Okt 2026; Sabtu bukan hari kerja.
Disclaimer & dasar aturan sesuai SKILL.md.

## Verifikasi independen tanggal (manual kalender Okt 2026)
23/10 = Jumat ✅. Mundur hari kerja lewati Sab/Min & Selasa 20/10: H-1 Kam 22, H-2 Rab 21, H-3 Sen 19, H-4 Jum 16, H-5 Kam 15, H-6 Rab 14, H-7 Sel 13 ✅. Sisa hari kerja dari 15/10 s.d. 22/10 (termasuk hari ini): 15, 16, 19, 21, 22 = 5 ✅. Penjelasan+1 = Sel 13 ✅.

## Catatan temuan
- Pengumuman & Penjelasan (acara yang sudah lewat) diberi label "TERLEWAT - kerjakan segera" — menyesatkan untuk acara yang tidak bisa diulang (aanwijzing). Sebaiknya "SUDAH LEWAT — baca Berita Acara Penjelasan/adendum".
- Skill tidak menyebut **jaminan pelaksanaan 5% nilai kontrak** (kontrak > Rp200 jt) dan **PPh final konstruksi** (tarif kualifikasi kecil) untuk perencanaan kas kontraktor; hanya PPh 22 barang yang disebut.
