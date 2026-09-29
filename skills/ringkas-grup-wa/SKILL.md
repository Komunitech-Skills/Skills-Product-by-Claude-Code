---
name: ringkas-grup-wa
description: Meringkas ekspor chat grup WhatsApp (.txt/.zip "Tanpa Media") menjadi daftar Perlu Perhatian, Info, dan Obrolan, plus daftar tindakan siapa-apa-tenggat dengan kutipan asli, tanpa mengarang isi. Gunakan saat pengguna menempel/mengunggah ekspor chat grup WA dan minta "ringkas grup", "apa yang perlu saya tanggapi", "rekap grup", atau WhatsApp group summary, chat digest, catch me up on this group.
---

# Ringkas Grup WhatsApp

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Grup WA kerja/proyek/komunitas sering punya ratusan pesan yang tenggelam. Skill ini membaca
**ekspor chat resmi WhatsApp** (fitur bawaan, bukan sadap/pantau diam-diam), mem-parsing pesan
secara terstruktur lewat script, lalu memilah mana yang **perlu ditanggapi**, mana yang sekadar
**info**, dan mana yang **obrolan biasa** — plus daftar tindakan siap tindak lanjut. Prinsip
utama: **setia pada isi asli**. Tidak ada isi yang ditambahkan; yang ambigu diberi tanda.

## Kapan digunakan
- Pengguna mengirim/menempel path file ekspor chat WhatsApp (`.txt` atau `.zip` "Tanpa Media") dan minta diringkas.
- Pengguna minta "apa yang perlu saya tanggapi di grup X", "rekap grup kerja hari ini/minggu ini", "catch me up" grup WA.
- Grup sangat ramai (ratusan pesan/hari) dan pengguna hanya butuh yang penting.

## Kapan TIDAK digunakan
- **Memantau grup/chat orang lain diam-diam tanpa sepengetahuan mereka** (mis. menyadap chat karyawan, pasangan, atau grup yang bukan milik pengguna) — **tolak**, jelaskan alasan etika & UU PDP (lihat Batasan).
- Rapat formal dengan transkrip Zoom/Meet/Teams → pakai `notulen-rapat` (format lebih lengkap: agenda, peserta, keputusan resmi).
- Grup keluarga, pasien/klinik, atau HR yang sangat sensitif dan pengguna mempertimbangkan **bot ikut memantau grup secara live** → **sarankan Jalur 1 (ekspor)**, bukan Jalur 2 (bot di grup); lihat `references/openclaw-grup.md`.
- Chat pribadi 1-on-1 (bukan grup) → ringkasan tetap bisa dibuat tapi konteksnya beda; tanyakan apakah tetap ingin diproses skill ini.
- Mentranskrip audio/video: skill ini tidak mentranskrip apa pun.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| File ekspor chat (path `.txt` atau `.zip`) | Ya | — (minta ekspor dulu, lihat README untuk caranya) |
| Rentang waktu (mis. "sejak kemarin 17.00", "3 hari terakhir", atau kosong = semua) | Tidak | Semua pesan dalam file |
| Nama saya di grup (untuk deteksi mention "perlu perhatian" & memisahkan pesan sendiri) | Tidak | Tanyakan sekali bila relevan; jika tidak dijawab, deteksi mention pakai `@` umum saja |
| Samarkan nama anggota? | Tidak | Tidak disamarkan, kecuali pengguna eksplisit minta anonim/rahasia. **Bersifat upaya terbaik** — lihat langkah 2 & Batasan. |

Jika file ekspor tidak ada, **minta pengguna mengekspor dulu** dengan langkah singkat ini (agent tidak selalu bisa membaca README pembeli):
- **Android:** buka grup → ⋮ (kanan atas) → Lainnya → **Ekspor chat** → **Tanpa media** → kirim file ke chat bot/Telegram atau simpan ke folder.
- **iPhone:** buka grup → ketuk nama grup → gulir ke bawah → **Ekspor Chat** → **Tanpa Media** → kirim/simpan file `.zip`.

Tanpa file ekspor — jangan mencoba meringkas dari ingatan/tempelan sebagian chat yang tidak lengkap tanpa memberi tahu keterbatasannya.
Jika info lain kurang, **jangan tanya lebih dari sekali**: proses dengan default di atas dan sebutkan asumsi di akhir.

## Langkah kerja
1. **Pastikan ini grup milik/diikuti pengguna sendiri**, bukan permintaan memantau orang lain tanpa izin. Jika ragu, tanyakan singkat: "Ini grup yang kamu ikuti sendiri kan?" Jika jawabannya menyiratkan menyadap pihak lain → tolak dan jelaskan alasannya (lihat Batasan).
2. **Jalankan parser** pada file ekspor. Path relatif terhadap folder `SKILL.md` ini; Windows pakai `python` atau `py`:
   ```bash
   python3 <folder-skill-ini>/scripts/parse_ekspor_wa.py "<path file .txt atau .zip>" --indent 0
   ```
   Tambahkan sesuai kebutuhan:
   - `--sejak "kemarin 17:00"` atau `--sejak "2026-09-12 08:00"` — hanya pesan sejak waktu itu.
   - `--hari-terakhir 3` — hanya 3 hari terakhir.
   - `--nama-saya "<nama Anda di grup>"` — menandai pesan Anda sendiri (`dari_saya`) dan membuat deteksi mention langsung ke Anda lebih akurat di `kandidat_perlu_perhatian`. Tanyakan sekali di awal jika belum tahu; boleh dilewati.
   - `--samarkan` — samarkan (**upaya terbaik, bukan jaminan mutlak**) pengirim, nama yang disebut di isi pesan/@mention/pesan sistem, sapaan+nama pihak yang bukan anggota terdaftar (mis. "Pak Budi" jadi "Orang N"), dan nomor telepon (Indonesia & internasional). **WAJIB**: setelah pakai `--samarkan`, periksa field `kemungkinan_nama_tersisa` di hasil JSON — itu daftar kata/frasa berhuruf kapital yang *mungkin* masih nama dan lolos dari penyamaran otomatis. Sebutkan isinya ke pengguna sebagai "perlu dicek manual sebelum dibagikan" bila tidak kosong; **jangan mengklaim hasil 100% anonim**.
   - Script punya uji regresi sendiri: `python3 <folder-skill-ini>/tests/uji_regresi.py` (untuk pengecekan, bukan langkah wajib tiap pemakaian).
3. **Baca JSON hasil script.** Field penting: `format_terdeteksi`, `urutan_tanggal` (dan `catatan` bila ambigu — sebutkan catatan ini ke pengguna apa adanya, jangan disembunyikan, termasuk peringatan "hanya satu kombinasi tanggal" bila muncul), `statistik` (jumlah pesan per pengirim, jam paling ramai, jumlah media/dihapus), `kandidat_perlu_perhatian[]`, dan `hari[]` (pesan sudah dikelompokkan per tanggal).
4. **Gunakan `kandidat_perlu_perhatian[]` sebagai checklist WAJIB, terutama untuk grup padat (>~50 pesan/hari).** Script menandai setiap pesan obrolan yang mengandung tanda tanya, mention, kata uang/nominal, tenggat/tanggal, atau kata keputusan/komplain. **Setiap item di daftar ini harus dipertimbangkan** (dimasukkan ke Perlu Perhatian, Info, atau sengaja dikeluarkan dengan alasan) — jangan menyisir ulang dari nol tanpa mencocokkan ke checklist ini, supaya tidak ada pertanyaan/tenggat/nominal yang terlewat. Lalu klasifikasikan tiap pesan `jenis: "obrolan"` (lewati `jenis: "sistem"`, hanya dihitung) ke salah satu:
   - **Perlu perhatian**: pertanyaan langsung ke pengguna atau mention nama/`@pengguna`, permintaan keputusan/persetujuan, tenggat/deadline, uang/pembayaran/tagihan, komplain/masalah. Tandai `✅ sudah dijawab` bila jawabannya ada di pesan lain yang lebih baru pada topik yang sama, atau `❗ masih menunggu` bila belum ada jawaban sampai akhir rentang yang diringkas.
   - **Info**: pengumuman, update status, info tanpa perlu balasan.
   - **Obrolan**: salam, candaan, stiker/emoji saja, basa-basi. **Cukup dihitung jumlahnya**, jangan dikutip satu-satu.
   - Pesan `jenis: "media"` → catat sebagai info singkat ("Budi mengirim media (foto/video), 08.10") kecuali konteksnya jelas penting.
   - Pesan `jenis: "dihapus"` → sebutkan bahwa ada pesan yang dihapus pengirimnya, jam & siapa (jika tidak disamarkan), tanpa menebak isinya.
   - Jika `--nama-saya` diberikan, pesan dengan `dari_saya: true` boleh dikecualikan dari "Perlu Perhatian ke Anda" (itu perkataan Anda sendiri), tapi tetap dihitung dalam statistik/daftar tindakan bila relevan (mis. Anda berjanji melakukan sesuatu).
5. **Jangan mengarang.** Jika maksud pesan ambigu (mis. pertanyaan retoris vs. serius, sudah dijawab di pesan lain atau belum), masukkan ke Perlu Perhatian dengan tanda `⚠️` dan alasan singkat, daripada menghilangkannya atau memastikan tanpa dasar.
6. **Susun daftar tindakan** (siapa – apa – tenggat) memakai format yang sama dengan `notulen-rapat`: PIC diambil dari pengirim tugas/yang diberi tugas jika jelas dari teks; tenggat mengikuti tulisan asli (jangan menghitung ulang tanggal relatif secara otomatis di sini — jika ingin dikonversi presisi, arahkan ke `notulen-rapat` yang punya `scripts/tanggal_relatif.py`). Tugas tanpa PIC/tenggat jelas → tandai `⚠️ belum jelas`.
7. **Sertakan kutipan asli singkat + jam** untuk tiap butir Perlu Perhatian (maks ±15 kata kutipan, bukan parafrase, agar pengguna bisa mengecek langsung di grup).
8. **Grup sangat ramai** (statistik total pesan tinggi, atau rentang > 1 hari dengan ratusan pesan/hari): sajikan **per hari** memakai grouping `hari[]` dari JSON, hari terbaru duluan; jangan gabung jadi satu daftar panjang tak terkelompok.
9. Tutup dengan ringkasan angka singkat (statistik) dan tawarkan: ringkas rentang waktu lain, atau ubah ke daftar tindakan saja untuk kirim ke grup (bukan skill ini yang mengirim — pengguna yang menyalin/mengirim sendiri).

## Format output
```
📋 RINGKASAN GRUP: [nama grup, jika diketahui dari nama file/konteks]
Rentang: [tanggal awal]–[tanggal akhir] · [N] pesan (dari [jumlah anggota aktif] orang)
[Catatan format/tanggal dari script, jika ada — tulis apa adanya]

🔴 PERLU PERHATIAN ([n])
1. [08.15] Sari: "kalau supplier kain belum bayar invoice bulan lalu gimana pak?"
   → butuh keputusan/balasan dari Anda
2. ...

📌 DAFTAR TINDAKAN
| Tugas | PIC | Tenggat |
|---|---|---|
| ... | ... | ... atau ⚠️ belum jelas |

🔵 INFO ([n])
- [jam] [ringkasan satu baris info, bukan kutipan penuh]

💬 OBROLAN
[n] pesan obrolan/candaan/stiker (tidak ditampilkan satu-satu)

📎 Lampiran/media: [n] · 🗑️ Pesan dihapus: [n]
⏰ Jam paling ramai: [dari statistik]

[Jika dibagi per hari, ulangi blok di atas per tanggal, terbaru di atas]

[Asumsi yang dipakai, jika ada]
```

## Contoh
**Input pengguna:** "Ringkas grup toko dari file ekspor ini, yang perlu saya tanggapi aja." (melampirkan `WhatsApp Chat with Toko Kue.zip`)

**Langkah:** jalankan `python3 scripts/parse_ekspor_wa.py "WhatsApp Chat with Toko Kue.zip" --indent 0`, baca hasil JSON (16 pesan, format Android, urutan d/m).

**Output (ringkas):**
```
📋 RINGKASAN GRUP: Toko Kue
Rentang: 12–13 Sep 2026 · 16 pesan (dari 4 orang)

🔴 PERLU PERHATIAN (2)
1. [08.15] Sari: "kalau supplier kain belum bayar invoice bulan lalu gimana pak? sudah lewat 2 minggu"
   → menunggu keputusan Anda soal pembayaran
2. [17.05] Budi: "oke fix ya kita naikkan harga produk A jadi Rp 85.000 mulai senin depan"
   → keputusan harga baru, pastikan tim admin tahu

📌 DAFTAR TINDAKAN
| Tugas | PIC | Tenggat |
|---|---|---|
| Transfer Rp 4.500.000 ke supplier kain | Budi | Sore ini (12 Sep) |
| Update katalog dengan harga baru Rp 85.000 | Sari | ⚠️ "Jumat depan" — cek tanggal pasti di notulen-rapat bila perlu presisi |

🔵 INFO (3)
- [08.10] Dimas mengirim media (foto stok gudang)
- [09.00] Fajar bergabung ke grup
- [09.10] Dimas menghapus satu pesan (isi tidak diketahui)

💬 OBROLAN
4 pesan obrolan/sapaan (mis. "siap pak", "halo semua 👋")

📎 Lampiran/media: 1 · 🗑️ Pesan dihapus: 1
⏰ Jam paling ramai: 08.00–09.00
```

## Checklist sebelum mengirim hasil
- [ ] Tidak ada isi/keputusan/nominal yang tidak ada di kutipan asli.
- [ ] Setiap butir Perlu Perhatian punya kutipan singkat + jam, bukan parafrase bebas.
- [ ] Setiap item di `kandidat_perlu_perhatian[]` sudah dipertimbangkan (masuk kategori, atau sengaja dikeluarkan).
- [ ] Catatan `urutan_tanggal`/ambiguitas dari script disampaikan ke pengguna, tidak disembunyikan — termasuk peringatan "satu kombinasi tanggal" bila ada.
- [ ] Daftar tindakan: setiap baris punya PIC & tenggat, atau ditandai ⚠️.
- [ ] Grup ramai (>~150 pesan atau >1 hari) disajikan per hari.
- [ ] Kalau `--samarkan` dipakai: `kemungkinan_nama_tersisa` sudah dicek dan disampaikan ke pengguna bila tidak kosong; tidak diklaim "100% anonim".
- [ ] Statistik (jumlah per pengirim, jam ramai, media/dihapus) disertakan.

## Batasan & penanganan error
- **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.
- **Tidak pernah memantau/menyadap diam-diam.** Skill ini hanya memproses ekspor yang pengguna buat sendiri secara sadar dari grup yang mereka ikuti. Permintaan meringkas chat/grup orang lain tanpa sepengetahuan mereka (mis. pasangan, karyawan) **ditolak** — jelaskan bahwa itu melanggar privasi dan berpotensi melanggar UU PDP, dan skill tidak dirancang untuk itu.
- **Privasi anggota grup**: isi grup adalah data pribadi orang lain, dan akan diproses oleh penyedia model AI yang dipakai pengguna. Ingatkan ini terutama untuk grup yang bukan seluruhnya kolega kerja (mis. ada anggota keluarga/pelanggan/pasien) dan tawarkan `--samarkan`. Untuk grup yang sangat sensitif (keluarga, pasien, HR), sarankan tetap pakai Jalur 1 (ekspor manual) dan **jangan** menyarankan Jalur 2 (bot live di grup) — lihat `references/openclaw-grup.md` untuk alasannya.
- **`--samarkan` bersifat upaya terbaik (best-effort), BUKAN jaminan mutlak.** Script mengganti pengirim, nama yang disebut di isi pesan/@mention/pesan sistem (termasuk kata depan/panggilan seperti "Budi" dari "Budi Santoso"), sapaan+nama pihak luar ("Pak Budi" → "Orang N"), dan nomor telepon Indonesia & internasional. Yang **tidak** selalu tertangkap: nama tanpa huruf kapital konsisten, singkatan/inisial, ejaan nama yang berbeda-beda, nama yang menyatu dengan kata lain tanpa spasi, atau nama yang kebetulan sama dengan kata umum. **Selalu** sampaikan isi `kemungkinan_nama_tersisa` ke pengguna sebagai daftar yang perlu dicek manual sebelum hasil dibagikan ke pihak lain — jangan pernah bilang hasilnya "pasti anonim".
- **Tidak mengirim apa pun ke grup atau ke siapa pun.** Skill hanya menghasilkan teks ringkasan untuk pengguna; pengguna yang menyalin/meneruskan sendiri.
- **Script gagal jalan (Python tidak tersedia):** jangan menebak-nebak isi ratusan pesan secara manual. Minta pengguna memastikan Python 3 terpasang, atau tempelkan langsung sepotong isi chat (bukan file penuh) untuk diringkas manual dengan disclaimer "tidak melalui parser terverifikasi, mohon dicek ulang jam & urutannya".
- **Format ekspor tidak dikenali / 0 pesan terbaca**: sampaikan pesan `catatan` dari script apa adanya ke pengguna, dan minta contoh 2–3 baris asli dari file untuk dicek manual polanya. Jangan mengarang bahwa file "kosong" bila sebenarnya formatnya di luar dukungan.
- **Urutan tanggal ambigu** (`urutan_tanggal` disertai catatan): sampaikan asumsi (default d/m Indonesia) ke pengguna dan minta koreksi bila hasilnya terasa janggal (mis. bulan yang tidak masuk akal).
- **File sangat besar** (ekspor tahunan, puluhan ribu pesan): sarankan mempersempit dengan `--sejak`/`--hari-terakhir` dulu agar hasil tetap relevan dan tidak melebihi kapasitas model.
- **Mode live di grup (bot ikut membaca semua chat)** bukan cakupan skill ini — lihat `references/openclaw-grup.md` untuk panduan konfigurasi OpenClaw beserta batasannya, dan sampaikan ke pengguna bahwa itu jalur terpisah dengan risiko & langkah setup berbeda (bukan sekadar mengetik satu perintah).
- **Batasan yang diketahui, tidak diperbaiki (jarang terjadi di ekspor WA asli):** nama kontak yang secara tidak wajar mengandung karakter `:` hanya terbaca sebagian (dipotong di `:` pertama). WhatsApp tidak mengizinkan `:` di nama kontak, jadi ini praktis hanya muncul pada file yang sudah diedit manual.
