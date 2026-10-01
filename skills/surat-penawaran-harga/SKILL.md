---
name: surat-penawaran-harga
description: Membuat Surat Penawaran Harga (SPH / quotation) profesional untuk usaha Indonesia lengkap dengan nomor surat, tabel rincian item, diskon, ongkir, PPN (hanya jika penjual PKP; non-mewah 12% x DPP 11/12), total, terbilang, masa berlaku, serta syarat bayar & kirim, plus versi singkat untuk WhatsApp. Angka dihitung script. Gunakan saat pengguna minta surat penawaran, penawaran harga, SPH, quotation, price quote, atau rincian harga untuk calon pembeli. Bukan untuk tagihan setelah transaksi (pakai buat-invoice) atau proposal kerja sama (pakai proposal-kerjasama).
---

# Surat Penawaran Harga (SPH)

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Menghasilkan SPH yang rapi, benar hitungannya, dan siap dikirim (dokumen + teks WhatsApp) dari informasi seadanya, sehingga pemilik usaha terlihat profesional di mata calon pembeli (kantor, instansi, EO, kontraktor, reseller).

## Kapan digunakan
- "Buatin surat penawaran harga untuk PT X, 20 kursi + 10 meja."
- Calon pembeli minta "quotation", "penawaran resmi", "rincian harga + PPN".
- Revisi SPH: ubah diskon, tambah item, perpanjang masa berlaku.

## Kapan TIDAK digunakan
- Tagihan setelah barang dikirim/jasa selesai → skill `buat-invoice`.
- Menawarkan kemitraan/sponsorship/konsinyasi (bukan jual-beli item) → `proposal-kerjasama`.
- Hitung PPN saja tanpa surat → `hitung-ppn`. Menentukan harga jual dari modal → `hitung-hpp` / `harga-jual-marketplace`.
- Jika skill rujukan di atas tidak terpasang, jelaskan singkat bedanya dan tawarkan draf sederhana tanpa mengubah SPH menjadi invoice/faktur.
- Mengikuti tender/LPSE pemerintah dengan format baku dokumen pengadaan: skill ini boleh dipakai untuk draf rincian harga, tapi ingatkan pengguna mengikuti format & ketentuan dokumen tender.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Nama usaha penjual + kontak (alamat, WA, email) | Ya | — (tanyakan; boleh ditulis `[isi alamat]`) |
| Nama calon pembeli (perusahaan/instansi + PIC) | Ya | — (tanyakan) |
| Daftar item: nama, jumlah, satuan, harga satuan | Ya | — (tanyakan) |
| Penjual PKP (memungut PPN) atau tidak? | Ya | Anggap **bukan PKP** (tanpa PPN) dan sebutkan asumsi |
| Harga sudah termasuk PPN atau belum | Tidak | Belum termasuk PPN |
| Diskon per item / diskon total | Tidak | Tanpa diskon |
| Ongkos kirim / biaya pasang | Tidak | Tidak ada; tulis "belum termasuk ongkir" di syarat |
| Masa berlaku penawaran | Tidak | 14 hari sejak tanggal surat |
| Syarat pembayaran | Tidak | DP 50% saat PO, pelunasan sebelum barang dikirim |
| Waktu & cara pengiriman | Tidak | 3–7 hari kerja setelah DP diterima; `[isi]` jika tidak tahu |
| Nomor urut & kode surat | Tidak | Nomor urut 001, kode `SPH/<singkatan usaha>` |
| Nama & jabatan penanda tangan | Tidak | `[Nama]`, `[Jabatan]` |
| Rekening bank | Tidak | Tulis `[Bank – No. Rek – a.n.]` |

Jika info wajib kurang, tanyakan **sekali** (maks. 5 pertanyaan bernomor). Jika pengguna ingin cepat, pakai default dan tulis "Asumsi yang dipakai" di akhir.

## Langkah kerja
1. **Kumpulkan & rapikan data item.** Samakan satuan (unit, pcs, box, m², paket, hari). Harga "1,5jt", "750rb", "Rp 72.500" semuanya boleh.
2. **Tentukan mode PPN** (lihat `references/regulasi.md`):
   - Penjual **bukan PKP** → `--ppn tidak` (default). Jangan menagih PPN; jangan menulis "sudah termasuk PPN".
   - PKP, barang/jasa biasa → `--ppn pkp` (12% × DPP nilai lain 11/12 = efektif 11%).
   - PKP, barang mewah kena PPnBM → `--ppn mewah` (12% × harga penuh; PPnBM tidak dihitung skill ini, sarankan konsultan pajak).
   - Ragu apakah PKP → tanyakan. Jika tetap tidak tahu, pakai `tidak` dan beri catatan.
   - **Ongkir/biaya pasang yang ditagih penjual ikut DPP dan dikenai PPN** (jika PKP). Selalu sebutkan ini di blok "Asumsi". Jika ongkir hanya titipan/penggantian biaya kurir yang ditagih terpisah (mis. pembeli membayar kurir langsung, atau reimburse sesuai resi), **jangan pakai `--ongkir`**; tulis di syarat pengiriman "Ongkos kirim ditanggung pembeli sesuai tarif ekspedisi".
3. **Hitung dengan script.** Script ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill); jangan mencarinya ke seluruh disk (`find /`). Windows: `python` atau `py`.
   ```bash
   python3 <folder-skill-ini>/scripts/hitung_sph.py \
     --item "Kursi kantor ergonomis|10|unit|Rp 1.250.000|5%" \
     --item "Meja kerja 120x60|10|unit|Rp 950.000" \
     --diskon-total "Rp 250.000" --ongkir "Rp 300.000" \
     --ppn pkp --nomor-urut 12 --kode "SPH/MKS" --tanggal 2026-09-23 --berlaku-hari 14
   ```
   - Format item: `Nama|qty|satuan|harga|diskon` (diskon opsional, `10%` atau `Rp 50.000` untuk baris itu). Jangan pakai tanda `|` di nama item.
   - Banyak item: simpan CSV berkolom `nama,qty,satuan,harga,diskon` lalu `--file items.csv`.
   - Harga item sudah termasuk PPN: tambahkan `--harga-termasuk-ppn`. PPN hanya dikeluarkan dari harga item; ongkir dianggap nilai bersih (belum termasuk PPN) sehingga PPN ongkir ditambahkan. Jika ongkir juga sudah termasuk PPN, masukkan ongkir sebagai item (`Ongkos kirim|1|paket|...`).
   - Semua baris `ASUMSI (sebutkan ke pengguna)` dari script **wajib** disalin ke blok "Asumsi yang dipakai".
   - `--format json` bila hanya butuh angka. Script keluar dengan kode ≠ 0 dan pesan `ERROR:` bila input salah; perbaiki lalu jalankan ulang, jangan menebak angka.
4. **Susun surat** memakai angka dari output script apa adanya (lihat Format output). Kerangka lengkap & variasi kalimat pembuka ada di `references/kerangka-sph.md`.
5. **Sediakan versi siap cetak — DI CHAT.** Balasan chat **SELALU** memuat (a) **isi surat lengkap** (kop sampai tanda tangan, siap salin/cetak) dan (b) **teks WhatsApp pendek siap kirim**. Menyimpan ke file saja **tidak cukup**: pengguna (mis. lewat Telegram) tidak bisa membuka path lokal, dan ringkasan angka tanpa surat dianggap gagal. File `SPH-<nomor urut>.md` hanya **tambahan** (bila bisa menulis file; sebutkan lokasinya, lampirkan bila kanal mendukung).
   - **PIC tidak diketahui:** pakai sapaan umum "Bapak/Ibu Bagian Pengadaan" (atau "Bapak/Ibu Pimpinan" untuk usaha kecil), **bukan** `[Nama PIC]`.
   - **Penjual bukan PKP:** tulis "Harga final; penjual bukan PKP sehingga tidak memungut PPN." Jangan menulis "belum kena PPN"/"belum termasuk PPN" (menyesatkan, seolah PPN menyusul). Skill ini **tidak membuat PDF**: katakan terus terang, lalu beri cara singkat — tempel/buka surat di Word atau Google Docs → *File → Download/Save as PDF*. Jangan memasang paket pembuat PDF.
6. **Buat versi WhatsApp — wajib tampil di chat, tanpa menunggu diminta** (ringkas, tanpa tabel, ≤ 15 baris). **Jangan menyebut lampiran/PDF yang tidak benar-benar dibuat dan dilampirkan.** Kalimat lampiran hanya dipakai bila file surat memang ikut dikirim, dengan menyebut format sebenarnya.
7. **Periksa** dengan checklist, lalu tawarkan revisi (diskon, masa berlaku, gaya bahasa lebih formal/santai).

### Fallback jika Python tidak bisa dijalankan
Hitung manual langkah demi langkah dan tulis perhitungannya, lalu beri tahu pengguna: "Angka dihitung manual, mohon dicek ulang."
1. Jumlah baris = qty × harga satuan − diskon baris (dibulatkan ke rupiah terdekat).
2. Subtotal = Σ jumlah baris. Setelah diskon = subtotal − diskon total.
3. DPP = setelah diskon + ongkir.
4. PPN: bukan PKP = 0; PKP non-mewah = DPP × 11/12 × 12% (= DPP × 11%); mewah = DPP × 12%. Hitung persis lalu **bulatkan ke bawah** sekali (buang pecahan rupiah).
5. Total = DPP + PPN. Jika harga item sudah termasuk PPN (non-mewah): DPP item = rupiah bulat terbesar sehingga DPP + PPN (ke bawah) ≤ harga item setelah diskon (mulai dari harga ÷ 1,11 lalu cek); sisa Rp 0–1 ditampilkan sebagai selisih pembulatan; ongkir tetap ditambah PPN 11% di atasnya.

## Format output
Berikan **dua bagian**: (A) surat lengkap dalam markdown, (B) teks WhatsApp.

```
**[NAMA USAHA]**
[Alamat] · WA [nomor] · [email]
---------------------------------------------
Nomor    : 012/SPH/MKS/IX/2026
Lampiran : -
Perihal  : Penawaran Harga [jenis barang/jasa]

[Kota], 23 September 2026

Kepada Yth.
[Nama PIC] – [Jabatan]
[Nama Perusahaan/Instansi]
di tempat

Dengan hormat,
[Kalimat pembuka: rujuk permintaan/pertemuan, 1–2 kalimat.]

| No | Uraian | Qty | Satuan | Harga Satuan | Diskon | Jumlah |
|---|---|---|---|---|---|---|
| ... baris dari script ... |

| | |
|---|---|
| Subtotal | Rp ... |
| Diskon tambahan | −Rp ... |
| Ongkos kirim | Rp ... |
| DPP | Rp ... |          ← hanya jika PKP
| PPN 12% (DPP nilai lain 11/12) | Rp ... |   ← hanya jika PKP
| **TOTAL** | **Rp ...** |

Terbilang: *... Rupiah*

**Syarat & ketentuan**
1. Harga [belum/sudah] termasuk PPN. [Jika bukan PKP, ganti dengan: "Harga final; penjual bukan PKP sehingga tidak memungut PPN."]
2. Penawaran berlaku sampai [tanggal dari script].
3. Pembayaran: [DP 50% saat PO, pelunasan ...] ke [Bank – No. Rek – a.n.].
4. Pengiriman: [estimasi], [franco/ambil sendiri/ongkir ditanggung ...].
5. [Garansi/retur jika ada.]

[Penutup 1–2 kalimat + ajakan konfirmasi PO.]

Hormat kami,

[Nama]
[Jabatan] – [Nama Usaha]
```
Di bawah surat, tambahkan blok **Asumsi yang dipakai** (jika ada) dan **Catatan** singkat: "Perhitungan PPN mengikuti PMK 131/2024 (berlaku per 2026-09-23). Bukan nasihat pajak; kasus khusus konsultasikan ke konsultan pajak/KPP."

(B) Teks WhatsApp:
```
Selamat [pagi/siang], Bapak/Ibu [Nama] 🙏
Berikut penawaran harga dari [Usaha] untuk [kebutuhan]:
• [Item 1] – [qty] [satuan] × Rp ... 
• [Item 2] – ...
Total: *Rp ...* ([termasuk/tanpa] PPN[, sudah termasuk ongkir])
Berlaku s.d. [tanggal]. Pembayaran [ringkas]. Pengiriman [ringkas].
[Hanya jika file surat benar-benar dilampirkan: "Surat penawaran resminya terlampir."]
[Jika belum ada file: "Surat penawaran resminya menyusul/bisa kami kirimkan bila diperlukan."]
Jika ada yang ingin disesuaikan, kabari saja ya, Bapak/Ibu.
```

## Contoh
**Input pengguna:** "Tolong buatkan SPH dari CV Maju Kreasi Sejahtera (Semarang, PKP) untuk PT Sinar Logistik, Bu Rina bagian GA. 10 kursi kantor ergonomis @1.250.000 diskon 5%, 10 meja kerja 120x60 @950rb. Kasih potongan 250rb, ongkir 300rb. Nomor urut 12."

**Output (ringkas):** script menghasilkan Subtotal Rp 21.375.000 → diskon tambahan −Rp 250.000 → ongkir Rp 300.000 → DPP Rp 21.425.000 → PPN Rp 2.356.750 → **Total Rp 23.781.750** (Dua Puluh Tiga Juta Tujuh Ratus Delapan Puluh Satu Ribu Tujuh Ratus Lima Puluh Rupiah), nomor `012/SPH/MKS/IX/2026`, berlaku s.d. 7 Oktober 2026. Surat disusun dengan format di atas + teks WA:
```
Selamat siang, Bu Rina 🙏
Berikut penawaran harga dari CV Maju Kreasi Sejahtera untuk kebutuhan furnitur kantor:
• Kursi kantor ergonomis – 10 unit × Rp 1.250.000 (diskon 5%)
• Meja kerja 120x60 – 10 unit × Rp 950.000
Total: *Rp 23.781.750* (sudah termasuk PPN & ongkir Semarang)
Berlaku s.d. 7 Oktober 2026. DP 50% saat PO, pelunasan sebelum kirim.
Surat penawaran resminya menyusul ya, Bu. Jika jumlahnya ingin disesuaikan, kabari saja.
```
(Surat lengkap tersedia dalam format siap cetak; PDF tidak dibuat oleh skill — buka di Word/Google Docs lalu simpan sebagai PDF bila perlu. Setelah pemilik melampirkan file-nya, kalimat "menyusul" boleh diganti "terlampir".)
Asumsi: ongkir Rp 300.000 ditagih penjual sehingga ikut DPP & dikenai PPN (jika ongkir hanya titipan biaya kurir, hitung ulang tanpa `--ongkir`); pembayaran DP 50%, pengiriman 5 hari kerja (tidak disebutkan pengguna).

## Checklist sebelum mengirim hasil
- [ ] Semua angka berasal dari output script (atau hitung manual yang ditulis lengkap + peringatan).
- [ ] Balasan chat memuat isi surat lengkap DAN teks WA (bukan hanya ringkasan/path file).
- [ ] Tidak ada `[Nama PIC]` bila pengguna bilang PIC tidak diketahui (pakai "Bapak/Ibu Bagian Pengadaan"); bukan PKP → tidak ada kata "belum kena/belum termasuk PPN".
- [ ] PPN hanya muncul jika penjual PKP; teks "termasuk/belum termasuk PPN" konsisten dengan angka.
- [ ] Total di tabel = total di teks WA = terbilang.
- [ ] Nomor surat, tanggal, masa berlaku, perihal, penerima terisi (atau `[isi ...]` yang jelas).
- [ ] Syarat pembayaran & pengiriman ada; rekening tidak dikarang.
- [ ] Tidak ada klaim yang tidak diberikan pengguna (garansi, SNI, TKDN, "termurah").
- [ ] Jika ongkir dipakai dan penjual PKP, asumsi "ongkir ikut DPP & kena PPN" tertulis. Jika ongkir gratis, tulis "Ongkos kirim: Gratis" atau "Harga franco [alamat]" di syarat.
- [ ] Asumsi ditulis jika memakai default.
- [ ] Teks WA tidak menyebut "terlampir"/"PDF" kecuali file itu benar-benar dibuat dan dilampirkan; bila PDF tidak dibuat, disebut terus terang beserta cara menyimpannya sebagai PDF.

## Batasan & penanganan error
- Skill tidak menerbitkan faktur pajak; faktur resmi dibuat PKP lewat Coretax. Standar pembulatan library: total baris & diskon ke rupiah terdekat, PPN dihitung persis lalu **dibulatkan ke bawah** sekali (sama dengan skill `hitung-ppn` & `buat-invoice`). Pembulatan ini **belum dicocokkan dengan Coretax**, jadi faktur resmi bisa berbeda Rp 1.
- Uji regresi script: `python3 scripts/test_hitung_sph.py` (opsional).
- Tidak menghitung PPnBM, PPh 22/23, atau DPP khusus (mis. jasa/barang yang punya DPP nilai lain tersendiri). Jika pengguna menyebut hal itu, beri tahu dan sarankan konsultan pajak.
- Harga satuan tidak bulat (mis. Rp 33.333,33): script menghitung jumlah dari nilai tepat, sedangkan harga satuan ditampilkan dibulatkan; beri tahu pengguna bila terlihat selisih.
- Mata uang selain Rupiah: jelaskan bahwa skill ini untuk Rupiah; minta pengguna mengonversi sendiri dengan kurs yang disepakati.
- Jangan mengarang harga pasar, stok, atau spesifikasi teknis; tanyakan atau tandai `[isi]`.
