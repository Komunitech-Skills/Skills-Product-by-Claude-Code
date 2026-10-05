# Uji A/B — skenario normal 1 (gabung 3 nota foto + kompres < 2 MB)

Permintaan yang sama dipakai: "Tolong gabungin 3 foto nota belanja ini jadi satu PDF,
terus kecilin biar bisa dikirim WA (di bawah 2 MB ya)."

## Tanpa skill `pdf-lokal` (agent umum, tidak tahu ada Stirling-PDF lokal)
Perilaku realistis seorang AI agent tanpa akses ke skill ini, berdasarkan kemampuan
umum agent coding (Python standar + tanpa API key/layanan eksternal yang jelas):
1. Agent kemungkinan besar **tidak tahu** ada Stirling-PDF terpasang di komputer
   pengguna, karena tidak ada instruksi yang memberitahunya untuk mengecek itu.
2. Opsi paling umum yang dipilih agent generik:
   - **Menulis kode Python ad hoc** dengan library yang mungkin/mungkin tidak
     terpasang (`Pillow`/`img2pdf`/`reportlab`) untuk gabung foto → PDF, lalu mencoba
     "kompres" dengan menurunkan kualitas JPEG asal-asalan (`quality=50`) tanpa target
     ukuran yang terukur — **tidak ada jaminan hasil < 2 MB**, hanya tebakan.
   - Atau, **menyarankan situs "PDF online gratis"** pihak ketiga ke pengguna untuk
     upload foto notanya — melanggar prinsip privasi data usaha (nota berisi rincian
     transaksi bisnis) tanpa peringatan risiko yang jelas.
   - Kemungkinan gagal total kalau library Python yang dibutuhkan (mis. `img2pdf`,
     `Pillow`) belum terpasang di komputer pengguna awam — dan agent generik tidak
     tahu itu sampai dicoba & error `ModuleNotFoundError`, yang membingungkan pengguna
     awam ("apa itu ModuleNotFoundError?").
3. Tidak ada jaminan file asli tidak tertimpa (nama file keluaran mungkin sama dengan
   input jika agent tidak berhati-hati).
4. Tidak ada verifikasi ukuran akhir — agent hanya bisa *bilang* "sudah dikompres"
   tanpa benar-benar mengukur, karena tidak ada alat pasti untuk itu.

**Hasil realistis tanpa skill:** kemungkinan gagal (dependency hilang), atau berhasil
tapi ukuran akhir tidak terjamin < 2 MB, atau — skenario terburuk — menyarankan upload
data usaha ke situs pihak ketiga tak dikenal.

## Dengan skill `pdf-lokal` (hasil sungguhan, lihat `01-gabung-kompres-nota.md`)
```
$ python3 scripts/pdf.py foto-ke-pdf bahan/nota-a-hd.jpg bahan/nota-b-hd.jpg bahan/nota-c-hd.jpg \
    --keluaran hasil/nota-hd-gabungan.pdf
Berhasil diubah jadi PDF (3 foto) -> .../hasil/nota-hd-gabungan.pdf   (3495 KB)

$ python3 scripts/pdf.py kompres hasil/nota-hd-gabungan.pdf --target 2MB \
    --keluaran hasil/nota-hd-kecil.pdf
Berhasil dikompres: 3495 KB -> 1352 KB
  -> .../hasil/nota-hd-kecil.pdf
```
- Ukuran akhir **1.32 MB, diverifikasi independen** dengan `os.path.getsize` (bukan
  cuma percaya output script) — **benar-benar < 2 MB**, bukan tebakan.
- Path lengkap hasil selalu disebut, tidak pernah menimpa file asli (diverifikasi sha256).
- Tidak ada file diunggah ke internet — semua lewat `localhost:8080` (Stirling-PDF lokal).
- Tidak butuh `pip install` apa pun di sisi agent; hanya `urllib` bawaan Python.

## Kesimpulan uji A/B
Skill **jelas lebih baik**:
- Hasil terukur & pasti (target ukuran benar-benar tercapai, diverifikasi independen)
  vs tebakan kualitas JPEG generik tanpa target.
- Privasi terjaga (lokal via Stirling-PDF) vs risiko disarankan upload situs pihak ketiga.
- Tidak bergantung pip install tambahan yang mungkin gagal di komputer awam.
- Pesan hasil siap tempel/kirim (path lengkap, bahasa Indonesia) vs output teknis generik.

Nilai tambah signifikan → **bukan kandidat skor maksimal 6** (skor final ada di `HASIL-UJI.md`).
