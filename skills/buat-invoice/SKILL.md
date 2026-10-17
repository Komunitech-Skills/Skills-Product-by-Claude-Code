---
name: buat-invoice
description: Membuat invoice/tagihan atau kuitansi profesional berbahasa Indonesia dengan nomor otomatis, daftar item, diskon, ongkir, PPN opsional khusus PKP (DPP nilai lain 11/12), DP/termin, sisa tagihan, terbilang, rekening, jatuh tempo, dan penanda bea meterai Rp10.000 bila penerimaan uang di atas Rp5 juta; output Markdown rapi plus HTML siap cetak. Gunakan saat pengguna minta "buatkan invoice", "nota tagihan", "kuitansi DP/lunas", atau invoice generator, receipt, billing. Menagih ulang piutang pakai tagih-piutang; penawaran harga pakai surat-penawaran-harga.
---

# Buat Invoice & Kuitansi

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; file baru hanya ditulis di folder kerja yang disepakati (bukan /tmp); lokasinya disebut di terminal/IDE, sedangkan di aplikasi chat cukup disebut bahwa berkas dibuat atau nomor sudah dicatat (tanpa path/nama folder).

> **Aturan balasan (wajib, terutama Telegram/WhatsApp):** yang pasti sampai ke pengguna hanya **balasan terakhir** giliran ini. Teks yang ditulis sebelum memanggil alat (melampirkan berkas, menjalankan perintah) bisa **tidak pernah terkirim**. Urutannya selalu: jalankan script → lampirkan berkas (langkah 3) → **baru** tulis balasan terakhir yang memuat **invoice/kuitansi lengkap** = seluruh bagian di atas garis `---` dari script, apa adanya: nomor, tanggal, pihak, tabel item, subtotal, TOTAL, terbilang, kota & penanda tangan (boleh `[isi ...]`), plus baris yang memang dicetak script **bila ada** (jatuh tempo, diskon, ongkir, PPN, DP/sudah dibayar, sisa, termin, PPh 23, rekening, meterai). Jangan menambah baris kosong atau karangan untuk yang tidak ada. Jangan menulis dokumen sebelum langkah lampir selesai. Jangan pernah menulis "lihat di atas", "sudah saya tulis di atas", atau "invoice di pesan sebelumnya", dan jangan mengganti dokumen dengan ringkasan.

## Tujuan
Menghasilkan invoice atau kuitansi yang rapi, angkanya pasti benar (dihitung script), dan siap dikirim lewat WhatsApp/email atau dicetak — tanpa aplikasi akuntansi.

## Kapan digunakan
- "Buatkan invoice untuk PT X: 100 kaos @65 ribu, diskon 5%, ongkir 75 ribu, DP sudah 3 juta."
- "Buat kuitansi pelunasan Rp7.500.000 untuk Bu Sari."
- Invoice dengan termin (DP 30% – termin 30% – pelunasan 40%).
- Invoice ber-PPN untuk penjual PKP.

## Kapan TIDAK digunakan
- Mengingatkan/menagih pelanggan yang telat bayar → skill `tagih-piutang`.
- Penawaran harga sebelum deal → skill `surat-penawaran-harga`.
- Faktur pajak resmi → dibuat di Coretax; invoice ini bukan faktur pajak.
- Hanya ingin tahu PPN suatu harga → skill `hitung-ppn`.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Nama penjual (usaha) | Ya | — (tanyakan) |
| Nama pembeli | Ya | — (tanyakan) |
| Item: nama, jumlah, harga satuan (+ diskon per item) | Ya | — (tanyakan) |
| Jenis dokumen: invoice atau kuitansi | Tidak | Invoice |
| Nomor terakhir / nomor yang diinginkan | Tidak | `INV/<tahun>/<bulan>/0001` + pengingat |
| Kota, nama & jabatan penanda tangan | Tidak | `[isi kota]`, `[isi nama penanda tangan]` — **jangan dikarang atau ditebak dari data lain** (nama pemilik rekening, nama usaha, nama pengirim pesan bukan nama penanda tangan) |
| Tanggal & jatuh tempo | Tidak | Hari ini; jatuh tempo 14 hari |
| Diskon total, ongkir | Tidak | 0 |
| Status PKP penjual (+ jenis PPN umum/mewah) | Tidak | Pengguna menyebut **PKP** → `"pkp": true` + `"ppn": true` (PPN 12% × DPP nilai lain 11/12, jenis umum) **tanpa bertanya**, sebut asumsinya. Tidak menyebut PKP → tanpa PPN |
| Pembeli memotong PPh 23 (klien badan/PT/CV membayar **jasa**) | Tidak | Bila pengguna menyebut "dipotong PPh 23" atau klien badan untuk jasa: **aktifkan** `"pph23": true` (2% dari nilai jasa tanpa PPN; tanpa NPWP 4%) dan sebut asumsinya |
| DP/pembayaran yang sudah diterima, termin | Tidak | Belum ada |
| Rekening, alamat/kontak, NPWP, catatan, jabatan | Tidak | Dikosongkan |

Jika info wajib kurang, tanyakan **sekali** dalam satu pesan bernomor (maks. 5 pertanyaan). Jika pengguna minta PPN, pastikan ia **PKP**; jika tidak, jelaskan bahwa PPN tidak boleh dicantumkan.

**PKP = PPN aktif secara default (jangan bertanya ulang).** Bila pengguna sudah menyebut dirinya PKP ("saya sudah PKP", "usaha kami PKP"), langsung buat invoice ber-PPN: **PPN 12% dengan DPP nilai lain 11/12** (PMK 131/2024, barang/jasa non-mewah). Tulis asumsinya di akhir balasan (mis. "PPN 12% × DPP nilai lain 11/12 karena Anda PKP; bila transaksi ini disepakati tanpa PPN, beri tahu saya"). Jangan pernah menanyakan atau menyebut "PPN 11%" ke pengguna — sebut selalu "PPN 12% (DPP nilai lain 11/12)". Nomor (default `0001`), kota, dan penanda tangan yang tidak disebut cukup jadi placeholder; itu juga bukan alasan untuk bertanya bila item, pembeli, dan penjual sudah lengkap.

**Jangan mengarang atau menebak data.** Kota, nama dan jabatan penanda tangan, nama usaha, alamat, rekening (termasuk nama pemilik rekening "a.n."), NPWP hanya diisi bila pengguna **menyebutnya langsung** untuk keperluan itu. Contoh yang dilarang: "BCA 123 a.n. Rini Kusumawati" lalu menulis Rini Kusumawati sebagai penanda tangan, atau menulis "a.n. <nama usaha>" padahal pemilik rekening tidak disebut. Bila tidak disebut, kosongkan kolomnya di JSON: script menulis `[isi kota]` / `[isi nama penanda tangan]` dan baris "PERLU DIISI" (jabatan, alamat, dan "a.n." yang kosong dibiarkan kosong/tidak ditampilkan) — sampaikan ke pengguna sebagai hal yang perlu diisi.

**Penomoran (wajib persis):** salin nomor terakhir **huruf demi huruf** dari pesan pengguna ke `--nomor-terakhir` (jangan dikurangi/ditebak). Nomor baru = nomor terakhir **+ 1** (`INV/2026/09/0012` → `INV/2026/09/0013`) dan **tidak pernah sama** dengan nomor terakhir yang disebut pengguna (script memberi PERHATIAN bila sama; kecuali memang revisi, perbaiki). Cocokkan baris `Nomor terakhir dibaca: X -> nomor baru: Y` di output script dengan pesan pengguna sebelum menampilkan invoice.
- Bulan/tahun dokumen berganti dari nomor terakhir → script mengganti periode dan mulai lagi dari `0001` (`INV/2026/09/0012` + tanggal Oktober → `INV/2026/10/0001`). Jika usaha pengguna melanjutkan nomor lintas bulan, tambah `--urut-lanjut` (→ `INV/2026/10/0013`). Bila tidak jelas, sebutkan aturan yang dipakai.
- Format lain dikenali: `012/INV/IX/2026` (bulan Romawi, urut di depan), `INV-2026-0012` (nomor tahunan).
- Tanggal dokumen lebih lama dari periode nomor terakhir → script menolak (nomor mundur); tanyakan ke pengguna.
- **Cegah nomor dobel:** selalu tambahkan `--counter-file nomor-invoice.json` di folder kerja yang disepakati (path yang sama setiap kali; terminal/IDE: sebut lokasinya; aplikasi chat: cukup "nomor terakhir sudah dicatat", tanpa path). Script mencatat setiap nomor + nama pembeli. Invoice kedua dst. dalam percakapan yang sama: `--nomor-terakhir` = nomor yang **baru dibuat script**, bukan nomor dari pesan awal pengguna. Bila script mencetak `PERHATIAN: Nomor ... sudah dipakai untuk ...`, pakai nomor yang tercetak di dokumen dan sampaikan ke pengguna; nomor yang sama untuk pembeli yang sama = revisi (nomor tetap).

## Langkah kerja
1. Susun data ke file JSON di folder kerja pengguna mengikuti `templates/contoh-invoice.json` (penjelasan kolom: `references/format-input.md`).
   - PPh 23: `"pph23": true` (default 2% × subtotal setelah diskon, tanpa PPN & ongkir) atau `{"tanpa_npwp": true}` (4%) / `{"dasar": "<nilai jasa saja>"}` bila invoice juga berisi barang. Ini **info** "estimasi diterima bersih"; total tagihan tidak berubah. Penjual PPh final 0,5% yang sudah memberi Surat Keterangan PP 55 ke klien → jangan diaktifkan.
2. Jalankan script. Script ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill); jalankan dari sana, jangan mencari ke seluruh disk (`find /`). Windows: `python` atau `py`:
   ```bash
   python3 <folder-skill-ini>/scripts/buat_invoice.py --file invoice.json --html invoice-{nomor}.html --txt invoice-{nomor}.txt --nomor-terakhir INV/2026/09/0007 --counter-file nomor-invoice.json
   ```
   Tulis `{nomor}` apa adanya (jangan diganti tangan): script menggantinya dengan nomor dokumen yang sama dengan yang tampil di chat (`/` menjadi `-`; `001/INV/X/2026` → `invoice-001-INV-X-2026.html`). Untuk kuitansi pakai `kuitansi-{nomor}.html` dan `kuitansi-{nomor}.txt`. Nama berkas tidak boleh dikarang atau ditebak dari nomor lain; nama dan lokasi berkas hanya yang dicetak script pada baris `BERKAS: <path absolut>` dan `BERKAS TEKS: <path absolut>` (lihat langkah 3).
   - `--nomor-terakhir` → nomor terakhir + 1 (aturan ganti bulan/tahun di atas; `--urut-lanjut` bila nomor tidak di-reset).
   - `--counter-file nomor-invoice.json` → mencatat nomor yang sudah dibuat (+ nama pembeli) dan nomor urut per bulan; tanpa `--nomor-terakhir`, nomor diambil dari file ini. Nomor yang sudah dipakai pembeli lain tidak pernah dipakai ulang.
   - `--html <file>` → versi HTML siap cetak (buka di browser → Cetak → Simpan sebagai PDF); path boleh memuat `{nomor}` atau berupa folder (nama berkas otomatis dari nomor).
   - `--txt <file>` → versi teks biasa (.txt, isi & angka sama, tanpa "Info untuk penjual"); cadangan lampiran bila kanal chat menolak berkas siap cetak.
   - `--format json` → angka mentah.
   - Kuitansi DP/cicilan: isi `pembayaran` dengan uang yang diterima sekarang; kuitansi menampilkan uang diterima, baris diterima & sisa belum dibayar, dan **satu** terbilang untuk uang yang diterima.
3. **Lampirkan berkas dulu (belum menulis dokumen).** Script mencetak path absolut pada baris `BERKAS: …` (versi siap cetak) dan `BERKAS TEKS: …` (versi teks biasa). Di aplikasi chat (Telegram/WhatsApp), untuk invoice **maupun** kuitansi:
   - **Utamakan alat kirim/lampir yang melaporkan berhasil atau gagal** (mis. alat kirim pesan dengan lampiran), dipanggil **sebelum** balasan terakhir. Path disalin **persis** dari baris itu (jangan menyusun, menebak, atau memperbaiki path; nama berkas tidak dikarang). Keterangan lampiran pakai kata awam, mis. "Invoice INV/2026/10/0008, siap cetak" atau "Kuitansi KWT/2026/10/0004, versi teks".
   - Urutan: `BERKAS:` sekali → bila gagal, `BERKAS TEKS:` sekali. Bila kanal chat diketahui menolak berkas siap cetak dari folder kerja (contoh: OpenClaw menolak berkas HTML dari folder kerja), langsung lampirkan `BERKAS TEKS:`. Maksimal dua percobaan; jangan mengulang berkas yang sama dengan opsi atau format lain.
   - **Bila satu-satunya cara melampirkan adalah baris lampiran di dalam balasan terakhir** (mis. baris tersendiri `MEDIA:<path>`), hasilnya tidak bisa diketahui: lampirkan **hanya** `BERKAS TEKS:` (versi teks; berkas siap cetak dari folder kerja ditolak kanal chat), tepat **satu** baris lampiran di baris paling akhir. Jangan pernah menulis dua baris lampiran untuk dokumen yang sama, dan pakai kalimat status netral (langkah 4).
   - Jangan menulis narasi ("sekarang saya lampirkan…") di antara langkah: teks itu tidak sampai ke pengguna.
   - Terminal/IDE (tanpa fitur lampiran): tidak perlu melampirkan; lokasi berkas disebut di balasan terakhir (langkah 4).
4. **Balasan terakhir = dokumen lengkap.** Salin bagian Markdown di atas garis `---` dari script apa adanya (termasuk baris judul tabel), lalu catatan singkat untuk penjual dari "Info untuk penjual" (meterai, PPN, PPh 23, peringatan, data yang perlu diisi; angka dan kalimat meterai disalin apa adanya) dengan label "catatan untuk Anda, jangan dikirim ke pembeli". Tutup dengan **satu** kalimat status berkas; `<dokumen>` = "invoice" atau "kuitansi" sesuai jenisnya:
   - Alat melaporkan berkas siap cetak terkirim: "Berkas <dokumen> siap cetak sudah saya kirim terpisah: buka, lalu Cetak atau Simpan sebagai PDF."
   - Alat melaporkan hanya versi teks terkirim: "Berkas siap cetak belum bisa dikirim lewat chat ini, jadi saya kirim versi teks <dokumen>. Untuk dicetak, salin teks <dokumen> di pesan ini ke Word/Google Docs."
   - Lampiran lewat baris di balasan (hasil tidak diketahui): "Versi teks <dokumen> saya lampirkan di pesan ini; kalau tidak muncul, balas 'kirim file'."
   - Semua percobaan gagal: "Berkas siap cetak belum bisa dikirim lewat chat ini; balas 'kirim file' kalau mau saya coba lagi, atau salin teks <dokumen> di pesan ini ke Word/WA."
   - Terminal/IDE: "Berkas siap cetak: <path dari BERKAS>. Versi teks: <path dari BERKAS TEKS>. Nomor dicatat di <path file pencatat nomor>."
   - Di aplikasi chat jangan memakai kata HTML, path/jalur, folder, sistem, akses baca, error, nama alat, atau nama berkas (baris lampiran `MEDIA:` bukan teks untuk pengguna). Tulis "terkirim/terlampir" hanya bila alat benar-benar melaporkan berhasil. "Balas 'kirim file'" hanya setelah percobaan nyata gagal atau bila hasilnya tidak diketahui, bukan pengganti mencoba.
   - Pengguna membalas "kirim file": **jangan menjalankan script lagi** (menjalankan ulang dengan `--nomor-terakhir` diam-diam membuat nomor baru, mis. 0009). Pakai lagi path `BERKAS:`/`BERKAS TEKS:` dari keluaran script sebelumnya dengan urutan langkah 3. Bila berkasnya sudah tidak ada, jalankan ulang dengan nomor yang sama di kolom `nomor` JSON (revisi, nomor tetap). Tetap tidak bisa → katakan jujur dengan kalimat awam dan sarankan menyalin teks ke Word/Google Docs lalu Simpan sebagai PDF. Pada jalur baris lampiran (hasil tidak diketahui), "kirim file" hanya diulang **sekali**; bila pengguna meminta lagi, jangan lampirkan ulang: katakan berkas belum bisa dipastikan sampai lewat chat ini dan sarankan menyalin teks. Pada giliran "kirim file" dokumen tidak perlu ditulis ulang, cukup satu kalimat status.
5. Meterai: salin kalimat "Bea meterai: …" dari script **apa adanya**; jangan membandingkan nominal dengan Rp5 juta sendiri atau merangkumnya ("di bawah/di atas" sudah dihitung script dari angka). Bila meterai wajib di dokumen ini, ingatkan menempel meterai Rp10.000 atau e-meterai sebelum tanda tangan.
6. **Fallback tanpa Python:** hitung dengan rumus di bawah dan tulis dokumen lengkap dengan format yang sama di balasan terakhir. Tidak ada berkas yang dibuat, jadi tidak ada lampiran. Tutup dengan: "Angka dihitung manual, mohon cek ulang sebelum dikirim. Berkas siap cetak tidak dibuat; salin teks <dokumen> di pesan ini ke Word/Google Docs untuk dicetak."

## UNTUK AGENT SAJA — lampiran & meterai (jangan dibacakan ke pengguna)
- Urutan giliran: script → lampir lewat alat yang melaporkan hasil (`BERKAS:` sekali → bila gagal `BERKAS TEKS:` sekali; kanal yang diketahui menolak berkas siap cetak → langsung `BERKAS TEKS:`) → balasan terakhir berisi dokumen lengkap. Hanya balasan terakhir yang pasti sampai di Telegram/WhatsApp; dokumen yang ditulis sebelum pemanggilan alat dianggap tidak terkirim (uji bot Telegram asli 17 Okt 2026: pengguna hanya menerima ringkasan).
- Lampiran hanya bisa lewat baris `MEDIA:` di balasan terakhir → satu baris, `BERKAS TEKS:` saja, kalimat status netral. Kanal chat OpenClaw menolak berkas HTML dari folder kerja; versi teks `.txt` diterima.
- Path berkas = isi baris `BERKAS:` / `BERKAS TEKS:` dari keluaran script, apa adanya. "Kirim file" → pakai path yang sama, jangan jalankan script lagi. Berlaku untuk invoice dan kuitansi, di kanal chat mana pun.
- Meterai: wajib bila nilai penerimaan uang **> Rp5.000.000** (Rp5.075.000 = di atas, kena; Rp5.000.000 pas = tidak). Kalimat meterai (termasuk penilaian sisa tagihan atau tiap termin) dihitung script; salin apa adanya ke catatan untuk pengguna, jangan menulis "di bawah Rp5 juta" dari kira-kira.
- Angka hasil script disalin apa adanya; jangan menghitung ulang atau membulatkan sendiri.

## Rumus (untuk hitung manual)
```
jumlah baris   = qty × harga − diskon baris        (diskon % dari qty × harga; dibulatkan ke rupiah terdekat)
subtotal       = jumlah semua baris
setelah diskon = subtotal − diskon total           (diskon % dari subtotal; dibulatkan ke rupiah terdekat)
DPP            = setelah diskon + ongkir           (ongkir tidak dimasukkan bila "ongkir_kena_ppn": false)
PPN (PKP saja) = non-mewah: 12% × DPP nilai lain (11/12 × DPP); mewah: 12% × DPP; dibulatkan KE BAWAH
TOTAL          = setelah diskon + ongkir + PPN
PPh 23 (info)  = 2% × nilai jasa tanpa PPN (default subtotal setelah diskon, tanpa ongkir); tanpa NPWP 4%;
                 dibulatkan KE BAWAH. Estimasi diterima bersih = TOTAL − PPh 23 (TOTAL tagihan tidak berubah;
                 dasar: UU PPh Pasal 23 ayat (1) huruf c & ayat (1a))
sisa tagihan   = TOTAL − pembayaran yang sudah diterima
termin persen  = TOTAL × persen, dibulatkan ke rupiah terdekat; termin terakhir = sisa agar jumlahnya pas
Bea meterai    = wajib Rp10.000 bila dokumen menyatakan penerimaan uang > Rp5.000.000 (DI ATAS Rp5 juta)
                 (kuitansi senilai uang diterima; invoice yang mencantumkan DP/pembayaran diterima)
                 Rp5.075.000 → di atas Rp5 juta → wajib; tepat Rp5.000.000 atau kurang → tidak wajib
                 sisa tagihan juga dibandingkan dengan Rp5.000.000 untuk kuitansi pelunasan (dihitung script)
```
Dasar aturan & sumber: `references/regulasi.md` (berlaku per 2026-09-23).

## Format output
```
# INVOICE / KUITANSI
No., Tanggal, Jatuh tempo, Status (BELUM DIBAYAR / SEBAGIAN DIBAYAR / LUNAS)
Dari: <penjual>   Kepada: <pembeli>
| No | Deskripsi | Qty | Harga | Diskon | Jumlah |
Subtotal, Diskon, Ongkir, [DPP, DPP nilai lain, PPN 12%], TOTAL, [Sudah dibayar, SISA TAGIHAN]
Terbilang, [Jadwal termin], Pembayaran ke, Catatan, Kota & tanggal, [Meterai], Tanda tangan
---
Info untuk penjual (meterai, PPN, pembulatan, peringatan)
```
Balasan terakhir di chat: [dokumen lengkap di atas] → [catatan untuk penjual] → [satu kalimat status berkas, bahasa awam].

## Contoh
**Input pengguna (Telegram):** "Buat invoice dari CV Contoh Kreasi ke PT Pelanggan Contoh: 100 kaos sablon @65 ribu diskon 5%, biaya desain 500 ribu, ongkir 75 ribu. DP 3 juta sudah masuk tanggal 20 September. Rekening BCA 0000000000."

**Balasan terakhir** (tanggal 23 September 2026; kanal menolak berkas siap cetak, versi teks terlampir lewat alat). Dokumen = salinan utuh bagian di atas `---` dari script; kota, penanda tangan, dan "a.n." tidak disebut pengguna sehingga tidak dikarang:
```
# INVOICE

**No.:** INV/2026/09/0001
**Tanggal:** 23 September 2026
**Jatuh tempo:** 7 Oktober 2026
**Status:** SEBAGIAN DIBAYAR

**Dari:**
**CV Contoh Kreasi**

**Kepada:**
**PT Pelanggan Contoh**

| No | Deskripsi | Qty | Harga | Diskon | Jumlah |
|---:|---|---:|---:|---:|---:|
| 1 | Kaos sablon custom | 100 pcs | Rp 65.000 | Rp 325.000 (5%) | Rp 6.175.000 |
| 2 | Biaya desain | 1 paket | Rp 500.000 | - | Rp 500.000 |

| | |
|---|---:|
| Subtotal | Rp 6.675.000 |
| Ongkos kirim | Rp 75.000 |
| **TOTAL** | **Rp 6.750.000** |
| Sudah dibayar - DP (20 September 2026) | -Rp 3.000.000 |
| **SISA TAGIHAN** | **Rp 3.750.000** |

Terbilang: _Tiga Juta Tujuh Ratus Lima Puluh Ribu Rupiah_

**Pembayaran ke:**
- BCA 0000000000

[isi kota], 23 September 2026

**[isi nama penanda tangan]**
CV Contoh Kreasi

Catatan untuk Anda (jangan dikirim ke pembeli):
- Bea meterai: Tidak perlu meterai: dokumen tidak menyatakan penerimaan uang di atas Rp5.000.000. Catatan: Sisa tagihan Rp 3.750.000 tidak lebih dari Rp5.000.000, jadi kuitansi pelunasan sekali bayar untuk sisa ini tidak wajib meterai.
- Kota dan nama penanda tangan belum diisi; kabari saya bila ingin dicantumkan.
- Nomor memakai 0001 dan sudah dicatat; sebutkan nomor invoice terakhir Anda bila ingin melanjutkan urutan lama.

Berkas siap cetak belum bisa dikirim lewat chat ini, jadi saya kirim versi teks invoice. Untuk dicetak, salin teks invoice di pesan ini ke Word/Google Docs.
```

## Checklist sebelum mengirim hasil
- [ ] Semua angka dari script; total, sisa tagihan, dan terbilang cocok.
- [ ] Klien badan + jasa + disebut "potong PPh 23" → PPh 23 & estimasi diterima bersih ikut tampil (dari script).
- [ ] **Balasan terakhir** memuat invoice/kuitansi lengkap = seluruh bagian di atas `---` dari script (nomor, item, subtotal, TOTAL, terbilang, kota & penanda tangan, plus jatuh tempo, diskon, ongkir, PPN, DP, sisa, rekening **bila ada**; tidak ada baris kosong/karangan), ditulis **sesudah** percobaan lampir; bukan ringkasan, tidak ada "lihat/sudah di atas".
- [ ] Lampiran lewat alat yang melaporkan hasil: `BERKAS:` sekali → bila gagal `BERKAS TEKS:` sekali (maks. dua percobaan), path persis. Hanya bisa lewat baris `MEDIA:` → satu baris `BERKAS TEKS:` saja + kalimat netral. Kalimat status sesuai jenis dokumen, tanpa kata HTML/path/sistem/error; "kirim file" tidak menjalankan ulang script.
- [ ] Nama berkas berasal dari nomor yang tampil di chat (`invoice-{nomor}.html` / `.txt`), bukan nomor lain.
- [ ] PPN hanya muncul bila penjual PKP; tidak ada PPN untuk non-PKP.
- [ ] Pengguna menyebut PKP → PPN 12% (DPP nilai lain 11/12) langsung dipakai tanpa bertanya, asumsi disebut; tidak ada tulisan "PPN 11%".
- [ ] Nomor = nomor terakhir dari pengguna + 1 (cek baris "Nomor terakhir dibaca"), tidak dobel dengan invoice lain (`--counter-file` dipakai, PERHATIAN nomor disampaikan); jatuh tempo tidak lebih awal dari tanggal dokumen.
- [ ] Tidak ada data karangan/tebakan: kota, nama & jabatan penanda tangan, alamat, dan "a.n." rekening yang tidak disebut tetap kosong/`[isi ...]` dan disampaikan ke pengguna (bukan diambil dari nama pemilik rekening atau nama usaha).
- [ ] Penanda meterai sesuai (> Rp5.000.000 penerimaan uang); kalimat meterai disalin dari script, bukan ditulis dari perkiraan (sisa Rp5.075.000 = di atas Rp5 juta).
- [ ] Rekening & nama penerima benar; tidak ada data pribadi yang tidak diminta.
- [ ] Bagian "Info untuk penjual" tidak ikut dikirim ke pembeli.

## Batasan & penanganan error
- Script keluar kode 2 + `ERROR: ...` bila: PPN diaktifkan tetapi penjual bukan PKP, item kosong, qty ≤ 0, harga/diskon bukan angka, diskon melebihi nilai, diskon persen > 100%, total persen termin ≠ 100%, jumlah termin ≠ total, tanggal tidak valid, jatuh tempo sebelum tanggal dokumen, nomor terakhir tanpa angka urut, tanggal dokumen lebih lama dari periode nomor terakhir, nomor manual yang sudah dipakai pembeli lain (tercatat di file counter), file counter rusak, atau JSON rusak. Jelaskan dengan bahasa sederhana dan perbaiki datanya.
- Pembayaran melebihi total → tetap dibuat dengan peringatan "lebih bayar".
- Satu jenis PPN per invoice (umum atau mewah). Barang dengan PPN khusus/dibebaskan, PPnBM, dan faktur pajak di luar cakupan → arahkan ke konsultan/DJP.
- Script hanya menulis file HTML/teks/counter ke path yang diberikan pengguna; tidak ada akses internet.
