# Contoh 01 – Surat kuasa pengambilan BPKB di leasing

## Skenario
S1, permintaan normal. Pemilik CV di Semarang memberi kuasa kepada staf admin untuk mengambil BPKB mobil operasional yang sudah lunas di kantor leasing. Pengguna menyebut nomor urut surat. Skill harus memakai kerangka surat kuasa sederhana, membuat nomor dan tanggal dengan script, membatasi kewenangan, dan memberi catatan meterai. Semua nama, NIK, dan pelat nomor fiktif.

## Input pengguna
```
Tolong buatin surat kuasa. Saya Hendra Gunawan, direktur CV Sinar Laras Abadi, Jl. Contoh Industri No. 8 Semarang. Saya kasih kuasa ke staf admin saya, Sri Wahyuni, buat ambil BPKB mobil kantor Toyota Avanza H 1234 XY yang sudah lunas di PT Contoh Finance cabang Semarang. Ini surat keluar ke-18 bulan ini.
```

## Proses (dijalankan agent)
```
$ python3 scripts/nomor_tanggal.py --tanggal 23-09-2026 --kota Semarang --urut 18 --kode KSA --instansi "CV-SLA" --format teks
Tanggal surat     : 23 September 2026
Hari              : Rabu
Bulan Romawi      : IX
Baris tanggal     : Semarang, 23 September 2026
Nomor surat       : 018/KSA/CV-SLA/IX/2026
```

## Output

```
CV SINAR LARAS ABADI
Jl. Contoh Industri No. 8, Semarang | Telp/WA [nomor] | Email [email]
________________________________________________________________

SURAT KUASA
Nomor: 018/KSA/CV-SLA/IX/2026

Yang bertanda tangan di bawah ini:
Nama              : Hendra Gunawan
Nomor identitas   : [NIK KTP pemberi kuasa]
Jabatan           : Direktur CV Sinar Laras Abadi
Alamat            : Jl. Contoh Industri No. 8, Semarang
selanjutnya disebut Pemberi Kuasa.

Dengan ini memberikan kuasa kepada:
Nama              : Sri Wahyuni
Nomor identitas   : [NIK KTP penerima kuasa]
Jabatan           : Staf Admin CV Sinar Laras Abadi
Alamat            : [alamat penerima kuasa]
selanjutnya disebut Penerima Kuasa.

KHUSUS
Untuk dan atas nama Pemberi Kuasa mengambil dokumen Buku Pemilik Kendaraan Bermotor (BPKB)
kendaraan Toyota Avanza Nomor Polisi H 1234 XY di kantor PT Contoh Finance cabang Semarang,
termasuk menandatangani tanda terima yang diperlukan untuk keperluan tersebut.

Surat kuasa ini berlaku sejak ditandatangani sampai dengan urusan pengambilan BPKB tersebut
selesai dan tidak dapat dialihkan kepada pihak lain.

Semarang, 23 September 2026

Penerima Kuasa,                      Pemberi Kuasa,
                                     [meterai Rp10.000]


Sri Wahyuni                          Hendra Gunawan
                                     Direktur
```

**Catatan untuk kamu** (tidak dicetak):
- **Isi dulu:** NIK kedua pihak, alamat Sri Wahyuni, dan telepon/email di kop.
- **Meterai:** tempel meterai Rp10.000 di atas nama Pemberi Kuasa, dan tanda tangan sebagian mengenai meterai. Meterai bukan syarat sah surat, tetapi leasing biasanya memintanya karena surat kuasa dipakai sebagai bukti.
- **Bawa saat pengambilan:** fotokopi KTP kedua pihak, surat kuasa asli, dan cap/stempel CV bila ada (di sisi kiri tanda tangan Pemberi Kuasa). Banyak leasing punya **format surat kuasa sendiri**. Tanyakan dulu ke PT Contoh Finance agar tidak bolak-balik.
- **Nomor rangka & nomor mesin:** jika leasing meminta, tambahkan nomor rangka dan nomor mesin kendaraan di bagian KHUSUS.
- Nomor surat dan tanggal dibuat dengan script (IX = September).

Mau dibuatkan versi tanpa kop (kuasa pribadi), atau surat pengantar untuk leasing sekalian?

## Catatan penguji
- **Script dijalankan sungguhan:** `018/KSA/CV-SLA/IX/2026` dan "Rabu, 23 September 2026". Nomor urut 18 menjadi 018, kode KSA dipakai sesuai tabel kode (bukan "SKU", sengaja dibedakan dari Surat Keterangan Usaha). **Verifikasi independen:** 23 September 2026 = Rabu (dicek `datetime`), September = IX.
- **Bagus:** kewenangan terbatas dan jelas (hanya ambil BPKB + tanda terima), tidak dapat dialihkan, ada masa berlaku. Catatan meterai sesuai *Batasan* (tidak mengklaim "tidak sah tanpa meterai"). NIK tidak dikarang.
- **Bagus:** EYD V: "Nomor Polisi", "Rp10.000" tanpa spasi, tanggal tanpa nol.
- **Kurang (ringan):** kerangka surat kuasa di `references/template-surat.md` tidak punya baris jabatan di bawah nama Pemberi Kuasa. Di sini ditambahkan agar jelas bertindak atas nama CV.
