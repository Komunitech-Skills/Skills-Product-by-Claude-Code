# Uji banding pesaing: skenario 01

**Penguji:** agent independen, 2026-09-25. Skill pesaing hanya **dibaca untuk dinilai** (diambil sebagai teks lewat raw.githubusercontent / halaman katalog). Tidak dipasang, tidak dijalankan, tidak disalin.

## Pencarian
| Sumber | Kata kunci | Temuan |
|---|---|---|
| Web / GitHub | "SKILL.md ads report", "ad performance skill Meta Ads CSV weekly report claude skill github" | `AgriciDaniel/claude-ads` (skill `ads-report`, `ads-meta`, `ads-google`, `ads-tiktok`), `coreyhaines31/marketingskills` (skill `ads`), `mardab96/google-ads-skills`, `ComposioHQ/awesome-claude-skills` (competitive-ads-extractor, tidak relevan) |
| ClawHub / clawskills.sh | "clawhub skill meta ads report weekly performance ROAS" | `kein-s/meta-ads-report` (clawskills.sh), `amekala/adspirer-ads-agent` |
| skills.sh / anthropics/skills | ads report, ROAS | tidak ada skill resmi Anthropic untuk laporan iklan |

## Kandidat
| Skill | Bukti pemakaian | Isi | Relevansi |
|---|---|---|---|
| **marketingskills `ads`** (Corey Haines, MIT) https://github.com/coreyhaines31/marketingskills/blob/main/skills/ads/SKILL.md | ±51,4k bintang, 7,8k fork, v2.3.2 | Strategi iklan berbayar: metrik per tujuan, "Weekly Review" (pacing, CPA/ROAS vs target, top/bottom ads, frekuensi), pagar audit ("Never sum conversions across attribution windows", "No fixed kill rules… check sample size"). Tanpa script; "direct access to ad platform accounts" | **Paling populer**; bagian laporan mingguan hanya daftar periksa |
| **claude-ads `ads-report` + `ads-meta`** (AgriciDaniel, MIT) https://github.com/AgriciDaniel/claude-ads | ±9,5k bintang, 1,4k fork | Kerangka audit 12 platform; laporan dirender dari "validated JSON run bundle"; kontrak bukti, read-only, gerbang mutasi | Untuk agensi; laporan membutuhkan audit JSON lengkap lebih dulu |
| **meta-ads-report** (@kein-s) https://clawskills.sh/skills/kein-s-meta-ads-report | 0 unduhan | Meta Graph API dengan `META_ACCESS_TOKEN`; spend, konversi, CAC per ad set | Butuh token API. Tidak lolos syarat "terbukti" |

## Banding berdampingan (skenario 01: Meta WA, 6 iklan, minggu ini vs lalu)
Simulasi agent yang mengikuti **marketingskills `ads`**: agent lebih dulu menanyakan target CPA/ROAS dan anggaran ("Before Starting"), lalu menyusun "Weekly Review" dengan menghitung sendiri (LLM, tanpa script). Hasil yang wajar: total biaya benar (membaca tabel utuh, sel kosong = tidak ada hasil), frekuensi 241.430/141.900 ≈ 1,7 dicatat, Retargeting 0 chat disorot, Foto Produk (4 chat) "diselidiki dulu, sampel kecil" alih-alih langsung dimatikan. Kelemahannya: bahasa Inggris, USD/format asing, perhitungan CPA/CTR rawan rata-rata kolom (lihat `00-pembanding-tanpa-skill.md`), tanpa format tetap untuk Telegram, tanpa konteks Shopee/TikTok Shop.

**claude-ads:** tidak bisa menjalankan skenario ini langsung. `ads-report` menolak "loose worker prose" dan butuh bundle JSON dari `/ads audit` (setup klien, profil KPI, evidence). Untuk pemilik UMKM awam, alur ini terlalu berat.

| Kriteria (1–5) | marketingskills `ads` | claude-ads | laporan-iklan-mingguan (File-0) | laporan-iklan-mingguan (ekspor apa adanya) |
|---|---|---|---|---|
| Angka dihitung pasti (script, rumus tertulis) | 2 (LLM) | 4 (skor deterministik, tapi butuh audit) | 5 (0 beda) | 2 (total & arah salah) |
| Tahan bentuk ekspor nyata (sel kosong, baris Total, judul Google) | 3 (LLM membaca fleksibel) | 3 | 4 | 2 |
| Perbandingan minggu lalu | 3 | 3 | 5 | 2 |
| Saran berbasis angka + hati-hati | 4 (pagar sampel kecil, atribusi) | 4 | 3 (tanpa catatan sampel kecil) | 2 (iklan terburuk hilang) |
| Konteks Indonesia (Rp, Shopee, TikTok Shop, bahasa awam, Telegram) | 1 | 1 | 5 | 5 |
| Setup untuk awam | 3 (asumsi akses akun) | 1 | 5 | 5 |
| Keamanan (tanpa kredensial/jaringan) | 3 | 4 | 5 | 5 |
| **Total /35** | **19** | **20** | **32** | **23** |

## Yang bisa dipelajari (tanpa menyalin)
1. **Jangan menjumlah konversi lintas platform/atribusi** (marketingskills: "Meta 7-day + Google 30-day is not a total; report them side by side"). Mode `gabung` kita menjumlahkan "Conversions" TikTok + Google tanpa peringatan bila namanya sama (skenario 03).
2. **Tidak ada aturan "matikan" yang kaku.** Beri catatan sampel kecil (mis. < 10 hasil) sebelum menyarankan "matikan".
3. **Unknown ≠ 0.** Sel kosong di ekspor berarti "tidak ada nilai", bukan "baris rusak". Laporan wajib jujur tentang data yang tidak terbaca (claude-ads: "Never hide partial or insufficient-evidence status").

**Kesimpulan:** tidak ada pesaing publik yang setara untuk UMKM Indonesia (Rp, Shopee/TikTok Shop, bahasa awam, script pasti). Untuk file bersih, skill kita **menang jelas** (32 vs 20/19). Namun pada ekspor Meta apa adanya, nilainya turun ke 23 karena angka utamanya salah. Pesaing tidak unggul di total nilai, tetapi unggul di "tahan bentuk data" dan "kehati-hatian saran". **Skill kita tidak kalah dari pesaing.** Batas skor tetap ditentukan oleh A/B (maks. 6).
