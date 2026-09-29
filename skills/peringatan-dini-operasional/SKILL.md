---
name: peringatan-dini-operasional
description: Membaca log harian operasional (CSV/Excel/tabel tempel - output produksi, reject, stok bahan & pemakaian, penjualan, keluhan, telat kirim, absensi) lalu menghitung rata-rata 7 hari, tren, banding target & hari yang sama 4 minggu lalu, batas kendali 2σ/3σ, dan sisa hari stok, menandai peringatan dini 🔴/🟠/🟡 beserta alasannya dalam bahasa sehari-hari, plus daftar cek akar masalah - laporan 1 halaman siap kirim ke Telegram, bisa dijadwalkan harian di OpenClaw. Gunakan saat pengguna minta "peringatan dini", "analisa masalah operasional", "prediksi kendala", "cek log produksi/harian", "kenapa reject naik", "stok cukup berapa hari", early warning, anomaly detection, control chart, daily operations KPI alert untuk pabrik/F&B/toko/distributor. Bukan untuk rekap penjualan biasa, laporan keuangan, atau ramalan penjualan jangka panjang.
---

# Peringatan Dini Operasional

## Tujuan
Manajer/pemilik usaha cukup mengisi log harian sederhana (tanggal + beberapa angka). Skill ini
memberi tahu **apa yang mulai tidak normal sebelum jadi masalah besar**, **seberapa serius**
(🔴/🟠/🟡), **kenapa dianggap tidak normal** (dengan angka), dan **apa yang perlu dicek hari
ini** — dalam satu pesan pendek siap kirim ke Telegram. Semua angka dihitung script (Python
standar), bukan ditebak.

## Kapan digunakan
- "Ini log produksi 30 hari terakhir, ada yang perlu diwaspadai?"
- "Reject minggu ini kok naik terus, cek dong." / "Stok tepung cukup sampai kapan?"
- "Analisa masalah operasional & prediksi kendala dari data harian ini."
- "Tiap malam kirimi saya peringatan kalau ada angka yang aneh." (+ jadwal OpenClaw)
- Cocok untuk pabrik/konveksi, dapur F&B/katering, toko/retail, gudang/distributor, klinik
  (hanya angka operasional agregat).

## Kapan TIDAK digunakan
- Rekap omzet/produk terlaris dari transaksi → `rekap-penjualan-csv`.
- Ringkasan harian semua alat lokal Komunitech (kasir, stok, absensi) → `laporan-harian-usaha`.
- Laporan keuangan/laba rugi → `laporan-keuangan-emkm`; proyeksi kas → `arus-kas-13minggu`.
- Menyusun laporan kejadian yang **sudah** terjadi (kronologi, dampak, minta maaf) →
  `laporan-insiden-usaha` (skill ini merujuk ke sana bila peringatan berujung kerugian/komplain).
- Ramalan penjualan bulanan/tahunan, perencanaan produksi, atau "pasti terjadi" → jelaskan jujur
  bahwa skill ini hanya peringatan statistik jangka pendek (≤ 7 hari).
- Data pasien/diagnosis, data per karyawan yang menyebut nama untuk dinilai → hanya angka
  agregat (jumlah absen, jumlah kunjungan). Jangan menilai orang tertentu.
- Pemantauan mesin real-time (sensor/IoT per menit) → di luar cakupan; skill ini untuk log harian.

## Input
Satu tabel log harian. Minimal kolom **tanggal** + 1 kolom angka. Diterima: `.csv` (koma, titik
koma, tab), `.xlsx` (lembar pertama), atau tabel yang ditempel di chat. Template kosong:
`templates/log-harian-template.csv`.

Kalau pengguna belum memberi data atau info kurang, tanyakan **sekali** dalam satu pesan:
1. Kirim/tempel log hariannya (minimal 7 hari; ideal ≥ 15 hari, terbaik 4–5 minggu). Belum
   punya? berikan `templates/log-harian-template.csv` dan jelaskan cara mengisinya.
2. Ada target? (mis. reject maks 50/hari, output min 2.000) — boleh dikosongkan.
3. Untuk stok: berapa hari biasanya pemasok mengirim setelah dipesan? (default 2 hari)
4. Nama usaha untuk judul laporan (opsional).

Pengguna ingin cepat → jalankan langsung dengan default (tanpa target, lead time 2 hari, arah
metrik ditebak dari nama kolom) dan sebutkan asumsinya di bawah laporan.

## Langkah kerja

### 1. Siapkan file
- File dari pengguna → pakai path-nya langsung.
- Tabel ditempel di chat → simpan apa adanya ke file sementara `log.txt` (tabel ber-garis tegak
  `|` dan tab dari Excel/Sheets terbaca). Tabel berspasi biasa (dari WA) → ubah dulu menjadi CSV
  titik koma **tanpa mengubah angka satu pun**.
- `.xls` lama/Google Sheets → minta simpan sebagai `.xlsx` atau CSV (File → Download → CSV).

### 2. Jalankan script
Path relatif terhadap folder berisi SKILL.md ini (Windows: `python` atau `py`):
```bash
python3 <folder-skill-ini>/scripts/peringatan_dini.py "<log.csv>" --format json
python3 <folder-skill-ini>/scripts/peringatan_dini.py "<log.csv>" --nama-usaha "<nama>"
```
Opsi (tambahkan pada kedua perintah):
| Kebutuhan | Opsi |
|---|---|
| Target (maks untuk hal buruk, min untuk hal baik) | `--target reject_pcs=50 --target output_pcs=2000`, atau baris `TARGET` di file |
| Arah salah tebak / kolom tak dikenal | `--arah suhu_oven=dua` · `--arah sisa_roti=naik` (`naik` = makin besar makin buruk) |
| Pasangan stok tidak terdeteksi otomatis | `--stok stok_gula:pakai_gula` (tanpa kolom pakai: `--stok stok_gula`) |
| Lama pemasok mengirim | `--lead-time 3` atau `--lead-time stok_tepung_kg=4` |
| Hari tidak normal (libur nasional, bazar) | `--abaikan-tanggal 2026-08-17,2026-09-05` |
| Laporan untuk tanggal tertentu | `--tanggal 2026-09-29` (default: tanggal terakhir di data) |
| Satu tanggal muncul beberapa baris (per shift) | `--duplikat jumlah` (default: baris terakhir dipakai) |
| Format tanggal bulan/hari (AS) | `--urutan-tanggal mdy` |
| Jangan tambahkan metrik % reject otomatis | `--tanpa-rasio` |
| Kejadian kritis: setiap angka > 0 = 🔴 (otomatis untuk kecelakaan/K3/cedera/insiden/kebakaran/keracunan) | `--kejadian mesin_rusak` |
| Kutip kolom catatan/keterangan di pesan (hanya bila pengguna minta; lihat Privasi) | `--sertakan-catatan` |

Dari JSON, periksa sebelum melapor:
- `metrik[].model` — `normal` (σ), `hitungan` (angka bulat rata-rata < 20/hari: keluhan, retur,
  telat, absen — pakai peluang Poisson), `kejadian` (tiap kejadian = 🔴), `konstan` (angka biasanya
  selalu sama → pakai persen selisih). Kolom yang jarang terjadi tapi kritis (mis. `mesin_rusak`,
  `tumpahan_bahan`) tanyakan: "setiap kejadian perlu 🔴?" → bila ya, jalankan ulang dengan `--kejadian`.
- `metrik[].arah` — kalau ada kolom yang arahnya salah (mis. `sisa_roti` ditebak `dua`), jalankan
  ulang dengan `--arah`. Kolom yang tidak dikenal lebih baik ditanyakan daripada ditebak.
- `kualitas_data` — `hari_kosong`, `baris_dilewati`, `sel_rusak`, `angka_ambigu`,
  `tanggal_duplikat`, `tidak_diisi_hari_ini`: sampaikan singkat ke pengguna.
- `catatan` — sampaikan apa adanya (mis. metrik `% reject` ditambahkan, angka ambigu).
- `data_sedikit: true` → tegaskan keterbatasannya (lihat Batasan).
- Kode keluar `2` / `galat` → tunjukkan pesannya, bantu perbaiki file, **jangan mengarang laporan**.

### 3. Sampaikan laporan
- Tampilkan `laporan_teks` (output mode teks) **apa adanya** — itu versi siap kirim Telegram
  (± 30 baris, tanpa tabel markdown supaya rapi di HP). Jangan mengubah angka, warna, atau alasan.
- Di bawahnya (di luar pesan siap kirim), tambahkan maksimal 3 kalimat analisis dari agent:
  kaitkan peringatan dengan `catatan_hari_ini` (JSON) bila relevan — **tanpa menyebut nama orang** (mis. "reject naik
  sejak 26 Sep, bersamaan dengan catatan 'tepung merk baru' 28 Sep — cek ini lebih dulu"), tanpa
  menyatakannya sebagai penyebab pasti.
- Tawarkan langkah lanjut: (a) isi 5 kenapa bersama tim untuk peringatan 🔴 teratas,
  (b) bila sudah ada kerugian/komplain → `laporan-insiden-usaha`, (c) jadwal harian (Langkah 4).

### 4. (Opsional) Jadwal harian di OpenClaw
Ikuti `references/jadwal-openclaw.md` — pola `openclaw automations add` di sana disalin dari
skill `laporan-otomatis-terjadwal` yang sudah diverifikasi; **jangan mengarang perintah atau
flag lain**. Urutan wajib: uji manual → tunjukkan contoh → minta izin "ya" → `add` → catat `id`
→ `run <id> --wait` → jelaskan cara jeda/hapus → ingatkan komputer harus menyala. Kanal default
Telegram; WhatsApp hanya nomor terpisah + persetujuan risiko tertulis, hanya ke pemilik sendiri.

## Format output (dari script)
```
🚨 PERINGATAN DINI OPERASIONAL
<Nama usaha> — <Hari, tanggal>
Data <awal>–<akhir> (<n> hari tercatat)
Ringkas: <n> 🔴 · <n> 🟠 · <n> 🟡 · <n> normal

🔴 <Metrik>: <nilai> hari ini (kemarin <nilai>)
   <alasan 1>; <alasan 2>; <alasan 3>.
🟠 Stok <bahan>: sisa <x> = ±<h> hari pemakaian ... -> perkiraan habis <tanggal>
✅ Normal: <daftar>
📝 Catatan hari ini: "<isi kolom catatan>"   ← hanya dengan --sertakan-catatan

❓ Cek hari ini (cari akar masalah, bukan cari kambing hitam):
<Metrik>: • 3 pertanyaan (bahan/mesin/orang/cara kerja/pengukuran)
5 kenapa: Kenapa <metrik> naik? → karena … → …
Kalau sudah ada kerugian/komplain pelanggan: susun laporan insiden (skill laporan-insiden-usaha).

ℹ️ Data: <hari kosong, baris dilewati, pencilan>
Catatan: ini peringatan statistik (tanda untuk dicek), bukan kepastian masalah atau ramalan pasti.
```
Aturan warna & ambang lengkap: `references/cara-kerja-aturan.md`.

## Contoh
**Input:** "Ini log 30 hari pabrik roti saya (file terlampir). Target reject maks 50, output min
2.000, penjualan min 9 juta. Pemasok tepung butuh 2 hari."

**Hasil (ringkas, lengkap di `examples/01-pabrik-roti-30-hari.md`):**
```
🔴 Reject (pcs): 63 hari ini (kemarin 46)
   6,8σ di atas rata-rata 27 hari sebelumnya (31,15) -- lewat batas bahaya 3σ; 112% di atas
   rata-rata hari Selasa 4 minggu terakhir (29,75); melewati target maks 50 (+26%).
🟠 Stok tepung (kg): sisa 169 = ±3,2 hari pemakaian (rata-rata 52,29/hari) -> perkiraan habis
   Jum, 2 Okt; pemasok butuh 2 hari -- siapkan pesanan
```

## Batasan & penanganan error
- **Bukan ramalan pasti.** Peringatan = "angka ini tidak biasa, layak dicek". Proyeksi hanya
  garis lurus 7 hari (ditulis "perkiraan kasar"). Jangan pernah menulis "pasti", "dijamin", atau
  menyebut penyebab sebagai fakta; penyebab dicari lewat pertanyaan cek & 5 kenapa.
- **Data minimum:** rata-rata 7 hari butuh 7 hari; tren butuh 5 angka dalam 7 hari terakhir;
  batas σ butuh 14 angka **sebelum** hari ini; banding hari yang sama butuh 2 minggu; sisa stok
  butuh 3 hari pemakaian. Kurang dari itu, aturan terkait dilewati dan laporan menyebutnya
  ("Data baru N hari ..."). < 7 hari: sarankan tetap mengisi log, hasil makin tajam tiap minggu.
- **Hari kosong tidak diisi tebakan;** `libur`/`tutup`/`-`/kosong = tidak ada data. Angka `0`
  = angka sungguhan. Log belum diisi untuk tanggal laporan → `⬜ LOG HARIAN BELUM DIISI`, tidak
  pernah dibilang aman.
- **Angka teks** (`1.250`, `1,2rb`, `Rp 9.000.000`, `9,1jt`, `2,5%`) dibaca otomatis. `1,250`
  (koma + 3 angka) dibaca 1250 dan dilaporkan sebagai ambigu. Sel yang tidak terbaca atau negatif
  diabaikan dan dihitung di `sel_rusak` — sampaikan ke pengguna.
- **Pencilan lama** (mis. hari listrik padam) dibuang sekali dari garis dasar dan disebut di
  laporan; hari khusus sebaiknya dikeluarkan dengan `--abaikan-tanggal`.
- **Musiman** (Ramadan, Lebaran, akhir tahun, tanggal gajian) wajar memicu peringatan; ingatkan
  pengguna bila periodenya bertepatan.
- **Tanpa Python:** jangan mengarang σ atau tren. Hitung manual hanya rata-rata 7 hari, banding
  target, dan sisa hari stok (stok ÷ rata-rata pemakaian) dengan rumus tertulis, lalu beri tahu
  bahwa hasil belum diverifikasi script dan aturan σ/tren tidak dijalankan.
- **Privasi:** semua hitungan lokal; jangan mengirim file ke layanan lain. Pesan siap kirim hanya
  berisi angka. Kolom teks selain catatan/keterangan (mis. `karyawan_absen`) diabaikan & tidak
  pernah dikutip. Kolom catatan hanya ikut bila `--sertakan-catatan` — sebelum memakainya
  (terutama di jadwal otomatis), peringatkan pengguna: "catatan bisa berisi nama karyawan/
  pelanggan dan akan terkirim ke Telegram; pastikan catatan tidak memuat nama." Sarankan kolom
  catatan ditulis tanpa nama orang.

## Riwayat versi
- **1.0.1 (2026-09-29)** — revisi hasil uji independen (6/10): aturan warna diganti model peluang
  (normal/hitungan Poisson/kejadian/konstan) dengan syarat selisih minimal & bertahan (2σ satu
  hari = 🟡; 🟠 = 3σ, atau 2σ di 2 dari 3 hari; 🔴 = 4σ, atau 3σ + kemarin ≥ 2σ); banding hari yang
  sama maks 🟡; metrik biasanya-nol & angka konstan tidak lagi "Normal" saat melonjak; `--kejadian`;
  kolom teks tidak dikutip kecuali `--sertakan-catatan`; stok < 1 hari = "habis besok" + perkiraan
  hari kosong; target 0, duplikat & angka ambigu di laporan teks, saran `--urutan-tanggal mdy`.
  Data stabil sintetis: hari ≥ 🟠 turun dari 31% → ±3%, 🔴 dari 5,9% → ±0,2%.
- **1.0.0 (2026-09-29)** — rilis awal (status uji).
