# Umami Analitik: Laporan Pengunjung Web Tanpa Google

**Tanya "pengunjung web saya minggu lalu berapa?", "promo di IG, TikTok, atau WA yang paling ramai?", atau "berapa yang klik tombol WA?" — AI Anda langsung membaca Umami, analitik website gratis tanpa cookie yang jalan di server Anda sendiri, lalu menjawab dengan angka pasti dan perbandingan minggu lalu.**

> Komunitech **tidak berafiliasi** dengan Umami Software, Inc. Umami adalah software open-source (lisensi MIT) milik pengembangnya; skill dan panduan ini adalah karya orisinal Komunitech untuk memudahkan pemakaiannya oleh UMKM Indonesia.

## Manfaat
- ✅ **Pengganti Google Analytics yang gratis & sederhana.** Tanpa biaya bulanan, tanpa spanduk "setuju cookie", data pengunjung tetap di server Anda sendiri.
- ✅ **Cukup ngobrol, tanpa belajar dashboard.** "Halaman apa yang paling dilihat?", "pengunjung pakai HP atau laptop?", "dari kota mana?" — jawaban rapi dengan angka gaya Indonesia (1.200 / 27,3%).
- ✅ **Tahu promo mana yang berhasil.** Laporan kampanye UTM Instagram/TikTok/WhatsApp, sumber trafik, klik link di bio IG/QR kemasan, dan **klik tombol WA/Beli** (tingkat konversi) — dihitung script, bukan dikira.
- ✅ **Perbandingan yang adil.** "Minggu ini vs minggu lalu" dibandingkan sampai jam yang sama, jadi Selasa sore tidak dibandingkan dengan satu minggu penuh.
- ✅ **Laporan tiap Senin di Telegram** (lewat OpenClaw) + ekspor CSV siap Excel.

## Cocok untuk siapa
- **UMKM dengan website, landing page, atau toko online sendiri** (WordPress, HTML, pembuat landing page yang bisa ditempel kode) yang jualan lewat Instagram, TikTok, dan WhatsApp.
- **Freelancer/agensi kecil** yang mengelola beberapa website klien dan butuh laporan mingguan singkat.
- Pemilik usaha yang ingin tahu hasil promo tanpa membuka dashboard yang rumit.

**Kurang cocok:** yang hanya berjualan di marketplace (Shopee/Tokopedia/TikTok Shop — statistiknya ada di aplikasi masing-masing); yang ingin tahu **identitas** pengunjung (Umami sengaja anonim); yang butuh angka omzet resmi (pakai skill keuangan). Umami untuk website publik butuh **server ber-HTTPS** (VPS murah) — laptop saja hanya untuk coba-coba.

## Contoh sebelum & sesudah
**Sebelum (tanpa skill):** AI hanya bisa menjelaskan cara membuka dashboard atau menebak alamat API Umami — tanpa membaca angka website Anda, tanpa perbandingan, dan tanpa tahu bahwa klik dari WhatsApp tercatat sebagai "Langsung".

**Sesudah:** ketik *"Pengunjung web saya minggu lalu berapa? Naik nggak?"*
```
RINGKASAN WEBSITE: Keripik Bu Sri (landing) (keripikbusri.contoh.id)
Periode: minggu lalu, Senin 21 Sep 2026 - Minggu 27 Sep 2026
Pembanding: 14 Sep 2026 - 20 Sep 2026
- Pengunjung unik       : 11   (sebelumnya 4; naik 7 (+175%))
- Kunjungan             : 12   (sebelumnya 4; naik 8 (+200%))
- Tayangan halaman      : 23   (sebelumnya 6; naik 17 (+283%))
- Bounce rate           : 25% (3 dari 12 kunjungan hanya 1 halaman tanpa klik)   (sebelumnya 50%)
- Rata-rata lama        : 48 dtk per kunjungan   (sebelumnya 17 dtk)
```
Ketik *"Berapa yang klik tombol WA minggu lalu?"*
```
  Event                     Jumlah  Pengunjung  Tingkat konversi  Sebelumnya
  klik-wa                        3           3             27,3%           1
  beli                           2           2             18,2%           0
- beli / nilai: total Rp47.000 dari 2 event (dari data tombol, BUKAN omzet resmi - cocokkan dengan catatan penjualan)
```
(Contoh nyata dari uji dengan Umami 3.4.0 asli dan data fiktif — lihat `examples/`.)

## Cara pakai
Setelah Umami terpasang dan tersambung, cukup ketik:
- "Cek Umami saya sudah nyambung belum"
- "Pengunjung web kemarin / minggu ini / bulan lalu berapa?"
- "Halaman mana yang paling banyak dibuka?"
- "Pengunjung datang dari mana? IG, TikTok, Google?"
- "Promo gajian hasilnya gimana per sumber?"
- "Pengunjung pakai HP atau laptop? Kota mana saja?"
- "Minggu ini dibanding minggu lalu gimana?"
- "Berapa yang klik tombol WA / tombol beli?"
- "Link di bio IG diklik berapa kali?"
- "Buatkan tautan UTM untuk promo Oktober di IG, TikTok, dan status WA"
- "Ekspor laporan web bulan lalu ke Excel"
- "Kirim laporan web ke Telegram saya tiap Senin jam 7 pagi" (OpenClaw)

## Instalasi singkat
1. **Umami** sudah terpasang dan menyala. Belum? Ikuti `docs/panduan-umami.md` di paket (Docker resmi, ±20–40 menit, termasuk pengamanan, HTTPS, kode lacak, tombol WA terlacak, dan tautan UTM) — atau pakai **jasa setup Komunitech**.
2. Salin folder `umami-analitik` ke folder skills AI agent:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

(Rincian & verifikasi lokasi ada di `docs/instalasi.md`.)

3. Buat akun "hanya lihat" + kunci API di Umami (panduan §7), lalu simpan sekali di terminal Anda sendiri (bukan di chat): `python3 ~/.openclaw/skills/umami-analitik/scripts/umami.py simpan-kunci` (Windows: `python` / `py`). Umami di server sendiri: `... umami.py simpan-alamat https://analitik.domainanda.id`.
4. Coba: "Cek Umami saya sudah nyambung belum?"

## FAQ
**Kenapa "rata-rata lama" bisa beberapa detik lebih kecil dari perkiraan saya?**
Angka itu mengikuti hitungan Umami sendiri: jarak waktu antara pencatatan pertama dan terakhir dalam satu kunjungan. Waktu setelah pencatatan terakhir (mis. menutup halaman) tidak terhitung, dan kunjungan 1 halaman dihitung 0 detik. Skill menampilkan angka yang sama dengan layar Umami dan menyertakan catatan ini di setiap laporan.

**Apakah data pengunjung saya dikirim ke Komunitech atau pihak lain?**
Tidak. Script hanya menghubungi Umami **milik Anda sendiri** dan hanya membaca angka ringkasan. Tidak ada data ke Komunitech, kecuali Anda sendiri mengatur laporan ke Telegram.

**Apakah AI bisa merusak atau menghapus data Umami saya?**
Tidak. Skill ini hanya punya perintah baca. Disarankan memakai akun Umami **"hanya lihat"** untuk AI, sehingga Umami sendiri menolak perubahan apa pun dari kunci itu. Kunci tidak pernah ditampilkan di chat maupun disimpan di jadwal.

**Apakah pakai Umami melanggar UU PDP / perlu spanduk cookie?**
Umami tidak memakai cookie dan tidak menyimpan IP atau identitas pengunjung — hanya statistik agregat, di server Anda. Panduan §9 berisi saran kalimat untuk kebijakan privasi website Anda (bukan nasihat hukum).
