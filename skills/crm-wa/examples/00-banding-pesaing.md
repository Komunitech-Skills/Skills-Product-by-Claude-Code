# 00 — Banding pesaing: skill/prompt CRM publik vs crm-wa (skenario 01)

Pesaing hanya **dibaca untuk dinilai**, tidak disalin. Tanggal riset: 24 Sep 2026.

## Pencarian
Kata kunci: "clawhub crm skill", "personal-crm OpenClaw", "skills.sh crm / sales pipeline / lead", "github agent skill personal CRM SKILL.md sqlite follow-up", "awesome-openclaw-skills marketing-and-sales".
Sumber: ClawHub, clawskills.sh, skills.sh, skills.lc, LobeHub (403), GitHub (awesome-openclaw-skills, claude-office-skills, awesome-claude-skills).

| Kandidat | Sumber | Bukti pemakaian | Sifat | Relevan untuk UMKM WA? |
|---|---|---|---|---|
| **personal-crm** (matthewpoe) | ClawHub (v1.1.0, MIT-0, diperbarui ±4 bulan lalu); skills.lc 562 instal | populer di kategorinya | CRM **relasi pribadi** di 2 file Markdown (NETWORK.md, NETWORK-ACTIVE.md), tier cadence mingguan/bulanan, ulang tahun, tanpa script | Paling mirip (lokal, tanpa API, tidak auto-kirim) → **dipakai untuk uji banding** |
| crm-automation (claude-office-skills) | GitHub, MIT, repo ±483★ | koleksi besar | Alur n8n/MCP untuk HubSpot/Salesforce/Pipedrive + Clearbit/OpenAI; Inggris/Mandarin | Tidak bisa jalan tanpa akun CRM berbayar & API key → gugur untuk skenario ini |
| lead-gen-crm (reighlan) | clawskills.sh | 0 unduhan | Prospek B2B via Brave/Hunter + HubSpot/Pipedrive/Zoho + SendGrid, email outreach | Butuh banyak API; email, bukan WA |
| pipeline-management (louisblythe/sales-skills) | skills.sh, 414 instal, repo 162★ | ada | Nasihat manajemen pipeline, tanpa penyimpanan data | Tidak mencatat apa pun |

URL: https://clawhub.ai/matthewpoe/personal-crm · https://skills.lc/openclaw/skills/openclaw-skills-skills-matthewpoe-personal-crm-skill-md · https://github.com/claude-office-skills/skills/blob/main/crm-automation/SKILL.md · https://clawskills.sh/skills/reighlan-lead-gen-crm · https://www.skills.sh/louisblythe/sales-skills/pipeline-management · https://github.com/VoltAgent/awesome-openclaw-skills/blob/main/categories/marketing-and-sales.md

Tidak ditemukan skill publik yang setara: CRM **penjualan** lokal berbasis chat WhatsApp, berbahasa Indonesia, dengan script hitungan.

## Uji banding skenario 01 (penguji menjalankan alur personal-crm sesuai rancangannya)
Pesan pemilik sama dengan skenario 01 (15 prospek, 10–24 Sep). Agent dengan personal-crm mencatat tiap orang sebagai entri YAML di NETWORK.md (nama, tier, riwayat obrolan) dan menyusun NETWORK-ACTIVE.md mingguan.

Hasil pada 24 Sep:
- "Siapa yang harus di-follow-up hari ini?" → agent memindai NETWORK-ACTIVE.md untuk kontak yang **melewati cadence tier-nya** (mis. tier "weekly"). Tidak ada konsep tahap penawaran/deal/batal, jadi prospek "ditawar, follow-up Jumat" diperlakukan seperti teman yang lama tidak disapa. Jadwal eksplisit ("follow-up 17/9", "25/9") tidak punya tempat baku.
- Pembuka obrolan hangat dan tanpa rasa bersalah (kelebihan pesaing), tapi bernada pertemanan ("Hai! Apa kabar?"), bukan follow-up penjualan berjenjang; tidak ada tautan wa.me.
- "Rekap bulan ini, sumber terbaik?" → **tidak didukung**: tidak ada nilai rupiah, tahap, konversi, win rate, sumber lead. Agent harus menghitung sendiri dari teks bebas.
- Nomor WA tidak dinormalisasi; tidak ada cek duplikat nomor (dua "Bu Sari" bergantung pada kehati-hatian agent).
- File Markdown 30 ribu kata dibaca model tiap kali → makin lambat/mahal seiring kontak bertambah; tidak ada cadangan otomatis.

## Skor berdampingan (penguji, 1–5)
| Kriteria | personal-crm | crm-wa |
|---|---|---|
| Cocok alur jualan chat → tawar → deal | 1 | 5 |
| Daftar follow-up berbasis jadwal nyata | 2 | 4 (S1) |
| Angka rekap (nilai, konversi, sumber) | 1 | 5 |
| Nomor WA, duplikat, tautan wa.me | 1 | 4 (S3 impor) |
| Nada pesan | 4 | 4 |
| Privasi & keamanan (lokal, tanpa auto-kirim) | 4 | 4 |
| Bahasa & konteks Indonesia | 1 | 5 |
| Tanpa setup / tanpa biaya | 5 | 4 (butuh Python; ada mode manual) |
| **Total** | **19/40** | **35/40** |

Kelebihan pesaing yang layak dipelajari (ditulis ulang dengan cara sendiri, bukan disalin): nada "tanpa rasa bersalah" dan pembuka yang merujuk obrolan terakhir; ringkasan mingguan (setara `rekap --periode minggu-lalu` yang sudah ada).

**Kesimpulan:** crm-wa **unggul jelas**; tidak ada pesaing publik setara untuk CRM penjualan WA lokal berbahasa Indonesia.
