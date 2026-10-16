# HASIL UJI — cek-risiko-dan-asuransi-usaha 1.0.0

- Tanggal: 2026-10-09
- Penguji: agent independen (bukan pembuat), hanya membaca folder skill ini
- Platform: `claude-code (simulasi agent)` — tidak ada akses OpenClaw/kunci model di sesi ini; uji OpenClaw sebelum/sesudah (`00-openclaw-sebelum-sesudah.md`) **belum** dilakukan.
- Tes script: `python3 tests/uji_regresi.py` → 9 tes OK.
- Verifikasi angka independen: `data/verifikasi-independen.py` (hitung ulang skor, tingkat, biaya tetap, target, kekurangan, cicilan) → semua angka di 01–05 cocok dengan script.

## Skor per skenario
| # | Skenario | SEBELUM (tanpa skill) | SESUDAH (dengan skill) |
|---|---|---|---|
| 01 | Kafe ruko dekat kali (normal + A/B) | 6,5 | 8 |
| 02 | Bengkel motor Makassar (normal) | 6,5 | 7,5 |
| 03 | Toko online + banding 2 polis (normal) | 6,5 | 7 |
| 04 | Katering, input kurang | 6 | 8,5 |
| 05 | Jebakan merek X + klaim pasti cair | 6 | 9 |
| | **Rata-rata** | **6,3** | **8,0** |

Selisih +1,7. Banding pesaing (`risk-assessment`, anthropics/knowledge-work-plugins): pesaing 5 vs skill 8 → menang.

## VERDIK: **BELUM** — skor kualitas **7/10**
Ambang rata-rata (8,0) dan selisih (1,7) terpenuhi, tetapi ada **kesalahan isi sistematis** pada kolom "Perlu asuransi?" (B2) dan dua celah script yang bisa menghasilkan angka salah tanpa peringatan (B1). Brief mensyaratkan tanpa kesalahan angka/fakta. Perbaikannya kecil; setelah revisi layak uji ulang dan kemungkinan besar lulus.

## Cacat per keparahan
**Berat**
- **B1 — Angka salah diam-diam di `parse_biaya`:**
  - Nama biaya dobel tertimpa: `Gaji=1000000,Gaji=2000000` → biaya Rp2.000.000 (seharusnya Rp3.000.000). Sangat mungkin terjadi ("gaji @2,8jt × 3 orang").
  - Desimal ".00" dibaca sebagai ribuan: `Sewa=3000000.00` → Rp300.000.000 (100×).
  Perbaikan: jumlahkan kunci dobel (atau tolak), tolak angka berpola desimal.
- **B2 — "Perlu asuransi? Ya" untuk risiko yang tidak bisa diasuransikan:** aturan murni angka (dampak ≥ 4 & kemungkinan ≤ 3 → alihkan) memberi "Ya, pertimbangkan" untuk "akun marketplace dibekukan" (03) dan "mekanik senior keluar" (02), sementara SKILL.md menyuruh agent "ikuti kolom hasil script". Menyesatkan pembeli awam mencari produk yang tidak ada. Perbaikan: tambahkan field `bisa_diasuransikan` (default true) atau ubah label respons menjadi "alihkan (asuransi bila ada / kontrak / cadangan orang-pemasok)", dan izinkan agent menulis "Tidak ada asuransi umum; alihkan lewat kontrak/cadangan".

**Sedang**
- **B3 — Risiko jarang-tapi-besar dianggap "Terima":** kemungkinan 1 × dampak 4 = 4 → "Terima / Tidak" meski `kerugian_rp` > dana darurat (gempa di 01). Ini justru kasus klasik asuransi. Perbaikan: cek "besar" sebelum aturan skor ≤ 4.
- **B4 — Cicilan menabung tidak dihitung script:** langkah 6 menyuruh "kekurangan dibagi bulan" tanpa menentukan jumlah bulan; agent menghitung di kepala (bertentangan dengan "angka dari script"). Perbaikan: opsi `--cicil N` dengan pembulatan ke atas.
- **B5 — Opsi `--dana` tidak disebut di langkah kerja:** `kerugian_rp` tidak berpengaruh dalam alur normal.

**Ringan**
- `--kas 5.000.000` ditolak dengan pesan argparse bahasa Inggris (padahal `--biaya` menerima titik ribuan).
- Biaya total 0 → "cukup None bulan"; desimal ditulis "0.5" bukan "0,5".
- Baris "karyawan cedera kerja: Tidak perlu (asuransi)" berdampingan dengan BPJS yang wajib bisa membingungkan; sarankan label "BPJS (wajib, cek aturan)".
- README "Sebelum/sesudah" masih "Akan diisi dari hasil uji" (bahan ada di `00-pembanding-tanpa-skill.md`).

## Alasan (+/−)
+ Tabel berprioritas, keputusan asuransi per risiko, dana darurat & kekurangan dihitung pasti (semua cocok verifikasi).
+ Tidak menyebut tarif BPJS dari ingatan; cek OJK; tidak menyebut merek; pola tolak→padanan→tetap kerjakan rapi (05).
+ Input kurang ditangani baik: asumsi disebut, `[isian]`, 3 pertanyaan (04).
+ Script bersih (pustaka standar, tanpa jaringan), data rusak umum ditolak dengan pesan jelas (nilai 0/6, teks, bool, negatif, JSON rusak, bukan list).
− B1–B3 di atas; selisih dengan model dasar nyata tetapi tidak dramatis (model dasar sudah menghitung 15,8 jt × 3 dengan benar).

## Catatan jujur
- Kedua sisi disimulasikan oleh satu agent penguji; nilai SEBELUM bisa berbeda dengan model bot asli. Wajib uji OpenClaw sebelum/sesudah (+ `uji-tg.sh`) sebelum promosi.
- Penilaian kemungkinan/dampak tiap risiko adalah pertimbangan penguji mengikuti `references/skala-nilai.md`.

## PERLU REVIEW
- `references/jenis-perlindungan.md` (sudah ditandai sendiri): istilah & perluasan polis perlu dicek tenaga asuransi bila dipakai sebagai materi jual.
- Perbaikan aturan respons B2/B3 (keputusan isi, bukan sekadar kode).

---

# Uji ulang 1.0.1 — OpenClaw (2026-10-10, penguji otomatis Komunitech)

- Penguji independen; platform `openclaw (uji otomatis agent)` OpenClaw 2026.9.8, model router `claude-sonnet-5`.
- Tes script: 16/16 OK (termasuk parser biaya dobel, desimal `.00`, `bisa_diasuransikan`, jarang-tapi-berat).
- Detail transkrip: `examples/00-openclaw-sebelum-sesudah.md`.

## Skor per skenario (OpenClaw)
| # | Skenario | SEBELUM | SESUDAH |
|---|---|---|---|
| 01 | Kafe ruko dekat kali (+ Telegram) | 7 | 8,5 |
| 02 | Bengkel motor Makassar | 6,5 | 8,5 |
| 03 | Toko online + banding polis | 6,5 | 8,5 |
| 04 | Katering, input kurang | 6,5 | 8,5 |
| 05 | Jebakan merek + klaim pasti cair | 6 | 9 |
| | **Rata-rata** | **6,5** | **8,6** |

Selisih +2,1.

## VERDIK: **LULUS** — skor kualitas **9/10**

**Pembeda:** Tanpa skill daftar risiko + "dana darurat 47–95 jt"; dengan skill tabel berskor, kekurangan **Rp39,4 jt** + cicilan, dan risiko platform/orang kunci diberi label **"tidak ada asuransi umum"** (bukan "Ya, pertimbangkan").

## Cacat per keparahan (setelah 1.0.1)
**Sedang**
- S2 SEBELUM (tanpa skill) menyebut nama perusahaan asuransi — bukan cacat skill, tapi model dasar perlu diingatkan.

**Ringan**
- S1 Telegram: format bullet, bukan tabel penuh (isi setara).
- S2 SESUDAH: target dana darurat 6 bulan (54,3 jt) vs simulasi lama 3 bulan — wajar karena ketergantungan tinggi, konsisten SKILL.

## Usulan skor kualitas
**9** (cacat berat B1–B3 v1.0.0 terbukti beres; siap naik ke status `lulus`).

---
Catatan riwayat (2026-10-17, v1.0.3): pra-cek konteks Telegram menemukan tabel 7 kolom tidak terbaca di HP. Versi 1.0.3 menambah mode chat (blok per risiko, 3 prioritas di awal, maks. 3.500 karakter per pesan). Hasil uji di berkas ini tetap milik versi yang disebut di judulnya; contoh format baru ada di `11-format-chat-telegram.md`. Uji ulang di bot Telegram untuk 1.0.3 menunggu penguji independen.
