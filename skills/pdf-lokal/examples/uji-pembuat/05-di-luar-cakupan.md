# Contoh 5 (di luar cakupan)

**Input pengguna:** "Dari PDF nota ini, tolong catat semua nominal & tanggalnya ke Excel"

**Respons agent yang benar:** ini bukan tugas pdf-lokal (skill ini cuma mengolah
BENTUK file PDF - gabung/pisah/kompres/dst - bukan MEMBACA/MEMAHAMI isinya). Arahkan
ke skill `ekstrak-nota-faktur` yang memang dibuat untuk membaca isi nota/faktur.

**Input pengguna lain di luar cakupan:** "Buatkan tanda tangan digital bersertifikat
di PDF kontrak ini yang sah secara hukum" → jelaskan itu fitur **proprietary/berbayar**
Stirling-PDF (certificate signing, di luar fitur inti/gratis), bukan bagian dari skill
ini - lihat `ATTRIBUTION.md`.

Skill ini juga menolak memproses ke server yang bukan localhost tanpa penegasan
eksplisit (`STIRLING_ALLOW_REMOTE=1`), sebagai perlindungan privasi default:
```
$ STIRLING_URL=http://203.0.113.5:8080 python3 scripts/pdf.py cek
GAGAL: Alamat Stirling-PDF (http://203.0.113.5:8080) bukan localhost/127.0.0.1. ...
```
