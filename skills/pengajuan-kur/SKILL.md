---
name: pengajuan-kur
description: Membantu UMKM menyiapkan pengajuan KUR (Kredit Usaha Rakyat) atau kredit usaha bank: cek plafon, bunga, tenor, NPWP & agunan terhadap Permenko 1/2026, checklist dokumen, narasi profil usaha, rencana penggunaan dana yang jumlahnya dicek, simulasi cicilan anuitas vs flat, rasio cicilan terhadap laba bersih dengan peringatan, dan plafon maksimal yang aman. Gunakan saat pengguna mau pinjam modal usaha, ajukan KUR BRI/Mandiri/BNI/BSI, tanya cicilan atau syarat KUR, business loan application, loan installment simulation. Bukan untuk proyeksi kas mingguan atau pinjol.
---

# Persiapan Pengajuan KUR

## Tujuan
Membuat pemilik usaha datang ke bank **siap dan realistis**: dokumen lengkap, cerita usaha yang jelas, rencana dana yang rapi, dan tahu sejak awal apakah cicilannya sanggup dibayar. Skill ini **tidak** menjanjikan kredit disetujui.

## Kapan digunakan
- "Saya mau ajukan KUR 50 juta, apa saja yang perlu disiapkan?"
- "Kalau pinjam 100 juta 3 tahun, cicilannya berapa? Sanggup nggak dengan laba saya?"
- "Buatkan profil usaha / rencana penggunaan dana untuk pengajuan KUR."
- Membandingkan penawaran bunga flat vs efektif/anuitas.

## Kapan TIDAK digunakan
- Proyeksi kas mingguan/kapan kas menipis → `arus-kas-13minggu` (boleh dipakai bersama untuk melihat dampak cicilan).
- Laporan laba rugi/neraca resmi untuk lampiran → `laporan-keuangan-emkm`.
- Pinjaman online/pinjol, gadai, atau "jasa pasti cair" → jangan dibantu; ingatkan risikonya dan arahkan ke lembaga resmi yang terdaftar OJK.
- KUR khusus (klaster dengan mitra usaha) atau KUR penempatan Pekerja Migran Indonesia → jelaskan singkat bahwa skemanya berbeda dan arahkan ke bank penyalur.
- Pertanyaan keputusan kredit spesifik ("apakah saya pasti disetujui?") → jelaskan hanya bank yang memutuskan.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Jumlah pinjaman (plafon) | Ya | — (tanyakan) |
| Tenor (bulan) | Ya | — (tanyakan; contoh umum 24–36 bulan) |
| Suku bunga per tahun dari bank | Tidak | **Bunga acuan Permenko 1/2026** via `--kur --sektor …` (Super Mikro 3%, Mikro/Kecil 6% efektif; perdagangan non-ekspor naik per akad), berlabel "acuan — konfirmasi ke bank penyalur". Sektor tidak diketahui → contoh 6% dengan `--bunga-contoh` |
| Sektor usaha (produksi / perdagangan berorientasi ekspor / perdagangan) & KUR ke berapa | Tidak | Tanyakan bila bunga dari bank belum ada; produksi = selain perdagangan |
| Penggunaan: modal kerja atau investasi | Tidak | Tanyakan (untuk cek batas tenor) |
| Laba bersih usaha per bulan | Ya (untuk rasio) | — (tanyakan; bantu hitung: omzet − semua biaya usaha) |
| Kebutuhan rumah tangga yang diambil dari usaha | Tidak | Tidak dihitung (sebut asumsi) |
| Cicilan lain yang berjalan | Tidak | Rp 0 |
| Profil usaha: nama, bidang, lama usaha, legalitas (NIB/SKU), karyawan, cara jualan, omzet rata-rata | Ya (untuk narasi) | `[isi: …]` pada bagian yang kosong |
| Rencana penggunaan dana (pos + nominal) | Ya (untuk rencana) | — (tanyakan) |
| Bank tujuan | Tidak | Umum (tidak menyebut syarat bank tertentu) |

Jika info wajib kurang, tanyakan **sekali** (maks. 5 pertanyaan bernomor): plafon & tenor; laba bersih per bulan (atau omzet & biaya); cicilan lain; rencana penggunaan dana; profil singkat usaha. Jika pengguna hanya ingin simulasi, cukup plafon, tenor, (bunga), dan laba.

## Langkah kerja
1. **Simulasi & rasio** — jalankan script (path relatif terhadap folder SKILL.md ini; Windows: `python` atau `py`):
   ```bash
   python3 <folder-skill-ini>/scripts/simulasi_kur.py --plafon "Rp 50.000.000" --tenor 36 \
     --kur --sektor produksi --akad-ke 1 --penggunaan modal-kerja \
     --laba-bersih "Rp 7.500.000" --cicilan-lain 0 \
     --rincian-dana "Oven & mixer=18jt; Bahan baku 2 bulan=22jt; Etalase=10jt"
   ```
   - `--kur` mengecek terhadap Permenko 1/2026: jenis KUR dari plafon, bunga acuan, batas tenor, kewajiban NPWP, dan larangan agunan tambahan ≤ Rp100 juta. Hasilnya ada di `cek_ketentuan_kur` (`sesuai` / `perhatian`). Sampaikan setiap `perhatian`.
   - Ada bunga dari bank → tambah `--bunga 6` (tetap boleh dengan `--kur`; bila berbeda dari acuan, script memberi catatan). Tanpa sektor dan tanpa bunga bank → `--bunga 6 --bunga-contoh`.
   - Bunga "per bulan" (mis. `"0,5%/bulan"`) otomatis dikonversi ×12 dengan peringatan. Tanpa `--kur`, script bisa dipakai untuk kredit usaha non-KUR.
   - `--biaya-rumah-tangga` bila uang rumah tangga diambil dari laba usaha (hasil lebih realistis).
   - `--jadwal` untuk tabel angsuran per bulan; `--output-csv jadwal-angsuran.csv` untuk Excel.
   - `--format teks` untuk ringkasan cepat; default JSON.
2. **Jelaskan anuitas vs flat** dengan angka dari output (`perbandingan`, `bunga_efektif_setara_per_tahun_persen`):
   - **Anuitas/efektif:** cicilan tetap, bunga dihitung dari **sisa** pokok → makin lama porsi bunga makin kecil. Bunga KUR ditetapkan sebagai bunga **efektif** per tahun (Permenko 1/2026 Pasal 30, 37, 44).
   - **Flat:** bunga dihitung dari **pokok awal** setiap bulan → pada angka bunga yang sama, total bunga lebih besar. Contoh: flat 6% setara efektif ±11%.
   - Untuk KUR, Permenko menyebut bunga flat harus **setara** dengan bunga efektifnya (`bunga_flat_setara_acuan_persen`; 6% efektif untuk 36 bulan ≈ 3,17% flat). Dalam mode `--kur`, kolom flat pada angka yang sama hanyalah **ilustrasi**; yang berlaku adalah kolom anuitas.
   - Pesan kunci: saat membandingkan penawaran, tanyakan "bunga flat atau efektif?" dan minta tabel angsuran resmi.
3. **Nilai kemampuan bayar** (rasio = total cicilan ÷ laba bersih per bulan; panduan umum skill ini, **bukan** aturan bank):
   - ≤ 30% 🟢 AMAN · > 30–50% 🟡 BERAT, perlu hati-hati · > 50% 🔴 TERLALU BERAT · ≥ 100% ⛔ laba tidak cukup.
   - Jika 🟡/🔴/⛔: **wajib** beri peringatan jelas + alternatif dari output (`plafon_maks_pada_target_rasio`, tenor lebih panjang, bertahap).
4. **Checklist dokumen** — dari `references/checklist-dan-narasi.md` bagian A. Syarat Permenko (KTP-el, NIB/SKU, usaha ≥ 6 bulan, NPWP sesuai plafon, belum pernah menerima kredit komersial produktif) boleh disebut dengan pasalnya. Item lain diberi label **(cek ke bank penyalur)**.
5. **Narasi profil usaha** — template bagian B; hanya fakta dari pengguna, bagian kosong ditulis `[isi: …]`.
6. **Rencana penggunaan dana** — tabel dari `rencana_penggunaan_dana` script; jika status bukan SESUAI, minta pengguna menyesuaikan.
7. **Info ketentuan KUR** — hanya dari `references/regulasi.md` (Permenko 1/2026, dicek per 2026-09-23). Yang TERVERIFIKASI-RESMI boleh disebut beserta pasalnya dan anjuran konfirmasi ke bank. Yang BELUM TERVERIFIKASI (mis. "tanpa biaya provisi") jangan dinyatakan pasti.
8. Periksa checklist, lalu kirim.

**Fallback tanpa Python** (beri tahu pengguna bahwa hasil dihitung manual): r = bunga tahunan ÷ 12 ÷ 100.
Anuitas: cicilan = P × r ÷ (1 − (1 + r)^−n). Flat: cicilan = P ÷ n + P × bunga tahunan ÷ 100 ÷ 12.
Rasio = cicilan ÷ laba bersih × 100%. Plafon maks (anuitas) = cicilan maks × (1 − (1 + r)^−n) ÷ r. Bulatkan ke rupiah penuh.

## Format output
```
## Persiapan Pengajuan KUR — <nama usaha>
⚠️ Suku bunga <x>% = <dari bank / ACUAN Permenko 1/2026 Pasal … — konfirmasi ke bank penyalur / ANGKA CONTOH — cek bank/kur.ekon.go.id>

### 1. Simulasi cicilan (Rp … , … bulan)
| | Anuitas (efektif) | Flat |
|---|---:|---:|
| Cicilan/bulan | Rp … | Rp … |
| Total bunga | Rp … | Rp … |
| Total dibayar | Rp … | Rp … |
Penjelasan singkat bedanya (2–3 kalimat, pakai angka di atas).

### 2. Kemampuan bayar
Laba bersih Rp …/bulan → cicilan …% dari laba → 🟢/🟡/🔴 … Sisa laba Rp ….
(Peringatan + alternatif bila berat: plafon maks aman Rp …, tenor lebih panjang, dll.)

### 3. Rencana penggunaan dana
| Pos | Nominal | % |
### 4. Profil usaha (siap salin)
### 5. Checklist dokumen (syarat Permenko 1/2026 + yang perlu dicek ke bank penyalur)
### 6. Langkah berikutnya
1. Cek SLIK OJK … 2. Datangi/daftar di bank penyalur … 3. Minta tabel angsuran resmi & tanyakan biaya …

Catatan: Simulasi ini bukan penawaran atau jaminan persetujuan kredit. Keputusan & angka final ada di bank.
Dasar: Permenko Perekonomian 1/2026 (dicek per 2026-09-23). Ketentuan dapat berubah — konfirmasi ke bank penyalur.
```

## Contoh
**Input pengguna:** "Saya punya usaha kue rumahan 2 tahun, laba bersih sekitar 7,5 juta sebulan. Mau pinjam KUR 50 juta 3 tahun buat beli oven 18 juta, bahan baku 22 juta, etalase 10 juta. Cicilannya berapa? Aman nggak?"

**Output (ringkas):**
```
⚠️ Bunga 6% efektif/tahun = ACUAN Permenko 1/2026 Pasal 37 (KUR Mikro, sektor produksi) — konfirmasi ke bank penyalur
Anuitas (yang berlaku): Rp 1.521.097/bulan, total bunga Rp 4.759.488
Ilustrasi bila dihitung flat 6%: Rp 1.638.889/bulan, total bunga Rp 9.000.000 (setara efektif ±11,08%, lebih mahal Rp 4.240.512)
→ Untuk KUR ini, bunga flat yang setara hanya ±3,17%/tahun. Jika bank menyebut "flat 6%", minta penjelasan.
Cek Permenko: plafon masuk KUR Mikro ✔ · tenor 36 bulan ≤ batas modal kerja 36 bulan ✔ · tanpa agunan tambahan (≤ Rp100 juta) ✔
Cicilan = 20,3% dari laba bersih → 🟢 AMAN, sisa laba Rp 5.978.903. Plafon maks agar ≤ 30%: Rp 73.959.000.
Rencana dana: Oven Rp 18.000.000 (36%) · Bahan baku Rp 22.000.000 (44%) · Etalase Rp 10.000.000 (20%) = Rp 50.000.000 ✔
+ profil usaha siap salin, checklist dokumen (cek ke bank penyalur), langkah berikutnya.
```

## Checklist sebelum mengirim hasil
- [ ] Sumber suku bunga dilabeli jelas (dari bank / ACUAN Permenko 1/2026 + pasal / ANGKA CONTOH), selalu dengan "konfirmasi ke bank penyalur".
- [ ] Semua `perhatian` dari `cek_ketentuan_kur` disampaikan (plafon di luar rentang, tenor melebihi batas, batas akad, bunga flat).
- [ ] Semua angka cicilan, rasio, total, persen dari script (atau fallback manual yang disebutkan).
- [ ] Beda anuitas vs flat dijelaskan dengan angka.
- [ ] Peringatan tegas bila rasio > 30%; alternatif konkret diberikan.
- [ ] Syarat Permenko disebut dengan pasalnya; dokumen lain bertanda "cek ke bank penyalur"; tidak ada hal BELUM TERVERIFIKASI (mis. bebas provisi) yang ditulis pasti.
- [ ] Narasi tanpa klaim karangan; bagian kosong `[isi: …]`.
- [ ] Tidak ada janji persetujuan, plafon, atau lama proses; disclaimer ada.

## Batasan & penanganan error
- Script keluar dengan kode ≠ 0 dan pesan JSON bila plafon/bunga/tenor tak terbaca, bunga kosong tanpa `--kur --sektor`, plafon > Rp500 juta dengan `--kur` (di atas KUR Kecil), akad ke-3 KUR Mikro perdagangan non-ekspor (tidak tersedia), bunga > 60%/tahun, tenor di luar 1–360 bulan, atau format rincian dana salah — jelaskan dan minta angka yang benar (tenor selalu dalam **bulan**).
- Laba nol/negatif: jangan dorong mengambil pinjaman; sarankan perbaiki pembukuan & laba dulu, atau plafon lebih kecil.
- Rumus anuitas/flat adalah standar; bank dapat memakai metode/pembulatan lain dan menambah biaya (asuransi, notaris, materai) — minta rincian resmi.
- Tidak mengisi formulir bank atau mengirim data ke bank mana pun; data (KTP, NIB) jangan ditempel di chat bila tidak perlu.
- Bukan nasihat keuangan/hukum profesional; untuk restrukturisasi utang atau kredit besar sarankan konsultasi dengan bank/konsultan keuangan.
