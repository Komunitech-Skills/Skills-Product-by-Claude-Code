# Uji 08 (normal 3) - Laundry kiloan: ekspor WA iPhone 2 bulan + tema.json
Penguji independen, 2026-09-29. Data fiktif: 23 baris ekspor iOS (`[02/08/26 08.15.22] Nama: ...`), pesan sistem terenkripsi, "pesan ini
dihapus", pengirim berisi nomor HP ("Andre 0857-...") dan nama kantor ("Sinta (kantor BRI Cabang Depok)"), alamat "Gg. Kenanga 3", email.

Perintah: `--daftar-pengirim` lalu
`python3 scripts/olah_masukan.py chat-ios.txt=WhatsApp --staf "Laundry Bersih Kilat" --tema tema.json --simpan-anonim anon.csv`
(tema.json penguji: `bau_apek` dampak 4, `kerusakan` [luntur/hilang/kancing/sobek/noda] dampak 5).

## Yang berjalan baik
- Format iOS, pesan sistem, pesan dihapus, dan pesan staf dilewati dengan benar (sistem/media 2, staf 2); 19 masukan.
- Penyamaran: nama pengirim, nomor di nama pengirim, nama kantor, email, alamat gang -> tidak ada yang bocor ke CSV anonim.
- Tren 2026-08 (8) vs 2026-09 (11) dihitung benar; contoh pengiriman: 1/8 = 12,5% -> 2/11 = 18,2% = +5,7 poin (dicek manual).
- Hasil hitungan diverifikasi ulang oleh `verifikasi.py`: cocok.

## Temuan
1. **"pelayanannya kurang ramah pas antar" dihitung PUJIAN layanan** ("ramah" + "pas" positif, "kurang" tidak menegasi). Sama dengan temuan 07.
2. **Tema bawaan bias usaha makanan:** "bau apek" masuk "Keamanan pangan / kebersihan" (dampak 5) sehingga isu yang sama tampil **dua kali**
   di tabel (Keamanan 3 + Bau apek 3, keduanya Segera); "setrikaan rapi" masuk Kemasan; "luntur" masuk juga Kualitas produk. Agent harus
   memakai `ganti_tema` atau menimpa id, tapi SKILL.md tidak menjelaskan cara menangani label bawaan yang tidak cocok.
3. "kurang 1 kaos kaki" (barang hilang, penting untuk laundry) tidak terdeteksi: pola `kurang (item|satu|dua)` tidak menerima angka.
4. "bisa langganan bulanan buat 20 seragam kantor? kirim invoice" -> Pengiriman + Pembayaran **pujian**; seharusnya permintaan/peluang (saran).

## Label manual vs script
Keluhan menurut penguji: bau apek 3, telat 3, rusak/hilang/luntur 5 (luntur, kancing, sobek-kusut, noda, kaos kaki), harga 1, admin lambat 1,
pelayan kurang ramah 1 = 14. Script (dengan tema.json) benar 12 (tidak termasuk dobel Keamanan), meleset 2 (kaos kaki, kurang ramah -> pujian).
Urutan prioritas setelah agent menghapus dobel: rusak/hilang (dampak 5) -> bau apek -> telat. Sesuai penilaian penguji.

## Nilai skenario: 7/10 (dengan tema.json kerjanya baik; kesalahan sentimen "kurang ..." tetap ada)
