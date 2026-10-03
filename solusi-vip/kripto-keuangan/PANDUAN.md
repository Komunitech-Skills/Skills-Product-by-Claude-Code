# Panduan Solusi VIP — Riset Kripto & Keuangan Pribadi

Untuk member VIP komunitech.com yang ingin **memahami, mencatat, dan memantau** dunia kripto
serta merapikan keuangan pribadi. Bahasa sehari-hari, langkah demi langkah. Setiap langkah
punya **cara cek berhasil** dan **kalau gagal**.

> **Paket ini untuk member VIP (akses semua skill).** Inti paket ini, `pantau-pasar-kripto`
> (notifikasi harga, ringkasan pagi, checklist riset, jurnal), hanya ada di akses penuh VIP dan
> ditandai **[VIP]** di bawah. Tidak ada bundle ecer untuk paket ini.

## Mulai dari sini
- **Pemakaian sehari-hari = ngobrol dengan agen OpenClaw** (Telegram atau chat OpenClaw)
  dengan kalimat biasa seperti contoh di Bab 5.
- **`jadwal-openclaw.md` hanya untuk pemasangan sekali** (membuat jadwal notifikasi otomatis).
  Itu pekerjaan terminal: minta bantuan orang teknis atau **jasa setup berbayar Komunitech**.
- **Gateway** = program OpenClaw yang berjalan di sebuah komputer dan menjalankan jadwal.

> **PERINGATAN RISIKO — baca dulu.** Paket ini adalah alat **informasi dan pencatatan**.
> **Bukan nasihat investasi, bukan rekomendasi beli/jual/tahan, bukan sinyal trading.**
> Aset kripto berisiko tinggi: harga bisa turun tajam dan Anda bisa kehilangan seluruh modal.
> Keputusan dan risikonya sepenuhnya milik Anda. Hanya gunakan uang yang siap Anda relakan.
> Tidak ada yang dapat menjamin keuntungan; janji "untung pasti" adalah tanda penipuan.

## Apa yang bisa dan tidak bisa dilakukan paket ini

| Bisa (**[VIP]** = butuh `pantau-pasar-kripto`) | Tidak (sengaja, keputusan Komunitech) |
|---|---|
| Ringkasan pagi: harga + berita **bertautan sumber** | Auto-trading **di paket ini** (tersedia terpisah lewat `bot-trading-kripto`, belum masuk paket, lihat Bab 0) |
| Notifikasi bila harga menyentuh ambang **yang Anda tetapkan sendiri** | Rekomendasi beli/jual/tahan, target harga, sinyal entry/exit |
| Checklist riset proyek (fakta, tim, audit, tokenomics, tanda penipuan) | Skill di paket ini menyimpan API key exchange atau mengeksekusi order |
| Jurnal trading: rapikan catatan, hitung untung/rugi (dihitung script) | Sinyal/strategi buatan Komunitech, janji profit |
| Anggaran, dana darurat, pelunasan utang, target tabungan | Prediksi harga atau "koin yang akan naik" |
| Catatan riset lokal & tulisan riset bersitasi | Grup sinyal, kelola dana orang lain |

---

## 0. Auto-trading: hanya lewat `bot-trading-kripto`, dengan syarat ketat

**Status (2026-10-01):** auto-trading **diizinkan** (keputusan pemilik Komunitech 2026-09-29)
dan disediakan oleh skill terpisah **`bot-trading-kripto`**. Skill itu **belum masuk paket VIP
ini** sampai uji testnet selesai (ditunda pemilik). Skill di paket ini (`pantau-pasar-kripto`
dkk.) tetap **tidak** mengeksekusi order dan tetap menolak permintaan auto-trading; bila Anda
memintanya, agent akan menjelaskan status ini.

Saat `bot-trading-kripto` tersedia, syaratnya **wajib semua**:
1. **Aturan milik Anda sendiri** (mis. DCA, grid, take-profit/stop-loss, rebalancing) di
   **akun bursa Anda sendiri**. Komunitech **tidak** memberi sinyal, rekomendasi beli/jual,
   strategi "pasti cuan", atau janji profit.
2. **Default simulasi:** backtest → paper trading (harga asli, order pura-pura) → testnet
   (uang mainan) → baru live setelah konfirmasi bertahap.
3. **API key tanpa izin tarik dana (withdraw MATI)**, idealnya dibatasi IP, disimpan sendiri
   oleh Anda (bukan ditempel ke chat). Untuk Indodax: daftar periksa + pernyataan yang Anda
   ketik sendiri bahwa izin tarik dana mati; skill tidak pernah memanggil metode withdraw.
4. **Batas risiko wajib:** modal maks per order & total, stop-loss, batas rugi harian,
   maks order terbuka, dan **tombol berhenti** (hentikan bot kapan saja lewat chat).
5. **Disclaimer risiko:** kripto berisiko tinggi; bot menjalankan aturan Anda apa adanya,
   termasuk saat aturan itu merugi. Keputusan dan risiko sepenuhnya milik Anda.

Kenapa syaratnya ketat:
- **Kesalahan = uang sungguhan.** Order yang sudah tereksekusi tidak bisa ditarik.
- **Konten web bisa disusupi** (*prompt injection*); karena itu bot hanya menjalankan aturan
  tertulis Anda, bukan "pendapat" AI dari berita.
- **Kunci bursa adalah kunci brankas.** Tanpa izin tarik dana, kunci yang bocor tidak bisa
  dipakai menguras saldo ke luar akun.
- **Komunitech tidak berizin memberi nasihat investasi** (diatur OJK), jadi strategi tetap
  milik Anda.

**Sebelum bot tersedia (atau bila Anda tidak ingin bot):** pakai fitur limit/stop order
**bawaan aplikasi bursa resmi** (Anda pasang sendiri di sana), ditambah notifikasi harga dan
jurnal dari paket ini.

**Kalau Anda pernah menempel API key exchange ke chat mana pun:** anggap sudah bocor.
**Cabut (revoke)** di exchange sekarang, lalu buat yang baru. Skill tidak akan menyimpan
atau mengulangnya.

**Bursa/exchange:** gunakan hanya bursa/penyelenggara perdagangan aset kripto yang
**terdaftar/berizin OJK**. Cek daftar resmi terbaru di **ojk.go.id** sebelum menyetor dana.
Dugaan penipuan/investasi ilegal: hubungi **OJK 157** atau **Satgas PASTI**. Aturan dapat
berubah; catatan ini bukan kepastian hukum.

---

## 1. Prasyarat

1. **OpenClaw sudah terpasang dan bisa diajak chat.** Ketik "halo".
2. **Mesin Gateway harus menyala di jam notifikasi.** Notifikasi harga per jam hanya jalan bila
   mesin menyala. Pilih: **(a)** laptop/PC yang menyala di jam yang Anda inginkan;
   **(b)** mini PC/laptop bekas yang menyala 24 jam; **(c)** VPS milik Anda sendiri;
   **(d)** **jasa setup berbayar Komunitech** untuk memasang & menguji (b)/(c).
   - **Cara cek berhasil:** Anda tahu mesin mana yang menjalankan Gateway dan kapan menyala.
   - **Kalau belum yakin:** mulai dengan ringkasan pagi saja (Bab 5b, **[VIP]**), saat laptop biasanya menyala.
   - Ingat: pasar kripto buka 24 jam, tapi notifikasi **tidak terkirim** saat mesin mati.

---

## 2. Pasang paket skill

(Pekerjaan sekali saja; buka **Terminal**/**PowerShell**, masuk ke folder hasil ekstrak ZIP.)
Skill: `karyawan-ai-mulai`, `cek-privasi-openclaw`, `atur-keuangan-pribadi`,
`notebook-riset-lokal`, `asisten-tulis-riset`, dan **[VIP]** `pantau-pasar-kripto`.

```bash
openclaw skills install ./karyawan-ai-mulai --global
openclaw skills install ./cek-privasi-openclaw --global
openclaw skills install ./atur-keuangan-pribadi --global
openclaw skills install ./notebook-riset-lokal --global
openclaw skills install ./asisten-tulis-riset --global
openclaw skills install ./pantau-pasar-kripto --global   # [VIP]
```
(Jalankan dari folder hasil ekstrak ZIP paket. Windows tanpa WSL: salin folder skill lewat File
Explorer ke `%USERPROFILE%\.openclaw\skills\`. Lihat `docs/instalasi.md`.)

- **Cara cek berhasil:** `openclaw skills list` menampilkan keenam nama (lima tanpa `pantau-pasar-kripto` bila tidak VIP).
- **Kalau gagal:** "already exists" aman dilewati; skill tidak muncul → pastikan folder yang
  disalin langsung berisi `SKILL.md`, buka sesi baru (`/new`); `exec` ditolak → salin manual.

---

## 3. Jalankan `karyawan-ai-mulai` lalu `cek-privasi-openclaw`

1. Ketik: **"mulai karyawan AI, saya ingin riset kripto dan atur keuangan pribadi"**. Jawab
   pertanyaan singkatnya. **Cek berhasil:** ada rekomendasi 3 skill + 1 hasil nyata.
2. Ketik: **"cek privasi saya"**. Catatan keuangan dan jurnal trading adalah data sensitif.
   Perbaikan dijalankan satu per satu dengan izin Anda.
   - **Cek berhasil:** laporan lampu lalu lintas 🔴/🟡/🟢 dengan bahasa awam.
   - **Kalau gagal:** ikuti perintah salin-tempel di terminal, tempel hasilnya ke chat.

**Aturan emas:** jangan pernah menempel **seed phrase / kunci privat / password / API key
exchange** ke chat AI. Tidak ada langkah di paket ini yang memintanya.

### Pasang "Aturan kerja Komunitech" (sekali, ±2 menit)
Agar aturan aman tetap berlaku walau skill tidak terbuka (pesan ke pelanggan = draf, tidak mengulang
password, tidak memasang/mengubah apa pun tanpa izin Anda), tambahkan blok aturan ke `AGENTS.md`
OpenClaw — file ini dibaca di setiap percakapan. `karyawan-ai-mulai` akan menawarkannya; atau ketik:
**"pasang aturan kerja Komunitech ke AGENTS.md"**. Isi blok ada di
`templates/openclaw-AGENTS-komunitech.md` (paket VIP). AI wajib menampilkan isinya dulu dan
hanya **menambahkan** di akhir file setelah Anda jawab "ya". Cara manual: Control UI →
Settings → Agents → Files → `AGENTS.md`, tempel blok di bagian paling bawah, simpan.

- **Cara cek berhasil:** buka sesi baru (`/new`), ketik "apa aturan kerja Komunitech?" — AI
  menyebut aturannya tanpa membuka file lain.

### WAJIB untuk paket kripto: tambahkan "Aturan kripto Komunitech" di bawah blok umum
Uji gabungan 3 Okt 2026 menemukan AI mencari CLI ke seluruh disk (`find /`) dan memeriksa
config gateway/kanal sendiri saat diminta "pasang alert", mengarang ambang untuk koin yang
tidak diberi ambang, dan tidak menyebut bahwa harga BTC sudah di bawah ambang yang diminta.
Tempel blok berikut di bawah blok umum di `AGENTS.md` (cara sama seperti di atas):

```markdown
## Aturan kripto Komunitech (wajib)

Berlaku di SETIAP percakapan, juga saat tidak ada skill yang dibuka. Jelaskan alasannya singkat bila menolak.

1. Skill ada di folder skills OpenClaw. Jangan mencari skill/CLI/file ke seluruh disk (`find /`, `locate`), jangan memeriksa atau mengubah config OpenClaw/gateway/kanal (termasuk `gateway config.get`, `openclaw doctor`, menanyakan isi `openclaw.json` ke tool/agent lain), dan jangan meminta token bot ke chat.
2. Jadwal/notifikasi: setelah pengguna menjawab "ya", coba buat jadwal SATU kali. Gagal/tidak tersedia/kanal belum siap → LANGSUNG berhenti: tanpa coba ulang, tanpa cek status berulang, tanpa mencari CLI/berkas (`find`, `which`, `ls` di luar folder skill); tempel draf perintah jadwal siap tempel (`scripts/draf_jadwal.py` skill pantau-pasar-kripto) untuk dipasang pemilik atau jasa setup Komunitech.
3. Ambang notifikasi HANYA dari pengguna. Bila tidak diberi, tanyakan; jangan mengisi angka sendiri (juga bukan "default"). Koin tanpa ambang = hanya ditampilkan harganya.
4. Saat memasang/mengubah alert, selalu tampilkan harga terkini (sumber + jam WIB) dan bandingkan dengan setiap ambang; sebut terang-terangan bila ambang SUDAH TERLEWATI (alert akan langsung terpicu).
5. Tautan berita harus URL artikel asli, bukan redirect agregator (mis. news.google.com/rss/...). Berita tanpa tautan asli tidak dimasukkan, atau ditaruh di akhir dengan tanda "[tanpa tautan]".
6. Tanpa sinyal/rekomendasi beli-jual-tahan, target harga, atau janji profit; jangan meneruskan proyeksi harga dari artikel. Penolakan menyebut OJK (POJK 27/2024), cek PAKD berizin di ojk.go.id, Satgas PASTI / OJK 157, dan diakhiri: "Informasi, bukan nasihat investasi. Keputusan & risiko sepenuhnya milik Anda."
7. API key/secret/seed phrase yang ditempel tidak diulang (sebagian maupun utuh) dan tidak disimpan; sarankan segera dicabut (revoke) dan dibuat ulang tanpa izin tarik dana.
8. Auto-trading/bot eksekusi order: ditunda — `bot-trading-kripto` belum termasuk paket ini. Jelaskan statusnya dan tawarkan limit/stop order bawaan aplikasi bursa resmi yang dipasang sendiri.
```

- **Cara cek berhasil:** sesi baru, ketik "apa aturan kripto Komunitech?" — AI menyebut 8 aturan di atas.

---

## 4. Hubungkan bot Telegram (kanal default)

(Sekali saja; boleh dibantu orang teknis atau jasa setup Komunitech.)
1. Di Telegram buka **@BotFather**, kirim `/newbot`, beri nama, salin **token**.
2. Ketik ke OpenClaw: *"Tambahkan kanal Telegram dengan token ini: <token>"* (atau
   `openclaw channels add --channel telegram --token <token>`).
3. Kirim "halo" ke bot Anda. Bila diminta persetujuan: `openclaw pairing approve telegram <KODE>`
   (kode dari `openclaw pairing list telegram`).
4. Kirim pesan ke **@userinfobot** untuk mengetahui **ID chat** Anda; catat angkanya.

- **Cara cek berhasil:** bot membalas "halo", ID chat tercatat di catatan pribadi.
- **Kalau gagal:** token salah salin (ada spasi) atau pairing belum disetujui.

**WhatsApp:** hanya notifikasi ke diri sendiri, **nomor terpisah**, dengan persetujuan risiko
tertulis (teks di `jadwal-openclaw.md` §0). Telegram lebih aman dari risiko blokir.

---

## 5. Rutinitas

### a. **[VIP]** Tetapkan daftar pantauan Anda sendiri (sekali)
Ketik: *"Saya mau pantau BTC dan ETH. Beri tahu saya kalau turun lebih dari 5% dalam sehari
atau harga BTC menyentuh Rp[angka]."* `pantau-pasar-kripto` membuat `kripto/PANTAU.md` dan
`kripto/konfigurasi.json`. **Angka ambang selalu dari Anda**, bukan dari AI. Skill tidak
akan menyarankan angka ambang "yang bagus" karena itu sama dengan memberi sinyal.
- **Cara cek berhasil:** skill menampilkan ulang daftar koin dan ambang untuk Anda konfirmasi.
- **Kalau gagal:** format aneh ("5 persen", "seratus juta") ditafsirkan lalu **ditunjukkan untuk
  dikonfirmasi** sebelum disimpan.

### b. **[VIP]** Ringkasan pagi: harga + berita bertautan sumber, 07.00 WIB (terjadwal)
Ketik: *"Kirimi saya ringkasan pagi kripto jam 7 lewat Telegram."* Isinya: harga koin pantauan,
judul berita **dengan tautan sumber**, dan disclaimer. Tanpa kesimpulan beli/jual. Bila AI tidak
punya akses pencarian web, ia jujur bilang berita tidak bisa dibuat dan hanya mengirim harga.
- **Cara cek berhasil:** jadwal diuji sekali (`automations run <id> --wait`), hasilnya dilihat
  sebelum dinyatakan aktif.

### c. **[VIP]** Notifikasi harga sesuai ambang Anda, per jam (terjadwal)
Ketik: *"Aktifkan notifikasi ambang harga kripto tiap jam."* Job berjalan tiap jam tetapi
**diam bila tidak ada yang terlewati**; pesan hanya muncul saat ambang **Anda** tersentuh atau
pemantauan bermasalah (data gagal/basi). Data basi selalu diberi label, angka tidak pernah
dikarang.
- **Kalau gagal:** uji dulu dengan data tenang (harus tidak ada pesan) lalu data ambang terlewati.

### d. **[VIP]** Riset proyek dengan checklist (manual)
Ketik: *"Riset proyek [nama koin]: saya ingin tahu fakta-faktanya."* Hasilnya checklist due
diligence (tim, audit, tokenomics, aktivitas, legalitas di Indonesia, tanda skema penipuan)
**tanpa kesimpulan beli/jual**. Tanda bahaya disebut netral & edukatif.

### e. **[VIP]** Jurnal trading & hitung untung/rugi (manual)
Ketik: *"Rapikan jurnal trading saya dan hitung untung/rugi bulan ini"* dan tempel/kirim
catatan Anda (tanggal, koin, harga, jumlah, biaya). Untung/rugi **dihitung script**, bukan ditebak; Anda menilai sendiri dari tabelnya.
Skill tidak menganalisis pola perilaku Anda dan tidak memberi saran transaksi. Catat alasan/rencana
Anda sendiri di kolom catatan jurnal. Untuk pajak atas transaksi kripto, tanyakan konsultan pajak.

### f. Anggaran & keuangan pribadi (manual)
`atur-keuangan-pribadi` menghitung dengan script: anggaran bulanan (zero-based, dibanding
50/30/20), dana darurat, pelunasan utang (avalanche/snowball), konversi bunga flat ke efektif,
dan tabungan bulanan untuk target. Contoh: *"Gaji saya Rp8 juta, tolong susun anggaran."* atau
*"Hitung dana darurat untuk saya yang sudah menikah dengan 2 anak."* Ini **perencanaan**,
bukan nasihat produk keuangan tertentu.
- **Penting untuk yang trading:** susun dana darurat dan lunasi utang mahal (termasuk pinjol)
  **sebelum** menambah modal aset berisiko. `atur-keuangan-pribadi` menghitung rencana
  pelunasan utang dan memperingatkan pinjol ilegal serta pola gali lubang tutup lubang.

### g. Catatan riset lokal (manual, perlu aplikasi tambahan)
`notebook-riset-lokal` mengoperasikan **Open Notebook** (aplikasi sumber terbuka yang jalan di
komputer sendiri lewat Docker, alternatif NotebookLM; tidak berafiliasi dengan Komunitech):
kumpulkan PDF/artikel/catatan, lalu tanya-jawab dengan kutipan sumber. Cocok untuk whitepaper,
laporan bursa, atau aturan OJK/pajak yang Anda kumpulkan. Karena perlu Docker, tawarkan
**jasa setup berbayar Komunitech** bila Anda tidak nyaman memasangnya. Ketik: *"Buat notebook
riset dari file-file ini."* Tanpa aplikasinya, riset tetap bisa lewat 5d dan 5h.

### h. Menulis ringkasan riset (manual)
`asisten-tulis-riset` membantu menyusun tulisan/ringkasan riset **dengan sitasi** untuk
catatan pribadi atau bahan diskusi. Ia tidak mengarang sumber dan tidak menulis ajakan
membeli aset tertentu.

---

## 6. Setelah semua jadwal aktif
- Cek jadwal: *"jadwal apa saja yang aktif?"*; jeda: *"jeda notifikasi kripto saya."*
- Bila Anda bukan member VIP: bagian 5f–5h tetap bisa dipakai; bagian **[VIP]** tidak.
- `kripto/`, jurnal, dan catatan keuangan adalah data pribadi: simpan di komputer sendiri,
  jangan dibagikan; cadangkan berkala.
- Ulangi `cek-privasi-openclaw` bila menambah kanal/skill baru.
- Isi `CEKLIS.md` untuk serah-terima.

## Batasan dan penolakan yang akan Anda temui
- Diminta "kapan beli/jual?", "koin apa yang akan naik?", atau sinyal → ditolak sopan, disertai
  info singkat bahwa perdagangan kripto diawasi OJK (POJK 27/2024), cara cek platform berizin,
  dan kanal lapor Satgas PASTI / Kontak OJK 157; lalu ditawari data, checklist riset, jurnal,
  notifikasi ambang Anda.
- Diminta "buatkan bot trading" → skill di paket ini tidak mengeksekusi order; agent menjelaskan
  bahwa auto-trading hanya lewat `bot-trading-kripto` dengan syarat di Bab 0, dan skill itu
  belum termasuk paket ini.
- Paket ini bukan pengganti perencana keuangan, konsultan pajak, atau penasihat investasi
  berizin. Untuk keputusan besar, temui profesional berizin.
- Data harga berasal dari sumber publik pihak ketiga dan bisa tertunda atau gagal; skill akan
  mengatakannya, tidak menutupinya.
