# HASIL UJI — pph-final-umkm

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Lingkungan:** folder kerja `/tmp/uji-pph-final-umkm/`, Python 3 standar
- **Skenario:** 01–05 + uji A/B (00)

## Audit keamanan
- `scripts/pph_final.py`: hanya `argparse, csv, datetime, json, re, sys, decimal`. Hanya membaca file yang diberikan lewat `--file`; tidak menulis file, tidak ada jaringan/subprocess/kredensial.
- SKILL.md/README/references: tidak ada prompt injection. **Aman.**

## Verifikasi angka (independen)
- Script terpisah (`verif.py`, aritmetika bilangan bulat, tidak mengimpor script skill) membandingkan **400 kasus acak** (OP/badan, 1–12 bulan, bulan awal acak, omzet sebelumnya 0–600 jt, omzet 0–1 M per bulan) → **0 selisih** untuk omzet kena pajak, PPh per bulan, total PPh, dan tanggal setor (termasuk Desember → 15 Januari tahun berikutnya).
- Rumus OP: kena pajak = max(0, kumulatif_sesudah − max(kumulatif_sebelum, 500 jt)) — bulan yang melewati batas dihitung proporsional. **Benar.** Badan: seluruh omzet, tanpa pembebasan. **Benar.**
- Contoh SKILL.md/README (Juni kumulatif 545 jt → kena 45 jt → Rp225.000; Juli 70 jt → Rp350.000): **benar**.
- Data tepi: "Rp 1.500.000", "1.500.000,50", omzet 0, CSV dengan "Rp 41.250.000" dan kolom PPh 22 kosong → benar. "abc", "-5jt", 13 bulan, mulai Desember + 2 nilai, file kosong, CSV tanpa kolom omzet, bulan ganda, `--jenis-badan` untuk OP → ditolak dengan `ERROR:` yang jelas. Omzet melewati Rp4,8 M (badan) → keterangan & catatan muncul.

## Kepatuhan fokus khusus
- Batas Rp500 juta OP & bulan proporsional: benar.
- Badan tanpa pembebasan: benar; CV/firma/PT diberi label simulasi + arahkan DJP.
- Klaim BELUM TERVERIFIKASI (masa transisi CV/firma/PT, batas jangka waktu tarif 0,5%, TikTok Shop sebagai pemungut) tidak dinyatakan pasti — tercantum sebagai "belum kami verifikasi" di output. Bagus.
- Disclaimer + dasar aturan + tanggal berlaku: selalu ada.

## Skor

| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description) | 9 | Frasa awam ("pajak UMKM bulan ini berapa", "omzet 500 juta bebas pajak") + EN; batas dengan hitung-ppn jelas |
| Kemudahan awam | 9 | Cukup ketik omzet per bulan; CSV/JSON juga bisa |
| Kualitas output | 8 | Tabel lengkap & siap simpan; belum menandai tanggal setor yang sudah lewat |
| Akurasi (angka/fakta) | 9 | 0 selisih pada 400 kasus; hal belum terverifikasi diberi label; bug teks kecil pada kumulatif tepat Rp500 juta |
| Penanganan input kurang | 9 | Pertanyaan tepat (jenis WP, omzet sebelumnya), catatan otomatis bila data tidak mulai Januari |
| Penanganan di luar cakupan | 9 | Pekerjaan bebas, PPh 21, SPT/kode billing jelas diarahkan |
| Keamanan | 10 | Bersih |

## SKOR AKHIR: **8 / 10** — LULUS

Uji A/B: dengan skill jelas lebih baik (tabel per bulan, tanggal setor, status aturan yang jujur; jawaban tanpa skill menyatakan pasti "maksimal 7 tahun" yang menurut referensi skill belum terverifikasi setelah PP 20/2026). Tidak ada cacat berat.

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
1. **Teks ringkasan salah saat omzet kumulatif tepat Rp500.000.000**: tercetak "Batas Rp500 juta bebas pajak sudah terlewati (None)." (uji: `--omzet 200jt 300jt`). Batas belum terlewati (tepat Rp500 juta masih bebas) dan "None" bocor ke output. Lokasi: `teks_markdown()`, cabang `else` setelah `if r["sisa_omzet_bebas_pajak"] > 0`. Saran: bila `bulan_mulai_kena_pajak` kosong, tulis "Batas Rp500 juta sudah tercapai (belum ada omzet kena pajak). Omzet berikutnya kena 0,5% penuh."
2. **Tanggal setor yang sudah lewat tidak ditandai.** Di S1 & S2 batas setor Agustus (2026-09-15) sudah lewat pada tanggal uji, tetapi output diam. Untuk alat pajak, ini risiko nyata (sanksi). Saran: di `hitung()`, bandingkan `batas_setor` dengan `datetime.date.today()`; bila lewat dan PPh > 0, tambah keterangan "batas setor sudah lewat — segera setor, cek sanksi ke DJP", dan tambahkan butir ini di checklist SKILL.md.

### Ringan
3. Badan dengan `--omzet-sebelumnya`: PPh atas omzet sebelumnya (mis. 0,5% × 900 jt = Rp4,5 jt) tidak disebut. Saran: tambahkan catatan otomatis untuk badan bila `omzet_sebelumnya > 0` ("PPh untuk omzet sebelumnya seharusnya sudah disetor per bulan: ±Rp…").
4. `baca_file()`: bila CSV terbaca sebagai satu kolom (Sniffer gagal, header "bulan;omzet"), `cari_kolom` mengembalikan indeks yang sama untuk bulan & omzet, sehingga pesan error menyesatkan ("'Jan' bukan angka"). Saran: bila `ib == io`, tampilkan "pemisah kolom tidak dikenali; pakai ; atau ,".
5. `references/regulasi.md` bagian PPh 22: tanggal "berlaku 1 Agustus 2026" ditulis tanpa kolom status, padahal butir lain punya status. Saran: beri status verifikasi + sumber tanggal mulai efektif.
6. README FAQ "Saya CV…": kalimat "Aturan baru (PP 20/2026) mengeluarkan CV, firma, dan PT biasa…" sebaiknya ditambah "lama masa transisinya belum kami verifikasi" agar selaras dengan referensi.

## Riwayat uji OpenClaw sebelum/sesudah per skill
| Tanggal | Versi | Uji | Tanpa skill | Dengan skill | Selisih | Verdik | Catatan |
|---|---|---|:-:|:-:|:-:|---|---|
| 2026-10-14 | 1.0.3 | OpenClaw 2026.10.2 lokal, hanya skill ini vs tanpa skill; 5 skenario (3 normal + 1 Telegram + 1 input kurang); penguji independen | 6,8 | 6,1 | -0,7 | **BELUM** | Rincian di `00-openclaw-sebelum-sesudah.md`. Angka script benar, tetapi: PPh 22 marketplace tidak diperhitungkan sebagai pengurang PPh final (FAQ DJP PMK 37/2025 versi 1 Juli 2026) sehingga "telat"/jumlah setor keliru; batas waktu tarif 0,5% masih menurut PP 55/2022 padahal PP 20/2026 menghapusnya untuk orang pribadi & PT perorangan (sumber praktisi, PERLU REVIEW naskah resmi); agent salah menyebut "hari ini 15 Okt" (2x) dan subtotal Rp995.000 (seharusnya Rp975.000). |
| 2026-10-16 | 1.0.5 | OpenClaw 2026.10.2 lokal, penguji independen; 5 skenario (termasuk konteks kanal Telegram `uji-tg.sh`); TANPA memakai skor 14 Okt | 6,8 | 8,8 | +2,0 | **LULUS** | Rincian di `00-openclaw-sebelum-sesudah.md`. Tanpa salah angka. Catatan: tabel 9 kolom dengan 7 baris Rp0, jawaban ±3.800–4.200 karakter (panjang untuk chat). |
| 2026-10-17 | 1.0.5 | Pra-cek konteks kanal Telegram Akun A (`uji-tg.sh`, satu giliran, hanya sisi DENGAN) | – | 7,5 | – | **TIDAK SIAP** | `koordinasi/pracek-telegram-akun-a-2026-10-17.md`. Semua angka benar (Rp107.500 / Rp330.000 / total Rp437.500; kurang setor Rp165.000; sisa batas Rp4.212.500.000), tetapi tabel 10 kolom di blok kode selebar ±120 karakter harus digeser ke samping di ponsel. Diperbaiki di 1.0.6 (bagian di bawah). |

## Revisi 1.0.6 (2026-10-17) — tampilan chat tanpa tabel lebar

**Temuan (pra-cek Telegram 17 Okt, versi 1.0.5):** angka benar, tetapi balasan memuat tabel Markdown 9–10 kolom. Di Telegram, OpenClaw mengubah tabel Markdown menjadi blok kode monospace (lihat juga `koordinasi/pilot-telegram-2026-10-02.md`), sehingga baris ±120 karakter harus digeser ke samping di ponsel.

**Perbaikan (pembuat skill):**
- Script mencetak blok chat siap salin sebagai tampilan bawaan (`--tampilan chat`): tanpa tabel dan tanpa blok kode; tiap bulan satu baris pendek maks. 3 kolom (`**Bulan** · omzet … · PPh …`) + satu kalimat keterangan (kena pajak, PPh 22 → kurang/lebih, setor paling lambat + status); bulan bebas berurutan digabung (lebih dipungut per bulan tetap disebut); ringkasan berupa baris pendek; catatan versi chat dengan kualifikasi aturan tetap ada. Tabel lebar hanya dengan `--tampilan tabel` (terminal/berkas).
- Blok maks. 3.800 karakter; data panjang → makin ringkas (3 tingkat) tanpa membuang kurang setor/tanggal/status atau PPh 22 & lebih dipungut per masa; bila masih terlalu panjang → dibagi dua pesan dengan penanda `<<< PESAN BERIKUTNYA >>>` (aturan di SKILL.md langkah 3).
- SKILL.md: di chat dilarang tabel & blok kode; blok keluaran disalin utuh; aturan dua pesan.

**Verifikasi independen draf pertama 1.0.6 (2026-10-17): PERLU_PERBAIKAN** (1 sedang + 4 ringan). Positif: JSON & tabel identik dengan 1.0.5 (33 masukan valid + 11 salah), hitung ulang Decimal independen cocok, tanpa tabel/``` di blok chat. Temuan: (sedang) blok > 3.800 karakter pada rekap 12 bulan orang pribadi dengan PPh 22 tiap bulan yang ditanya sesudah tahun berakhir (profil verifikator: median 3.749, p90 3.992, maks 4.234; 376/800 > 3.800); (ringan) di tingkat paling ringkas bulan lunas/lebih kehilangan baris keterangan sehingga PPh 22 & lebih dipungut per masa hilang, dan tes melewati cek status bila itu terjadi; klaim "≤ 60 karakter" tidak mutlak; beberapa kualifikasi aturan terpotong dibanding 1.0.5; materi README masih tabel lama. Semua diperbaiki (rincian di `CHANGELOG.md`).

**Verifikasi oleh pembuat sesudah perbaikan (otomatis):**
- Skenario pra-cek (skenario 1 `00-openclaw-sebelum-sesudah.md`, hari ini Sabtu 17 Oktober 2026): blok chat 2.780 karakter (satu pesan), baris data terpanjang 56 karakter tampil; angka sama: Agustus PPh Rp107.500 (kena Rp21.500.000; PPh 22 Rp180.000 → lebih Rp72.500), September PPh Rp330.000 (PPh 22 Rp165.000 → kurang Rp165.000, Kamis 15 Okt 2026 SUDAH LEWAT), total Rp437.500, sisa batas Rp4,8 miliar Rp4.212.500.000, surat pernyataan paling lambat Senin 31 Agustus 2026 (bersyarat), pembulatan belum dicocokkan dengan Coretax.
- Profil rekap tahunan verifikator (alat verifikator dipakai ulang): 796/800 satu pesan, terpanjang 3.798; 4/800 dibagi dua pesan. Profil omzet Rp40–120 juta/bulan: 1.600/1.600 satu pesan. Fuzz berat 12 bulan (bulat & bersen, 24.000 kasus): tidak ada bagian > 3.800, tidak ada keterangan wajib yang hilang; ±5% dibagi dua. Contoh verifikator (2027, hari ini 15 Feb 2028) → dua pesan 2.219 + 3.064 karakter, termasuk Maret "PPh 22 Rp3.241.000; lebih Rp926.000".
- Baris data terlebar: 56 (pra-cek), 60 (omzet < Rp1 miliar tanpa sen), 64 (omzet ≥ Rp1 miliar dan bersen).
- Keluaran `--format json` dan `--tampilan tabel` identik dengan 1.0.5 pada 311 kasus; hanya nomor versi berbeda → logika hitung tidak berubah.
- `tests/test_pph_final.py`: 27 tes lulus (9 untuk tampilan chat).

**Status:** perbaikan tampilan selesai; **masih perlu pra-cek ulang konteks kanal Telegram (`uji-tg.sh`) oleh penguji independen** sebelum masuk gelombang Telegram bot asli. Tampilan di aplikasi Telegram/WhatsApp sungguhan belum dilihat.
