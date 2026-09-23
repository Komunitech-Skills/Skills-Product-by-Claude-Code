# Template SP1, SP2, SP3 & Berita Acara Klarifikasi

Ganti semua `[...]`. Nomor surat contoh: `001/SP-1/[SINGKATAN-USAHA]/[bulan Romawi]/[tahun]`.

---
## 1. SP1 (Surat Peringatan Pertama)
```
[NAMA USAHA]
[Alamat lengkap] | Telp/WA [nomor] | [email]
________________________________________________________________

SURAT PERINGATAN PERTAMA (SP-1)
Nomor: [nomor]

Yang bertanda tangan di bawah ini:
Nama     : [nama pemberi]
Jabatan  : [jabatan]
dengan ini memberikan Surat Peringatan Pertama kepada:
Nama     : [nama karyawan]
Jabatan  : [jabatan]
Bagian   : [bagian/divisi]
NIK Karyawan (jika ada): [nomor induk karyawan]

A. Pelanggaran
Berdasarkan [bukti: rekap absensi/laporan/CCTV], Saudara/Saudari [fakta: apa, kapan, berapa kali].

B. Dasar
Perbuatan tersebut melanggar [Pasal .. Peraturan Perusahaan / Perjanjian Kerja / Tata Tertib Karyawan]
yang berbunyi "[kutipan singkat]". Saudara/Saudari telah didengar penjelasannya pada [tanggal]
sebagaimana tercatat dalam Berita Acara Klarifikasi terlampir.

C. Harapan perbaikan
Kami meminta Saudara/Saudari untuk:
1. [perilaku terukur]
2. [perilaku terukur]
Perusahaan bersedia [pembinaan/pendampingan/pelatihan ulang, bila ada].
Apabila selama masa berlaku surat ini Saudara/Saudari kembali melakukan pelanggaran, perusahaan
dapat memberikan Surat Peringatan Kedua sesuai ketentuan yang berlaku.

D. Masa berlaku
[kalimat_surat dari script masa_berlaku.py]

Demikian surat peringatan ini dibuat untuk diperhatikan dan menjadi bahan perbaikan.

[Kota], [tanggal]

Pemberi peringatan,                       Diterima oleh,


[Nama]                                     [Nama karyawan]
[Jabatan]                                  Tanggal terima: ______________

Saksi,


[Nama, Jabatan]

Lampiran: Berita Acara Klarifikasi; [bukti]
Tembusan: 1. Arsip personalia  2. [Atasan langsung]
```

## 2. Perbedaan untuk SP2
- Judul: `SURAT PERINGATAN KEDUA (SP-2)`.
- Tambahkan di bagian A: "Pelanggaran ini terjadi pada saat Surat Peringatan Pertama Nomor [..] tanggal [..] masih berlaku (berlaku s.d. [..])."
- Bagian C: "...perusahaan dapat memberikan Surat Peringatan Ketiga (terakhir) sesuai ketentuan yang berlaku."

## 3. Perbedaan untuk SP3 (peringatan terakhir)
- Judul: `SURAT PERINGATAN KETIGA (SP-3) — PERINGATAN TERAKHIR`.
- Bagian A menyebut SP1 dan SP2 beserta nomor & tanggal, serta bahwa SP2 masih berlaku.
- Bagian C: "Surat ini merupakan peringatan terakhir. Apabila Saudara/Saudari kembali melakukan pelanggaran selama masa berlaku surat ini, perusahaan dapat mengambil langkah lebih lanjut sesuai peraturan perundang-undangan dan Peraturan Perusahaan."
- **Catatan proses wajib:** "Setelah SP3, langkah berikutnya menyangkut PHK. Konsultasikan ke ahli hukum ketenagakerjaan/Disnaker sebelum bertindak."

---
## 4. Berita Acara Klarifikasi
```
BERITA ACARA KLARIFIKASI
Nomor: [nomor]

Pada hari [hari], tanggal [tanggal], pukul [jam], bertempat di [lokasi], telah dilakukan klarifikasi:
Pihak perusahaan : [nama, jabatan]
Karyawan         : [nama, jabatan]
Saksi            : [nama, jabatan]

Pokok permasalahan:
[fakta pelanggaran + bukti yang ditunjukkan]

Penjelasan karyawan:
[tulis apa adanya, dengan kata-kata karyawan]

Tanggapan/kesepakatan:
[mis. karyawan mengakui / tidak mengakui; komitmen perbaikan; tindak lanjut]

Demikian berita acara ini dibuat dengan sebenarnya dan dibaca ulang di hadapan para pihak.

Pihak perusahaan,          Karyawan,               Saksi,


[Nama]                     [Nama]                  [Nama]
```

---
## 5. Contoh kasus lokal (acuan penulisan fakta)
1. **Toko bangunan, Sidoarjo — kasir terlambat 6x/bulan** → SP1 (sudah 2x teguran lisan).
2. **Online shop skincare, Tangerang — staf packing salah kirim 5 paket dalam 2 minggu saat SP1 (terbit 14 Juli 2026) masih berlaku** → cek script `--terbit 14-07-2026 --cek <tanggal pelanggaran>` → masih aktif → SP2. Lampirkan daftar nomor pesanan & komplain pembeli.
3. **Warung makan, Makassar — pramusaji membentak pelanggan, ada 2 saksi & video** → SP1 dengan kutipan keterangan saksi; tawarkan pelatihan layanan.
4. **Bengkel motor, Medan — mekanik merokok dekat tangki bensin, SP1 terbit 2 Januari 2026, pelanggaran baru 20 September 2026** → script menunjukkan SP1 sudah berakhir (1 Juli 2026) → kembali SP1, kecuali PP bengkel mengatur pelanggaran K3 sebagai pelanggaran berat.
