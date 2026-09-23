# 00 — Uji banding pesaing (S1)

## Pencarian
- Kata kunci: "follow-up sequence SKILL.md", "sales follow-up", "no reply prospect", "ghosting", "cold email sequence", "follow up WhatsApp".
- Sumber dicek: github.com/VoltAgent/awesome-openclaw-skills (email-manager-ai, cold-email, action-suggester, meeting-autopilot — halaman ClawHub/clawskills.sh **diblokir proxy**, isi tidak terbaca), github.com/anthropics/skills (tidak ada), manairalabs/bicara-skills (hanya `wa-reply-id` untuk balas CS), alvinindra/bahasa-skills (gaya bahasa umum), pencarian web GitHub.
- Temuan yang terbaca & paling sebanding: **`sales-followup`** — github.com/zubair-trabzada/ai-sales-team-claude (skills/sales-followup/SKILL.md), lisensi **MIT**. Punya skenario post-meeting, post-demo, post-proposal, ghost recovery, nurture.
- Script pihak ketiga tidak dijalankan; isi tidak disalin.

## Input S1 (sama)
> Kemarin (22 Sept) saya demo aplikasi kasir KasirPintar Fiktif ke Pak Joni, pemilik Resto Padang Rasa Minang Fiktif di Depok. Paket 199rb/bulan, gratis setup. Dia mau diskusi dulu sama istrinya yang pegang keuangan. Dia nanya soal printer Epson TM-U220 — bisa. Nama saya Rudi. Bikinin follow-up WA ya.

## Output dengan instruksi pesaing (`sales-followup`, disimulasikan)
Instruksi pesaing: kumpulkan 10 data konteks (minimal 3 poin diskusi, pain point, temperatur, tahap deal…), pilih "Scenario 2: Post-Demo (4 emails)" dengan jadwal hari 0 / +3 / +5 / +7 (kumulatif hari 0, 3, 8, 15), tiap email 60–100 kata + subjek, ditambah aksi LinkedIn, 2 naskah voicemail, 2–3 SMS, kalender kadensi; tulis ke FOLLOWUP-SEQUENCE.md.
```
# Follow-Up Sequence: Pak Joni — Resto Padang Rasa Minang Fiktif
Scenario: Post-Demo · Temperature: Warm · Deal Stage: Active evaluation

Email 1 (Day 0) — Subject: "Struk langsung dari Epson TM-U220 + langkah berikutnya"
Pak Joni, terima kasih atas waktunya. Bagian yang paling Bapak perhatikan tadi adalah cetak struk
ke printer lama — itu sudah didukung penuh. Ringkasan: • Rp199.000/bulan • setup gratis • laporan
harian. Pertanyaan apa yang muncul setelah demo?

Email 2 (Day 3) — Subject: "Soal biaya bulanan"  [Feel-Felt-Found: "Pemilik resto lain juga
merasa…, yang mereka temukan…"] + tawaran bicara dengan pelanggan referensi.
Email 3 (Day 8) — Subject: "[Resto serupa] mencapai [hasil]" — studi kasus resto serupa.
Email 4 (Day 15) — Subject: "Timeline keputusan" — tanya prioritas kuartal ini, tawarkan ringkasan 1 halaman.

LinkedIn: lihat profil Pak Joni, komentari postingannya…
Voicemail 1 & 2 (≤ 30 detik) · SMS 1–3 (hanya bila opt-in)
Cadence calendar: Day 0 email, Day 1 LinkedIn, Day 3 email, …
```
Catatan simulasi: pesaing melarang placeholder `[...]` di output akhir, sehingga studi kasus/hasil resto serupa berisiko dikarang bila pengguna tidak memberikannya.

## Output dengan skill kita
Lihat `01-setelah-demo-aplikasi-kasir.md` (4 pesan WA bertanggal dari script, aturan main, bank balasan, asumsi).

## Penilaian

| Kriteria | Pesaing (`sales-followup`) | Skill kita |
|---|---|---|
| Kualitas pesan | Kuat secara teknik (tiap email bernilai baru, Feel-Felt-Found, breakup email) | Setara dalam prinsip (tujuan berbeda tiap pesan, pamit sopan), lebih ringkas |
| Konteks Indonesia | Email + LinkedIn + SMS + voicemail — tidak cocok untuk pemilik resto yang hidup di WhatsApp; jam kirim gaya AS; tidak tahu salat Jumat/libur | WA-first, sapaan Bapak/Ibu/Kak, jam kirim lokal, UU PDP |
| Akurasi | Tanggal relatif ("Day 3"), tidak menggeser akhir pekan/libur; risiko mengarang studi kasus karena larangan placeholder | Tanggal pasti dari script, geser akhir pekan/libur; klaim tak diberikan ditandai "usulan" |
| Siap pakai | Banyak bagian tidak terpakai (LinkedIn/voicemail) | Siap salin-kirim |
| **Total** | Kalah untuk pasar sasaran | **Menang** |

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
1. **Matriks kadensi berdasarkan "temperatur" prospek** (panas/hangat/dingin) — bisa menjadi pilihan `--hari` otomatis di SKILL.md.
2. **Naskah telepon/voice note singkat** — di Indonesia voice note WA lazim; satu naskah VN 20–30 detik untuk pesan ke-3 bisa menambah nilai.
3. **Kerangka menjawab keberatan "rasa–pernah merasa–ternyata"** untuk pesan ke-2 setelah demo.
4. Aturan tegas **"jangan pernah kirim pesan 'cuma mau follow up' tanpa nilai baru"** — sudah tersirat di skill kita, bisa dijadikan butir checklist eksplisit.
