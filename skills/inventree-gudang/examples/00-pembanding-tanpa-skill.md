# Uji A/B — skenario normal 1 tanpa skill vs dengan skill

**Skenario:** "Stok semen berapa, di rak mana saja? Barang apa yang hampir habis?" — InvenTree 1.5.6 asli (Docker), data penguji (lihat 01).

## A. Tanpa skill (agent umum, menebak API sendiri)
Perilaku khas yang dijalankan penguji:
1. Agent tidak tahu di mana InvenTree & tokennya → **meminta pengguna menempel token API di chat** (token lalu tersimpan di riwayat percakapan/log).
2. Mencoba beberapa endpoint (`/api/part/?search=semen`, `/api/stock/?part=1`, `/api/part/?low_stock=true`) dengan curl; hasil JSON mentah:
```
BS-10 Besi Beton 10 mm 120.0 120.0 150.0 0.0 0.0
KW-01 Kawat Bendrat 17.25 17.25 25.0 0.0 0.0 kg
SM-01 Semen Portland 50 kg 91.0 91.0 100.0 100.0 0.0 sak
...
3 4 8.0 SMN-2608      <- lokasi hanya berupa angka id (4), bukan "Toko Depan"
2 2 25.0 SMN-2609
1 2 58.0 SMN-2608
```
3. Jawaban yang disusun: angka stok benar bila agent teliti, tetapi: lokasi berupa id (perlu panggilan tambahan), "semen" ambigu (SM-01 vs SM-02) biasanya **ditebak**, kolom `ordering` sering diabaikan → menyarankan membeli semen padahal 100 sak sudah dipesan; kemasan pemasok (roller 1 dus = 6) tidak diketahui; angka gaya Inggris (`17.25`, `1500.0`); tidak ada rumus "perlu dipesan" yang konsisten dari hari ke hari.
4. Untuk menulis (opname/terima barang) agent tanpa skill akan menyusun POST sendiri — tanpa pratinjau baku, tanpa cek "stok berubah sejak lembar dibuat", tanpa pembedaan "TIDAK PASTI" saat timeout (risiko posting ganda).
Waktu: ±8–12 panggilan alat, 3–5 menit trial-error endpoint.

## B. Dengan skill
Lihat `01-cek-stok-dan-menipis.md`: 3 perintah, token tidak pernah lewat chat (`simpan-kunci`), nama ambigu ditanyakan (kode 7), lokasi berupa jalur (`Gudang Utama/Rak A`), batch & kedaluwarsa, angka Indonesia (`18,5 kg`, `1.500 kg`), rumus saran eksplisit yang memperhitungkan barang sedang dipesan/diproduksi, semua angka terverifikasi cocok dengan API.

## Penilaian
| Kriteria | Tanpa skill | Dengan skill |
|---|---|---|
| Keamanan token | buruk (tempel di chat) | baik (file 600, disamarkan) |
| Kebenaran angka | benar bila teliti; saran beli sering salah (abaikan `ordering`) | benar & terverifikasi |
| Siap tempel untuk awam | tidak (JSON/id angka) | ya |
| Konsistensi | berubah-ubah | format tetap |
| Keamanan tulis | tidak ada pratinjau/pengaman | pratinjau + `--ya` + cek perubahan + kode 8 |
**Kesimpulan: dengan skill jelas lebih baik** — syarat nilai tambah terpenuhi.
