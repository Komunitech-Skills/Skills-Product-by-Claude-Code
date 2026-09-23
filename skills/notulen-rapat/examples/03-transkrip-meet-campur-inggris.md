# Contoh 03 – Transkrip Google Meet: label "Speaker", campur Inggris, angka janggal, info gaji

## Skenario
S3, permintaan normal dengan input sulit. Transkrip otomatis Google Meet dari perusahaan logistik kecil di Jakarta. Isinya: label pembicara tanpa nama ("Speaker 1/2"), kalimat campur bahasa Inggris ("let's go with vendor B", "maybe we should revisit pricing", "EOD"), angka yang janggal (sewa gudang "450 juta" padahal bulan lalu 42 juta), dan info sensitif (kenaikan gaji seorang karyawan). Skill harus menjaga keputusan tetap akurat, menandai kejanggalan tanpa mengoreksi diam-diam, dan tidak memasukkan gaji ke pesan grup. Semua nama fiktif.

## Input pengguna
```
Buatkan notulen dari transkrip weekly ops kemarin (Senin 21 Sep 2026) ini ya:

[00:01] Speaker 1: Oke guys kita mulai ya, weekly ops meeting. Halo, kedengeran?
[00:02] Speaker 2: Kedengeran Mas.
[00:03] Speaker 1: Pertama soal vendor last mile. Kita udah compare vendor A sama vendor B. Rafi, gimana hasilnya?
[00:05] Rafi: Vendor A ongkos per paket 9.500, SLA 2 hari. Vendor B 8.700, SLA 2 hari juga, tapi coverage Bekasi belum full.
[00:07] Speaker 1: Oke, let's go with vendor B. Rafi tolong siapin draft kontraknya, lusa ya.
[00:09] Maya: Soal pricing ke klien, maybe we should revisit pricing untuk klien UMKM, margin kita tipis.
[00:10] Speaker 1: Noted, nanti kita bahas lagi minggu depan.
[00:12] Maya: Terus biaya sewa gudang Cakung bulan ini jadi 450 juta, naik dari 42 juta bulan lalu.
[00:13] Speaker 1: Hmm oke, Maya tolong kirim rincian invoice gudangnya EOD.
[00:15] Speaker 2: Satu lagi Mas, soal Dimas, gajinya jadi naik ke 9 juta mulai Oktober sesuai hasil review kemarin ya.
[00:16] Speaker 1: Iya betul.
[00:17] Speaker 2: Sama rekrut 3 kurir tambahan untuk Bekasi, JD-nya saya bikin jumat ini.
[00:18] Speaker 1: Oke. Udah ya, thanks all.
```

## Proses (dijalankan agent)
```
$ python3 scripts/tanggal_relatif.py --rapat "21-09-2026" --ekspresi "lusa" "EOD" "jumat ini" "minggu depan" --format teks
Tanggal rapat: Senin, 21 September 2026
- "lusa" -> Rabu, 23 September 2026 [pasti]
- "EOD" -> (tidak dikenali) [tidak_dikenali] | Ekspresi tidak dikenali; biarkan apa adanya dan tandai ⚠️ di notulen.
- "jumat ini" -> Jumat, 25 September 2026 [pasti]
- "minggu depan" -> Senin, 28 September 2026 [perkiraan] | Tidak menyebut hari; diartikan Senin minggu depan. Mohon dikonfirmasi.
```

## Output

# NOTULEN RAPAT
**Weekly Ops Meeting (disimpulkan)**

| | |
|---|---|
| Hari, tanggal | Senin, 21 September 2026 |
| Waktu | [isi] (durasi transkrip ±18 menit) |
| Tempat/platform | Google Meet |
| Pemimpin rapat | Speaker 1 ⚠️ (nama tidak disebut) |
| Notulis | [isi] |
| Peserta | Speaker 1, Speaker 2, Rafi, Maya (dari transkrip, mohon dicek) (4 orang) |

## Agenda (dikelompokkan dari isi)
1. Pemilihan vendor last mile
2. Harga layanan untuk klien UMKM
3. Biaya sewa gudang Cakung
4. Kenaikan gaji karyawan
5. Rekrutmen kurir tambahan Bekasi

## Pembahasan
### 1. Pemilihan vendor last mile
- Rafi membandingkan dua vendor: Vendor A Rp 9.500/paket, SLA (batas waktu kirim) 2 hari; Vendor B Rp 8.700/paket, SLA 2 hari, tetapi jangkauan Bekasi belum penuh.
- Speaker 1 memutuskan memakai Vendor B.

### 2. Harga layanan untuk klien UMKM
- Maya mengusulkan meninjau ulang harga untuk klien UMKM karena margin tipis ("maybe we should revisit pricing").
- Speaker 1: dibahas lagi minggu depan.

### 3. Biaya sewa gudang Cakung
- Maya menyampaikan biaya sewa gudang Cakung bulan ini **Rp 450.000.000**, naik dari Rp 42.000.000 bulan lalu. ⚠️ Kenaikan lebih dari 10 kali lipat; kemungkinan salah dengar transkrip (di transkrip tertulis: "450 juta"). Mohon dicek.

### 4. Kenaikan gaji karyawan
- Speaker 2 menyampaikan gaji Dimas naik mulai Oktober sesuai hasil review; dikonfirmasi Speaker 1. (Rincian di notulen lengkap saja, lihat 🔒.)

### 5. Rekrutmen kurir tambahan Bekasi
- Akan direkrut 3 kurir tambahan untuk area Bekasi.

## Keputusan
1. Vendor last mile yang dipakai: **Vendor B** (Rp 8.700/paket).
2. Gaji Dimas naik menjadi Rp 9.000.000 mulai Oktober 2026. 🔒
3. Rekrut 3 kurir tambahan untuk area Bekasi.

## Action Items
| No | Tugas | PIC | Tenggat | Status |
|---|---|---|---|---|
| 1 | Mengirim rincian invoice sewa gudang Cakung | Maya | "EOD" ⚠️ (kemungkinan akhir hari rapat, Senin, 21 September 2026) | Belum mulai |
| 2 | Menyiapkan draf kontrak Vendor B | Rafi | Rabu, 23 September 2026 ("lusa") | Belum mulai |
| 3 | Membuat job description (JD) kurir Bekasi | Speaker 2 ⚠️ | Jumat, 25 September 2026 ("jumat ini") | Belum mulai |

## Belum diputuskan / dibahas di rapat berikutnya
- Peninjauan harga untuk klien UMKM (usulan Maya). Dibahas minggu depan.

## Perlu dikonfirmasi
- **Siapa Speaker 1 dan Speaker 2?** Speaker 1 memimpin rapat dan mengambil keputusan (kemungkinan Head of Ops). Speaker 2 memegang urusan gaji dan rekrutmen (kemungkinan HR).
- **Sewa gudang Rp 450.000.000 atau Rp 45.000.000?** Kenaikan dari Rp 42.000.000 tidak wajar. Cek invoice yang akan dikirim Maya.
- **"EOD"** (end of day) diartikan akhir hari rapat, **Senin, 21 September 2026**. Mohon dicek.
- **"Minggu depan"** untuk pembahasan harga diartikan **Senin, 28 September 2026** (atau di rapat mingguan berikutnya).
- Jangkauan Vendor B di Bekasi belum penuh, padahal kurir tambahan juga untuk Bekasi. Apakah Bekasi tetap memakai kurir sendiri? Tidak dibahas.

Rapat berikutnya: belum ditentukan (kemungkinan weekly berikutnya, Senin, 28 September 2026).

> 🔒 **Catatan untukmu:** keputusan kenaikan gaji Dimas adalah **informasi sensitif**. Isinya ada di notulen lengkap ini (batasi penerimanya), tapi **tidak dimasukkan ke pesan grup WA**.

---
## Pesan untuk grup WhatsApp
```
*Ringkasan Weekly Ops — Senin, 21 Sep 2026*
✅ Keputusan:
1. Vendor last mile: *Vendor B* (Rp 8.700/paket)
2. Rekrut 3 kurir tambahan untuk Bekasi
📌 Tugas:
• @Maya: rincian invoice sewa gudang Cakung, *hari ini (EOD)*
• @Rafi: draf kontrak Vendor B, *Rabu, 23 Sep*
• @[Speaker 2]: JD kurir Bekasi, *Jumat, 25 Sep*
❓ Dibahas lagi minggu depan: peninjauan harga klien UMKM.
Notulen lengkap menyusul. Thanks all 🙏
```

## Catatan penguji
- **Script dijalankan sungguhan.** "EOD" berstatus `tidak_dikenali`, jadi ditulis apa adanya + ⚠️ sesuai langkah 5. Tafsiran agent diberi tanda dan masuk "Perlu dikonfirmasi". **Verifikasi independen:** 21/9 = Senin, 23/9 = Rabu, 25/9 = Jumat, 28/9 = Senin.
- **Bagus:** "let's go with vendor B" dari pemimpin rapat menjadi keputusan. "Maybe we should revisit pricing" menjadi usulan yang ditunda. Ini persis contoh kasus 2 di `references/aturan-klasifikasi.md`. Label "Speaker" dipakai apa adanya dan ditanyakan. "SLA" dijelaskan.
- **Bagus:** angka janggal (450 juta vs 42 juta) **tidak dikoreksi diam-diam**, sesuai *Batasan*. Info gaji ada di notulen lengkap tapi tidak di pesan WA, dan pengguna diberi tahu.
- **Kurang (ringan):** script tidak mengenali istilah Inggris yang umum di rapat kantor ("EOD", "next week", "end of month", "tomorrow"). Padahal README/SKILL.md menjanjikan dukungan rapat campuran bahasa Inggris. Agent tetap menanganinya dengan benar lewat jalur `tidak_dikenali` + ⚠️. Saran: tambahkan alias Inggris dasar di `tafsir()`.
- **Catatan:** "Pemimpin rapat: Speaker 1 ⚠️" dan "(kemungkinan Head of Ops)" adalah dugaan yang diberi tanda di "Perlu dikonfirmasi". Tidak ada nama yang dikarang.
