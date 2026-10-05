# Uji 01 (penguji independen, Akun B) - Toko skincare, TikTok Ads + TikTok Shop (GMV Max)

> Uji simulasi agent oleh penguji terpisah dari pembuat, 2026-09-26. Agent hanya membaca folder
> `skills/audit-akun-iklan/`. Data fiktif. Jenis skenario: **normal 1** (juga dipakai untuk uji A/B dan banding pesaing).

## Permintaan pengguna
"Tolong audit iklan skincare saya. Saya pakai TikTok Ads ke website (Shopify) Rp4,5 jt/bulan dan
iklan TikTok Shop (GMV Max) Rp6 jt/bulan. Serum 20 ml harga Rp89rb, modal Rp32rb. Potongan TikTok
Shop kira-kira 14,5% + komisi afiliasi 10%, kemas Rp1.500. Rasanya boncos."

## Perilaku agent (sesuai SKILL.md)
1. `daftar --platform tiktok,tiktokshop` → 28 cek (T01–T17, TS01–TS11).
2. Tanya sekali (7 pertanyaan: Events Manager, Business Center > Anggota, status ad group,
   pratinjau 3 video, laporan per video 14 hari, target ROI GMV Max, jam anggaran habis).
3. `roas-impas` dulu karena T09/TS02/TS04 membutuhkannya. Komisi afiliasi dimasukkan ke persen
   biaya sesuai catatan TS02 (14,5% + 10% = 24,5%).
4. Isi jawaban → `hitung` dengan belanja kedua platform.

## File jawaban (diringkas)
```
T01 lulus | T02 sebagian (Complete Payment 38 vs order nyata 52; kampanye B tak tercatat)
T03 gagal (freelancer lama masih admin, 2FA mati) | T04 lulus | T05 gagal (3/5 ad group Learning limited >10 hari)
T06 lulus | T07 tidak_tahu | T08 gagal (anggaran Rp100rb/hari, CPA Rp45rb) | T09 gagal (CPA Rp45rb > laba Rp33.695)
T10 sebagian | T11 gagal (produk muncul detik ke-6) | T12 gagal (1-2 video/ad group) | T13 lulus | T14 lulus
T15 gagal (video sama 6 minggu) | T16 tidak_berlaku (belum punya audiens pembeli) | T17 tidak_tahu
TS01 sebagian | TS02 gagal | TS03 lulus | TS04 gagal (target ROI 2,0 < impas 2,65) | TS05 gagal (habis 17.00, LIVE 19.00)
TS06 lulus (11 video, 8 afiliasi berizin) | TS07 sebagian | TS08 lulus | TS09 lulus | TS10 lulus | TS11 gagal
```

## Perintah & output script (dipotong seperlunya, angka apa adanya)
```
$ python3 scripts/skor_audit.py roas-impas --harga 89rb --modal 32rb --biaya-persen "24,5" --biaya-lain 1.500
Biaya platform        : Rp 21.805
Laba kotor/pesanan    : Rp 33.695
ROAS/ROI impas        : 2,65 (di bawah angka ini iklan rugi; dibulatkan ke atas)

$ python3 scripts/skor_audit.py hitung jawaban.csv --belanja tiktok=4,5jt --belanja tiktokshop=6jt --mulai 2026-09-28 --usaha "Glowria Skincare"
Skor gabungan: 53,9 / 100 (Perlu perbaikan) - FINAL; bobot: porsi belanja
- TikTok Ads Manager: 51,9/100 (Perlu perbaikan); bukti 95,8% (final); belanja Rp 4.500.000
    Pelacakan 75,0 | Struktur 27,3 | Audiens 100,0 | Anggaran 0,0 | Materi 46,4 | Halaman 100,0 | Frekuensi 0,0 | Pengecualian belum tahu
- Iklan TikTok Shop / Tokopedia: 55,3/100 (Perlu perbaikan); bukti 100,0% (final); belanja Rp 6.000.000
    Pelacakan 25,0 | Struktur 100,0 | Anggaran 0,0 | Materi 86,4 | Halaman 100,0 | Pengecualian 0,0
PRIORITAS: 1 T03 (15, +4,8) · 2 T02 (10, +5,3) · 3 TS04 (9, +15,0) · 4 T08 (9, +7,9) · 5 T09 (9, +7,9)
           6 TS02 (9, +7,5) · 7 TS01 (9, +3,8) · 8 T11 (6, +5,6) · 9 T12 (6, +5,6) · 10 TS07 (6, +3,4) ...
Rencana: Hari 1 T03,T02 · Hari 2 TS04,T08,T09 · Hari 3 TS02,TS01 · Hari 4 T11 · Hari 5 T12 · Hari 6 diam · Hari 7 laporan
Antrean berikutnya: TS07, T05, T10, TS11, TS05, T15
```

## Jawaban akhir agent (ringkas)
AUDIT AKUN IKLAN – Glowria Skincare (26 Sep 2026)
Skor: **53,9/100 – Perlu perbaikan – final** (bukti TikTok Ads 95,8%, TikTok Shop 100%)

3 MASALAH TERBESAR
1. **Akun iklan bisa dibajak** – freelancer lama masih admin & 2FA mati. Cabut aksesnya dan nyalakan
   verifikasi 2 langkah di Business Center (±15 menit).
2. **Target ROI GMV Max 2,0, padahal impas serum 2,65** – setiap pesanan lewat iklan rugi hingga
   ±Rp11rb. Naikkan target ROI ke ≥ 2,65 (±5 menit), lalu jangan diubah 3–5 hari.
3. **Pelacakan web meleset** – Complete Payment 38 vs order nyata 52, kampanye B tidak tercatat
   sama sekali. Cek event di Events Manager/Shopify (±1 jam, bisa minta pembuat web).
Rencana 7 hari & daftar tunggu disalin dari script. Yang belum bisa dinilai: T07 (audiens kustom), T17 (penempatan/Pangle).

## Catatan penguji
- Semua angka cocok dengan verifikasi independen (lihat `HASIL-UJI.md`).
- ⚠️ **Saran bertabrakan tidak ditangani skill:** T08 (anggaran ≥ 20× CPA = Rp900rb/hari) dan T09
  (CPA Rp45rb di atas laba Rp33.695 → matikan) dijadwalkan di hari yang sama. Menaikkan anggaran
  ad group yang sedang rugi adalah saran buruk. Agent penguji menulis "satukan ad group dulu; jangan
  menaikkan anggaran sebelum CPA di bawah Rp33.695" — tetapi itu inisiatif agent, SKILL.md tidak
  memintanya. Hal serupa: TS04 (naikkan target ROI) vs TS05 (anggaran habis sebelum LIVE).
- Komisi afiliasi dimasukkan ke persen biaya — sesuai petunjuk TS02. Baik.
