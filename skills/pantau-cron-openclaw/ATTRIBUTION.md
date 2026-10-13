# Atribusi

Skill ini adalah karya **orisinal** Komunitech (komunitech.com). Seluruh kode (`scripts/pantau_cron.py`, `tests/uji_regresi.py`), teks, dan data contoh ditulis dari nol; data contoh bersifat fiktif.

## Asal ide (konsep saja)
Konsep "dead man's switch" untuk job terjadwal -- tiap job mengirim *ping* saat sukses dan alarm berbunyi bila ping tidak datang dalam jadwal + masa tenggang -- dikenal luas dan dipopulerkan antara lain oleh proyek **Healthchecks** (https://github.com/healthchecks/healthchecks, lisensi BSD-3-Clause, (c) Healthchecks.io dan kontributor). Yang diambil hanya gagasan umum itu. **Tidak ada kode, teks, antarmuka, ataupun model data Healthchecks yang disalin atau diadaptasi.** Parser cron, perhitungan jatuh tempo, penyimpanan, dan format laporan ditulis sendiri.

Opsi lanjutan (ping ke layanan Healthchecks milik pengguna) hanya memanggil alamat ping yang dimiliki pengguna sendiri; Komunitech tidak berafiliasi dengan proyek atau layanan Healthchecks. Nama "Healthchecks" disebut sebagai penyebut produk.

Catatan audit: catatan riset internal kurator (tidak disertakan dalam paket).

Penggunaan tunduk pada `LISENSI.txt` yang disertakan dalam paket pembelian.
