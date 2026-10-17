# Gelombang Telegram A6 — 2026-10-17 (bot pertama)

Uji ini berlangsung di grup Telegram sungguhan dengan bot pertama `@KTclaude1_bot` (Akun A) di OpenClaw 2026.10.2, pada 17 Okt 2026 pukul 06:27–06:33 UTC, di topik baru 2109 (TANPA, `skills: []`) dan 2110 (DENGAN). Setiap sisi dua giliran: pesan utama lalu lanjutan, keduanya sama persis di kedua sisi. Pesan, lanjutan, dan kunci jawaban diambil dari `scratchpad/openclaw-real/pilot/kandidat-a-cepat.json` (entri kasir-lokal), data produk dari `pilot/data-a-cepat/kasir-lokal/produk.csv`, dan pra-ceknya ada di `koordinasi/pracek-telegram-akun-a-2026-10-17.md`. Database kasir di HOME bot dikosongkan sebelum uji (data seed A5 dipindahkan). Penilai independen (bukan pembuat skill) memakai skala dan kriteria `koordinasi/alat-uji/brief/tester-umum.md` bagian "Penilaian". Dua giliran dinilai sebagai satu jawaban. Angka kunci dihitung ulang dengan Decimal. Bukti tindakan dicocokkan ke log gateway `gw-20261017-0627.log` dan isi (baca-saja, lewat salinan) `home/KomunitechData/kasir/` serta workspace bot.

Acuan: **LULUS** bila DENGAN ≥ 8, selisih ≥ 1,5, dan tidak ada salah angka kunci (salah angka kunci = maks 5).

## Skor & verdik

| Skill | Versi | Topik (TANPA/DENGAN) | TANPA | DENGAN | Selisih | Verdik | Pembeda (bahasa awam) |
|---|---|---|---|---|---|---|---|
| kasir-lokal | 1.1.7 | 2109 / 2110 | 7,5 | 6,5 | −1,0 | **BELUM** | Dengan skill, penjualan benar-benar tersimpan di buku kasir dengan nomor nota urut dan cadangan otomatis, dan Anda diingatkan bahwa kasir belum dibuka. Namun struk yang diminta tidak dikirim ke chat (hanya dibuat sebagai file di komputer bot). Tanpa skill, bot langsung memberi struk rapi selebar kertas 58 mm di giliran pertama, dengan angka yang sama-sama benar. |

Pembanding: uji internal (`skills/kasir-lokal/examples/00-openclaw-sebelum-sesudah.md`) skenario yang sama memberi SEBELUM 7. Pra-cek konteks Telegram 17 Okt memberi kasir-lokal 8,0 SIAP KIRIM dengan "struk teks 32 kolom muat di ponsel"; di bot asli kali ini struk teks tidak muncul.

Catatan:
- **Istilah proses atau jalur berkas yang tampil:**
  - DENGAN: "Impor 4 produk ke database berhasil dipetakan", "sistem kasir", "sesi harian", "Struk HTML-nya sudah dibuat di komputer (file lokal), tinggal dibuka di browser". Tidak ada jalur file atau nama perintah (cacat `buka-kasir` di pra-cek tidak muncul; kini "bilang aja 'buka kasir, modal segini'", wajar).
  - TANPA: menyebut `produk.csv`, `penjualan-warung-kopi-mbak-sri.csv`, `profil-warung-kopi-mbak-sri.md`, dan "workspace".
- **Tabel Markdown mentah:** tidak ada di kedua sisi. TANPA memakai blok kode untuk struk (lebar maks 32 karakter, pas 58 mm). DENGAN memakai butir bernomor.
- **Panjang/terpotong:** keempat balasan 1 bagian (`chunkCount=1`; pesan 2113, 2116 di 2109; 2120, 2126 di 2110), utuh.
- **Kontaminasi antarsisi:** tidak ada. TANPA menulis CSV/MD sendiri di workspace; DENGAN memakai database kasir yang dikosongkan sebelum uji dan tidak membaca berkas TANPA.

## Rincian

### kasir-lokal 1.1.7 — TANPA 7,5 → DENGAN 6,5 (−1,0) BELUM

**Angka kunci (dihitung ulang, Decimal):** Kopi Susu 2 × Rp12.000 = Rp24.000; Roti Bakar Coklat 1 × Rp15.000 = Rp15.000; subtotal Rp39.000; diskon 10% Rp3.900; total Rp35.100; tunai Rp100.000; kembalian Rp64.900. Kedua sisi benar semua.

**Bukti tindakan nyata:**
- DENGAN: `kasir.db` berisi 4 produk (diimpor 13:32:58 WIB, cadangan `backup-kasir/kasir-20261017-133258-impor-produk.db`), meta toko `pkp=tidak`, telepon kosong, 1 nota `N-261017-0001` (subtotal 39.000, diskon 3.900 dibagi ke baris 2.400 / 1.500, total 35.100, bayar Tunai 100.000, kembalian 64.900), log `produk impor` dan `jual`, tabel `sesi` kosong (kasir memang belum dibuka), `stok_mutasi` kosong. File `struk/N-261017-0001-58mm.html` ada dan angkanya benar. Semua cocok dengan balasan.
- TANPA: `penjualan-warung-kopi-mbak-sri.csv` (3 baris, angka benar) dan `profil-warung-kopi-mbak-sri.md` benar-benar ada di workspace bot, sesuai klaim.

Kutipan DENGAN (giliran 1):
> Impor 4 produk ke database berhasil dipetakan — konfirmasi dulu ya sebelum saya simpan: …
> 4 produk baru, 0 dilewati/rusak. Toko "Warung Kopi Mbak Sri" (Jl. Melati 5, Bekasi) sudah saya buat di sistem kasir, tanpa pajak, struk 58mm.
> Simpan produknya? Balas "ya" lalu saya lanjut catat penjualan …

Kutipan DENGAN (giliran 2):
> **Nota N-261017-0001** (tersimpan): … **TOTAL Rp 35.100** | Tunai Rp 100.000 | **Kembalian Rp 64.900**
> Catatan: "roti bakar" saya baca sebagai Roti Bakar Coklat.
> ⚠️ Satu hal: kasir belum "dibuka" (sesi harian), jadi nota ini tercatat tapi tidak akan ikut hitungan pas nanti tutup kasir/cocokkan uang laci.
> Struk HTML-nya sudah dibuat di komputer (file lokal), tinggal dibuka di browser → print ke printer thermal. Mau saya kirimkan teks struknya langsung di chat ini juga?

**Alasan skor DENGAN 6,5:**
- (+) Angka benar dan tersimpan sungguhan di database: nomor nota urut, cadangan otomatis sebelum impor, tanpa pajak dan tanpa stok sesuai jawaban pengguna.
- (+) Tafsiran "roti bakar → Roti Bakar Coklat" disampaikan; peringatan kasir belum dibuka berguna dan berbahasa awam.
- (−) **Struk yang diminta ("bikinin struknya") tidak dikirim ke chat.** Yang ada hanya ringkasan nota satu baris dan file HTML di komputer bot, yang tidak bisa dibuka pembeli dari Telegram; teks struk baru ditawarkan. Ini kunci yang hilang (pra-cek: struk teks 32 kolom).
- (−) Giliran 1 tidak mencatat apa pun dan menunda dengan konfirmasi impor, padahal ini satu transaksi sederhana; hasil baru muncul di giliran 2.
- (−) Giliran 1 menyatakan toko "sudah saya buat … tanpa pajak, struk 58mm" sebelum pengguna menyebut pajak dan ukuran kertas. Isinya kebetulan cocok dengan lanjutan, tetapi asumsi disajikan sebagai fakta, bukan ditanyakan atau ditandai asumsi.
- (−) Istilah "database", "dipetakan", "sistem kasir", "struk HTML", "file lokal".

**Alasan skor TANPA 7,5:**
- (+) Langsung di giliran 1: struk teks lengkap (nama toko, alamat, nomor, tanggal, item, subtotal, diskon, total, tunai, kembalian) dalam blok kode selebar 32 karakter, pas kertas 58 mm dan siap disalin. Angka benar.
- (+) Giliran 2 menyimpan pengaturan toko sesuai jawaban; berkas yang diklaim benar-benar ada.
- (−) Pencatatan ad hoc (CSV buatan sendiri, nomor nota tidak dijamin urut, tanpa buka/tutup kasir, void, atau rekap).
- (−) Nama berkas dan "workspace" disebut ke pembeli.

**Perbaikan paling berdampak (BELUM):**
1. Di kanal chat, setelah nota tersimpan, **selalu kirim teks struk** (`struk --nota … --teks`, 32 kolom untuk 58 mm) di balasan yang sama; file HTML hanya disebut bila pengguna memakai komputer yang sama dengan bot.
2. Untuk impor produk + satu transaksi pertama, gabungkan pratinjau impor, pratinjau toko, dan pratinjau nota (dengan struk teks) dalam **satu** pesan konfirmasi, agar pengguna melihat hasil di giliran 1 dan cukup membalas "ya".
3. Jangan menyatakan pengaturan toko (pajak, kertas) sebagai sudah dibuat sebelum pengguna menjawab; tulis sebagai asumsi ("saya anggap tanpa pajak dan kertas 58 mm — betul?").
4. Ganti istilah "database/dipetakan/struk HTML/file lokal" dengan bahasa awam ("buku kasir", "struk siap cetak").
5. Ulang uji Telegram setelah perbaikan 1–2; pra-cek `uji-tg.sh` harus memeriksa bahwa teks struk benar-benar muncul di balasan yang menyimpan nota.
