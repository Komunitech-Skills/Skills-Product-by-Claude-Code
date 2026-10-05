# Telegram gelombang 5 — 5 skill (2026-10-03)

Disetujui pemilik 2026-10-03 (keputusan no. 6 di grup). Penilaian oleh penilai independen (agent terpisah, hanya membaca pesan uji, jawaban bot, dan rujukan skill untuk cek fakta). Data di pesan uji fiktif.

## Cara
- 10 topik di grup uji (627–636): `G5 <skill> — TANPA skill` (setelan topik `skills: []`) dan `G5 <skill> — DENGAN skill`.
- Bot penguji mengirim 10 pesan (1 per sisi per skill), pesan identik untuk kedua sisi, berurutan, tanpa balas-otomatis.
- Jawaban diambil dari Telegram (`scratchpad/pilot/jawaban-g5-tg.txt`); pemakaian alat dari `jawaban-g5.txt`: semua sisi DENGAN skill membaca SKILL.md/rujukan dan menjalankan script (`exec`); sisi TANPA skill tanpa alat.
- Skor 1–10 per sisi menimbang: ketepatan, siap pakai, aturan Indonesia, keamanan/privasi, kejelasan. Semua angka dihitung ulang dengan python oleh penilai.

## Hasil

| Skill | TANPA | DENGAN | Selisih | Pembeda (satu kalimat) |
|---|---|---|---|---|
| katalog-reseller | 5 | 8,5 | +3,5 | DENGAN menghitung harga dari diskon atas harga eceran + untung mitra setelah biaya Shopee dan tidak menyuruh reseller jual di bawah harga eceran sendiri; TANPA menyarankan reseller jual Rp20–22 rb (merusak harga eceran Rp25 rb) tanpa memperhitungkan potongan Shopee. |
| kebijakan-privasi-pdp | 5,5 | 8,5 | +3 | DENGAN memuat dasar pemrosesan per tujuan, masa simpan, transfer luar negeri (Ps. 56), kebocoran 3×24 jam (Ps. 46), hak Ps. 5–13, plus Shopify/WhatsApp sebagai penerima; TANPA langsung jadi tetapi menyebut data Meta Pixel "bukan data pribadi" dan melewatkan transfer luar negeri, kebocoran, dan masa simpan. |
| lowongan-kerja | 5 | 9 | +4 | DENGAN menghapus keempat syarat diskriminatif (wanita, maks 25 th, belum menikah, berpenampilan menarik) dengan dasar SE Menaker M/6/HK.04/V/2025 + 3 versi (portal/IG/WA) + pertanyaan seleksi + cek UMK; TANPA masih memuat "wanita, usia maks 25" dan menawarkan menambah kembali syarat yang dihapus. |
| perjanjian-sederhana | 6 | 6,5 | +0,5 | DENGAN lebih benar isinya (jadwal 4 cicilan, total Rp36 jt, peringatan status hak pakai kios pasar, meterai), tetapi **file perjanjian lengkap gagal terkirim** sehingga pengguna hanya menerima ringkasan; TANPA memberi naskah utuh siap cetak meski lebih tipis. |
| program-referral-loyalitas | 5,5 | 9 | +3,5 | DENGAN menghitung biaya per referral vs laba pesanan pertama & seumur pelanggan, kuota anggaran, batas aman, dan opsi lebih hemat dari iklan, plus aturan anti-curang dan teks WA satu-per-satu dengan STOP; TANPA salah hitung laba bersih per pelanggan (diskon terhitung dua kali) dan teks WA bernada blast. |

Rata-rata: TANPA 5,4 → DENGAN 8,3 (selisih +2,9). Empat skill memenuhi acuan (sesudah ≥ 8, selisih ≥ 1,5); **perjanjian-sederhana tidak** di gelombang ini karena kegagalan kirim file.

## Verifikasi angka (python, penilai)

**katalog-reseller** (HPP Rp9.500, eceran Rp25.000)
- TANPA: dropship 18.000 / reseller 16.000 (×20 = 320.000 ✅) / agen 13.500 (×100 = 1.350.000 ✅). Margin produsen 47,2% / 40,6% / 29,6%. Untung reseller "Rp4–6 rb" = 20.000/22.000 − 16.000 ✅ tetapi di bawah harga eceran sendiri dan belum dipotong biaya Shopee.
- DENGAN: diskon 20/25/35% dibulatkan ke bawah per Rp100 → 20.000 / 18.700 / 16.200 ✅; modal 20 pcs 374.000 ✅, 100 pcs 1.620.000 ✅; untung mitra setelah biaya jual 10% (22.500 − harga mitra) = 2.500 / 3.800 (×20 = 76.000) / 6.300 (×100 = 630.000) ✅; margin produsen 52,5% / 49,2% / 41,4% → "40%+" ✅.

**program-referral-loyalitas** (pesanan Rp150.000, laba kotor 45%)
- Laba per pesanan 67.500; diskon 15% = 22.500; biaya per referral 22.500 + 25.000 = 47.500 ✅ (31,67% pesanan ✅, 70,37% laba ✅); laba pesanan pertama setelah hadiah 20.000 ✅; lebih mahal dari iklan Rp7.500 ✅.
- Anggaran Rp1 jt: 21 referral, terpakai 997.500, sisa 2.500 ✅ (TANPA: 40 bila hanya voucher ✅, 21 bila total ✅).
- Laba seumur pelanggan 8 × 67.500 = 540.000; batas 30% = 162.000 ✅; saran konservatif 50% laba pesanan pertama = 33.750 ✅.
- Opsi hemat: 15.000 + 22.500 = 37.500 (25%) ✅, 2.500 lebih murah dari iklan ✅, 26 referral, sisa 25.000 ✅.
- **TANPA salah:** laba 8 bulan 517.500 (diskon sudah dikurangi di bulan 1) lalu dikurangi lagi 47.500 (diskon terhitung dua kali) → Rp470.000; yang benar 540.000 − 47.500 = **Rp492.500**.

**perjanjian-sederhana**: Rp18 jt × 2 th = 36.000.000 ✅; cicilan 9.000.000 ×4 (1 Nov 2026, 1 Mei 2027, 1 Nov 2027, 1 Mei 2028) ✅; periode 1 Nov 2026 – 31 Okt 2028 ✅ (keduanya). Denda DENGAN 0,1%/hari maks 5% → Rp9.000/hari, maks Rp450.000 per cicilan (asumsi template, diminta konfirmasi). Meterai Rp10.000 × 2 rangkap (UU 10/2020) ✅.

**kebijakan-privasi-pdp**: hitungan isian kosong "11 isian, 14 tempat" dicocokkan ✅ (alamat 2×, WA 3×, masa simpan 3 jenis).

**lowongan-kerja**: tenggat 17 Okt 2026 = 14 hari dari 3 Okt ✅ (tidak diminta pengguna, default skill).

## Cek fakta aturan
- **UU PDP 27/2022**: hak subjek Ps. 5–13 ✅; transfer ke luar negeri Ps. 56 ✅; pemberitahuan kebocoran tertulis 3×24 jam ke subjek & lembaga Ps. 46 ✅; tanggapan 3×24 jam Ps. 30/32/40 sesuai rujukan skill. PP 33/2026 & "lembaga pengawas belum terbentuk" berasal dari `references/dasar-hukum.md` yang sendiri menandai naskah PP belum terbaca langsung → tetap PERLU REVIEW. TANPA: klaim Meta Pixel "bukan data pribadi identitas" tidak tepat (piksel dapat mengirim pengenal ter-hash & perilaku yang terkait orang); persetujuan promo digabung dengan persetujuan pemesanan.
- **Anti-diskriminasi rekrutmen**: SE Menaker M/6/HK.04/V/2025 (larangan syarat usia, penampilan, status perkawinan, dll. yang tidak terkait pekerjaan) dan UU 13/2003 Ps. 5–6 ✅. Pengecualian upah minimum usaha mikro & kecil (PP 36/2021) disebut tepat secara umum; gaji Rp2,5–3 jt kemungkinan jauh di bawah UMK Sidoarjo — DENGAN meminta pengguna cek angka UMK alih-alih menyebut angka (aman, tetapi bisa lebih tegas).
- **katalog-reseller**: "harga minimum anjuran" + konsekuensi non-denda selaras dengan `references/regulasi.md` (UU 5/1999 Ps. 8 RPM, Ps. 50 huruf h pengecualian usaha kecil) ✅.
- **Perjanjian sewa (KUHPerdata)**: TANPA menulis NIK/alamat perlu dilengkapi "biar sah secara hukum" — tidak tepat; syarat sah Ps. 1320 KUHPerdata tidak bergantung pada NIK atau meterai (meterai = bea dokumen/alat bukti). DENGAN benar menyoroti status hak pakai kios pasar & izin pengelola.

## Cacat / temuan
1. **perjanjian-sederhana DENGAN — file gagal terkirim** (`perjanjian_sewa_kios_b12.md: Delivery failed`): naskah lengkap tidak sampai ke pengguna; yang terlihat hanya ringkasan pasal. Perlu perbaikan di skill/alur bot: tampilkan naskah utuh di chat bila lampiran gagal (atau pecah per pesan).
2. **perjanjian-sederhana DENGAN — kontradiksi iuran pasar**: Pasal 5(2)b menyebut iuran pengelola pasar ditanggung penyewa, sementara daftar asumsi menyebut "PBB/iuran pengelola pasar ditanggung pemilik (Pasal 4)". Template memuat klausul pengosongan tanpa proses hukum (Pasal 7(3)) — sudah diberi peringatan, tetapi sebaiknya tidak dijadikan default.
3. **perjanjian-sederhana TANPA** menulis "untuk kebutuhan testing" di catatan (bot tahu sedang diuji) — artefak lingkungan uji.
4. **kebijakan-privasi-pdp DENGAN**: pengguna minta "langsung jadi", hasil berstatus "BELUM SIAP" dengan 14 tempat kosong — jujur dan aman, tetapi kurang instan; pertimbangkan default terisi (tanggal = hari ini, masa simpan saran) dengan tanda asumsi.
5. **lowongan-kerja DENGAN**: menambahkan tenggat 17 Okt 2026 yang tidak diminta (minor; sebutkan sebagai asumsi). TANPA menawarkan menambahkan kembali syarat diskriminatif "risiko kamu tanggung sendiri".
6. **program-referral-loyalitas DENGAN**: opsi hemat Rp37.500 masih di atas saran konservatif Rp33.750 tetapi tidak disebut (minor). TANPA: salah hitung Rp470.000 (benar Rp492.500) dan ajakan "share ke grup".
7. **katalog-reseller TANPA**: pesan ajakan disebut "siap kirim/broadcast" dan tanpa opsi berhenti; DENGAN memakai "Balas STOP".
8. Nomor WA dan nama di pesan uji fiktif; tidak disalin ke laporan ini.

## Rekomendasi
- katalog-reseller, kebijakan-privasi-pdp, lowongan-kerja, program-referral-loyalitas: layak masuk daftar tampil (selisih ≥ 3).
- perjanjian-sederhana: perbaiki penanganan lampiran gagal kirim + kontradiksi iuran, lalu ulang uji Telegram (perlu persetujuan pemilik).
