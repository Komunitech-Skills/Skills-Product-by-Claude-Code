# 01 - Impor kontak dari CSV (data fiktif, listmonk 6.2.0 asli)

**Pengguna:** "Ini daftar pelanggan toko saya (kontak.csv), masukkan ke newsletter ya."

Berkas: pemisah `;`, ada BOM, duplikat, salah ketik domain, satu email rusak, satu orang menulis "tidak" di kolom Setuju, satu baris kosong.

```
$ listmonk.py periksa-kontak kontak.csv --keluaran bersih.csv
Kontak valid dan siap diimpor : 5
Email tidak valid (dibuang)   : 1
Duplikat (dibuang)            : 1
Menolak/belum setuju (dibuang): 1
Baris kosong                  : 1
Perlu dicek manual (salah ketik?) - TETAP disertakan: 1
  baris 5: t***@gmial.com (mungkin maksudnya @gmail.com)
Kolom tambahan disimpan sebagai atribut: Kota
INGAT: pastikan tiap orang di berkas ini SUDAH setuju menerima email Anda (lihat SKILL.md, UU PDP).
```
**Agent bertanya sekali:** "Dari mana kontak ini dan bagaimana mereka setuju menerima email Anda? Satu orang menolak dan dibuang; 'tin@gmial.com' mungkin salah ketik - mau dibetulkan dulu?"

**Pengguna:** "Dari formulir daftar di toko, Agu-Sep 2026. Yang gmial biarkan."

```
$ listmonk.py impor kontak.csv --list 4 --sumber-persetujuan "Formulir daftar di toko, Agu-Sep 2026" --saya-punya-izin
Tujuan: list #4 'Newsletter Toko Uji' (opt-in double), status langganan awal: unconfirmed
BELUM DIIMPOR. Tunjukkan ringkasan ini ke pengguna, lalu jalankan ulang dengan --ya.
$ listmonk.py impor ... --ya
Impor finished: 5 dari 5 baris.
LANGKAH BERIKUTNYA: kirim email konfirmasi (double opt-in) dengan 'kirim-optin'.
$ listmonk.py kirim-optin --list 4
Email konfirmasi akan dikirim ke 5 orang berstatus 'belum konfirmasi' di list 'Newsletter Toko Uji'.
BELUM DIKIRIM. Tanya pengguna, lalu ulangi dengan --ya --konfirmasi-penerima 5
```
Hasil nyata di listmonk: 5 email konfirmasi terkirim setelah `--ya --konfirmasi-penerima 5`; setelah 2 orang klik konfirmasi, `daftar-pelanggan` menunjukkan sudah konfirmasi 2, belum 3. Nama `=cmd|x` dibersihkan menjadi `cmd|x` (cegah rumus Excel).
