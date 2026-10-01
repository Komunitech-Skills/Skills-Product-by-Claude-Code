# Uji ulang OpenClaw — Konsultan 02 · Surat penawaran harga non-PKP (surat-penawaran-harga 1.0.3)

Tanggal: 2026-10-01 (Asia/Jakarta) · Penguji independen (bukan pembuat skill) · Uji pertama: [02-surat-penawaran-harga.md](02-surat-penawaran-harga.md)

OpenClaw lokal, model router Komunitech (`ninerouter/komunitech`, jawaban `claude-sonnet-5`). Home `sol-konsultan` direset dari skill terbaru (`reset-konsultan.sh`), sesi baru. Giliran 1 & 2 = pesan yang sama persis dengan uji pertama. Sisi SEBELUM memakai hasil uji pertama.

**Cacat yang diuji ulang:** teks WA menulis "Surat penawaran resmi (PDF) terlampir" padahal tidak ada file yang dibuat.

Catatan: di uji ulang, agent **tidak** menulis teks WA di giliran 2 (hanya menawarkannya). Agar perbaikan teks WA bisa dinilai, penguji menambah **giliran 3 tambahan** "iya bikinin versi WA nya" — giliran ini tidak ada di uji pertama dan dicatat terpisah.

## Pesan member giliran 1 (sama persis)

```
Bikinin surat penawaran harga ke CV Berkah Jaya Bakery dong. Jasa desain logo + brand guideline Rp 7,5 jt, desain template feed IG 12 desain @150rb, kasih diskon 10% dari total. Saya freelancer, belum PKP. DP 50%, penawaran berlaku 14 hari. Nama saya Dita Rahmawati.
```

## Pesan member giliran 2 (sama persis)

```
Kota Bandung, WA 0812-0000-1111. PIC nggak tahu. Rekening BCA 9876543210 a.n. Dita Rahmawati. Pengerjaan 14 hari kerja setelah DP. Sisanya pakai default aja, langsung jadiin.
```

## Balasan SESUDAH baru — giliran 1 (utuh)

_Alat: `read` · durasi 16 detik_

> Sebelum saya susun suratnya, boleh lengkapi 3 hal ini ya (biar surat terlihat profesional dan lengkap):
> 
> 1. Kontak kamu (WA dan/atau email) untuk dicantumkan di kop surat?
> 2. Nama & jabatan PIC di CV Berkah Jaya Bakery yang dituju?
> 3. Surat ini diterbitkan dari kota mana (buat tanggal & nomor surat)?
> 
> Kalau mau cepat, aku bisa pakai placeholder `[isi]` untuk yang belum ada — tinggal bilang "lanjut pakai placeholder aja".
## Balasan SESUDAH baru — giliran 2 (utuh)

_Alat: `exec, write` · durasi 46 detik · file dibuat: `SPH-001-Berkah-Jaya-Bakery.md` di workspace_

> Surat penawaran untuk CV Berkah Jaya Bakery sudah jadi dan tersimpan di `SPH-001-Berkah-Jaya-Bakery.md`.
> 
> **Rincian:**
> | Item | Qty | Harga Satuan | Jumlah |
> |---|---|---|---|
> | Jasa desain logo + brand guideline | 1 paket | Rp 7.500.000 | Rp 7.500.000 |
> | Desain template feed Instagram | 12 desain | Rp 150.000 | Rp 1.800.000 |
> 
> - Subtotal: Rp 9.300.000
> - Diskon 10%: −Rp 930.000
> - **Total: Rp 8.370.000** (Delapan Juta Tiga Ratus Tujuh Puluh Ribu Rupiah)
> - Tanpa PPN (kamu belum PKP)
> - DP 50% = Rp 4.185.000, sisanya Rp 4.185.000 sebelum file final diserahkan
> - Berlaku s.d. 15 Oktober 2026
> - Pengerjaan 14 hari kerja setelah DP
> 
> **Asumsi yang dipakai** (karena tidak disebutkan):
> - Nama PIC di CV Berkah Jaya Bakery ditulis `[Nama PIC]` — isi manual sebelum kirim, atau kabari aku namanya nanti biar aku update.
> - Ketentuan revisi memakai klausul standar (revisi besar di luar brief awal bisa kena biaya tambahan) — sesuaikan kalau beda kesepakatan.
> 
> Catatan: skill ini tidak membuat PDF. Cara convert cepat: buka file `.md` ini di Word/Google Docs → **File → Download/Save as PDF**.
> 
> Mau aku buatkan juga versi ringkas untuk WhatsApp?
### Isi file `SPH-001-Berkah-Jaya-Bakery.md` (utuh, dibuat agent)

```markdown
**DITA RAHMAWATI**
*Freelance Graphic & Brand Designer*
Bandung · WA 0812-0000-1111
---------------------------------------------
Nomor    : 001/SPH/DR/X/2026
Lampiran : -
Perihal  : Penawaran Harga Jasa Desain Logo, Brand Guideline & Template Feed Instagram

Bandung, 1 Oktober 2026

Kepada Yth.
[Nama PIC] – Pimpinan/Penanggung Jawab
CV Berkah Jaya Bakery
di tempat

Dengan hormat,
Sehubungan dengan kebutuhan CV Berkah Jaya Bakery akan identitas visual dan konten media sosial, kami mengajukan penawaran harga sebagai berikut.

| No | Uraian | Qty | Satuan | Harga Satuan | Diskon | Jumlah |
|---|---|---|---|---|---|---|
| 1 | Jasa desain logo + brand guideline | 1 | paket | Rp 7.500.000 | - | Rp 7.500.000 |
| 2 | Desain template feed Instagram | 12 | desain | Rp 150.000 | - | Rp 1.800.000 |

| | |
|---|---|
| Subtotal | Rp 9.300.000 |
| Diskon tambahan (10%) | −Rp 930.000 |
| **TOTAL** | **Rp 8.370.000** |

Terbilang: *Delapan Juta Tiga Ratus Tujuh Puluh Ribu Rupiah*

**Syarat & ketentuan**
1. Harga tidak dikenakan PPN (penyedia jasa bukan PKP).
2. Penawaran berlaku sampai dengan **15 Oktober 2026** (14 hari sejak tanggal surat).
3. Pembayaran: DP 50% saat PO sebesar **Rp 4.185.000**, pelunasan sebesar **Rp 4.185.000** dibayarkan sebelum file final diserahkan. Transfer ke rekening **BCA 9876543210 a.n. Dita Rahmawati**.
4. Pengerjaan: 14 hari kerja setelah DP diterima. File final diserahkan dalam format digital (siap pakai/cetak) sesuai kebutuhan.
5. Revisi mengikuti ketentuan yang disepakati saat briefing; jumlah revisi besar yang berlebihan di luar brief awal dapat dikenakan biaya tambahan.

Demikian penawaran ini kami sampaikan. Apabila CV Berkah Jaya Bakery berkenan melanjutkan, kami akan segera menyiapkan kontrak kerja/invoice DP setelah konfirmasi PO. Kami menunggu kabar baik dari Bapak/Ibu.

Hormat kami,


Dita Rahmawati
Freelance Graphic & Brand Designer
```

## Giliran 3 TAMBAHAN (penguji, bukan bagian uji pertama)

Pesan: `iya bikinin versi WA nya` · _Alat: tidak ada · durasi 12 detik_

> Berikut versi WhatsApp-nya:
> 
> ```
> Selamat siang 🙏
> Berikut penawaran harga dari Dita Rahmawati (Freelance Graphic & Brand Designer) untuk CV Berkah Jaya Bakery:
> • Jasa desain logo + brand guideline – 1 paket × Rp 7.500.000
> • Desain template feed Instagram – 12 desain × Rp 150.000
> Diskon 10% dari total.
> Total: *Rp 8.370.000* (belum kena PPN)
> Berlaku s.d. 15 Oktober 2026.
> Pembayaran: DP 50% (Rp 4.185.000) saat PO, sisanya Rp 4.185.000 sebelum file final diserahkan, ke BCA 9876543210 a.n. Dita Rahmawati.
> Pengerjaan 14 hari kerja setelah DP masuk.
> Surat penawaran resminya menyusul/bisa saya kirimkan bila diperlukan ya.
> Kalau ada yang mau disesuaikan, kabari saja 🙏
> ```
> 
> Siap dikirim langsung. Mau sekaligus aku lampirkan file surat lengkapnya (`SPH-001-Berkah-Jaya-Bakery.md`) kalau nanti kamu kirim lewat sini, atau ini cukup teks WA-nya saja?
## Verifikasi independen (Python)

| Pos | Benar | Uji ulang |
|---|---|---|
| Subtotal 7.500.000 + 12 × 150.000 | 9.300.000 | ✅ |
| Diskon 10% | 930.000 | ✅ |
| Total | 8.370.000 | ✅ (tabel = ringkasan = terbilang = WA) |
| DP / pelunasan | 4.185.000 / 4.185.000 | ✅ |
| Berlaku 14 hari | s.d. 15 Okt 2026 | ✅ |

## Penilaian

- **Cacat "PDF terlampir": HILANG — ya.** Giliran 2: *"Catatan: skill ini tidak membuat PDF. Cara convert cepat: buka file `.md` ini di Word/Google Docs → File → Download/Save as PDF."* Teks WA (giliran 3): *"Surat penawaran resminya menyusul/bisa saya kirimkan bila diperlukan ya."* — tidak lagi mengklaim lampiran yang tidak ada. Agent juga bertanya apakah file surat mau dilampirkan.
- **Regresi baru (nyata):**
  1. **Format keluaran tidak lengkap di giliran 2.** SKILL.md mewajibkan dua bagian: (A) surat lengkap, (B) teks WA. Agent hanya menyimpan surat ke file `.md` di workspace dan di chat memberi ringkasan + nama file; teks WA baru dibuat setelah diminta. Member di Telegram **tidak bisa membuka file workspace** dan tidak melihat isi surat di chat. Uji pertama menampilkan surat utuh + WA di chat. Ini mundur dari sisi "siap pakai".
  2. **"[Nama PIC]" tetap muncul** padahal member sudah menjawab "PIC nggak tahu" (uji pertama menulis "Pimpinan CV Berkah Jaya Bakery" — benar). Surat kini bertuliskan "[Nama PIC] – Pimpinan/Penanggung Jawab" dan member diminta mengisi manual.
  3. **Teks WA "(belum kena PPN)"** — frasa ini menyiratkan PPN bisa ditambahkan nanti; surat sendiri benar ("tidak dikenakan PPN (penyedia jasa bukan PKP)"). Di uji pertama, kesalahan serupa ("belum termasuk PPN") adalah alasan pengurangan nilai sisi SEBELUM.
  4. Kecil: jabatan "Freelance Graphic & Brand Designer" dan "pelunasan sebelum file final diserahkan" tidak disebut member (default wajar, tetapi tidak dicantumkan di daftar asumsi).
- Positif: giliran 1 tetap bertanya sekali dengan opsi placeholder; angka benar; tidak memasang paket PDF; file siap cetak benar-benar dibuat.

| | Sesudah (lama) | Sesudah (baru) |
|---|---|---|
| Skor | 8 | **7,5** |

Alasan: cacat yang dilaporkan tertutup, tetapi muncul tiga regresi yang membuat hasil kurang siap pakai bagi member Telegram (surat tidak tampil di chat, WA baru setelah diminta) dan satu kalimat PPN yang kurang tepat. **Belum lulus** sebagai perbaikan bersih.
