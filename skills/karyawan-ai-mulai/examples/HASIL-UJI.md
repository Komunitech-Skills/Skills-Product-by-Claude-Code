# HASIL UJI — karyawan-ai-mulai

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Lingkungan:** OpenClaw 2026.9.5 (ec9c1a1), HOME uji terisolasi `/tmp/uji-vip/home`, tanpa
  login kanal apa pun. Skill dipasang sungguhan dengan `openclaw skills install ./<folder> --global`.

## Verifikasi perintah OpenClaw yang ditulis skill
| Perintah / klaim | Hasil |
|---|---|
| `openclaw skills list --eligible` | ✅ jalan (27/27 ready; skill kita "openclaw-managed") |
| `openclaw skills list --verbose --json` | ✅ jalan (JSON: workspaceDir, managedSkillsDir, skills) |
| `openclaw skills install ./<skill> --global` | ✅ terpasang ke `~/.openclaw/skills/<skill>`, termasuk `scripts/`. Pasang ulang skill yang sudah ada: "Skill already exists… Re-run with force/update" (tidak disebut di skill) |
| `openclaw skills check` / `skills info karyawan-ai-mulai` | ✅ Ready, visible to model, available as command |
| `openclaw automations add "0 7 * * 1" "<pesan>" --name … --tz Asia/Jakarta --session isolated --announce --channel telegram --to …` | ✅ argumen diterima parser, gagal hanya karena Gateway belum berjalan/berkredensial (wajar di mesin uji). `automations` = alias `cron`, `create` = alias `add` ✅ |
| Memori lewat `USER.md`/`MEMORY.md` di workspace, tanpa CLI tulis | ✅ sesuai docs (`concepts/agent-workspace.md`; USER.md dibatasi 4.000 karakter) |
| Kutipan "Cron runs inside the Gateway process…" | ✅ konsisten dengan docs automation |
| Semua nama skill di `peta-skill.md` & script ada di library | ✅ (35/35) |

## Audit keamanan singkat
Tidak ada panggilan jaringan, perintah destruktif, pembacaan kredensial, atau prompt injection.
Script hanya memakai stdlib (argparse/json/unicodedata). Instal dari luar paket dan publikasi ke
ClawHub dilarang eksplisit. ✅

## Skor
| Kriteria | Skor | Alasan |
|---|---|---|
| Pemicu (description) | 8 | Kata kunci ID/EN jelas, batas dengan cek-privasi tegas |
| Kemudahan awam | 8 | Satu pesan, pilihan bernomor, "terserah" → default. Minus: path Starter Kit untuk install tidak dijelaskan |
| Kualitas output | 8 | Hasil nyata + rencana 7 hari + privasi (A/B jelas menang) |
| Akurasi | 5 | Perintah OpenClaw benar, tapi script pemetaan salah cocok untuk frasa umum persona utama ("kurir" → pengajuan-kur) |
| Penanganan input kurang | 8 | Tanya sekali + default. Minus: default kanal WA bertentangan dengan keputusan pemilik |
| Penanganan di luar cakupan | 7 | Menolak auto-trading/posting otomatis/diagnosis. Aturan WA Copilot, kripto yang boleh, dan larangan scraping marketplace tidak tertulis |
| Keamanan | 9 | Izin eksplisit sebelum install, tidak ada data pelanggan di memori |

## SKOR AKHIR: 6 / 10 — **REVISI**
Kerangka dan pengalaman pengguna sangat baik, dan menang di A/B maupun uji banding pesaing.
Skor dibatasi karena ada cacat berat pada script pemetaan: persona retail diarahkan ke skill
yang salah. Setelah perbaikan di bawah, skill ini berpotensi 8.

## Daftar cacat & saran perbaikan

### Berat
1. **`scripts/peta_kebutuhan.py` salah cocok karena substring** (fungsi `cocokkan_tugas`, baris
   95–101, dan daftar `PEMETAAN` baris 26–62). Terbukti: "input no resi **kur**ir" → `pengajuan-kur`,
   "gaji **sop**ir" → `sop-writer`, "pendapatan harian" → `perjanjian-sederhana` (kunci "nda"), "atur **agen**da" → `katalog-reseller`, "urus **nota**ris" → `ekstrak-nota-faktur`, "hitung
   a**mou**nt" → perjanjian, industri "s**hr**imp farm" → paket HR (`cocokkan_industri`, baris 104–109).
   **Perbaikan:** cocokkan per kata utuh (regex `\b…\b` setelah normalisasi), hapus kunci terlalu
   pendek/ambigu ("kur", "nda", "mou", "agen", "hr", "ter "), dan tambah tes unit untuk 20 frasa
   persona nyata (termasuk di atas).

### Sedang
2. **Frasa sehari-hari & industri umum tidak dikenali**: "rekap jualan", "bales wa", "bikin konten",
   "posting ig", "laporan omzet", "gaji karyawan"; industri "restoran", "rumah makan", "kafe",
   "dokter", "bengkel" → `null`. Tambah sinonim ke `PEMETAAN`/`PAKET_INDUSTRI` dan tabel §2 peta-skill.md.
3. **Script tidak menjamin 3 rekomendasi** (baris 135–139: paket industri hanya dipakai bila
   *tidak ada* tugas yang cocok). Isi sisa slot dari paket industri, lalu paket umum, tanpa duplikat.
4. **Bertentangan dengan keputusan pemilik jalur 3**: default kanal = "WhatsApp" (SKILL.md baris
   38). Ubah ke **Telegram**. Tambahkan di "Batasan": WA hanya nomor terpisah + persetujuan risiko,
   agen CS WA = mode **Copilot** (AI menyiapkan draf, manusia mengirim), tanpa broadcast. Tambahkan
   juga aturan kripto (hanya riset/jurnal/notifikasi harga) dan larangan scraping marketplace
   lewat login browser (persona retail resi Shopee).
5. **Path install tidak jelas bagi awam** (SKILL.md langkah 5 dan references/openclaw.md §2 memakai
   `./<nama-skill>`). Tambahkan langkah: tanyakan/temukan folder hasil ekstrak ZIP Starter Kit
   (mis. cari `*/rekap-penjualan-csv/SKILL.md` di Downloads). Bila skill sudah ada, jelaskan pesan
   "already exists" (pakai `--force` hanya dengan izin). Verifikasi dengan `openclaw skills info <nama>`.
6. **Peta skill belum mencakup solusi VIP baru**: `laporan-otomatis-terjadwal` (sedang dibuat di
   repo) belum ada di `peta-skill.md`/script, padahal otomasi laporan adalah kebutuhan #1 (~20
   member). Paket "Kesehatan" (sop-writer, surat-resmi, notulen-rapat) tidak menjawab kebutuhan
   dokter solo (balasan pasien, edukasi pasien). Tambahkan `balas-chat-cs` ke paket kesehatan.

### Ringan
7. `references/peta-skill.md` baris 4 memuat path internal `/home/user/Skills/skills/`. Ganti dengan
   "folder skills platform Anda".
8. Pertanyaan 2 punya 5 kategori, bertabrakan dengan aturan "maks. 4 opsi" (baris 30–31). Sediakan versi 4 opsi baku.
9. Tambahkan cek prasyarat: skill ini dan skill ber-script butuh `exec` (bukan `tools.profile:
   messaging`). Ini ide dari pesaing, dan penting karena `cek-privasi-openclaw` bisa menyarankan profil ketat.
10. Rekap belum per cabang. Untuk usaha multi-cabang (persona F&B 50+), sarankan file per cabang secara eksplisit.

## Verifikasi angka
Script skill ini tidak menghitung uang. Angka pada contoh 01 berasal dari `rekap-penjualan-csv/scripts/rekap.py`
dan **diverifikasi independen** dengan python terpisah: total Rp 46.477.000, rata-rata Rp 6.639.571/hari,
urutan & persen 5 menu, hari terbaik (Sab 19/9, Rp 8.763.000) dan terendah (Sen 21/9, Rp 5.286.000). Semua cocok.
