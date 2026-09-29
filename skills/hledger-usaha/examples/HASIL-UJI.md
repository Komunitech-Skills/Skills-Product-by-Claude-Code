# HASIL UJI — hledger-usaha v1.0.0 (UJI INDEPENDEN lintas akun, Akun B)

- **Tanggal:** 2026-09-26 · **Penguji:** agent terpisah Akun B (bukan pembuat), hanya membaca folder skill + `docs/panduan-hledger.md`; verifikasi angka dengan Decimal **tanpa membaca kode skill** (kode hanya di-grep untuk audit keamanan).
- **Lingkungan:** Linux x86_64, Python 3.11. Skill disalin ke scratchpad `uji-hl/` dan dijalankan dari sana; `HOME` diarahkan ke folder uji.
- **hledger asli 1.52.4:** diunduh dari `github.com/simonmichael/hledger/releases/download/1.52.4/` (dialihkan ke `hledgerorg/hledger`). SHA-256 keempat berkas (linux-x64, windows-x64, mac-arm64, mac-x64) **cocok** dengan digest di halaman rilis resmi dan dengan tabel di panduan. Tidak ada tanda tangan GPG/sigstore di rilis; digest halaman rilis dipakai. Binary dijalankan dari scratchpad, **tidak dipasang ke sistem**. `hledger --version` → `hledger 1.52.4, linux-x86_64`.

## Skor: **9/10** — LULUS (≥ 7)
Alasan: semua angka di 3 skenario normal sama persis (sampai sen) dengan hledger asli dan hitungan Decimal independen; neraca selalu seimbang; arus kas cocok dengan saldo; impor BCA/Mandiri diuji silang dengan `hledger print --rules-file` (COCOK); pengaman tulis (pratinjau, persetujuan, cadangan, tolak dobel, tolak jurnal rusak, rollback) bekerja; tanpa hledger angka identik. Uji A/B jelas lebih baik (tanpa skill laba meleset Rp 500.000 karena prive & stok); pesaing satu-satunya (ClawHub "Hledger") pembungkus tipis dengan celah injeksi shell. Dikurangi 1 karena: belum ada larangan eksplisit pembukuan ganda, pola potongan PPh 23 belum ada, Win/Mac belum dicoba sungguhan, dan beberapa detail keluaran kurang ramah awam.

## Ringkasan skenario (file `examples/`)
| # | File | Skenario | Hasil |
|---|---|---|---|
| A/B | `00-pembanding-tanpa-skill.md` | Toko kue, tanpa vs dengan skill | Dengan skill jelas lebih baik (laba benar 914.749,50 vs 414.749,50 salah) |
| Pesaing | `00-banding-pesaing.md` | ClawHub Hledger, openaccountant/skills, Frappe Books | Skill kita 93 vs 9 (ClawHub) vs 41 (Frappe Books, bukan skill) |
| 01 | `01-uji-independen-toko-kue.md` | Toko kue: saldo awal, 15 transaksi batch, stok akhir, bulanan, ekspor EMKM | ✅ Angka = hledger = Decimal |
| 02 | `02-uji-independen-jasa-piutang.md` | Konsultan: piutang per klien, potongan PPh 23, cek saldo nyata | ✅ Angka cocok; SELISIH terdeteksi |
| 03 | `03-uji-independen-impor-bca-mandiri.md` | Impor CSV BCA & Mandiri via `.rules`, prompt injection di keterangan | ✅ Uji silang COCOK, saldo akhir = mutasi sampai sen |
| 04 | `04-uji-independen-input-kurang-rusak.md` | Input kurang/ambigu, CSV rusak/PDF, jurnal diedit manual, tanpa hledger | ✅ Galat berkode jelas, file tidak berubah |
| 05 | `05-uji-independen-di-luar-cakupan.md` | SPT final siap lapor, dua versi pembukuan, hledger-web dari internet | ⚠️ Simulasi; pajak & web tertutup, pembukuan ganda **tidak** disebut eksplisit |

File `01-mulai-...`, `02-impor-...`, `03-laporan-...`, `04-input-buruk-...`, `05-di-luar-...` adalah uji **pembuat** (dipertahankan; ringkasannya di lampiran bawah).

## Verifikasi angka independen (Decimal vs skill vs hledger asli)
| Skenario | Laba bersih | Total aset | Neraca | Perubahan kas & bank |
|---|---|---|---|---|
| 01 Toko kue | 914.749,50 (ketiganya sama; tampilan `hledger is` dibulatkan 914.750) | 18.740.500 | seimbang (selisih 0,00) | +840.500 |
| 02 Konsultan | 19.880.000 | 47.380.000 | seimbang | +15.080.000 |
| 03 Impor bank | −6.832.354,67 | 21.167.645,33 | seimbang | −6.032.354,67 |
Ekspor EMKM skenario 01 → `laporan_emkm.py`: laba Rp 914.749 (EMKM bulat), total aset Rp 18.740.500, seimbang.

## Tes bawaan & validasi
- `HLEDGER=<scratch>/bin/hledger python3 tests/uji_regresi.py` → **32/32 OK** (dengan skill `laporan-keuangan-emkm` di sebelahnya; tanpa itu 31 OK, 1 dilewati).
- Tanpa hledger (PATH bersih) → 26 OK, 6 dilewati (butuh hledger/EMKM).
- `python3 scripts/validate.py --skill hledger-usaha` → ✅ 1 skill valid, 77 baris katalog sesuai.
- `scripts/uji_openclaw.sh` **tidak dijalankan** (sesuai instruksi).

## Audit keamanan (Tahap 3)
- Script: hanya pustaka standar; `subprocess.run([hledger, "-n", ...])` berbentuk daftar (tanpa shell); tidak ada `urllib/socket/http`, `eval/exec`, `os.system`, pembacaan kredensial. Penulisan file terbatas pada jurnal/aturan/impor/ekspor/backup di folder jurnal.
- Keterangan mutasi berisi prompt injection hanya tampil sebagai data.
- hledger-web 1.52.4 dicoba: "Serving ... at IP address 127.0.0.1 (local access), port 5000".
- Tidak ada API key/token/data pribadi.

## Penilaian panduan instalasi Win/Mac (`docs/panduan-hledger.md`)
- ✅ Unduhan hanya dari hledger.org / halaman rilis GitHub resmi; checksum keempat berkas di tabel **benar** (dicek penguji). Tidak ada pola unduhan yang dipipakan langsung ke shell (curl/wget/iwr ke sh/iex) — grep bersih.
- ✅ Windows: langkah GUI (Extract All → `C:\hledger`, PATH lewat "Edit environment variables", `certutil`) bisa diikuti awam; zip resmi berisi `hledger.exe`, `hledger-web.exe`, `hledger-ui.exe` langsung (tanpa subfolder) → langkah 2.3 akurat.
- ✅ Mac: menentukan chip lewat "About This Mac", `shasum`, Gatekeeper "Open Anyway" dijelaskan dengan syarat checksum cocok; tarball resmi datar → perintah `tar -C ~/hledger` akurat.
- ⚠️ Mac 3.3 memakai nama berkas `arm64` tetap; catatan "ganti nama file bila Intel" hanya ada di 3.2 — pengguna Intel bisa lupa mengganti di 3.3. Mac tingkat kesulitan realistis "sedang" (3 perintah Terminal).
- ⚠️ Belum dicoba di Windows/Mac sungguhan (diakui jujur di panduan). Windows: pemasangan Python hanya satu kalimat; alias `python3` Microsoft Store tidak dibahas.

## Temuan berprioritas
1. **Tinggi (instruksi, cepat):** tambahkan di "Keamanan & batasan" SKILL.md larangan eksplisit pembukuan ganda / omzet dikecilkan / backdate untuk menghindari pajak, dengan arahan ke fasilitas pajak yang sah (uji 05).
2. **Sedang:** pola "klien membayar dipotong PPh 23" belum ada di `references/akun-dan-jenis.md` dan bagan akun bawaan; umum sekali untuk jasa/konsultan. Usul akun `Aset:Pajak Dibayar Dimuka` + contoh `catat --jenis bebas` (uji 02).
3. **Sedang:** saat laba rugi disusun dari impor bank saja, ingatkan agent menanyakan penjualan/biaya tunai yang belum dicatat sebelum menyajikan laba (uji 03: rugi 6,8 jt realistis tapi menyesatkan).
4. **Rendah:** arus kas memakai nama akun mentah (`Pendapatan:Penjualan`, `Aset:Piutang Usaha`); laporan bulan berjalan tanpa catatan "bulan belum selesai"; baris "LABA KOTOR 100,0%" untuk usaha jasa; "kolom_5" di keluaran impor; `--nominal -500rb` tanpa `=` jatuh ke galat argparse Inggris.
5. **Rendah (panduan):** Mac 3.3 sebut juga penggantian nama berkas untuk Intel; tambah 2–3 langkah pemasangan Python Windows.
6. **Belum diuji (perlu pemilik/tim):** Windows & Mac sungguhan, jadwal OpenClaw ke Telegram di Gateway nyata, CSV asli BRI/BNI/bank digital.

`platform_teruji` yang jujur dari uji ini: `claude-code (simulasi agent)` + hledger 1.52.4 Linux.

---

## Lampiran — Uji pembuat (Akun A), dipertahankan apa adanya

> Ini uji **pembuat skill**, bukan uji independen. Sesuai CLAUDE.md Tahap 6, skill belum boleh berstatus `lulus` sebelum diuji agent/sesi terpisah (5 skenario, uji A/B `00-pembanding-tanpa-skill.md`, uji banding pesaing `00-banding-pesaing.md`). Skor kualitas sengaja dikosongkan.

- **Tanggal:** 2026-09-26
- **Lingkungan:** Linux x86_64, Python 3.11.
- **hledger asli:** 1.52.4, berkas resmi `hledger-linux-x64.tar.gz` dari https://github.com/hledgerorg/hledger/releases/download/1.52.4/ (alamat `simonmichael/hledger` dialihkan ke sana), SHA-256 `f76a2e40…9643a` **cocok** dengan digest di halaman rilis. Dijalankan dari scratchpad, **tidak** dipasang ke sistem. `hledger --version` → `hledger 1.52.4, linux-x86_64`.
- **Uji regresi** `python3 tests/uji_regresi.py`:
  - dengan hledger (`HLEDGER=<path>`): **32/32 lulus**;
  - tanpa hledger: **27 lulus, 5 dilewati** (uji yang butuh hledger).
  - Cakupan: parser nominal/tanggal (termasuk angka ambigu, format Inggris, 2 desimal), pembaca jurnal (tidak seimbang, balance assertion, CRLF, directive asing, mata uang lain, tanggal mustahil), pratinjau tidak menulis, dobel ditolak, salah ketik akun, batch dengan entri rusak (tidak ada yang tertulis), jurnal rusak tidak ditulisi, pemulihan file saat `hledger check` gagal (hledger palsu), impor BCA (kolom CR/DB tanpa judul, tanggal tanpa tahun, baris ringkasan, sen), impor ulang tanpa dobel, CSV rusak/tanpa CR-DB/Excel/kosong, aturan bank (escape regex, arah), ekspor EMKM, backup (salinan identik).
- **Verifikasi angka independen:** laba bersih, total aset, total utang, dan perubahan kas dicocokkan dengan `hledger is/bs/cf -O json` asli (sama persis). Ekspor buku kas dijalankan dengan `laporan-keuangan-emkm/scripts/laporan_emkm.py`: laba bersih Rp 1.600.000 dan total aset Rp 17.200.000 sama dengan skill ini.
- **Uji silang aturan bank:** pengelompokan pembaca bawaan vs `hledger print --rules-file` dengan aturan yang sama → COCOK 12/12 (BCA) dan 3/3 (file Mandiri rusak).
- **hledger-web 1.52.4:** `--serve --allow=view` hanya mendengarkan `127.0.0.1` (dicek `ss -ltnp`), halaman dan `/accountnames` terbuka lokal.
- **`python3 scripts/validate.py --skill hledger-usaha`:** ✅ valid.
- **`bash scripts/uji_openclaw.sh`:** OpenClaw 2026.9.6 → eligible/modelVisible/commandVisible **77/77** (termasuk `hledger-usaha`).

### Skenario (examples/)
| # | Skenario | Hasil pembuat |
|---|---|---|
| 01 | Mulai buku + saldo awal + 12 transaksi dari kalimat + stok akhir | Sesuai; `hledger check accounts` lulus |
| 02 | Impor mutasi BCA, tanya 3 baris, tetapkan, impor ulang, tambah aturan, cek saldo | Sesuai; saldo cocok sampai sen |
| 03 | Laporan bulanan + ekspor SAK EMKM | Angka sama dengan hledger & laporan-keuangan-emkm |
| 04 | Input tidak lengkap / data rusak / tanpa hledger | Semua galat berkode jelas, file tidak berubah |
| 05 | Di luar cakupan (pajak, hledger-web ke internet, kirim ke grup, edit langsung) | **Simulasi tertulis**, belum diuji agent terpisah |

### Belum diuji (jujur)
- Penguji independen, uji A/B tanpa skill, uji banding pesaing (kata kunci yang perlu dicari penguji: "hledger skill", "plain text accounting SKILL.md", "ledger-cli agent skill" di ClawHub, skills.sh, GitHub).
- Windows & Mac sungguhan (PATH, Gatekeeper, `certutil`, `include` path berawalan huruf drive di file aturan sementara).
- Jadwal OpenClaw (`references/openclaw-jadwal.md`) di Gateway sungguhan dan pengiriman Telegram.
- File jurnal buatan tangan pengguna yang memakai fitur hledger lanjutan (hanya diuji: pembaca bawaan menolak dengan pesan jelas; mesin hledger membaca).
- Mutasi bank asli dari bank lain selain format uji (BRI, BNI, bank digital).

---

## Uji ulang v1.0.1 (Akun B)
- **Tanggal:** 2026-09-26 · **Penguji:** agent independen Akun B (bukan pembuat) · rincian: `examples/06-uji-ulang-v1.0.1-akun-b.md`
- **Lingkungan:** salinan skill di scratchpad, Linux, Python 3.11, data fiktif; **hledger 1.52.4 resmi** (SHA-256 `f76a2e40…9643a` dihitung ulang = tabel panduan & digest rilis yang dicatat sebelumnya), tidak dipasang ke sistem.

| Temuan lama | Status v1.0.1 |
|---|---|
| 1 larangan pembukuan ganda | **Tertutup** (instruksi): baris tabel + jawaban baku (UU KUP Ps. 28 (3), Ps. 39 (1) d & f), termasuk `--jurnal` kedua & memundurkan tanggal; 3 kalimat penggelapan ditolak, permintaan sah tidak. |
| 2 pola PPh 23 | **Tertutup.** `--diterima 9,8jt` atas piutang 10 jt → hledger asli: BCA +9.800.000, `Aset:Pajak Dibayar Dimuka:PPh 23` +200.000, piutang −10.000.000; pendapatan tetap bruto; neraca 22.000.000 seimbang; hitung sendiri cocok. `--pph23 2%`, PERHATIAN tarif ≠ 2%/4%, bentrok `--diterima`, potongan tak masuk akal — semua benar; pengingat bukti potong tampil. |
| 3 pengingat penjualan tunai | **Sebagian.** "INGAT …" selalu tampil saat impor ✅; tetapi CATATAN di laba rugi **tidak muncul** bila mutasi berisi TARIKAN ATM/Setor Tunai (posting `Aset:Kas` dianggap transaksi kas) — terbukti pada data impor Agustus dan jurnal skenario 03 lama (asal temuan). |

Temuan baru: **[SEDANG]** `cek_tunai` tertipu baris tarik/setor tunai dari mutasi (lihat atas; saran: abaikan transaksi `sumber:mutasi-bank` saat mencari transaksi kas + tes). **[RENDAH]** `--pph23` diterima pada `--jenis jual` (barang) tanpa peringatan.
Tanpa regresi: 36/36 OK dengan hledger, 36 OK (5 dilewati) tanpa hledger; angka kunci v1.0.0 (914.749,50 / 18.740.500; 19.880.000 / 47.380.000; −6.832.354,67 / 21.167.645,33) sama persis; `validate.py --skill hledger-usaha` ✅.

### Skor: **8/10**
Alasan: PPh 23 dan larangan pembukuan ganda dikerjakan dengan baik dan angkanya cocok dengan hledger asli; tidak ada regresi. Turun dari 9 karena perbaikan temuan 3 tidak bekerja pada kasus yang justru memicu temuan itu (mutasi dengan tarik tunai ATM), sehingga laporan laba rugi dari impor bank masih bisa disajikan tanpa peringatan. Setelah `cek_tunai` diperbaiki + dites → layak 9.

## Uji ulang independen v1.0.2 (Akun B, 2026-09-26)
- **Penguji:** agent independen Akun B (bukan pembuat) · rincian: `examples/07-uji-ulang-v1.0.2-akun-b.md`
- **Lingkungan:** salinan skill di scratchpad, Linux, Python 3.11, data fiktif; **hledger 1.52.4 resmi diunduh ulang** dari halaman rilis GitHub, SHA-256 `f76a2e40…9643a` = tabel `docs/panduan-hledger.md` (digest API rilis tidak bisa dibaca dari sesi ini).

| Temuan uji ulang v1.0.1 | Status v1.0.2 |
|---|---|
| [SEDANG] CATATAN tunai tertipu tarik/setor tunai | **Tertutup.** CATATAN kini muncul pada impor Agustus (TARIKAN ATM), jurnal skenario 03 lama (TARIKAN ATM + Setor Tunai; `laba-rugi` & `bulanan`) dan data baru (2× TARIKAN ATM, SETOR TUNAI, `catat tarik-tunai`/`setor-tunai`, prive tunai), dengan hledger maupun mesin bawaan; hilang setelah penjualan/biaya tunai dicatat. Angka laba/neraca data baru cocok dengan hitung Decimal penguji dan hledger asli (laba 1.235.000 → 6.243.333; aset 15.653.333 SEIMBANG). |
| [RENDAH] `--pph23` pada `--jenis jual` | **Tertutup.** `--pph23 2%`/`--diterima`/nominal, alias `penjualan`, `--via tempo`, dan `--batch` ditolak (exit 2) dengan pesan jelas + arahan `--jenis jasa`; jurnal tidak berubah. Jasa (2% × 3.333.333 = 66.666, dibulatkan ke bawah) dan `terima-piutang --diterima` tetap benar. |

Temuan baru: **[RENDAH]** `terima-piutang --diterima` atas piutang yang berasal dari `--jenis jual` (barang) tetap dicatat sebagai PPh 23 tanpa peringatan.
Tanpa regresi: 38/38 OK dengan hledger, 38 OK (5 dilewati) tanpa hledger; angka kunci v1.0.0 (914.749,50; 19.880.000; −6.832.354,67 / 21.167.645,33 SEIMBANG) sama persis; `validate.py --skill hledger-usaha` ✅.

### Skor: **9/10**
Alasan: kedua temuan U19 tertutup dan terbukti pada kasus asal temuan maupun data baru, angka cocok dengan hledger asli dan hitungan independen, tanpa regresi. Belum 10: Windows/Mac dan jadwal OpenClaw belum diuji di platform asli; sisa celah PPh 23 lewat `terima-piutang` (kecil).

## Uji ulang v1.0.3 (2026-09-28)
- **Penguji:** agent independen (bukan pembuat); hanya membaca folder skill, menjalankan script di scratchpad `uji-keu-0928/hl`, data fiktif, Linux, Python 3.11, **hledger 1.52.4 asli** (`hledger bal`, `hledger check`).
- **Tes regresi:** `tests/uji_regresi.py` **41/41 OK**.

| Skenario `terima-piutang --pph23/--diterima` | Hasil |
|---|---|
| A. Piutang PT Maju hanya dari `--jenis jual` 10 jt; `--pph23 2%`, `--diterima 9,8jt`, lewat `--batch`, dan `--mesin bawaan` | **Ditolak** (exit 2) dengan pesan jelas + arahan (biaya transfer / PPh 22 / ubah jadi jasa); jurnal tidak berubah. ✅ |
| F. Penjualan barang ke sub-akun pihak, pelunasan tanpa `--pihak` (akun induk) | Ditolak (sub-akun ikut dibaca). ✅ |
| B. Piutang jasa 12.345.678, `--pph23 2%` | Diizinkan tanpa PERHATIAN asal. Bank 12.098.765, PPh 23 dibayar dimuka 246.913 (2% = 246.913,56 dibulatkan ke bawah), piutang 0 — cocok Decimal penguji & hledger. ✅ |
| C. Campuran barang 5 jt + jasa 3 jt, `--pph23 60rb` | Diizinkan + PERHATIAN "bercampur" + PERHATIAN bukan 2%/4%. Bank 7.940.000, PPh 23 60.000, piutang 0 — cocok. ✅ |
| D. Asal tidak ada di jurnal (saldo awal), 7.777.777 `--diterima 7.622.222` | Diizinkan + PERHATIAN "asal tidak ditemukan". Kas 7.622.222, PPh 23 155.555 (dalam toleransi 2%), piutang −7.777.777 — cocok. ✅ |

Selisih angka vs hitung independen/hledger: **0**.

Temuan (semua RENDAH):
1. **[RENDAH]** Asal piutang dibaca dari **nama akun pendapatan**, bukan dari jenis catatan: `--jenis jual --akun "Pendapatan:Usaha"` (tanpa kata penjualan/barang) digolongkan "lain" → `--pph23` diterima **tanpa PERHATIAN**. Saran: tandai transaksi `jual` (mis. tag) atau beri PERHATIAN juga untuk golongan "lain".
2. **[RENDAH]** Skenario D membuat saldo piutang negatif tanpa peringatan (saldo awal belum dicatat). Saran: ingatkan catat saldo awal piutang dulu.

### Skor: **9/10**
Alasan: penolakan PPh 23 atas piutang barang bekerja di semua jalur (CLI, batch, hledger & mesin bawaan, akun induk/sub-akun), kasus campuran/tidak diketahui diizinkan dengan PERHATIAN yang tepat, angka tepat ke rupiah di hledger asli, tanpa regresi. Belum 10: celah kecil via akun pendapatan bernama umum dan platform asli belum diuji.
