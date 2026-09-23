# 00 — Uji banding pesaing (S1)

## Pencarian
- Kata kunci: "quotation", "quote", "price quote", "estimate", "SPH", "penawaran harga", "SKILL.md quote".
- Sumber dicek: github.com/VoltAgent/awesome-openclaw-skills (daftar kategori), github.com/anthropics/skills, github.com/manairalabs/bicara-skills, github.com/alvinindra/bahasa-skills, pencarian web GitHub. ClawHub/clawskills.sh **diblokir proxy jaringan** (403) sehingga halaman skill di sana tidak bisa dibaca — dicatat apa adanya.
- Temuan relevan: **`quote-drafter`** dari github.com/Ootto-AI/claude-invoice-skills (lisensi **MIT**, v1.0.0) — "turn a few bullet points into a clean, client-ready quote or proposal". Lainnya (bexio, estimate-builder konstruksi, invoice-template) berupa integrasi API atau tidak terbaca; tidak ada skill SPH berbahasa Indonesia di bicara-skills/bahasa-skills/anthropics.
- Script pihak ketiga tidak dijalankan; isi tidak disalin.

## Input S1 (sama)
> Tolong bikinin surat penawaran harga dari usaha saya Percetakan Sinar Jaya Fiktif (…, belum PKP) buat SMA Harapan Bangsa Fiktif, ke Bu Wati bendahara. 500 buku tulis custom logo @7.500, 20 banner 3x1 m @150rb, 1000 kartu pelajar PVC @12rb. Diskon 5% dari total, ongkir gratis dalam kota. Nomor surat 45.

## Output dengan instruksi pesaing (`quote-drafter`, disimulasikan)
Instruksi pesaing: kumpulkan klien/kebutuhan/scope/harga/timeline/pengecualian; susun 6 bagian (ringkasan, scope, tabel harga + grand total, timeline, yang tidak termasuk, langkah berikut); jangan mengarang harga/tanggal; pertanyaan yang kurang ditaruh di atas.
```
Pertanyaan sebelum finalisasi:
- Kapan pesanan dibutuhkan / estimasi waktu pengerjaan?
- Ada hal yang tidak termasuk (mis. desain logo, revisi)?

PENAWARAN HARGA – Percetakan Sinar Jaya Fiktif untuk SMA Harapan Bangsa Fiktif

Ringkasan
Kami memahami SMA Harapan Bangsa Fiktif membutuhkan perlengkapan sekolah bercetak logo untuk
tahun ajaran ini. Kami menawarkan paket buku tulis custom, banner, dan kartu pelajar PVC dalam satu pesanan.

Lingkup pekerjaan
- Cetak 500 buku tulis dengan logo sekolah
- Cetak 20 banner ukuran 3x1 m
- Cetak 1.000 kartu pelajar PVC

Harga
| Item | Qty | Harga | Total |
| Buku tulis custom | 500 | Rp 7.500 | Rp 3.750.000 |
| Banner 3x1 m | 20 | Rp 150.000 | Rp 3.000.000 |
| Kartu pelajar PVC | 1.000 | Rp 12.000 | Rp 12.000.000 |
| Subtotal | | | Rp 18.750.000 |
| Diskon 5% | | | -Rp 937.500 |
| TOTAL | | | Rp 17.812.500 |

Timeline: [menunggu konfirmasi]
Tidak termasuk: [menunggu konfirmasi]; ongkir gratis dalam kota.
Langkah berikutnya: balas email ini dengan konfirmasi pesanan untuk memulai produksi.
```

## Output dengan skill kita
Lihat `01-percetakan-ke-sekolah-non-pkp.md`.

## Penilaian

| Kriteria | Pesaing (`quote-drafter`) | Skill kita |
|---|---|---|
| Kualitas & kelengkapan | Rapi, 6 bagian; tanpa nomor surat, tanpa masa berlaku, tanpa syarat bayar/rekening, tanpa terbilang | Surat lengkap: nomor baku, masa berlaku bertanggal, syarat bayar & kirim, terbilang, + teks WA |
| Kesesuaian konteks Indonesia | Format proposal gaya Barat; tidak tahu PKP/PPN, pola nomor surat, "Kepada Yth." | Format SPH lokal, PPN PMK 131/2024, non-PKP → "tidak dikenakan PPN" |
| Akurasi | Benar di kasus ini (hitungan sederhana di kepala); tidak ada mekanisme untuk kasus PKP/diskon per baris | Script teruji (0 selisih pada 400 kasus acak) |
| Siap pakai | Perlu diedit jadi surat resmi | Siap kirim (PDF + WA) |
| **Total** | Kalah | **Menang** |

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
1. Bagian **"yang tidak termasuk"** (mis. desain, revisi, pemasangan) mengurangi sengketa — bisa ditambahkan sebagai poin opsional di syarat & ketentuan.
2. **Ringkasan satu paragraf yang menunjukkan pemahaman kebutuhan pembeli** sebelum tabel — cocok untuk penawaran proaktif.
3. Menaruh pertanyaan yang kurang **di atas draf** sambil tetap memberi draf — pola yang sama dengan "default + asumsi" kita, tetapi lebih terlihat.

Kesimpulan: tidak ada pesaing yang lebih baik; skill kita unggul terutama pada aspek lokal (PPN/PKP, format surat, WA).
