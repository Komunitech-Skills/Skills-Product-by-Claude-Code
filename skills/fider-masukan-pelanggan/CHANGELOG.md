# Riwayat perubahan — fider-masukan-pelanggan

Catatan teknis per versi.

## Catatan revisi 1.0.9 (2026-10-13)
- Balasan ke pengguna tidak lagi memakai kata teknis internal (token, gateway, nama perintah atau berkas konfigurasi); diganti bahasa sehari-hari seperti "kunci akses", "bot", "jadwal", "pengaturan". Perintah teknis hanya ditampilkan bila pengguna memintanya.
- Rujukan ke panduan Fider di bagian batasan disederhanakan (nama berkas disebut hanya bila pengguna perlu membukanya). Konstanta versi di script disamakan dengan katalog.

## Catatan revisi 1.0.8 (2026-10-12)
- Revisi dari uji ulang OpenClaw: script mencari dan membaca kunci API sendiri (urutan: `--kunci-file`, variabel lingkungan, lalu berkas simpanan), sehingga agent tidak perlu membuka berkas atau variabel apa pun dan tidak meminta `simpan-kunci` lebih dulu.
- Bila belum ada kunci, agent tetap memberi pratinjau usulan (judul singkat netral, data pribadi disamarkan, butir kembar digabung) dengan tanda jelas bahwa itu pratinjau awal yang belum dibandingkan dengan usulan di papan.

## Catatan revisi 1.0.7 (2026-10-02)
- Perbaikan kecil kalimat aturan "Pos publik tanpa data pribadi" di SKILL.md (rincian di riwayat git).

## Catatan revisi 1.0.6 (2026-10-02)
- Ditambah larangan di SKILL.md: bila pengguna menempel kunci/token/sandi di chat, agent tidak boleh menulis ulang satu karakter pun darinya; cukup menyebut "kunci yang Anda tempel".

## Catatan revisi 1.0.5 (2026-10-02)
- Revisi dari uji OpenClaw: nama orang yang ditulis dengan sapaan (Pak/Bu/Kak/Mas/Mbak/Bang dst. diikuti nama) kini ikut disamarkan, selain nomor HP, telepon, dan email, di tulisan baru, kolom sumber, catatan, komentar, dan saat menampilkan pos lama. Bagian yang disamarkan ditandai di pratinjau.
- Judul usulan ditulis singkat dan netral; pelanggan disebut "seorang pelanggan". Alasan status "Ditolak" wajib berasal dari pemilik: agent tidak boleh mengarang alasan, dan bila belum ada ia bertanya dulu. 45 uji regresi.

## Catatan revisi 1.0.4 (2026-10-01)
- SKILL.md kini menyebut bahwa script ada di subfolder `scripts/` di folder skill, dan agent tidak boleh mencari file ke seluruh disk (mis. `find /`). Logika tidak berubah.

## Catatan revisi 1.0.3 (2026-09-30)
- Ditambah baris "Aturan kerja" di SKILL.md: tidak memasang paket/aplikasi sendiri, tidak membuka file di luar yang diberikan pengguna dan isi folder skill, dan menyebut lokasi file baru. Logika tidak berubah.

## Catatan revisi 1.0.2 (2026-09-29)
- Alamat Fider yang memuat spasi atau port rusak ditolak dengan pesan jelas; batas jumlah pelanggan diperkenalkan.
- Penyamaran nomor diperluas: deretan angka yang dipisah spasi, titik, strip, kurung, atau garis panjang dikenali sebagai nomor HP/telepon, juga di kolom sumber dan saat menampilkan pos lama. Singkatan opsi baris perintah ditolak (`allow_abbrev=False`). 43 uji regresi.

## Catatan revisi 1.0.1 (2026-09-29)
- Revisi dari uji independen pertama: HTTP polos hanya diizinkan untuk localhost dan alamat IP privat sungguhan (nama host seperti `10.contoh.com` dianggap internet dan wajib HTTPS).
- Deteksi usulan kembar kini membandingkan kata penentu dan sinonim (GoPay tidak sama dengan QRIS, email tidak sama dengan WA); hasilnya hanya petunjuk, pemilik yang memutuskan. Pesan galat Fider diterjemahkan ke Bahasa Indonesia; telepon rumah/kantor ikut disamarkan; uraian dibatasi 5.000 huruf; `simpan-kunci` memberi pesan jelas bila dijalankan lewat pipa. 37 uji regresi.

## Catatan revisi 1.0.0 (2026-09-29)
- Rilis awal (uji internal): mengelola papan masukan Fider milik pengguna sendiri lewat REST API resmi (cek, daftar, cari, ringkasan mingguan, draf balasan, impor catatan WhatsApp/ulasan, tag, gabung usulan kembar, status, komentar). Perintah yang menulis ke Fider hanya menampilkan pratinjau kecuali ditambah `--ya`; kunci API tidak pernah dicetak. Diuji dengan Fider v0.38.0 asli.
