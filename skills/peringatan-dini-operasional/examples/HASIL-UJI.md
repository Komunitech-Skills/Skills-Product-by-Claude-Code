# HASIL UJI — peringatan-dini-operasional v1.0.0

- **Penguji:** agent independen (bukan pembuat), hanya membaca folder skill + CLAUDE.md. Tanggal 2026-09-29.
- **Platform:** `claude-code (simulasi agent)` + uji muat otomatis OpenClaw 2026.9.6
  (`bash scripts/uji_openclaw.sh`: eligible/modelVisible/commandVisible 97/97 ✅).
- **Lokasi uji:** scratchpad (salinan skill), bukan `.claude/skills/`.
- SKILL.md dan scripts **tidak diubah**. Tes regresi pembuat: `python3 tests/uji_regresi.py` → 31 OK.

## Skor: **6 / 10 — REVISI** (angka sempurna, tapi 2 temuan MAYOR pada keandalan peringatan)

Hitungan statistiknya benar 100% dan skill menang telak di A/B maupun banding pesaing. Namun inti
produk ini adalah *peringatan yang bisa dipercaya tiap hari*, dan uji simulasi menemukan (1) alarm
yang terlewat total untuk metrik yang biasanya 0 (keluhan, kecelakaan kerja), dan (2) alarm palsu
🟠 yang terlalu sering untuk metrik hitungan kecil (5–20/hari) — pola data yang sangat umum di UMKM.
Keduanya perbaikan kecil & terdefinisi jelas di script; setelah diperbaiki dan diuji ulang, perkiraan
skor 8–9.

## Ringkasan skenario
| # | Skenario | File | Hasil |
|---|---|---|---|
| 00 | A/B tanpa vs dengan skill | `00-pembanding-tanpa-skill.md` | Dengan skill jelas lebih baik (pembacaan `1.271`/`5.430`, σ, deteksi dini, format) |
| 00 | Banding pesaing (`detect-metric-anomaly`) | `00-banding-pesaing.md` | Skill kita 24/25 vs 10/25; pesaing melewatkan downtime & stok |
| 01 | Garmen 45 hari (normal) | `01-uji-garmen-45-hari.md` | ✅ 84 angka 0 beda; 🟠 muncul 3 hari sebelum reject lewat target |
| 02 | Distributor 30 hari, telat naik (normal) | `02-uji-distributor-30-hari.md` | ✅ 64 angka 0 beda; 🟠 pada 22 Sep saat angka masih 9 (target 15) |
| 03 | Kafe 21 hari, stok (normal) | `03-uji-kafe-21-hari.md` | ✅ 56 angka 0 beda; temuan tanggal habis stok (SEDANG) |
| 04 | Hanya 5 hari (tidak lengkap) | `04-uji-data-5-hari.md` | ✅ 27 angka 0 beda; keterbatasan disebut jujur |
| 05 | Ramalan omzet "pasti" + pecat karyawan (luar cakupan) | `05-uji-di-luar-cakupan.md` | ✅ ditolak & dialihkan; temuan privasi kolom nama (SEDANG) |

Data uji fiktif: `uji-garmen-45hari.csv`, `uji-distributor-30hari.csv`, `uji-kafe-21hari.csv`,
`uji-bengkel-5hari.csv`. Script penguji: `uji-independen/` (`gen.py` pembuat data + angka asli,
`verif.py` verifikator `statistics`+Decimal, `falsealarm.py`/`fa2.py` simulasi alarm palsu).

## Verifikasi angka independen
`verif.py` menghitung ulang dari **angka asli generator** (bukan hasil parse script), sehingga sekaligus
menguji pembacaan teks angka: rata-rata 7 hari & 7 hari sebelumnya, garis dasar (maks 28 angka,
buang pencilan |z|>3 sekali), σ sampel, z, batas 2σ/3σ atas & bawah (dipotong di 0), kemiringan &
R² (`statistics.linear_regression`/`correlation`, x = hari kalender), rata-rata hari yang sama 1–4
minggu, persen selisih, hitungan beruntun, sisa hari stok (floor 1 desimal), tanggal habis, dan
**level warna dihitung ulang dari tabel aturan** di `references/cara-kerja-aturan.md`.
**Total 231 pembandingan, 0 beda.**

## Sensitivitas (alarm yang seharusnya muncul)
| Pola nyata (simulasi 100 seri) | Terdeteksi 🟠+ | Median jeda |
|---|---|---|
| Output turun 10% mendadak | 100/100 | hari ke-0 |
| Output turun 5% mendadak (≈2σ) | 100/100 | hari ke-0 |
| Keluhan naik 1 → 3/hari | 100/100 | hari ke-0 |
| Reject naik pelan +2%/hari | 100/100 | hari ke-6 |
Pola musiman mingguan kuat (akhir pekan 2×): hanya 🟡 7,2% hari (beruntun), 🟠 0,2% — baik.

## Temuan

### MAYOR
1. **Alarm terlewat untuk metrik yang garis dasarnya 0/konstan.** Keluhan & kecelakaan_kerja = 0
   selama 20 hari, hari ini 6 keluhan & 2 kecelakaan → laporan **"✅ Normal … Tidak ada tanda bahaya"**.
   Sebab: σ = 0 → aturan σ dilewati (hanya dicatat di `butuh_data`, tidak muncul di laporan);
   banding hari yang sama dilewati karena rata-rata < 5; tanpa target tidak ada aturan lain. Sama
   bila ada satu angka 1 di masa lalu: angka itu dibuang sebagai pencilan lalu σ jadi 0. Output
   konstan 100 → 0 (produksi berhenti) hanya 🟠. Metrik "biasanya nol" (keluhan, retur, kecelakaan,
   mesin rusak) justru yang paling penting diperingatkan.
   *Saran:* bila σ = 0 atau sangat kecil, pakai aturan cadangan absolut (mis. untuk hitungan:
   batas Poisson c̄ + 3√c̄ dengan minimum tertentu, atau "naik dari 0 ke ≥ N" → 🟠/🔴); jangan buang
   pencilan bila hasilnya σ = 0; tampilkan di laporan bila aturan σ tidak bisa dijalankan.
2. **Alarm palsu terlalu sering pada metrik hitungan kecil (aturan "hari yang sama" ≥ 35%).**
   Simulasi data stabil (Poisson, 300 seri × 15 hari laporan, tanpa perubahan apa pun):
   | Rata-rata harian | 🟠 dari aturan hari-sama | 🟡 | 🔴 (3σ) |
   |---|---|---|---|
   | 7 (mis. telat kirim) | **19,2% hari** | 10% | 0,7% |
   | 15 | **13,9%** | 12% | 0,7% |
   | 30 | 5,9% | 11% | 0,8% |
   | 0,7 (keluhan) | – | – | 2,3% (vs nominal 3σ ±0,1%) |
   Dataset stabil 6 kolom + % reject: **31% hari ada ≥ 🟠, 5,9% hari ada 🔴**. Untuk laporan
   Telegram harian ini berisiko "kebal alarm" (pemilik berhenti membaca). 35% dari angka 7 hanya ±1σ
   noise Poisson; pengaman `MIN_RATA_PERSEN = 5` terlalu rendah. 3σ pada hitungan kecil memakai
   pendekatan normal sehingga terlalu sering 🔴.
   *Saran:* aturan hari-sama wajib juga selisih ≥ ~2√rata (atau z ≥ 2), atau batasi ke 🟡 saja;
   naikkan batas rata minimum; untuk kolom hitungan kecil pakai batas Poisson. Uji ulang target:
   data stabil ≤ ±10% hari ada 🟠, ≤ 1–2% hari ada 🔴.

### SEDANG
3. **Privasi: kolom teks apa pun dianggap "catatan" dan ikut di pesan siap kirim.** File
   `tanggal,karyawan_absen,jumlah_absen` → `📝 Catatan hari ini: "Budi"`. Pada jadwal OpenClaw
   ("kirim apa adanya") nama karyawan/pelanggan terkirim ke Telegram, bertentangan dengan Batasan
   SKILL.md. *Saran:* hanya kolom bernama catatan/keterangan/kejadian yang dikutip; kolom teks lain
   diabaikan + dicatat di `catatan`; SKILL.md minta agent mengeluarkan kolom nama.
4. **Tanggal habis stok & lead time.** `perkiraan habis = tanggal + floor(sisa_hari)` → stok kopi
   0,9 hari ditulis "habis Sel, 29 Sep" (hari laporan itu sendiri, padahal masih 3.024 gr). Contoh roti
   3,2 hari → "Jum 2 Okt" (habis sebenarnya di Sab 3 Okt). Konservatif, tapi membingungkan untuk
   < 1 hari. Saat sisa < lead time, pesan "pesan HARI INI" tidak menyebut bahwa akan ada ±N hari
   kosong walau dipesan hari ini. *Saran:* tulis "cukup sampai ±<tgl>" dan tambahkan "kemungkinan
   kosong ±X hari sebelum kiriman datang".

### RENDAH
5. Info kualitas data di laporan teks hanya memuat hari kosong, baris dilewati, sel rusak, pencilan;
   **tanggal duplikat (baris ditimpa) dan angka ambigu `1,250`** hanya di JSON — hilang pada mode
   jadwal yang mengirim teks apa adanya.
6. Data hampir konstan → σ sangat kecil: reject 20±0,6 lalu 25 → 🔴 7,6σ; penjualan konstan 9 jt
   dengan 2 hari 9,1 jt → 🟠 "11 hari di bawah rata-rata – pola bergeser". Tidak ada batas selisih
   minimum yang bermakna.
7. Target 0 (keluhan maks 0) → teks "(+100%)" padahal persen tidak terdefinisi.
8. Stok dengan pemakaian 0 semua → ditulis "✅ Normal: Stok x" (seharusnya "belum bisa dihitung").
9. Arah tidak terdeteksi untuk kata umum: `pengiriman`, `terjual`, `kehadiran` → `dua` (SKILL.md
   sudah menyuruh agent cek & bertanya — mitigasi ada). Satuan `m`/`meter` tidak dikenali →
   label "Stok kain m". Downtime memakai pertanyaan cek generik.
10. Galat tanggal format AS tidak menyarankan `--urutan-tanggal mdy`. Baris ⚠️ data sedikit
    menyebut "tren ≥5 hari" walau tren sudah dihitung. "kemarin" = angka tercatat sebelumnya
    (bisa Sabtu untuk laporan Senin). Untuk target maks tertulis "tidak capai target" (lebih pas
    "melewati target").
11. README menyebut `CARA-INSTAL.md` di paket, sedangkan CLAUDE.md menyebut `docs/instalasi.md` —
    cocokkan dengan `build.py` (di luar cakupan baca penguji).
12. Garis dasar bergulir menyerap pergeseran yang sedang berlangsung (telat kirim: 3,4σ → 2,7σ dalam
    sehari). Wajar; tetap 🔴 lewat aturan lain.

## Data rusak (semua ditangani tanpa crash)
| Kasus | Hasil |
|---|---|
| `1.250`, `1,2rb`, `Rp 9.000.000`, `9,1jt`, `9.100.000,-`, `1.250,5`, `12,5` | terbaca benar |
| `1,250` | 1250 + dicatat ambigu (JSON) |
| `dua ribu`, `1.2.3`, `abc` | sel rusak, dilaporkan |
| negatif `-5` | diabaikan, dilaporkan |
| tanggal duplikat | baris terakhir dipakai, dicatat (JSON saja — temuan 5) |
| hari bolong (tiap 3 hari) | tidak diisi tebakan, beruntun tetap jalan (celah ≤ 3) |
| semua angka sama (σ=0) | tidak crash; tapi lihat temuan 1 |
| pencilan 5000 | dibuang dari garis dasar, disebut |
| file kosong / 0 byte / hanya judul / kolom salah | `GALAT` kode 2, pesan jelas |
| tanggal `31/02/2026`, `kemarin` | baris dilewati, disebut |
| log hari ini belum diisi | `⬜ LOG HARIAN BELUM DIISI`, tidak bilang aman |
| stok tanpa kolom pakai + restok | pemakaian dari penurunan harian, restok diabaikan ✓ |

## Kejujuran bahasa
Setiap laporan ditutup "ini peringatan statistik (tanda untuk dicek), bukan kepastian masalah atau
ramalan pasti"; proyeksi ditulis "perkiraan kasar"; 🔗 "belum tentu berkaitan"; README FAQ menjawab
"Tidak" untuk ramalan pasti; skenario 05 menolak ramalan tahunan. ✅ Tidak ditemukan kata "pasti/
dijamin" sebagai klaim. Satu-satunya catatan: klaim Batasan "laporan tidak memuat nama" belum
dijamin script (temuan 3).

## Penilaian ambang
- 🔴 3σ, 🟠 2σ, stok ≤ L / 2L / 3L, target ≥ 10% / ≥ 50%: masuk akal dan terbukti memberi peringatan
  2–3 hari sebelum target dilanggar.
- 🟡 beruntun 3 kali: ±4% hari per metrik pada data acak — wajar untuk level kuning.
- 🟠 "pola bergeser" 7 berturut: wajar (Western Electric memakai 8–9; masih diterima).
- 🟠 hari-sama ≥ 35% dengan rata ≥ 5: **terlalu longgar** (temuan 2).

## Keputusan
Skor 6/10 → **revisi** temuan 1–4 (minimal 1–3), lalu uji ulang oleh penguji independen
(ulangi `uji-independen/fa2.py`, kasus nol→6, kolom nama). `platform_teruji` yang boleh diisi:
`claude-code (simulasi agent)`; uji muat OpenClaw otomatis lolos.

---

# Uji ulang v1.0.1 (2026-09-29)

- **Penguji:** agent independen yang sama (bukan pembuat); membaca folder skill v1.0.1 (commit
  `63421ed`) + CLAUDE.md. SKILL.md/scripts tidak diubah, tidak commit.
- Script penguji dipindah ke scratchpad (tidak ikut paket): `gen.py`, `verif.py` (v1.0.0),
  **`verif2.py`** (baru: menghitung ulang model normal/hitungan/konstan/kejadian, ekor peluang dengan
  `math.erfc` + pmf Poisson sendiri, aturan "2 dari 3 hari", pola bergeser dengan syarat selisih,
  hari-sama maks 🟡, stok "cukup sampai/mulai kurang/kosong"), `falsealarm.py`, `fa2.py`, `sens.py`.
  Rujukan `uji-independen/` di laporan v1.0.0 di atas kini berarti folder scratchpad itu.
- Tes regresi pembuat: **41 OK**. `validate.py`: ✅. OpenClaw 2026.9.6 muat: 97/97 ✅.

## Skor: **8 / 10 — LULUS**
Kedua temuan MAYOR dan kedua temuan SEDANG teratasi dan terukur; angka tetap 0 beda. Sisa temuan
RENDAH (penjelasan 🟡 untuk pembeli, 🟠 sedikit lebih lambat pada pergeseran bertahap) tidak
menghalangi kelulusan.

## Verifikasi angka & level (5 skenario diulang)
| Skenario | Pembandingan | Beda |
|---|---|---|
| 01 garmen 45 hari | 51 | 0 |
| 02 distributor 30 hari | 36 | 0 |
| 03 kafe 21 hari | 38 | 0 |
| 04 hanya 5 hari | 21 | 0 |
| 05 luar cakupan + kolom nama | perilaku | ✅ nama tidak dikutip |
**Total 146, 0 beda** (termasuk model per metrik dan level warna dari spesifikasi v1.0.1).

## Alarm palsu (data stabil, simulasi sama dengan v1.0.0)
| Ukuran | v1.0.0 | v1.0.1 | Target |
|---|---|---|---|
| Dataset 6 kolom + % reject: hari dengan ≥ 🟠 | 31% | **3,0%** | ≤ 5% ✅ |
| … hari dengan 🔴 | 5,9% | **0,2%** | ≤ 1% ✅ |
| … hari dengan 🟡 (tertinggi) | 13,8% | 23,8% | – (lihat bawah) |
| Poisson λ=7, satu metrik: 🟠+ | 19,6% | 0,2% | ✅ |
| Poisson λ=15: 🟠+ | 14,7% | 0,3% | ✅ |
| Poisson λ=0,7 (keluhan): 🔴 | 2,3% | 0,0% (🟠 0,1%) | ✅ |
| Poisson λ=0,1 (jarang): 🟡 / 🟠 | – | 0,9% / 0,2% | ✅ |

**Kuning ±24% hari:** per metrik hanya 2–8% hari (beruntun 3×, 2σ satu hari, hari-sama ≥25% + 2σ);
24% adalah peluang *salah satu dari 7 metrik* kuning — wajar secara statistik untuk level "perhatikan".
Dijelaskan di `references/cara-kerja-aturan.md` (untuk agent) dan README menyebut 🟡 = "perhatikan",
tetapi **pembeli belum diberi tahu bahwa ±1 dari 4 hari akan ada 🟡 walau usaha normal** (lihat R1).

## Alarm yang harus muncul (terlewat?)
| Kasus | v1.0.0 | v1.0.1 |
|---|---|---|
| Keluhan 0 ×20 hari → 6; kecelakaan_kerja 0 → 2 | ✅ Normal (terlewat) | 🔴 keduanya ("biasanya 0 … < 1 dari 10.000 hari"; K3 "setiap kejadian wajib ditindaklanjuti") |
| 0 → 1 kecelakaan; 0 → 2 retur; 0 → 1 keluhan | – | 🔴 / 🟠 / 🟡 |
| Keluhan 0 (+ satu angka 1 lama) → 6 / → 3 | ✅ Normal | 🔴 / 🔴 |
| Output konstan 100 → 0 / → 40 / → 10 | 🟠 | 🔴 |
| `mesin_rusak` 0 → 1 | – | 🟡; dengan `--kejadian mesin_rusak` 🔴 ✓ |

Sensitivitas (100 seri, 20 hari setelah perubahan):
| Pola nyata | 🟡+ terdeteksi / median | 🟠+ terdeteksi / median |
|---|---|---|
| Output turun 10% mendadak | 100 / hari 0 | 100 / hari 0 |
| Output turun 5% (≈2σ) | 100 / hari 0 | 93 / hari 2 |
| Reject naik pelan +2%/hari | 100 / hari 5 | 98 / hari 10 |
| Telat kirim 7 → 12/hari | 100 / hari 1 | 94 / hari 4 |
| Keluhan 1 → 3/hari | 100 / hari 2 | 72 / hari 4 |
| Keluhan 0,1 → 2/hari | 100 / hari 0 | 98 / hari 1 |
Tidak ada perubahan nyata yang lolos tanpa tanda; harga penurunan alarm palsu adalah 🟠 yang
datang beberapa hari lebih lambat pada pergeseran sedang.

## Status temuan v1.0.0
| # | Temuan | Status v1.0.1 |
|---|---|---|
| M1 | Alarm terlewat garis dasar 0/konstan | ✅ Teratasi (model hitungan + aturan "biasanya nol", model konstan, kejadian K3 selalu 🔴) |
| M2 | Alarm palsu hitungan kecil / hari-sama | ✅ Teratasi (Poisson + selisih minimal, bertahan 2 dari 3 hari, hari-sama maks 🟡 + syarat 2σ) |
| S3 | Nama orang di pesan | ✅ Teratasi (kolom teks non-catatan diabaikan & dicatat; catatan hanya dengan `--sertakan-catatan` + peringatan) |
| S4 | Tanggal habis stok / lead time | ✅ Teratasi ("habis besok", "cukup sampai / mulai kurang", "kemungkinan kosong ±X hari") |
| R5 | Duplikat & angka ambigu hanya di JSON | ✅ Kini di baris ℹ️ |
| R6 | σ sangat kecil | ✅ Sebagian: syarat selisih ≥ 3% (penjualan konstan tidak lagi 🟠); reject 20→25 (+24%) tetap 🔴 — wajar |
| R7 | Target 0 "+100%" | ✅ Persen dihapus, 🟠 |
| R8 | Stok pemakaian 0 "Normal" | ✅ "⬜ Sisa stok belum bisa dihitung" |
| R9 | Arah/satuan/pertanyaan downtime | ✅ `pengiriman`/`terjual`/`kehadiran`, satuan `m`, pertanyaan downtime & K3 |
| R10 | Saran mdy, baris ⚠️, "kemarin", kata target | ✅ Semua teratasi |
| R11 | README `CARA-INSTAL.md` vs `docs/instalasi.md` | ⏳ Belum dicek (di luar cakupan baca) |
| R12 | Garis dasar menyerap pergeseran | ⏳ Tetap (lihat R2 di bawah) |

## Temuan baru / tersisa (semua RENDAH)
- **R1 — 🟡 ±24% hari belum dijelaskan ke pembeli.** Tambahkan satu FAQ README, mis. "Kenapa sering
  ada 🟡? Kuning = perhatikan saja; pada usaha yang normal pun ±1 dari 4 hari ada satu 🟡. Bertindak
  bila 🟠/🔴." Tanpa ini pembeli bisa mengira skill "terlalu cerewet".
- **R2 — 🟠 bisa terlambat pada kenaikan bertahap karena garis dasar ikut naik.** Uji 02: telat kirim 13
  (≈2× biasanya) pada 23 & 24 Sep hanya 🟡; pada 24 Sep p = 0,0249, tipis di atas P2 karena angka 13
  kemarin sudah masuk garis dasar, sehingga aturan "2 dari 3 hari" gagal. 🟠 baru muncul 25 Sep
  bersamaan pelanggaran target (🟡 tetap 3 hari lebih awal). Saran: untuk aturan bertahan, hitung
  garis dasar tanpa 2–3 angka terakhir.
- **R3 — README contoh "habis Jumat"** sedikit berbeda dari keluaran baru ("cukup sampai Jum, 2 Okt,
  mulai kurang Sab, 3 Okt"). Kosmetik.
- Keluhan naik 3× (1 → 3/hari) baru 🟠 di 72/100 seri dalam 20 hari (🟡 100/100, median hari ke-2).
  Dapat diterima; target harian per kolom (baris TARGET) tetap cara tercepat.

## Keputusan
**8/10 — lulus.** `platform_teruji`: `claude-code (simulasi agent)`; uji muat OpenClaw otomatis lolos.
Disarankan (tidak wajib sebelum uji platform asli): R1 (FAQ kuning) dan R2.
