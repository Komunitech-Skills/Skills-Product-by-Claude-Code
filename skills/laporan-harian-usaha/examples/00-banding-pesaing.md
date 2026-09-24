# Uji banding pesaing — skenario 01

**Penguji:** agent independen, 2026-09-24. Skill pesaing hanya **dibaca untuk dinilai**, tidak disalin atau dipasang (dua di antaranya ditandai "Suspicious" oleh pemindai ClawHub/VirusTotal).

## Pencarian
| Sumber | Kata kunci | Temuan |
|---|---|---|
| Web / clawskills.sh / ClawHub | "clawhub skill daily business report owner dashboard sales summary" | `visualdeptcreative/daily-report`, `mariusfit/oc-daily-business-report` |
| VoltAgent/awesome-openclaw-skills (52,8k bintang) | daily report, business report, sales summary, KPI, briefing | `ariktulcha/biz-reporter`, `daily-report`, `ai-daily-briefing` |
| GitHub / skills.sh / skills.lc | "claude skill daily sales report SKILL.md POS inventory small business", "openclaw skill shopify daily sales summary telegram owner" | `majiayu000/claude-skill-registry` commerce-inventory, `mardab96/ecommerce-claude-skills`, `sellerai-com/sellerclaw` owner-notifications |
| anthropics/skills | business report / sales | tidak ada skill laporan usaha |

## Kandidat yang dinilai
| Skill | Bukti pemakaian | Isi | Relevansi |
|---|---|---|---|
| **biz-reporter** (@ariktulcha, ClawHub, MIT-0, v1.0.0) https://clawhub.ai/ariktulcha/biz-reporter | 758 unduhan; clawskills.sh menandai "Suspicious" | Laporan KPI harian/mingguan/bulanan dari GA4, Search Console, Stripe, PayPal, HubSpot, Airtable, media sosial, CSV/Sheets; tandai anomali > 20%; jadwal cron ke Slack/Notion/email | **Paling dekat** (laporan harian + banding minggu lalu + jadwal). Tidak ada script; angka dirangkum LLM; butuh kredensial API |
| **daily-report** (@visualdeptcreative) https://clawskills.sh/skills/visualdeptcreative-daily-report | 3,6k unduhan; OpenClaw "Suspicious" | Laporan pagi/sore/mingguan untuk **pipeline lead generation** (jumlah lead, outreach, biaya); butuh Ollama + token bot Telegram | Domain lain (lead gen), bukan omzet/stok/karyawan |
| **oc-daily-business-report** (@mariusfit) https://clawskills.sh/skills/mariusfit-oc-daily-business-report | 345 unduhan; VirusTotal "Suspicious" | Cuaca, harga kripto, berita, kutipan, disk/RAM | Tidak menghitung penjualan, tidak relevan |
| **sellerclaw owner-notifications** (sellerai-com, MIT) https://skills.lc/sellerai-com/sellerclaw/… | 1 instal | Notifikasi Telegram ke pemilik toko Shopify dropship: order baru/terkirim/tertunda, saldo supplier | Terikat ke sistem SellerClaw + Shopify; tanpa kasir/stok lokal/absensi |

## Banding berdampingan (skenario 01, data Kedai Kopi Senja)
Simulasi agent yang mengikuti **biz-reporter** dengan sumber "Custom: CSV files / any API": tidak ada konektor untuk SQLite kasir/stok/absensi, sehingga agent menebak skema sendiri (hasilnya sama dengan "tanpa skill" di `00-pembanding-tanpa-skill.md`), lalu memformat "Daily KPI Snapshot" berbahasa Inggris dengan metrik web/Stripe yang kosong.

| Kriteria (bobot sama) | biz-reporter | laporan-harian-usaha |
|---|---|---|
| Sumber data cocok untuk UMKM Indonesia (kasir lokal, stok, absen, piutang) | 1/5 (Stripe/GA4/HubSpot) | 5/5 |
| Angka dihitung pasti (script, rumus tertulis) | 1/5 (LLM) | 5/5 (perintah resmi alat + rumus % eksplisit, cocok 100% dengan hitung manual) |
| Perbandingan periode | 3/5 (WoW, anomali 20%) | 5/5 (kemarin, hari yang sama minggu lalu, mingguan adil untuk minggu berjalan) |
| Masalah operasional (selisih kas, stok minus, lembur, piutang) | 1/5 | 5/5 |
| Privasi & keamanan data | 2/5 (kredensial API; ditandai suspicious) | 5/5 (hanya baca, tanpa internet, tanpa nama pelanggan, `--samarkan`) |
| Bahasa & konteks lokal (Rp, WIB, Telegram, PBJT) | 1/5 (Inggris, USD) | 5/5 |
| Setup untuk awam | 2/5 (kredensial beberapa layanan) | 4/5 (butuh Python + alat Komunitech di folder yang sama) |
| Kelebihan pesaing | Banyak sumber online, bulanan/YoY, rekomendasi strategis | Tidak ada (sengaja dibatasi alat lokal) |
| **Total** | **11/35** | **34/35** |

## Yang bisa dipelajari dari pesaing (tanpa menyalin)
- biz-reporter menandai **anomali otomatis** (mis. perubahan > 20%) dan laporan bulanan. Laporan kita menampilkan % tetapi tidak menandai "turun tajam" di PERLU PERHATIAN. Ide untuk versi berikut: butir perhatian bila omzet turun ≥ X% dari hari yang sama minggu lalu.

**Kesimpulan:** tidak ditemukan skill publik yang setara (laporan gabungan kasir + stok + absensi + piutang lokal untuk pemilik UMKM). Pesaing terdekat (biz-reporter) kalah jauh untuk target ini. **Skill kita tidak kalah.**
