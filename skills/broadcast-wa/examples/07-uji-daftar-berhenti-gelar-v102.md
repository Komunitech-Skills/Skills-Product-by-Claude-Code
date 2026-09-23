# 07 — Uji ulang v1.0.2: daftar berhenti bercatatan, opt-out palsu, gelar ganda

## Skenario
Uji ulang perbaikan v1.0.2 atas cacat v1.0.1 (B3 daftar berhenti bercatatan, S-1 opt-out salah lolos, S-2 gelar).
Penguji merancang data baru: `stop.txt` 24 baris dengan catatan gaya admin toko (tanggal, jam, nama, hitungan, nomor urut,
dua nomor per baris) untuk 26 nomor sasaran, file kontak berisi ke-26 nomor itu + 5 kontak aman; 19 teks berhenti
(9 palsu, 10 sah); dan 29 nama bergelar/berkombinasi. Harapan ditulis sebelum script dijalankan. Kerja di
`/tmp/uji-broadcast-wa-v102/`, nomor fiktif 0812-0000-0xxx.

## Input pengguna
```
Ini daftar yang udah minta stop dari catatan HP admin, aku copas aja ke stop.txt ya, maaf berantakan ada tanggal
sama catatannya. Kontaknya di kontak.csv. Pesannya yang kemarin aja.
```

## Output (mengikuti SKILL.md v1.0.2, langkah 4)

## Broadcast WA — hasil pengolahan kontak

⚠️ **Status: PERIKSA DULU — jangan kirim dulu.**
Daftar berhenti: 24 nomor terbaca, tetapi **2 baris tidak bisa dibaca** nomornya:
- baris 15 `5. 0812-0000-0215`
- baris 16 `1) 0812 0000 0216`

Tolong rapikan dua baris itu (hapus nomor urut "5." dan "1)" di depannya, cukup nomornya saja), lalu saya jalankan ulang.
Orang di baris itu sudah minta berhenti dan saat ini **masih ada** di daftar kirim.

Sementara ini: siap kirim 12 dari 31 kontak | dilewati 19 (ada di daftar berhenti).
File: `broadcast_siap.csv` — **jangan dipakai sebelum dijalankan ulang.**

### Sebelum kirim (UU PDP)
- [ ] Semua baris stop.txt terbaca (status SIAP)
- [ ] Yang membalas STOP/BERHENTI tidak dikirimi lagi
- [ ] File kontak disimpan aman, tidak dibagikan

*(Catatan penguji: output di atas adalah yang akan dilaporkan agent dengan jujur dari ringkasan script. Agent **tidak tahu**
bahwa 5 kontak lain yang sudah minta berhenti juga lolos — lihat tabel di bawah. Setelah pengguna merapikan baris 15–16,
status menjadi SIAP dan 5 kontak itu tetap terkirimi.)*

## Tabel verifikasi daftar berhenti (24 baris, 26 nomor sasaran)

| # | Baris di stop.txt | Nomor yang dimaksud | Dibaca script sebagai | Status | Hasil |
|---|---|---|---|---|---|
| 1 | `0812-0000-0120 tgl 12/09` | 0812-0000-0120 | 6281200000120 | - | dikecualikan ✔ |
| 2 | `Galih 0812 0000 0139 (minta stop 2026-09-01)` | 0812-0000-0139 | 6281200000139 | - | dikecualikan ✔ |
| 3 | `0812 0000 0201 12 Sept 2026` | 0812-0000-0201 | 628120000020112 | - | **TETAP DIKIRIMI — diam-diam** ✘ |
| 4 | `0812-0000-0202 - 3x minta` | 0812-0000-0202 | 62812000002023 | - | **TETAP DIKIRIMI — diam-diam** ✘ |
| 5 | `0812-0000-0203 (2)` | 0812-0000-0203 | 62812000002032 | - | **TETAP DIKIRIMI — diam-diam** ✘ |
| 6 | `0812 0000 0204 jam 10.30` | 0812-0000-0204 | 6281200000204 | - | dikecualikan ✔ |
| 7 | `+62 812 0000 0205 / via DM` | 0812-0000-0205 | 6281200000205 | - | dikecualikan ✔ |
| 8 | `Bu Ros: 0812-0000-0206, udah 2 kali komplain` | 0812-0000-0206 | 6281200000206 | - | dikecualikan ✔ |
| 9 | `0812-0000-0207 0812-0000-0208` | 0812-0000-0207 / 0812-0000-0208 | 6281200000207, 6281200000208 | - | dikecualikan ✔ |
| 10 | `0812-0000-0209,0812-0000-0210` | 0812-0000-0209 / 0812-0000-0210 | 6281200000209, 6281200000210 | - | dikecualikan ✔ |
| 11 | `081200000211 stop 25/9` | 0812-0000-0211 | 6281200000211 | - | dikecualikan ✔ |
| 12 | `Pak Dedi (0812) 0000-0212 blokir` | 0812-0000-0212 | 6281200000212 | - | dikecualikan ✔ |
| 13 | `0812.0000.0213` | 0812-0000-0213 | 6281200000213 | - | dikecualikan ✔ |
| 14 | `0812-0000-0214 no.5` | 0812-0000-0214 | 6281200000214 | - | dikecualikan ✔ |
| 15 | `5. 0812-0000-0215` | 0812-0000-0215 | (tidak terbaca) | PERIKSA DULU | tetap di file kirim, tapi status PERIKSA DULU ⚠ |
| 16 | `1) 0812 0000 0216` | 0812-0000-0216 | (tidak terbaca) | PERIKSA DULU | tetap di file kirim, tapi status PERIKSA DULU ⚠ |
| 17 | `0812-0000-0217 ke-2` | 0812-0000-0217 | 6281200000217 | - | dikecualikan ✔ |
| 18 | `0062 812 0000 0218 (TKI Malaysia)` | 0812-0000-0218 | 6281200000218 | - | dikecualikan ✔ |
| 19 | `0812-0000-0219 minta stop 2026` | 0812-0000-0219 | 6281200000219 | - | dikecualikan ✔ |
| 20 | `0812-0000-0220 RT 03 RW 05` | 0812-0000-0220 | 6281200000220 | - | dikecualikan ✔ |
| 21 | `0812 0000 0221 25 September` | 0812-0000-0221 | 628120000022125 | - | **TETAP DIKIRIMI — diam-diam** ✘ |
| 22 | `Andi 812 0000 0222` | 0812-0000-0222 | 6281200000222 | - | dikecualikan ✔ |
| 23 | `0812-0000-0223 x2` | 0812-0000-0223 | 6281200000223 | - | dikecualikan ✔ |
| 24 | `0812 0000 0224 - 17 Agustus` | 0812-0000-0224 | 628120000022417 | - | **TETAP DIKIRIMI — diam-diam** ✘ |

**Rekap:** 17 baris (19 nomor) dikecualikan dengan benar; 2 baris (nomor urut di depan) ditandai PERIKSA DULU;
**5 baris dibaca menjadi nomor yang salah tanpa peringatan apa pun** — angka kecil di belakang nomor (tanggal "12 Sept",
"25 September", "17 Agustus", hitungan "(2)", "3x") ikut tergabung, hasilnya 14–15 digit yang masih dianggap "valid".
Daftar kirim akhir memuat 7 kontak yang sudah minta berhenti (5 tanpa tanda + 2 bertanda PERIKSA DULU).

## Teks berhenti (cek "instruksi tindakan" v1.0.2)

| Teks variasi | Harapan | Hasil v1.0.2 |
|---|---|---|
| "promo non-stop sepanjang hari!" | tolak | DITOLAK ✔ |
| "siapa yang tidak mau dapat diskon 50%?" | tolak | DITOLAK ✔ |
| "kalau tidak ingin menerima kabar diskon, sayang banget lho" | tolak | DITOLAK ✔ |
| "beli sekarang untuk berhenti pusing mikir lauk!" | tolak | DITOLAK ✔ |
| "Bus stop Senen … Kirim stoples kosongnya ya" | tolak | DITOLAK ✔ |
| "diskon unsubscribe-proof!" | tolak | DITOLAK ✔ |
| "**jangan balas STOP ya**, nanti rugi!" | tolak | LOLOS ✘ |
| "pokoknya **jangan sampai kirim berhenti**" | tolak | LOLOS ✘ |
| "Ketik **stop-motion** di IG kami" | tolak | LOLOS ✘ |
| "Tidak ingin menerima info promo lagi? Balas STOP." | lolos | LOLOS ✔ |
| "Balas \*STOP\* untuk berhenti." / "Balas “BERHENTI” …" / "Balas 'stop' bila tidak berkenan." | lolos | LOLOS ✔ |
| "Mau berhenti terima info? Balas STOP/BERHENTI." / "Reply STOP to unsubscribe." | lolos | LOLOS ✔ |
| "Balas **dengan kata** STOP jika tidak ingin dikirimi lagi." | lolos | DITOLAK ✘ (aman, tapi mengganggu) |
| "cukup **balas: STOP**" | lolos | DITOLAK ✘ (aman) |
| "**Balas ke nomor ini dengan** STOP untuk berhenti." | lolos | DITOLAK ✘ (aman) |

Tiga salah lolos memerlukan kalimat yang sengaja menyesatkan/kebetulan ("jangan balas STOP", "stop-motion"); teks buatan
agent yang mengikuti SKILL.md selalu sah. Tiga salah tolak bersifat aman (script berhenti dengan pesan jelas).

## Nama bergelar (mode default = nama depan)

| Nama di file | Hasil | |
|---|---|---|
| Hj. Dr. Ir. Siti Aminah, S.E., M.M. | Bu Siti | ✔ |
| Prof. Dr. H. Ahmad Syafii | Pak Ahmad | ✔ |
| Bu Hj. Dra. Ratna / Pak H. Ir. Budi / Ir. Hj. Lina | Bu Ratna / Pak Budi / Bu Lina | ✔ |
| IBU HJ. AMINAH / Hj Aminah / Hajjah Fatimah / Ustadzah Nur | Bu Aminah / Bu Aminah / Bu Fatimah / Bu Nur | ✔ |
| H. Rahmat / Haji Lulung / KH. Ma'ruf / Drs. H. Tono, M.Si. | Pak Rahmat / Pak Lulung / Pak Ma'ruf / Pak Tono | ✔ |
| dr. Andi / Sdr. Andi Wijaya / Andi, S.T. / NUR / Hj. | Kak Andi / Kak Andi / Kak Andi / Kak Nur / Bu | ✔ |
| Bang H. Rhoma / Dra. Hj. Sri Mulyani, M.Pd. | Bang Rhoma / Bu Sri | ✔ |
| **Hj.Nurul** / **Dr.Rina** (tanpa spasi) | Kak Hj.nurul / Kak Dr.rina | ✘ |
| **H.M. Yusuf** | Kak H.m. | ✘ |
| **Muh. Rizki** / **Ny. Susi** / **Tn. Budi** | Kak Muh. / Kak Ny. / Kak Tn. | ✘ |
| Kapten Budi / Cut Nyak Dien | Kak Kapten / Kak Cut | ± (jarang) |

Dengan `--nama-lengkap`: gelar belakang bertitik tetap terbawa ("Bu Siti Aminah S.e. M.m.", "Pak Tono M.si.", "Kak Andi S.t.").

## Catatan penguji
- **Perbaikan nyata:** format catatan yang paling umum (tanggal lengkap, "tgl 12/09", jam, nama di depan, koma/spasi
  antar dua nomor, 0062, tanpa nol) kini terbaca; ada status PERIKSA DULU dan jumlah nomor terbaca. Opt-out palsu dari uji
  v1.0.1 kini ditolak. Gelar depan (termasuk bertumpuk) dirapikan dengan benar pada mode default.
- **Masih bocor (berat):** angka kecil di belakang nomor bergabung ke nomor tanpa peringatan (5/24 baris). Penulisan
  "0812… 25 September" atau "(2)" sangat wajar untuk admin toko.
- Sisa lain (ringan): nomor urut di depan hanya ditandai, tidak diperbaiki; opt-out yang sengaja menyesatkan; gelar tanpa
  spasi / Ny. / Tn. / Muh.
