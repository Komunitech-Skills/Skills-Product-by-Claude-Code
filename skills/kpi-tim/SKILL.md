---
name: kpi-tim
description: KPI & target tim untuk UMKM (data di Excel/Google Sheets, kertas, grup WA) - pilih KPI dari katalog per peran (sales, CS, produksi, gudang, keuangan, marketing, admin, kurir, kasir), buat rencana KPI (bobot 100%, target, ambang) sebagai CSV/XLSX, ubah laporan grup WA ("Andi closing 12 deal") jadi draf realisasi, hitung capaian & skor tertimbang per orang/divisi/perusahaan dengan script (arah naik/turun, batas 120%, status hijau/kuning/merah, tren, data kosong), OKR ringan, draf laporan Telegram & catatan 1:1, jadwal OpenClaw. Gunakan saat pengguna minta "buat KPI karyawan", "target sales per orang", "hitung pencapaian KPI", "penilaian kinerja tim", "OKR", KPI scorecard, team targets, performance dashboard, weighted KPI score. Bukan untuk hitung gaji/bonus, PHK/sanksi, atau memantau karyawan diam-diam.
---

# KPI Tim

## Tujuan
Membantu pemilik usaha/manajer yang awam teknologi punya **target yang jelas per orang & divisi**
dan **skor pencapaian yang dihitung benar** tiap minggu/bulan, dari data yang sudah mereka
punya (Excel, Google Sheets, catatan grup WA), tanpa aplikasi berlangganan. Semua angka dihitung
`scripts/skor_kpi.py` (Python standar, data lokal), bukan dikira.

## Kapan digunakan
- "KPI apa yang cocok untuk admin gudang saya?" / "Buatkan KPI untuk 8 karyawan saya."
- "Buat template target sales per orang di Excel/Google Sheets."
- "Ini rekap grup WA akhir bulan, hitung pencapaian KPI tim."
- "Hitung skor KPI September dari file ini, bandingkan dengan Agustus."
- "Siapkan bahan 1:1 untuk Joko." / "Buat OKR kuartal ini untuk divisi sales."
- "Kirim laporan KPI ke Telegram saya tiap tanggal 2."

## Kapan TIDAK digunakan
- Hitung gaji, lembur, THR, bonus → `gaji-umkm`, `slip-gaji-bpjs`, `hitung-thr` (skill ini hanya
  memberi skor; aturan bonus ditetapkan pemilik).
- Surat peringatan / PHK / sengketa → `surat-peringatan-karyawan` atau profesional hukum. Skill ini
  **tidak** merekomendasikan pemecatan dan tidak dipakai sebagai dasar sanksi otomatis.
- Absensi & jam kerja → `absensi-lokal`. Tugas harian → `vikunja-tugas`.
- Melacak lokasi, membaca chat pribadi, merekam layar karyawan → **tolak** (KPI ≠ pengawasan,
  lihat `references/privasi-etika.md`).
- Sistem multi-pengguna (karyawan mengisi sendiri, atasan menyetujui, 20+ orang) → jelaskan
  batas skill ini; itu butuh server (mis. Frappe HRMS/Leantime, jasa setup Komunitech).

## Input
Tanyakan **sekali**, dalam satu pesan bernomor; lewati yang sudah disebut pengguna.

| # | Pertanyaan | Default bila tidak dijawab |
|---|---|---|
| 1 | Daftar orang: nama panggilan, divisi, peran (sales/CS/gudang/...) | Wajib; tanpa ini tidak bisa |
| 2 | Periode penilaian: bulanan atau mingguan? | Bulanan (`2026-10`) |
| 3 | Sudah punya target/angka 3 bulan terakhir? | Pakai target contoh katalog, **ditandai "perlu disesuaikan"** |
| 4 | Data realisasi dari mana? (Excel/Sheets, rekap grup WA, skill Komunitech lain) | Lembar realisasi CSV dari template |
| 5 | Laporan untuk siapa? | Pemilik saja (bukan grup) |

Ingin cepat → pakai default, sebut asumsinya.

## Langkah kerja
Semua perintah: `python3 scripts/skor_kpi.py <perintah>` dari folder skill ini (Windows:
`python` atau `py`). Tambah `--json` untuk dibaca agent. Rincian: `references/aturan-skor.md`.

### 1. Pilih KPI (G5)
- `skor_kpi.py katalog [--peran gudang]` → set bawaan 4 KPI/peran + bobot usulan.
- Baca `references/katalog-kpi.md` untuk alternatif, rumus, sumber data (skill Komunitech mana
  yang menghasilkan angkanya), dan §11 prinsip KPI yang adil. Sampaikan singkat ke pengguna:
  3–5 KPI per orang, bisa dikendalikan orangnya, seimbang jumlah & mutu.

### 2. Buat rencana KPI (G1)
1. Tulis daftar tim ke CSV (`nama,divisi,peran`, contoh `templates/tim-contoh.csv`).
2. `skor_kpi.py template --tim tim.csv --periode 2026-10 --keluar KPI/` → `rencana-kpi.csv`,
   `rencana-kpi.xlsx` (lembar "Petunjuk" ikut), dan `realisasi-2026-10.csv` kosong.
3. Sesuaikan target dengan data pengguna (target katalog hanya contoh). Kolom: `periode`
   (kosong = semua periode), `divisi`, `orang` (kosong = KPI divisi), `kpi`, `satuan`, `arah`
   (`naik`/`turun`), `bobot` (total 100 per orang), `target`, `ambang` (opsional: batas minimal
   untuk naik / maksimal untuk turun), `maks_capai` (opsional, default 120), `kata_kunci`
   (untuk membaca teks WA), `sumber`.
4. `skor_kpi.py cek --rencana KPI/rencana-kpi.csv` → wajib ✅ sebelum lanjut. Error (bobot ≠ 100,
   target 0 arah naik, target negatif, arah tak dikenal, ambang terbalik, satu orang dua divisi)
   disampaikan apa adanya + cara memperbaikinya.
5. Google Sheets: pengguna **Impor** file `.xlsx`/`.csv`, lalu **Download** `.xlsx`/`.csv` untuk
   dihitung. Agent tidak membuka Sheet lewat akun/API.

### 3. Kumpulkan realisasi (G4, G6)
Pilih sesuai sumber data:
- **Excel/Sheets/CSV**: kolom `periode, divisi, orang, kpi, realisasi, catatan` (satu file
  untuk semua periode supaya tren terbaca). Angka boleh `1.250.000`, `Rp 162.000.000`, `4,6`,
  `85%`, atau `14/50` (dibaca 28%).
- **Teks grup WA / ketikan**: `skor_kpi.py baca-teks --rencana ... --teks rekap.txt --periode
  2026-09 --keluar draf.csv` (atau `--teks -` dari stdin). Hasilnya **DRAF** (`status_draf =
  PERLU KONFIRMASI`) + daftar "tidak terbaca". Tunjukkan tabel draf ke pengguna, minta
  konfirmasi/koreksi, baru ubah `status_draf` menjadi `dikonfirmasi` dan gabungkan ke file
  realisasi. Baris draf yang belum dikonfirmasi **selalu dilewati** saat menghitung skor.
  Untuk ekspor chat grup yang panjang, ringkas dulu dengan `ringkas-grup-wa` bila terpasang.
- **Log harian** (komplain, respons CS, pengiriman, produksi): catat di format
  `templates/log-operasional-contoh.csv` (`tanggal, divisi, orang, kpi, nilai, cara` dengan
  cara `jumlah`/`rata-rata`/`persen` ya-tidak), lalu `skor_kpi.py rekap-log --log log.csv
  --periode 2026-09 --keluar realisasi-log.csv`.
- **Skill Komunitech lain** (`kasir-lokal`, `crm-wa`, `absensi-lokal`, `buku-stok`,
  `buku-piutang`, `kas-umkm`, `laporan-iklan-mingguan`, `rekap-penjualan-csv`): jalankan
  rekapnya, **salin angka apa adanya** ke file realisasi, catat sumbernya di kolom `catatan`.

### 4. Hitung skor (G1)
```bash
python3 scripts/skor_kpi.py skor --rencana KPI/rencana-kpi.csv --realisasi KPI/realisasi.csv \
  --periode 2026-09 [--data-kosong tandai|bobot-ulang|nol] [--cap 120] [--bobot-divisi "Sales=50,..."]
```
- Arah `naik`: realisasi ÷ target × 100. Arah `turun`: (2 − realisasi ÷ target) × 100; target
  0 = aturan "nol kejadian" (100% jika 0, selain itu 0%). Capaian dibatasi 0–120%.
- Skor orang = Σ(bobot × capaian) ÷ 100. 🟢 ≥ 100, 🟡 ≥ 80, 🔴 < 80 (ubah dengan `--hijau`,
  `--kuning`). Status KPI memakai `ambang` bila diisi.
- **Data kosong** (default `tandai`): orang dengan KPI tanpa data = ⚪ belum lengkap, tidak ikut
  rata-rata divisi. `bobot-ulang` = hitung dari KPI yang ada bila bobotnya ≥ 50%. `nol` = kosong
  dihitung 0% (hanya bila disepakati). **Selalu sebutkan mode yang dipakai** ke pengguna.
- Divisi = rata-rata orang lengkap (atau KPI divisi bila ada). Perusahaan = rata-rata divisi.
- Tren otomatis vs periode sebelumnya di file (`--periode-lalu` untuk memilih).
- Error/peringatan (realisasi ganda, nama KPI salah ketik + saran, realisasi negatif, periode
  tanpa data) disampaikan apa adanya. **Jangan** mengarang angka yang hilang.
- `--csv-keluar hasil.csv` menyimpan rincian untuk Excel/Sheets/`dasbor-lokal`.

### 5. Susun laporan (G8)
- **Ringkasan pemilik** (default teks, siap Telegram): perusahaan → divisi → orang (urut divisi &
  nama, **bukan peringkat**), KPI paling perlu perhatian per orang, peringatan. Kirim apa adanya.
- **Grup/papan kantor**: `--tanpa-nama` (hanya perusahaan & divisi), setelah pemilik setuju.
- **Bahan 1:1**: `skor --orang "Joko Susilo"` → rincian per KPI (realisasi, target, capaian,
  bobot, nilai, tren). Isi `templates/catatan-1on1.md`: angka disalin dari script, apresiasi
  dulu, pertanyaan terbuka, kemungkinan penyebab sebagai **hipotesis**, kolom kesepakatan kosong.
  Jangan menilai sifat pribadi ("malas"); tulis perilaku & angka.

### 6. OKR ringan (G2)
`templates/okr-contoh.csv` (`periode, pemilik, objective, key_result, awal, target, sekarang,
progres`). 1 objective = 2–4 key result terukur. `skor_kpi.py okr --okr okr.csv --periode
2026-Q4 [--jalan 0,5]`. Progres KR = (sekarang − awal) ÷ (target − awal), dibatasi 0–1,0.
Check-in mingguan: perbarui kolom `sekarang`, jalankan dengan `--jalan` = bagian waktu yang lewat.
OKR untuk arah & fokus, tidak masuk skor KPI dan tidak untuk gaji.

### 7. Jadwal otomatis (OpenClaw, opsional)
Ikuti `references/jadwal-openclaw.md` (pola terverifikasi dari `laporan-otomatis-terjadwal`):
tunjukkan contoh laporan dulu → penerima hanya pemilik/manajer via Telegram → minta izin →
`openclaw automations add "0 7 2 * *" "<pesan>" --name ... --tz "Asia/Jakarta" --session isolated
--announce --channel telegram --to "<chat-id>"` → catat `id` → `automations run <id> --wait` →
jelaskan cara jeda/hapus + syarat komputer menyala.

## Format output
- Laporan teks: judul `📊 *Laporan KPI Tim — <periode>*`, baris perusahaan, bagian *Divisi*,
  bagian *Per orang*, ⚠️ peringatan (maks 5), satu baris keterangan aturan. Angka gaya Indonesia
  (`93,6`, `Rp 162.000.000`), tren `▲6,3`/`▼4,2`.
- Setelah laporan, tambahkan maksimal 3 saran tindak lanjut **berbasis angka** (mis. "Joko:
  salah kirim 6 dari target 3; cek bersama di 1:1"), tanpa label negatif tentang orang.
- Contoh lengkap: `examples/contoh-distributor.md`.

## Contoh
**Input:** "Ini rekap grup WA akhir September. Hitung KPI tim saya ya." (+ teks WA)

**Alur:** `baca-teks` → tampilkan draf 9 baris + 0 tidak terbaca → pengguna konfirmasi →
gabung ke `realisasi.csv` → `skor --periode 2026-09` → kirim ringkasan:
```
📊 *Laporan KPI Tim — 2026-09*
Perusahaan: 🟡 93,6 (▲6,3 vs 2026-08) — sebagian
*Divisi*
🟡 Gudang & Pengiriman: 91,7 ▼4,2
🟡 Keuangan & Admin: 93,1 ▲17,6 (tanpa Tono Wijaya)
🟡 Sales: 96,1 ▲5,6
...
```

## Batasan & penanganan error
- **Angka hanya dari script.** Python tidak bisa dijalankan → hitung manual dengan rumus di
  `references/aturan-skor.md` langkah demi langkah, tampilkan rumusnya, dan tulis "belum
  diverifikasi script".
- **Tidak ada realisasi untuk periode itu** → script berhenti; sampaikan, jangan kirim angka nol.
- **File `.xls` lama** → minta simpan ulang sebagai `.xlsx`/CSV. **Google Sheets** → unduh
  `.xlsx`/`.csv`; agent tidak masuk ke akun Google.
- **Teks WA** → selalu draf yang dikonfirmasi; "tidak terbaca" ditanyakan, bukan ditebak.
- **Target dari katalog** hanya contoh; ingatkan untuk disesuaikan dengan data sendiri.
- **Privasi**: skor per orang = data pribadi karyawan. Simpan lokal, kirim ke pemilik/manajer
  saja, jangan buat peringkat publik (lihat `references/privasi-etika.md`).
- **Bukan dasar keputusan otomatis**: skor adalah bahan diskusi. Permintaan "siapa yang harus
  dipecat berdasarkan KPI" → tolak memberi keputusan; tawarkan bahan 1:1, rencana perbaikan,
  dan rujuk ke peraturan perusahaan/`surat-peringatan-karyawan`/profesional.
- **XLSX** ditulis dengan Python standar (tanpa rumus/warna bersyarat). Bila Excel menolak
  membuka, pakai `rencana-kpi.csv` (isinya sama).
