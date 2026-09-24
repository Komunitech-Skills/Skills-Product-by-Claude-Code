# Uji A/B — Skenario S1 (artikel blog SEO "cara UMKM lapor SPT tahunan 2026")

**Tanggal uji:** 2026-09-23
**Penguji:** agent penguji independen (simulasi, Claude Code)
**Input pengguna (sama untuk kedua kondisi):**
> "Tulis artikel blog SEO buat website konsultan pajak saya, judulnya seputar cara UMKM lapor SPT
> tahunan 2026, sekitar 1000 kata, sumbernya harus resmi dari DJP."

---

## Kondisi A — TANPA skill (agent biasa, tanpa membaca SKILL.md, tanpa riset web sungguhan)

*Ditulis dari pengetahuan umum model, gaya khas jawaban AI generik tanpa instruksi sitasi wajib.*

> # Panduan Lengkap Lapor SPT Tahunan UMKM 2026
>
> Setiap tahun, pelaku UMKM di Indonesia wajib melaporkan Surat Pemberitahuan (SPT) Tahunan sebagai
> bagian dari kewajiban perpajakan. Di tahun 2026, proses ini semakin dipermudah dengan sistem digital
> yang terus disempurnakan oleh Direktorat Jenderal Pajak (DJP).
>
> ## Siapa yang Wajib Lapor SPT?
> UMKM yang sudah memiliki NPWP dan menjalankan usaha dengan omzet di bawah Rp4,8 miliar per tahun
> umumnya dikenakan tarif PPh Final 0,5% dan tetap wajib melaporkan SPT Tahunan setiap tahun, biasanya
> paling lambat akhir Maret untuk wajib pajak orang pribadi.
>
> ## Langkah-Langkah Lapor SPT Online
> 1. Siapkan NPWP dan EFIN Anda.
> 2. Login ke situs DJP Online di djponline.pajak.go.id.
> 3. Pilih menu e-Filing dan pilih jenis formulir SPT yang sesuai (1770 atau 1770S).
> 4. Isi data penghasilan, omzet, dan harta sesuai catatan usaha Anda.
> 5. Kirim SPT dan simpan bukti tanda terima elektronik.
>
> ## Manfaat Lapor Tepat Waktu
> Selain menghindari sanksi denda, lapor SPT tepat waktu juga membuat rekam jejak pajak Anda tetap
> bersih, yang penting jika suatu saat Anda mengajukan pinjaman usaha ke bank. Berdasarkan data DJP,
> tingkat kepatuhan pelaporan SPT UMKM terus meningkat setiap tahunnya seiring digitalisasi layanan
> pajak.
>
> ## Tips Praktis
> - Catat omzet bulanan secara rutin agar tidak kerepotan saat lapor tahunan.
> - Manfaatkan aplikasi pencatatan keuangan sederhana.
> - Jangan tunggu mendekati deadline karena sistem sering mengalami lonjakan trafik di akhir Maret.
>
> Dengan mengikuti langkah di atas, pelaporan SPT Tahunan UMKM 2026 Anda bisa berjalan lancar dan bebas
> masalah.

*(±350 kata dalam cuplikan ini; agent generik biasanya akan meneruskan pola serupa hingga ±1000 kata
tanpa nomor kutipan sama sekali.)*

**Masalah pada Kondisi A (diverifikasi manual):**
- Menyebut "djponline.pajak.go.id" dan formulir "e-Filing" / "1770 / 1770S" — ini **alur DJP Online lama**
  yang sudah digantikan Coretax DJP mulai tahun pajak 2025 (dikonfirmasi lewat sumber resmi di Kondisi
  B, lihat `01-draf.md`). Informasi ini **berpotensi keliru/usang** untuk pembaca 2026.
- Klaim "Berdasarkan data DJP, tingkat kepatuhan pelaporan SPT UMKM terus meningkat setiap tahunnya" —
  **tidak ada angka, tidak ada sumber, tidak bisa ditelusuri**. Ini persis pola halusinasi yang coba
  dicegah skill: klaim faktual dibungkus "berdasarkan data X" tanpa kutipan nyata.
- Tidak ada satu pun nomor kutipan `[n]` atau Daftar Pustaka — pembaca tidak bisa memverifikasi apa pun.
- Ambang batas omzet "Rp4,8 miliar" disebut tanpa sumber/tahun rujukan (benar secara umum per aturan PP
  55/2022, tapi tidak diverifikasi ulang di sini dan tidak dikutip — persis risiko yang coba dicegah).

## Kondisi B — DENGAN skill (`asisten-tulis-riset`, riset web sungguhan)

Lihat draf lengkap di `01-draf.md` (skenario S1 penuh, ±850 kata + Daftar Pustaka).

Cuplikan pembuka:
> Tahun pajak 2025 adalah tahun pertama pelaporan SPT Tahunan sepenuhnya lewat sistem Coretax DJP [1].
> Bagi pelaku UMKM yang membayar PPh final 0,5% dari omzet, kabar baiknya: data setoran bulanan yang
> sudah dibayar akan otomatis muncul (ter-*prepopulated*) di konsep SPT Tahunan...

Setiap klaim faktual (alur Coretax, syarat data, tenggat 31 Maret, denda Rp100.000) diberi `[n]` yang
menunjuk ke 3 sumber resmi pajak.go.id, semuanya **benar-benar dibuka** lewat web fetch dan diverifikasi
isinya cocok dengan yang dikutip (lihat `HASIL-UJI.md` untuk rincian verifikasi sitasi).

---

## Penilaian: apa yang lebih baik berkat skill

| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Akurasi alur teknis | **Salah** — masih pakai alur DJP Online/e-Filing lama, bukan Coretax | Benar — sesuai Coretax DJP 2026, diverifikasi ke sumber resmi |
| Sitasi | Tidak ada sama sekali | 3 sumber resmi pajak.go.id, semua dibuka & dicocokkan isinya |
| Klaim tanpa dasar | Ada ("tingkat kepatuhan terus meningkat" — karangan) | Tidak ada; klaim tanpa sumber ditandai `[perlu sumber]` bila muncul |
| Kepercayaan pembaca/klien konsultan pajak | Rendah — tidak bisa dibuktikan, berisiko reputasi bila salah | Tinggi — bisa ditelusuri ulang ke pajak.go.id |
| Kesiapan pakai | Terlihat siap pakai tapi **berbahaya** karena info usang | Siap pakai dan akurat per tanggal akses |

**Kesimpulan:** skill memberi nilai tambah **jelas dan besar** — bukan hanya menambah format sitasi,
tapi mencegah kesalahan faktual signifikan (alur pelaporan yang sudah tidak berlaku) yang akan muncul
kalau agent hanya mengandalkan pengetahuan umum tanpa riset web sungguhan. Untuk domain yang berubah
cepat (pajak, regulasi), ini bedanya artikel yang aman dipublikasi vs. yang berisiko menyesatkan klien.
