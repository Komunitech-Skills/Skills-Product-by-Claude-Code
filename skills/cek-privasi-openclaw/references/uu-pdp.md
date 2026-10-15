# Ringkasan UU PDP untuk Pengguna OpenClaw (bahasa awam)

**Dasar hukum (dicek 15 Oktober 2026):**
- **Undang-Undang Nomor 27 Tahun 2022** tentang Pelindungan Data Pribadi (UU PDP), diundangkan
  17 Oktober 2022. Masa penyesuaian paling lama 2 tahun (Pasal 74) berakhir Oktober 2024, jadi
  kewajibannya **sudah berlaku penuh sejak Oktober 2024**.
- **Peraturan Pemerintah Nomor 33 Tahun 2026** tentang Peraturan Pelaksanaan UU 27/2022:
  diundangkan 16 Juli 2026, **mulai berlaku 16 Januari 2027** (Pasal 225). PP ini menambah
  aturan teknis/operasional; ia **tidak menunda** kewajiban UU PDP yang sudah berlaku sejak
  Oktober 2024. Isi rinci PP belum diringkas di skill ini — untuk kewajiban teknis dari PP,
  arahkan ke salinan resminya atau konsultan hukum/DPO.
- Sumber: naskah UU 27/2022 (JDIH Kemkomdigi) dan salinan resmi PP 33/2026 (peraturan.go.id).
  Ringkasan umum, bukan nasihat hukum. Jangan mengutip nomor pasal lain yang tidak tercantum di
  file ini tanpa cek ulang ke naskah resmi.

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
5. **Pemberitahuan kalau terjadi kebocoran data** (UU 27/2022 Pasal 46 ayat (1)): pengendali
   data wajib memberi tahu **secara tertulis paling lambat 72 jam (3×24 jam)** kepada pemilik
   data (orang yang datanya bocor) dan kepada lembaga pelindungan data pribadi. Tenggatnya
   pendek — kalau ada dugaan kebocoran, segera libatkan konsultan hukum/DPO.

**Sanksi (sekadar pengingat):** pelanggaran kewajiban pengendali data dapat dikenai sanksi
administratif UU PDP (Pasal 57): peringatan tertulis, penghentian sementara pemrosesan,
penghapusan/pemusnahan data, sampai denda administratif paling tinggi 2% dari pendapatan atau
penerimaan tahunan terkait pelanggaran.

## Data kesehatan = kategori khusus (Pasal 4 UU PDP)
UU PDP membedakan data pribadi **umum** (nama, alamat, nomor HP) dan data pribadi **spesifik**
(Pasal 4), yang secara umum mencakup: data kesehatan, data biometrik, data genetika, catatan
kejahatan, data keuangan pribadi, dan data anak. Data pribadi spesifik mendapat perlindungan
lebih ketat. **Kalau OpenClaw pengguna memproses data pasien/kesehatan**, perlakukan sebagai
kategori khusus ini — jangan disamakan dengan data pelanggan toko biasa. Skill ini tetap
**tidak** memberi kepastian hukum untuk kasus kesehatan; arahkan ke tenaga profesional/legal.

## Yang bisa langsung diterapkan di OpenClaw (rekomendasi praktis, bukan kewajiban hukum pasti)
- **Beri tahu identitas asisten virtual** di pesan pertama ke pelanggan (mis. "Ini asisten
  virtual toko kami, balasan bisa dibantu AI"). Jujur, tidak menyamar sebagai manusia.
- **Beri tahu anggota grup** kalau bot ikut membaca/meringkas percakapan grup, terutama grup
  yang berisi data sensitif (keluarga, pasien, HR internal).
- **Simpan data pelanggan seperlunya** di file lokal (mis. daftar piutang), bukan lebih dari
  yang dipakai untuk pekerjaan itu.
- **Kalau ada permintaan pelanggan untuk dihapus datanya**, pastikan pemilik usaha tahu di mana
  data itu tersimpan secara lokal (folder workspace OpenClaw), dan bisa dihapus lewat
  `openclaw memory forget` (lihat `references/openclaw.md` §7) atau menghapus filenya langsung.
- **Langkah manual tambahan untuk data sensitif** (di luar config OpenClaw, tapi tetap relevan
  untuk kepatuhan praktis): aktifkan enkripsi disk penuh (FileVault di Mac, BitLocker di
  Windows), kunci layar otomatis, dan backup terenkripsi untuk komputer yang menyimpan data
  pasien/pelanggan sensitif.

## Permintaan menyadap/membaca chat orang lain (ditolak)
Membaca atau menyadap chat/perangkat orang lain tanpa hak dapat melanggar **UU ITE — UU 11/2008
jo. UU 19/2016 jo. UU 1/2024, Pasal 31** (larangan intersepsi/penyadapan), selain UU PDP.
Karena itu skill menolak permintaan semacam ini dan menawarkan alternatif sah (kebijakan
tertulis pemakaian perangkat/akun kerja yang disetujui karyawan, akun WA Business kantor,
konsultasi ke HR/konsultan hukum).

## Disclaimer
Ringkasan ini **bukan nasihat hukum**. Untuk kepatuhan penuh (terutama usaha yang memproses
banyak data pelanggan atau data sensitif), konsultasikan ke konsultan hukum/Data Protection
Officer. Skill ini hanya membantu pengaturan teknis dasar di OpenClaw, bukan kepatuhan hukum
menyeluruh.
