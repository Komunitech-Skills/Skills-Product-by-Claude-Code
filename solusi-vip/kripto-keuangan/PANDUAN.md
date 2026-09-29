# Panduan Solusi VIP — Riset Kripto & Keuangan Pribadi

Untuk member VIP komunitech.com yang ingin **memahami, mencatat, dan memantau** dunia kripto
serta merapikan keuangan pribadi. Bahasa sehari-hari, langkah demi langkah. Setiap langkah
punya **cara cek berhasil** dan **kalau gagal**.

> **PERINGATAN RISIKO — baca dulu.** Paket ini adalah alat **informasi dan pencatatan**.
> **Bukan nasihat investasi, bukan rekomendasi beli/jual/tahan, bukan sinyal trading.**
> Aset kripto berisiko tinggi: harga bisa turun tajam dan Anda bisa kehilangan seluruh modal.
> Keputusan dan risikonya sepenuhnya milik Anda. Hanya gunakan uang yang siap Anda relakan.
> Tidak ada yang dapat menjamin keuntungan; janji "untung pasti" adalah tanda penipuan.

## Apa yang bisa dan tidak bisa dilakukan paket ini

| Bisa | Tidak (sengaja, keputusan Komunitech) |
|---|---|
| Ringkasan pagi: harga + berita **bertautan sumber** | Auto-trading / bot beli-jual otomatis |
| Notifikasi bila harga menyentuh ambang **yang Anda tetapkan sendiri** | Rekomendasi beli/jual/tahan, target harga, sinyal entry/exit |
| Checklist riset proyek (fakta, tim, audit, tokenomics, tanda penipuan) | Menyimpan API key/secret exchange atau mengeksekusi order |
| Jurnal trading: rapikan catatan, hitung untung/rugi (dihitung script) | Membuat/mengajari membuat bot trading |
| Anggaran, dana darurat, pelunasan utang, target tabungan | Prediksi harga atau "koin yang akan naik" |
| Catatan riset lokal & tulisan riset bersitasi | Grup sinyal, kelola dana orang lain |

---

## 0. Kenapa auto-trading tidak disediakan (penjelasan sopan)

Kami tahu banyak member menginginkan bot yang trading sendiri. Kami **sengaja tidak
menyediakannya**, dan permintaan itu akan ditolak dengan sopan oleh skill. Alasannya:

1. **Kesalahan AI = uang sungguhan yang hilang.** Model AI bisa salah membaca angka, salah
   paham perintah, atau "yakin tapi keliru". Order yang sudah dieksekusi tidak bisa ditarik.
2. **Berita dan halaman web bisa disusupi.** AI yang membaca konten dari internet dapat
   terkecoh oleh teks tersembunyi (*prompt injection*) yang mencoba memicu transaksi.
3. **Kunci exchange adalah kunci brankas.** API key yang tersimpan di komputer yang juga
   membaca konten luar adalah risiko keamanan. Bila bocor, dana bisa terkuras.
4. **Kami tidak berizin memberi nasihat investasi.** Pengelolaan dan rekomendasi transaksi
   aset keuangan adalah kegiatan yang diatur OJK. Kami memilih tetap menjadi alat bantu
   informasi yang jujur.
5. **Disiplin tetap di tangan Anda.** Alat terbaik untuk trader pemula bukan otomatisasi,
   melainkan **jurnal dan riset** yang membuat Anda belajar dari keputusan sendiri.

**Yang aman sebagai gantinya:** fitur limit/stop order **bawaan aplikasi exchange resmi**
(Anda yang memasang dan mengaturnya sendiri di sana), ditambah notifikasi harga dan jurnal
dari paket ini.

**Kalau Anda pernah menempel API key exchange ke chat mana pun:** anggap sudah bocor.
**Cabut (revoke)** di exchange sekarang, lalu buat yang baru. Skill tidak akan menyimpan
atau mengulangnya.

**Bursa/exchange:** gunakan hanya penyelenggara yang **terdaftar/berizin**. Sejak 2025 pengawasan
aset kripto beralih dari Bappebti ke **OJK** (masa transisi berakhir 20 Januari 2026 — cek
ojk.go.id untuk daftar terbaru). Selalu cek daftar resmi di **ojk.go.id** sebelum menyetor
dana. Dugaan penipuan/investasi ilegal: hubungi **OJK 157** atau **Satgas PASTI**. Aturan
dapat berubah; jangan menganggap catatan ini sebagai kepastian hukum terkini.

---

## 1. Prasyarat

1. **OpenClaw sudah terpasang dan bisa diajak chat.** Ketik "halo".
2. **Mesin Gateway harus menyala di jam notifikasi.** Notifikasi harga per jam hanya jalan bila
   mesin menyala. Pilih: **(a)** laptop/PC yang menyala di jam yang Anda inginkan;
   **(b)** mini PC/laptop bekas yang menyala 24 jam; **(c)** VPS milik Anda sendiri;
   **(d)** **jasa setup berbayar Komunitech** untuk memasang & menguji (b)/(c).
   - **Cara cek berhasil:** Anda tahu mesin mana yang menjalankan Gateway dan kapan menyala.
   - **Kalau belum yakin:** mulai dengan ringkasan pagi saja (Bab 5b), saat laptop biasanya menyala.
   - Ingat: pasar kripto buka 24 jam, tapi notifikasi **tidak terkirim** saat mesin mati.

---

## 2. Pasang paket skill

Skill: `karyawan-ai-mulai`, `cek-privasi-openclaw`, `pantau-pasar-kripto`,
`atur-keuangan-pribadi`, `notebook-riset-lokal`, `asisten-tulis-riset`.

```bash
openclaw skills install ./karyawan-ai-mulai --global
openclaw skills install ./cek-privasi-openclaw --global
openclaw skills install ./pantau-pasar-kripto --global
openclaw skills install ./atur-keuangan-pribadi --global
openclaw skills install ./notebook-riset-lokal --global
openclaw skills install ./asisten-tulis-riset --global
```
(Jalankan dari folder hasil ekstrak ZIP paket. Windows tanpa WSL: salin folder skill lewat File
Explorer ke `%USERPROFILE%\.openclaw\skills\`. Lihat `docs/instalasi.md`.)

- **Cara cek berhasil:** `openclaw skills list` menampilkan keenam nama.
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

---

## 4. Hubungkan bot Telegram (kanal default)

1. Di Telegram cari **@BotFather**, kirim `/newbot`, salin **token**.
2. Jalankan:
   ```bash
   openclaw channels add --channel telegram --token <token-dari-BotFather>
   ```
3. Kirim "halo" ke bot (memicu **pairing**), lalu setujui:
   `openclaw pairing list telegram` → `openclaw pairing approve telegram <KODE>` (berlaku 1 jam).
4. Catat **ID chat** Anda lewat **@userinfobot**. Angka ini dipakai di semua jadwal.

- **Cara cek berhasil:** bot membalas "halo", ID chat tercatat di catatan pribadi.
- **Kalau gagal:** token salah salin (ada spasi) atau pairing belum disetujui.

**WhatsApp:** hanya notifikasi ke diri sendiri, **nomor terpisah**, dengan persetujuan risiko
tertulis (teks di `jadwal-openclaw.md` §0). Telegram lebih aman dari risiko blokir.

---

## 5. Rutinitas

### a. Tetapkan daftar pantauan Anda sendiri (sekali)
Ketik: *"Saya mau pantau BTC dan ETH. Beri tahu saya kalau turun lebih dari 5% dalam sehari
atau harga BTC menyentuh Rp[angka]."* `pantau-pasar-kripto` membuat `kripto/PANTAU.md` dan
`kripto/konfigurasi.json`. **Angka ambang selalu dari Anda**, bukan dari AI. Skill tidak
akan menyarankan angka ambang "yang bagus" karena itu sama dengan memberi sinyal.
- **Cara cek berhasil:** skill menampilkan ulang daftar koin dan ambang untuk Anda konfirmasi.
- **Kalau gagal:** format aneh ("5 persen", "seratus juta") ditafsirkan lalu **ditunjukkan untuk
  dikonfirmasi** sebelum disimpan.

### b. Ringkasan pagi: harga + berita bertautan sumber, 07.00 WIB (terjadwal)
Ketik: *"Kirimi saya ringkasan pagi kripto jam 7 lewat Telegram."* Isinya: harga koin pantauan,
judul berita **dengan tautan sumber**, dan disclaimer. Tanpa kesimpulan beli/jual. Bila AI tidak
punya akses pencarian web, ia jujur bilang berita tidak bisa dibuat dan hanya mengirim harga.
- **Cara cek berhasil:** jadwal diuji sekali (`automations run <id> --wait`), hasilnya dilihat
  sebelum dinyatakan aktif.

### c. Notifikasi harga sesuai ambang Anda, per jam (terjadwal)
Ketik: *"Aktifkan notifikasi ambang harga kripto tiap jam."* Job berjalan tiap jam tetapi
**diam bila tidak ada yang terlewati**; pesan hanya muncul saat ambang **Anda** tersentuh atau
pemantauan bermasalah (data gagal/basi). Data basi selalu diberi label, angka tidak pernah
dikarang.
- **Kalau gagal:** uji dulu dengan data tenang (harus tidak ada pesan) lalu data ambang terlewati.

### d. Riset proyek dengan checklist (manual)
Ketik: *"Riset proyek [nama koin]: saya ingin tahu fakta-faktanya."* Hasilnya checklist due
diligence (tim, audit, tokenomics, aktivitas, legalitas di Indonesia, tanda skema penipuan)
**tanpa kesimpulan beli/jual**. Tanda bahaya disebut netral & edukatif.

### e. Jurnal trading & hitung untung/rugi (manual)
Ketik: *"Rapikan jurnal trading saya dan hitung untung/rugi bulan ini"* dan tempel/kirim
catatan Anda (tanggal, koin, harga, jumlah, biaya). Untung/rugi **dihitung script**, bukan
ditebak. Skill boleh menunjukkan pola (mis. kapan Anda sering keluar terlalu cepat) sebagai
refleksi pribadi, **bukan** sebagai saran transaksi berikutnya. Untuk pajak atas transaksi
kripto, konsultasikan ke konsultan pajak.

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
- `kripto/`, jurnal, dan catatan keuangan adalah data pribadi: simpan di komputer sendiri,
  jangan dibagikan; cadangkan berkala.
- Ulangi `cek-privasi-openclaw` bila menambah kanal/skill baru.
- Isi `CEKLIS.md` untuk serah-terima.

## Batasan dan penolakan yang akan Anda temui
- Diminta "kapan beli/jual?", "koin apa yang akan naik?", atau "buatkan bot trading" → ditolak
  sopan dan ditawari yang diperbolehkan: data, checklist riset, jurnal, notifikasi ambang Anda.
- Paket ini bukan pengganti perencana keuangan, konsultan pajak, atau penasihat investasi
  berizin. Untuk keputusan besar, temui profesional berizin.
- Data harga berasal dari sumber publik pihak ketiga dan bisa tertunda atau gagal; skill akan
  mengatakannya, tidak menutupinya.
