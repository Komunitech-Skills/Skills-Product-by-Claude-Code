# Gelombang Telegram A8 — 2026-10-17 (bot pertama) — bagian 1

Uji ini berlangsung di grup Telegram sungguhan dengan bot pertama `@KTclaude1_bot` (Akun A) di OpenClaw 2026.10.2, pada 17 Okt 2026 pukul 07:47–07:56 UTC, di topik baru 2183–2188. Pesan uji sama persis di sisi TANPA (topik dengan `skills: []`; selama sisi TANPA folder skill juga dipindah keluar HOME bot, dan log tidak menunjukkan akses ke folder skill) dan sisi DENGAN. Setiap sisi mendapat dua giliran: pesan utama, lalu lanjutan "ya". Pesan, lanjutan, dan kunci jawaban diambil dari `scratchpad/openclaw-real/pilot/kandidat-a-cepat.json` (entri buku-stok, versi 1.1.7), dan pra-ceknya ada di `koordinasi/pracek-telegram-akun-a-2026-10-17.md` kelompok 5. Penilai independen (bukan pembuat skill) memakai skala dan kriteria `koordinasi/alat-uji/brief/tester-umum.md` bagian "Penilaian". Dua giliran dinilai sebagai satu jawaban. Angka kunci dihitung ulang dengan Decimal. Jawaban ganda yang identik di transkrip adalah salinan log dan hanya dihitung sekali.

Acuan: **LULUS** bila DENGAN ≥ 8, selisih ≥ 1,5, dan tidak ada salah angka kunci (salah angka kunci = maks 5).

## Skor & verdik

| Skill | Versi | Topik (TANPA/DENGAN) | TANPA | DENGAN | Selisih | Verdik | Pembeda (bahasa awam) |
|---|---|---|---|---|---|---|---|
| buku-stok | 1.1.7 | 2183 / 2184 | 5,0 | 9,0 | +4,0 | **LULUS** | Dengan skill, Anda lebih dulu melihat ringkasan yang akan disimpan, lengkap dengan kode barang dan modal rata-rata Rp34.662. Data baru disimpan setelah Anda membalas "ya", lalu bot menyebut nilai stok Rp3.825.000. Tanpa skill, bot langsung menyimpan tanpa bertanya, mengarang rak penyimpanan dan "sisa 3 pcs" yang tidak pernah Anda sebut, serta menampilkan nama berkas. |

Pembanding uji internal lama (`skills/buku-stok/examples/00-openclaw-sebelum-sesudah.md`, v1.1.5, OpenClaw 2026.9.6 lokal): rata-rata SEBELUM 6,0 → SESUDAH 8,5 (LULUS). Pra-cek konteks Telegram 17 Okt (kelompok 5): 8,5, SIAP KIRIM.

## Rincian

### buku-stok 1.1.7 — TANPA 5,0 → DENGAN 9,0 (+4,0) LULUS

**Angka kunci (dihitung ulang, Decimal):**
- Biaya barang datang: 50 × 34.000 + 25.000 = Rp1.725.000. Ongkir per pcs 25.000 ÷ 50 = Rp500, jadi Rp34.500 per pcs.
- Kaos hitam M: (24 × 35.000 + 1.725.000) ÷ 74 = 2.565.000 ÷ 74 = 34.662,16, dibulatkan menjadi **Rp34.662**. Stok **74**.
- Nilai persediaan: 2.565.000 + 30 × 33.000 + 15 × 18.000 = **Rp3.825.000**.

Sisi DENGAN benar semua: Rp34.500 per pcs, stok 24 → 74, HPP Rp35.000 → Rp34.662, dan nilai persediaan Rp3.825.000. Sisi TANPA menulis stok 74 dan HPP "~Rp34.662" dengan benar, serta total biaya Rp1.725.000. Nilai persediaan tidak disebut.

Kutipan DENGAN:
> Siap, saya catat ya. Ini yang akan saya simpan (belum tersimpan):
> - Barang datang hari ini: Kaos Hitam M +50 @ Rp 34.000 (+ ongkir Rp 25.000, jadi Rp 34.500 per pcs) → stok 24 → 74. Modal rata-rata per barang (HPP) Rp 35.000 → Rp 34.662
> Kode barang saya buatkan dari nama barangnya; kalau mau diganti, tinggal bilang. Simpan? Balas "ya".
>
> (giliran 2) Sudah tersimpan. Stok sekarang: Kaos Hitam M 74, Kaos Putih M 30, Tote Bag Natural 15. Nilai persediaan (total modal yang tertahan di stok) Rp 3.825.000.

**Alasan skor DENGAN 9,0:**
- (+) Sesuai kunci: pratinjau dulu dengan "belum tersimpan" dan "Balas ya". Penyimpanan baru terjadi di giliran 2.
- (+) Kode barang (SKU) dijelaskan dan boleh diganti. Istilah HPP dijelaskan sebagai "modal rata-rata per barang". Nilai persediaan juga dijelaskan dengan bahasa awam.
- (+) Tidak ada jalur berkas atau kata proses. Kalimat "tersimpan di komputer ini" cukup jujur.
- (+) Ringkas: 1 pesan per giliran, tanpa tabel.
- (−) Margin per barang (jual − modal) tidak ditampilkan. Ini nilai tambah kecil yang mudah diberikan.
- (−) Penutup giliran 2 tidak memberi contoh kalimat untuk mencatat penjualan, misalnya "terjual 3 kaos hitam M".

**Alasan skor TANPA 5,0:** HPP dan stok 74 benar, termasuk ongkir yang ikut dihitung. Kekurangannya:
- Bot mengarang fakta. Kaos hitam M disebut "yang sudah ada di data, sisa 3 pcs @35rb", padahal pengguna menulis 24 pcs. Klaim ini juga tidak cocok dengan stok 74 yang ditulis bot sendiri. Lokasi rak "A3" dan "B4" juga tidak pernah disebut pengguna.
- Data langsung disimpan tanpa pratinjau atau konfirmasi. Giliran "ya" tidak menambah apa pun.
- Nama berkas `data/barang-masuk.csv` ditampilkan ke pembeli.
- Tidak ada kode barang dan tidak ada nilai persediaan. HPP ditulis dengan tanda "~" (kira-kira).

Catatan: rak dan "sisa 3 pcs" kemungkinan berasal dari data lama di workspace bot yang dipakai bersama, bukan dari pesan uji. Sisi DENGAN tidak terpengaruh, karena menghitung dari 24 pcs sesuai pesan. Untuk uji berikutnya, workspace bot sebaiknya dibersihkan sebelum sisi TANPA.

**Lintas cek:**
- Istilah proses atau jalur berkas: hanya di sisi TANPA.
- Tabel Markdown mentah: tidak ada.
- Terpotong: tidak ada.
- Panjang: 1 bagian per giliran di kedua sisi.

## Status sisi lain A8

| Skill | Topik (TANPA/DENGAN) | Status |
|---|---|---|
| absensi-lokal | 2185 / 2186 | TANPA (2185) lengkap. DENGAN (2186) giliran 2 gagal (router HTTP 530). **Menunggu kirim ulang**, belum dinilai. |
| pph-final-umkm | 2187 / 2188 | Gagal router. **Menunggu kirim ulang**, belum dinilai. |

## Catatan Akun A (17 Okt)
Sisi TANPA buku-stok (2183) kemungkinan membaca berkas sisa uji lain di workspace bot (`data/stok.csv`, `data/lokasi-rak.csv` dari A1 resi-picking) — asal "sisa 3 pcs" & rak A3/B4. Pengaruhnya menurunkan skor TANPA, jadi selisih +4,0 mungkin sedikit lebih besar dari semestinya; walau TANPA dinaikkan ke 7, selisih tetap ≥ 1,5 (LULUS tetap). Sejak 08:05 UTC sisa berkas uji lama di workspace bot dipindahkan ke cadangan scratchpad sebelum tiap gelombang.
