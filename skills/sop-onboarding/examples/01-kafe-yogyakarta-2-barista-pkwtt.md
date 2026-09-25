# Uji 01 — Kafe di Yogyakarta, 2 Barista Baru PKWTT (6 hari kerja, shift)

Penguji independen (Tahap 6), 25 September 2026. Agent pengguna hanya membaca folder `sop-onboarding/`.
Script dijalankan dari salinan di scratchpad.

## Input pengguna
> "Kafe saya di Yogyakarta nerima 2 barista baru, statusnya karyawan tetap (PKWTT). Mulai Senin 5 Oktober
> 2026. Kerja 6 hari seminggu, ada shift pagi & sore. Tolong bikinin paket onboarding lengkap."

Data yang tidak diberikan: nama kafe, nama barista, buddy, jam shift, aturan cuti, apakah memakai masa
percobaan. Karena pengguna meminta paket lengkap tanpa detail, agent **tidak bertanya ulang** (sesuai
SKILL.md: buat dengan data yang ada, tandai `[isi: ...]`, sebutkan asumsi).

## Perintah script
```bash
python3 scripts/jadwal_onboarding.py --mulai "Senin, 5 Oktober 2026" --hari-kerja 6 --jenis pkwtt \
  --nama "2 Barista Baru" --format markdown
```
Dijalankan ulang dengan `--libur libur-nasional-2026-2027.csv` (24–25 Des 2026, 1 & 5 Jan 2027, dst. dari
SKB 3 Menteri) → hasil **identik** (tidak ada tanggal jatuh di hari libur). Exit code 0.

---

# Paket Onboarding — 2 Barista Baru, [isi: Nama Kafe] Yogyakarta

**Asumsi yang dipakai (mohon koreksi bila salah):**
1. Kedua barista PKWTT **dengan masa percobaan 3 bulan** yang dicantumkan tertulis di perjanjian kerja /
   surat pengangkatan. Bila tidak dicantumkan tertulis, dianggap tidak ada masa percobaan.
2. Satu jadwal berlaku untuk kedua barista (mulai di hari yang sama).
3. Kafe libur hari Minggu (script `--hari-kerja 6` menganggap Minggu hari libur). Bila kafe buka Minggu
   dengan libur bergilir, tanggal "digeser" di bawah cukup disesuaikan dengan jadwal shift masing-masing.

## 1. Checklist Pra-Hari-Pertama
Usaha: [isi: Nama Kafe], Yogyakarta | Jabatan: Barista (2 orang) | Mulai kerja: Senin, 5 Oktober 2026 |
Disiapkan oleh: [isi: nama/jabatan]

### A. Dokumen dari karyawan (minta seperlunya, simpan aman — UU 27/2022 PDP)
| # | Dokumen | Barista 1 | Barista 2 | Catatan |
|---|---|---|---|---|
| 1 | Fotokopi/scan KTP | ☐ | ☐ | |
| 2 | NPWP atau NIK yang sudah terintegrasi NPWP | ☐ | ☐ | Untuk PPh 21 (lihat `slip-gaji-bpjs`) |
| 3 | Nomor rekening bank aktif | ☐ | ☐ | Nama rekening = nama KTP |
| 4 | Pas foto (untuk ID card) | ☐ | ☐ | |
| 5 | Sertifikat barista/pelatihan (bila disyaratkan) | ☐ | ☐ | Salinan saja, **jangan tahan dokumen asli** |
| 6 | Kartu keluarga (hanya bila mendaftarkan tanggungan BPJS Kesehatan) | ☐ | ☐ | |
| 7 | Surat keterangan sehat/food handler (bila disyaratkan Pemda/kebijakan kafe) | ☐ | ☐ | Varian kafe |
| 8 | Pernyataan kerahasiaan & penggunaan data (ditandatangani) | ☐ | ☐ | `templates/pernyataan-kerahasiaan.md` |

⚠️ Minta dokumen yang benar-benar diperlukan saja. Simpan salinan KTP/KK di map terkunci atau folder
digital berpassword dengan akses terbatas (pemilik/HR), **bukan** di grup WA atau komputer kasir bersama.

### B. Pendaftaran & administrasi (WAJIB)
| # | Tugas | Penanggung jawab | Selesai? | Catatan |
|---|---|---|---|---|
| 9 | Daftarkan BPJS Ketenagakerjaan (JKK, JKM, JHT; JP bila berlaku) | [isi] | ☐ | Wajib, paling lambat 30 hari sejak mulai kerja → **target sebelum 3 November 2026** |
| 10 | Daftarkan BPJS Kesehatan | [isi] | ☐ | Wajib |
| 11 | Perjanjian kerja PKWTT siap tanda tangan | [isi] | ☐ | Bila memakai masa percobaan: tulis tegas, **maks. 3 bulan**, upah selama percobaan tidak di bawah upah minimum yang berlaku |
| 12 | Daftarkan di absensi/payroll | [isi] | ☐ | |
| 13 | ID card / name tag | [isi] | ☐ | |

### C. Perangkat & akun kerja
| # | Item | Penanggung jawab | Selesai? |
|---|---|---|---|
| 14 | Apron/seragam, name tag, sepatu tertutup anti-slip | [isi] | ☐ |
| 15 | Akses aplikasi kasir/POS & akun pemesanan online (bila barista merangkap kasir) | [isi] | ☐ |
| 16 | Loker & tempat simpan barang pribadi | [isi] | ☐ |
| 17 | Resep standar minuman (recipe card) & takaran | [isi] | ☐ |

### D. Persiapan tim
| # | Tugas | Penanggung jawab | Selesai? |
|---|---|---|---|
| 18 | Tentukan buddy **di shift yang sama** minimal 2 minggu pertama | [isi] | ☐ |
| 19 | Susun jadwal shift minggu 1–2 (usahakan barista baru tidak langsung sendirian di shift sibuk) | [isi] | ☐ |
| 20 | Kirim pengumuman ke grup tim | [isi] | ☐ |
| 21 | Cetak buku saku karyawan | [isi] | ☐ |

Bila ada dokumen belum lengkap di H1, tetap sambut dan jadwalkan susulan maks. 1 minggu — **kecuali**
BPJS (paling lambat 30 hari) dan perjanjian kerja (tandatangani sebelum/saat H1).

## 2. Jadwal Onboarding (H1 – 90 Hari)
(Tabel disalin dari output script.)

| Tahap | Tanggal target | Tanggal disesuaikan | Digeser? | Penanggung jawab | Kegiatan |
|---|---|---|---|---|---|
| Hari pertama (H1) | 5 Oktober 2026 | 5 Oktober 2026 | Tidak | Pemilik/Atasan langsung | Penyambutan, serah terima perangkat & akun, penjelasan buku saku karyawan |
| Akhir minggu 1 | 11 Oktober 2026 | 12 Oktober 2026 | Ya | Buddy/rekan pendamping | Cek pemahaman tugas dasar & SOP harian, tanya kendala |
| Evaluasi 30 hari | 3 November 2026 | 3 November 2026 | Tidak | Atasan langsung | Evaluasi checklist tugas dasar; beri umpan balik tertulis singkat |
| Evaluasi 60 hari | 3 Desember 2026 | 3 Desember 2026 | Tidak | Atasan langsung | Evaluasi kemandirian kerja & kepatuhan SOP |
| Evaluasi 90 hari / akhir orientasi | 2 Januari 2027 | 2 Januari 2027 | Tidak | Pemilik/Atasan | Evaluasi akhir masa orientasi (isi formulir evaluasi) |
| Akhir masa percobaan (batas hukum) | 4 Januari 2027 | 4 Januari 2027 | Tidak | Pemilik/Atasan | Keputusan lanjut sebagai karyawan tetap atau tidak (evaluasi disarankan selesai paling lambat hari kerja ini, SEBELUM tanggal hukum berakhir) |

- **Akhir masa percobaan (batas hukum)**: Masa percobaan maks. 3 bulan, upah selama percobaan tidak boleh
  di bawah upah minimum (UU 13/2003 Pasal 60 jo. UU 6/2023). Tanggal ini TIDAK digeser walau libur; hanya
  tanggal evaluasi yang disarankan dimajukan.

**Target khusus barista (ditambahkan agent, sesuaikan):**
| Titik | Target yang bisa dicek |
|---|---|
| H1 | Tur area bar & dapur, aturan higiene, kenalan tim shift, shadowing buddy |
| Minggu 1 | Bisa menyiapkan 5 menu terlaris sesuai recipe card dengan pengawasan; paham buka/tutup bar |
| Hari 30 | Seluruh menu kopi inti sesuai standar rasa & waktu saji [isi: target menit]; kalibrasi grinder dasar |
| Hari 60 | Pegang shift bersama tanpa pendampingan penuh; tangani komplain ringan sesuai SOP |
| Hari 90 | Mandiri di jam sibuk; bisa closing bar & stok bahan harian |

Catatan shift: untuk 2 minggu pertama, tempatkan setiap barista di shift yang sama dengan buddy-nya.

## 3. Pesan Sambutan & Pengumuman Tim
**WA ke masing-masing barista (kirim 1–3 hari sebelum H1, mis. Jumat 2 Oktober 2026):**
```
Halo [Nama]! 🎉

Selamat bergabung di [Nama Kafe] sebagai Barista. Kami senang kamu akan mulai bekerja
pada Senin, 5 Oktober 2026 pukul [isi: jam masuk shift].

Beberapa info penting untuk hari pertama:
📍 Lokasi: [isi: alamat/patokan kafe]
👤 Yang akan menyambut: [isi: nama & jabatan]
👕 Pakaian: [isi: mis. kaos hitam polos, celana panjang, sepatu tertutup — apron disediakan]
📄 Dokumen yang perlu dibawa: KTP asli (untuk dicocokkan), buku/nomor rekening, NPWP bila ada

Kalau ada pertanyaan sebelum hari-H, langsung hubungi saya ya di nomor ini.
Sampai jumpa Senin!

Salam,
[Nama pengirim], [Jabatan]
```

**Pengumuman ke grup WA tim:**
```
Halo tim! 👋

Mulai Senin, 5 Oktober 2026, kita kedatangan 2 barista baru:

👤 [Nama 1] — Barista, shift [isi]
👤 [Nama 2] — Barista, shift [isi]
🤝 Buddy pendamping: [isi nama buddy 1] untuk [Nama 1], [isi nama buddy 2] untuk [Nama 2]
   — tolong dampingi di 2 minggu pertama ya!

Yuk sambut dengan ramah dan bantu kalau ada yang ditanyakan. Terima kasih! 🙏

[Nama pengirim]
```

## 4. Buku Saku Karyawan (ringkas) — [Nama Kafe]
Versi 1.0 | Berlaku mulai 5 Oktober 2026

1. **Jam kerja**: Senin–Sabtu (6 hari) · Shift pagi [isi: jam] · Shift sore [isi: jam] · Istirahat [isi] ·
   Toleransi terlambat [isi].
2. **Cuti & izin**: Cuti tahunan [isi: sesuai aturan kafe, minimal 12 hari kerja setelah 12 bulan bekerja
   terus-menerus] · Cara mengajukan [isi] · Izin sakit [isi] · Tukar shift: [isi: izin siapa].
3. **Seragam & penampilan**: [isi: apron, rambut diikat/penutup kepala, kuku pendek, tanpa perhiasan
   tangan saat meracik].
4. **Higiene**: cuci tangan sebelum meracik & setelah dari toilet/pegang uang; bahan dengan label tanggal
   buka; [isi: aturan cicip menu]; tanyakan alergi pelanggan bila memesan menu dengan kacang/susu.
5. **HP & perangkat**: [isi: mis. HP disimpan di loker saat di bar].
6. **Layanan pelanggan**: [isi — rujuk SOP komplain/closing kasir dari `sop-writer` bila sudah ada].
7. **Kerahasiaan**: data pelanggan (nomor WA, pesanan online) & data kafe tidak boleh disebar (UU 27/2022).
8. **Siapa yang dihubungi**: Buddy [isi] · Kepala shift [isi] · Gaji/BPJS/cuti: [isi] · Darurat: [isi].

⚠️ Bagian `[isi: ...]` wajib diisi sebelum dicetak — agent tidak mengarang jam kerja atau jumlah cuti.

## 5. Formulir Evaluasi Akhir Orientasi
Nama: [Nama barista] | Jabatan: Barista | Mulai kerja: 5 Oktober 2026 | **Tanggal evaluasi: Sabtu,
2 Januari 2027** (paling lambat Senin, 4 Januari 2027 — batas akhir masa percobaan) | Jenis: PKWTT (masa
percobaan)

A. Penilaian kompetensi (skala 1–5): kepatuhan SOP & higiene · kualitas rasa & konsistensi resep · kecepatan
saji jam sibuk · kehadiran · kerja sama tim · sikap ke pelanggan · kemauan belajar → total [isi]/35.
B. Target: Hari 30 (3 Nov 2026) [isi] · Hari 60 (3 Des 2026) [isi] · Hari 90 (2 Jan 2027) [isi].
C. Catatan kualitatif.
D. Keputusan: ☐ Lanjut (lulus percobaan) · ☐ Perpanjang pemantauan (**masa percobaan tidak boleh melewati
4 Januari 2027**) · ☐ Tidak dilanjutkan — konsultasikan ke ahli hukum ketenagakerjaan/Disnaker sebelum
memutus hubungan kerja, termasuk saat masih masa percobaan.

Catatan penyesuaian jenis usaha: varian **Kafe/restoran** — dokumen kesehatan/food handler, higiene &
alergi di buku saku, buddy per shift, target barista spesifik.
Data yang masih perlu dilengkapi: nama kafe & barista, buddy, jam shift, aturan cuti/izin, seragam,
alamat, kontak.
Disclaimer: Paket ini alat bantu administrasi HR, bukan nasihat hukum. Dasar: UU 13/2003 Pasal 58 & 60 jo.
UU 6/2023; PP 35/2021; UU 24/2011; UU 27/2022 (dicek 25 September 2026). Aturan ketenagakerjaan bisa
berubah (RUU Pelindungan Ketenagakerjaan). Untuk keputusan PHK/kontrak, konsultasikan ahli hukum/Disnaker.

Tawaran lanjutan: perjanjian kerja → (PKWTT di luar cakupan template) / PKWT → `kontrak-kerja-pkwt`; SOP
buka-tutup bar & higiene → `sop-writer`; slip gaji & iuran BPJS → `slip-gaji-bpjs`.

---
## Penilaian penguji
| Kriteria | Hasil |
|---|---|
| Tanggal dari script, cocok verifikasi mandiri | ✅ (H1 5 Okt; mg1 11→12 Okt; 30=3 Nov; 60=3 Des; 90=2 Jan 2027; akhir percobaan 4 Jan 2027) |
| Masa percobaan maks. 3 bulan + upah minimum | ✅ |
| BPJS wajib + batas 30 hari | ✅ |
| PDP/minimisasi | ✅ |
| Tidak mengarang jam/cuti | ✅ |
| Kekurangan | Script tidak punya target per jabatan (agent harus menambah sendiri); "akhir minggu 1" digeser ke Senin minggu ke-2; nuansa upah minimum usaha mikro/kecil (kafe kecil) tidak dijelaskan; asumsi "pakai masa percobaan" diambil karena default script `pkwtt` |
