# Umami Analitik: Laporan Pengunjung Web Tanpa Google

**Tanya "pengunjung web saya minggu lalu berapa?", "promo di IG, TikTok, atau WA yang paling ramai?", atau "berapa yang klik tombol WA?" — AI Anda langsung membaca Umami, analitik website gratis tanpa cookie yang jalan di server Anda sendiri, lalu menjawab dengan angka dan perbandingan minggu lalu.**

Diuji AI penguji independen di OpenClaw (dengan server Umami tiruan dan data contoh, bukan Umami hidup): 5,3 → 8,7 dari 10 (tanpa skill, AI hanya meminta alamat dan kunci tanpa hasil apa pun; dengan skill langsung menjawab dengan angka dan perbandingan minggu lalu).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux (Windows dan macOS belum diuji langsung). Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Software tambahan: Umami (gratis, open-source; panduan pemasangan disertakan), dijalankan di server Anda sendiri; server ber-HTTPS (mis. VPS, yaitu server sewaan) dan domain untuk website publik adalah biaya tersendiri di luar paket ini. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Pengganti Google Analytics yang sederhana.** Umami sendiri gratis, tanpa langganan bulanan dan tanpa spanduk "setuju cookie"; data pengunjung tetap di server Anda sendiri. Biaya nyata yang tetap ada: server ber-HTTPS (VPS) dan domain untuk website publik.
- ✅ **Cukup ngobrol, tanpa belajar dashboard.** "Halaman apa yang paling dilihat?", "pengunjung pakai HP atau laptop?", "dari kota mana?" — jawaban rapi dengan angka gaya Indonesia (1.200 / 27,3%). Diuji dengan Umami 3.4.0 asli (penguji independen) dan dengan server tiruan di OpenClaw, belum di Umami milik pembeli sungguhan.
- ✅ **Tahu promo mana yang berhasil.** Laporan kampanye UTM (tag di tautan untuk melacak asal pengunjung) Instagram/TikTok/WhatsApp, sumber trafik, klik link di bio IG/QR kemasan, dan **klik tombol WA/Beli** (tingkat konversi, yaitu berapa persen pengunjung yang mengklik) — dihitung script, bukan dikira.
- ✅ **Perbandingan yang adil.** "Minggu ini vs minggu lalu" dibandingkan sampai jam yang sama, jadi Selasa sore tidak dibandingkan dengan satu minggu penuh.
- ✅ **Laporan tiap Senin di Telegram** (opsional, lewat OpenClaw; jadwal otomatis ini belum diuji langsung) + ekspor CSV (file tabel) siap Excel.

## Cocok untuk siapa
- **UMKM dengan website, landing page, atau toko online sendiri** (WordPress, HTML, pembuat landing page yang bisa ditempel kode) yang jualan lewat Instagram, TikTok, dan WhatsApp.
- **Freelancer/agensi kecil** yang mengelola beberapa website klien dan butuh laporan mingguan singkat.
- Pemilik usaha yang ingin tahu hasil promo tanpa membuka dashboard yang rumit.

**Kurang cocok:** yang hanya berjualan di marketplace (Shopee/Tokopedia/TikTok Shop — statistiknya ada di aplikasi masing-masing); yang ingin tahu **identitas** pengunjung (Umami sengaja anonim); yang butuh angka omzet resmi (pakai skill keuangan). Umami untuk website publik butuh **server ber-HTTPS** (alamat web aman bergembok; mis. VPS murah) — laptop saja hanya untuk coba-coba.

## Contoh sebelum & sesudah
**Sebelum (tanpa skill):** AI hanya bisa menjelaskan cara membuka dashboard atau menebak alamat akses (API) Umami — tanpa membaca angka website Anda, tanpa perbandingan, dan tanpa tahu bahwa klik dari WhatsApp tercatat sebagai "Langsung".

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
(Contoh nyata dari uji dengan Umami 3.4.0 asli dan data fiktif — lihat `examples/`. Bounce rate = persen kunjungan yang hanya melihat satu halaman.)

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
- "Kirim laporan web ke Telegram saya tiap Senin jam 7 pagi" (OpenClaw; jadwal otomatisnya belum diuji langsung)

## Instalasi singkat
1. **Umami** sudah terpasang dan menyala. Belum? Ikuti `references/panduan-umami.md` di paket (isinya sama dengan `docs/panduan-umami.md`; memakai Docker, yaitu cara resmi memasang server dengan sekali perintah, ±20–40 menit, termasuk pengamanan, HTTPS, kode lacak, tombol WA terlacak, dan tautan UTM) — atau pakai **jasa setup Komunitech**.
2. Salin folder `umami-analitik` ke folder skills AI agent:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

(Rincian & verifikasi lokasi: `docs/instalasi.md`, di dalam paket bernama `CARA-INSTAL.md`.)

3. Buat akun "hanya lihat" + kunci API (kunci akses untuk program) di Umami (bagian 7 "Akun khusus AI" di `references/panduan-umami.md`), lalu simpan sekali di terminal Anda sendiri (bukan di chat): `python3 ~/.openclaw/skills/umami-analitik/scripts/umami.py simpan-kunci` (Windows: `python` / `py`). Umami di server sendiri: `... umami.py simpan-alamat https://analitik.domainanda.id`.
4. Coba: "Cek Umami saya sudah nyambung belum?"

Komunitech tidak berafiliasi dengan Umami Software, Inc. Umami (lisensi MIT) tidak ikut didistribusikan di paket ini; skill dan panduannya karya Komunitech. Rincian: `ATTRIBUTION.md`.

**Hasil uji (angka nyata):** dua sumber yang terpisah.
- **Uji OpenClaw, uji otomatis agent, v1.0.6** (angka dari `examples/00-openclaw-sebelum-sesudah.md`): rata-rata nilai 5,3 tanpa skill menjadi 8,7 dengan skill (skala 10). Tanpa skill, AI tidak menemukan konfigurasi Umami dan hanya meminta alamat, ID website, dan kunci API tanpa hasil apa pun; dengan skill langsung menjawab dengan angka seperti di atas. Pada pertanyaan privasi (melacak individu), AI tanpa skill pun sudah menolak dengan baik (8 vs 9). Catatan jujur: uji OpenClaw memakai data contoh dan server tiruan yang memutar rekaman respons Umami 3.4.0 asli, bukan Umami hidup di server Anda; belum diuji: pengiriman laporan ke Telegram sungguhan dan Windows/macOS.
- **Uji penguji independen pada Umami 3.4.0 asli (Docker), skill v1.0.0:** skor 8/10; angka cocok dengan data mentah Umami (`examples/HASIL-UJI.md`).

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent, server tiruan) dan pada Umami asli oleh penguji independen; Codex, Claude Code, dan Cursor belum diuji langsung (format skill-nya sama). Jadwal ke Telegram dan Windows/macOS belum diuji langsung.

## FAQ
**Kenapa "rata-rata lama" bisa beberapa detik lebih kecil dari perkiraan saya?**
Angka itu mengikuti hitungan Umami sendiri: jarak waktu antara pencatatan pertama dan terakhir dalam satu kunjungan. Waktu setelah pencatatan terakhir (mis. menutup halaman) tidak terhitung, dan kunjungan 1 halaman dihitung 0 detik. Skill menampilkan angka yang sama dengan layar Umami dan menyertakan catatan ini di setiap laporan.

**Apakah data pengunjung saya dikirim ke Komunitech atau pihak lain?**
Tidak. Script hanya menghubungi Umami **milik Anda sendiri** dan hanya membaca angka ringkasan. Tidak ada data ke Komunitech, kecuali Anda sendiri mengatur laporan ke Telegram. Angka yang Anda minta tentu terbaca oleh AI agent yang Anda pakai, sesuai kebijakan penyedia AI-nya.

**Apakah AI bisa merusak atau menghapus data Umami saya?**
Seharusnya tidak. Skill ini hanya berisi perintah baca. Disarankan memakai akun Umami **"hanya lihat"** untuk AI, sehingga Umami sendiri menolak perubahan apa pun dari kunci itu. Skill dirancang agar kunci tidak ditampilkan di chat maupun disimpan di jadwal.

**Apakah pakai Umami melanggar UU PDP / perlu spanduk cookie?**
Menurut dokumentasi Umami, ia tidak memakai cookie dan tidak menyimpan alamat IP atau identitas pengunjung — hanya statistik agregat, di server Anda. Bagian 9 "Privasi: tanpa cookie & UU PDP" di `references/panduan-umami.md` berisi saran kalimat untuk kebijakan privasi website Anda (bukan nasihat hukum).

## Riwayat perubahan

Versi terkini: **1.0.6**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
