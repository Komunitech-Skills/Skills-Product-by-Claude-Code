# Ringkasan UU PDP untuk Pengguna OpenClaw (bahasa awam)

**Dasar hukum:** Undang-Undang Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP),
**berlaku penuh sejak Oktober 2024**. Sumber: hukumonline.com — ringkasan umum, bukan nasihat
hukum. (Peraturan Pemerintah pelaksana lebih lanjut ada, tapi nomor & isinya **belum
diverifikasi** dalam sesi ini — jangan mengutip nomor PP secara pasti tanpa cek ulang.)

Bagian ini dipakai skill `cek-privasi-openclaw` **hanya** untuk mengingatkan, bukan untuk
memberi kepastian hukum. Untuk kasus spesifik (data kesehatan, data anak, insiden kebocoran),
arahkan pengguna ke konsultan hukum/DPO.

## Kapan relevan untuk pengguna OpenClaw
UU PDP relevan begitu OpenClaw milik pengguna **memproses data pelanggan/pihak ketiga** —
misalnya: agen CS yang membaca chat pelanggan, bot yang ikut di grup WhatsApp berisi anggota
lain, atau menyimpan daftar piutang/kontak pelanggan.

## Prinsip dasar (ringkas)
1. **Ada dasar hukum/persetujuan.** Idealnya pelanggan tahu dan setuju datanya diproses
   (termasuk oleh asisten AI/chatbot).
2. **Beri tahu tujuannya.** Pelanggan berhak tahu untuk apa datanya dipakai.
3. **Kumpulkan/simpan seperlunya (minimisasi data).** Jangan menyimpan lebih dari yang perlu
   untuk pekerjaan itu (mis. tidak perlu menyimpan nomor KTP kalau tidak dibutuhkan).
4. **Hak subjek data:** pelanggan berhak mengakses, mengoreksi, menghapus datanya, dan menarik
   persetujuan.
5. **Notifikasi kalau ada kebocoran data**, sesuai jangka waktu yang diatur (ringkasan umum:
   dalam hitungan hari sejak diketahui — cek ketentuan resmi terbaru untuk angka pastinya).

## Yang bisa langsung diterapkan di OpenClaw (rekomendasi praktis, bukan kewajiban hukum pasti)
- **Beri tahu identitas asisten virtual** di pesan pertama ke pelanggan (mis. "Ini asisten
  virtual toko kami, balasan bisa dibantu AI"). Jujur, tidak menyamar sebagai manusia.
- **Beri tahu anggota grup** kalau bot ikut membaca/meringkas percakapan grup, terutama grup
  yang berisi data sensitif (keluarga, pasien, HR internal).
- **Simpan data pelanggan seperlunya** di file lokal (mis. daftar piutang), bukan lebih dari
  yang dipakai untuk pekerjaan itu.
- **Data kesehatan/pasien** perlu perlakuan lebih hati-hati (kategori data sensitif) — skill ini
  **tidak** memberi kepastian hukum untuk kasus kesehatan; arahkan ke tenaga profesional/legal.
- **Kalau ada permintaan pelanggan untuk dihapus datanya**, pastikan pemilik usaha tahu di mana
  data itu tersimpan secara lokal (folder workspace OpenClaw) agar bisa dihapus.

## Disclaimer
Ringkasan ini **bukan nasihat hukum**. Untuk kepatuhan penuh (terutama usaha yang memproses
banyak data pelanggan atau data sensitif), konsultasikan ke konsultan hukum/Data Protection
Officer. Skill ini hanya membantu pengaturan teknis dasar di OpenClaw, bukan kepatuhan hukum
menyeluruh.
