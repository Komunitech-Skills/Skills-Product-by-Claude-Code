---
name: perjanjian-sederhana
description: Menyusun draf surat perjanjian sederhana berbahasa Indonesia dengan struktur pasal standar (para pihak, ruang lingkup, hak & kewajiban, harga & pembayaran, jangka waktu, wanprestasi, keadaan memaksa, penyelesaian sengketa, tanda tangan & meterai Rp10.000) untuk reseller/distributor, supplier/pemasok, NDA/kerahasiaan, sewa tempat, sewa alat, kerja sama bagi hasil, dan jasa freelance, plus checklist sebelum tanda tangan. Gunakan saat pengguna minta surat perjanjian, kontrak, MoU (agreement, contract, NDA). Bukan untuk jual beli tanah, investasi, pihak asing, atau kontrak kerja karyawan.
---

# Perjanjian Sederhana

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; file baru hanya ditulis di folder kerja yang disepakati (bukan /tmp); lokasinya disebut di terminal/IDE, sedangkan di aplikasi chat (Telegram/WhatsApp) jalur, folder, dan nama berkas **tidak pernah** disebut.

## Tujuan
Membantu pelaku usaha kecil dan profesional membuat draf perjanjian yang rapi, seimbang, dan mudah dipahami. Draf memakai struktur pasal yang lazim di Indonesia, angka dan terbilangnya dihitung ulang dengan rumus pasti, pasal berisiko ditandai, dan disertai checklist sebelum tanda tangan. Ini draf, bukan nasihat hukum.

## Kapan digunakan
- "Buatkan surat perjanjian reseller / kerja sama supplier / NDA / sewa kios / sewa alat / bagi hasil / kontrak freelance."
- Pengguna punya kesepakatan lisan/chat dan ingin dituangkan jadi perjanjian tertulis.
- Pengguna ingin mengecek draf perjanjian buatannya (kelengkapan pasal, angka vs terbilang, meterai).

## Kapan TIDAK digunakan (tolak menyusun draf, rujuk ke profesional)
Rincian dan template jawaban penolakan ada di `references/batasan-rujukan.md`:
- Jual beli/hibah/balik nama **tanah, rumah, bangunan** (termasuk PPJB) → notaris/PPAT.
- **Investasi**, saham, pendirian PT/CV, imbal hasil tetap/pasti, menghimpun dana dari banyak orang → pengacara/notaris, cek aturan OJK.
- Pihak **asing**/valuta asing → pengacara (wajib dwibahasa, UU 24/2009 Ps. 31).
- Utang-piutang dengan **jaminan** (sertifikat, BPKB, fidusia), perjanjian **kerja karyawan**, waralaba/lisensi merek, kontrak **pemerintah/BUMN**, dan kasus yang **sudah bersengketa** → profesional terkait.
- Isi yang melanggar hukum → tolak.
- Surat non-perjanjian (surat kuasa, pernyataan, undangan) → skill `surat-resmi`. Penawaran harga → `surat-penawaran-harga`. Proposal kerja sama (belum mengikat) → `proposal-kerjasama`.

Saat menolak, tetap bantu: daftar dokumen yang perlu disiapkan, pertanyaan untuk dibawa ke notaris/pengacara, dan ringkasan kesepakatan (bukan perjanjian).

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Jenis perjanjian | Ya | — (tebak dari konteks, konfirmasi) |
| Identitas para pihak: nama, NIK, alamat (dan jabatan + nama badan usaha bila mewakili PT/CV) | Ya | Isian `[isi: ...]` untuk diisi tangan |
| Objek: produk/barang/tempat/alat/pekerjaan + rincian | Ya | — (tanyakan) |
| Harga, cara & jadwal bayar | Ya (kecuali NDA) | Sesuai default di template |
| Jangka waktu | Tidak | Default per template (mis. 12 bulan) |
| Kota penandatanganan & penyelesaian sengketa | Tidak | Musyawarah 30 hari → Pengadilan Negeri kota Pihak Pertama |
| Posisi pengguna (pihak mana) | Tidak | Peran PIHAK PERTAMA/KEDUA mengikuti template (mis. klien = PIHAK PERTAMA, freelancer = PIHAK KEDUA); sebutkan posisi pengguna di ringkasan |

Jika info wajib kurang, tanyakan **sekali** dalam satu pesan (maks 5 pertanyaan bernomor). Contoh untuk sewa kios:
1. Nama, NIK, dan alamat pemilik dan penyewa?
2. Alamat kios, luas, dan nomor sertifikatnya (atau dasar hak menyewakan)?
3. Harga sewa, lama sewa, dan dibayar sekaligus atau bertahap? Ada uang jaminan?
4. Siapa yang bayar listrik, air, dan iuran?
5. Kamu di posisi pemilik atau penyewa?
Jika pengguna ingin cepat, isi dengan default template, biarkan data pribadi sebagai `[isi: ...]`, dan cantumkan daftar asumsi.

## Langkah kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.
1. **Saring batasan** (daftar "Kapan TIDAK digunakan"). Nilai ≥ Rp500 juta atau jangka > 5 tahun: boleh dibuat, tetapi beri judul "DRAF BAHAN DISKUSI, WAJIB DITINJAU PENGACARA".
2. **Pilih template** di `templates/`: `reseller-distributor.md`, `supplier-pemasok.md`, `nda-kerahasiaan.md`, `sewa-tempat.md`, `sewa-alat.md`, `bagi-hasil.md`, `jasa-freelance.md`. Baca blok PANDUAN AGENT di atasnya (info wajib, default, peringatan). Kombinasi (mis. reseller + NDA) → gabungkan pasal dari `references/klausul-pilihan.md`.
3. **Hitung semua angka lewat script** (path relatif terhadap folder SKILL.md ini; Windows: `python`/`py`):
   ```bash
   python3 <folder-skill-ini>/scripts/perjanjian.py tanggal 2026-09-23            # kalimat "Pada hari ini, Rabu, tanggal ..."
   python3 <folder-skill-ini>/scripts/perjanjian.py tanggal                       # tanggal TT belum disebut -> [isi: tanggal]
   python3 <folder-skill-ini>/scripts/perjanjian.py terbilang "Rp 7.500.000"      # Rp 7.500.000 (tujuh juta lima ratus ribu rupiah)
   python3 <folder-skill-ini>/scripts/perjanjian.py termin --total "Rp 7.500.000" --persen 50,50 --nama "Uang muka,Pelunasan"
   python3 <folder-skill-ini>/scripts/perjanjian.py bagihasil --persen 60,40 --pihak "Pemodal,Pengelola" --contoh "Rp 10.000.000"
   python3 <folder-skill-ini>/scripts/perjanjian.py denda --nilai "Rp 5.000.000" --persen-per-hari 0,1 --hari 30 --maks-persen 5
   python3 <folder-skill-ini>/scripts/perjanjian.py sampai 2026-10-01 --bulan 12     # berakhir 30 September 2027
   python3 <folder-skill-ini>/scripts/perjanjian.py retainer --per-bulan "Rp 3.000.000" --bulan 6 --mulai 2026-10-01
   python3 <folder-skill-ini>/scripts/perjanjian.py meterai --rangkap 2            # kuitansi: --jenis kwitansi --nilai ...
   ```
   Pembulatan: ke rupiah terdekat (0,5 ke atas). Sisa pembulatan termin/bagi hasil masuk ke baris terakhir agar total tepat.
4. **Isi template.** Ganti setiap `[isi: ...]` dengan data pengguna. Data yang belum diketahui biarkan `[isi: ...]` agar terlihat. Hanya satu gaya isian: `[isi: ...]` (jangan `[[...]]`, `____`, atau `<...>`).
   **Tanggal penandatanganan jangan diisi sendiri** (hari ini belum tentu hari tanda tangan): bila pengguna tidak
   menyebutnya, pakai `perjanjian.py tanggal` tanpa argumen → `Pada hari ini, [isi: hari], tanggal [isi: tanggal] ...`.
   **Default template** yang dipakai tanpa disebut pengguna (mis. denda keterlambatan 0,1%/hari maks 5%, siapa
   menanggung PBB/iuran, batas revisi, jangka waktu) wajib dicantumkan di bagian "Asumsi dari template" pada
   output sebagai hal yang **perlu dikonfirmasi**, lengkap dengan nilainya. Hapus blok PANDUAN AGENT. Pertahankan tanda `> ⚠ TINJAU PENGACARA` pada pasal berisiko. Jangan menambah klaim (halal, BPOM, izin) yang tidak diberikan pengguna. Seimbangkan hak kedua pihak. Jangan membuat pasal yang hanya menguntungkan pengguna secara tidak wajar. **Pengakhiran/pengosongan** default: teguran tertulis → tenggat → pemberitahuan → musyawarah/pengadilan. Klausul pengosongan/pengambilalihan sepihak (kunci, segel, bongkar, ambil paksa, sisa sewa hangus) hanya bila pengguna sendiri memintanya, sebagai opsi dari `references/klausul-pilihan.md` lengkap dengan peringatan risiko ⚠ TINJAU PENGACARA.
5. **Cek konsistensi kewajiban para pihak.** Buat daftar pos biaya: listrik, air, internet, kebersihan/keamanan, iuran lingkungan, iuran/retribusi pengelola pasar/gedung, PBB/pajak, perbaikan besar, perbaikan kecil. Setiap pos dibebankan ke **satu pihak saja** (atau tertulis jelas "dibagi ... %"), dan pihak itu **sama** di semua pasal (hak & kewajiban, harga, uang jaminan) **dan** di "Asumsi dari template". Jangan menulis pos yang sama di kewajiban kedua pihak.
6. **Periksa draf:** simpan ke file lalu jalankan `python3 <folder-skill-ini>/scripts/perjanjian.py cek draf.md`. Perbaiki semua temuan "Harus diperbaiki" (angka vs terbilang, penomoran pasal, meterai, bagian standar, **"Beban '...' bertentangan"** dari cek konsistensi beban biaya; baris "Beban biaya per pos" dipakai untuk mencocokkan daftar asumsi). Temuan "Rujuk profesional" (tanah/PPJB/kavling, investasi/keuntungan tetap per bulan, pinjaman berbunga/BPKB/jaminan, harga jual kembali minimum, pihak asing, dll.) → kembali ke langkah 1. Uji regresi pemeriksa: `python3 <folder-skill-ini>/scripts/uji_regresi.py`.
7. **Sajikan teks perjanjian LENGKAP di balasan chat** — bukan hanya nama berkas atau ringkasan pasal. Pengguna (mis. di Telegram/WhatsApp) harus bisa langsung menyalin naskah utuh dari chat, karena lampiran bisa gagal terkirim.
   - **Format kanal chat:** naskah dikirim sebagai **teks biasa**, BUKAN di dalam blok kode (```), tanpa judul Markdown `#`/`##` (judul ditulis huruf kapital biasa, mis. `PASAL 3 — HARGA SEWA`), dan Lampiran ditulis sebagai baris pendek (mis. `1. Pintu rolling door: baik`), bukan tabel `|`. Pecah menjadi "Bagian 1/N", "Bagian 2/N", dst., **tiap bagian < 3.800 karakter**, dipotong **hanya di antara pasal** (atau sebelum Lampiran/penutup), lalu catatan (yang perlu dilengkapi, asumsi, pasal ditinjau, checklist, disclaimer) sebagai pesan terakhir. Cara pasti: `python3 <folder-skill-ini>/scripts/perjanjian.py bagi draf.md` (keluaran sudah teks biasa, berlabel "Bagian i/N", pesan dipisah baris `<<<PESAN BERIKUTNYA>>>` — baris pemisah itu tidak ikut dikirim). Isi pasal tidak boleh berubah.
   - **Jangan sebut lokasi berkas.** Bila draf juga disimpan sebagai berkas, tulis hanya: "Draf juga sudah saya simpan sebagai berkas. Balas 'kirim file' bila mau dikirim sebagai dokumen." Tanpa jalur, nama folder, atau nama berkas.
   - **Jangan sebut alat kerja.** Di balasan tidak boleh ada kata script, skrip, tool, exec, atau python. Tulis hasilnya saja, mis. "angka & terbilang sudah dihitung ulang", "draf sudah diperiksa ulang: tidak ada beban biaya yang bertentangan".
   - Sebelum mengirim, simpan balasan ke berkas sementara lalu jalankan `python3 <folder-skill-ini>/scripts/perjanjian.py cek-balasan balasan.txt`; perbaiki sampai status SIAP KIRIM.
   - Jangan menulis "naskah lengkap ada di file" tanpa menampilkan naskahnya. Bila pengiriman lampiran gagal, tetap tampilkan naskah utuh di chat.
   - Tutup dengan tawaran versi .docx/PDF atau penyesuaian pasal. Di terminal/IDE (bukan chat) lokasi berkas boleh disebut.

### Fallback jika Python tidak bisa dijalankan
Beri tahu pengguna (tanpa menyebut Python/alat) bahwa angka dihitung manual dan mohon dicek ulang. Tanggal berakhir = sehari sebelum tanggal yang sama pada bulan/tahun berikutnya (mis. 1 Okt 2026 + 12 bulan → 30 Sep 2027). Aturan: terbilang ditulis per kelompok tiga digit (triliun, miliar, juta, ribu); "seribu" dan "seratus" untuk angka 1; 11 = "sebelas", 12–19 = "... belas". Termin = total × persen, dibulatkan ke rupiah, termin terakhir = total − jumlah termin lain. Denda = nilai × persen/hari × hari, maksimal batas yang disepakati. Meterai = Rp10.000 × jumlah rangkap asli. Cek kelengkapan pasal dengan daftar di "Checklist" di bawah secara manual.

## Format output
```
**⚠ Draf ini bukan nasihat hukum.** [ringkas 1 kalimat + status: SIAP DITINJAU / PERLU DILENGKAPI]

--- (draf perjanjian LENGKAP sebagai teks biasa di chat, siap salin: judul, nomor, pembuka tanggal, para pihak, latar belakang, PASAL 1..n, penutup, tanda tangan + [Meterai Rp10.000], lampiran baris pendek. Pecah "Bagian 1/N" < 3.800 karakter, potong antar-pasal. Tanpa blok kode, judul #, tabel |. Berkas hanya tambahan, tanpa jalur.) ---

YANG MASIH PERLU DILENGKAPI
- [isi: ...] yang tersisa (dari hasil pemeriksaan draf), termasuk tanggal penandatanganan bila belum disebut

ASUMSI DARI TEMPLATE (MOHON DIKONFIRMASI)
- Denda keterlambatan: <nilai default, mis. 0,1%/hari dari jumlah terlambat, maks. 5%> — Pasal X
- <default lain yang dipakai tanpa disebut pengguna: PBB/iuran, jangka waktu, batas revisi, dll.> — pihak penanggung tiap biaya harus SAMA dengan pasalnya

PASAL YANG SEBAIKNYA DITINJAU PENGACARA
- Pasal X: alasan singkat

SYARAT SAH PERJANJIAN (PASAL 1320 KUHPERDATA)
Sepakat · Cakap · Hal tertentu · Sebab halal → 1 baris status masing-masing untuk draf ini

CHECKLIST SEBELUM TANDA TANGAN
(8–12 poin relevan, dari references/checklist-tanda-tangan.md)

CATATAN METERAI
Surat perjanjian wajib bermeterai Rp10.000 berapa pun nilainya (UU 10/2020); 2 rangkap asli = 2 meterai. Meterai bukan syarat sah, tetapi diperlukan bila dokumen dipakai sebagai alat bukti.

_Disclaimer: Draf ini disusun otomatis berdasarkan informasi dari Anda, mengacu pada ketentuan yang berlaku per 23 September 2026. Ini bukan nasihat hukum dan tidak menggantikan pengacara/notaris. Untuk nilai besar atau kasus kompleks, mintalah peninjauan profesional._
```

## Contoh
**Input pengguna:** "Buatin kontrak freelance desain logo buat klien toko kue, harga 7,5 juta, DP 50%, revisi 2x, selesai 3 minggu. Aku desainernya."

**Output (dipotong; di chat ditulis sebagai teks biasa, bukan blok kode):**
```
⚠ Draf ini bukan nasihat hukum. Status: PERLU DILENGKAPI (identitas & rekening).
Bagian 1/3

PERJANJIAN JASA DESAIN LOGO
...
PASAL 3 — BIAYA JASA DAN PEMBAYARAN
(1) Biaya jasa untuk seluruh Pekerjaan adalah Rp 7.500.000 (tujuh juta lima ratus ribu rupiah).
(2) a. uang muka 50% sebesar Rp 3.750.000 (tiga juta tujuh ratus lima puluh ribu rupiah) ...
...
Pasal yang sebaiknya ditinjau pengacara: Pasal 6 (Hak atas Hasil Karya) bila logo akan didaftarkan sebagai merek.
```

**Di luar cakupan:** "Bikinin perjanjian jual beli tanah kavling 300 juta" → tolak menyusun draf, jelaskan perlunya akta PPAT, beri daftar dokumen (sertifikat, PBB, KTP/KK, surat nikah/persetujuan pasangan) dan pertanyaan untuk notaris.

## Checklist sebelum mengirim hasil
- [ ] Jenis perjanjian tidak termasuk daftar tolak; nilai besar diberi peringatan.
- [ ] Ada: judul & nomor, pembuka tanggal, identitas para pihak, latar belakang, ruang lingkup, hak & kewajiban, harga & pembayaran (kecuali NDA), jangka waktu, wanprestasi, keadaan memaksa, penyelesaian sengketa, lain-lain, tanda tangan + meterai.
- [ ] Semua nominal ditulis `Rp 1.250.000 (terbilang)` dari hasil hitung langkah 3; `cek` tidak melaporkan ketidakcocokan.
- [ ] Pasal berisiko bertanda ⚠ dan dirangkum; daftar `[isi: ...]` tersisa disebutkan; tidak ada `[[...]]`.
- [ ] Checklist sebelum tanda tangan, catatan meterai, dan disclaimer tercantum.
- [ ] Naskah perjanjian utuh tampil di balasan chat, bukan hanya nama berkas.
- [ ] Kanal chat: teks biasa (tanpa blok kode, judul #/##, tabel |); "Bagian 1/N" masing-masing < 3.800 karakter, dipotong antar-pasal (`bagi`).
- [ ] Tidak ada jalur/folder/nama berkas; bila disimpan, hanya kalimat "Draf juga sudah saya simpan sebagai berkas. Balas 'kirim file' bila mau dikirim sebagai dokumen."
- [ ] Tidak ada kata script/skrip/tool/exec/python di balasan; `cek-balasan` berstatus SIAP KIRIM.
- [ ] Tiap pos biaya (listrik, air, iuran/retribusi, PBB/pajak, perbaikan) ditanggung satu pihak dan sama di semua pasal + daftar asumsi; `cek` tidak melaporkan "bertentangan".
- [ ] Tanggal tanda tangan tidak diisi sendiri; default template (denda, PBB/iuran, dll.) tercantum di "Asumsi dari template".
- [ ] Bahasa Indonesia baku tetapi mudah dipahami; tidak ada klaim/izin karangan.

## Batasan & penanganan error
- Script keluar dengan kode ≠ 0 dan pesan `GALAT: ...` (nominal tak terbaca, persen tidak 100%, file kosong/.docx, tanggal salah). Perbaiki input sesuai pesan.
- `cek` hanya pemeriksa bantu (pola teks), bukan penilaian hukum.
- Dasar hukum & tanggal berlaku: `references/regulasi.md`. Aturan bisa berubah; sarankan cek peraturan.bpk.go.id atau konsultasi.
- Data pribadi (NIK, alamat) hanya dipakai untuk draf. Jangan disimpan atau dikirim ke tempat lain.
