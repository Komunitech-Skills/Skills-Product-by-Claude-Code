# 00 — Uji A/B: S1 dengan vs tanpa skill

**Input pengguna (sama persis dengan S1):**
> Tolong bikinin kalender konten November 2026 buat toko hijab online aku, Nura Hijab (Bandung). Jualan pashmina ceruty, bergo instan, sama inner. Jualannya di Shopee & TikTok Shop, kontennya di IG sama TikTok aja. Tgl 11.11 ada promo diskon 20% semua pashmina + voucher gratis ongkir Shopee. Pembeli kebanyakan karyawati, gajiannya tgl 25.

## Output TANPA skill (AI agent biasa, tanpa membaca skill apa pun)
```
Kalender Konten Nura Hijab – November 2026

Minggu 1 (1–7 November)
| Tanggal | Hari   | Konten                                   | Platform |
| 1 Nov   | Minggu | Perkenalan koleksi pashmina ceruty        | IG, TikTok |
| 2 Nov   | Senin  | Tutorial pashmina simpel untuk kerja      | TikTok |
| 3 Nov   | Selasa | Testimoni pelanggan                       | IG |
| 4 Nov   | Rabu   | Tips memilih inner                         | IG, TikTok |
| 5 Nov   | Kamis  | Behind the scene packing                   | TikTok |
| 6 Nov   | Jumat  | Promo Jumat Berkah: diskon 10% bergo       | IG, TikTok |
| 7 Nov   | Sabtu  | OOTD weekend                               | IG |

Minggu 2 (8–14 November)
| 8 Nov   | Minggu | Q&A seputar hijab                          | IG Story |
| 9 Nov   | Senin  | Teaser 11.11: "2 hari lagi!"               | IG, TikTok |
| 10 Nov  | Selasa | Countdown 11.11: "Besok diskon besar!"     | IG, TikTok |
| 11 Nov  | Rabu   | PROMO 11.11! Diskon 20% semua pashmina + gratis ongkir | IG, TikTok |
| 12 Nov  | Kamis  | Promo 11.11 diperpanjang! Last call        | IG, TikTok |
| 13 Nov  | Jumat  | Tutorial pashmina kondangan                | TikTok |
| 14 Nov  | Sabtu  | Testimoni                                  | IG |

Minggu 3 (15–21 November)
... (pola serupa: tutorial, testimoni, tips, OOTD)

Minggu 4 (22–30 November)
... (pola serupa) 
| 25 Nov  | Rabu   | Promo Gajian! Diskon 15% semua produk      | IG, TikTok |

Tips: posting konsisten setiap hari, gunakan hashtag #hijabbandung #pashminaceruty, dan manfaatkan tren audio TikTok.
```

## Output DENGAN skill
Lihat `01-toko-hijab-november-11-11.md` (tabel 30 baris lengkap: tanggal, hari, momen, pilar, format, ide, hook ≤ 10 kata, CTA, status; CSV; tips; asumsi).

## Berdampingan

| Aspek | TANPA skill | DENGAN skill |
|---|---|---|
| Kelengkapan | Minggu 3–4 disingkat "pola serupa…" (hanya ±16 dari 30 hari terisi) | 30/30 hari terisi, tidak ada "dst." |
| Hari peringatan | **10 Nov (Hari Pahlawan) diisi countdown promo** "Besok diskon besar!" | 10 Nov konten penghormatan, tanpa promo |
| Promo karangan | "Jumat Berkah diskon 10% bergo", "diperpanjang 12 Nov", "Promo Gajian diskon 15%" — **tidak diberikan pengguna** | Hanya promo 11.11 dari pengguna; hari lain harga normal / `[isi: promo jika ada]` |
| Tanggal & hari | Benar untuk baris yang ada (dicek) | Benar 30/30 (script + verifikasi Zeller) |
| Momen lokal | Hanya 11.11 | 11.11, Hari Pahlawan, tanggal tua (konten hemat), gajian 25, Hari Guru |
| Struktur kerja | Konten 1 kolom | Pilar, format, hook, CTA, status (bisa dicentang) + CSV siap spreadsheet |
| Porsi jualan | ±7 promo di 16 baris (≈44%) | 7/30 (23%) |

## Penilaian
- **Lebih baik berkat skill:** (1) tidak ada promo di Hari Pahlawan — versi tanpa skill justru menaruh countdown promo di sana; (2) tidak ada promo karangan
  (tanpa skill mengarang 3 promo yang bisa membuat pemilik terikat janji diskon); (3) semua 30 hari terisi, siap dipakai admin; (4) CSV & kolom status.
- **Setara:** ide konten dasar (tutorial, testimoni, OOTD) mirip kualitasnya.
- **Kesimpulan:** hasil dengan skill **jelas lebih baik**.
