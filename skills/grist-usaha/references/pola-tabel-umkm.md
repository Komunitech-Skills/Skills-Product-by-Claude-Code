# Pola tabel siap pakai untuk UMKM (Grist)

Referensi untuk agent saat pengguna minta dibuatkan tabel di Grist. Empat pola di bawah
menjawab kebutuhan paling umum. **Selalu tanyakan dulu** (dalam satu pesan) hal yang tidak
disebutkan pengguna: nama dokumen/tabel yang dipakai, dan apakah field opsional (mis. "Kota",
"Sumber lead") memang diperlukan — pakai default di bawah bila pengguna ingin cepat.

Tipe kolom Grist yang dipakai di sini: `Text`, `Numeric` (angka desimal), `Int` (bilangan
bulat), `Bool` (ya/tidak), `Date`, `DateTime`, `Choice` (pilihan tunggal), `ChoiceList`
(pilihan banyak), `Ref:<Tabel>` (rujukan ke satu baris tabel lain), `RefList:<Tabel>` (rujukan
ke banyak baris). Kolom `id` (angka urut) dibuat otomatis oleh Grist — jangan buat ulang.

Format tiap baris kolom: `colId | Label tampilan | tipe | isFormula | formula/keterangan`.
`isFormula=ya` berarti kolom **rumus** (nilainya dihitung, tidak diisi manual) — lihat
`rumus-umum.md` untuk penjelasan tiap rumus.

## 1. Daftar Pelanggan (`Pelanggan`)

| colId | Label | Tipe | Rumus? | Keterangan |
|---|---|---|---|---|
| Nama | Nama | Text | tidak | wajib |
| Telepon | No. WA/Telepon | Text | tidak | simpan sebagai teks (bukan Numeric) supaya angka 0 di depan tidak hilang |
| TeleponRapi | WA Rapi | Text | **ya** | `rumus_wa_rapi` — lihat rumus-umum.md #1 |
| Kota | Kota | Text | tidak | opsional |
| Sumber | Sumber | Choice | tidak | pilihan: IG, TikTok, Marketplace, Referensi, Walk-in, Lainnya |
| Catatan | Catatan | Text | tidak | opsional |
| TanggalDaftar | Tgl Daftar | Date | tidak | diisi manual (klik tanggal) saat pelanggan pertama dicatat |

**Kapan dipakai:** daftar kontak sederhana yang ingin bisa difilter/disortir bebas, atau
digabung dengan tabel Pesanan lewat kolom `Ref:Pelanggan`. **Kalau kebutuhannya sekaligus
follow-up WA berjenjang (tahap pipeline, draf pesan, pengingat harian)** → arahkan ke skill
`crm-wa` (aplikasi khusus, bukan Grist).

## 2. Pesanan (`Pesanan`)

| colId | Label | Tipe | Rumus? | Keterangan |
|---|---|---|---|---|
| Tanggal | Tanggal | Date | tidak | |
| Pelanggan | Pelanggan | Ref:Pelanggan | tidak | pilih dari tabel Pelanggan (buat tabel Pelanggan dulu) |
| Barang | Barang | Text | tidak | atau `Ref:Stok` bila dipakai bareng tabel Stok Sederhana |
| Jumlah | Jumlah | Int | tidak | |
| HargaSatuan | Harga Satuan | Numeric | tidak | dalam Rupiah, tanpa simbol |
| Diskon | Diskon % | Numeric | tidak | opsional, default 0 |
| Total | Total | Numeric | **ya** | `rumus_total_baris` — rumus-umum.md #2 |
| Status | Status | Choice | tidak | pilihan: Baru, Diproses, Dikirim, Selesai, Batal |
| Catatan | Catatan | Text | tidak | opsional |

**Kapan dipakai:** usaha yang ingin mencatat pesanan dengan tampilan spreadsheet bebas
(kolom bisa ditambah sendiri, bisa dibuat tampilan Kanban per Status). **Kalau kebutuhannya
sekaligus potong stok otomatis dari file pesanan marketplace (Shopee/TikTok/Tokopedia) +
picking list** → arahkan ke skill `buku-stok` (aplikasi khusus dengan logika itu bawaan).

## 3. Stok Sederhana (`Stok`)

| colId | Label | Tipe | Rumus? | Keterangan |
|---|---|---|---|---|
| Nama | Nama Barang | Text | tidak | wajib |
| Kode | Kode/SKU | Text | tidak | opsional |
| Satuan | Satuan | Text | tidak | pcs, kg, box, dll. |
| StokMasuk | Masuk | Int | tidak | total kumulatif — atau pakai tabel `Mutasi` terpisah bila ingin riwayat per transaksi |
| StokKeluar | Keluar | Int | tidak | |
| StokSaatIni | Sisa Stok | Int | **ya** | `rumus_sisa_stok` — rumus-umum.md #3 |
| BatasMinimum | Batas Minimum | Int | tidak | untuk peringatan menipis |
| Status | Status | Text | **ya** | `rumus_status_stok` — rumus-umum.md #4 |

**Kapan dipakai:** stok ringan, dicatat manual, tanpa riwayat transaksi rinci atau HPP. **Kalau
butuh HPP rata-rata, impor otomatis dari file pesanan marketplace, stock opname, dan picking
list** → arahkan ke skill `buku-stok` (dirancang khusus untuk itu, lebih kuat dari tabel Grist
biasa).

## 4. Jadwal Konten (`JadwalKonten`)

| colId | Label | Tipe | Rumus? | Keterangan |
|---|---|---|---|---|
| Tanggal | Tanggal Tayang | Date | tidak | |
| Platform | Platform | ChoiceList | tidak | pilihan: Instagram, TikTok, Facebook, WhatsApp Status, Lainnya (bisa pilih lebih dari satu) |
| Judul | Judul/Topik | Text | tidak | |
| Draf | Draf Isi | Text | tidak | teks caption/naskah |
| StatusProduksi | Status | Choice | tidak | pilihan: Ide, Draf, Siap, Tayang |
| PJ | Penanggung Jawab | Text | tidak | opsional, untuk tim |
| HariMenuju | H- | Int | **ya** | `rumus_hari_menuju` — rumus-umum.md #5 |

**Kapan dipakai:** kalender konten sederhana untuk usaha yang mengelola sosmed sendiri. Bukan
pengganti `caption-sosmed-umkm` (yang menulis isi captionnya) — tabel ini hanya menjadwalkan.

## Cara merancang dari kalimat bebas pengguna (langkah agent)

1. Tangkap **entitas** (benda/orang yang dicatat) dari kalimat pengguna — biasanya cocok
   dengan salah satu dari 4 pola di atas. Kalau ada 2+ entitas yang berkaitan (mis. "pelanggan"
   + "pesanan"), buat 2 tabel dan hubungkan dengan kolom `Ref:`.
2. Untuk tiap entitas, cocokkan field yang disebut pengguna ke kolom di pola terdekat. Field
   yang tidak ada di pola → tambahkan sebagai kolom `Text`/`Numeric`/`Date` biasa sesuai jenis
   datanya (tanyakan bila ambigu, mis. "ukuran" bisa Text "S/M/L" atau Numeric cm).
3. Sebutkan pola mana yang dipakai & kolom yang ditambah/dihapus dari pola dasar, supaya
   pengguna bisa mengoreksi sebelum dibuat.
4. Kalau REST API tersedia (lihat `SKILL.md` bagian Persiapan) → tawarkan `buat-tabel` (dengan
   pratinjau, minta konfirmasi). Kalau tidak → tuliskan daftar kolom+tipe siap tempel ke layar
   Grist ("+ Add Column" untuk tiap baris), dan salin rumus dari `rumus-umum.md` ke kotak formula.
5. Untuk kebutuhan yang **lebih cocok jadi aplikasi khusus** (lihat kolom "Kapan dipakai" tiap
   pola) → arahkan ke `buku-stok`/`crm-wa`, jangan dipaksakan jadi tabel Grist.
