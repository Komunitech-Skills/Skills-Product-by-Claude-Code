# Aturan hitung skor KPI (dipakai `scripts/skor_kpi.py`)

Semua angka dihitung dengan `Decimal` (tidak ada galat pecahan biner) dan **dibulatkan sekali**
saat ditampilkan: capaian & skor 1 desimal, cara *half-up* (0,05 → 0,1). Perhitungan antara
memakai angka penuh, jadi skor = jumlah kontribusi yang belum dibulatkan.

## 1. Capaian per KPI

| Arah | Rumus capaian | Contoh |
|---|---|---|
| `naik` (makin tinggi makin baik) | realisasi ÷ target × 100 | omzet 162 jt, target 150 jt → 108% |
| `turun` (makin rendah makin baik), target > 0 | (2 − realisasi ÷ target) × 100 | respons 8 menit, target 10 → 120%; 15 menit → 50% |
| `turun`, target = 0 ("nol kejadian") | 100 jika realisasi 0, selain itu 0 | kecelakaan 0 → 100%; 1 → 0% |

- Rumus `turun` dipilih karena tetap bisa dihitung saat realisasi 0 (target ÷ realisasi akan
  membagi dengan nol) dan turun lurus: tiap kelebihan 10% dari target mengurangi 10 poin.
- **Batas bawah 0%.** Realisasi yang sangat buruk tidak membuat skor minus.
- **Batas atas `maks_capai`** (default **120%**, ubah per KPI di kolom `maks_capai` atau global
  `--cap`). Tujuannya: satu KPI yang sangat tinggi tidak menutupi KPI lain yang gagal.
  Capaian asli tetap ditampilkan, ditandai "(dibatasi 120%)".
- Target `naik` = 0 **ditolak** (tidak bisa dibagi). Target negatif ditolak.
- Realisasi berbentuk `a/b` (mis. `14/50`) dibaca sebagai persen: 14 ÷ 50 × 100 = 28.

## 2. Status per KPI 🟢🟡🔴

1. 🟢 **hijau**: capaian asli ≥ 100% (target tercapai).
2. Bila kolom `ambang` diisi (dalam satuan KPI):
   - arah `naik`: 🟡 bila realisasi ≥ ambang (batas minimal), selain itu 🔴.
   - arah `turun`: 🟡 bila realisasi ≤ ambang (batas maksimal), selain itu 🔴.
3. Bila `ambang` kosong: 🟡 bila capaian ≥ `--kuning` (default 80%), selain itu 🔴.

Ambang hanya menentukan warna, **tidak** mengubah angka skor. Contoh: akurasi stok 96%, target
99%, ambang 97% → capaian 97,0% tetapi 🔴 karena di bawah batas minimal yang disepakati.

## 3. Skor orang

skor = Σ(bobot × capaian dipakai) ÷ Σ bobot. Bobot per orang **wajib tepat 100** (bila ditulis
pecahan 0,4 + 0,6 = 1, otomatis dibaca 40 + 60 dengan catatan). Status skor: 🟢 ≥ `--hijau`
(default 100), 🟡 ≥ `--kuning` (default 80), 🔴 di bawahnya.

Skor 100 berarti "rata-rata tertimbang target tercapai". Karena ada batas 120%, skor maksimum
teoritis = 120.

## 4. Data yang belum ada (aturan eksplisit, pilih dengan `--data-kosong`)

| Mode | Perilaku | Kapan dipakai |
|---|---|---|
| `tandai` (**default**) | Orang dengan KPI tanpa data → ⚪ **belum lengkap**, skor tidak dihitung, **tidak ikut** rata-rata divisi. Skor sementara (dari KPI yang ada) ditampilkan terpisah hanya di JSON/rincian. | Laporan rutin: memaksa data dilengkapi dulu, tidak ada yang dirugikan karena data telat. |
| `bobot-ulang` | Skor = Σ(bobot × capaian) ÷ Σ bobot yang **ada datanya**, asalkan bobot berdata ≥ `--min-bobot` (default 50%). Di bawah itu tetap ⚪. Laporan menulis "(dihitung dari 85% bobot)". | Data satu KPI memang tidak tersedia periode ini (mis. opname belum dilakukan). |
| `nol` | KPI tanpa data dihitung 0%. | Hanya bila sudah disepakati "tidak lapor = tidak tercapai". Keras; jangan dipakai diam-diam. |

Laporan selalu menyebut siapa yang belum lengkap dan KPI apa yang kosong. Jika **tidak ada satu
pun** realisasi untuk periode itu, script berhenti dengan error: tidak pernah mengirim laporan
berisi angka nol.

## 5. Skor divisi & perusahaan

- Divisi **tanpa** KPI divisi: rata-rata skor orang yang lengkap (bobot sama per orang).
  Bila ada anggota ⚪, divisi ditandai "(tanpa Nama)".
- Divisi **dengan** KPI divisi (baris rencana dengan kolom `orang` kosong): skor divisi = skor
  KPI divisi. Rata-rata individu tetap ditampilkan (`rata_individu`).
- Perusahaan: rata-rata skor divisi (bobot sama), atau `--bobot-divisi "Sales=50,Gudang=30,
  Keuangan=20"` (wajib total 100, semua divisi harus disebut). Ditandai "sebagian" bila ada
  divisi/orang yang belum lengkap.

## 6. Tren

Periode pembanding = periode sebelumnya yang ada di file realisasi dengan pola sama (`2026-08`
untuk `2026-09`, `2026-W39` untuk `2026-W40`, `2026-Q3` untuk `2026-Q4`), atau `--periode-lalu`.
Tren = skor sekarang − skor lalu, dalam poin (▲ naik, ▼ turun). Tidak ada tren bila salah satu
skor belum lengkap. Periode lalu dihitung dengan rencana yang berlaku di periode itu.
Tren tidak pernah hilang diam-diam: ⚠️ bila file tidak berisi periode sebelumnya, bila periode
tepat sebelumnya (mis. 2026-10 untuk 2026-11) tidak ada sehingga dipakai periode lebih lama, bila
rencana tidak berlaku di periode lalu, dan bila jumlah orang yang dinilai di sebuah divisi
berbeda antara dua periode. Di rincian 1:1, perubahan per KPI ditulis "(capaian ▼4,2 poin vs
2026-08)" = selisih capaian, bukan selisih nilai.

## 7. Rencana per periode (masa berlaku)

Kolom `periode` di rencana:

| Isi | Arti | Prioritas |
|---|---|---|
| kosong | berlaku semua periode | 1 |
| `2026-10..` | berlaku mulai 2026-10 dan seterusnya (diisi otomatis oleh `template --periode 2026-10`) | 2 |
| `2026-10..2026-12` atau `2026-10 s/d 2026-12` | rentang tertutup | 2 |
| `2026-11` | hanya periode itu | 3 |

Per orang/divisi dipakai **satu kelompok baris** dengan prioritas tertinggi yang berlaku (tidak
dicampur), supaya bobot tetap 100. Dua rentang berbeda yang sama-sama berlaku → error "tumpang
tindih". Format periode harus sama polanya dengan periode realisasi (`2026-10`, `2026-W40`,
`2026-Q4`).

## 8. Realisasi ganda

Dua baris realisasi untuk orang + KPI + periode yang sama → error (default `--duplikat tolak`).
`--duplikat jumlah` menjumlahkan (tidak boleh untuk KPI bersatuan %); `--duplikat terakhir`
memakai baris paling bawah. Kolom `status_draf` (hasil `baca-teks`): hanya baris **kosong**
atau `dikonfirmasi` (juga `ok`/`benar`) yang dihitung; `PERLU KONFIRMASI`, `ditolak`, dan isi
lain dilewati dengan ⚠️.

## 9. Realisasi negatif & angka tidak wajar

Dilewati dengan peringatan (kemungkinan salah ketik). Bila memang bisa minus (mis. laba),
jalankan dengan `--izinkan-minus`; capaian tetap dibatasi minimal 0%. Tanda minus dikenali di
semua bentuk: `-5.000.000`, `Rp -5.000.000`, `-Rp5jt`, `(5.000.000)`, `(Rp 5.000)`. Sufiks
`jt`/`juta`, `rb`/`ribu`, `miliar` dikalikan. Capaian mentah di bawah 0 ditampilkan "0,0% (batas
bawah; realisasi jauh dari target)", tidak pernah persen minus. Capaian arah naik < 1% atau
> 1000% memberi ⚠️ "tidak wajar" (sering karena `1,250` dibaca 1,25).

## 10. OKR ringan (`okr`)

- Progres key result = kolom `progres` (0–1,0 atau 0–100%), atau (sekarang − awal) ÷ (target −
  awal), dibatasi 0–1,0. Rumus ini juga benar untuk KR yang menurun (awal 8 → target 2).
- Progres objective = rata-rata KR (bobot sama). Saran 2–4 KR per objective (di luar itu hanya
  diberi catatan).
- Status akhir periode: 🟢 ≥ 0,7, 🟡 ≥ 0,4, 🔴 < 0,4 (0,7 dianggap berhasil untuk target
  menantang). Di tengah periode pakai `--jalan 0,5` (separuh waktu lewat): 🟢 bila progres ≥
  waktu berjalan, 🟡 bila ≥ 70% dari itu, 🔴 di bawahnya.
- OKR **tidak** dihitung ke skor KPI dan tidak dipakai untuk bonus/gaji.

## 11. Rekap log (`rekap-log`)

Log harian (`tanggal, divisi, orang, kpi, nilai, cara`) direkap per bulan (`--per bulan`,
`2026-09`) atau minggu ISO (`--per minggu`, `2026-W37`, Senin–Minggu):
`jumlah` = total nilai (kosong = 1), `rata-rata` = rata-rata nilai, `persen` = jumlah "ya" ÷
jumlah baris × 100. Hasil dibulatkan 2 desimal dan siap dipakai sebagai file realisasi.
