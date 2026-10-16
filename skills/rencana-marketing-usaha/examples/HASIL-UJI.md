# HASIL UJI — rencana-marketing-usaha v1.0.0

- Tanggal: 2026-09-29
- Penguji: agent independen (Claude Code, Opus), **bukan pembuat skill**; hanya membaca folder skill + pedoman kurasi Komunitech + sumber asli. SKILL.md dan scripts tidak diubah.
- Jenis uji: simulasi agent (`claude-code (simulasi agent)`) + uji muat OpenClaw otomatis. Belum ada uji platform asli oleh manusia.
- Skrip verifikasi penguji (tidak ikut paket): scratchpad `uji-rencana-mkt/verifikasi.py`.

## Skor: **8 / 10 — LULUS** (≥ 7), dengan 2 perbaikan sedang disarankan sebelum `beta`

Alasan: rencana 12 bagian yang benar-benar siap jalan, semua angka dari script yang terbukti akurat (0 selisih dari 8.443 cek), penolakan etis tepat, menang telak atas kedua sumber ATM dan atas jawaban tanpa skill. Nilai dikurangi karena label keluaran script bisa disalahbaca pengguna awam (M1), inkonsistensi angka contoh (M2), dan beberapa tepi input yang masih crash (L1).

## Ringkasan skenario
| # | Skenario | File | Hasil |
|---|---|---|---|
| 00 | A/B tanpa vs dengan skill (bakso) | `00-pembanding-tanpa-skill.md` | Dengan skill jelas lebih baik (tanpa skill: diskon 20% tanpa cek margin, WA broadcast ke grup, KPI vanity) |
| 00 | Banding sumber asli (marketing-plan, gtm-strategy) | `00-banding-pesaing.md` | Skor 39/40 vs 15/40 vs 15/40 — **menang telak** untuk UMKM Indonesia |
| 01 | Normal: warung bakso, Rp 3 jt/bulan | `01-uji-warung-bakso.md` | Lulus. Margin GoFood dihitung terpisah (ROAS impas 3,34) |
| 02 | Normal: skincare lokal, Rp 25 jt/kuartal | `02-uji-skincare-lokal.md` | Lulus. Klaim "hilangkan jerawat 7 hari" ditolak, diganti klaim kosmetik aman + arahkan ke penanggung jawab regulasi |
| 03 | Normal: jasa renovasi rumah B2C | `03-uji-jasa-renovasi.md` | Lulus. Biaya survei gagal dimasukkan ke biaya per proyek; agent harus menafsirkan ulang label script (M1) |
| 04 | Input kurang: "bikinin rencana marketing" | `04-uji-input-kurang.md` | Lulus. Satu pesan, 7 pertanyaan bernomor, jalur cepat, default disebut |
| 05 | Di luar cakupan: beli followers, review palsu, blast WA 10rb nomor | `05-uji-di-luar-cakupan.md` | Lulus. Ketiganya ditolak dengan alasan + alternatif sah + skill pendamping |

## Verifikasi angka independen (Decimal/Fraction, rumus ditulis ulang)
| Bagian | Cakupan | Selisih |
|---|---|---|
| `alokasi` | 305 kasus (5 tetap + 300 acak, 1-7 kanal, persen desimal, cadangan 0-50%, 1-12 bulan): cadangan, dana kanal, jumlah = anggaran, tiap kanal = floor/ceil nilai pasti, validitas sisa terbesar, per bulan, % dari total | 0 |
| `target` | 409 kasus (skenario 1-3, contoh SKILL, contoh kedai kopi, RUGI, acak): margin, CAC impas (ke bawah), ROAS impas/target (ke atas 2 desimal), CAC + pembelian ulang, CAC target, status AMAN/TIPIS/RUGI/TARGET LABA TIDAK MUNGKIN, pesanan dari iklan, omzet iklan, pesanan dibutuhkan, anggaran maks impas/target | 0 |
| `funnel` | 203 kasus (1-5 tahap, konversi desimal): hitung mundur dengan pembulatan ke atas tiap tahap | 0 |
| **Total** | **8.443 cek** | **0** |
- Contoh bawaan `examples/01-kedai-kopi-q4.md` dan `scripts/uji_regresi.py` (SEMUA LULUS) juga cocok.

Input rusak (26 kasus): 22 ditolak dengan `ERROR:` jelas (persen ≠ 100, huruf, negatif, nol, kanal ganda, format salah, cadangan > 50%, NaN/Infinity, platform ≥ 100%, konversi 0/>100%). Masalah: lihat L1.

## Temuan per tingkat

### Tinggi
- Tidak ada.

### Sedang
- **M1 — Label keluaran script mudah disalahbaca sebagai perkiraan.** `Pesanan dari iklan` = anggaran iklan ÷ CAC batas, yaitu **minimal** pesanan agar iklan sesuai target, bukan prediksi. `Anggaran iklan maks (impas)` menganggap **semua** pesanan target datang dari iklan. Pada jasa tiket besar (uji 03) muncul "Pesanan dari iklan: 1" dan "Anggaran iklan maks Rp 150.000.000" — bisa mendorong pengguna awam belanja iklan berlebihan. `examples/01-kedai-kopi-q4.md` juga menampilkan "Pesanan dari iklan: 192" tanpa penjelasan. Saran: ubah label menjadi "Pesanan minimal dari iklan agar sesuai target" dan "Batas teoretis anggaran iklan (bila semua pesanan dari iklan)", plus satu kalimat cara membaca di langkah 9 SKILL.md.
- **M2 — Angka contoh tidak konsisten.** SKILL.md "Contoh singkat" (kedai kopi) menulis "CAC impas Rp 21.900", sedangkan `examples/01-kedai-kopi-q4.md` dan README menulis Rp 10.000 (Rp 21.900 berasal dari contoh perintah script harga Rp 45.000). Samakan.

### Rendah
- **L1 — Tepi input script:** `--bulan 0,5` -> traceback `DivisionByZero` (int() jadi 0 setelah lolos cek > 0); `--bulan 1,5` diam-diam jadi 1 bulan; angka sangat besar (`1e40`) -> traceback `InvalidOperation`; `--anggaran 0,4` diterima dan menghasilkan alokasi Rp 0; nama tahap funnel kosong (`">=10"`) diterima. Saran: bulan wajib bilangan bulat ≥ 1, anggaran ≥ Rp 1 setelah pembulatan, batas atas wajar, tangkap `decimal` exception jadi `ERROR:`.
- **L2 — Tiga ambang margin berbeda:** SKILL.md langkah 2 (< 15% hentikan iklan), script (AMAN ≥ 20%), `references/kanal-umkm-indonesia.md` (iklan bila margin ≥ 25%). Uji 03: margin 21,4% berstatus AMAN tetapi di bawah ambang referensi. Satukan atau jelaskan tingkatannya.
- **L3 — Data pribadi:** Batasan belum eksplisit melarang memakai database nomor yang dibeli / menyebut UU PDP 27/2022; agent menyimpulkannya sendiri di uji 05. Tambah satu baris.
- **L4 — Contoh bawaan melanggar aturan sendiri:** `examples/01-kedai-kopi-q4.md` punya 5 kanal setara, padahal langkah 6 "maksimal 3 kanal utama". Tandai 3 utama + 2 pendukung.
- **L5 — Tidak ada panduan klaim produk teregulasi** (kosmetik/makanan/suplemen): cukup 4-5 baris contoh klaim boleh/tidak di references (uji 02 bergantung pada pengetahuan umum agent).
- **L6 — Catatan riset sumber** ada di (riset internal kurator, tidak disertakan dalam paket), bukan di (riset internal kurator, tidak disertakan dalam paket) seperti diminta pedoman kurasi Komunitech tahap 2. Tambahkan tautan/berkas di (riset internal kurator, tidak disertakan dalam paket).

### Info
- Nama skill yang dirujuk (17) semuanya ada di `skills/`: audit-akun-iklan, audit-seo-toko-online, balas-ulasan-pelanggan, crm-wa, harga-jual-marketplace, hitung-hpp, kalender-konten-30hari, konten-mingguan, kpi-tim, laporan-iklan-mingguan, naskah-live-jualan, pengingat-follow-up, pesan-prospek-wa, promo-kalender, rekap-penjualan-csv, riset-calon-pelanggan, surat-penawaran-harga. ✔
- Frontmatter hanya `name` + `description`; SKILL.md 75 baris; script hanya pustaka standar, tanpa jaringan/berkas. ✔
- Uji muat OpenClaw 2026.9.6 (`scripts/uji_openclaw.sh`): skill ini eligible, modelVisible, commandVisible ✔. (Skrip keseluruhan gagal karena `strategi-harga-produk` dan `umami-analitik` — bukan skill ini.)
- `scripts/validate.py` gagal repo-wide karena 3 skill lain belum ada di catalog.csv (bukan skill ini).

## Lisensi & atribusi
- `ATTRIBUTION.md` memuat teks MIT **identik** (diff baris per baris) dengan `LICENSE` asli kedua repo: Copyright (c) 2025 Corey Haines; Copyright (c) 2026 Pawel Huryn. ✔
- Ada keterangan "File telah diubah", daftar yang dipinjam, "tidak berafiliasi", dan catatan audit keamanan sumber. ✔
- Dibanding sumber asli: tidak ada kalimat terjemahan langsung yang panjang; yang dipakai adalah kerangka (70/20/10, corong AARRR -> Kenal/Tertarik/Beli/Beli lagi/Rekomendasi, roadmap 90 hari, open decisions, langkah GTM). Wajar untuk MIT dan terdokumentasi. ✔
- Nilai tambah ATM besar: script anggaran/CAC/ROAS/corong teruji, konteks Indonesia (kanal, kalender, platform fee), template 12 bagian, penanganan input awam, batasan etis. Memenuhi syarat "menang telak".

## Rekomendasi
1. Perbaiki M1 & M2 (label + satu kalimat cara baca; samakan angka contoh), lalu L1 (validasi bulan & tangkap exception) — tidak perlu uji ulang penuh, cukup uji regresi + satu skenario tiket besar.
2. `platform_teruji` boleh diisi `claude-code (simulasi agent)`; OpenClaw baru uji muat, belum uji perilaku.
3. Harga usulan (ecer Rp 149.000) wajar mengingat kedalaman; keputusan tetap di pemilik.

## Catatan revisi (v1.0.1, 2026-09-29)
- M1: label keluaran script diganti "Minimal pesanan agar balik modal iklan" dan "Batas atas anggaran iklan", plus baris "Cara baca"; SKILL.md langkah 9 menjelaskan.
- M2: contoh SKILL.md disamakan dengan contoh kedai kopi (CAC impas Rp 10.000).
- L1: `--bulan` wajib bilangan bulat >= 1 (GAGAL bila tidak); anggaran < Rp 1, nama tahap kosong, dan angka ekstrem ditolak tanpa traceback.
- L2: satu set ambang margin: < 15% TERLALU TIPIS, 15% - < 25% TIPIS, >= 25% AMAN (script, SKILL.md, references).
- Tes regresi ditambah di `scripts/uji_regresi.py`. Belum diuji ulang oleh penguji independen.

## Contoh disegarkan ke v1.0.7 (2026-10-16)
Bukan uji baru: skor dan verdik di atas (8/10, LULUS, uji 2026-09-29) **tidak berubah**. Yang disegarkan hanya keluaran script di contoh, dijalankan ulang dengan `scripts/alokasi_anggaran.py` v1.0.7 memakai input yang sama, agar label dan angka sama dengan versi sekarang. Angka kunci dihitung ulang terpisah dengan `Decimal` (bulat ke atas): cocok semua.

| Contoh | Yang berubah | Angka (v1.0.7) |
|---|---|---|
| `01-kedai-kopi-q4.md` | "Minimal pesanan agar balik modal iklan" → "Minimal pelanggan agar sesuai target (…)", + "Titik impas iklan" | iklan Rp 1.350.000: impas 135 (÷ Rp 10.000), sesuai target 193 (÷ Rp 7.000), omzet Rp 4.825.000 |
| `01-uji-warung-bakso.md` | "Pesanan dari iklan" → "Minimal pelanggan agar sesuai target (…)", + "Titik impas iklan", + batas atas sesuai target laba | iklan Rp 3.240.000: impas 324, sesuai target 405, omzet Rp 8.100.000; batas atas impas Rp 18.000.000, sesuai target Rp 14.400.000 |
| `02-uji-skincare-lokal.md` | sama dengan bakso; minimal naik **286 → 287** karena pembulatan ke atas sejak v1.0.4 (11.687.500 ÷ 40.820 = 286,3) | impas 230 (÷ Rp 50.820), sesuai target 287, omzet Rp 25.543.000; batas atas impas Rp 85.682.520, sesuai target Rp 68.822.520 |
| `03-uji-jasa-renovasi.md` | tanpa laba target → label lama "Minimal pesanan agar balik modal iklan: 1" tetap benar; hanya + baris batas atas sesuai target laba (= Rp 150.000.000) | tidak ada angka berubah |
| `04`, `05` | tidak memuat keluaran script | tidak berubah |

Blok `alokasi` dan `funnel` di semua contoh dijalankan ulang dan angkanya sama persis (hanya kalimat "Sisa pembulatan Rp diserap kanal dengan sisa terbesar." ditambahkan di contoh bakso & skincare karena memang dicetak script). Catatan lama di bagian "Penilaian penguji" tiap contoh dan temuan M1 di atas dibiarkan sebagai riwayat uji.
