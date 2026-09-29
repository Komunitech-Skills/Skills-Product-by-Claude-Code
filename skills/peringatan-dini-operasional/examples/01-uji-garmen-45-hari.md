# Uji 01 (normal) — Pabrik garmen fiktif, log 45 hari

> Uji independen (penguji terpisah, simulasi agent `claude-code (simulasi agent)`), 2026-09-29.
> Data **fiktif** buatan penguji: `examples/uji-garmen-45hari.csv` (16 Agu – 29 Sep 2026, Minggu
> libur, angka campur `1.271`, `1,2rb`, stok `5.430`, 4 Sep listrik padam 4 jam: output 610,
> downtime 240). Pola yang ditanam: reject naik bertahap 28 → 31 → 33 → 44 → 52 sejak 24 Sep;
> downtime melonjak 95 menit hari ini; stok kain ±2,8 hari. Baris `TARGET`: output min `1.200`,
> reject maks 40, absen maks 3.

## Input pengguna
"Ini log produksi konveksi saya 45 hari terakhir, ada yang perlu diwaspadai? Pemasok kain butuh
3 hari. Nama usaha Konveksi Maju Jaya."

## Perintah yang dijalankan agent
```bash
python3 scripts/peringatan_dini.py examples/uji-garmen-45hari.csv --lead-time 3 --format json
python3 scripts/peringatan_dini.py examples/uji-garmen-45hari.csv --lead-time 3 --nama-usaha "Konveksi Maju Jaya (fiktif)"
```
Cek JSON: arah output=`turun`, reject/downtime/absen=`naik`, `% reject` ditambahkan, stok
`stok_kain_m`+`pakai_kain_m` terpasang otomatis; `sel_rusak` kosong; `angka_ambigu` kosong. Tidak
perlu `--arah`.

## Output siap kirim (apa adanya dari script)
```
🚨 PERINGATAN DINI OPERASIONAL
Konveksi Maju Jaya (fiktif) — Sel, 29 Sep 2026
Data 17 Agu–29 Sep (38 hari tercatat)
Ringkas: 4 🔴 · 0 🟠 · 2 🟡 · 0 normal

🔴 Downtime (menit): 95 hari ini (kemarin 23)
   7,0σ di atas rata-rata 27 hari sebelumnya (25,89) -- lewat batas bahaya 3σ; 255% di atas rata-rata hari Selasa 4 minggu terakhir (26,75).
🔴 Reject (pcs): 52 hari ini (kemarin 44)
   6,4σ di atas rata-rata 27 hari sebelumnya (23,26) -- lewat batas bahaya 3σ; 163% di atas rata-rata hari Selasa 4 minggu terakhir (19,75); melewati target maks 40 (+30%); 2 dari 7 hari terakhir tidak capai target.
🔴 % reject: 4,24 hari ini (kemarin 3,52)
   4,6σ di atas rata-rata 27 hari sebelumnya (1,98) -- lewat batas bahaya 3σ; naik 4 hari berturut-turut.
🔴 Stok kain m: sisa 5.430 = ±2,8 hari pemakaian (rata-rata 1.920/hari) -> perkiraan habis Kam, 1 Okt; pemasok butuh 3 hari -- pesan HARI INI
🟡 Absen: 3 hari ini (kemarin 2)
   naik 3 hari berturut-turut.
🟡 Output (pcs): 1.225 hari ini (kemarin 1.250)
   3 dari 7 hari terakhir tidak capai target min 1.200.
🔗 Downtime (menit) dan Reject (pcs) memburuk bersamaan — cek apakah penyebabnya sama (belum tentu berkaitan).
📝 Catatan hari ini: "mesin jahit obras line 3 sering putus benang"

❓ Cek hari ini (cari akar masalah, bukan cari kambing hitam):
Downtime (menit):
 • Apa yang berubah dibanding minggu lalu (orang, bahan, mesin, cara kerja, pelanggan)?
 • Mulai sejak tanggal berapa, dan terjadi di bagian/shift mana?
 • Angka ini dicatat dengan cara yang sama seperti biasanya?
Reject (pcs):
 • Material: ada bahan baku batch/pemasok baru, atau bahan disimpan terlalu lama?
 • Mesin: suhu/setting mesin (oven, mixer, sealer) berubah, baru diservis, atau sempat rusak?
 • Manusia & metode: operator baru/ganti shift? resep, SOP, atau ukuran batch berubah?
5 kenapa: Kenapa Downtime (menit) naik? → karena … → kenapa itu terjadi? → … (ulang sampai ketemu hal yang bisa diperbaiki).
Kalau sudah ada kerugian/komplain pelanggan: susun laporan insiden (skill laporan-insiden-usaha).

ℹ️ Data: 6 hari kosong (Min, 23 Agu, Min, 30 Agu, Min, 6 Sep…) tidak diisi tebakan; 4 angka ekstrem lama tidak dipakai di rata-rata.
Catatan: ini peringatan statistik (tanda untuk dicek), bukan kepastian masalah atau ramalan pasti.
```

## Tambahan analisis agent (di luar pesan)
Reject sudah mulai naik sejak Kam 24 Sep (28 → 52), jadi lonjakan hari ini bukan kejadian sehari;
catatan hari ini ("mesin jahit obras line 3 sering putus benang") layak dicek lebih dulu bersama
downtime 95 menit, tapi belum tentu satu-satunya penyebab. Kain sebaiknya dipesan hari ini: sisa
±2,8 hari, pemasok butuh 3 hari — kemungkinan ada ±1 hari tanpa kain bila tidak dipercepat.
Mau saya bantu isi 5 kenapa untuk reject, atau jadwalkan laporan ini tiap malam ke Telegram?

## Verifikasi independen (`verif.py` penguji, modul `statistics` + Decimal, dari angka asli generator)
| Angka | Verifikator | Script |
|---|---|---|
| Garis dasar reject (27 angka, 4 Sep dibuang sbg pencilan) | rata 23,26; sd 4,503 | 23,26; 4,5030 |
| z reject | (52 − 23,26)/4,503 = 6,38 | 6,4σ |
| Selasa 4 minggu reject | 19,75 → +163,3% | 19,75; 163% |
| Downtime z / Selasa | 7,01 / 26,75 (+255,1%) | 7,0σ / 255% |
| % reject z | 4,60 (rata 1,98) | 4,6σ |
| Tren reject 7 hari | slope 3,957/hari, R² 0,900 | 3,9571; 0,9000 |
| Stok kain | 5.430 / 1.920 = 2,828 → 2,8 hari ≤ lead 3 → 🔴 | 2,8; 🔴 |
| Output target 7 hari | 3 dari 7 hari < 1.200 → 🟡 | 🟡 |
**84 angka dibandingkan, 0 beda.**

## Kapan peringatan pertama muncul (uji `--tanggal` mundur)
| Tanggal | Reject | Level script | Alasan utama |
|---|---|---|---|
| 24 Sep | 28 | 🟡 | 27% di atas rata-rata Kamis |
| 25 Sep | 31 | 🟠 | 2,0σ |
| 26 Sep | 33 | 🟠 | 2,3σ + proyeksi ±5 hari lewat target |
| 28 Sep | 44 | 🔴 | 4,6σ, lewat target 40 |
Peringatan 🟠 muncul **3 hari sebelum** reject melewati target — memang "dini".

## Penilaian
Benar & berguna. Catatan kecil: label `Stok kain m` (satuan `m` tidak dikenali), pertanyaan cek
untuk downtime masih generik, dan tiga 🔴 (reject, % reject, downtime) bisa terasa berlebihan untuk
satu masalah yang sama.

---

## Uji ulang v1.0.1 (2026-09-29, penguji independen)
Perintah sama. Output siap kirim v1.0.1:
```
🚨 PERINGATAN DINI OPERASIONAL
Konveksi Maju Jaya (fiktif) — Sel, 29 Sep 2026
Data 17 Agu–29 Sep (38 hari tercatat)
Ringkas: 4 🔴 · 0 🟠 · 2 🟡 · 0 normal

🔴 Downtime (menit): 95 hari ini (kemarin 23)
   7,0σ di atas rata-rata 27 hari sebelumnya (25,89) -- lewat batas bahaya 3σ; 255% di atas rata-rata hari Selasa 4 minggu terakhir (26,75).
🔴 Reject (pcs): 52 hari ini (kemarin 44)
   6,4σ di atas rata-rata 27 hari sebelumnya (23,26) -- lewat batas bahaya 3σ (2 dari 3 hari terakhir); melewati target maks 40 (+30%); 2 dari 7 hari terakhir melewati target; naik 4 hari berturut-turut.
🔴 % reject: 4,24 hari ini (kemarin 3,52)
   4,6σ di atas rata-rata 27 hari sebelumnya (1,98) -- lewat batas bahaya 3σ (2 dari 3 hari terakhir); naik 4 hari berturut-turut.
🔴 Stok kain (m): sisa 5.430 = ±2,8 hari pemakaian (rata-rata 1.920/hari) -> cukup sampai Kam, 1 Okt, mulai kurang Jum, 2 Okt; pemasok butuh 3 hari -- pesan HARI INI; walau dipesan hari ini (datang ±Jum, 2 Okt), kemungkinan kosong ±0,2 hari
🟡 Absen: 3 hari ini (kemarin 2)
   naik 3 hari berturut-turut.
🟡 Output (pcs): 1.225 hari ini (kemarin 1.250)
   3 dari 7 hari terakhir di bawah target min 1.200.
🔗 Downtime (menit) dan Reject (pcs) memburuk bersamaan — cek apakah penyebabnya sama (belum tentu berkaitan).

❓ Cek hari ini (cari akar masalah, bukan cari kambing hitam):
Downtime (menit):
 • Mesin mana yang berhenti, berapa lama, dan apa gejalanya sebelum berhenti?
 • Jadwal perawatan/servis terakhir kapan? Ada suku cadang yang aus?
 • Berhentinya karena mesin, listrik/angin/air, atau menunggu bahan/operator?
Reject (pcs):
 • Material: ada bahan baku batch/pemasok baru, atau bahan disimpan terlalu lama?
 • Mesin: suhu/setting mesin (oven, mixer, sealer) berubah, baru diservis, atau sempat rusak?
 • Manusia & metode: operator baru/ganti shift? resep, SOP, atau ukuran batch berubah?
5 kenapa: Kenapa Downtime (menit) naik? → karena … → kenapa itu terjadi? → … (ulang sampai ketemu hal yang bisa diperbaiki).
Kalau sudah ada kerugian/komplain pelanggan: susun laporan insiden (skill laporan-insiden-usaha).

ℹ️ Data: 6 hari kosong (Min, 23 Agu, Min, 30 Agu, Min, 6 Sep…) tidak diisi tebakan; 4 angka ekstrem lama tidak dipakai di rata-rata.
Catatan: ini peringatan statistik (tanda untuk dicek), bukan kepastian masalah atau ramalan pasti.
```
Verifikasi `verif2.py` (spesifikasi v1.0.1: model normal/hitungan, peluang ekor, aturan bertahan):
**51 angka/level dibandingkan, 0 beda.** Level reject/downtime/% reject 🔴, stok 🔴 (2,8 ≤ lead 3,
"kosong ±0,2 hari" = 3 − 2,828 ✓), absen 🟡 (model hitungan, beruntun 3), output 🟡 (3/7 di bawah target).
Deret reject per tanggal: 23 Sep 🟡 · 24 Sep ✅ · 25 Sep 🟡 (2,0σ) · **26 Sep 🟠** (2,3σ, 2 dari 3 hari) ·
28 Sep 🔴 — 🟠 masih 2 hari sebelum target 40 dilanggar (v1.0.0: 3 hari). Label `Stok kain (m)` ✓,
pertanyaan cek downtime kini spesifik ✓, catatan hari ini tidak dikutip (tanpa `--sertakan-catatan`) ✓.
