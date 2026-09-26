# Contoh 3: Input tidak lengkap

**Permintaan pengguna:** "Cek status website saya dong."

**Masalah:** pengguna belum pernah memberi tahu alamat Uptime Kuma/status page-nya, dan tidak
disebutkan alamat websitenya sendiri untuk mode `cek-cepat`.

**Yang dilakukan agent:** tidak menebak alamat. Tanya **sekali**, satu pesan, berisi daftar
pilihan singkat:
> Boleh dibantu, dua hal dulu ya:
> 1. Sudah pasang Uptime Kuma? Kalau sudah, boleh minta alamat status page-nya (bentuk
>    `http://ALAMAT:PORT/status/NAMA-SLUG`, biasanya ada di address bar browser saat membuka
>    halaman status-nya)?
> 2. Kalau belum pasang, tidak apa — beri tahu alamat website Anda saja, saya cek sekali langsung
>    (mode cepat tanpa Uptime Kuma).

**Bila dipaksa mencoba tanpa info (mis. untuk menunjukkan pesan galatnya ke pengguna teknis):**
```bash
python3 scripts/pantau.py cek
```
Keluaran nyata:
```
GALAT: Wajib isi --status-url (alamat lengkap status page) ATAU keduanya --url dan --slug.
```
(kode keluar 2 — kesalahan pemakaian, bukan kesalahan koneksi)

Setelah pengguna menjawab "belum pasang, alamatnya tokosaya.contoh" misalnya, agent langsung
memakai mode `cek-cepat` (lihat `examples/02-cek-cepat-tanpa-uptime-kuma.md`), tanpa menanyakan
lagi.
