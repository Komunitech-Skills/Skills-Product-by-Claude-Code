# Skenario 04 (input buruk) — 6 kasus rusak/tidak lengkap

Menguji beberapa kasus sekaligus (bukan cuma satu) karena pedoman kurasi Komunitech meminta cakupan
"file bukan PDF, PDF terkunci tanpa sandi, file 0 byte, Stirling mati, URL publik, nama
file dengan spasi/karakter Indonesia".

## A. File bukan PDF sungguhan (teks biasa diberi nama `.pdf`)
```
$ echo "ini bukan pdf sungguhan" > bahan/palsu.pdf
$ python3 scripts/pdf.py gabung bahan/palsu.pdf bahan/kontrak-sewa-ruko.pdf
GAGAL: Stirling-PDF gagal memproses file ini: Job failed: java.io.IOException: JPDFium
merge failed. Biasanya artinya file rusak, bukan PDF yang valid, atau formatnya tidak
didukung. Coba perintah 'python3 pdf.py cek' dulu untuk pastikan server sehat, dan
periksa file aslinya bisa dibuka normal.
exit code: 1
```
**Lulus** — tidak crash mentah (traceback Python), pesan bahasa Indonesia awam, exit code
bukan 0 (agent tahu ini gagal).

## B. File 0 byte
```
$ touch bahan/kosong.pdf
$ python3 scripts/pdf.py kompres bahan/kosong.pdf
GAGAL: Stirling-PDF menolak permintaan ini: File cannot be null or empty
exit code: 1
```
**Lulus.**

## C. PDF terkunci, sandi yang dicoba salah
```
$ python3 scripts/pdf.py buka-kunci hasil/kontrak-pasal3-5-final.pdf --sandi "sandisalah"
GAGAL: PDF ini terkunci kata sandi, atau kata sandi yang diberikan salah. Kalau baru
memakai perintah 'buka-kunci', coba periksa lagi ejaan/besar-kecil hurufnya. Kalau
belum, buka dulu dengan 'buka-kunci --sandi ...' (pakai kata sandi yang benar), baru
proses lagi.
exit code: 1
```
**Lulus** — pesan tidak membocorkan info teknis mentah, mengarahkan aksi yang benar.

## D. Stirling-PDF mati (container dihentikan sementara)
```
$ docker stop stirling-214
$ python3 scripts/pdf.py cek
GAGAL: Tidak bisa menghubungi Stirling-PDF di http://localhost:8080 ([Errno 111]
Connection refused). Pastikan aplikasi Stirling-PDF sudah dibuka & sedang berjalan di
komputer ini. Lihat docs/panduan-stirling-pdf.md untuk cara memasang dan
menyalakannya, atau ikuti 'Cara manual tanpa script' di SKILL.md bila belum sempat
memasangnya.
exit code: 1
```
**Lulus** — pesan actionable, tidak menyalahkan pengguna, mengarah ke dokumentasi.
(Container dinyalakan kembali setelah tes ini untuk melanjutkan skenario lain.)

## E. URL server publik (bukan localhost) ditolak
```
$ python3 scripts/pdf.py cek --url "http://contoh-server-publik.com:8080"
GAGAL: Alamat Stirling-PDF (http://contoh-server-publik.com:8080) bukan
localhost/127.0.0.1. Skill ini dirancang untuk memproses file HANYA di komputer
sendiri. Jika kamu memang sengaja memakai server lain (mis. server kantor di
jaringan lokal) dan paham risikonya (file dikirim ke alamat itu), set environment
variable STIRLING_ALLOW_REMOTE=1 lalu coba lagi.
exit code: 1
```
**Lulus** — klaim "tolak URL non-lokal" di deskripsi skill **terbukti benar**, dan tetap
ada jalan keluar sadar (`STIRLING_ALLOW_REMOTE=1`) untuk kasus sah (server kantor).

## F. Nama file dengan spasi & karakter Indonesia (bukan input "buruk" secara teknis,
tapi rawan bug lintas-OS — realistis untuk pengguna awam yang menamai file semaunya)
```
$ cp bahan/resi-01.pdf "bahan/resi kilat Bu Sri (Jl. Kenanga No.3).pdf"
$ python3 scripts/pdf.py gabung "bahan/resi kilat Bu Sri (Jl. Kenanga No.3).pdf" \
    bahan/resi-02.pdf --keluaran "hasil/gabungan tokoku – bulan September.pdf"
Berhasil digabung (2 file) -> /tmp/.../hasil/gabungan tokoku – bulan September.pdf
exit code: 0
```
Diverifikasi file benar-benar ada di path persis itu (termasuk spasi, tanda kurung, dan
en-dash "–"). **Lulus** — tidak ada masalah encoding/escaping.

## Kesimpulan skenario 04
Semua 6 kasus ditangani tanpa crash, tanpa traceback mentah, dengan pesan bahasa
Indonesia yang jelas dan actionable, dan exit code selalu bukan 0 saat gagal (penting
agar agent tahu harus berhenti, bukan melanjutkan seolah berhasil). Tidak ditemukan
cacat pada penanganan input buruk itu sendiri — lihat `HASIL-UJI.md` untuk cacat terkait
**konfigurasi server** (bukan input pengguna) yang jauh lebih berdampak.
