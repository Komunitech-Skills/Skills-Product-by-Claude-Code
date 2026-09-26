# Skenario 01 (normal) — Gabung 3 nota foto jadi 1 PDF lalu kompres < 2 MB untuk WA

**Permintaan pengguna (simulasi):** "Tolong gabungin 3 foto nota belanja ini jadi satu PDF,
terus kecilin biar bisa dikirim WA (di bawah 2 MB ya)."

**Lingkungan uji:** Stirling-PDF v2.14.3 asli via Docker (`ghcr.io/stirling-tools/stirling-pdf:2.14.3`,
`-e SECURITY_ENABLELOGIN=false` — lihat catatan kritis di `HASIL-UJI.md` soal kenapa flag ini
harus ditambahkan meski tidak ada di contoh `docker run` bawaan `docs/panduan-stirling-pdf.md`).
Foto nota dibuat sendiri (noise acak + teks) agar ukurannya realistis (~3.1–3.2 MB per foto,
meniru foto kamera HP asli), bukan file kosong yang gampang dikompres.

## File asal
```
bahan/nota-a-hd.jpg   3.22 MB
bahan/nota-b-hd.jpg   3.24 MB
bahan/nota-c-hd.jpg   3.13 MB
```

## Langkah 1 — gabung foto jadi PDF
```
$ python3 scripts/pdf.py foto-ke-pdf bahan/nota-a-hd.jpg bahan/nota-b-hd.jpg bahan/nota-c-hd.jpg \
    --keluaran hasil/nota-hd-gabungan.pdf
Berhasil diubah jadi PDF (3 foto) -> /tmp/.../hasil/nota-hd-gabungan.pdf
```
- Hasil: **3 halaman**, ukuran **3495 KB (3.41 MB)** — diverifikasi independen dengan `pdfinfo`.
- Path lengkap ditampilkan apa adanya, sesuai klaim skill. **Lulus.**

## Langkah 2 — kompres di bawah 2 MB
```
$ python3 scripts/pdf.py kompres hasil/nota-hd-gabungan.pdf --target 2MB \
    --keluaran hasil/nota-hd-kecil.pdf
Berhasil dikompres: 3495 KB -> 1352 KB
  -> /tmp/.../hasil/nota-hd-kecil.pdf
```
- Verifikasi independen (`os.path.getsize`, bukan pakai angka dari script): **1 319 834 byte
  (1.32 MB)** — di bawah target 2 MB. **Cocok.**
- `pdfinfo` konfirmasi tetap **3 halaman** setelah kompres (tidak ada halaman hilang).
- Render halaman 1 hasil kompres (`pdftoppm`) masih terbaca jelas, tidak pecah/blur berlebihan.

## Verifikasi tambahan (independen, bukan dari klaim script)
| Cek | Hasil |
|---|---|
| sha256 3 foto asli sebelum vs sesudah kedua langkah | **Identik** — file asli sama sekali tidak disentuh |
| Tidak ada file yang menimpa nama file asli | **Benar** — semua hasil di path `--keluaran` baru |
| Jumlah halaman gabungan = jumlah foto input (3) | **Benar** |
| Ukuran akhir < 2 MB sesuai target pengguna | **Benar** (1.32 MB) |

## Kesimpulan skenario
Perintah bekerja tepat seperti dijanjikan SKILL.md: path lengkap disebut, file asli tak
berubah, hasil sesuai target. Satu-satunya cara ini bisa gagal total di hari pertama pembeli
adalah bila mereka menyalin **persis** perintah `docker run` di `docs/panduan-stirling-pdf.md`
bagian 3.2 — lihat cacat **T1 (Tinggi)** di `HASIL-UJI.md`: perintah itu ternyata membuat
server minta login/API key, sehingga `gabung`/`kompres` di atas akan gagal 401 sebelum
konfigurasi tambahan dilakukan.
