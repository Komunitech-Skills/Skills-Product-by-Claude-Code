# Uji banding pesaing - Skenario 01 (ICBP)

> Penguji independen, 2026-09-29. Skill pesaing hanya **dibaca untuk dinilai**, tidak disalin.
> Pencarian: GitHub ("SKILL.md stock research", "equity research skill"), ClawHub ("stock analysis", "saham"), skills.sh, agent-skills.md.
> Tidak ditemukan skill riset saham khusus BEI/IDX berbahasa Indonesia.

## Pesaing yang dinilai
| Pesaing | Bukti pemakaian | Lisensi | Ringkas |
|---|---|---|---|
| tradermonty/claude-trading-skills -> `us-stock-analysis` | 2,9k bintang, 662 fork, 850 commit | MIT | Analisis fundamental/teknikal saham AS; laporan lengkap menghasilkan **"Buy/Hold/Sell rating", "Target price with timeframe", "Conviction level"**. Rasio dihitung LLM dari referensi definisi (tanpa script). Tanpa disclaimer di SKILL.md. |
| ClawHub `udiedrichsen/stock-analysis` v6.2.0 | skill populer ClawHub, MIT-0 | MIT-0 | Yahoo Finance, skor 8 dimensi -> **sinyal BUY/HOLD/SELL**, alert "signal change BUY->SELL"; "US markets only"; fitur sosial perlu kredensial X. |
| rollingSirius/equity-research-skill | 449 bintang, 57 fork | MIT | Laporan 9 bab US/HK/A-share, DCF script, verdict **undervalued/overvalued + action + position sizing**. Aturan sumber & timestamp kuat. |

## Skenario 01 dijalankan dengan pesaing terkuat untuk tugas ini (`us-stock-analysis`, alur "Fundamental Analysis")
Hasil penguji mengikuti SKILL.md pesaing (diringkas):
- Mencari data di Yahoo/Google Finance/Seeking Alpha; untuk ICBP (.JK) data Yahoo tersedia sebagian, berita Indonesia tidak dicakup instruksi.
- Menampilkan metrik (P/E TTM dari Yahoo, bukan dari LK interim), margin, dan "bull/bear case".
- Alur "Comprehensive report" mewajibkan **rating Buy/Hold/Sell + target harga** -> **melanggar aturan pemilik** (tidak ada rekomendasi/target).
- Tidak ada penanganan: laporan interim, satuan "dalam jutaan", format angka Indonesia, dividen cum/ex/recording BEI, konflik sumber, HARGA LAMA.

## Penilaian berdampingan (1-5)
| Kriteria | riset-saham-berita | us-stock-analysis (pesaing) |
|---|---|---|
| Kepatuhan aturan (tanpa rekomendasi/sinyal) | 5 | 1 |
| Akurasi angka (script Decimal, interim, rugi, ekuitas negatif) | 5 | 3 (LLM; bergantung data agregator) |
| Konteks Indonesia (BEI, OJK, dividen, Rupiah, bahasa) | 5 | 1 |
| Sumber + tanggal + tanda data basi | 5 | 3 ("verify recency") |
| Kedalaman analisis (valuasi, peer, teknikal) | 3 | 5 |
| Tanpa setup/API key | 5 | 3 (FMP opsional/wajib di skill lain) |
| **Total** | **28** | **16** |

**Kesimpulan:** skill kita unggul untuk pasar sasaran (awam Indonesia, BEI, aturan tanpa rekomendasi). Pesaing lebih dalam
di valuasi/peer comparison, tetapi keunggulan itu justru terlarang oleh aturan pemilik. Yang layak dipelajari (ditulis ulang
dengan cara sendiri, bukan disalin): (1) perbandingan **antar-emiten sejenis** dalam satu tabel rasio netral; (2) aturan
rollingSirius "setiap angka kunci punya sumber + timestamp" sudah setara di skill kita.
