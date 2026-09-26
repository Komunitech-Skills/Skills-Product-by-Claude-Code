# Template struktur SOP & FAQ untuk basis pengetahuan SiYuan

Template asli Komunitech, dipakai sebagai patokan saat agent membuat dokumen baru lewat perintah
`buat`. Sesuaikan isinya dengan usaha pengguna - jangan mengarang angka/kebijakan yang belum
dikonfirmasi pengguna (lihat `SKILL.md` §Batasan).

> **Penting (temuan uji nyata):** SiYuan otomatis menambahkan judul dokumen (segmen terakhir
> `--path`) sebagai heading `# <Judul>` paling atas. **Jangan** menulis ulang baris `# <Judul>` yang
> sama di awal isi Markdown, karena akan tampil dua kali. Langsung mulai dari isi (lihat contoh di
> bawah - tidak ada baris `#` pertama).

## 1. Struktur dokumen SOP (path disarankan: `/SOP/<Nama Prosedur>`)
```markdown
**Tujuan:** <satu kalimat, hasil akhir yang diinginkan>
**Berlaku untuk:** <peran, mis. "kasir", "admin gudang">
**Versi:** 1.0 - <tanggal>

## Langkah
1. <langkah pendek, kalimat perintah>
2. <langkah pendek>
3. ...

## Checklist harian
- [ ] <item checklist siap cetak/centang>
- [ ] <item checklist>

## Kalau terjadi masalah
- <situasi> → <tindakan>
```
Untuk SOP yang lebih lengkap (indikator keberhasilan, penanggung jawab, riwayat revisi), arahkan
pengguna ke skill **`sop-writer`** lalu simpan hasilnya ke SiYuan lewat `siyuan-sop` (lihat
"Serah Terima" di `SKILL.md`).

## 2. Struktur dokumen FAQ toko (path disarankan: `/FAQ/<Topik>`)
```markdown
**P: <pertanyaan pelanggan yang sering muncul>**
J: <jawaban singkat, siap salin-tempel ke chat>

**P: <pertanyaan lain>**
J: <jawaban>
```
Kelompok topik FAQ yang lazim untuk toko/klinik: Produk & Harga, Stok, Jam Buka, Ongkos Kirim &
Pengiriman, Cara Bayar, Kebijakan Retur/Tukar, Garansi, Cara Pesan.

## 3. Struktur notulen rapat (path disarankan: `/Notulen/<Tanggal> - <Topik>`)
Simpan **hasil jadi** dari skill `notulen-rapat` apa adanya (jangan diringkas ulang), dengan judul
dokumen memuat tanggal supaya mudah dicari lewat `cari` dan diurutkan lewat `lama`.

## 4. Konvensi penamaan path (disiplin agar basis pengetahuan tetap rapi & bisa dicari)
- Satu buku catatan (notebook) per usaha/klinik cukup untuk UMKM; dalam satu buku catatan, pisahkan
  dengan folder-tingkat: `/SOP/...`, `/FAQ/...`, `/Notulen/...`, `/Kebijakan/...`.
- Judul dokumen singkat dan spesifik ("Retur Barang Rusak", bukan "SOP 1").
- Boleh memakai emoji di judul untuk kemudahan visual (mis. "🕐 Jam Buka") - skill ini sudah diuji
  dengan judul/isi Unicode dan emoji.

## 5. Contoh isi FAQ toko online (dipakai di `examples/`, path `/FAQ/Ongkos Kirim`)
```markdown
**P: Berapa ongkirnya?**
J: Ongkir dihitung otomatis oleh sistem checkout sesuai berat & kota tujuan.

**P: Apakah bisa COD?**
J: Bisa untuk area yang didukung kurir (dicek otomatis saat checkout).
```

## 6. Rangkaian ke skill CS (`agen-cs-toko` / `balas-chat-cs`)
Setelah basis pengetahuan terisi, jalankan `siyuan.py ekspor-basis --notebook <ID>` untuk
menggabungkan seluruh SOP/FAQ satu buku catatan menjadi satu file Markdown. File itu lalu dipakai
sebagai "basis pengetahuan lokal" pada skill `agen-cs-toko` (lihat `SKILL.md` §Serah Terima ke
skill lain), sehingga draf balasan CS selalu berdasar isi SiYuan, bukan karangan model.
