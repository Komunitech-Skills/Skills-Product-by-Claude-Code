# Skenario 02 (uji Akun B) — Basis pengetahuan CS klinik: FAQ + proteksi timpa + ekspor-basis (normal)

**Penguji:** Akun B, kernel tiruan `127.0.0.1:16806`.

## Permintaan pengguna
> "Simpan FAQ jam praktik dan biaya periksa klinik mata saya, lalu gabungkan jadi satu file untuk agen CS."

## Langkah & hasil nyata
1. Buat `/FAQ/Jam Praktik` dan `/FAQ/Biaya Periksa` (dengan `--ya`) → keduanya `TERSIMPAN`.
2. **Uji proteksi tulis ulang:** coba `buat` lagi ke path yang SAMA tanpa `--timpa`:
   ```
   GAGAL: TIDAK DIBUAT: sudah ada dokumen di path '/FAQ/Jam Praktik' (id ...). Pakai perintah `tambah`
   ... atau `buat ... --timpa --ya` untuk MENGGANTI seluruh isi.
   ```
   Kode keluar **7**, sesuai dokumentasi — dokumen lama **tidak** tersentuh.
3. `tambah --id <id Jam Praktik> --md "...Sabtu..." --ya` → menambahkan poin baru **di akhir**, isi lama utuh (diverifikasi dengan `baca` — kedua poin tampil, urutan lama lalu baru).
4. `ekspor-basis --notebook 20260101000001-klinikbx --file basis-klinik.md`:
   ```
   TERSIMPAN: 2 dokumen digabung ke 'basis-klinik.md' (356 karakter).
   ```
   Isi file (dicek langsung, lihat `basis-klinik.md` di scratchpad uji): berisi kedua FAQ lengkap,
   dipisah `---`, judul sebagai heading path (`# /FAQ/Biaya Periksa`, dst.), urut alfabetis path.

## Serah terima ke skill lain
File `basis-klinik.md` hasil ekspor **langsung terbaca** sebagai basis pengetahuan untuk skill
`agen-cs-toko` (formatnya cocok untuk dijadikan "basis pengetahuan toko") dan bisa dipakai
`balas-chat-cs` sebagai sumber fakta saat membalas chat pelanggan — sesuai klaim SKILL.md §G.

## Kesimpulan
Sesuai dokumentasi. Proteksi anti-timpa dan `tambah` non-destruktif terverifikasi berfungsi persis
seperti diklaim, bukan cuma tertulis. Tidak ada temuan baru.
