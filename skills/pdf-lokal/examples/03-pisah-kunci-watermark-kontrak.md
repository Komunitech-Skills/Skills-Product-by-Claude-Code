# Skenario 03 (normal) — Ambil halaman 3-5 kontrak, watermark "SALINAN", lalu kunci sandi

**Permintaan pengguna (simulasi):** "Dari kontrak sewa ruko ini, ambil pasal 3 sampai 5 saja
buat dikirim ke calon penyewa. Kasih watermark SALINAN, terus kunci pakai kata sandi biar
nggak sembarangan diedit."

**Lingkungan:** Stirling-PDF v2.14.3 asli via Docker. Data: `kontrak-sewa-ruko.pdf` 10 halaman
fiktif dibuat dengan reportlab, tiap halaman berlabel "Halaman N dari 10" agar mudah diverifikasi.

## Langkah 1 — pisah rentang halaman 3-5
```
$ python3 scripts/pdf.py pisah-rentang bahan/kontrak-sewa-ruko.pdf --halaman 3-5 \
    --keluaran hasil/kontrak-pasal3-5.pdf
Berhasil diambil halaman 3-5 -> /tmp/.../hasil/kontrak-pasal3-5.pdf
```
Verifikasi independen `pdftotext`: isi 3 halaman hasil persis "Halaman 3 dari 10",
"Halaman 4 dari 10", "Halaman 5 dari 10" — **halaman yang diambil benar, tidak geser satu**
(kesalahan off-by-one adalah bug klasik untuk fitur rentang halaman).

## Langkah 2 — watermark "SALINAN"
```
$ python3 scripts/pdf.py watermark hasil/kontrak-pasal3-5.pdf --teks "SALINAN" \
    --keluaran hasil/kontrak-pasal3-5-wm.pdf
Berhasil ditambah watermark 'SALINAN' -> /tmp/.../hasil/kontrak-pasal3-5-wm.pdf
```
Diverifikasi visual (render `pdftoppm` ke PNG): watermark "SALINAN" tampil berulang miring
transparan di seluruh halaman, teks asli kontrak tetap terbaca jelas di atasnya.

## Langkah 3 — kunci kata sandi
```
$ python3 scripts/pdf.py kunci hasil/kontrak-pasal3-5-wm.pdf --sandi "RahasiaKontrak2026" \
    --keluaran hasil/kontrak-pasal3-5-final.pdf
Berhasil dikunci kata sandi -> /tmp/.../hasil/kontrak-pasal3-5-final.pdf
PENTING: simpan kata sandi ini baik-baik. Tanpa itu, PDF tidak bisa dibuka lagi.
```

## Verifikasi independen (tidak pakai kode skill sama sekali, pakai `qpdf`)
| Cek | Perintah | Hasil |
|---|---|---|
| File benar-benar terenkripsi | `qpdf --check` tanpa sandi | `invalid password` → **terkunci sungguhan**, bukan cuma klaim |
| Sandi yang diberikan memang bisa membuka | `qpdf --password=RahasiaKontrak2026 --decrypt ...` | **Berhasil dekripsi**, 3 halaman utuh |
| Isi setelah dekripsi = hasil langkah 2 (watermark tetap ada) | render PNG | **Benar**, watermark "SALINAN" terlihat miring transparan di render |
| File kontrak asli (10 halaman) tidak berubah | sha256 sebelum/sesudah 3 langkah | **Identik** |
| Tidak ada penimpaan nama file | manual | Setiap langkah pakai `--keluaran` sendiri, tidak ada yang menimpa `kontrak-sewa-ruko.pdf` asli maupun file antara |

## Kesimpulan
Rantai 3 perintah (pisah → watermark → kunci) — pola umum untuk dokumen legal/kontrak
usaha kecil — bekerja benar end-to-end, halaman tepat, watermark tampil, password
benar-benar mengenkripsi (diverifikasi pakai alat pihak ketiga `qpdf`, bukan cuma percaya
pesan sukses script). Tidak ditemukan cacat pada alur ini.
