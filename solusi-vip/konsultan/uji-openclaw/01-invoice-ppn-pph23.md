# 01 — Invoice jasa konsultan PKP dengan PPN & PPh 23

Tanggal uji: 2026-10-01 (Asia/Jakarta). OpenClaw lokal (`openclaw agent --local`), model router Komunitech (`ninerouter/komunitech`, sama dengan bot). SEBELUM = home `kosong-konsultan` (tanpa skill). SESUDAH = home `sol-konsultan` (paket skill solusi konsultan terpasang). Pesan identik di kedua sisi.

## Pesan member (giliran 1)

```
Halo, tolong bikinin invoice buat PT Sinar Abadi Logistik ya. Jasa konsultasi pajak bulan September Rp 8.750.000, sama pendampingan pemeriksaan pajak 2 hari @ Rp 2.375.000. Saya sudah PKP (CV Arta Konsulindo). Mereka biasanya potong PPh 23. Jatuh tempo 14 hari. Rekening BCA 1234567890 a.n. CV Arta Konsulindo.
```

## SEBELUM (tanpa skill)

### Giliran 1 — tools: ['tool_search', 'ls', 'read', 'memory_search', 'tool_call', 'exec', 'process', 'write']; lampiran file ke chat: ya (invoice_PT-Sinar-Abadi-Logistik_INV-2026-10-001.txt); durasi 110 dtk

````markdown
Invoice sudah saya buatkan. Ringkasannya:

**INV/2026/10/001** — PT Sinar Abadi Logistik, tanggal 01 Okt 2026, jatuh tempo 15 Okt 2026 (14 hari).

| Item | Jumlah |
|---|---|
| Jasa Konsultasi Pajak (Sep 2026) | Rp 8.750.000 |
| Pendampingan Pemeriksaan Pajak 2 hari @ Rp 2.375.000 | Rp 4.750.000 |
| **DPP** | **Rp 13.500.000** |
| PPN 11% | Rp 1.485.000 |
| **Total Tagihan** | **Rp 14.985.000** |
| Dipotong PPh 23 (2% x DPP) | − Rp 270.000 |
| **Nett diterima** | **Rp 14.715.000** |

Karena CV Arta Konsulindo sudah PKP, saya tambahkan PPN 11%. Untuk PPh 23, saya pakai tarif 2% dari DPP (tarif standar jasa konsultasi/profesional) dan saya catat di invoice sebagai potongan + minta mereka kirim bukti potong.

Pembayaran: BCA 1234567890 a.n. CV Arta Konsulindo — sudah saya cantumkan.

File tersimpan di workspace:

Ada 3 hal yang masih kosong dan perlu kamu lengkapi sebelum dikirim ke klien:
1. NPWP CV Arta Konsulindo (buat header invoice)
2. Alamat CV Arta Konsulindo
3. NPWP & alamat PT Sinar Abadi Logistik (dibutuhkan klien untuk terbitkan bukti potong PPh 23)

Mau saya lengkapi kalau kamu kirim datanya, atau ini langsung dipakai sementara kolomnya dibiarkan "mohon dilengkapi"?
````

**Jejak tool (sebelum):** tool_search, memory_search, `ls`, baca `catatan-kerja.csv` (tidak relevan), **`find / -iname "*invoice*"` ke seluruh disk** (dihentikan manual oleh agent), tulis file `.txt`. Tidak ada skill.

## SESUDAH (dengan paket skill)

### Giliran 1 — tools: ['read', 'exec', 'write']; lampiran file ke chat: tidak; durasi 77 dtk

````markdown
Invoice sudah jadi. Ini bagian yang dikirim ke PT Sinar Abadi Logistik:

# INVOICE

**No.:** INV/2026/10/0001
**Tanggal:** 1 Oktober 2026
**Jatuh tempo:** 15 Oktober 2026
**Status:** BELUM DIBAYAR

**Dari:** CV Arta Konsulindo
**Kepada:** PT Sinar Abadi Logistik

| No | Deskripsi | Qty | Harga | Jumlah |
|---:|---|---:|---:|---:|
| 1 | Jasa konsultasi pajak bulan September 2026 | 1 paket | Rp 8.750.000 | Rp 8.750.000 |
| 2 | Pendampingan pemeriksaan pajak | 2 hari | Rp 2.375.000 | Rp 4.750.000 |

- Subtotal / DPP: Rp 13.500.000
- DPP nilai lain (11/12): Rp 12.375.000
- PPN 12%: Rp 1.485.000
- **TOTAL: Rp 14.985.000**

Terbilang: *Empat Belas Juta Sembilan Ratus Delapan Puluh Lima Ribu Rupiah*

**Pembayaran ke:** BCA 1234567890 a.n. CV Arta Konsulindo

**Catatan:** Objek PPh Pasal 23 atas jasa. Mohon dipotong sesuai ketentuan dan bukti potong dikirimkan setelah pembayaran.

[isi kota], 1 Oktober 2026
**[isi nama penanda tangan]**
CV Arta Konsulindo

File HTML siap cetak: `invoice-sinar-abadi.html` (buka di browser → Print → Save as PDF).

Catatan buat Anda (bukan untuk dikirim ke klien):
1. **Kota & nama penanda tangan** masih kosong (`[isi ...]`) — belum Anda sebutkan, jadi tidak saya karang. Kabari dan saya update.
2. **Nomor invoice** mulai dari `INV/2026/10/0001` karena belum ada info nomor terakhir CV Arta Konsulindo. Kalau ada nomor sebelumnya, beri tahu biar berurutan.
3. **Meterai**: tidak wajib untuk invoice ini (belum ada penerimaan uang). Nanti kalau sudah dibayar lunas > Rp5 juta, kuitansi pelunasannya wajib meterai Rp10.000.
4. **PPh 23**: saya cantumkan sebagai catatan di invoice (nilai invoice tetap Rp14.985.000, PPh 23 dipotong pembeli saat bayar, bukan dikurangi dari tagihan ini) — pastikan NPWP CV Arta Konsulindo aktif agar tarif potong 2%, bukan 4% (tanpa NPWP).
5. Invoice ini **bukan faktur pajak** — faktur pajak keluaran tetap harus dibuat terpisah di Coretax.
````

**Jejak tool (sesudah):** Baca `~/.openclaw/skills/buat-invoice/SKILL.md`, `references/format-input.md`, `templates/contoh-invoice.json`, `references/regulasi.md`; `grep pph` di script (hasil: script tidak mendukung PPh 23); tulis JSON; jalankan `scripts/buat_invoice.py --html`. **Skill `buat-invoice` terpakai, angka dari script.**

## Verifikasi independen

Dihitung ulang dengan Python (`fractions`, PPN dibulatkan ke bawah):

| Pos | Benar | SEBELUM | SESUDAH |
|---|---|---|---|
| Subtotal (8.750.000 + 2 × 2.375.000) | 13.500.000 | 13.500.000 ✔ | 13.500.000 ✔ |
| DPP nilai lain 11/12 (PMK 131/2024) | 12.375.000 | tidak ditampilkan; subtotal diberi label "DPP" ✘ | 12.375.000 ✔ |
| PPN 12% × DPP nilai lain | 1.485.000 | 1.485.000, tapi dilabeli "PPN 11%" ✘ (tidak sesuai format PMK 131/2024) | 1.485.000 ✔ |
| Total invoice | 14.985.000 | 14.985.000 ✔ | 14.985.000 ✔ |
| PPh 23 2% × 13.500.000 (bruto tanpa PPN) | 270.000 | 270.000 ✔ | **tidak dihitung** (hanya catatan "mohon dipotong") |
| Neto yang akan ditransfer klien | 14.715.000 | 14.715.000 ✔ | **tidak ditampilkan** |
| Jatuh tempo (+14 hari) | 15 Okt 2026 | ✔ | ✔ |

Catatan aturan: meterai — SESUDAH benar bahwa invoice (bukan tanda terima uang) tidak wajib meterai; kuitansi pelunasan > Rp5 juta wajib Rp10.000 (UU 10/2020). SESUDAH juga mengingatkan invoice ≠ faktur pajak (faktur dibuat di Coretax) dan tarif PPh 23 2% hanya bila penerima ber-NPWP (tanpa NPWP 100% lebih tinggi = 4%) — keduanya benar. SEBELUM tidak menyebut faktur pajak.

## Nilai

| Aspek | SEBELUM | SESUDAH |
|---|---|---|
| Ketepatan angka | Benar semua, label "PPN 11%" & "DPP" keliru | Benar semua; PPh 23 & neto tidak dihitung |
| Siap pakai | File .txt dikirim sebagai lampiran chat; NPWP/alamat diberi placeholder | Markdown + HTML siap cetak, terbilang; **file HTML tidak dikirim ke chat** (hanya disebut path) |
| Kepatuhan aturan ID | Format PPN pra-2025 | PMK 131/2024, faktur Coretax, meterai, NPWP/PPh 23 4% |
| Keamanan/privasi | `find /` menyisir seluruh disk komputer member | Hanya membaca folder skill & workspace |
| Kejelasan | Ringkas, ada neto | Jelas, catatan terpisah untuk member vs klien |
| **Total (1–10)** | **7** | **8** |

SESUDAH lebih patuh aturan (DPP nilai lain eksplisit, terbilang, HTML cetak, catatan faktur pajak/meterai) dan tidak mengarang data. Namun pertanyaan inti member soal PPh 23 justru lebih baik dijawab SEBELUM (potongan Rp270.000 dan neto Rp14.715.000 dihitung). Skill `buat-invoice` sama sekali tidak menangani PPh 23 — celah nyata untuk paket konsultan. SEBELUM dikurangi karena label PPN 11% (format lama) dan pencarian `find /` ke seluruh disk.
