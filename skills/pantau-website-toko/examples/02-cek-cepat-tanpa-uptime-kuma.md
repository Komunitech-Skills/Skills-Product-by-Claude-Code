# Contoh 2: Cek cepat tanpa Uptime Kuma sama sekali

**Permintaan pengguna:** "Cek website saya masih hidup nggak, alamatnya toko-contoh.example.com"
(domain contoh fiktif; angka di bawah berasal dari satu kali cek sungguhan pada 2026-09-26 terhadap
sebuah server https publik, dengan nama domainnya diganti domain contoh — satu kali cek saja, sesuai
kebijakan skill. Di pemakaian nyata, skill hanya mengecek situs milik pengguna).

**Perintah yang dijalankan agent:**
```bash
python3 scripts/pantau.py cek-cepat https://toko-contoh.example.com --timeout 8
```

**Keluaran (angka dari satu kali permintaan HTTP + pemeriksaan SSL sungguhan, dijalankan 2026-09-26; domain diganti domain contoh):**
```
CEK CEPAT: https://toko-contoh.example.com
HTTP    : 404 (GALAT KLIEN (4xx))
Respons : 63.5 ms
SSL     : 25 hari lagi (kedaluwarsa 2026-10-21)
```

Versi `--json` dari permintaan yang sama:
```json
{
  "ok": true,
  "url": "https://toko-contoh.example.com",
  "kode_http": 404,
  "kategori": "GALAT KLIEN (4xx)",
  "waktu_respons_ms": 86.7,
  "ssl": {
    "valid": true,
    "sisa_hari": 25,
    "kedaluwarsa": "2026-10-21",
    "catatan": null
  }
}
```

**Jawaban agent ke pengguna (contoh):**
> Servernya AKTIF dan merespons dalam 64 ms — cepat. Kode HTTP-nya 404 ("halaman tidak ditemukan"
> di alamat persis ini; bila ini bukan halaman utama toko, coba alamat halaman produknya langsung).
> Sertifikat SSL aman, masih 25 hari lagi sebelum kedaluwarsa (21 Oktober 2026).

**Catatan sertifikat tidak terpercaya (skenario lain, diuji di `tests/uji_regresi.py` dengan
sertifikat self-signed sungguhan):** bila sertifikat tidak terpercaya (self-signed/kedaluwarsa/
hostname tidak cocok), `cek-cepat` tetap melaporkan status HTTP-nya, tapi bagian SSL ditandai
jelas, misalnya:
```
SSL     : 29 hari lagi (kedaluwarsa 2026-10-26)  [PERINGATAN: sertifikat tidak terpercaya]
```
