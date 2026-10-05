# Uji OpenClaw — Toko Online · Hitung harga jual Shopee (target untung 25%)

Tanggal uji: 2026-10-01 (Asia/Jakarta) · Penguji independen · Skill yang diharapkan: `harga-jual-marketplace`

OpenClaw lokal (`openclaw agent --local`), model router Komunitech (`ninerouter/komunitech`) yang sama dengan bot. SEBELUM = home `kosong-toko-online` (tanpa skill). SESUDAH = home `sol-toko-online` (paket skill solusi terpasang). Pesan identik.

## Pesan member

> kak aku jual tumbler stainless modal 38rb udh sm packing, mau jual di shopee. admin 8% , ikut gratis ongkir xtra 4% maks 10rb, biaya proses 1250 per pesanan. mau untung 25% brp harga jualnya ya

## Balasan SEBELUM (tanpa skill) — utuh

_Alat yang dipakai agent: `tidak ada` · model jawaban: `claude-sonnet-5` · durasi 29 detik_

> Oke, hitungannya gini kak (pakai metode harga jual mundur, biar persentase admin/ongkir/untung dihitung dari harga jual — ini cara standar seller Shopee itung harga):
>
> **Rumus:**
> HJ = (Modal + Biaya Proses) ÷ (1 − %Admin − %Ongkir − %Untung)
> HJ = (38.000 + 1.250) ÷ (1 − 0,08 − 0,04 − 0,25)
> HJ = 39.250 ÷ 0,63
> HJ ≈ **Rp 62.300**
>
> **Cek ulang (biar yakin):**
> - Harga jual: Rp 62.300
> - Admin 8%: Rp 4.984
> - Ongkir xtra 4% (belum nyentuh cap 10rb, aman): Rp 2.492
> - Biaya proses: Rp 1.250
> - Total potongan: Rp 8.726
> - Diterima bersih: Rp 53.574
> - Modal: Rp 38.000
> - **Untung bersih: Rp 15.574 → persis 25% dari harga jual ✅**
>
> Kalau mau angka lebih "cantik" buat listing, bulatkan ke **Rp 62.900** atau **Rp 63.000** — untungnya malah naik dikit jadi ~25,5–25,7%, masih aman.
>
> Catatan: ongkir xtra 4% baru kena cap 10rb kalau harga jual di atas ~Rp 250.000, jadi di range harga tumbler ini itungannya aman pakai persentase penuh.
>
> Kalau maksud "untung 25%" kakak itu dari modal (bukan dari harga jual), hasilnya beda — bisa aku hitungin juga kalau mau.

## Balasan SESUDAH (dengan paket skill) — utuh

_Alat yang dipakai agent: `read, exec` · model jawaban: `claude-sonnet-5` · durasi 23 detik_

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
> - Kalau mau pasang di angka cantik kayak Rp 59.900 atau Rp 62.900, bilang aja, aku hitungin ulang labanya persis di harga itu.

## Verifikasi angka & fakta (independen)

Dihitung ulang dengan Python (independen):

| Hal | SEBELUM | SESUDAH | Hitung ulang penguji |
|---|---|---|---|
| Rumus target margin 25% tanpa PPh 22 | 39.250 ÷ 0,63 = 62.301,59 → ditulis **Rp 62.300** | — | 62.301,59 (dibulatkan **ke bawah** ke 62.300 → margin 24,998%, sedikit di bawah target; klaim "persis 25%" tidak tepat, selisih kecil) |
| PPh 22 marketplace 0,5% (PMK 37/2025, berlaku 1 Agustus 2026 menurut `references/regulasi.md` skill) | **tidak dihitung** | dihitung Rp 315 | Dengan PPh 22, laba SEBELUM di Rp 62.300 = Rp 15.262 (margin 24,5%), bukan Rp 15.574 |
| Harga minimal balik modal | tidak diberikan | Rp 44.858 | 39.250 ÷ 0,875 = 44.857,14 → dibulatkan ke atas Rp 44.858 ✅ |
| Harga rekomendasi | Rp 62.300 (atau 62.900/63.000) | Rp 63.000 | Target dengan PPh = 62.800 → kelipatan Rp 500 ke atas = 63.000 ✅ |
| Rincian di Rp 63.000 | — | admin 5.040, ongkir 2.520, PPh 315, diterima 53.875, laba 15.875, margin 25,2%, markup 41,8% | 5.040 / 2.520 / 315 / 53.875 / 15.875 / 25,20% / 41,78% ✅ |
| Batas maks gratis ongkir 10rb | "baru kena kalau harga > ~Rp 250.000" | "2.520 < 10.000, aman" | 10.000 ÷ 4% = 250.000 ✅ keduanya benar |

Kesalahan fakta/aturan: SEBELUM melewatkan PPh 22 marketplace 0,5% yang sudah berlaku dan sedikit membulatkan ke bawah. SESUDAH benar semua angkanya; kekurangan kecil: catatan aturan hanya "berlaku per PMK terbaru" tanpa nomor PMK & tanggal berlaku (checklist skill meminta disclaimer + tanggal berlaku).

## Nilai

| | SEBELUM | SESUDAH |
|---|---|---|
| Skor (1–10) | 6.5 | 8.5 |

- **SEBELUM 6,5/10** — cepat dan rumusnya benar, plus menawarkan tafsir "untung dari modal". Tapi tidak memasukkan PPh 22 0,5% (aturan yang berlaku sejak Agustus 2026), tidak memberi harga balik modal, dan menyebut "persis 25%" padahal sedikit di bawah.
- **SESUDAH 8,5/10** — skill terpakai (`read` SKILL.md + `exec` script `harga_marketplace.py`; format & angka ceiling persis keluaran script). Harga minimal + rekomendasi + tabel siap pakai, PPh 22 disertakan dengan catatan pengecualian omzet ≤ Rp500 juta. Minus: tanpa nomor aturan/tanggal berlaku dan tanpa kalimat disclaimer "bukan nasihat pajak".

Kriteria: ketepatan, langsung siap pakai, kepatuhan aturan Indonesia, keamanan/privasi, kejelasan untuk awam.
