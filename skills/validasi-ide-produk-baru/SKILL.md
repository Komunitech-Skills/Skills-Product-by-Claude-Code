---
name: validasi-ide-produk-baru
description: Mengubah satu kalimat ide produk/menu/layanan baru menjadi hipotesis teruji (siapa pembeli, masalah apa, harga berapa) lalu merancang uji murah 7 hari ala Indonesia (pre-order WA/status, polling story IG, lapak marketplace percobaan, sampel ke 10 pelanggan tetap, titip di warung) dengan kriteria lulus/gagal berbasis angka dan skrip penghitung konversi — supaya UMKM tahu LANJUT, UBAH, atau HENTIKAN sebelum invest modal besar. Gunakan saat pengguna sudah punya SATU ide konkret dan mau tahu apakah layak dijalankan (validate product idea, cheap MVP test, pre-order test, product-market fit UMKM). Untuk MENGGALI ide dari nol → brainstorming-ide-usaha; untuk MENGHITUNG modal/HPP → hitung-hpp; untuk STRATEGI harga jual → harga-jual-marketplace; untuk MENCARI daftar calon pelanggan baru → riset-calon-pelanggan.
---

# Validasi Ide Produk Baru

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Mengubah ide satu kalimat ("saya mau jual kopi susu gula aren kemasan literan") menjadi hipotesis yang bisa diuji, lalu memandu uji pasar **murah dan cepat (≤7 hari)** memakai kanal yang sudah dimiliki UMKM Indonesia (WA, IG, marketplace, warung langganan) — dan menutup dengan keputusan **LANJUT / UBAH / HENTIKAN** berdasarkan angka hasil uji, bukan feeling atau "kayaknya laku".

## Kapan digunakan
- "Saya mau coba jual [produk/menu/jasa baru], tapi belum yakin laku atau enggak. Gimana cara tesnya tanpa modal besar?"
- "Sebelum saya produksi 100 pcs, gimana cara tahu ada yang mau beli dulu?"
- "Saya mau buka jasa laundry sepatu, worth it enggak ya sebelum sewa tempat?"
- "Mau bikin kelas online Canva, cara ngetes minatnya gimana?"
- Sudah menjalankan uji dan punya data (jumlah ditawari, jumlah pre-order) → minta dihitung dan diputuskan lanjut/tidak.

## Kapan TIDAK digunakan
- Belum ada ide sama sekali, masih mau curah gagasan dari nol → `brainstorming-ide-usaha` dulu, baru kembali ke sini setelah dapat 1 ide spesifik.
- Sudah yakin lanjut dan hanya butuh hitung HPP/margin/BEP secara rinci → `hitung-hpp`.
- Sudah yakin lanjut dan hanya butuh strategi harga untuk listing marketplace → `harga-jual-marketplace`.
- Mau mencari daftar calon pelanggan baru di luar kontak/pengikut yang sudah ada (lead generation) → `riset-calon-pelanggan`. Skill ini menguji minat memakai audiens yang **sudah dimiliki** (kontak WA, follower IG, pelanggan tetap, warung langganan), bukan mencari prospek baru.
- Riset pasar mendalam (survei berskala besar, analisis kompetitor terinci, proyeksi finansial multi-tahun) → di luar cakupan; skill ini hanya uji cepat-murah untuk sinyal awal.
- Ide di kategori terlarang (skema piramida/money game, investasi tanpa izin OJK, klaim obat/kesehatan tanpa izin edar BPOM, produk ilegal) → tolak dengan sopan dan jelaskan alasannya, jangan bantu "validasi" ide semacam ini.

## Input
Gali (atau simpulkan dari cerita pengguna) sebelum mulai:

| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Ide dalam satu kalimat (apa yang dijual, ke siapa kira-kira) | Ya | — (tanyakan) |
| Harga rencana per unit/paket (Rupiah, kasar tidak apa-apa) | Ya | — (tanyakan) |
| Kanal yang **sudah dimiliki**: jumlah kontak WA, follower IG, langganan warung/pelanggan tetap | Tidak | Tanyakan singkat — menentukan metode uji mana yang cocok |
| Sudah pernah coba jual ide serupa sebelumnya? | Tidak | Anggap belum |
| Target waktu uji | Tidak | 7 hari |
| Modal/HPP per unit (kalau sudah tahu) | Tidak | Uji tetap jalan tanpa ini; keputusan margin di Langkah 5 dilewati/ditandai perkiraan |

Jika info wajib kurang, tanyakan **sekali** dalam satu pesan berisi daftar pertanyaan singkat bernomor. Jika pengguna ingin cepat, pakai default dan sebutkan asumsinya di akhir.

## Langkah Kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.

### 1. Susun hipotesis dari ide satu kalimat
Ubah ide jadi kalimat hipotesis eksplisit dengan format:

> "Kami percaya **[calon pembeli spesifik]** mau membayar **Rp[harga]** untuk **[produk/jasa]** karena bisa menyelesaikan **[masalah/kebutuhan]**. Kami akan tahu ini benar jika **[jumlah minimal]** dari **[jumlah yang ditawari]** orang benar-benar memesan/membayar dalam **[jangka waktu]**."

Tajamkan tiga hal supaya tidak kabur:
1. **Calon pembeli** — jangan "semua orang", persempit ("ibu-ibu kantoran di kompleks X", "pemilik warung kopi rumahan", "pemilik UMKM yang jualan di Shopee tapi belum punya desain toko").
2. **Masalah/alasan beli** — kenapa mereka mau bayar, bukan sekadar fitur produk.
3. **Harga rencana** — angka pasti, bukan "murah" atau "sesuai pasar".

Jika pengguna belum yakin di salah satu bagian, itu justru sinyal untuk diuji, bukan alasan menunda — tulis sebagai asumsi terbaik lalu lanjut ke uji.

### 2. Pilih metode uji murah sesuai kanal yang dimiliki
Cocokkan dengan tabel di [`references/menu-uji-murah.md`](references/menu-uji-murah.md). Ringkasnya:

| Metode | Cocok kalau | **Pesanan** (masuk hitungan) | **Minat** (dilaporkan terpisah) |
|---|---|---|---|
| **Pre-order via broadcast/status WA** | Punya ≥30 kontak relevan | Sudah transfer/DP ÷ jumlah dikirimi | Balas "mau"/konfirmasi tapi belum bayar |
| **Polling story Instagram** | Punya ≥100 follower aktif | — (polling saja tidak menghasilkan pesanan; DM pemilih "Ya" dengan tawaran PO + DP) | Vote "mau beli" ÷ views |
| **Lapak percobaan di marketplace** (sistem PO) | Sudah ada toko marketplace atau gampang buka | Order di-checkout/dibayar ÷ views listing | Chat tanya harga/cara beli |
| **Sampel ke pelanggan tetap** | Punya ≥10 pelanggan langganan/reguler | Pesan ulang & bayar dalam 7 hari ÷ jumlah diberi sampel | "Iya, mau beli rutin" tanpa pesan |
| **Titip di warung/reseller** | Ada warung/toko langganan yang mau dititipi | Laku terjual ÷ jumlah dititipkan | — |

**ATURAN HITUNG (wajib, tanpa pengecualian):**
- **Pesanan** = tindakan berkomitmen: pre-order yang sudah transfer/DP/bayar, order checkout, barang laku terjual. **Hanya pesanan** yang masuk konversi, pendapatan, margin, dan balik modal.
- **Minat** = vote polling, like, emoji, komentar "mau", chat tanya harga, janji "nanti beli", konfirmasi tanpa bayar. Minat **tidak pernah** dihitung sebagai pesanan, **tidak pernah** dijumlahkan dengan pesanan, dan **tidak pernah** dikalikan harga/margin. Laporkan di baris tersendiri ("52 vote = sinyal minat, belum pesanan").
- Boleh pakai lebih dari satu metode. Pesanan dari beberapa kanal berkomitmen boleh dijumlahkan; kanal yang hanya menghasilkan minat dilaporkan terpisah. Tampilkan juga konversi per kanal. Jika semua kanal hanya menghasilkan minat → hasil **BELUM BISA DINILAI**; sarankan ubah minat jadi PO berbayar dulu.
- Jika pengguna menyebut angka tanpa jelas jenisnya ("yang mau 20 orang"), tanyakan sekali: "sudah transfer/DP atau baru bilang mau?" — bila tidak dijawab, anggap **minat**.

### 3. Tetapkan kriteria lulus/gagal SEBELUM mulai uji
Ini wajib ditentukan dulu, supaya tidak "menggeser target" setelah lihat hasil. Pakai ambang default berikut (heuristik praktis Komunitech, **bukan hukum pasti** — boleh disesuaikan dan sebutkan alasannya kalau diubah):

- **Jumlah minimal ditawari:** ≥20 orang/tampilan, supaya hasil tidak kebetulan (kalau kurang dari 20, tandai hasil sebagai "indikasi awal", bukan kesimpulan).
- **LULUS (lanjut produksi/investasi):** konversi ≥ 15% — misal ≥3 pre-order dari 20 yang ditawari.
- **LULUS BERSYARAT (ubah dulu sebelum lanjut penuh):** konversi 8%–<15% — ada minat tapi belum kuat; biasanya harga, penawaran, atau target pembeli perlu direvisi.
- **GAGAL (hentikan/ganti ide):** konversi < 8%.

Produk harga rendah/impulsif (di bawah ~Rp30rb, dibeli tanpa banyak mikir) boleh naikkan ambang ke 20%/10%; produk harga tinggi/pertimbangan lama (di atas ~Rp300rb) boleh turunkan ke 10%/5% — jelaskan penyesuaian ini ke pengguna, jangan diam-diam ubah tanpa bilang. **Tetapkan SATU set ambang di awal sesuai harga** dan pakai itu saja di seluruh jawaban (jalankan script dengan `--ambang-lulus`/`--ambang-bersyarat` yang sesuai); jangan menampilkan dua klasifikasi dengan ambang berbeda.

Konversi dihitung dari **pesanan** (lihat Aturan Hitung di Langkah 2), bukan dari minat.

### 4. Siapkan pesan & form pencatatan
Pakai template siap pakai di [`templates/pesan-uji-murah.md`](templates/pesan-uji-murah.md) (broadcast WA, caption status/story, caption polling IG, deskripsi listing PO marketplace, pitch titip warung) — sudah dalam bahasa Indonesia sehari-hari, tinggal isi kurung siku `[...]`.

Untuk mencatat hasil, pakai tabel di [`templates/form-pencatatan.md`](templates/form-pencatatan.md): tanggal, kanal, jumlah ditawari/dilihat, jumlah pre-order/beli, alasan yang tidak beli (kalau sempat ditanya — ini bahan revisi kalau LULUS BERSYARAT).

### 5. Jalankan uji 7 hari, lalu hitung hasil
Setelah masa uji selesai, **angka konversi, margin, dan untung/rugi wajib dihitung lewat script** `scripts/hitung_validasi.py` (Python standar, tanpa instalasi; Windows: `python` atau `py`) — jangan dihitung di kepala:

```
python3 scripts/hitung_validasi.py --ditawari 20 --preorder 4 --minat 6 --harga 25000 --hpp 12000 --biaya-uji 50000
```
`--preorder` = pesanan berkomitmen saja (isi 0 bila belum ada); `--minat` (opsional) = vote/like/komentar — dilaporkan terpisah dan tidak ikut hitungan uang.

Untuk beberapa kanal sekaligus, pakai file JSON mode `kanal` (pesanan & minat dipisah otomatis):
```json
{"harga": 18000, "hpp": 9500, "biaya_uji": 60000,
 "kanal": [{"nama": "Broadcast WA", "ditawari": 45, "preorder": 4},
           {"nama": "Polling IG", "ditawari": 380, "minat": 52}]}
```
Hasil yang benar untuk contoh ini: pesanan 4 dari 45 (8,9%), margin 4 × Rp8.500 = Rp34.000, selisih Rp34.000 − Rp60.000 = **−Rp26.000 (belum balik modal)**. 52 vote = minat, bukan pesanan.

Atau lewat file JSON:
```
python3 scripts/hitung_validasi.py --file data-uji.json
```
Isi `data-uji.json` contoh:
```json
{"ditawari": 20, "preorder": 4, "harga": 25000, "hpp": 12000, "biaya_uji": 50000}
```

Script menghitung (dan menampilkan rumusnya): persentase konversi, klasifikasi LULUS/LULUS BERSYARAT/GAGAL (bisa override ambang dengan `--ambang-lulus` dan `--ambang-bersyarat`), margin per unit (jika `--hpp` diisi), total margin dari pre-order, dan selisih terhadap biaya uji (balik modal atau belum). Jika jumlah ditawari < 20, script menambahkan peringatan sampel kecil.

Field uang (`--harga`, `--hpp`, `--biaya-uji`) menerima format Indonesia: angka polos (`25000`), titik ribuan (`25.000`, `Rp25.000`), atau singkatan (`25rb`, `1jt`, `1,5jt`). Format yang tidak jelas (mis. `25.5`, `1.234,56`) **ditolak** dengan pesan error, bukan ditebak — tulis ulang sesuai salah satu format di atas.

Jika tidak ada Python yang bisa dijalankan, hitung manual dan **tampilkan setiap rumus beserta angkanya** (jangan hanya hasil akhir):
- `konversi (%) = pesanan ÷ ditawari (kanal pesanan) × 100`, bulatkan ke satu desimal
- `margin per unit = harga − HPP`
- `total margin = margin per unit × pesanan` (**pesanan saja**, bukan minat)
- `selisih = total margin − biaya uji` (negatif = belum balik modal)
Bandingkan konversi ke ambang Langkah 3 — skill tetap berguna tanpa script.

### 6. Rekomendasikan keputusan
Berdasarkan klasifikasi hasil:
- **LULUS** → LANJUT: mulai produksi/investasi bertahap (bukan langsung besar-besaran), tawarkan lanjut ke `hitung-hpp` (hitung HPP & BEP rinci) dan `harga-jual-marketplace` (strategi harga jual final).
- **LULUS BERSYARAT** → UBAH: revisi satu variabel dulu (harga, penawaran/kemasan, atau target pembeli — bukan sekaligus semua supaya jelas apa yang berubah), lalu uji ulang 7 hari dengan hipotesis baru.
- **GAGAL** → HENTIKAN ide ini (atau pivot besar): sampaikan dengan sopan bahwa datanya belum mendukung, tawarkan opsi lanjut ke `brainstorming-ide-usaha` untuk mencari ide lain memakai alasan penolakan sebagai bahan.

Selalu tampilkan alasan yang diberikan calon pembeli yang menolak (dari form pencatatan) sebagai bahan keputusan, bukan cuma angka.

## Format Output
1. **Hipotesis** — kalimat lengkap format Langkah 1.
2. **Metode uji terpilih** — nama metode + alasan cocok dengan kanal pengguna.
3. **Kriteria lulus/gagal** — ambang angka yang dipakai + alasan bila disesuaikan dari default.
4. **Pesan/template siap pakai** — hasil isi dari `templates/pesan-uji-murah.md` untuk kanal terpilih.
5. **Form pencatatan kosong** — siap ditempel ke Notes/spreadsheet pengguna.
6. **(Setelah uji selesai) Hasil perhitungan** — output `hitung_validasi.py` atau perhitungan manual + klasifikasi.
7. **Keputusan & langkah berikut** — LANJUT/UBAH/HENTIKAN + skill lanjutan yang relevan.

## Contoh
Lihat `examples/01-kopi-susu-literan.md` (kopi susu gula aren kemasan literan, pre-order via status WA, hasil LULUS) dan `examples/02-jasa-laundry-sepatu.md` (jasa laundry sepatu, polling story IG + titip flyer di warung, hasil LULUS BERSYARAT → revisi harga). Kasus tambahan (kelas online Canva, uji lewat pre-order WA ke grup alumni pelatihan) dibahas ringkas di `references/menu-uji-murah.md`.

## Batasan & Penanganan Error
- **Minat ≠ pesanan.** Vote/like/komentar/"mau" tanpa bayar tidak pernah dihitung sebagai pesanan atau pendapatan. Klaim "sudah balik modal"/"untung" hanya boleh muncul dari hasil script atau rumus eksplisit yang ditampilkan.
- **Bukan riset pasar ilmiah.** Ambang 15%/8% adalah heuristik praktis, bukan angka baku industri — sebutkan ini ke pengguna, terutama untuk keputusan bermodal besar (di atas puluhan juta Rupiah), sarankan tambah metode uji atau konsultasi profesional.
- **Sampel kecil = hasil belum pasti.** Selalu tandai hasil dari <20 orang yang ditawari sebagai "indikasi awal", jangan disebut kesimpulan final.
- **Bukan pengganti kalkulasi biaya rinci.** Kalau pengguna butuh HPP/BEP presisi sebelum memutuskan modal produksi besar, arahkan ke `hitung-hpp` setelah hasil validasi LULUS.
- **Data uji tidak masuk akal** (mis. jumlah pre-order lebih besar dari jumlah ditawari, angka negatif, harga Rp0, atau format harga ambigu seperti `25.5`/`1.234,56`) → script menolak dan menjelaskan bagian mana yang salah; jangan memaksakan perhitungan atau menebak angka.
- **Pesan pre-order harus jujur soal batal/refund** — jangan pernah kirim template pre-order (#1/#4 di `templates/pesan-uji-murah.md`) tanpa mengisi bagian kebijakan batal/refund; ini wajib, bukan opsional. Jika alurnya tidak meminta bayar/DP di depan, ganti kalimat refund dengan "belum perlu bayar sekarang" — dan ingat hasilnya hanya minat sampai ada pembayaran.
- **Tidak mendukung klaim medis/investasi/keuangan berizin khusus** — kalau ide produk menyentuh area ini (mis. suplemen kesehatan, produk investasi), ingatkan kebutuhan izin resmi (BPOM, OJK, dll.) di luar cakupan validasi pasar skill ini.
