# Uji OpenClaw sebelum/sesudah: harga-jual-marketplace (1.0.3 dan uji ulang 1.0.4)

Berkas ini hanya merangkum dan mengutip hasil uji yang **sudah tercatat** di `solusi-vip/toko-online/UJI-OPENCLAW.md` dan `solusi-vip/toko-online/uji-openclaw/01-harga-jual-shopee.md`, `01-harga-jual-shopee-ulang.md`, `01-harga-jual-shopee-ulang2.md` (rujukan di repo Komunitech). Tidak ada uji baru dijalankan untuk berkas ini; semua kutipan balasan agent disalin dari berkas-berkas itu (dipotong seperlunya, tanda `[…]`).

## Kepala uji

- **Tanggal uji:** 2026-10-01 (Asia/Jakarta), tiga putaran pada tanggal yang sama: uji pertama (TANPA dan DENGAN), uji ulang 1 (hanya DENGAN, skill 1.0.3), uji ulang 2 (hanya DENGAN, skill 1.0.4).
- **Penguji:** agent penguji independen Komunitech (bukan pembuat skill).
- **Cara uji:** OpenClaw lokal (`openclaw agent --local`, tanpa Telegram/gateway), memakai model router Komunitech yang sama dengan bot member (`ninerouter/komunitech`; jawaban dilayani `claude-sonnet-5` di kedua sisi). SEBELUM = home `kosong-toko-online` (skill dimatikan: folder `~/.openclaw/skills` kosong). SESUDAH = home `sol-toko-online` (paket skill Toko Online + skill tambahan VIP terpasang). Pesan identik di kedua sisi, ditulis seperti pemilik toko awam mengetik di chat. Uji ulang memakai home yang dibuat ulang (direset) dari skill terbaru di repo sebelum skenario, pesan member sama persis, hanya sisi SESUDAH. Pemakaian skill dicek dari daftar tool di keluaran JSON (`successfulToolNames`) dan format keluaran yang sama dengan keluaran script skill.
- **Versi OpenClaw:** tidak dicatat di berkas-berkas sumber uji ini. `catalog.csv` mencatat untuk skill ini "openclaw 2026.9.6–9.7 (uji sebelum/sesudah otomatis 2026-10-01)".
- **Versi skill yang diuji:** uji ulang 1 = **1.0.3**; uji ulang 2 = **1.0.4**. Versi skill pada uji pertama tidak dicatat di berkas sumber; `CHANGELOG.md` mencatat revisi 1.0.3 dibuat sebagai tanggapan atas temuan uji OpenClaw, jadi uji pertama berjalan pada versi sebelum 1.0.3. Versi di katalog sekarang: **1.0.6**.
- **Data:** fiktif (tumbler stainless; semua angka ada di pesan, tanpa berkas).
- **Verifikasi angka:** dihitung ulang penguji dengan Python secara independen; di uji ulang 2 script skill juga dijalankan ulang oleh penguji.

**Catatan jujur tentang cakupan:** uji ini dijalankan sebagai **satu skenario (skenario 01 dari 5)** dalam uji solusi VIP Toko Online, bukan 5 skenario per skill. Skor "rata-rata 6,4 → 8,4" di `UJI-OPENCLAW.md` adalah rata-rata 5 skill berbeda, bukan angka skill ini. Sisi TANPA skill dijalankan **sekali** (uji pertama); uji ulang hanya sisi DENGAN, sehingga pembandingnya tetap skor TANPA uji pertama. Konteks kanal Telegram untuk skenario ini tidak diuji. Argumen tool call tidak bisa diperiksa (hanya nama tool: `read, exec`); bukti pemakaian script disimpulkan dari format keluaran. Versi skill sekarang (1.0.6) lebih baru daripada yang diuji (lihat "Catatan versi" di bawah).

## Tugas (pesan pengguna)

> kak aku jual tumbler stainless modal 38rb udh sm packing, mau jual di shopee. admin 8% , ikut gratis ongkir xtra 4% maks 10rb, biaya proses 1250 per pesanan. mau untung 25% brp harga jualnya ya

**Angka penguji (hitung ulang Python):** (38.000 + 1.250) ÷ (1 − 0,08 − 0,04 − 0,005 − 0,25) = **62.800** → kelipatan Rp500 ke atas **Rp63.000** · harga balik modal 39.250 ÷ 0,875 = 44.857,14 → **Rp44.858** · di Rp63.000: admin 5.040, gratis ongkir xtra 2.520 (di bawah batas 10.000), PPh 22 marketplace 315, uang diterima 53.875, **laba 15.875**, margin 25,20%, markup 41,78%. Tanpa PPh 22, harga Rp62.300 memberi margin 24,998%; dengan PPh 22 di harga yang sama, laba **Rp15.262** (margin 24,5%), bukan Rp15.574.

## Skor

| Putaran | Skill yang diuji | TANPA skill | DENGAN skill | Verdik |
|---|---|:-:|:-:|---|
| Uji pertama (2026-10-01) | versi tidak dicatat di sumber (sebelum 1.0.3) | **6,5** | **8,5** | belum ada verdik per skill; temuan: catatan aturan hanya "berlaku per PMK terbaru" |
| Uji ulang 1 (2026-10-01) | 1.0.3 | tidak diulang (pembanding 6,5) | **8,5** (sebelumnya 8,5) | **LULUS** (saran: harga alternatif wajib dihitung script) |
| Uji ulang 2 (2026-10-01) | 1.0.4 | tidak diulang (pembanding 6,5) | **8,5** (sebelumnya 8,5) | **LULUS** (saran: ganti teks catatan script jadi "minta hitung ulang tanpa PPh 22") |

Selisih terhadap TANPA skill pada skenario ini: +2,0 poin (8,5 − 6,5). Kriteria nilai (1–10): ketepatan, langsung siap pakai, kepatuhan aturan Indonesia, keamanan/privasi, kejelasan untuk awam.

## Hasil TANPA skill (6,5)

_Alat yang dipakai agent: tidak ada · model jawaban: `claude-sonnet-5` · durasi 29 detik._

> Oke, hitungannya gini kak (pakai metode harga jual mundur, biar persentase admin/ongkir/untung dihitung dari harga jual — ini cara standar seller Shopee itung harga):
>
> **Rumus:**
> HJ = (Modal + Biaya Proses) ÷ (1 − %Admin − %Ongkir − %Untung)
> HJ = (38.000 + 1.250) ÷ (1 − 0,08 − 0,04 − 0,25)
> HJ = 39.250 ÷ 0,63
> HJ ≈ **Rp 62.300**
>
> **Cek ulang (biar yakin):**
> […]
> - Total potongan: Rp 8.726
> - Diterima bersih: Rp 53.574
> - Modal: Rp 38.000
> - **Untung bersih: Rp 15.574 → persis 25% dari harga jual ✅**
>
> Kalau mau angka lebih "cantik" buat listing, bulatkan ke **Rp 62.900** atau **Rp 63.000** — untungnya malah naik dikit jadi ~25,5–25,7%, masih aman.
> […]
> Kalau maksud "untung 25%" kakak itu dari modal (bukan dari harga jual), hasilnya beda — bisa aku hitungin juga kalau mau.

**Kelemahan (menurut penguji):**
- Tidak memasukkan PPh 22 marketplace 0,5% (menurut `references/regulasi.md` skill saat itu, berlaku sejak Agustus 2026; tanggalnya dikoreksi di 1.0.6, lihat "Catatan versi"). Laba dilaporkan Rp15.574, padahal dengan PPh 22 di harga yang sama Rp15.262 (margin 24,5%).
- Klaim "persis 25%" tidak tepat: Rp62.300 adalah pembulatan ke bawah dari 62.301,59, marginnya 24,998%.
- Tidak memberi harga balik modal (harga minimal).
- Sisi baiknya: rumus benar, cepat, dan menawarkan tafsir "untung dari modal".

## Hasil DENGAN skill (8,5, uji pertama)

_Alat yang dipakai agent: `read, exec` · model jawaban: `claude-sonnet-5` · durasi 23 detik._

> Modal 38rb, admin 8%, gratis ongkir xtra 4% (maks 10rb), biaya proses 1.250/pesanan, target margin 25%:
>
> ### Shopee - target margin 25%
> - Harga minimal biar ga rugi: **Rp 44.858**
> - **Harga rekomendasi: Rp 63.000**
>
> | Komponen | Nilai |
> |---|---:|
> | Harga tayang | Rp 63.000 |
> | Admin (8%) | -Rp 5.040 |
> | Gratis ongkir xtra (4%) | -Rp 2.520 |
> | Biaya proses/pesanan | -Rp 1.250 |
> | PPh 22 marketplace (0,5%) | -Rp 315 |
> | **Uang diterima** | **Rp 53.875** |
> | Modal | -Rp 38.000 |
> | **Laba bersih** | **Rp 15.875** (margin 25,2%, markup 41,8%) |
>
> Catatan:
> - 4% gratis ongkir xtra belum kena batas maks 10rb di harga ini (2.520 < 10.000), jadi aman.
> - PPh 22 0,5% dari marketplace sudah dimasukkan (berlaku per PMK terbaru). Kalau kamu penjual perorangan dengan omzet setahun ≤ Rp500jt dan sudah kasih surat pernyataan ke Shopee, bisa dikecualikan — laba bisa naik dikit lagi.
> […]

**Kelebihan (menurut penguji):** `SKILL.md` dibaca dan script `harga_marketplace.py` dijalankan (format dan angka pembulatan persis keluaran script). Semua angka cocok dengan hitung ulang penguji. Harga minimal + rekomendasi + tabel siap pakai, PPh 22 disertakan dengan catatan pengecualian omzet ≤ Rp500 juta. **Kekurangan:** tanpa nomor aturan/tanggal berlaku dan tanpa kalimat disclaimer "bukan nasihat pajak".

## Uji ulang 1 (skill 1.0.3, hanya sisi DENGAN): 8,5

_Alat: `read, exec` · 18 detik._ Cacat lama (catatan aturan diringkas) **hilang**: blok catatan disalin utuh dari script.

> **Catatan & asumsi**
> […]
> - PPh 22 marketplace 0,5% (PMK 37/2025, berlaku 1 Agustus 2026). Penjual orang pribadi dengan omzet setahun s.d. Rp500 juta bisa dikecualikan jika sudah menyampaikan surat pernyataan ke marketplace; hitung ulang tanpa PPh 22 kalau sudah daftar.
> - Berlaku per 2026-09-23. Alat bantu hitung, bukan nasihat pajak.
>
> 💡 Rp 63.000 udah pas kelipatan Rp500 dan laba sedikit di atas target (25,2% vs 25% yang diminta), aman buat dipasang. Kalau mau psikologis Rp 62.900 atau Rp 59.900, laba/marginnya bakal turun sedikit di bawah target — mau aku hitungin juga?

**Angka:** semua angka script benar (minimal 44.858, rekomendasi 63.000, laba 15.875, margin 25,2%). **Temuan baru (kecil):** narasi model di luar script menyatakan Rp62.900 "di bawah target", padahal marginnya 25,10% (salah; Rp59.900 memang di bawah target). Risiko rendah karena model menawarkan menghitung ulang. Saran penguji: jangan menyatakan untung/rugi harga lain sebelum dihitung script.

## Uji ulang 2 (skill 1.0.4, hanya sisi DENGAN): 8,5

_Alat: `read, exec`._ Cacat sisa dari uji ulang 1 **hilang**: tidak ada lagi klaim untung/rugi harga lain tanpa script.

> Status: **memenuhi target margin 25%** (hasil hitung script, bukan taksiran).
>
> 💡 Saran:
> - Rp 63.000 udah "pas" psikologis-ish. Kalau mau coba harga lebih "nanggung" kayak Rp 62.900, bisa aku hitung ulang labanya biar ketahuan masih kena target atau turun dikit.
> […]
>
> **Catatan & asumsi**
> […]
> - PPh 22 marketplace 0,5% (PMK 37/2025, berlaku 1 Agustus 2026). Penjual orang pribadi dengan omzet setahun s.d. Rp500 juta bisa dikecualikan jika sudah menyampaikan surat pernyataan ke marketplace; hitung ulang dengan --pph22 tidak. PPh 22 ini bukan pajak baru; cara memperhitungkannya dengan PPh final Anda, tanyakan ke DJP/konsultan.
> - Berlaku per 2026-09-23. Alat bantu hitung, bukan nasihat pajak.

**Angka:** benar semua (target 62.800 → 63.000, minimal 44.858, laba 15.875, margin 25,2%, markup 41,78%); pembanding penguji: Rp62.900 → margin 25,10% (memenuhi), Rp59.900 → 21,97% (di bawah). **Temuan baru (kecil, jargon):** karena catatan disalin kata per kata, teks perintah script ikut sampai ke member awam ("hitung ulang dengan --pph22 tidak"). Sumbernya teks catatan di script sendiri; saran penguji: ubah menjadi "minta hitung ulang tanpa PPh 22".

## Verdik: LULUS

Uji ulang terakhir (1.0.4): DENGAN skill **8,5** (≥ 8), selisih terhadap TANPA skill **+2,0** (≥ 1,5). Angka hasil script di sisi DENGAN skill benar pada ketiga putaran; satu klaim narasi model yang salah (Rp62.900 "di bawah target", padahal margin 25,10%) muncul di putaran 1.0.3 dan tidak muncul lagi di 1.0.4. Batasan: ini **satu skenario**, satu pesan, satu run per sisi per putaran.

## Catatan versi (setelah uji)

Perubahan berikut ada di `CHANGELOG.md` dan **tidak** tercakup uji di atas (berkas sumber uji berhenti di 1.0.4):
- **1.0.5:** catatan PPh 22 di keluaran script tidak lagi menampilkan teks perintah `--pph22 tidak` (menjawab temuan jargon uji ulang 2).
- **1.0.6:** tanggal PPh 22 marketplace dikoreksi: bukan "berlaku 1 Agustus 2026", melainkan dipungut sejak 1 Oktober 2026. Kutipan balasan agent di atas adalah rekaman uji 2026-10-01 dan sengaja tidak diubah, jadi masih memuat tanggal lama.

## Kalimat pembeda

Tanpa skill, AI menghitung harga Shopee dengan potongan admin dan gratis ongkir tetapi melewatkan PPh 22 marketplace 0,5%, sehingga laba tampak Rp15.574 ("persis 25%") padahal Rp15.262 di harga yang sama; dengan skill, harga minimal Rp44.858 dan harga rekomendasi Rp63.000 dihitung script lengkap dengan PPh 22 (Rp315) dan laba bersih Rp15.875 (margin 25,2%).
