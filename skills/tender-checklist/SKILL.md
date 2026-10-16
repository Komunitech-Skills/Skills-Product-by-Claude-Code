---
name: tender-checklist
description: Pendamping UMKM ikut pengadaan barang/jasa pemerintah (tender, seleksi, pengadaan langsung di SPSE/LPSE, e-katalog/e-purchasing, toko daring) - cek kelayakan (usaha kecil, NIB & KBLI OSS, NPWP/PKP, SBU/SKK, pengalaman, sisa kemampuan paket), checklist dokumen administrasi/teknis/harga per metode, jadwal mundur dari batas unggah (H-7/H-3/H-1), pemeriksa rincian penawaran vs HPS (volume x harga, PPN, terbilang, peringatan di bawah 80% HPS) dihitung script, dan daftar kesalahan yang menggugurkan. Gunakan saat pengguna menyebut tender, lelang pemerintah, LPSE, SPSE, INAPROC, HPS, pokja, dokumen penawaran, pengadaan langsung, e-katalog, government tender, public procurement bid checklist, atau bid deadline. Bukan untuk SPH ke pembeli swasta (surat-penawaran-harga) atau proposal kemitraan (proposal-kerjasama).
---

# Tender Checklist (Pengadaan Pemerintah untuk UMKM)

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Membantu pemilik usaha kecil yang awam tender untuk: memutuskan **layak ikut atau tidak**, menyiapkan **dokumen lengkap**, **tidak telat unggah**, dan mengirim **harga yang benar hitungannya** — sehingga tidak gugur karena kesalahan yang bisa dicegah.

## Kapan digunakan
- "Saya mau ikut tender pengadaan ATK di LPSE kabupaten, apa saja yang harus disiapkan?"
- "Cek rincian penawaran saya ini, HPS-nya Rp250 juta." (tempel tabel/CSV)
- "Batas unggahnya 15 Oktober jam 14.00, bikinin jadwal persiapan."
- "Usaha saya CV kecil, KBLI 47611, bisa ikut paket ini?"
- "Kenapa penawaran bisa gugur?" / "Harga saya 75% HPS, aman?"
- Diundang pengadaan langsung, atau mau jualan lewat e-katalog/toko daring pemerintah.

## Kapan TIDAK digunakan
- Penawaran harga ke pembeli **swasta** / instansi tanpa proses tender → `surat-penawaran-harga`.
- Proposal kemitraan/sponsorship → `proposal-kerjasama`. Surat resmi umum → `surat-resmi`.
- Menyusun HPS **untuk instansi** (pihak pemerintah) — skill ini untuk penyedia; boleh menjelaskan konsep, tapi arahkan ke pedoman LKPP.
- Sengketa/sanggah banding, gugatan, audit BPK/APIP → sarankan konsultan hukum PBJ.
- Jika skill rujukan tidak terpasang, jelaskan bedanya singkat lalu bantu seperlunya.

**Tolak dengan sopan (etika):** permintaan mengatur pemenang/"arisan tender", penawaran pendamping, pinjam bendera, memalsukan dokumen/pengalaman/tanda tangan, atau memberi "uang terima kasih" ke pokja/PPK. Sebut singkat: persekongkolan tender dilarang **UU 5/1999 Pasal 22**; suap/gratifikasi & pemalsuan dapat dipidana (**UU 31/1999 jo. UU 20/2001**) serta berujung **daftar hitam**. Tawarkan jalur sah (mis. KSO resmi, subkontrak yang diizinkan dokumen, menaikkan kualifikasi).

## Input
| Info | Wajib? | Default jika tidak ada |
|---|---|---|
| Jenis bantuan: kelayakan / checklist / jadwal / cek harga / kesalahan gugur | Ya | Tebak dari kalimat; jika umum ("mau ikut tender") → jalankan alur lengkap 1–5 |
| Metode (tender, seleksi, pengadaan langsung, e-purchasing, tender cepat) & jenis (barang, konstruksi, jasa lainnya, konsultansi, pekerjaan terintegrasi) | Ya | Tender barang/jasa lainnya, pascakualifikasi (sebut sebagai Asumsi; jenis menentukan jaminan penawaran & potongan pajak saat dibayar) |
| Data usaha: bentuk (CV/PT/perorangan/koperasi), kualifikasi di NIB, KBLI, status PKP, SBU (konstruksi), pengalaman, paket berjalan | Untuk kelayakan | Tanyakan; tulis `[cek]` bila belum tahu |
| Rincian harga (uraian, volume, satuan, harga satuan), HPS, pagu | Untuk cek harga | Tanpa HPS → hanya hitung total |
| Harga sudah termasuk PPN? | Tidak | Belum termasuk; PPN hanya jika PKP |
| Tanggal: batas unggah (+jam), penjelasan, pengumuman, hari libur | Untuk jadwal | Hari ini = tanggal sistem; libur nasional tidak otomatis — minta pengguna menyebutkan |

Info kurang → tanyakan **sekali** (maks. 5 pertanyaan bernomor). Ingin cepat → pakai default & tulis "Asumsi".

## Langkah Kerja
Langkah 1–7 adalah urutan **kerja**; jawaban ke pengguna disusun mengikuti urutan di **Format Output**.

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.
1. **Pahami paket.** Minta (atau baca bila ditempel) ringkasan dari dokumen pemilihan: metode, jenis, kualifikasi usaha, KBLI/SBU, HPS, pagu, jadwal, jaminan penawaran, masa berlaku penawaran. Ingatkan: **dokumen pemilihan + adendum adalah acuan utama**.
2. **Cek kelayakan** (tabel A di `references/checklist-dokumen.md`). Beri status per butir: ✅ memenuhi / ❌ tidak / ❓ perlu dicek. Aturan kunci:
   - Paket barang/konstruksi/jasa lainnya **pagu s.d. Rp15 miliar** pada dasarnya untuk usaha mikro, kecil & koperasi (Perpres 16/2018 jo. 46/2025 Pasal 65 ayat (3)), kecuali paket yang menuntut kemampuan teknis yang tidak dapat dipenuhi UMK (Pasal 65 ayat (4)).
   - KBLI di NIB (OSS RBA, PP 28/2025) harus cocok dengan KBLI yang diminta.
   - Konstruksi: SBU subklasifikasi & kualifikasi sesuai, SKK personel, **SKP = 5 − jumlah paket konstruksi yang sedang dikerjakan** (usaha kecil); SKP ≤ 0 → tidak memenuhi.
   - Usaha kecil berdiri < 3 tahun dapat dikecualikan dari syarat pengalaman untuk paket s.d. Rp2,5 miliar (cek LDK).
   - Batas pengadaan langsung: konstruksi s.d. Rp400 jt, barang/jasa lainnya s.d. Rp200 jt, konsultansi s.d. Rp100 jt (Pasal 38 ayat (3), Pasal 41 ayat (3)).
   - Syarat PDN (bila diminta): produk ber-**TKDN paling sedikit 25%** (artinya ≥ 25%; 25% tepat sudah memenuhi) bila ada produk dengan TKDN + BMP paling sedikit 40% (Pasal 66 ayat (2)–(4)).
   - Akses portal (A10): tender lewat LPSE di **spse.inaproc.id**; SPSE 4.5 meminta **kode TOTP** (2FA dari aplikasi autentikator) saat login — sarankan uji login jauh sebelum H-1. Data kualifikasi & riwayat kinerja ada di **SIKaP: sikap.inaproc.id** (alamat baru sejak 15 Des 2025, menggantikan sikap.lkpp.go.id).
   Tutup dengan **keputusan: IKUT / TIDAK / IKUT DENGAN SYARAT** + alasan.
3. **Checklist dokumen — WAJIB selalu ada di jawaban utama**, juga bila pengguna tidak menanyakannya dan **walau batas unggah sudah lewat** (beri judul "untuk adendum perpanjangan/tender berikutnya"). Ambil dari bagian B & C `references/checklist-dokumen.md` sesuai metode & jenis; bila berkas itu tidak terbaca, pakai checklist minimal di bawah. Tampilkan kotak [ ] per kelompok **Administrasi & kualifikasi / Teknis / Harga**. Jangan menambah syarat di luar dokumen pemilihan — tandai "(bila diminta)".
   **Checklist minimal — tender/seleksi pascakualifikasi, barang/jasa lainnya:**
   - Administrasi & kualifikasi: [ ] isian kualifikasi SPSE (NIB + KBLI, akta & pengurus, NPWP/PKP, pengalaman, tenaga, peralatan) sama dengan dokumen asli · [ ] surat penawaran: masa berlaku ≥ yang diminta, bertanggal, ditandatangani direktur/penerima kuasa sah · [ ] pakta integritas · [ ] surat kuasa/akta bila penanda tangan bukan direktur utama · [ ] perjanjian KSO (bila KSO) · [ ] dokumen asli untuk pembuktian kualifikasi · [-] jaminan penawaran: tidak disyaratkan untuk barang/jasa lainnya (isi hanya bila dokumen pemilihan memintanya).
   - Teknis: [ ] spesifikasi/brosur memenuhi atau melebihi yang diminta (merek/tipe jelas) · [ ] jadwal & jangka waktu pengiriman ≤ yang ditetapkan · [ ] surat dukungan pemasok/garansi/layanan purnajual (bila diminta) · [ ] bukti TKDN/PDN (bila disyaratkan; TKDN paling sedikit 25%).
   - Harga: [ ] rincian harga (volume sama dengan dokumen, volume × harga benar, PPN bila PKP) · [ ] total ≤ HPS · [ ] angka = terbilang di surat penawaran · [ ] bukti kewajaran harga (penawaran pemasok/nota) bila < 80% HPS.
   - Konstruksi tambah: SBU & SKK personel, sisa kemampuan paket, metode pelaksanaan, daftar personel & peralatan, RKK (bila diminta), jaminan penawaran bila HPS > Rp10 M. Pengadaan langsung / e-purchasing: bagian B2 / B3.
4. **Jadwal mundur.** Jalankan:
   `python3 scripts/cek_penawaran.py jadwal --batas "2026-10-15 14:00" --penjelasan 2026-10-06 --libur 2026-10-12 --hari-ini <hari ini>` (Windows: `py` atau `python`; tambah `--konstruksi`, `--jaminan`, `--sabtu-kerja` bila relevan).
   **Batas unggah sudah lewat** (tanggal hari ini sesudah batas, atau sama dan jamnya lewat): kalimat **pertama** jawaban = batas sudah lewat (sebut tanggal & jam) + sarankan cek SPSE apakah ada adendum perpanjangan jadwal. Bagian jadwal cukup 1–2 baris ("tahap H-7 s.d. H-1 sudah lewat; kirim tanggal batas baru bila diperpanjang, saya hitung ulang"). **Bagian lain tetap lengkap** — tenggat yang lewat bukan alasan memotong jawaban.
   Tanpa script: hitung mundur **hari kerja** (lewati Sabtu, Minggu, libur yang disebut): H-7 kumpulkan & cek masa berlaku dokumen (+ajukan jaminan penawaran bila konstruksi/terintegrasi & diminta), H-5 dokumen teknis & harga pemasok, H-3 finalisasi harga & tanda tangan, H-2 pemeriksaan silang, H-1 **unggah**, H hanya darurat. Tugas persiapan yang tanggalnya sudah lewat → "TERLEWAT – kerjakan segera"; acara pengumuman/penjelasan yang sudah lewat → "SUDAH LEWAT – baca Berita Acara Penjelasan & adendum" (tidak bisa diulang).
5. **Cek harga penawaran.** Simpan rincian ke CSV (kolom `Uraian;Volume;Satuan;Harga Satuan`, plus kolom **`Jumlah`** bila pengguna punya — lihat `templates/contoh-rincian.csv`) lalu:
   `python3 scripts/cek_penawaran.py harga rincian.csv --ppn nonmewah --hps "Rp 250.000.000" --jenis barang [--pagu ...] [--termasuk-ppn]`
   `--ppn tidak` (default, bukan PKP) | `nonmewah` | `mewah`. `--jenis konstruksi|barang|jasa-lainnya|konsultansi|terintegrasi` (tanpa ini script menyebut asumsi; tanyakan jenis bila HPS > Rp10 M). Angka hitungan tidak dipengaruhi `--jenis`, hanya pesan jaminan. Untuk `--jenis terintegrasi`, isi juga `--pagu`: jaminan penawaran (1–3%) dan jaminan pelaksanaan (ambang 80% & 5%) dihitung dari pagu; tanpa `--pagu` angka dari HPS hanya gambaran. HPS/pagu boleh "185jt", "2,4 M", "Rp2,4 miliar". Salin angka **persis** dari output. Script menerima "Rp1.250.000,00", volume "1,5", sel kosong, baris judul bagian, dan baris total/PPN yang ikut tertempel (label boleh di kolom mana pun; dibandingkan, tidak dihitung ganda).
   - **Kolom Jumlah pengguna** dicek per baris: bagian "Baris salah hitung" menunjuk baris yang volume × harga ≠ jumlah tertulis beserta selisihnya — sampaikan ke pengguna baris demi baris. Script selalu memakai volume × harga satuan.
   - Kolom `Jumlah` (banyaknya) **dan** `Jumlah Harga` sekaligus → Jumlah = volume, Jumlah Harga = jumlah per baris yang dicek.
   - **Baris total di file** dicocokkan sesuai labelnya (Total/"setelah/termasuk PPN" → sesudah PPN; Jumlah/Subtotal/DPP/"sebelum PPN" → sebelum PPN; "DPP Nilai Lain (11/12)" → 11/12 × DPP, toleransi Rp1; PPN → PPN). "Total di file BELUM TERMASUK PPN" = kesalahan gugur/rugi yang umum — tegaskan angka yang benar. Label mirip total yang tidak dikenali (mis. "Harga Total") muncul di Info "TIDAK diperiksa" — sampaikan & minta pengguna memastikan. Saat TOTAL BELUM FINAL, baris total hanya "sama dengan angka SEMENTARA", jangan sebut cocok.
   - Kode keluar: **0** bersih; **1** ada PERINGATAN (sampaikan semuanya); **2** input buruk/GALAT (tanpa hasil); **3** TOTAL BELUM FINAL (ada baris tak terbaca).
   **Rumus eksplisit (bila script tak bisa dijalankan):**
   - Jumlah baris = volume × harga satuan → bulatkan ke rupiah terdekat.
   - Subtotal = Σ jumlah baris = DPP (harga belum termasuk PPN).
   - PPN non-mewah = 12% × (11/12 × DPP) = **11% × DPP**, dihitung persis lalu **dibulatkan ke bawah**; mewah = 12% × DPP (bulat ke bawah). Bukan PKP → PPN 0.
   - Harga sudah termasuk PPN: DPP = rupiah bulat terbesar dengan DPP + PPN ≤ harga (≈ harga ÷ 1,11); tampilkan sisa.
   - Total = DPP + PPN. % HPS = total ÷ HPS × 100 (2 desimal). Batas 80% = 0,8 × HPS.
   - Total > HPS → **gugur**. Total < 80% HPS → **klarifikasi kewajaran harga**; tidak wajar → gugur.
   - **Jaminan — tulis sebagai DUA butir terpisah; jangan digabung dalam satu kalimat:**
     - *Jaminan penawaran* (diserahkan bersama penawaran): **hanya pekerjaan konstruksi & pekerjaan terintegrasi** dengan HPS **paling sedikit di atas Rp10 miliar**, 1–3% HPS (terintegrasi: 1–3% pagu) — Pasal 30 ayat (2) (diubah Perpres 46/2025) & Pasal 31. Barang/jasa lainnya/konsultansi: **tidak disyaratkan** Perpres (tetap ikuti dokumen pemilihan bila memintanya). Ambang Rp200 juta **tidak** berlaku untuk jaminan penawaran.
     - *Jaminan pelaksanaan* (disiapkan bila menang): kontrak barang/konstruksi/jasa lainnya **paling sedikit di atas Rp200 juta**, termasuk e-purchasing (pengecualian e-purchasing sudah dihapus Perpres 46/2025; tidak diperlukan hanya untuk jasa lainnya yang aset penyedia dikuasai pengguna): penawaran 80–100% HPS → **5% nilai kontrak**; < 80% HPS → **5% nilai HPS** (terintegrasi: 80–100% pagu → 5% kontrak; < 80% pagu → 5% pagu, Pasal 33 ayat (4)) — Pasal 33. Kontrak s.d. Rp200 juta umumnya tanpa jaminan pelaksanaan. Masukkan ke rencana kas.
   - Terbilang ditulis penuh + "Rupiah", harus sama dengan angka.
   - **Pengingat pembayaran — WAJIB di bagian harga** (hasil hitung juga mencetaknya di "Saat dibayar"): bendahara instansi **memungut PPN** (bila PKP) dan **memotong PPh Pasal 22 1,5%** dari harga tanpa PPN (pembelian barang) saat membayar → uang yang masuk ke rekening lebih kecil dari total; siapkan arus kas. Nilai penawaran & perbandingan dengan HPS **tetap termasuk PPN**. Jasa: umumnya PPh 23. **Konstruksi:** PPh final (PP 9/2022, tarif tergantung kualifikasi/SBU) — satu kalimat & arahkan ke konsultan pajak; jangan hitung sendiri.
6. **Kesalahan yang menggugurkan.** Tampilkan 5–8 butir paling relevan dari `references/kesalahan-gugur.md` untuk metode/jenis paket pengguna.
7. **Penutup (selalu):** baris Asumsi + baris **Dasar aturan & penafian** persis seperti di Format Output.

## Format Output
Urutan **tetap** di semua kanal. Untuk pertanyaan tentang paket tender yang ingin diikuti, **kelima bagian + penutup wajib ada**; bagian yang datanya belum ada diberi `[cek]` + data yang perlu dikirim, bukan dihapus.
```
1. Tenggat & jadwal   (paket singkat: nama, metode, HPS; bila batas sudah lewat → kalimat PERTAMA jawaban)
2. Kelayakan: IKUT / TIDAK / IKUT DENGAN SYARAT   (✅/❌/❓ per butir + alasan)
3. Cek harga   (rincian per baris, DPP, PPN, total, terbilang, % HPS + batas 80% HPS,
               jaminan penawaran & jaminan pelaksanaan sebagai 2 butir terpisah, pengingat PPN/PPh 22 saat dibayar)
4. Checklist dokumen   ([ ] Administrasi & kualifikasi / Teknis / Harga)
5. Awas gugur   (5–8 butir paling relevan)
Asumsi: ...
Dasar aturan: Perpres 16/2018 sebagaimana diubah Perpres 12/2021 dan Perpres 46/2025; Peraturan LKPP 12/2021 jo. 4/2024 (e-katalog: Peraturan LKPP 2/2026); PMK 131/2024 (PPN) & PMK 59/2022 (pemungutan bendahara) — dicek 26 Sep 2026, portal 15 Okt 2026. Acuan utama: dokumen pemilihan & adendum paket Anda di SPSE. Bukan nasihat hukum/pajak; pembulatan PPN belum dicocokkan dengan Coretax.
```
- Permintaan satu topik untuk paket tertentu (mis. hanya cek harga) → bagian itu penuh, bagian lain boleh 1–3 baris, tetapi **checklist dokumen** (minimal satu baris per kelompok) dan **Dasar aturan** tetap ada. Pertanyaan umum tanpa paket (mis. "apa itu HPS?") → jawab langsung + baris Dasar aturan.
- **Kanal chat (Telegram/WhatsApp):** satu balasan utuh dengan urutan di atas — jangan menunda bagian ke pesan berikutnya, jangan menawarkan "mau saya buatkan checklist?" sebagai pengganti isinya, dan jangan menulis "hasil cek lengkap"/"lihat file" untuk isi yang tidak ditampilkan. Pakai daftar berbutir (bukan tabel), satu baris per butir; rincian per baris harga hanya bila ≤ 6 baris atau ada baris salah hitung; checklist ringkas ±12 butir. Target ≤ 4.000 karakter (batas satu pesan Telegram ±4.096) dengan memadatkan kalimat, **bukan** membuang bagian.
- **Bahasa ke pengguna:** jangan menyebut script/skrip, "hitungan script", nama berkas (.py/.csv/.md), folder/path, perintah, atau opsi (`--ppn`, `--hps`). Tulis angkanya saja ("Total: Rp44.142.480"); berkas pengguna disebut "rincian harga Anda".
- **Cek sebelum kirim:** ☐ tenggat di awal ☐ kelayakan berkeputusan ☐ % HPS & batas 80% ☐ jaminan penawaran & pelaksanaan terpisah ☐ pengingat PPN/PPh 22 ☐ checklist dokumen ada ☐ awas gugur ☐ baris Dasar aturan di akhir ☐ tanpa kata proses/nama berkas.

## Contoh
**Input:** "CV saya usaha kecil, KBLI 47611, bukan PKP. Mau ikut tender ATK HPS Rp45 jt, batas unggah 15/10/2026 jam 14.00. Rincian: kertas 150 rim @52.500, tinta 24 botol @1.250.000, map 500 @3.750."
**Output (ringkas, urutan tetap):**
1. Jadwal: H-7 Selasa 6/10, H-5 Kamis 8/10, H-3 Senin 12/10, H-2 Selasa 13/10, H-1 Rabu 14/10 unggah. Catatan: nilai Rp45 jt di bawah batas pengadaan langsung Rp200 jt — pastikan metodenya memang tender.
2. Kelayakan: IKUT DENGAN SYARAT — ✅ usaha kecil (paket < Rp15 M); ❓ KBLI 47611, cocokkan dengan KBLI di LDK (ATK biasanya 47612/46xx); ✅ NPWP; bukan PKP → **tanpa PPN**.
3. Harga: 7.875.000 + 30.000.000 + 1.875.000 = **Rp39.750.000**; PPN Rp0; total **Rp39.750.000** (Tiga Puluh Sembilan Juta Tujuh Ratus Lima Puluh Ribu Rupiah) = **88,33% HPS** (batas 80% = Rp36.000.000) → aman. Jaminan penawaran: tidak disyaratkan (barang). Jaminan pelaksanaan: kontrak ≤ Rp200 jt, umumnya tidak. Saat dibayar bendahara memotong PPh 22 1,5% → uang masuk < total.
4. Checklist dokumen (Administrasi & kualifikasi / Teknis / Harga). 5. Awas gugur. Lalu Asumsi + Dasar aturan.
Contoh lengkap: `examples/uji-pembuat-01-atk-usaha-kecil.md`.

## Batasan & Penanganan Error
- Aturan PBJ sering berubah; angka di skill dicek **2026-09-25**, pasal Perpres dicocokkan dengan naskah konsolidasi resmi LKPP (https://jdih.lkpp.go.id/regulation/download/konsolidasi-nomor-46-tahun-2025/1) pada **2026-09-26** (`references/dasar-aturan.md`). Butir yang masih bertanda PERLU REVIEW (mis. klarifikasi < 80% HPS & pengecualian pengalaman dari Peraturan LKPP 12/2021, SKP) harus dicocokkan dengan dokumen pemilihan.
- Script tidak mengakses SPSE/OSS/Coretax; tidak memverifikasi keaslian dokumen atau status daftar hitam — hanya mengingatkan cara cek.
- Output script "GALAT: ..." → jelaskan dengan bahasa awam & minta data yang benar. "TOTAL BELUM FINAL" → sebutkan baris bermasalah, jangan sajikan total sebagai final.
- Baris total yang tertempel di CSV tidak ikut dijumlah; bila nilainya tidak cocok → tunjukkan selisihnya (kemungkinan rumus Excel salah).
- PPN khusus (DPP nilai lain/besaran tertentu selain 11/12, fasilitas dibebaskan) di luar cakupan → sarankan konsultan pajak.
- Jangan menjamin menang tender; skill mengurangi risiko gugur administratif, bukan menilai daya saing harga pesaing.
