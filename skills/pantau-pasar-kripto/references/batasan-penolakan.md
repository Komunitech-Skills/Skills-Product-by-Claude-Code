# Batasan, penolakan & penanganan error (dipindah dari SKILL.md v1.0.9)

**Baca file ini hanya bila:** pengguna bersikeras setelah ditolak (minta penjelasan lebih
panjang), menempel kredensial, atau menanyakan privasi data / perubahan regulasi. Template
penolakan singkat ada di SKILL.md "Batas tegas".

## 1. Mengapa tidak ada auto-trading / API key exchange (bila pengguna bersikeras)
1. Berita/web yang dibaca agent bisa disusupi instruksi tersembunyi (*prompt injection*) yang
   mencoba memicu transaksi.
2. Kesalahan model AI dalam auto-trading = kerugian uang nyata yang tidak bisa dibatalkan.
3. Kredensial exchange di mesin yang juga membaca konten luar = risiko keamanan.
Alternatif aman: limit/stop order **bawaan aplikasi bursa resmi**, dipasang & dipantau member
sendiri. Bot trading otomatis ada di skill terpisah `bot-trading-kripto` (statusnya ditunda;
belum termasuk paket ini).

## 2. Penolakan sinyal / auto-trade / broadcast
- Selalu memuat rujukan singkat: perdagangan aset kripto diawasi **OJK** (POJK 27/2024, diubah
  POJK 23/2025); cek platform di daftar **PAKD** berizin/terdaftar OJK (lihat `regulasi.md`);
  grup "sinyal pasti cuan" bisa dilaporkan ke **Satgas PASTI** / Kontak OJK 157. Diakhiri
  disclaimer baku.
- Jangan menyebut nama sistem/agent/model (mis. "openclaw") dalam kalimat ke member.
- Modal dari cicilan/utang/kebutuhan pokok → arahkan ke skill `atur-keuangan-pribadi` (bila
  terpasang) untuk menata cicilan & dana darurat dulu.
- Laporan untuk grup/pelanggan/broadcast → di luar cakupan; notifikasi hanya untuk member
  sendiri (draf boleh, dikirim sendiri oleh member).
- Clone suara/wajah untuk promosi koin → ditolak di skill mana pun.

## 3. Kredensial & jadwal
JANGAN mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`,
`printenv`), file konfigurasi (`openclaw.json`, `.env`), atau riwayat. Kanal Telegram diatur
lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. **Dilarang:** `find`, `locate`,
`which`, `ls` di luar folder skill/mencari CLI, `gateway config.get`, `openclaw doctor`,
menanyakan isi `openclaw.json`/status kanal ke tool atau agent lain, mengubah config/gateway/
kanal, meminta token bot ke chat. API key/secret/seed phrase yang ditempel: tidak diulang
(sebagian maupun utuh), tidak disimpan; sarankan revoke & buat ulang tanpa izin tarik dana.

## 4. Regulasi & pajak
- `regulasi.md` = fakta terverifikasi PER TANGGAL referensinya. Kepastian hukum terkini →
  ojk.go.id / peraturan.bpk.go.id / konsultan hukum.
- SPT/kewajiban pajak tahunan → konsultan pajak/DJP. Estimasi PPh final per transaksi jual
  hanya lewat `hitung_pl_jurnal.py` (SKILL.md Langkah D).
- Jurnal tanpa Python: jangan menghitung P/L banyak baris secara manual; tawarkan bantuan
  memasang Python, atau hitung 1–2 baris sederhana sambil menyebut "belum diverifikasi script".

## 5. Data pribadi
`kripto/PANTAU.md`, `konfigurasi.json`, `state.json`, `JURNAL.csv` berisi data finansial
pribadi member, tersimpan lokal di komputer member. Skill tidak mengirim isinya ke server mana
pun selain penyedia model AI (sama seperti percakapan biasa) dan API harga/RSS publik (yang
hanya menerima kode koin, bukan data member).
