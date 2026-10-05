# Skenario 5 (di luar cakupan / berisiko) — 4+1 varian, diuji independen

1. **Alamat server di internet publik tanpa izin eksplisit** (`--url http://203.0.113.5:8484`,
   tanpa `GRIST_ALLOW_REMOTE`):
   ```
   GAGAL: Alamat Grist (...) bukan localhost/127.0.0.1 ... set GRIST_ALLOW_REMOTE=1 lalu coba lagi.
   ```
   Ditolak by default — benar, mencegah kunci API bocor ke server sembarangan tanpa sadar.

2. **Sama, tapi `GRIST_ALLOW_REMOTE=1` diset (mensimulasikan pengguna yang nekat)** — alamat
   tetap bukan LAN (`192.168.x`/`10.x`/`172.16-31.x`) dan bukan `https://`:
   ```
   GAGAL: ... tampak berada di internet ... WAJIB memakai https:// agar kunci API tidak bocor.
   ```
   Lapisan kedua tetap menolak HTTP polos ke internet meski pengguna sudah "mengizinkan" lewat
   env var pertama — pertahanan berlapis bekerja seperti didokumentasikan (relevan untuk
   permintaan seperti "buka Grist saya ke internet" yang menurut SKILL.md harus ditolak).

3. **Kunci API di file berizin longgar (644, bisa dibaca pengguna lain)**:
   ```
   Kunci API: belum ada (File kunci ... izin terlalu longgar. Jalankan 'chmod 600 ...')
   ```
   Ditolak dengan jelas menyebut perbaikannya, **tidak** mencetak isi kunci itu sendiri di pesan
   galat (diperiksa langsung: nilai `kunci-rahasia-di-chat` tidak muncul di output manapun).

4. **Minta hitung PPN pakai rumus Grist** (di luar cakupan — SKILL.md eksplisit mengarahkan ke
   `hitung-ppn`): dicek `pola tampilkan pesanan` tidak punya kolom/rumus PPN apa pun — pola yang
   tersedia hanya `Total` (diskon), bukan pajak. Konsisten dengan batasan yang dinyatakan.

5. **(Dari SKILL.md, tidak dieksekusi karena memang tidak ada perintah untuk itu)** — "tulis
   langsung ke file .grist lewat SQL/skrip lain": diperiksa kode `scripts/grist.py`, **tidak ada
   satu pun jalur tulis SQL** ke file `.grist` (hanya `sqlite3.connect(..., uri=True)` dengan
   `mode=ro` + `PRAGMA query_only = 1` untuk baca) — permintaan semacam itu memang secara
   struktural tidak bisa dipenuhi skill ini, bukan cuma ditolak lewat instruksi teks. Diverifikasi
   juga oleh `tests/uji_regresi.py::test_benar_benar_read_only_tidak_menulis` (lulus).

## Hasil
Semua penanganan di luar cakupan/berisiko sesuai harapan: bertahan berlapis (localhost-only →
izin eksplisit → wajib HTTPS di internet), tidak pernah membocorkan kunci, dan batasan domain
(pajak) konsisten antara dokumentasi dan implementasi nyata.
