# Hasil Review Independen — kantor-manajemen & kripto-keuangan (2026-09-29)

Reviewer independen (bukan pembuat). Tidak ada commit. Tidak ada file diubah selain berkas ini.

## Skor
| Paket | Skor | Ringkas |
|---|---|---|
| kantor-manajemen | 7/10 | Isi akurat, aturan pemilik dipatuhi. Kurang di celah bundle dan bahasa untuk pemilik awam |
| kripto-keuangan | 7/10 | Kepatuhan larangan kripto sangat baik. Bundle tidak memuat skill inti, dan langkah awam kurang jelas |

## Hasil cek
1. **Skill ada di catalog.csv:** semua 22 skill yang dirujuk ada di catalog.csv dan foldernya ada, semua berstatus `lulus`
   (`vikunja-tugas` tercatat teruji `claude-code (simulasi agent)` dan uji muat openclaw).
2. **Perintah jadwal:** semua perintah `openclaw automations add` di kedua `jadwal-openclaw.md` sama persis (flag, cron, argv)
   dengan `references/openclaw-jadwal.md` skill sumbernya atau paket `usaha-offline`/`konsultan`. Tidak ada flag karangan.
   Yang ditambahkan pembuat sendiri: kalimat "JANGAN memberi rekomendasi..." pada prompt ringkasan pagi kripto (menguatkan aturan),
   dan penggantian `<chat-id...>` dengan `"<ID ...>"`. Keduanya aman.
3. **Aturan pemilik:** Telegram sebagai default, WA hanya nomor terpisah plus persetujuan tertulis, tidak ada broadcast.
   Tugas dari grup WA berupa draf yang dikonfirmasi manusia, piutang berupa draf yang dikirim staf.
   Pelacakan tugas dinyatakan bukan pengawasan karyawan. Tidak ada data pribadi member.
   Kripto: pencarian "sinyal / rekomendasi beli / entry / target profit / target harga" hanya muncul dalam konteks penolakan
   atau larangan. Disclaimer risiko ada di awal PANDUAN dan di setiap jadwal.
4. **Validasi:** `validate.py` lulus (92 skill valid). `build.py --pembeli "UJI" --bundle paket-kantor-manajemen --izinkan-draft`
   berhasil (16 skill). `dist/` sudah dibersihkan.

## Temuan

### TINGGI
- **T1. Bundle kripto tidak memuat `pantau-pasar-kripto`.** Skill inti (notifikasi harga, ringkasan pagi, riset, jurnal) hanya ada di
  "akses penuh VIP" (tercatat di `solusi-vip/README.md`), padahal PANDUAN Bab 2, 5a–5e, dan jadwal §1–2 mengandalkannya.
  Pembeli bundle akan gagal di `openclaw skills install ./pantau-pasar-kripto`. Usulan: masukkan ke bundle (status `lulus`),
  atau tandai jelas di PANDUAN "khusus VIP".
- **T2. Bundle kantor tidak memuat `laporan-harian-usaha`, `frappe-books-usaha`, `dolibarr-usaha`.** PANDUAN Bab 1 menyebut
  `laporan-harian-usaha` sebagai "skill inti", dan Bab 5a–5b, jadwal §1–2, §6, dan §9 memakainya. Ini tidak akan terpasang untuk
  pembeli bundle. Usulan: tambahkan `laporan-harian-usaha` ke bundle, atau beri label VIP-only di PANDUAN dan CEKLIS
  (CEKLIS juga mencantumkannya sebagai skill inti).

### SEDANG
- **S1. Overclaim `laporan-harian-usaha` untuk perusahaan distribusi.** PANDUAN 5a berkata "merangkum penjualan/stok". Skill sumbernya
  membaca kasir-lokal, buku-stok, absensi-lokal, pengingat, dan crm-wa. Tanpa kasir-lokal, "penjualan" hanya berupa `omzet_tercatat`
  dari buku-stok. Perusahaan distribusi besar yang tidak memakai alat-alat itu hanya akan mendapat laporan stok. Perlu kalimat jujur.
- **S2. Overclaim jurnal kripto.** PANDUAN kripto 5e menyebut skill "boleh menunjukkan pola (mis. kapan Anda sering keluar terlalu
  cepat)". `SKILL.md` pantau-pasar-kripto hanya merapikan jurnal dan menghitung P/L lewat script, tidak ada fitur analisis pola.
  Hapus kalimat itu atau tulis "Anda bisa menilai sendiri dari tabel". Analisis pola perilaku juga berdekatan dengan saran transaksi.
- **S3. Data harus diisi dulu, tapi tidak disebut.** `buku-stok` (5j) dan `buku-piutang` (5j) mengandalkan data yang sudah dicatat.
  PANDUAN kantor tidak berkata "isi stok/piutang awal dulu (impor Excel)". Pemilik awam akan menerima laporan kosong dan mengira gagal.
  Kalimat "data belum ada, laporan bilang kosong" di 5a belum cukup.
- **S4. Blok `openclaw skills install` (kantor Bab 1) mencantumkan `frappe-books-usaha` DAN `dolibarr-usaha`.**
  Teks di bawahnya bilang pilih salah satu. Pemilik awam akan menyalin seluruh blok. Pisahkan jadi blok opsional/komentar.
- **S5. Klaim regulasi kripto yang tidak bisa diverifikasi dari repo.** "Masa transisi berakhir 20 Januari 2026 ... beralih dari
  Bappebti ke OJK" (Bab 0). Kalimat penutup sudah memberi peringatan. Sarankan menyebut sumber/tanggal cek, atau mengutip
  `skills/pantau-pasar-kripto/references/regulasi.md` agar konsisten.

### RENDAH
- R1. Kedua PANDUAN merujuk "Bab 5k–5l" sebelum dijelaskan, dan 5f/5g bergantung pada Vikunja yang baru dipasang di 5k.
  Urutan langkah membingungkan; tambahkan "lewati 5f–5g sampai Vikunja terpasang".
- R2. Ikon 🔴🟡🟢 dan tanda ✅/📖/⚠️ di `jadwal-openclaw.md` perlu penjelasan satu baris (legenda ada, tapi teknis).
- R3. `jadwal-openclaw.md` kantor §7 mengarah ke Bentuk A tanpa perintah lengkap (merujuk skill). Cukup, tapi pembuat sebaiknya
  menyalin satu contoh.
- R4. Windows: `python3` diganti `py` di kantor, `python` di kripto. Samakan (`py`/`python`) dan tetap diberi label "belum diuji".
- R5. Status jadwal buku-stok/agent dan piutang ditandai ✅/📖 secara jujur. Tidak ada masalah, hanya catatan bahwa pengiriman nyata
  ke Telegram tetap belum pernah diuji (sudah tertulis).

## Simulasi pembaca awam

### Pemilik perusahaan distribusi, 50 tahun (kantor-manajemen/PANDUAN.md)
Langkah yang berpotensi membingungkan:
1. **Prasyarat 0.2** menyebut "Gateway OpenClaw", "VPS", "mini PC" tanpa penjelasan singkat "Gateway = program OpenClaw yang
   berjalan di komputer". Pilihan (a)–(d) tanpa rekomendasi default untuk kantor besar.
2. **Bab 1**: 19 baris perintah `openclaw skills install` di terminal. Tidak dijelaskan cara membuka terminal, cara masuk ke folder
   hasil ekstrak ZIP, atau bahwa ini pekerjaan staf IT. Tidak ada saran "minta staf IT / jasa setup" di titik ini (S4 juga berlaku).
3. **Bab 3** memakai "opsi `--samarkan`", "UU PDP (Bab 3)" tanpa arti awam.
4. **Bab 4** (BotFather, token, pairing, `@userinfobot`, ID chat) adalah tugas teknis paling rawan di seluruh paket. Tidak ada
   gambar/tangkapan layar, dan tidak ada opsi "minta staf IT mengerjakan langkah 4".
5. **Bab 5**: semua rutinitas memakai kalimat chat ("Aktifkan laporan..."), sedangkan `jadwal-openclaw.md` berisi perintah terminal
   dengan `NAMA`, path panjang, `--command-argv`. PANDUAN tidak menjelaskan kapan cukup mengetik ke bot dan kapan harus membuka
   `jadwal-openclaw.md`. Di §10 jadwal, membuat jadwal lewat chat diakui bisa gagal.
6. **5f/5g** bergantung pada Vikunja (5k) yang belum terpasang. **5j** butuh data stok/piutang yang belum ada (S3).
7. **6**: `openclaw automations list --all` disebut tanpa konteks. Cukup kalimat chat, sudah ada.

### Member penasaran kripto (kripto-keuangan/PANDUAN.md)
1. **Bab 0** (penjelasan auto-trading) panjang dan muncul sebelum langkah pemasangan; pemula bisa tersesat. Usulan: pindah ke akhir
   atau ringkas 3 baris di awal.
2. **Bab 1**: sama seperti kantor (Gateway/VPS tidak dijelaskan).
3. **Bab 2**: skill `pantau-pasar-kripto` tidak ada di bundle (T1).
4. **Bab 5a**: istilah "ambang" dan file `kripto/PANTAU.md`, `konfigurasi.json` tanpa penjelasan; member mengira harus mengeditnya.
5. **5b–5c**: kalimat chat ("kirimi saya...") vs. perintah terminal di `jadwal-openclaw.md` tanpa petunjuk. 5c "uji dulu dengan
   data tenang lalu data ambang terlewati" tidak bisa dilakukan awam; arahkan ke `SKILL.md` atau jasa setup.
6. **5g**: Docker + Open Notebook untuk pemula kripto. Sudah ada tawaran jasa setup dan alternatif 5d/5h. Cukup.
7. **Bab 4**: token BotFather/pairing (sama seperti di kantor).

## Yang sudah baik (dipertahankan)
- Setiap langkah punya "Cara cek berhasil" dan "Kalau gagal".
- Larangan kripto konsisten di PANDUAN, CEKLIS, jadwal, dan skill sumber (bahkan menolak "ambang yang bagus").
- Legenda verifikasi jujur (✅/📖/⚠️), Telegram belum diuji pengiriman nyata dinyatakan terbuka.
- Kepatuhan UU PDP dan pemberitahuan ke karyawan disebut eksplisit; digest tugas difokuskan pada "pekerjaan macet", bukan siapa malas.
- Nama merek pihak ketiga disertai keterangan tidak berafiliasi.

## Perbaikan yang dilakukan reviewer
Tidak ada (tidak ditemukan typo/tautan rusak yang sepele).

---

## Review ulang (2026-09-29)

Checklist 1–5 dijalankan ulang. `validate.py` lulus (92 skill). Build `paket-kantor-manajemen --izinkan-draft` berhasil (16 skill), `dist/` dibersihkan. Perintah jadwal tidak berubah (tidak ada flag baru); hanya label [VIP]/[PILIH SATU] dan teks ditambahkan.

| Temuan awal | Status |
|---|---|
| T1 bundle kripto tanpa `pantau-pasar-kripto` | Selesai. Bundle ecer kripto dihapus, paket ditandai khusus VIP di PANDUAN, README solusi-vip, dan `bundles/README.md` |
| T2 bundle kantor tanpa laporan-harian/Frappe/Dolibarr | Selesai. Ditandai [VIP] dan [PILIH SATU] di PANDUAN, CEKLIS, jadwal, dan ada catatan untuk pembeli ecer |
| S1 overclaim laporan-harian-usaha | Selesai. 5a menyebut sumber data dan batasannya |
| S2 klaim analisis pola jurnal | Selesai. Diganti "tidak menganalisis pola perilaku" |
| S3 data awal | Selesai. Ada bagian "isi data awal dulu" dan catatan di CEKLIS |
| S4 blok install Frappe+Dolibarr | Selesai. Dipisah dengan panduan memilih |
| S5 tanggal transisi OJK | Selesai. Tanggal dihapus, diarahkan ke ojk.go.id |
| R1 urutan 5f/5g/5k | Sebagian. Vikunja tetap dipasang di Bab 1, tapi tidak ada catatan "lewati 5f-5g sampai terpasang" |
| Simulasi awam | Membaik. Kotak "Mulai dari sini", definisi Gateway, terminal diserahkan ke staf IT/jasa setup. Sisa: Bab 4 (BotFather/pairing) tanpa gambar |

Larangan kripto (sinyal, rekomendasi, entry, target) tetap hanya muncul sebagai penolakan. Disclaimer ada. Tidak ada data pribadi.

**Isu baru (rendah):**
- Kantor 5a merujuk `rekap-penjualan-csv` (ada di catalog.csv, tetapi tidak termasuk daftar skill paket ini; sebutkan perlu dipasang terpisah).
- Sisa R1 di atas.

**Skor baru:** kantor-manajemen 8.5/10, kripto-keuangan 8.5/10.

## Tindak lanjut koordinator (2026-09-29)
- `rekap-penjualan-csv` ditambahkan ke `bundles/paket-kantor-manajemen.txt` (dirujuk di 5a).
- R1: catatan "Lewati sampai Vikunja terpasang" sudah ada di awal bagian 5f (baris ±209) — dianggap selesai.
- Bab 4 (BotFather/pairing) tetap teknis → kandidat perbaikan bersama untuk semua paket (dan jasa setup).
- Status: kedua paket **siap dipakai member VIP** (8,5/10).
