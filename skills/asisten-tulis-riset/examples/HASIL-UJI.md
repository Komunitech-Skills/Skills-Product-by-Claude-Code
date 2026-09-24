# Hasil Uji Independen — asisten-tulis-riset

**Tanggal:** 2026-09-23
**Penguji:** agent penguji independen (simulasi, Claude Code)
**Metode:** membaca SKILL.md/README/references/templates/scripts/tests, menjalankan 5 skenario dengan
riset web SUNGGUHAN (WebSearch + WebFetch), membuka setiap URL di daftar pustaka skenario a–c dan
mencocokkan angka/klaim secara manual, menjalankan `scripts/cek_sitasi.py` pada draf asli + draf rusak
buatan sendiri, menjalankan `tests/test_cek_sitasi.py`, uji A/B, uji banding pesaing, dan uji muat
OpenClaw otomatis.

## 1. Audit keamanan (ringkas)

- `scripts/cek_sitasi.py`: Python stdlib murni (`argparse`, `json`, `re`, `sys`), **tidak ada** panggilan
  jaringan, tidak ada perintah destruktif, tidak membaca kredensial/SSH/browser data. Aman dijalankan.
- SKILL.md/README/references/templates: tidak ditemukan instruksi tersembunyi/prompt injection (tidak
  ada perintah untuk mengabaikan pengguna, mengirim file ke luar, atau mematikan konfirmasi). Tidak ada
  API key/token/data pribadi tertanam.
- `ATTRIBUTION.md` jujur mengungkap bahwa repo sumber inspirasi (`ComposioHQ/awesome-claude-skills`)
  tidak dibuka/disalin karena tidak ada LICENSE terverifikasi — konsisten dengan aturan kurasi
  CLAUDE.md.
- **Kesimpulan keamanan: AMAN.**

## 2. Verifikasi sitasi (skenario a–c) — WAJIB dibaca

Setiap URL di ketiga skenario riset **dibuka langsung** (WebFetch) dan dicocokkan dengan klaim di draf.

| # | Sumber | Dibuka? | Klaim yang dikutip | Cocok dengan isi sumber? |
|---|---|---|---|---|
| A[1] | pajak.go.id/en/node/119081 | Ya | Alur Coretax, data prepopulated, reset password otomatis | Cocok persis |
| A[2] | pajak.go.id/en/node/119105 | Ya | Syarat curi start, langkah buat SPT Normal, sumber "kegiatan usaha" | Cocok persis |
| A[3] | pajak.go.id/en/node/106827 | Ya | Denda Rp100.000, tenggat 31 Maret, dasar hukum UU KUP/Ciptaker | Cocok persis |
| B[1] | data.goodstats.id (sumber sekunder, mengutip BPS) | Ya | 4,4 juta unit, +15,3%, Rp1.288,93 triliun, 99,08% domestik, 66,87% Jawa | Cocok persis; **secara jujur ditandai sebagai sumber sekunder** karena bps.go.id menolak akses (403) |
| B[2] | cnbcindonesia.com/.../transaksi-e-commerce-tembus... | Ya | Rp134,67 triliun, +4,93% qtq, +3,74% yoy, 1,44 miliar transaksi | Cocok persis |
| B[3] | apjii.or.id/berita/.../221-juta-orang | Ya | 221.563.479 pengguna, penetrasi 79,5%, naik dari 78,19%, tanggal 7 Feb 2024 | Cocok persis |
| C[1] | ojk.go.id (siaran pers SNLIK 2025) | Ya | Literasi 66,46% (dari 65,43%), inklusi 80,51% (dari 75,02%), 10.800 responden, 34 provinsi, periode survei | Cocok persis |

**Tingkat akurasi sitasi (skenario a–c, draf final): 7/7 = 100%.** Tidak ditemukan sumber atau angka
karangan pada draf final. Angka yang tidak bisa dikonfirmasi ke satu rilis resmi (pertumbuhan yoy ~20%
di skenario B, rilis APJII 2025) **ditandai `[perlu sumber]`** sesuai aturan, bukan dipaksakan sebagai
fakta.

**Catatan penting proses (bukan cacat pada draf final, tapi temuan risiko nyata):** pada draf kerja awal
skenario B, kutipan [2] sempat memakai URL `kabarbisnis.com` yang **belum benar-benar dibuka** — hanya
diambil dari ringkasan jawaban WebSearch yang terdengar meyakinkan dan sudah menyertakan angka + daftar
"Sources". Saat dicoba dibuka langsung, URL itu ternyata mengembalikan **HTTP 403** dan tidak bisa
dibaca. Ini ditemukan & diperbaiki sendiri sebelum draf final (diganti sumber cnbcindonesia.com yang
berhasil dibuka dan berisi angka sama). **Ini bukti nyata risiko yang coba dicegah §ATURAN
ANTI-HALUSINASI poin 1: jawaban ringkasan mesin pencari yang tampil meyakinkan dan berisi angka bukan
jaminan sumbernya sudah benar-benar dibaca isinya.** Lihat §6 Rekomendasi.

## 3. Uji `scripts/cek_sitasi.py` — draf asli & draf rusak

### 3a. Tests otomatis
```
python3 tests/test_cek_sitasi.py
```
**Hasil: 13/13 test lulus (OK).**

### 3b. Draf hasil skenario (setelah perbaikan format URL, lihat §5)
- `01-artikel-spt-umkm.md`: 0 error, 0 peringatan.
- `02-whitepaper-ecommerce-logistik.md`: 0 error, 5 peringatan (semua kalimat statistik yang kutipannya
  ada di kalimat lain dalam paragraf yang sama — heuristik per baris bekerja sesuai desain yang
  didokumentasikan, bukan bug).
- `03-newsletter-koperasi-literasi-keuangan.md`: 0 error, 1 peringatan (idem, heuristik per baris).

### 3c. Draf rusak buatan penguji (edge case)
Dibuat file uji berisi: nomor loncat (`[6]` tanpa dipakai di teks), `[5]` dipakai tapi tidak ada di
pustaka, entri pustaka tanpa URL, URL duplikat dua nomor berbeda, angka Rupiah tanpa kutipan, gaya
sitasi campur (APA + nomor), kutipan berulang wajar (`[3]` dua kali).

**Hasil:** script mendeteksi dengan benar — 2 error keras (`[5]` hilang di pustaka; URL duplikat nomor
`[2]`/`[3]`), 3 peringatan (entri `[4]` tanpa URL, entri `[6]` tidak pernah dikutip, baris Rupiah tanpa
`[n]`). Exit code 1 sesuai desain (ada error keras). **Sesuai ekspektasi.**

File kosong (`""`): error keras "Tidak ditemukan bagian Daftar Pustaka", exit code 1, jumlah
kutipan/entri 0 — **tidak meledak, sesuai ekspektasi** (juga tercakup test otomatis).

File tidak ada: pesan error ramah "Tidak bisa membaca file: ... No such file or directory", exit code 2
— **sesuai ekspektasi.**

**File dengan encoding tidak valid (byte non-UTF-8)** — **CACAT SEDANG ditemukan:**
```
Traceback (most recent call last):
  File ".../scripts/cek_sitasi.py", line 195, in <module>
    main()
  ...
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 131: invalid continuation byte
```
Script **menampilkan traceback Python mentah** (bukan pesan ramah Bahasa Indonesia seperti kasus file
tidak ditemukan) dan keluar dengan kode default. Ini bisa terjadi nyata di dunia pembeli awam — mis. draf
ditempel dari Word/aplikasi lain yang menyisipkan karakter aneh, atau file diedit di editor dengan
encoding berbeda (Windows Notepad lama, dsb.). Untuk audiens awam yang jadi target Komunitech, traceback
mentah membingungkan dan terkesan "aplikasi rusak" — **lihat rekomendasi di §6.**

**"URL tidak terbaca" palsu pada entri pustaka yang aslinya PUNYA URL — CACAT SEDANG ditemukan:**
`POLA_ENTRI_PUSTAKA` hanya mencocokkan baris yang **diawali** `[n]`; bila entri pustaka ditulis melebar
ke baris berikutnya (format yang justru **dicontohkan sendiri** di `references/gaya-sitasi.md`, mis.
```
[1] Statistik E-Commerce 2025. Badan Pusat Statistik. 2025. https://www.bps.go.id/publikasi/... .
    Diakses 24 September 2026.
```
— dan pada draf uji awal penguji, URL sempat ditulis di baris kedua), maka script **melaporkan
"Entri [n] tidak punya URL yang terbaca"** padahal URL-nya nyata dan ada, hanya salah baris. Ini
peringatan (bukan error keras) sehingga tidak menggagalkan proses, tapi berpotensi membuat
penulis/pembeli panik menganggap sumbernya dicurigai karangan padahal hanya soal pemformatan baris.
Lihat rekomendasi konkret di §6.

## 4. Uji A/B (wajib) — `00-pembanding-tanpa-skill.md`

Kondisi tanpa skill menghasilkan artikel yang **terlihat lancar dan meyakinkan** tapi (a) memakai alur
DJP Online/e-Filing lama yang sudah tidak berlaku untuk pelaporan 2026 (seharusnya Coretax DJP), dan
(b) menyelipkan klaim "berdasarkan data DJP, tingkat kepatuhan pelaporan SPT UMKM terus meningkat"
tanpa sumber apa pun — persis pola halusinasi yang coba dicegah skill. Kondisi dengan skill akurat dan
bisa ditelusuri. **Skill memberi nilai tambah besar dan jelas**, bukan hanya kosmetik sitasi.

## 5. Uji banding pesaing (wajib) — `00-banding-pesaing.md`

Pesaing relevan ditemukan: **`grounded-citations`** (NousResearch/hermes-agent, lisensi MIT, dibaca
untuk dinilai, tidak disalin). Pesaing lebih kuat secara **mekanis** (ledger `url→[n]` yang mencegah ID
karangan secara struktural + verifikasi kutipan verbatim otomatis oleh script), tapi skill kita lebih
unggul untuk **kebutuhan pembeli**: konteks Indonesia penuh (BPS/OJK/BI/SINTA, gaya sitasi awam, aturan
SEO, penolakan tugas kuliah), dan **tanpa setup** (pesaing perlu CLI multi-perintah `reset/add/render/
verify`, tidak cocok untuk pembeli awam). **Skill kita tidak kalah secara keseluruhan** — lihat §6 untuk
ide yang layak diadopsi dari pesaing.

## 6. Cacat & rekomendasi perbaikan konkret

### BERAT
Tidak ditemukan cacat berat pada isi/keamanan skill maupun pada draf final (setelah koreksi sumber di
§2). Anti-halusinasi, penolakan etika, dan sitasi berfungsi seperti dijanjikan.

### SEDANG
1. **`cek_sitasi.py` crash dengan traceback mentah pada file berencoding bukan UTF-8**
   (`scripts/cek_sitasi.py` baris ~157–169, fungsi `main()`). Saran: tambahkan `UnicodeDecodeError` ke
   blok `except` yang sudah menangani `OSError`, beri pesan ramah seperti "Tidak bisa membaca file —
   pastikan file disimpan dengan encoding UTF-8 (coba buka & simpan ulang lewat editor teks biasa)",
   exit code 2 (konsisten dengan kasus file tidak ditemukan).
2. **False warning "tidak punya URL" saat entri pustaka melebar ke baris berikutnya**
   (`POLA_ENTRI_PUSTAKA`, baris ~32, dan `ambil_entri_pustaka`, baris ~66–79 — regex hanya membaca satu
   baris per entri). Ini bertentangan dengan contoh format di `references/gaya-sitasi.md` sendiri yang
   menunjukkan entri boleh melebar 2 baris. Saran: gabungkan baris lanjutan (baris berikutnya yang TIDAK
   diawali `[n]` dan bukan baris kosong) ke entri sebelumnya sebelum dicek URL-nya — atau, lebih
   sederhana dan lebih aman: ubah instruksi di §7 Draf & §8 SKILL.md serta contoh di
   `references/gaya-sitasi.md`/`templates/daftar-pustaka.md` agar **secara eksplisit meminta satu
   entri = satu baris tanpa pelipatan**, supaya format selalu cocok dengan asumsi script.
3. **Risiko sumber "terverifikasi semu" dari ringkasan mesin pencari** (temuan proses di §2). SKILL.md
   §4 "Kumpulkan sumber" sudah bilang "benar-benar buka" tiap sumber, tapi tidak secara eksplisit
   memperingatkan bahwa **jawaban ringkasan alat pencarian web** (yang sering sudah menyertakan angka +
   daftar "Sources" yang terlihat meyakinkan) **bukan pengganti** membuka URL-nya satu per satu dengan
   alat pengambil halaman (fetch). Saran: tambahkan kalimat eksplisit di §4 SKILL.md, mis. "Jangan
   menganggap sumber sudah 'dibuka' hanya karena alat pencarian menampilkan cuplikan/ringkasan berisi
   angka meyakinkan disertai daftar tautan — tetap buka URL-nya satu per satu dengan alat pengambil
   halaman (fetch) sebelum mengutip, karena ringkasan pencarian bisa salah rangkum atau salah kaitkan
   angka ke sumber."

### RINGAN
4. Meta description pada draf skenario A hanya berupa teks italic tanpa label eksplisit "Meta
   description:" — SKILL.md §Format output sudah menyebut label ini; instruksikan agent lebih tegas
   untuk selalu memberi label jelas (bukan hanya italic) supaya pembeli awam langsung tahu bagian mana
   yang harus ditempel ke field SEO situsnya.
5. Panjang whitepaper "singkat" tidak punya patokan kata eksplisit di SKILL.md (hanya "3–5 halaman"
   untuk whitepaper umum); hasil uji skenario B jadi ±915 kata, di bawah ekspektasi umum "whitepaper
   singkat" pembeli. Saran: tambahkan patokan kata untuk newsletter (±400–800) dan whitepaper singkat
   vs lengkap di tabel §Input SKILL.md.
6. Tidak ada patokan jumlah sumber minimum untuk newsletter (hanya artikel & whitepaper yang diberi
   angka di §4). Newsletter skenario C hanya pakai 1 sumber — sudah sesuai aturan yang ada (karena tidak
   diatur), tapi longgarnya aturan ini berisiko newsletter jadi terlalu tipis riset. Saran: tambahkan
   patokan longgar (mis. minimal 1–3 sumber tergantung panjang) di §4.

## 7. Skor kualitas (1–10 per kriteria)

| Kriteria | Skor | Alasan |
|---|---|---|
| Pemicu (description tepat) | 9 | Kata kunci ID & EN lengkap (artikel/blog/SEO/whitepaper/newsletter/materi presentasi/research writing/content writing/cek sumber/anti-halusinasi), batasan cakupan jelas ("TIDAK untuk caption/kalender medsos", "TIDAK untuk tugas kuliah/skripsi") sehingga tidak akan salah trigger atau salah tidak-trigger di skenario uji manapun |
| Kemudahan awam | 8 | Alur brief→riset→kerangka→draf jelas, bahasa instruksi tidak jargon, tapi §Input meminta hingga 5 pertanyaan sekaligus untuk kasus topik kosong — masih dalam batas wajar dan sesuai prinsip CLAUDE.md, hanya bisa dirasa agak panjang bagi pengguna paling malas |
| Kualitas output | 9 | Ketiga draf riset (a–c) siap tempel, terstruktur, nada sesuai audiens masing-masing (konsultan pajak, startup logistik, koperasi), disclaimer tepat di tempat yang butuh |
| Akurasi (angka/fakta) | 9 | 7/7 sitasi diverifikasi cocok dengan sumber asli; klaim tak terverifikasi ditandai jujur `[perlu sumber]`; dikurangi sedikit karena proses awal sempat nyaris mengutip sumber yang belum dibuka (lihat §2 & §6.3) — meski akhirnya dikoreksi sendiri sebelum diserahkan |
| Penanganan input kurang | 9 | S4 ditangani persis sesuai §Input: maksimal 5 pertanyaan bernomor + opsi jalan cepat dengan asumsi disebutkan |
| Penanganan di luar cakupan | 10 | S5a (skripsi) & S5b (minta data karangan) keduanya ditolak tegas dengan alasan jelas dan alternatif konstruktif, konsisten 100% dengan §2 dan §ATURAN ANTI-HALUSINASI |
| Keamanan | 10 | Script stdlib murni, tidak ada jaringan/destruktif/kredensial, tidak ada prompt injection |

**SKOR AKHIR: 8/10 — LULUS (≥7).**

Alasan skor akhir (bukan rata-rata otomatis): skill ini sudah kuat di bagian yang paling krusial untuk
produk berbayar — penolakan etika/karangan data sempurna, dan akurasi sitasi akhir 100% pada 7 sumber
yang diuji. Skor tidak diberi 9–10 karena dua cacat SEDANG yang nyata dan mudah dieksploitasi tanpa
sadar: (1) script bisa crash mentah pada file berencoding aneh, situasi yang realistis untuk pembeli
awam yang tempel-tempel dari berbagai aplikasi; (2) format sitasi 2-baris yang **dicontohkan sendiri**
oleh `references/gaya-sitasi.md` memicu peringatan palsu "URL tidak terbaca" dari script pendampingnya
sendiri — inkonsistensi internal antara dokumentasi dan alat bantu yang perlu diperbaiki sebelum rilis
luas. Tidak ada cacat BERAT (tidak ada sumber/angka karangan lolos ke draf final, tidak ada pelanggaran
keamanan), sehingga skor tetap di atas ambang lulus.

## 8. Uji muat OpenClaw otomatis

Dijalankan `openclaw skills install --global` lalu `openclaw skills check --json` pada instalasi bersih
(OpenClaw 2026.9.5). Hasil: `asisten-tulis-riset` **eligible: true, modelVisible: true,
commandVisible: true, blocked: false, disabled: false, missingRequirements: false**. **Lulus uji muat
OpenClaw.**

## 9. Kolom `platform_teruji`
`openclaw (otomatis, uji muat skills check); claude-code (simulasi agent, 5 skenario penuh + verifikasi
sitasi manual)` — belum ada uji manusia langsung di platform (Codex/Cursor/OpenClaw interaktif); jangan
klaim "teruji" di platform tersebut sampai Tahap 6.10 (uji platform asli oleh pemilik/tim) dilakukan.
