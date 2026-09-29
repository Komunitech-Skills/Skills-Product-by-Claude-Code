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
