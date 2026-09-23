# Atribusi

Skill `ekstrak-nota-faktur` **diadaptasi dan diubah secara substansial** dari skill
**invoice-extract-id** karya **Manaira Labs**:

- Sumber: https://github.com/manairalabs/bicara-skills (folder `skills/invoice-extract-id/`)
- Versi yang ditinjau: v0.1.0 (commit awal 2026-04-17), ditinjau 2026-09-23
- Lisensi sumber: MIT (teks lengkap di bawah)

Adaptasi oleh Komunitech (komunitech.com). Penggunaan versi adaptasi ini tunduk pada `LISENSI.txt`
yang disertakan dalam paket pembelian, **tanpa mengurangi** ketentuan lisensi MIT di bawah untuk bagian
yang berasal dari karya asli.

## Yang diambil dari sumber
- Gagasan skill: mengekstrak data nota, kuitansi, invoice, faktur pajak, dan bukti transfer Indonesia ke data terstruktur.
- Gagasan kolom data (penjual/pembeli, NPWP, NITKU, item, DPP, PPN, PPh, meterai, total, terbilang, pembayaran) dan tiga cek konsistensi angka (item vs DPP, PPN vs DPP, total).
- Beberapa jebakan umum: format angka Indonesia (titik ribuan, koma desimal), NPWP "-" dianggap kosong, jangan mengarang item, jangan tertukar penjual dan pembeli.

## Yang diubah / ditambahkan oleh Komunitech
1. **Aturan pajak diperbarui ke era Coretax (per 23 September 2026):** PPN 12% × DPP nilai lain 11/12 untuk barang/jasa biasa (PMK 131/2024), 12% penuh hanya untuk barang mewah, tarif lama menurut tanggal dokumen. Sumber menghitung PPN 12% × DPP penuh untuk barang biasa, yang kini keliru.
2. **Format identitas diperbarui:** nomor seri faktur Coretax 17 digit, NITKU 22 digit, NPWP 16 digit (15 digit sebagai format lama). Sumber memakai format e-Faktur lama 16 digit dan menolak NPWP selain 15/16 digit; versi ini hanya memberi peringatan dan menandai format sebagai BELUM TERVERIFIKASI.
3. **Script Python baru** `scripts/cek_nota.py` (ditulis dari nol, library standar): cek per item, subtotal, DPP, DPP nilai lain, PPN, total (termasuk PPh dipotong dan meterai), membaca terbilang jadi angka, cek format NPWP/NITKU/nomor seri faktur, deteksi dokumen dobel, pengingat meterai, dan ekspor CSV (`;`, `,`, tab) serta JSON.
4. **Rekap banyak dokumen** jadi rekap pengeluaran per kategori, per penjual, dan per bulan.
5. **Penanganan foto buram:** pembedaan `null` (tidak ada) dan `TIDAK_TERBACA` (ada tapi tidak terbaca). Sumber justru meminta kolom wajib tetap diisi walau kurang yakin; versi ini melarang menebak.
6. **Skema data ditulis ulang** dalam Bahasa Indonesia, dengan tambahan: struk harga termasuk PPN, jenis PPN (umum/mewah/dibebaskan/lainnya), biaya lain, potongan lain, kategori, penanda ikut rekap.
7. **Output untuk pembeli awam:** tabel ringkas, daftar "yang perlu Anda cek" dalam bahasa sehari-hari, CSV siap tempel ke Excel, JSON opsional.
8. **Contoh lokal baru** (nota warung tulisan tangan, struk minimarket, faktur Coretax, invoice jasa dengan PPh 23, kuitansi tukang, bukti transfer). Contoh faktur sumber tidak dipakai.
9. Dasar aturan + sumber di `references/regulasi.md`, disclaimer pajak, arahan ke DJP/konsultan, README untuk pembeli.
10. Dihapus: field frontmatter `license` dan `version`, dan rujukan ke paket npm `@manairalabs/id-locale`.

Seluruh teks SKILL.md, README, referensi, template, dan script ditulis ulang dalam Bahasa Indonesia; tidak ada bagian sumber yang disalin utuh.

## Teks lisensi asli (MIT)

Disalin persis dari https://raw.githubusercontent.com/manairalabs/bicara-skills/main/LICENSE:

```
MIT License

Copyright (c) 2026 Manaira Labs

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
