# Pembanding A/B – Permintaan S1 dengan dan tanpa skill

**Permintaan yang sama (S1):**
```
Tolong buatin surat kuasa. Saya Hendra Gunawan, direktur CV Sinar Laras Abadi, Jl. Contoh Industri No. 8 Semarang. Saya kasih kuasa ke staf admin saya, Sri Wahyuni, buat ambil BPKB mobil kantor Toyota Avanza H 1234 XY yang sudah lunas di PT Contoh Finance cabang Semarang. Ini surat keluar ke-18 bulan ini.
```

## A. Tanpa skill (AI agent biasa, tanpa membaca skill apa pun)

> **SURAT KUASA**
> No: 18/SK/IX/2026
>
> Yang bertanda tangan di bawah ini:
> Nama : Hendra Gunawan
> Jabatan : Direktur CV Sinar Laras Abadi
> Alamat : Jl. Contoh Industri No. 8 Semarang
>
> Dengan ini memberikan kuasa kepada:
> Nama : Sri Wahyuni
> Jabatan : Staf Admin
>
> Untuk mengurus dan mengambil BPKB kendaraan Toyota Avanza dengan nomor polisi H 1234 XY di PT Contoh Finance cabang Semarang.
>
> Demikian surat kuasa ini dibuat dengan sebenar-benarnya untuk dapat dipergunakan sebagaimana mestinya.
>
> Semarang, 23 September 2026
>
> | Penerima Kuasa | Pemberi Kuasa |
> |---|---|
> | | Materai 10.000 |
> | (Sri Wahyuni) | (Hendra Gunawan) |

## B. Dengan skill `surat-resmi`
Output lengkap ada di `01-surat-kuasa-ambil-bpkb.md`. Ringkasnya:
- Kop CV, nomor dari script `018/KSA/CV-SLA/IX/2026`, dan baris tanggal EYD V.
- Identitas lengkap kedua pihak, termasuk kolom NIK dan alamat (placeholder, tidak dikarang).
- Bagian **KHUSUS** dengan kewenangan terbatas: hanya mengambil BPKB dan menandatangani tanda terima. Kuasa berlaku sampai urusan selesai dan tidak dapat dialihkan.
- Blok tanda tangan siap cetak, dengan posisi meterai Rp10.000.
- "Catatan untuk kamu": placeholder yang harus diisi, cara menempel meterai yang benar (tanpa klaim "tidak sah tanpa meterai"), dokumen yang harus dibawa, saran menanyakan format leasing, dan nomor rangka/mesin.

## Penilaian singkat
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Nomor surat | `18/SK/IX/2026`: tidak 3 digit, tanpa kode instansi, dan kode "SK" bentrok dengan Surat Keterangan. | `018/KSA/CV-SLA/IX/2026` dari script, dengan kode khusus surat kuasa. |
| Identitas | Tanpa NIK dan alamat penerima. Leasing biasanya menolak surat seperti ini. | Kolom NIK dan alamat lengkap. |
| Batas kewenangan | "Mengurus dan mengambil" (terlalu luas), tanpa masa berlaku, bisa dialihkan. | Terbatas, ada masa berlaku, tidak dapat dialihkan. |
| Ejaan | "Materai" (tidak baku), "10.000" tanpa Rp, nama dalam kurung. | "meterai Rp10.000" (EYD V), nama tanpa kurung. |
| Panduan praktis | Tidak ada. | Placeholder, meterai, dokumen bawaan, format leasing. |
| Kop | Tidak ada. | Ada. |

**Kesimpulan: hasil dengan skill lebih baik secara jelas, walau selisihnya tidak sebesar skill lain.** Surat tanpa skill "jadi", tapi berisiko ditolak leasing (tanpa NIK/alamat), kewenangannya terlalu luas, dan ejaannya tidak baku. Skill menghasilkan surat yang siap cetak dan siap diterima instansi, plus panduan yang mencegah pengguna awam bolak-balik. Nilai tambah script (hari/bulan Romawi) lebih terasa pada surat undangan (lihat contoh 02 dan 03).
