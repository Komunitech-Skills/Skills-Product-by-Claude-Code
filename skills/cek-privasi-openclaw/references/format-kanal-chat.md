# Format balasan di kanal chat (Telegram, WhatsApp, dll.)

Dibaca agent **sebelum menulis balasan pertama** bila pengguna chat lewat kanal pesan (atau
agent ragu). Pembacanya pemilik usaha awam yang membaca di HP: pesan pendek, bahasa sehari-hari,
tidak ada jalur komputer atau perintah terminal kecuali diminta. Semua pemeriksaan di SKILL.md
tetap dijalankan penuh; yang berubah hanya **cara menyampaikannya**.

## 1. Kerangka balasan pertama (≤ 3.000 karakter, termasuk spasi)

```
HASIL CEK PRIVASI BOT ANDA
Penilaian: <perlu dibereskan | cukup baik, ada yang bisa dirapikan | baik>. <A> berbahaya, <B> perlu perhatian, <C> sudah aman. Belum ada yang saya ubah.
Data Anda: <satu kalimat: tersimpan di komputer Anda sendiri; isi pesan diproses penyedia AI yang dipilih>.
<Bila relevan: 1-2 kalimat UU PDP + "Ini bukan nasihat hukum." + tawaran balas "PDP">

🔴 BERBAHAYA (A)
1. <temuan dalam bahasa awam + kenapa penting, maks. 2 kalimat>

🟡 PERLU PERHATIAN (B)
3. <idem>
<Temuan sisa: satu kalimat "N lagi: <inti>. Balas "detail".">

🟢 SUDAH AMAN (C)
- <satu baris per butir, singkat>

TAWARAN (belum ada yang diubah)
- Balas "rapikan": <apa yang berubah, dari -> ke>. <Efek yang berhenti bekerja>. <Cara batal>.
- Balas "ubah N": <dari -> ke>. <Efek yang berhenti bekerja>. <Cara batal>.
- <Butir berisiko: tidak ada tombol; tawarkan "bantu butir N">
- Balas "tampilkan perintahnya" bila ingin menjalankan sendiri.
```

Aturan isi:
- Penilaian: ada butir berbahaya → "perlu dibereskan"; hanya perhatian → "cukup baik, ada yang
  bisa dirapikan"; tidak ada keduanya → "baik". Jangan mengarang skor angka.
- Nomor butir berlanjut dari BERBAHAYA ke PERLU PERHATIAN agar bisa dirujuk di tawaran.
- Emoji hanya tiga di atas (satu per judul bagian). Tanpa tabel, blok kode, atau tebal berlebihan.
- Terlalu panjang? Kurangi dulu bagian SUDAH AMAN (jadi satu kalimat), lalu rinci hanya 3 teratas
  per kelompok; sisanya lewat "detail". Jangan memotong tawaran tindakan.
- "Data Anda" memakai kata "folder pengaturan OpenClaw Anda" bila perlu menyebut lokasi.
- Tawaran "rapikan" hanya muncul bila audit melaporkan berkas/folder pengaturan bisa dibaca akun
  lain (dan bukan di Windows; lihat `references/openclaw.md` §10). Butir yang tidak punya
  perbaikan pengaturan langsung (model lokal, kunci layar, enkripsi disk) ditulis sebagai saran
  manual, bukan tombol.
- Efek yang berhenti bekerja diambil dari `references/dampak-perubahan.md`, ditulis ulang awam
  dan disesuaikan jawaban "dipakai untuk apa". Tanpa baris itu, tawaran tidak boleh dikirim.

## 2. Contoh lengkap (fiktif, hanya bentuk; bukan hasil audit pengguna mana pun)

Pemilik toko online, bot melayani pelanggan lewat Telegram. 2.116 karakter.

```
HASIL CEK PRIVASI BOT ANDA
Penilaian: perlu dibereskan. 2 berbahaya, 3 perlu perhatian, 3 sudah aman. Belum ada yang saya ubah.
Data Anda: obrolan dan ingatan bot tersimpan di komputer Anda sendiri, bukan di server Komunitech. Isi pesan diproses penyedia AI yang Anda pilih.
Karena bot melayani pelanggan, data mereka masuk aturan UU PDP (UU 27/2022). Balas "PDP" untuk ringkasannya. Ini bukan nasihat hukum.

🔴 BERBAHAYA (2)
1. Bot boleh menjalankan perintah di komputer tanpa bertanya dulu, padahal ia juga melayani pelanggan. Pesan jebakan dari orang asing bisa membuat bot menurut.
2. Layanan inti bot (bagian yang menerima pesan dan menjalankan bot) belum dikunci dengan kunci rahasia. Aman selama hanya dibuka dari komputer ini, berbahaya bila suatu saat dibuka lewat internet.

🟡 PERLU PERHATIAN (3)
3. Berkas pengaturan bot Anda bisa dibaca pengguna lain di komputer ini. Di dalamnya ada kunci rahasia penyambung bot ke Telegram.
4. Folder pengaturan OpenClaw Anda juga bisa dibaca pengguna lain. Isinya percakapan dan ingatan bot.
5. Satu lagi: semua orang yang chat pribadi ke bot berbagi satu ingatan. Balas "detail" untuk penjelasannya.

🟢 SUDAH AMAN (3)
- Statistik pemakaian anonim mati.
- Pengirim baru harus disetujui dulu sebelum bisa chat pribadi.
- Cek versi harian tidak membawa isi pesan.

TAWARAN (belum ada yang diubah)
- Balas "rapikan": saya kunci berkas dan folder pengaturan (butir 3 dan 4) dari "bisa dibaca pengguna lain" menjadi "hanya akun Anda". Yang berubah hanya izin, isinya tidak. Yang berhenti bekerja: tidak ada fitur bot, hanya akun lain di komputer ini yang tak bisa membacanya lagi. Bisa dikembalikan: balas "kembalikan".
- Balas "ubah 1": izin menjalankan perintah dari "langsung jalan" menjadi "minta persetujuan dulu". Yang berhenti bekerja: jadwal otomatis yang menjalankan program akan ditolak otomatis (bila Anda memakainya). Bisa dikembalikan ke semula.
- Butir 2 tidak saya ubah dari chat karena perlu mulai ulang layanan inti bot dan kunci baru di aplikasi Anda. Balas "bantu butir 2" bila mau dipandu.
- Balas "tampilkan perintahnya" bila ingin menjalankan sendiri.
```

Catatan: contoh di atas sengaja tidak memuat jalur, angka izin, perintah, atau nama kunci
pengaturan. Bila hasil sungguhan lebih panjang, ikuti aturan pemangkasan di bagian 1.

## 3. Kamus istilah (jelaskan SEKALI saat pertama muncul, setelah itu pakai kata awamnya)

| Istilah teknis | Kata awam di chat | Penjelasan satu kalimat |
|---|---|---|
| exec / perintah komputer | izin bot menjalankan perintah di komputer | Bot bisa membuka, mengubah, atau menghapus berkas dan menjalankan program atas nama Anda. |
| sandbox | ruang terbatas | Bot dikurung di area terpisah sehingga tidak menyentuh seluruh komputer. |
| token / API key / secret | kunci rahasia | Semacam kata sandi yang dipakai bot untuk masuk ke layanan lain; jangan dibagikan. |
| gateway | layanan inti bot | Bagian yang menerima pesan dan menjalankan bot di komputer. |
| Control UI | halaman kontrol bot | Halaman tempat Anda mengatur dan menyetujui tindakan bot. |
| security audit | pemeriksaan keamanan | Pemeriksaan baca-saja; tidak mengubah apa pun. |
| config / konfigurasi | pengaturan | |
| dmPolicy / allowFrom | siapa yang boleh chat pribadi ke bot | |
| groupPolicy / groupAllowFrom | siapa di grup yang boleh menyuruh bot | |
| groups | grup mana yang diproses bot | |
| pairing | persetujuan pengirim baru | Pengirim baru harus Anda setujui dulu. |
| dmScope | ingatan bersama atau terpisah | Apakah semua pengirim berbagi satu ingatan bot. |
| tools.profile | daftar kemampuan bot | |
| telemetri | statistik pemakaian | |
| perms / chmod | izin berkas | Siapa yang boleh membaca berkas di komputer. |

## 4. Kata balasan pengguna dan artinya

| Balasan | Arti | Catatan keamanan |
|---|---|---|
| rapikan | Kunci izin berkas pengaturan + folder pengaturan seperti di tawaran | Hanya sah bila tawaran sudah ditampilkan di pesan sebelumnya. Tidak mencakup `config set`, `--fix`, atau butir lain. |
| kembalikan | Pulihkan izin ke kondisi tercatat sebelum "rapikan" | Pakai izin yang dicatat agent, bukan tebakan. |
| ubah N | Jalankan perbaikan pengaturan butir N | Hanya butir yang tawarannya lengkap (dari-ke, efek, cara batal). Satu persetujuan = satu butir. |
| bantu butir N | Pandu langkah butir berisiko (kunci baru, mulai ulang, Docker) | Tidak ada perubahan sampai pengguna menjawab "ya" setelah risikonya dijelaskan. |
| tampilkan perintahnya | Lampirkan perintah teknis untuk butir yang diminta | Satu-satunya saat perintah muncul di chat. |
| detail | Kirim daftar temuan lengkap | Pecah per bagian, tiap pesan ≤ 3.000 karakter. |
| PDP | Kirim ringkasan UU PDP dari `references/uu-pdp.md` | Sertakan "bukan nasihat hukum". |
| "ya semua" | Setuju untuk semua tawaran | Hanya sah setelah pengguna melihat daftar lengkapnya; tetap dikerjakan satu per satu. |

## 5. Balasan lanjutan (kerangka)

**Setelah "rapikan"** (laporkan hanya yang benar-benar terverifikasi):
```
Sudah saya kunci, dari "bisa dibaca pengguna lain" menjadi "hanya akun Anda":
- berkas pengaturan bot Anda
- folder pengaturan OpenClaw Anda
Isi berkas tidak saya buka atau ubah. Saya cek ulang dengan pemeriksaan keamanan: <temuan izin berkas sudah hilang | hasil sebenarnya>.
Mau dikembalikan? Balas "kembalikan". Butir lain masih menunggu keputusan Anda: balas "ubah 1" atau "tampilkan perintahnya".
```
Bila pemeriksaan ulang masih menunjukkan temuan izin, tulis jujur "belum berhasil" dan sebabnya
(mis. berkas dimiliki akun lain); jangan memakai `sudo`.

**Setelah "tampilkan perintahnya"** (contoh untuk butir izin berkas; di sini boleh ada blok kode):
```
Perintah untuk butir 3 dan 4. Jalankan di Terminal komputer tempat OpenClaw terpasang. Ganti isian
[isian: folder pengaturan OpenClaw Anda] dengan alamat folder itu (biasanya folder ".openclaw" di folder
rumah Anda):

chmod 600 "[isian: folder pengaturan OpenClaw Anda]/openclaw.json"
chmod 700 "[isian: folder pengaturan OpenClaw Anda]"

Untuk mengembalikan, pakai izin lama yang saya catat: <izin lama berkas> untuk berkas, <izin lama folder> untuk folder.
```

## 6. Yang tidak boleh muncul di balasan chat (periksa sebelum kirim)
Jalur berkas/folder apa pun (termasuk jalur komputer uji), angka izin seperti 644 atau 600,
perintah `chmod` atau `openclaw ...` (kecuali setelah "tampilkan perintahnya"), nama kunci
pengaturan seperti `tools.exec.mode`, kode temuan audit, nama berkas `openclaw.json`, isi kunci
rahasia/token, tabel, JSON mentah, lebih dari tiga emoji.
