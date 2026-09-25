# Uji 02 — Toko online hijab cari ide promo menjelang Harbolnas 11.11 (skenario normal)

Penguji independen (Tahap 6), 2026-09-25 (11.11.2026 jatuh pada **Rabu**, 47 hari lagi — dihitung dengan `datetime`). Jawaban pengguna disimulasikan.

## Permintaan awal

> "Kak, aku jualan hijab di Shopee sama TikTok Shop. Mau ikutan 11.11 tapi bingung promonya apa selain diskon. Ada ide?"

## Dialog

**Agent (klasifikasi):** "Ini ide promo untuk toko yang sudah jalan dan bisa diuji sebelum hari-H — saya pakai **Jalur B (Perlu Diuji)**. Setelah idenya dipilih, hitungan diskon aman & jadwal kampanye lengkapnya lebih pas pakai skill `promo-kalender` (ada cek margin otomatis)."

**Agent (1 pertanyaan):** "Produk terlaris dan kisaran harga + modalnya berapa?"
**Pengguna:** "Pashmina ceruty 45 ribu, modal 24 ribu. Bergo instan 55 ribu, modal 30 ribu. Sehari rata-rata 30 pesanan."

**Agent:** "Anggaran promo & stok tambahan untuk 11.11 kira-kira berapa, dan siapa yang packing?"
**Pengguna:** "Budget 3 juta buat stok tambahan. Packing aku sama adik."

**Agent:** "Tahun lalu ikut 11.11? Apa yang terjadi?"
**Pengguna:** "Ikut, diskon 30%, rame tapi untungnya tipis banget, capek."

**Agent (tulis ulang pemahaman):**
> **Disebutkan:** toko hijab online (Shopee + TikTok Shop), ±30 pesanan/hari, pashmina Rp45.000 (modal Rp24.000), bergo Rp55.000 (modal Rp30.000), dana stok Rp3 juta, tenaga packing 2 orang, 11.11 tahun lalu diskon 30% = ramai tapi untung tipis.
> **Asumsi saya:** tujuan = omzet naik di 11.11 **tanpa** perang diskon besar; berhasil = pesanan 11.11 ≥ 2× rata-rata harian (≥60) dengan untung per pesanan tidak turun jauh dari hari biasa. Potongan biaya marketplace belum dihitung — nanti dicek di `promo-kalender`/`harga-jual-marketplace`.
> Betul?

**Pengguna:** "Betul."

**Agent (teknik: Gabung-Kombinasi "Produk + Momen" & Pembalikan Masalah):**
Alasan pembeli tidak jadi beli saat 11.11: "toko lain diskon lebih besar" → jangan adu diskon, adu **nilai paket**; "ongkir mahal" → gratis ongkir dengan minimum belanja; "takut warna beda" → video warna asli saat live.

Ide mentah (5): bundling hijab + inner + bros edisi 11.11; mystery box Rp111.000; pre-order warna eksklusif 11.11; live 11 jam dengan flash sale per jam; gratis ongkir min. belanja Rp111.000.

Karena ada 5 ide dan pengguna bertanya "mana yang paling cocok", agent **menawarkan** skor tertimbang (SKILL.md hanya mewajibkannya di Jalur C); pengguna setuju dan memberi bobot: permintaan & margin paling penting (5), kemudahan 4, modal 3, keahlian 2.

```
python3 scripts/skor_ide.py skor --ide ide02.csv --bobot bobot02.json
```
Keluaran asli:
```
1         Bundling hijab + inner + bros edisi 11.11             4.105
2         Gratis ongkir min belanja 111 ribu                    3.684
3         Pre-order warna eksklusif 11.11                       3.632
4         Mystery box hijab 111 ribu                            3.474
5         Live jualan 11 jam (flash sale per jam)               3.368
Bobot kriteria dipakai (total bobot = 19)
```
Verifikasi independen (Python terpisah, Σ nilai×bobot ÷ 19): 78/19 = 4,1053; 70/19 = 3,6842; 69/19 = 3,6316; 66/19 = 3,4737; 64/19 = 3,3684 — **cocok**.

**Agent (2–3 teratas + untung-rugi):**

| Ide | Untung | Risiko |
|---|---|---|
| **Bundling hijab + inner + bros "Paket 11.11"** (4,11) | Nilai terasa besar tanpa diskon dalam; margin paket bisa dijaga; stok inner/bros murah | Perlu foto paket baru; stok bros harus pas |
| **Gratis ongkir min. belanja Rp111.000** (3,68) | Paling mudah dijalankan, mendorong beli 2–3 pcs | Biaya ongkir menggerus margin — wajib dicek di `promo-kalender` |
| **Pre-order warna eksklusif** (3,63) | Margin tertinggi, tanpa stok di muka | Tidak cocok bila pembeli 11.11 mengharap kirim cepat |

Rekomendasi: **Paket 11.11** sebagai ide utama, digabung syarat gratis ongkir (paket otomatis ≥ Rp111.000). Skor hanya alat bantu; keputusan tetap di Anda.

**Pengguna:** "Oke bundling + gratis ongkir."

## Output akhir

1. **Ringkasan:** omzet 11.11 ≥ 60 pesanan tanpa perang diskon, dana stok Rp3 juta, packing 2 orang.
2. **Ide dipertimbangkan:** tabel skor di atas (5 ide, bobot disepakati).
3. **Ide terpilih:** Paket 11.11 (pashmina + inner + bros) + gratis ongkir min. Rp111.000.
4. **Uji murah (MVP) sebelum hari-H:** pasang Paket 11.11 sebagai "early access" di etalase + story/live 1 minggu (26 Okt–1 Nov 2026, jauh sebelum 11.11). Target: ≥15 paket terjual atau ≥50 orang memasukkan ke keranjang/"ingatkan saya". Lanjut & stok penuh jika tercapai; perbaiki isi paket jika 8–14; ganti ke ide lain (pre-order warna) jika < 5. Biaya uji maks Rp600.000 (stok 20 inner + 20 bros).
5. **Rencana Aksi 7 Hari** (mulai Senin 26 Okt 2026):

| Hari | Tugas |
|---|---|
| 1 | Tentukan isi 2 varian paket; hitung harga & diskon aman pakai skill `promo-kalender` (cek margin setelah potongan marketplace) |
| 2 | Foto/video paket (warna asli, cahaya siang) |
| 3 | Upload "Paket 11.11 – early access" di Shopee & TikTok Shop, stok terbatas 20 |
| 4 | Live 1 jam memperkenalkan paket; catat keranjang & pesanan |
| 5 | Broadcast ke pembeli lama lewat fitur chat/voucher toko (bukan blast WA) |
| 6 | Rekap pesanan, keranjang, pertanyaan pembeli |
| 7 | Putuskan: stok penuh untuk 11.11, ubah isi paket, atau ganti ide |

6. **Asumsi:** biaya admin/layanan marketplace belum dihitung; angka target 60 pesanan adalah usulan agent, bukan data pasar.

## Catatan penguji
- Tanggal 11.11 benar (tetap tiap tahun); tidak ada klaim tanggal Harbolnas resmi yang dikarang.
- Pembagian kerja dengan `promo-kalender` jelas (brainstorming = pilih ide; promo-kalender = mekanisme, diskon, margin).
- Temuan kecil: `references/musim-dan-momentum.md` menulis "9.9, 10.10, 11.11, 12.12, plus 1.1 & Harbolnas 12.12 nasional" — 12.12 disebut dua kali; dan rentang "gajian 25–30" tumpang tindih dengan "tanggal tua 20–28".
