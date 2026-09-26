# Jadwal OpenClaw siap salin — Klinik

Sumber flag: `references/openclaw*.md` di `laporan-otomatis-terjadwal`, `konten-mingguan`, dan
`references/eskalasi-dan-kanal.md` di `agen-cs-toko`. Untuk sesi penyusunan paket ini, semua flag
di bawah **diverifikasi ulang** lewat `openclaw automations add --help` dan `openclaw channels
add --help` sungguhan di OpenClaw **2026.9.6 (eb377ac)** (dipasang lewat `bash
scripts/uji_openclaw.sh 2026.9.6`). Tidak ada flag yang berubah/hilang. **Tidak ada perintah baru
yang ditebak** — kombinasi pesan (`--message`) yang menyebut `edukasi-pasien-klinik` di §2 dan §3
adalah kombinasi **baru** untuk paket ini (skill itu sendiri belum punya `references/openclaw.md`),
jadi ditandai 📖/⚠️ sesuai bagiannya, BUKAN ✅.

Legenda: ✅ = dijalankan sungguhan terhadap Gateway nyata. 📖 = flag/perintah dicek via
`--help`/`config schema`, kombinasi utuh belum dicoba. ⚠️ = belum diverifikasi sama sekali.

**Semua jadwal di bawah mengirim hanya ke pemilik/PIC klinik — tidak pernah ke grup atau
pasien.** Tunjukkan ringkasan dan tanya "Lanjut? (ya/tidak)" sebelum menjalankan.

## 1. Rekap CS harian (mode Copilot), jam 20.00 WIB 📖
Flag inti sama dengan yang ✅ dijalankan sungguhan oleh `laporan-otomatis-terjadwal`/
`pengingat-follow-up`:
```bash
openclaw automations add \
  --cron "0 20 * * *" --tz "Asia/Jakarta" \
  --name "Rekap CS klinik harian" \
  --message "Baca isi file cs/log/<tanggal hari ini>.md di workspace. Ringkas: jumlah chat dibalas, kategori pertanyaan terbanyak (jadwal/biaya/BPJS/lainnya), jumlah yang dieskalasi ke dokter/staf, dan pertanyaan yang belum ada di cs/PENGETAHUAN.md. JANGAN sebut nama pasien. Jika file belum ada/kosong, katakan belum ada aktivitas, jangan mengarang. Bahasa Indonesia, maksimal 15 baris." \
  --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik/PIC>"
```
Log `cs/log/<tanggal>.md` **wajib** hanya berisi kategori + ringkasan pertanyaan, **tanpa** nama/
nomor HP pasien (aturan sama seperti agen-cs-toko untuk toko, lebih ketat karena data kesehatan =
data pribadi spesifik menurut UU PDP).

## 2. Laporan operasional klinik agregat, contoh mingguan Senin 08.00 WIB 📖
```bash
openclaw automations add "0 8 * * 1" \
  "Pakai skill edukasi-pasien-klinik: jalankan scripts/rekap_kunjungan.py pada file CSV kunjungan minggu lalu di <folder-kerja>/klinik/kunjungan/. Laporkan HANYA angka agregat: total kunjungan, per poli/penjamin, jam ramai, tidak datang. JANGAN sebut nama/NIK/diagnosis pasien walau ada di file sumber. Jika file belum ada, katakan data minggu ini belum masuk, jangan mengarang." \
  --tz "Asia/Jakarta" --name "Laporan operasional klinik mingguan" --session isolated --tools exec,read \
  --announce --channel telegram --to "<ID chat Telegram pemilik/PIC>"
```
- `--tools exec,read` 📖 membatasi jadwal ini hanya boleh membaca & menjalankan script — **tidak**
  bisa menulis/mengubah file kunjungan.
- Sebelum mempercayai jadwal, uji sekali: `openclaw automations run <id> --wait` (✅ pola ini
  dibuktikan di Gateway uji oleh skill lain — tunjukkan hasilnya ke PIC klinik dan pastikan
  **tidak ada** nama pasien yang lolos ke laporan sebelum mengaktifkan jadwal sungguhan).
- Ganti `"0 8 * * 1"` untuk laporan harian (mis. `"0 20 * * *"`) sesuai kebutuhan klinik.

## 3. Konten edukasi kesehatan mingguan — Jumat jam 16.00 WIB ✅/📖
Pola & flag sama persis dengan `konten-mingguan/references/openclaw-jadwal.md` (✅ untuk flag
inti), hanya pesannya disesuaikan untuk konten kesehatan:
```bash
openclaw automations add "0 16 * * 5" \
  "Jalankan skill konten-mingguan bersama edukasi-pasien-klinik untuk topik edukasi kesehatan minggu depan, memakai profil klinik di konten/PROFIL.md. Kutip HANYA sumber resmi (Kemenkes/WHO/organisasi profesi) dengan tautan & tanggal, TANPA klaim menyembuhkan/testimoni/before-after. Tandai bahwa draf wajib ditinjau dokter sebelum diposting. Simpan arsip ke konten/minggu-<label>.md." \
  --tz "Asia/Jakarta" --name "Konten edukasi kesehatan Jumat" --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik/PIC>"
```
**Wajib disebut ke klinik:** draf ini **tetap harus ditinjau dokter/tenaga kesehatan** sebelum
diposting — skill tidak menggantikan tinjauan profesional, dan OpenClaw **tidak memposting
otomatis** ke Instagram/TikTok/Facebook.

## 4. Skill baru tanpa jadwal (dokumen, dipicu manual)
`kebijakan-privasi-pdp`, `sop-onboarding`, dan `kontrak-kerja-pkwt` (lihat `PANDUAN.md` §5f–h)
adalah skill dokumen yang dipicu **manual** per kebutuhan (buat/cek kebijakan privasi, onboarding
staf baru, buat/periksa kontrak) — sengaja **tidak** dijadwalkan otomatis karena kebutuhannya
muncul sewaktu-waktu (staf baru masuk, kebijakan perlu diperbarui), bukan rutin di jam tetap.

## 5. Mengelola jadwal (✅, sama seperti paket lain)
```bash
openclaw automations list --all
openclaw automations run <id> --wait
openclaw automations disable <id>     # hanya id
openclaw automations enable <id>      # hanya id
openclaw automations rm <id>          # hanya id, permanen
```

## WhatsApp (hanya bila semua syarat terpenuhi)
1. Nomor **terpisah** dari nomor pendaftaran/CS pasien.
2. Hanya ke **pemilik/PIC klinik sendiri**.
3. Persetujuan risiko tertulis (kalimat baku sama seperti paket toko-online).
4. `dmPolicy: "allowlist"` (BUKAN `pairing`) + `allowFrom` hanya nomor pemilik/PIC — **penting
   khusus WA**: dengan `dmPolicy: "pairing"` (default), OpenClaw **otomatis mengirim pesan
   pairing ke setiap pengirim baru yang belum dikenal** — kalau nomor itu sampai bocor ke pasien,
   pasien baru akan menerima pesan otomatis dari bot. Set `allowlist` **sebelum** memberi tahu
   nomor ke siapa pun. Detail urutan setup: `skills/agen-cs-toko/references/eskalasi-dan-kanal.md`
   §2 (terverifikasi jalan di Gateway uji).

## Yang BELUM diverifikasi ⚠️
- Kombinasi utuh "agent menjalankan `rekap_kunjungan.py` di dalam job terjadwal dan mengirim hasil
  yang sudah tersaring privasinya" — pola cron-nya (✅) sudah terbukti untuk skill lain, tapi
  belum dicoba khusus dengan script `edukasi-pasien-klinik`. **Uji manual dulu** (jalankan sekali
  di chat biasa, cek hasilnya benar-benar agregat tanpa nama) sebelum mengaktifkan jadwal.
- Membuat jadwal di atas langsung lewat chat WhatsApp/Telegram.
- Pesan benar-benar tiba di Telegram/WhatsApp pembeli (uji internal tidak memakai token/nomor
  asli).
- **Pengingat kontrol/vaksin per pasien terjadwal** — sengaja **tidak** disediakan di sini, lihat
  "Celah" di `solusi-vip/README.md`.
