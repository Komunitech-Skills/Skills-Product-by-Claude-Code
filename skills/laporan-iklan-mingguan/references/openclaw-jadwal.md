# Menjadwalkan laporan iklan mingguan lewat OpenClaw

Skill ini **sendiri tidak membuat jadwal apa pun** — ia hanya menghitung laporan dari file yang
sudah ada. Halaman ini menjelaskan cara menyerahkan resepnya ke skill `laporan-otomatis-terjadwal`
(yang memang bertugas membuat jadwal `openclaw automations`) SETELAH laporan manual di atas
terbukti benar minimal sekali.

## 0. Ekspor iklan tetap manual (keputusan pemilik Komunitech, 2026-09-23)
OpenClaw **tidak** login atau menarik data secara otomatis dari Meta Ads Manager, TikTok Ads
Manager, Shopee Ads, TikTok Shop Ads, maupun Google Ads — mengotomasi login/scraping platform
pihak ketiga berisiko (kredensial tersimpan, melanggar Ketentuan Layanan platform tersebut) dan
sengaja **ditolak** sebagai fitur skill ini. Pemilik/admin iklan tetap mengekspor CSV secara
manual dari masing-masing Ads Manager, 1-2 menit per platform per minggu, lalu menaruhnya di
folder yang sama setiap minggu (mis. `Dokumen/Laporan-AI/masuk/iklan/`).

Perintah `openclaw automations add`/`add --command-argv` di bawah **sama persis** dengan yang
sudah diverifikasi lewat CLI OpenClaw asli di `laporan-harian-usaha/references/openclaw-jadwal.md`
(2026.9.5) dan diverifikasi ulang lewat `openclaw automations add --help` OpenClaw 2026.9.6
(lihat `solusi-vip/README.md` §"Metodologi verifikasi"). Halaman ini **tidak menebak flag baru** —
hanya menerapkan pola yang sudah ada ke resep laporan iklan. Bagian "Pengiriman sungguhan ke
Telegram" tetap berstatus ⚠️ (belum diuji butuh token bot asli), sama seperti skill lain di
repo ini.

## 1. Aturan kanal (sama untuk seluruh repo)
- **Telegram (bot resmi) = default.** `--to` = ID chat pemilik/admin iklan.
- **WhatsApp** hanya dengan nomor terpisah milik pemilik + persetujuan risiko tertulis (lihat teks
  lengkap di `laporan-otomatis-terjadwal/SKILL.md` §4).
- **Tanpa broadcast**, tidak pernah ke grup/pelanggan.

## 2. Siapkan resep laporan
Gunakan alur `laporan-otomatis-terjadwal` (Langkah 1 "Pilih resep laporan"): karena belum ada
resep siap pakai untuk iklan di skill itu, salin pola resep yang paling mirip lalu isi:
- Sumber data: folder ekspor CSV iklan (mis. `laporan/masuk/iklan/`), **satu file per platform per
  minggu**, nama file konsisten (mis. `meta-YYYY-MM-DD.csv`) agar mudah dicek "apakah sudah
  diekspor minggu ini".
- Perintah: `python3 <folder-skill-ini>/scripts/laporan_iklan.py analisis <file> --sebelumnya
  <file-minggu-lalu> --json`, lalu (bila lebih dari 1 platform) `gabung`.
- **Cek kesiapan data dulu** dengan `laporan-otomatis-terjadwal/scripts/cek_sumber_data.py`
  (`--maks-umur-hari 6` untuk mingguan) sebelum menjalankan analisis — jangan kirim laporan dari
  file ekspor yang sudah lama/lupa diganti.

## 3a. Bentuk perintah langsung (DISARANKAN: angka tidak ditulis ulang oleh AI)
Job `--command-argv` menjalankan script apa adanya, jadi teks laporan yang terkirim **persis**
keluaran `laporan_iklan.py` (sesuai Langkah 4 SKILL.md: angka tidak diubah). Pola ini diuji penguji
independen 25 September 2026 (OpenClaw 2026.9.6, Gateway `--dev`): `automations run --wait` →
`status: ok`, `summary` = teks laporan lengkap, sama persis dengan uji terminal. Pengiriman
Telegram sungguhan belum diuji (butuh token bot asli).

Pakai **nama file tetap** supaya perintahnya tidak perlu diubah tiap minggu:
- Tiap Senin pagi, sebelum jam jadwal: ganti nama `meta-minggu-ini.csv` yang lama menjadi
  `meta-minggu-lalu.csv` (timpa yang lama), lalu simpan ekspor baru sebagai `meta-minggu-ini.csv`.
- Script memberi ⚠️ bila kedua file ternyata sama persis atau periodenya sama (lupa ganti file).

```bash
openclaw automations add --name "Laporan iklan mingguan" --cron "50 7 * * 1" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/laporan-iklan-mingguan/scripts/laporan_iklan.py","analisis","/home/NAMA/Laporan-AI/iklan/meta-minggu-ini.csv","--sebelumnya","/home/NAMA/Laporan-AI/iklan/meta-minggu-lalu.csv","--nama-hasil","pesan WA"]' \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```
- Jam 07.50 memberi waktu ekspor pagi. Ganti path & `--nama-hasil` sesuai milik pengguna.
- Nama file berisi tanggal (`meta-2026-09-21.csv`) **tidak** bisa dipakai di bentuk ini; pakai
  nama tetap di atas, atau Bentuk A (agent) di bawah.
- Lebih dari satu platform: bentuk ini hanya satu file per job. Buat satu job per platform, atau
  pakai Bentuk A agar agent menjalankan `analisis --json` per platform lalu `gabung`.
- Windows: bentuk `--command-argv` belum diuji di Gateway Windows; pakai Bentuk A.

## 3. Contoh jadwal (Bentuk A, sudah diuji untuk pola job serupa — lihat § 0)
Senin pagi 07.00 WIB, satu platform (Meta), Telegram:
```bash
openclaw automations add "0 7 * * 1" \
  "Jalankan resep laporan iklan mingguan (skill laporan-iklan-mingguan) untuk file minggu lalu di laporan/masuk/iklan/. Tulis ringkas dalam Bahasa Indonesia, angka penting di atas, format Rupiah 'Rp 1.250.000'. Kalau file ekspor minggu ini belum ada di folder, katakan itu dengan jelas -- JANGAN kirim angka nol atau angka minggu sebelumnya seolah data baru." \
  --name "Laporan iklan mingguan" --tz "Asia/Jakarta" --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
Untuk WhatsApp (hanya setelah syarat §1 dipenuhi): ganti baris terakhir menjadi
`--channel whatsapp --to "+62<nomor pemilik>"`.

**Ambil `id` dari hasil `add`** dan pakai untuk `run --wait` (uji sekali sebelum aktif),
`list`/`show`/`disable`/`enable`/`edit`/`rm` — sama seperti seluruh skill penjadwalan di repo ini.
Detail lengkap & alasan tiap flag: `laporan-otomatis-terjadwal/references/openclaw.md` §1-§5 dan
`laporan-harian-usaha/references/openclaw-jadwal.md` §1-§6 (perintah `add`/`run`/`list` yang sama
persis sudah diuji terhadap Gateway lokal di situ).

## 4. Ingatkan sebelum jadwal dianggap aktif
- **Ekspor tetap manual tiap minggu** — jadwal ini hanya menjalankan `laporan_iklan.py` terhadap
  file yang SUDAH ada. Sarankan pengingat terpisah ("ekspor iklan tiap Senin pagi sebelum jam 7")
  bila pemilik sering lupa, atau jadwalkan laporan agak siang (mis. jam 8-9 WIB) untuk memberi
  waktu ekspor pagi itu.
- **Komputer/Gateway harus menyala** saat jam jadwal (lihat `references/mesin-24-jam.md` di skill
  `laporan-otomatis-terjadwal`) — tawarkan 3 opsi yang sama (komputer selalu menyala, mini PC/VPS
  sendiri, atau jasa setup Komunitech, tanpa menyebut harga).
- **Uji dulu** (`openclaw automations run <id> --wait`) dan tunjukkan hasilnya sebelum menyatakan
  jadwal aktif — sama seperti checklist `laporan-otomatis-terjadwal`.
