# Contoh 8 (Uji Akun B): Input tidak lengkap

**Permintaan pengguna:** "Website saya kok kayaknya lambat, cek dong."

**Masalah:** tidak ada alamat website/status page sama sekali disebutkan.

**Perilaku yang diverifikasi (sesuai SKILL.md bagian "Prinsip untuk pembeli awam"):** agent seharusnya bertanya **sekali**, satu pesan, bukan menebak alamat. Dicoba memaksa script tanpa argumen untuk melihat pesan galat mentahnya:
```bash
python3 scripts/pantau.py cek-cepat
```
```
usage: pantau.py cek-cepat [-h] [--timeout TIMEOUT] [--json] url
pantau.py cek-cepat: error: the following arguments are required: url
```
(kode keluar 2 — argparse bawaan Python, bukan lewat kelas `Gagal` skill; pesan ini **bahasa Inggris teknis**, tidak cocok ditunjukkan langsung ke pembeli awam. SKILL.md sudah benar mengarahkan agent untuk **bertanya dulu**, bukan menjalankan lalu menunjukkan pesan mentah ini — perilaku yang diuji di sini mengonfirmasi kenapa aturan itu penting: pesan argparse murni tidak ramah pengguna awam.)

```bash
python3 scripts/pantau.py ringkasan
```
```
GALAT: Wajib isi --status-url (alamat lengkap status page) ATAU keduanya --url dan --slug.
```
(kode keluar 2, lewat kelas `Gagal` — pesan ini jauh lebih ramah dan bisa diteruskan ke pengguna apa adanya bila perlu.)

**Kesimpulan pengujian:** perilaku agent yang benar (bertanya sekali dengan pilihan jelas: sudah pasang Uptime Kuma atau belum) sudah terdokumentasi dengan baik di SKILL.md dan `examples/03-input-tidak-lengkap.md` milik pembuat. Satu catatan tambahan dari pengujian independen ini: subperintah `cek-cepat` tanpa argumen menghasilkan pesan galat Python mentah (bukan pesan `Gagal` berbahasa Indonesia), berbeda dari `cek`/`ringkasan`/`mingguan` yang semuanya lewat `Gagal`. Tidak fatal (agent tetap diarahkan untuk bertanya dulu, bukan menjalankan perintah tanpa argumen), tapi untuk konsistensi, akan lebih baik bila `cek-cepat` juga menangani argumen kosong lewat pesan `Gagal` yang seragam.
