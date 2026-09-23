# HASIL UJI — laporan-otomatis-terjadwal

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Lingkungan:** Python 3.11; OpenClaw **2026.9.5 (ec9c1a1)** di `/tmp/oc` dengan HOME uji sendiri (`/tmp/uji-oc-home`). Semua perintah dicek lewat `--help`, lalu **dijalankan sungguhan** pada Gateway lokal uji (`gateway run --allow-unconfigured --bind loopback --token ...`, tanpa model AI & tanpa kanal login). Data uji di `/tmp/uji-laporan-otomatis-terjadwal/`.
- **Versi skill:** 1.0.0 (catalog: draft)

## Verifikasi perintah OpenClaw
| Perintah di skill | `--help` | Dijalankan di Gateway uji |
|---|---|---|
| SKILL.md L5: `automations add "<cron>" "<pesan>" --name --tz Asia/Jakarta --session isolated --announce --channel telegram --to` | valid | **Berhasil**: job dibuat, jalan berikutnya Senin 28 Sep 2026 07:00 WIB, `announce -> telegram:123456789` |
| references §1: `add "<schedule-atau-nama>" "<pesan>" --cron ... --name "..."` | — | **Gagal** bila nama posisi ≠ `--name`: "Pass the automation name either positionally or with --name, not both." (berhasil hanya bila keduanya identik) |
| `automations list --all` / `list --json` | valid | Berhasil |
| `automations show <id-atau-nama> --json` | valid ("Job id or exact name") | Berhasil dengan nama |
| `automations run <id-atau-nama> --wait` (SKILL.md L139, references L71) | argumen = "Job id" | Dengan nama: **"Automation not found"**. Dengan id: run masuk antrean; `--wait` timeout karena mesin uji tanpa model (batas lingkungan) |
| `disable/enable/edit/rm <id>` | valid (id saja) | Berhasil dengan id; `edit --cron --tz` dan `edit --to` benar; dengan nama → "Automation not found" |
| `automations runs <id>` | valid | Berhasil (riwayat kosong) |
| `--best-effort-deliver`, `--model`, `--at`, `--every`, `--trigger-script`, `--clear-to`, `--clear-channel` | ada di `--help` | tidak dijalankan |
| `channels add --channel telegram --token <token>` | valid (ada di contoh `--help`) | tidak dijalankan (butuh token asli) |
| `channels add --channel whatsapp`, `channels login --channel whatsapp` | valid | tidak dijalankan (butuh scan QR) |
| `channels.whatsapp.allowFrom` | ada di skema konfigurasi | — |
| Perintah resep lain: `proyeksi_kas.py --saldo-awal --mulai --jumlah-minggu --format json`, `hitung_telat.py --file --tanggal --format json`, `laporan_emkm.py --nama-usaha --periode-awal --periode-akhir --format json` | semua flag ada | tidak dijalankan end-to-end (di luar penugasan) |

## Uji end-to-end & tepi
- **Resep penjualan** (`cek_sumber_data` → `rekap.py` → `susun_pesan`) dengan CSV kasir 70 baris (`;`, "Rp 30.000,-", 7 Batal, 1 tanggal rusak): omzet Rp 2.778.000, 62 baris, rata-rata Rp 396.857, 3 teratas & hari terbaik/terendah — **cocok dengan hitungan independen**. Pesan 13 baris (≤ 15).
- **Data kosong → tidak ada nol palsu:** folder tidak ada / file 0 byte / hanya judul / baris `;;;` → `siap: false`, exit 1, pesan jelas; semua baris Batal → `rekap.py` exit 1 "Tidak ada baris valid". Lulus.
- **Stok menipis dengan buku-stok:** `stok.py laporan menipis --json` memberi daftar + rata-rata laku + perkiraan habis (angka diverifikasi). Resep saat ini **tidak memakainya** dan gagal di kasus "0 produk menipis" (lihat S-3).
- **Privasi:** `susun_pesan.py` tidak punya field kontak (bagus), tetapi deteksinya lemah (lihat S-5).
- **Kanal:** Telegram default di wawancara, Langkah 4, dan contoh perintah; WA hanya nomor terpisah + persetujuan tertulis + hanya ke pemilik; broadcast ditolak. Sesuai keputusan pemilik.
- **Audit keamanan:** 2 script hanya library standar, tanpa jaringan/subprocess/eval, hanya membaca folder yang diberikan. Tidak ada prompt injection. Catatan: job yang dibuat OpenClaw berjalan dengan `toolsAllow: ["*"]` dan `scheduledToolPolicy: trusted` (terlihat di output `add`).

## Skor
| Kriteria | Skor |
|---|---|
| Pemicu (description tepat) | 9 |
| Kemudahan awam | 8 |
| Kualitas output | 8 |
| Akurasi (angka/fakta) | 6 |
| Penanganan input kurang | 9 |
| Penanganan di luar cakupan | 9 |
| Keamanan | 8 |
| **SKOR AKHIR** | **6 / 10 — REVISI** |

Alasan: alur utama benar, angka akurat, dan jauh lebih baik dari tanpa skill maupun pesaing. Tetapi ada beberapa cacat sedang di jalur kritis yang dijanjikan "reliable": langkah uji wajib (Langkah 6) gagal bila agent memakai nama, template di references ditolak CLI padahal diklaim "semua terverifikasi", resep stok menipis salah untuk kasus nol, dan data basi bisa terkirim ulang sebagai laporan baru. Tidak ada cacat berat; setelah revisi (kecil-menengah) layak ≥ 8.

## Daftar cacat

### Berat
Tidak ada.

### Sedang
**S-1. `run`/`edit`/`disable`/`enable`/`rm` hanya menerima id, bukan nama.** SKILL.md baris 139 (`automations run <id-atau-nama> --wait`), references/openclaw.md baris 34 ("`--name` ... dipakai lagi di `show`/`edit`/`rm` sebagai pengganti id"), baris 71. Diuji: nama → "Automation not found".
*Perbaikan:* setelah `add`, ambil `"id"` dari output JSON dan pakai id di Langkah 6–7; sebutkan hanya `show` yang menerima nama persis; contoh `openclaw automations list --json` untuk mencari id.

**S-2. Template references/openclaw.md §1 (baris 23–26) memakai nama posisi + `--name` sekaligus → ditolak CLI**, dan baris 5 mengklaim "Tidak ada satu pun perintah di sini yang belum dicek lewat `--help`".
*Perbaikan:* samakan dengan bentuk SKILL.md L5 (`add "<cron>" "<pesan>" --name ...`) atau bentuk opsi penuh `add --name ... --cron ... --message ...` (keduanya lolos di Gateway uji); ubah klaim menjadi "diuji pada Gateway lokal 2026.9.5".

**S-3. Resep stok menipis belum memakai buku-stok dan salah untuk kasus "tidak ada yang menipis".** `templates/RESEP-stok-menipis.md` baris 1–4 & 20–27 meminta CSV + `cek_sumber_data.py` dan filter manual; bila CSV dibuat dari `stok.py laporan menipis --csv` dan tidak ada produk menipis, CSV hanya judul → `cek_sumber_data` "siap: false, Laporan TIDAK dibuat" (diuji). SKILL.md baris 61 menyebut "Perhitungan sendiri (script skill ini)" padahal tidak ada script stok.
*Perbaikan:* tambahkan jalur utama "Pengguna buku-stok": `stok.py info --json` (DB ada + `mutasi_terakhir` untuk umur data) → `stok.py laporan menipis --json` (hanya baca; tanpa `--ya`) → pesan dengan "sisa/ambang/perkiraan habis". Jalur CSV tetap sebagai cadangan, dengan catatan bahwa CSV berisi **semua** produk (`laporan stok --csv`) agar kasus nol tidak dianggap data kosong. Prompt jadwal: batasi `--tools` (mis. `exec,read`).

**S-4. Data basi / banyak file tidak tertangani.** Resep penjualan memakai hanya "file terbaru" (baris 25) dengan `--maks-umur-hari 10` untuk laporan mingguan (baris 21): (a) file minggu lalu (umur 7 hari) lolos tanpa peringatan → angka minggu lalu terkirim ulang sebagai laporan baru; (b) pengguna yang menaruh file harian → laporan mingguan hanya menghitung 1 hari.
*Perbaikan:* setelah `rekap.py`, bandingkan `periode.awal/akhir` dengan periode yang diminta — bila tidak mencakup periode, kirim "data periode ini belum ada", bukan angka; set `maks-umur-hari` < irama jadwal (harian 1, mingguan 6); jelaskan cara menggabungkan beberapa file (atau minta satu ekspor per periode).

**S-5. Deteksi data pribadi di `susun_pesan.py` lemah dan bocor ke pesan.** Baris 43: `"nik"` dicocokkan sebagai substring → "Jumlah produk **unik**", "**Klinik**" (target member kesehatan) memicu peringatan palsu; nomor HP berbentuk angka (`081200001234`), email, dan "alamat" tidak terdeteksi; peringatan PDP dimasukkan ke **isi pesan yang dikirim** (bukan hanya stderr), berulang per baris.
*Perbaikan:* pakai regex batas kata (`\bnik\b`, `\bktp\b`), tambah pola telepon `(\+62|62|0)8\d{7,11}` dan email; tulis peringatan PDP **hanya** ke stderr + exit code khusus (mis. 3) agar agent berhenti sebelum membuat jadwal.

### Ringan
- R-1. Pemotongan `--maks-baris` (susun_pesan.py ±baris 160–175) membuang `catatan/peringatan` lebih dulu → peringatan kualitas data (baris dilewati, data lama) bisa hilang; rujukan "folder arsip laporan" (baris 175) tidak pernah dibuat skill. Sisakan minimal 1 baris peringatan.
- R-2. "Jumlah transaksi" diisi `jumlah_baris_valid` (RESEP-penjualan.md) — untuk ekspor marketplace satu pesanan bisa banyak baris; beri label "Jumlah baris/item terjual" atau hitung nomor pesanan unik.
- R-3. README & contoh-pesan: judul "Laporan Penjualan **Harian**" dengan periode 2 hari (21–22 Sep).
- R-4. references/openclaw.md baris 92: `channels list --all` menampilkan katalog kanal, bukan cara menemukan chat id Telegram; beri langkah konkret (kirim pesan ke bot → lihat pairing/log di Control UI).
- R-5. Semua catatan netral juga diberi ikon ⚠️ (mis. "Data stok dari buku-stok ...") — bedakan "catatan" (ℹ️/tanpa ikon) dari "peringatan".

## Verifikasi angka independen
**Ya.** Rekap penjualan (omzet, jumlah, rata-rata, terlaris, hari terbaik/terendah) dan angka stok menipis (rata-rata laku, perkiraan habis) dihitung ulang dengan Python terpisah dan cocok.
