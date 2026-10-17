# Cek silang draf pengumuman 18 Okt 2026 (C6, Akun A, 17 Okt 2026)

Dicek dengan skrip python terhadap `sebelum-sesudah.jsonl`, `SEBELUM-SESUDAH.md`, `bundles/*.txt` + `bundles/README.md`, `catalog.csv`.

## Hasil
1. 10 besar: OK. Nama, judul jualan, skor sebelum->sesudah, dan urutan selisih (7,5/7/7/6/6/5,9/5,75/5,6/5,5/5,3) cocok dengan jsonl; semuanya `lolos_promosi` true dan tampil di halaman. Skill ke-11 (5,25) tidak memotong tie.
2. Paket: OK. 10 paket, jumlah skill (16/15/8/10/8/7/10/5/14/20) = isi `bundles/*.txt` = `bundles/README.md`; harga cocok.
3. Label medis: SATU KEKURANGAN, DIPERBAIKI. Varian 2 (daftar paket) dan Varian 1 (WA) menyebut Paket Klinik tanpa label; ditambah "belum direview tenaga medis". Varian 3 sudah benar. `pengingat-pasien-klinik` berlabel di semua varian.
4. Klaim "bot OpenClaw asli": OK. 9 skill bertag "openclaw bot Telegram asli"; `odoo-usaha` tidak, dan memang tidak diklaim. Catatan: untuk `siyuan-sop` tag berasal dari uji jadwal terkirim (13 Okt), bukan uji sebelum/sesudah; sesuai aturan tag, tapi pemilik perlu tahu.
5. Janji/kata mutlak: tidak ditemukan; disclaimer "bukan jaminan hasil" ada.

## Untuk Akun B (data tidak diubah)
- `pengingat-follow-up`: contoh "Pak Andi utang 5m" di draf berasal dari `cuplikan_jualan`, sedangkan `tanpa_skill` di jsonl berbunyi "menebak nominal, menyimpan nomor pihak ketiga, ..." dan `tugas` berbeda. Mohon pastikan cuplikan sesuai uji yang dinilai.
- Status 10 skill itu masih `beta` (bukan `rilis`); konfirmasi kesiapan jual 18 Okt.
