# C16 — Uji panduan beta tester (simulasi Akun C)

**Tanggal:** 2026-10-13 UTC  
**Tester:** simulasi internal (bukan tester VIP nyata)  
**Lingkungan:** VM Cursor Cloud, OpenClaw lokal (`run-uji.sh`, HOME terpisah `c16-beta`), **tanpa** bot produksi / bot uji Telegram  
**Paket:** `dist/komunitech-vip-beta-uji-internal-akun-c-7f9fe557c103.zip` (KMT-7F9F-E557-C103) — **tidak** di-commit ke repo

## Ringkasan

| Langkah panduan | Hasil | Catatan |
|-----------------|-------|---------|
| Build & terima ZIP | OK | `python3 scripts/build.py --pembeli "Beta - uji internal Akun C" --vip --beta` ~2 s; ZIP ~9,4 MB |
| Ekstrak | OK | `CARA-INSTAL.md`, `LISENSI.txt`, 140 folder skill + `docs/`, `solusi-vip/`, `templates/` |
| Pasang 3 skill beta | OK | Salin folder dari ZIP ke HOME uji (setara bagian 3 panduan); watermark lisensi terbaca di `SKILL.md` |
| Kalimat uji Hari 1 (3 skill) | OK | Semua tanda berhasil panduan tercapai (lihat bawah) |
| Formulir §7 (simulasi) | Diisi | Label SIMULASI per skill |

**Verdik panduan:** bisa diikuti oleh tester awam **bila** sudah punya OpenClaw + Terminal; bagian Telegram/OpenClaw tetap dominan — tester hanya Claude/Cursor perlu baca FAQ §8 dengan saksama.

---

## Langkah demi langkah (waktu perkiraan)

1. **Unduh/buat ZIP** (~2 menit) — satu perintah build; jelas untuk tim, tester nyata menerima dari Telegram.
2. **Ekstrak** (~1 menit) — banyak folder; panduan Hari 1 sudah memperingatkan “>100 folder” dan menunjuk 10 nama beta — **cukup**, tapi awam bisa kaget sebelum sampai bullet itu.
3. **Pasang skill** (~5 menit simulasi) — panduan menawarkan seret folder **atau** `openclaw skills install ./nama-skill --global` dari folder ekstrak; keduanya masuk akal. Simulasi: salin 3 folder ke `~/.openclaw/skills/` (HOME uji).
4. **Percakapan baru + kalimat uji** (~2–3 menit per skill, total ~2,5 menit agent) — lihat hasil di bawah.
5. **Formulir** (~15 menit untuk 3 skill simulasi) — salin-tempel §7 jelas.

---

## Hasil kalimat uji (tanda berhasil panduan)

### `kelayakan-investasi-usaha`

- **Perintah:** `Hitung kelayakan beli mesin kopi Rp25 juta, omzet tambahan Rp4 juta per bulan.`
- **Tanda berhasil:** jawaban tegas **LAYAK** + balik modal + tabel angka (NPV, IRR).
- **Waktu agent:** ~49 s.
- **Tools:** `read`, `exec` (script jalan).

### `simulasi-cicilan-pinjaman`

- **Perintah:** `Motor 25 juta, DP 20%, 3 tahun, bunga 0,8% per bulan. Cicilannya berapa? Mahal nggak?`
- **Tanda berhasil:** cicilan **Rp715.556/bulan**, bunga efektif dijelaskan, perbandingan flat vs anuitas.
- **Waktu agent:** ~33 s.

### `tangani-keberatan-pelanggan`

- **Perintah:** `Pelanggan bilang 'kemahalan kak'. Aku jual kopi susu Rp35000.` (placeholder `[produk]`/`[harga]` diganti — sesuai catatan panduan §5)
- **Tanda berhasil:** 3 balasan WA + pertanyaan lanjutan + kapan berhenti; ada `[isian]` yang memang diharapkan bila data kurang.
- **Waktu agent:** ~31 s.

---

## Temuan → usulan perbaikan panduan

| # | Temuan | Usulan |
|---|--------|--------|
| 1 | Setelah ekstrak, `docs/` / `solusi-vip/` / `templates/` sejajar dengan folder skill — awam bisa salah seret ke folder skills | Tambah satu kalimat di §2/§3: “Jangan seret folder `docs`, `solusi-vip`, atau `templates` ke folder skills.” (sebagian sudah ada di §3 Claude Code; ulangi di blok OpenClaw Hari 1) |
| 2 | §5 skill 9 masih menampilkan template `[produk]`/`[harga]` — tester awam mungkin tempel literal | Sudah ada catatan “ganti `[isian]`”; boleh tambah contoh satu baris lengkap (kopi susu Rp35.000) di samping template |
| 3 | Cek skill (`openclaw skills list`) diasumsikan Terminal di mesin OpenClaw — tester VIP hanya HP+Telegram mungkin stuck | Sudah ada “Perlu bantuan” + FAQ; cukup |
| 4 | `pantau-cron-openclaw` / `cek-privasi-openclaw` butuh OpenClaw penuh — tidak diuji run ini (3 skill non-cron) | Sesuai scope C16 |

**Perubahan `docs/panduan-beta-tester.md`:** usulan #1 diterapkan commit terpisah bila pemilik setuju; run ini **tidak** mengubah panduan (hanya catat).

---

## Formulir masukan SIMULASI (§7)

### kelayakan-investasi-usaha

1. Platform & OS: OpenClaw lokal, Linux (VM Cursor), simulasi tanpa Telegram  
2. Instalasi: Ya (salin folder dari ZIP)  
3. Pemakaian nyata simulasi: 1 (kalimat uji Hari 1)  
4. Kegunaan: 5  
5. Langsung dipakai: Sering (perlu koreksi asumsi omzet bersih)  
6. Lama: tanpa skill ~30 menit spreadsheet; dengan skill ~1 menit + baca  
7. Hasil aneh: tidak  
8. Disukai: verdict jelas + skenario meleset  
9. Perbaiki: ingatkan awam bedakan omzet kotor vs bersih lebih awal  
10. Harga wajar: Rp99rb  
11. Testimoni: Tidak (simulasi)

### simulasi-cicilan-pinjaman

1. Platform & OS: sama  
2. Instalasi: Ya  
3. Pemakaian: 1  
4. Kegunaan: 5  
5. Langsung dipakai: Selalu  
6. Lama: tanpa skill ~20 menit; dengan skill ~1 menit  
7. Hasil aneh: tidak  
8. Disukai: bunga efektif dijelaskan dengan bahasa awam  
9. Perbaiki: —  
10. Harga wajar: Rp49rb  
11. Testimoni: Tidak (simulasi)

### tangani-keberatan-pelanggan

1. Platform & OS: sama  
2. Instalasi: Ya  
3. Pemakaian: 1  
4. Kegunaan: 4  
5. Langsung dipakai: Sering (isi `[isian]` dulu)  
6. Lama: tanpa skill ~15 menit; dengan skill ~1 menit  
7. Hasil aneh: tidak  
8. Disukai: nada WA natural + “kapan berhenti”  
9. Perbaiki: contoh produk/harga konkret di §5  
10. Harga wajar: Rp49rb  
11. Testimoni: Tidak (simulasi)

---

## Run 2 (C17) — 2026-10-13 ~22:40 UTC

**Skill:** `rapor-mingguan-ai`, `landing-page-siap-tayang`, `cek-risiko-dan-asuransi-usaha`  
**HOME uji:** `c17-beta` (3 skill, `run-uji.sh`, tanpa Telegram)  
**Paket:** skill disalin dari repo workspace (setara isi ZIP beta; tidak rebuild `dist/`).

### Hasil kalimat uji (tanda berhasil panduan)

| Skill | Perintah (FIKSI) | Tanda berhasil | Waktu agent (perkiraan) | Catatan |
|-------|------------------|----------------|-------------------------|---------|
| `cek-risiko-dan-asuransi-usaha` | Kafe ruko dekat sungai, 3 karyawan — risiko & asuransi | Tabel risiko + skor + langkah murah + jenis asuransi + disclaimer | ~66 s | Script `exec`; dana darurat minta input lanjutan (sesuai skill) |
| `landing-page-siap-tayang` | Landing jasa servis AC, WA 0812-3456-7890 | `index.html` utuh di chat, `wa.me/6281234567890`, panduan Netlify, FAQ | ~173 s (retry 1× karena lock DB saat uji paralel) | `[isian: …]` masih ada — sesuai panduan |
| `rapor-mingguan-ai` | Rapor minggu ini + 7 percakapan FIKSI | Nilai A–D per kriteria, kesalahan tersering, PR siap tempel | ~106 s (attempt 3; attempt 2 timeout router) | Attempt 1 tanpa percakapan → agent minta tempel ulang (benar) |

### Friksi / temuan panduan

| # | Temuan | Usulan |
|---|--------|--------|
| 1 | Uji 2 skill paralel ke HOME sama → `openclaw.sqlite` busy | Catat di C16/C17: uji beta **serial** per HOME |
| 2 | `rapor-mingguan-ai` butuh percakapan panjang; timeout model bila prompt terlalu berat | Tester awam: tempel percakapan dulu, baru minta rapor (sudah implisit di panduan) |
| 3 | Landing page jawaban panjang (2 bagian HTML) — wajar untuk Telegram | OK |

### Formulir masukan SIMULASI (§7) — Run 2

**rapor-mingguan-ai:** Platform OpenClaw lokal Linux simulasi; instal Ya; 1× uji; kegunaan 4; Sering; tanpa skill ~45 mnt manual vs ~2 mnt; tidak aneh; suka rubrik A–D + PR; perbaiki ingatkan min. 10 percakapan; harga Rp99rb; testimoni Tidak (simulasi).

**landing-page-siap-tayang:** sama; kegunaan 5; Sering setelah isi `[isian]`; tanpa skill ~2 jam vs ~3 mnt + edit; suka HTML mobile-first + WA; perbaiki —; harga Rp99rb; testimoni Tidak (simulasi).

**cek-risiko-dan-asuransi-usaha:** sama; kegunaan 5; Sering; tanpa skill ~1 jam vs ~2 mnt; suka tabel + disclaimer; perbaiki —; harga Rp99rb; testimoni Tidak (simulasi).

---

## Run 3 (C22) — 2026-10-14 ~10:30 UTC

**Skill:** `cek-privasi-openclaw`, `seleksi-cv-pelamar`, `satu-lawan-satu-dan-umpan-balik`, `pantau-cron-openclaw`, `bandingkan-pemasok-vendor`, `rencana-restok-barang`, `panduan-wawancara-kerja`  
**HOME uji:** `c22-<skill>` (1 skill per HOME, `run-uji.sh`, tanpa Telegram)  
**Paket:** skill disalin dari repo workspace (setara isi ZIP beta).

### Hasil kalimat uji (tanda berhasil panduan)

| Skill | Perintah (FIKSI) | Tanda berhasil | Waktu agent (perkiraan) | Catatan |
|-------|------------------|----------------|-------------------------|---------|
| `cek-privasi-openclaw` | Amankah OpenClaw saya? Cek privasi dong. | 🔴/🟡/🟢 + saran perbaikan + izin sebelum ubah | ~189 s | `security audit` + baca config; exec/read |
| `satu-lawan-satu-dan-umpan-balik` | Saya nggak enak negur kasir yang sering telat. | WA ajakan + naskah empat mata + langkah tindak lanjut | ~25 s | `[isian]` wajar bila jam standar belum disebut |
| `seleksi-cv-pelamar` | 3 CV FIKSI admin toko — pilih 2 + pertanyaan + draf WA | Tabel skor kriteria + shortlist + pertanyaan wawancara | ~99 s | 3 CV ringkas (bukan 12); format lengkap |
| `bandingkan-pemasok-vendor` | 3 penawaran tepung 600 kg / 5 hari (FIKSI) | Rekomendasi + tabel peringkat + skor + risiko PPN/tenggat | ~54 s | Selaras contoh uji 01-normal |
| `rencana-restok-barang` | CSV penjualan+stok di workspace — kulakan minggu ini | Blok PESAN SEKARANG + total Rp + per barang | ~52 s | `exec` script; file contoh dari `examples/data/` |
| `panduan-wawancara-kerja` | Rubrik kasir kelontong 45 menit 2 pewawancara (FIKSI) | Kompetensi + pertanyaan STAR + rubrik 1–5 + aturan UU | ~118 s | Jawaban panjang (~12,7 rb karakter) |
| `pantau-cron-openclaw` | Pantau laporan 21.00 & piutang 07.45… / Job terlambat? | Rencana pengawas + konfirmasi "ya" (panduan §5 skill 1) | **GAGAL** | Run 1: timeout router lalu HTTP 530; run 2: 530 langsung — **bukan** kegagalan skill. Kabar HILANG Telegram sudah LOLOS di **C18** (2026-10-13). |

### Usulan kalimat §5 panduan (3 skill baru, belum ada di §5)

**`bandingkan-pemasok-vendor`:** `Tolong bandingin 3 balasan WA supplier [bahan] ini — butuh [jumlah] paling lambat [N] hari lagi:` (tempel chat WA pemasok).

**`rencana-restok-barang`:** `Ini penjualan 90 hari plus stok sekarang toko [jenis toko] — minggu ini harus kulakan apa, berapa?` (tempel CSV atau letakkan file di folder kerja bot).

**`panduan-wawancara-kerja`:** `Buatkan pertanyaan wawancara dan rubrik skor untuk [posisi], wawancara [durasi] menit, [N] pewawancara.`

### Friksi / temuan panduan

| # | Temuan | Usulan |
|---|--------|--------|
| 1 | `pantau-cron-openclaw` di §5 sudah jujur soal alur chat→"ya" belum ujung ke ujung; C22 lokal gagal karena router model, bukan panduan | Tester VIP: ikuti §5 skill 1; tim: ulang C22 lokal bila router hidup |
| 2 | Skill baru (bandingkan/restok/wawancara) belum masuk §5 — tester beta hanya lihat 10 skill fokus | Tambah sub-bagian opsional "Skill VIP lain di ZIP" atau tunggu rilis penuh |
| 3 | `rencana-restok-barang` butuh file CSV di workspace — awam mungkin hanya tempel di chat | Panduan §5 skill baru: sebut "salin file contoh atau tempel tabel penjualan" |

**Perubahan `docs/panduan-beta-tester.md`:** tidak ada (temuan belum terbukti salah langkah; usulan §5 dicatat di atas untuk Akun B).

### Formulir masukan SIMULASI (§7) — Run 3 (ringkas)

Semua: OpenClaw lokal Linux simulasi; instal Ya; 1× uji; kegunaan 4–5; Sering/Selalu setelah isi `[isian]`; tidak aneh (kecuali pantau: tidak teruji); harga wajar Rp49–99rb; testimoni Tidak (simulasi).

---

## Run berikutnya

- **C22 selesai** (6/7 kalimat uji OK; pantau-cron menunggu router / sudah tercover C18 Telegram).
- **C23** konsistensi dokumen vs katalog.
