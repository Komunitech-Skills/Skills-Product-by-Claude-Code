# Riwayat perubahan — pantau-pasar-kripto

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Riwayat versi
- **Catatan revisi 1.0.11 (2026-10-15)** — tindak lanjut verifikasi rujukan aturan (dicek
  15 Oktober 2026 ke pajak.go.id & ojk.go.id): (1) **pajak kripto dibatasi tanggal**: tarif
  PMK 50/2025 (0,21% / 1% atas nilai jual) kini hanya dipakai `scripts/hitung_pl_jurnal.py` untuk
  transaksi jual **sejak 1 Agustus 2025**; jual sebelum tanggal itu (aturan lama PMK
  68/PMK.03/2022, digantikan PMK 50/2025) tidak diestimasi dan didaftar di field baru
  `jual_sebelum_1_agustus_2025` + `catatan_aturan_lama` — tarif lama tidak disebut tanpa tanggal;
  hitungan P/L FIFO tidak berubah; tes regresi 130–132 ditambahkan; (2) README: perkiraan PPh
  final menyebut PMK 50/2025 + tanggal berlaku, transaksi beli tidak kena PPh, dan arahan ke
  konsultan pajak/DJP; status regulasi menyebut masa peralihan Bappebti → OJK berakhir
  **20 Januari 2026**; (3) `references/regulasi.md`: catatan cek ulang 2026-10-15 di bagian atas
  (akhir transisi 20 Januari 2026), batas tanggal PMK 50/2025 vs PMK 68/PMK.03/2022 dengan sumber
  artikel DJP, dan tautan halaman peraturan PMK 50/2025 di pajak.go.id; SKILL.md langkah D.4
  ikut diperbarui.
- **Catatan revisi 1.0.10 (2026-10-05)** — dari uji ulang ke-3 paket (pesan gabungan berita +
  riset + alert sering tidak terjawab dalam batas waktu): (1) instruksi skill dipangkas dari 370
  ke ±190 baris, rincian dipindah ke `references/` dan hanya dibaca bila perlu; ada "anggaran
  kerja" per pesan (±6 pengambilan web, ±20 langkah) dan urutan jawab tetap: harga & status
  ambang → berita → riset koin → draf jadwal; (2) berita kini **satu perintah**
  `scripts/ambil_berita.py` (RSS publik CoinDesk/Cointelegraph/The Block/Decrypt, tanpa API key):
  langsung keluar daftar final bertautan artikel asli, tanpa judul prediksi harga;
  (3) riset koin **satu perintah** `scripts/cek_koin.py`: harga, pasokan, tautan resmi, daftar
  bursa, dan jumlah pair Indodax yang **dihitung** (bukan dikira); (4) draf jadwal memakai folder
  kerja standar `$HOME/.openclaw/workspace`, tidak lagi diisi path tebakan; (5) `PANTAU.md` &
  `konfigurasi.json` baru disimpan setelah Anda menjawab "ya", dan lokasinya disebut — pratinjau
  harga bisa jalan tanpa file; (6) kalimat penolakan auto-trade/sinyal ditulis baku (key tanpa
  izin tarik dana, status `bot-trading-kripto`, limit/stop order bawaan bursa, POJK 27/2024, cek
  PAKD di OJK) juga di aturan paket VIP.
- **Catatan revisi 1.0.9 (2026-10-05)** — dari uji ulang ke-2 paket: (1) saat alert dipasang,
  tampilan harga memakai `--pratinjau` sehingga notifikasi pertama tidak lagi diredam;
  (2) prediksi harga/peringkat/"flippening" dari artikel tidak ditampilkan sama sekali;
  (3) jadwal: draf ditampilkan dulu, baru dipasang setelah Anda menjawab "ya" atas draf itu;
  (4) berita selalu dirapikan `rapikan_berita.py`; (5) draf jadwal memakai lokasi standar
  `~/.openclaw/skills/...`; (6) penolakan auto-trade menyebut key tanpa izin tarik dana,
  status `bot-trading-kripto`, dan limit/stop order bawaan bursa.
- **Catatan revisi 1.0.8 (2026-10-03)** — dari uji ulang paket: (1) pemasangan jadwal kini
  pasti — AI mencoba **sekali**; bila gagal, langsung memberi draf perintah jadwal siap tempel
  (`scripts/draf_jadwal.py`) tanpa mencoba ulang atau mencari program di komputer Anda;
  (2) berita dirapikan `scripts/rapikan_berita.py`: hanya judul dengan tautan artikel asli,
  yang tanpa tautan dibuang atau ditandai "[tanpa tautan]" di akhir.
- **Catatan revisi 1.0.7 (2026-10-03)** — dari uji gabungan paket solusi VIP kripto-keuangan:
  (1) saat alert dipasang, script menampilkan status **setiap** ambang — "SUDAH TERLEWATI"
  bila harga sekarang sudah melewati ambang Anda (mis. BTC sudah di bawah ambang bawah), atau
  "belum terlewati" + jaraknya; (2) angka ambang **hanya dari Anda** — AI tidak lagi memakai
  default ±5% atau mengarang ambang; koin yang hanya untuk ringkasan pagi boleh tanpa ambang;
  (3) tautan berita redirect Google News diganti URL artikel asli, atau ditandai "tautan asli
  belum didapat"; (4) bila jadwal belum bisa dipasang, AI cek sekali lalu memberi draf jadwal —
  tidak menyelidiki disk/config/gateway sendiri.
- **Catatan revisi 1.0.6 (2026-10-01)** — dari uji ulang OpenClaw: (1) **perbaikan pajak**:
  estimasi PPh final kini **hanya dihitung script jurnal** dan hanya atas **nilai transaksi
  JUAL** sesuai PMK 50/2025 (0,21% di exchange dalam negeri berizin OJK, 1% di exchange luar
  negeri; beli tidak kena PPh; PPN atas penyerahan kripto tidak dipungut sejak 1 Agustus 2025).
  Versi 1.0.5 sempat menghitung atas beli + jual (Rp48.951; benar Rp18.585 pada kasus uji) dan
  menebak pajak sudah termasuk fee — kini AI dilarang menebak dan meminta Anda mengecek kolom
  pajak di riwayat transaksi exchange; (2) setiap berita/fakta riset wajib ber-URL lengkap ke
  artikel/halaman yang dikutip (bukan beranda atau "via Google News"); (3) jam data dihitung
  ke WIB lewat script baru `scripts/jam_wib.py` (sebelumnya jam UTC pernah tertulis sebagai
  WIB, selisih 7 jam); (4) data alokasi token hanya dari sumber resmi proyek dengan tanggal
  sumber, atau dinyatakan "belum bisa dicek".
- **Catatan revisi 1.0.5 (2026-10-01)** — dari uji OpenClaw solusi VIP kripto-keuangan:
  (1) tabel harga memakai **satu mata uang acuan** untuk persen 24 jam (tidak lagi campur
  Rupiah/USD) dan selalu menyebut sumber + jam data; (2) hasil riset koin untuk chat dibuat
  ringkas (±1.500–2.500 karakter, rincian lengkap bila diminta) dan setiap sumber berupa
  tautan lengkap; (3) jurnal trading kini **menandai biaya transaksi yang janggal** (di atas
  1% nilai transaksi atau jauh berbeda dari transaksi lain, mis. fee jual 0,4% vs 0,2%) tanpa
  mengubah hitungan untung/rugi; (4) saat menolak permintaan sinyal, AI menyebut singkat bahwa
  perdagangan kripto diawasi OJK (POJK 27/2024), cara cek legalitas platform, dan kanal lapor
  Satgas PASTI / Kontak OJK 157.
