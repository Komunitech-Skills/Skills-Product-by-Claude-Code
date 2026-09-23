# 06 — Uji data tepi: file kontak "nakal" 55 baris + daftar berhenti (v1.0.1, diulang di v1.0.2)

## Skenario
Uji ulang cacat berat v1.0.0 (B1: kolom Berhenti berisi "STOP"/"x"/tanggal tidak dianggap berhenti; B2: nomor yang
minta berhenti di satu baris tetap dikirimi bila muncul lagi di baris lain). Penguji merancang sendiri file kontak
55 baris (nomor fiktif 0812-0000-01xx) berisi variasi nomor 08/+62/0062/62/8xx hilang nol/apostrof Excel/format ilmiah,
duplikat dengan format berbeda (sebelum **dan** sesudah baris berhenti), 15 variasi nilai Persetujuan dan 17 variasi nilai
Berhenti, nama yang hanya sapaan/kosong/bergelar, dan kolom `{kota}` kosong. Setiap baris diberi label harapan
(KIRIM / TIDAK / ABU = ambigu) **sebelum** script dijalankan; hasil script lalu dibandingkan dengan label itu memakai
python terpisah yang punya fungsi normalisasi nomor sendiri.

## Input pengguna
```
Ini file pelanggan dari aplikasi kasir, agak berantakan ya, ada yang dobel juga. Yang udah minta stop aku tandain di
kolom Berhenti (ada yang aku tulis STOP, ada yang x, ada yang tanggalnya), sama ada juga stop.txt dari HP admin.
Pesannya pakai yang promo gajian roti kemarin, sebut kotanya juga. Mulai Jumat 25 Sept jam 10.
```

## Output

## Broadcast WA — Promo Gajian Roti Hangat Mbak Sri (daftar kirim dari file kasir)

Variasi pesan sama dengan contoh 01, ditambah `{kota}` ("Buat pelanggan kami di {kota}, ..."). Setiap variasi punya
teks berhenti ("Balas STOP" / "Balas BERHENTI").

### Hasil pengolahan kontak
Status: **SIAP** (daftar berhenti: 2 nomor terbaca, 0 baris gagal dibaca)
Siap kirim: **26** dari 55 baris
Dilewati:
- **8** minta berhenti (kolom Berhenti berisi STOP, stop, x, tanggal, ya, Unsub, Berhenti, ✓)
- **3** nomornya minta berhenti/tidak setuju di **baris lain** (baris dobel)
- **5** belum/tidak setuju (kosong, tidak, Tidak, belum, tdk)
- **2** ada di stop.txt
- **5** nomor kosong/tidak valid (telepon rumah, format ilmiah Excel `8.12E+11`, nomor terlalu pendek, kosong, dua nomor dalam satu sel)
- **2** nomor dobel
- **1** kolom `{kota}` kosong (baris 25 — nomor yang sama di baris 26 sudah lengkap, jadi tetap dikirimi sekali)
- **3 sel tidak baku — mohon dirapikan:** baris 23 Persetujuan "ya (lisan)" (dianggap belum setuju; kalau memang setuju,
  ubah jadi "ya" + tanggal), baris 45 Berhenti "masih aktif" dan baris 53 "N/A" (dianggap berhenti; kosongkan bila masih aktif).

Sebaran variasi: V1 = 9, V2 = 9, V3 = 8 | Jadwal: Jumat 25 Sep 2026 10.00 → 10.55 WIB (dua batch: 10.00–10.19 dan 10.50–10.55), selesai sebelum jam salat Jumat.
Nama bergelar sudah dirapikan otomatis ("IBU HJ. AMINAH" → "Bu Aminah", "dr. Andi" → "Kak Andi").
File: `broadcast_siap.csv` (jadwal, pesan terisi, link wa.me per kontak — simpan di komputer sendiri, jangan dibagikan).

**Konfirmasi dulu:** siap kirim ke **26 kontak** mulai Jumat 25 September 10.00 WIB? Kalau 3 sel di atas mau dirapikan dulu,
perbaiki file lalu saya jalankan ulang.

### Sebelum kirim (UU PDP)
- [ ] Semua penerima sudah setuju (kolom Persetujuan = ya)
- [ ] Yang membalas STOP/BERHENTI dicatat di kolom Berhenti atau stop.txt (satu nomor per baris; catatan taruh di **depan** nomor atau pisahkan dengan koma)
- [ ] File kontak & `broadcast_siap.csv` disimpan aman, tidak dibagikan

📝 Asumsi: WIB; sapaan default "Kak"; nama depan saja.

## Tabel verifikasi per baris (harapan penguji vs hasil script)

| Baris | Nama | No HP (mentah) | Persetujuan | Berhenti | Kota | Harapan penguji | Hasil script v1.0.2 |
|---|---|---|---|---|---|---|---|
| 2 | Bu Siti Aminah | `0812-0000-0101` | ya | (kosong) | Solo | KIRIM — 08 berstrip | **KIRIM** |
| 3 | Pak Joko | `+62 812 0000 0102` | Ya | tidak | Solo | KIRIM — +62 spasi, Ya+spasi | **KIRIM** |
| 4 | Mbak Rina | `0062812-0000-0103` | YA | - | Sukoharjo | KIRIM — 0062 | **KIRIM** |
| 5 | Dewi | `62812 0000 0104` | iya | 0 | Solo | KIRIM — 62 tanpa + | **KIRIM** |
| 6 | Andi | `812-0000-0105` | setuju | (kosong) | Klaten | KIRIM — nol hilang (Excel) | **KIRIM** |
| 7 | Bu | `0812-0000-0106` | ya | (kosong) | Solo | KIRIM — nama hanya sapaan | **KIRIM** |
| 8 | Pak | `0812-0000-0107` | 1 | Tidak | Solo | KIRIM — nama hanya sapaan | **KIRIM** |
| 9 | (kosong) | `0812-0000-0108` | yes | (kosong) | Solo | KIRIM — nama kosong | **KIRIM** |
| 10 | Mas. | `0812-0000-0109` | ✓ | (kosong) | Solo | KIRIM — sapaan bertitik | **KIRIM** |
| 11 | Sari | `0812-0000-0110` | ya | STOP | Solo | TIDAK — B1 STOP | lewat: minta berhenti (kolom berhenti) |
| 12 | Tono | `0812-0000-0111` | ya | 2026-09-01 | Solo | TIDAK — B1 tanggal | lewat: minta berhenti (kolom berhenti) |
| 13 | Ani | `0812-0000-0112` | ya | x | Solo | TIDAK — B1 x | lewat: minta berhenti (kolom berhenti) |
| 14 | Budi | `0812-0000-0113` | ya | stop | Solo | TIDAK — B1 stop kecil | lewat: minta berhenti (kolom berhenti) |
| 15 | Hadi | `0812-0000-0114` | ya | ya | Solo | TIDAK — berhenti | lewat: minta berhenti (kolom berhenti) |
| 16 | Hadi Dup | `+62-812-0000-0114` | ya | (kosong) | Solo | TIDAK — B2 dup setelah berhenti | lewat: nomor ini minta berhenti/tidak setuju di baris lain |
| 17 | Lina | `0812-0000-0115` | ya | (kosong) | Solo | TIDAK — B2 dup SEBELUM baris berhenti | lewat: nomor ini minta berhenti/tidak setuju di baris lain |
| 18 | Lina Dup | `62 812 0000 0115` | ya | Unsub | Solo | TIDAK — berhenti Unsub | lewat: minta berhenti (kolom berhenti) |
| 19 | Rudi | `0812-0000-0116` | tidak | (kosong) | Solo | TIDAK — tolak | lewat: belum/tidak setuju menerima broadcast |
| 20 | Rudi Dup | `812 0000 0116` | ya | (kosong) | Solo | TIDAK — B2 tolak di baris lain | lewat: nomor ini minta berhenti/tidak setuju di baris lain |
| 21 | Maya | `0812-0000-0117` | (kosong) | (kosong) | Solo | TIDAK — persetujuan kosong | lewat: belum/tidak setuju menerima broadcast |
| 22 | Nina | `0812-0000-0118` | belum | (kosong) | Solo | TIDAK — belum | lewat: belum/tidak setuju menerima broadcast |
| 23 | Oki | `0812-0000-0119` | ya (lisan) | (kosong) | Solo | ABU — persetujuan tak baku | lewat: nilai persetujuan tidak baku 'ya (lisan)' (dianggap belum setuju; rapikan jadi ya/tidak) |
| 24 | Putri | `0812-0000-0120` | ya | (kosong) | Solo | TIDAK — ada di stop.txt | lewat: ada di daftar berhenti |
| 25 | Qori | `0812-0000-0121` | ya | (kosong) | (kosong) | TIDAK — kota kosong -> baris ini dilewati | lewat: kolom {kota} kosong |
| 26 | Qori | `0812-0000-0121` | ya | (kosong) | Solo | KIRIM — dup dengan kota terisi | **KIRIM** |
| 27 | Rahmat | `021-555-0000` | ya | (kosong) | Solo | TIDAK — telepon rumah | lewat: nomor kosong/tidak valid |
| 28 | Sinta | `8.12E+11` | ya | (kosong) | Solo | TIDAK — format ilmiah Excel | lewat: nomor kosong/tidak valid |
| 29 | Tari | `0812000` | ya | (kosong) | Solo | TIDAK — terlalu pendek | lewat: nomor kosong/tidak valid |
| 30 | Umar | `(kosong)` | ya | (kosong) | Solo | TIDAK — nomor kosong | lewat: nomor kosong/tidak valid |
| 31 | Vina | `0812-0000-0122 / 0813-0000-0122` | ya | (kosong) | Solo | TIDAK — dua nomor satu sel | lewat: nomor kosong/tidak valid |
| 32 | Wati | `0812-0000-0101` | ya | (kosong) | Solo | TIDAK — duplikat Siti | lewat: nomor duplikat |
| 33 | Xena | `+62 (0)812-0000-0123` | ya | (kosong) | Solo | KIRIM — +62 (0) | **KIRIM** |
| 34 | Yudi | `0812-0000-0124` | OK | Belum | Solo | KIRIM — OK / Belum | **KIRIM** |
| 35 | Zaki | `0812-0000-0125` | TRUE | FALSE | Solo | KIRIM — TRUE/FALSE | **KIRIM** |
| 36 | IBU HJ. AMINAH | `0812-0000-0126` | ya | (kosong) | Solo | KIRIM — gelar Hj. | **KIRIM** |
| 37 | dr. Andi | `0812-0000-0127` | ya | (kosong) | Solo | KIRIM — gelar dr. | **KIRIM** |
| 38 | Kak Lala | `0812-0000-0128` | sudah | n | Solo | KIRIM | **KIRIM** |
| 39 | Teh Euis | `0812-0000-0129` | bersedia | no | Bandung | KIRIM | **KIRIM** |
| 40 | Koh Ahong | `0812-0000-0130` | boleh | aktif | Semarang | KIRIM | **KIRIM** |
| 41 | Mbok Darmi | `0812-0000-0131` | v | (kosong) | Denpasar | KIRIM | **KIRIM** |
| 42 | Gilang | `0812-0000-0132` | Tidak | (kosong) | Solo | TIDAK — Tidak kapital | lewat: belum/tidak setuju menerima broadcast |
| 43 | Fajar | `0812-0000-0133` | ya | Berhenti | Solo | TIDAK — berhenti | lewat: minta berhenti (kolom berhenti) |
| 44 | Eko | `0812-0000-0134` | ya | ✓ | Solo | TIDAK — centang di kolom berhenti | lewat: minta berhenti (kolom berhenti) |
| 45 | Citra | `0812-0000-0135` | ya | masih aktif | Solo | ABU — frasa bebas | lewat: nilai kolom berhenti tidak baku 'masih aktif' (dianggap berhenti; kosongkan bila masih aktif) |
| 46 | Dian | `0812 0000 0136` | ya | (kosong) | Solo | KIRIM | **KIRIM** |
| 47 | Dian | `0062 812 0000 0136` | Ya | (kosong) | Solo | TIDAK — duplikat 0062 | lewat: nomor duplikat |
| 48 | Endah | `+62 0812 0000 0137` | ya | (kosong) | Solo | KIRIM — +62 0812 | **KIRIM** |
| 49 | Farah | `6281200000138` | ya | (kosong) | Solo | KIRIM — 62 rapat | **KIRIM** |
| 50 | Galih | `0812-0000-0139` | ya | (kosong) | Solo | TIDAK — stop.txt tanpa nol | lewat: ada di daftar berhenti |
| 51 | Hana | `0812-0000-0140` | Y | (kosong) | Solo | KIRIM | **KIRIM** |
| 52 | Ika | `0812-0000-0141` | ya | (spasi) | Solo | KIRIM — berhenti spasi saja | **KIRIM** |
| 53 | Jaka | `0812-0000-0142` | ya | N/A | Solo | ABU — N/A | lewat: nilai kolom berhenti tidak baku 'N/A' (dianggap berhenti; kosongkan bila masih aktif) |
| 54 | Kiki | `'0812-0000-0143` | ya | (kosong) | Solo | KIRIM — apostrof Excel | **KIRIM** |
| 55 | Luki | `0812-0000-0144` | Setuju | TIDAK | Solo | KIRIM | **KIRIM** |
| 56 | Siapa yang tidak mau | `0812-0000-0145` | tdk | (kosong) | Solo | TIDAK — tdk | lewat: belum/tidak setuju menerima broadcast |

**Hasil verifikasi independen:** harapan KIRIM = 26 nomor; script = 26 nomor, unik, **identik**. Salah kirim (kontak
TIDAK yang lolos) = **0**. Terlewat (kontak KIRIM yang dibuang) = **0**. Tiga baris ABU dibuang (arah aman) dan di v1.0.2 dilaporkan per sel sebagai "nilai … tidak baku". Hasil v1.0.1 dan v1.0.2 identik (26 nomor yang sama).
Semua link `wa.me/<nomor>?text=` terdekode sama persis dengan kolom `pesan`; tidak ada `{placeholder}` tersisa;
semua pesan memuat "Balas STOP/BERHENTI".

## Uji tambahan (dijalankan di `/tmp/uji-broadcast-wa-v101/`)

**Jadwal Jumat 11.30–13.00 (120 kontak fiktif):**

| Kasus | Hasil | Status |
|---|---|---|
| Mulai Jumat 10.00, jeda 3 menit | batch 1 10.00–10.57, batch 2 seharusnya 11.30 → digeser ke 13.00; 0 pesan di 11.30–13.00 | ✔ |
| Mulai Jumat 11.45 | pesan pertama 13.00 | ✔ |
| Jendela 09.00–12.00, mulai Jumat 11.40 | digeser ke Sabtu 09.00 | ✔ |
| Mulai Kamis 19.55, maks 10/hari, jendela 11.00–20.00, jeda 5 menit | Jumat 11.00–11.25 lalu 13.00, 13.05 | ✔ |
| Default (batch 20, jeda 60 dtk), mulai Jumat 10.00 | 11.00–11.09 lalu 13.00; 100/hari lalu Sabtu | ✔ |
| `--kirim-saat-jumatan` | 20 pesan di 11.30–12.27 (sesuai opsi) | ✔ |

**Cek teks berhenti (script harus menolak variasi tanpa cara berhenti):**

| Teks variasi | Hasil v1.0.1 | Hasil v1.0.2 |
|---|---|---|
| "promo non-stop sepanjang hari!" | DITOLAK ✔ | DITOLAK ✔ |
| "STOP! Jangan lewatkan promo ini." | DITOLAK ✔ | DITOLAK ✔ |
| 2 variasi, variasi 1 tanpa teks berhenti | DITOLAK ✔ | DITOLAK ✔ |
| "Ketik STOP untuk berhenti." / "Balas \"BERHENTI\" jika tidak mau lagi." / "cukup balas STOP ya" | LOLOS ✔ | LOLOS ✔ |
| "**Siapa yang tidak mau dapat diskon 50%?** Buruan order!" (tanpa cara berhenti) | **LOLOS** ✘ | DITOLAK ✔ |
| "Kalau **tidak ingin menerima** kabar diskon, sayang banget lho." | **LOLOS** ✘ | DITOLAK ✔ |
| "Beli sekarang **untuk berhenti** pusing mikir lauk!" | **LOLOS** ✘ | DITOLAK ✔ |

**Daftar berhenti dengan catatan & nama bergelar:** v1.0.1 membuang diam-diam baris seperti `0812-0000-0120 tgl 12/09`
dan menghasilkan "Bu HJ." / "Kak Dr.". Di v1.0.2 kedua hal itu sudah benar; uji lanjutan (24 variasi catatan, 29 variasi
gelar, 19 teks berhenti) ada di `07-uji-daftar-berhenti-gelar-v102.md`.

**File rusak:** file kosong / hanya judul → "File kontak tidak berisi data"; bukan UTF-8 → petunjuk simpan ulang "CSV UTF-8";
pemisah `;` terbaca; judul kolom tak dikenal ("Setuju Promo (ya/tidak)") → ditolak dengan petunjuk `--kolom-persetujuan`. ✔

**Uji regresi:** v1.0.1 → 6/6 OK; v1.0.2 → 11/11 OK.

## Catatan penguji
- **B1 dan B2 v1.0.0 sudah diperbaiki**, terbukti pada data yang dirancang penguji (bukan hanya pada uji regresi
  pembuat): STOP/stop/x/tanggal/Unsub/✓ dianggap berhenti, dan baris dobel (baik sebelum maupun sesudah baris berhenti,
  termasuk beda format +62/812/0062) ikut dikecualikan. Daftar kirim akhir 26/26 identik dengan hitungan penguji.
- Jumat 11.30–13.00 selalu dilewati; 0062, nama hanya sapaan, dan cek "promo non-stop" sudah benar.
- **v1.0.2:** hasil sama (26/26, salah kirim 0); sel tidak baku kini dilaporkan per nilai, gelar dirapikan, status SIAP/PERIKSA DULU
  dan jumlah nomor daftar berhenti yang terbaca muncul di ringkasan. Sisa cacat ada di `07-…` dan `HASIL-UJI.md`.
