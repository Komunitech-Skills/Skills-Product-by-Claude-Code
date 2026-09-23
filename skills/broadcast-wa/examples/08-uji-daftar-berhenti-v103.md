# 08 — Uji ulang v1.0.3: daftar berhenti dengan jam, "x2", nomor kantor, nomor luar negeri, dua nomor + catatan

## Skenario
Uji ulang perbaikan B3′ (v1.0.3: tanggal/nomor urut/angka kecil dibersihkan sebelum membaca nomor + jaring pengaman
"nomor stop tidak cocok kontak mana pun → PERIKSA DULU" + kontak yang nomornya muncul sebagai deretan angka di baris stop
ikut dikecualikan). Data: 24 baris `stop_nakal.txt` dari uji v1.0.2 **ditambah 20 baris pola baru** rancangan penguji
(jam, "x2"/"2x"/"x 3", nomor kantor, nomor Malaysia/Singapura/AS, dua nomor + catatan dalam satu baris, nomor 11 & 13 digit,
link wa.me, nominal rupiah) → 44 baris untuk 48 nomor sasaran. File kontak: 48 nomor sasaran + 10 kontak kontrol yang
**tidak** minta berhenti (sebagian sengaja mirip nomor sasaran). Ditambah 15 baris format ekstrem (tanda hubung berspasi,
en dash, huruf O, angka full-width, format ilmiah Excel, CSV berkutip, `tel:`). Kerja di `/tmp/uji-broadcast-wa-v103/`,
nomor fiktif.

## Input pengguna
```
Ini daftar stop gabungan dari HP admin sama HP kantor, campur-campur ya ada nomor kantor, nomor luar negeri pelanggan
yang kerja di Malaysia, catatan jam, macem-macem. Kontaknya kontak.csv. Pesannya yang kemarin.
```

## Output (mengikuti SKILL.md v1.0.3, langkah 4)

## Broadcast WA — hasil pengolahan kontak

⚠️ **Status: PERIKSA DULU — cocokkan 5 baris ini sebelum mengirim.**
Daftar berhenti: 49 nomor terbaca dari 44 baris. Semua pelanggan yang ada di daftar berhenti **sudah dikecualikan**, tapi ada
baris yang perlu kamu lihat sebentar:
- baris 31, 32 — ada **nomor kantor** (021-…) yang bukan nomor WA; nomor HP di baris itu sudah terbaca.
- baris 33, 34 — ada **nomor luar negeri** (+60, +65) yang tidak bisa diproses; nomor Indonesia di baris 33 sudah terbaca.
- baris 35 — `+1 (812) 000-0310` terbaca sebagai nomor Indonesia 0812-000-0310 dan **tidak cocok** dengan kontak mana pun.
  Kalau itu memang nomor luar negeri, abaikan saja.

Siap kirim: **7** dari 58 kontak | Dilewati: 49 ada di daftar berhenti, 2 nomornya muncul di baris daftar berhenti
(cocok sebagian — baris 41: `0812-3456-78901`; periksa apakah 0812-3456-7890 / 0812-3456-789 memang orang yang sama).
File: `broadcast_siap.csv`.

**Konfirmasi dulu:** kalau 5 baris di atas sudah sesuai, siap kirim ke 7 kontak?

## Tabel verifikasi pola baru (baris 25–44; baris 1–24 = `stop_nakal.txt`, lihat 07)

Baris 1–24: **24/24 terbaca benar** (termasuk 5 baris yang bocor di v1.0.2 dan 2 baris bernomor urut).

| # | Baris di stop.txt | Sasaran | Dibaca v1.0.3 | Tanda |
|---|---|---|---|---|
| 25 | `0812-0000-0301 jam 14:30` | 0812-0000-0301 | 6281200000301 | - |
| 26 | `0812 0000 0302 pk 09.15 minta stop` | 0812-0000-0302 | 6281200000302 | - |
| 27 | `0812 0000 0303 jam 9 malam` | 0812-0000-0303 | 6281200000303 | - |
| 28 | `0812-0000-0304 x2` | 0812-0000-0304 | 6281200000304 | - |
| 29 | `0812 0000 0305 2x` | 0812-0000-0305 | 6281200000305 | - |
| 30 | `0812 0000 0306 x 3` | 0812-0000-0306 | 6281200000306 | - |
| 31 | `Kantor 021-5550-1234 / HP 0812-0000-0307` | 0812-0000-0307 | 6281200000307 | PERIKSA: bagian tak terbaca `02155501234` |
| 32 | `0812-0000-0308 (kantor: (021) 555 0000)` | 0812-0000-0308 | 6281200000308 | PERIKSA: bagian tak terbaca `(021)5550000` |
| 33 | `+60 12-345 6789 (Malaysia) — nomor lama 0812 0000 0309` | 0812-0000-0309 | 6281200000309 | PERIKSA: bagian tak terbaca `+60123456789` |
| 34 | `+65 8123 4567` | (bukan nomor Indonesia) | — | PERIKSA: bagian tak terbaca `+6581234567` |
| 35 | `+1 (812) 000-0310` | (bukan nomor Indonesia) | 628120000310 | PERIKSA: tidak cocok kontak |
| 36 | `0812-0000-0311 & 0812-0000-0312 (suami istri) stop 3/9` | 0812-0000-0311 + 0812-0000-0312 | 6281200000311, 6281200000312 | - |
| 37 | `0812 0000 0313/0813 0000 0313 x2 jam 10.00` | 0812-0000-0313 + 0813-0313 | 6281200000313, 6281300000313 | - |
| 38 | `Bu Ani 0812-0000-0314, Pak Budi 0812 0000 0315 - 2x` | 0812-0000-0314 + 0812-0000-0315 | 6281200000314, 6281200000315 | - |
| 39 | `0812 0000 0316 0812 0000 0317 25 Sept` | 0812-0000-0316 + 0812-0000-0317 | 6281200000316, 6281200000317 | - |
| 40 | `08120000318 (nomor 11 digit) 5 Okt` | 0812-0000-318 (11 digit) | 628120000318 | - |
| 41 | `0812-3456-78901 stop 12 Des` | 0812-3456-78901 (13 digit) | 62812345678901 | - |
| 42 | `wa.me/6281200000319 minta hapus` | 0812-0000-0319 | 6281200000319 | - |
| 43 | `0812-0000-0320 Rp 25.000 belum bayar` | 0812-0000-0320 | 6281200000320 | - |
| 44 | `0812 0000 0321 no 7` | 0812-0000-0321 | 6281200000321 | - |

**Verifikasi independen daftar kirim:** 48/48 nomor sasaran **tidak** ada di `broadcast_siap.csv` (bocor = 0). Dari 10 kontak
kontrol, 7 dikirimi; 3 dikecualikan: satu karena salah rancang penguji (nomornya sama dengan sasaran 0201, jadi benar
dikecualikan), dua (0812-3456-7890 dan 0812-3456-789) oleh jaring pengaman karena digitnya ada di dalam `0812-3456-78901`
— arah aman, dan dilaporkan dengan alasan "cocok sebagian — periksa baris itu". Kontrol yang mirip sasaran (0812-0000-2012,
-3010, -0330, 0812-5550-1234 yang digitnya mirip nomor kantor, 0812-0000-0310 vs `+1 (812) 000-0310`) tetap dikirimi ✔.

## Format ekstrem (15 baris, 15 sasaran + 1 kontrol)

| Baris stop | Dibaca | Hasil |
|---|---|---|
| `0812 - 0000 - 0331` (tanda hubung berspasi) | — (tidak terbaca, tanpa tanda) | dikecualikan oleh jaring pengaman ✔ |
| `0812–0000–0338` (en dash) | — (tidak terbaca, tanpa tanda) | dikecualikan oleh jaring pengaman ✔ |
| `O812-0000-0333` (huruf O di depan) | 6281200000333 | dikecualikan ✔ |
| `0812 0000 03 34`, `(+62) 812 0000 0335`, `+62-812-0000-0336`, `62 812-0000-0337` | benar | dikecualikan ✔ |
| `0812-0000-0341 ext. 12`, `0812-0000-0342;Bu Tuti;2026-09-01`, `"0812-0000-0343","Pak Joko"`, `tel:+6281200000344`, `0812 0000 0345.` | benar | dikecualikan ✔ |
| `０８１２０００００３３９` (angka full-width) | tak terbaca | **tetap di daftar kirim**, status PERIKSA DULU ⚠ |
| `8.12000003E+11` (format ilmiah Excel) | 62812000003 (presisi hilang) | **tetap di daftar kirim**, status PERIKSA DULU (tidak cocok kontak) ⚠ |
| `0812-OOOO-0332` (huruf O di tengah) | — | **TETAP DIKIRIMI tanpa tanda apa pun** ✘ |

Kontak kontrol (0812-0000-0999) dikirimi ✔.

## Catatan penguji
- **B3′ tertutup:** semua pola catatan realistis (tanggal angka/teks, jam, hitungan "x2"/"(2)"/"- 3x", nomor urut, nominal
  rupiah, "no 7", nomor kantor, nomor luar negeri, dua nomor + catatan) terbaca benar — 44/44 baris, 0 bocor. Jaring
  pengaman menangkap format yang parser-nya gagal (tanda hubung berspasi, en dash) tanpa perlu tanda.
- Status PERIKSA DULU kini juga muncul untuk hal yang sebenarnya sudah aman (nomor kantor/luar negeri di baris stop). Ini
  menambah satu langkah cek bagi pengguna, tapi arahnya aman.
- **Sisa (sedang):** baris stop yang tidak menghasilkan nomor sama sekali dan tidak punya deretan angka panjang
  (mis. huruf O di tengah nomor, atau "Bu Tuti minta stop" tanpa nomor) tidak diberi tanda — orangnya tetap dikirimi.
- Sisa ringan: jaring pengaman bisa mengecualikan nomor mirip (arah aman); angka full-width/format ilmiah hanya ditandai.
