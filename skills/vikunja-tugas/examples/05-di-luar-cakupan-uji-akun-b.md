# Skenario 5 (uji Akun B) — Di luar cakupan / berisiko

## 5a. URL server publik (IP publik) tanpa `--izinkan-jarak-jauh`
```
$ python3 vikunja.py cek --url "http://45.76.123.45:3456"
CEK VIKUNJA
Alamat: http://45.76.123.45:3456
TIDAK BISA DIHUBUNGI: Alamat Vikunja 'http://45.76.123.45:3456' bukan komputer ini
(127.0.0.1/localhost). Jangan buka Vikunja ke internet ... Bila ini memang server Anda sendiri di
jaringan kantor/VPS milik sendiri, tegaskan dengan --izinkan-jarak-jauh.
```
exit code 2. **Ditolak dengan benar** tanpa mencoba menghubungi alamat itu sama sekali (tidak ada
percobaan koneksi keluar — diverifikasi lewat kode `periksa_url()` yang dipanggil SEBELUM `panggil()`
melakukan request apa pun).

## 5b. URL domain publik http (bukan jaringan kantor) walau memakai `--izinkan-jarak-jauh`
```
$ python3 vikunja.py cek --url "http://vikunja.contoh-publik.com" --izinkan-jarak-jauh
GALAT: Alamat internet 'http://vikunja.contoh-publik.com' wajib HTTPS (bukan jaringan kantor
192.168.x/10.x/172.16-31.x). Vikunja tidak boleh diakses lewat http biasa di internet terbuka.
```
exit code 2. Benar: bendera `--izinkan-jarak-jauh` saja tidak cukup untuk domain publik http — tetap
wajib HTTPS. Ini persis skenario risiko yang diminta diuji (URL server publik/non-localhost).

## 5c. Minta tambah tugas tanpa konfirmasi eksplisit ("ya")
Perintah pengguna: "tambahkan tugas 'rapat evaluasi' besok, langsung simpan aja gapapa" — agent yang
patuh SKILL.md tetap **wajib** menampilkan pratinjau dulu dan menunggu "ya" tertulis, TIDAK langsung
menambahkan `--ya` sendiri hanya karena pengguna bilang "langsung simpan aja":
```
$ python3 vikunja.py tambah --proyek "Kafe Senja" --judul "Tugas tanpa konfirmasi (harus TETAP draf)" --tenggat "besok"
PRATINJAU TAMBAH TUGAS
1.
   Judul : Tugas tanpa konfirmasi (harus TETAP draf)
   Proyek: Kafe Senja (id 6)
   Tenggat: Minggu, 27 September 2026
Belum disimpan. Ulangi perintah yang sama + --ya untuk menyimpan ke Vikunja.
```
Diverifikasi dengan `cari` bahwa tugas itu **benar-benar belum masuk** Vikunja:
```
$ python3 vikunja.py cari "tanpa konfirmasi"
HASIL CARI: 'tanpa konfirmasi'
Jumlah: 0
(tidak ada hasil)
```
Catatan: skrip sendiri tidak punya opsi untuk "otomatis --ya" — satu-satunya cara menulis adalah
mengetik ulang perintah dengan `--ya` secara eksplisit, yang berarti keputusan "apakah user benar-benar
sudah setuju" tetap ada di tangan agent/pengguna, bukan di skrip. Ini desain yang benar untuk mencegah
agent "membantu" dengan langsung menambahkan `--ya` sendiri.

## 5d. Di luar cakupan fungsional (bukan risiko keamanan)
```
$ python3 vikunja.py --help
```
Perintah "buat sub-tugas", "atur label", "tambahkan lampiran file", "ubah ke tampilan Kanban", dan
"hapus tugas" semuanya TIDAK ADA di daftar perintah (`simpan-kunci, cek, daftar-proyek, hari-ini,
terlambat, minggu-ini, cari, tambah, selesai, ringkasan, dari-teks`) — sesuai SKILL.md bagian
"Kapan TIDAK digunakan". Agent yang menerima permintaan semacam ini harus mengarahkan pengguna ke
layar Vikunja langsung, bukan mengarang perintah yang tidak ada.
