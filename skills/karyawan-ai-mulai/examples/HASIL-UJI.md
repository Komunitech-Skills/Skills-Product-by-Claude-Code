# HASIL UJI — karyawan-ai-mulai v1.1.0 (uji ulang)

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi diuji:** v1.1.0 (revisi setelah uji v1.0: skor 6, REVISI)
- **Lingkungan:** OpenClaw 2026.9.5 (ec9c1a1), **HOME uji baru** `/tmp/uji-vip/home-v11`, tanpa
  login kanal. Skill dan skill terkait (rekap-penjualan-csv, buku-stok, laporan-otomatis-terjadwal,
  cek-privasi-openclaw) dipasang sungguhan dengan `openclaw skills install ./<folder> --global`.
  Data persona & uji v1.0 di `/tmp/uji-vip/` dipakai ulang.

## Verifikasi perintah OpenClaw (ulang, HOME baru)
| Perintah / klaim di skill v1.1.0 | Hasil |
|---|---|
| `openclaw skills list --eligible`, `skills list --verbose --json`, `skills check` | ✅ jalan |
| `openclaw skills install <folder> --global` | ✅ terpasang ke `~/.openclaw/skills/<nama>` (termasuk `scripts/`) |
| Pesan "Skill already exists… Re-run with force/update" saat pasang ulang | ✅ persis seperti dikutip skill |
| `--force` untuk menimpa (`skills install ./x --global --force`) | ✅ jalan (exit 0) |
| `openclaw skills info <nama>` → Ready / Visible to model / Available as command | ✅ persis |
| `openclaw automations add "0 7 * * 1" "<pesan>" --name … --tz Asia/Jakarta --session isolated --announce --channel telegram --to …` | ✅ argumen diterima (berhenti hanya karena Gateway tanpa kredensial di mesin uji). `automations` = alias `cron`, `create` = alias `add` |
| Klaim `exec.mode → ask` membuat automation ditolak tanpa klien approval (references §5) | ✅ sesuai docs `tools/exec-approvals.md` |
| Memori lewat `USER.md`/`MEMORY.md`, tanpa CLI tulis | ✅ sesuai docs |
| Semua nama skill di `peta-skill.md` & script ada di library | ✅ (termasuk `buku-stok`, `laporan-otomatis-terjadwal`) |

## Uji script `peta_kebutuhan.py` v1.1.0
- `--self-test`: **25/25 lulus**, exit 0.
- **Regresi salah cocok v1.0 (uji independen penguji):** "input no resi kurir", "cetak resi …
  nomor resi kurir", "kirim barang lewat kurir", "gaji sopir", "pendapatan harian", "atur agenda
  meeting", "urus notaris", "hitung amount", industri "shrimp farm" → **tidak ada lagi salah
  cocok** ✅. "cek stok kurang" → `buku-stok` (benar).
- **Frasa baru rancangan penguji (43 tugas + 18 industri):**
  - Benar: "bales wa customer", "auto reply pasien", "laporan keuangan bulanan buat bank",
    "bikin caption promo", "restock barang", "dropship"; industri restoran/rumah makan/toko
    online/dokter/klinik gigi.
  - Selalu ≥ 3 rekomendasi tanpa duplikat ✅ (3 persona dicek).
  - **Tidak cocok (jatuh ke paket industri, tidak berbahaya):** "ngecek stok bahan baku", "stok
    bahan baku" (`\bcek` tidak cocok dengan "ngecek"), "jawab wa pasien…", "balesin chat pasien",
    "laporan harian otomatis ke hp", "bikin laporan", "upload konten tiktok", "gajian karyawan",
    "nagih pelanggan", "pengingat tagihan pelanggan"; industri "HRD", apotek, salon, distributor, kontraktor.
  - **Prioritas keliru:** "kirim laporan penjualan otomatis tiap pagi ke telegram" →
    `rekap-penjualan-csv` (bukan `laporan-otomatis-terjadwal`, kebutuhan #1 member).
  - **Salah cocok kecil yang tersisa:** "saya belum bayar pajak" → `tagih-piutang`; "follow up
    supplier" → `follow-up-prospek`; "loker karyawan rusak" → `lowongan-kerja`; industri "jasa
    kesehatan" → paket jasa (urutan dict: "jasa" sebelum "kesehatan").

## Audit keamanan singkat
Tidak ada panggilan jaringan, perintah destruktif, atau pembacaan kredensial. Tidak ada prompt
injection. Script hanya memakai stdlib (argparse/json/re/unicodedata). `--force` hanya dengan izin
eksplisit per perintah. Tidak memasang dari luar paket. ✅

## Skor
| Kriteria | v1.0 | v1.1.0 | Alasan |
|---|---|---|---|
| Pemicu (description) | 8 | 8 | Tidak berubah, tetap tepat |
| Kemudahan awam | 8 | 9 | Cara menemukan folder Starter Kit, pesan "already exists" dijelaskan, 4 opsi baku |
| Kualitas output | 8 | 8 | Hasil nyata + 7 hari + privasi; saran per cabang untuk 50+ |
| Akurasi | 5 | 8 | Salah cocok berbahaya hilang, self-test 25 kasus; sisa sinonim/prioritas (sedang) |
| Penanganan input kurang | 8 | 9 | Default Telegram, 4 opsi baku, asumsi disebut |
| Penanganan di luar cakupan | 7 | 9 | Aturan pemilik tertulis: WA Copilot/nomor terpisah, kripto, kesehatan, tanpa scraping marketplace, tanpa broadcast |
| Keamanan | 9 | 9 | Izin eksplisit, tidak ada data pelanggan di memori |

## SKOR AKHIR: 8 / 10 — **LULUS**
Cacat berat v1.0 (salah cocok substring) sudah diperbaiki dan terbukti lewat regresi independen.
Semua aturan pemilik jalur 3 sekarang tertulis di skill. A/B dan uji banding pesaing tetap menang.
Sisa cacat berikut layak diperbaiki di v1.1.1 tetapi tidak menghalangi kelulusan.

## Cacat tersisa & saran perbaikan

### Berat
- Tidak ada.

### Sedang
1. **Merekomendasikan skill yang belum rilis.** `buku-stok` dan `laporan-otomatis-terjadwal` berstatus
   **uji** di `catalog.csv` (belum `rilis`), tetapi `peta-skill.md` (baris 14–15, 58) dan script
   (`PEMETAAN` baris 45–48) merekomendasikannya seolah pasti ada di paket pembeli. **Perbaikan:**
   tambahkan aturan "cek dulu ada di folder Starter Kit/terpasang; kalau tidak ada, katakan 'belum
   tersedia di paket Anda' dan pakai skill terdekat", atau tahan rilis karyawan-ai-mulai sampai
   kedua skill itu `rilis`.
2. **Sinonim & prioritas script** (`PEMETAAN`): tambahkan "stok" berbentuk frasa ("stok bahan",
   "stok barang", "ngecek stok"), "jawab wa", "balesin", "nagih", "gajian", "upload konten";
   letakkan kunci `laporan-otomatis-terjadwal` ("otomatis", "tiap pagi", "terjadwal" bersama
   "laporan") **sebelum** kunci `rekap-penjualan-csv`, atau dukung dua skill per tugas; tambahkan
   industri "hrd", "apotek", "salon", "distributor". Tambahkan frasa-frasa itu ke `KASUS_UJI`.

### Ringan
3. Salah cocok kecil: "belum bayar" (→ tagih-piutang) sebaiknya dibatasi dengan "pelanggan belum
   bayar". "jasa kesehatan" → urutkan industri spesifik (kesehatan/klinik/dokter) sebelum "jasa".
4. `references/openclaw.md` §7 merujuk `pedoman kurasi Komunitech` §1. File itu tidak ada di paket pembeli; ganti
   dengan "aturan paket Komunitech".
5. Contoh profil memori (`references/openclaw.md` §4) masih "Kanal favorit: WhatsApp" dan "skala
   6–15" (tidak cocok dengan 4 opsi baku dan default Telegram).
6. Docstring script menyebut "20 frasa". Isinya 25.

## Verifikasi angka
Script skill ini tidak menghitung uang. Angka contoh 01 (dari `rekap-penjualan-csv/scripts/rekap.py`)
**diverifikasi independen** dengan python terpisah: total Rp 46.477.000, rata-rata Rp 6.639.571/hari,
urutan & persen 5 menu, hari terbaik Sab 19/9 Rp 8.763.000, terendah Sen 21/9 Rp 5.286.000. Semua cocok.
