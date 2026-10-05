# Rincian berita & riset koin (dipindah dari SKILL.md v1.0.9)

**Baca file ini hanya bila:** `ambil_berita.py` gagal/kosong dan Anda perlu cara cadangan,
pengguna meminta riset LENGKAP satu koin (bukan ringkasan), atau ada pertanyaan soal format
mata uang/jam. Untuk ringkasan berita & riset singkat biasa, SKILL.md Langkah B–C sudah cukup.

## 1. Berita -- cadangan bila `ambil_berita.py` gagal (exit 3) atau sebuah koin kosong
1. Bila agent punya pencarian web: maks. **2 pencarian** (mis. "<nama koin> news" rentang
   seminggu). Ambil hanya butir yang URL-nya **URL artikel lengkap** (`https://media/.../judul`).
2. Tautan redirect agregator (`news.google.com/rss/articles/...`, `t.co`, `bit.ly`) bukan URL
   sumber; beranda situs bukan URL artikel; halaman ringkasan AI/agregator (mis. coinstats.app/ai)
   bukan sumber.
3. Rapikan dalam SATU perintah, tanpa membuat file:
   ```bash
   echo '[{"judul":"...","url":"https://...","media":"CoinDesk","tanggal":"03-10-2026"}]' \
     | python3 <folder-skill-ini>/scripts/rapikan_berita.py - --tandai
   ```
   (`--tandai` = butir tanpa URL asli ditaruh di akhir berlabel "[tanpa tautan]" dengan
   keterangan "tautan asli belum didapat".) Daftar berita di balasan hanya dari keluaran itu.
4. Tanpa akses web sama sekali: tulis jujur *"Ringkasan berita tidak bisa dibuat -- tidak ada
   akses pencarian web/RSS saat ini. Harga & ambang tetap di bawah."* Jangan menulis berita dari
   ingatan.
5. Berita yang sepi untuk suatu koin: katakan apa adanya ("berita khusus SOL sepi minggu ini").

## 2. Proyeksi = TIDAK ditampilkan sama sekali
Prediksi/target harga, kapitalisasi atau peringkat masa depan ("SOL akan menyalip ETH",
"flippening"), level support/resistance, rekomendasi analis -- dari siapa pun, termasuk
pendiri -- tidak dikutip, tidak diparafrasekan, tidak dipakai sebagai judul. `ambil_berita.py`
sudah membuang judul semacam itu; isi artikel yang memuatnya cukup diberi catatan *"artikel ini
juga memuat proyeksi analis -- tidak ditampilkan di sini"* tanpa angkanya. Ringkas hanya
**peristiwa yang sudah terjadi** (rilis, regulasi, kemitraan, listing/delisting, peretasan,
penutupan jaringan). Angka di ringkasan berita = fakta peristiwa dari artikel itu saja.

Kalender peristiwa (listing/delisting, jadwal regulasi) hanya bila ditemukan dengan sumber
jelas; tidak ditemukan → tidak ditulis.

## 3. Mata uang & jam
- Satu mata uang acuan per tabel: harga Rupiah → persen 24 jam SEMUA koin dari data IDR yang
  sama (CoinGecko `idr_24h_change`); harga USD boleh sebagai keterangan. Sebut di atas tabel:
  sumber, mata uang acuan persen, jam data WIB.
- Jam WIB dihitung, bukan ditebak: pakai `jam_data` dari `cek_ambang.py` / jam di keluaran
  `cek_koin.py`, atau `python3 <folder-skill-ini>/scripts/jam_wib.py <waktu>` (07:10 UTC =
  14:10 WIB). Waktu tanpa zona → jangan diberi label WIB.

## 4. Riset LENGKAP satu koin (hanya bila diminta)
1. Mulai dari `cek_koin.py` (harga, kapitalisasi saat ini, pasokan, situs/whitepaper/explorer,
   bursa di data ticker, pair Indodax yang DIHITUNG). Lalu isi `checklist-riset.md` (tim,
   tokenomics, audit kontrak, likuiditas, status legal) -- HANYA fakta bersumber; yang tidak
   ditemukan ditulis "tidak ditemukan / perlu dicek".
2. **Tokenomics/alokasi token** hanya dari sumber resmi proyek (dokumentasi/blog resmi,
   whitepaper terbaru) dan **wajib menyebut tanggal sumbernya**; Wikipedia/artikel lama bukan
   sumber alokasi. Tidak bisa dibuka → *"alokasi belum bisa saya cek dari sumber resmi terbaru
   -- perlu dicek"*.
3. Status legal Indonesia: `regulasi.md` (fakta per tanggal referensinya). Status terkini →
   arahkan verifikasi ke ojk.go.id / peraturan.bpk.go.id. Ada/tidak ada di bursa ≠ legal.
4. Tanda skema penipuan/pump (janji imbal hasil tetap, tekanan "buru-buru", tim anonim tanpa
   audit, grup yang melarang bertanya kritis) → bagian "Perhatian", netral & edukatif, plus
   kanal lapor Satgas PASTI / Kontak OJK 157 (bukan tuduhan).
5. Format chat: balasan pertama ±1.500–2.500 karakter (5–8 poin fakta + "Perhatian" bila ada +
   disclaimer), tawarkan rincian per bagian checklist. **Setiap poin diberi tautan lengkap**
   (`https://...`), bukan nama domain. Poin tanpa tautan yang bisa dicek: hapus atau "perlu
   dicek". Tanpa kesimpulan "layak dibeli".
