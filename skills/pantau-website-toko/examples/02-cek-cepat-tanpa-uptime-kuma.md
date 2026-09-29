# Contoh 2: Cek cepat tanpa Uptime Kuma sama sekali

**Permintaan pengguna:** "Cek website saya masih hidup nggak, alamatnya api.anthropic.com" (dipakai
di sini sebagai domain https publik nyata untuk menunjukkan hasil sungguhan tanpa memantau situs
orang lain berulang — satu kali cek saja, sesuai kebijakan skill).

**Perintah yang dijalankan agent:**
```bash
python3 scripts/pantau.py cek-cepat https://api.anthropic.com --timeout 8
```

**Keluaran nyata (satu kali permintaan HTTP + pemeriksaan SSL sungguhan, dijalankan 2026-09-26):**
```
CEK CEPAT: https://api.anthropic.com
HTTP    : 404 (GALAT KLIEN (4xx))
Respons : 63.5 ms
SSL     : 25 hari lagi (kedaluwarsa 2026-10-21)
```

Versi `--json` dari permintaan yang sama:
```json
{
  "ok": true,
  "url": "https://api.anthropic.com",
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
