# 00 — Uji banding pesaing (S1)

## Pencarian
- Kata kunci: "partnership proposal", "sponsorship proposal", "sales proposal SKILL.md", "consignment", "reseller program", "proposal kerjasama".
- Sumber dicek: github.com/VoltAgent/awesome-openclaw-skills (freelance-proposal-engine, simple-proposal-template-v2, business-development — halaman ClawHub/clawskills.sh **diblokir proxy** sehingga isinya tidak terbaca), github.com/anthropics/skills (tidak ada), manairalabs/bicara-skills & alvinindra/bahasa-skills (tidak ada skill proposal), pencarian web GitHub.
- Temuan yang terbaca:
  - **`sales-proposal`** — github.com/zubair-trabzada/ai-sales-team-claude, lisensi **MIT**. Paling sebanding (generator proposal lengkap). Dipakai untuk simulasi.
  - `partnerships-architect` — github.com/borghei/Claude-Skills, lisensi **MIT + Commons Clause** (tidak boleh dijual ulang); fokus strategi program kemitraan korporat, bukan menulis proposal. Hanya dibaca sebagai referensi.
  - `quote-drafter` — Ootto-AI/claude-invoice-skills (MIT); lebih ke penawaran harga.
- Script pihak ketiga tidak dijalankan; isi tidak disalin.

## Input S1 (sama)
> Usaha sambal botol "Sambal Bu Tatik Fiktif" (Malang, 2 tahun), mau titip jual di Toko Oleh-oleh Pusaka Fiktif (3 cabang di Batu). Harga jual 35rb/botol, toko ambil 25%. Modal 18rb. Proposal singkat 1 halaman.

## Output dengan instruksi pesaing (`sales-proposal`, disimulasikan)
Instruksi pesaing: wajib mengumpulkan 8 input (termasuk minimal 3 pain point, model engagement, budget, timeline, **2–3 studi kasus dengan hasil terukur**) dan "jangan membuat proposal bila input kritis kurang"; 11 bagian; harga 3 tingkat Good-Better-Best dengan tingkat tengah "RECOMMENDED"; setiap harga wajib disertai ROI; ringkasan eksekutif ditutup dengan urgensi; ditulis ke file PROPOSAL-*.md.
```
Sebelum saya menyusun proposal, saya perlu beberapa informasi:
1. Nama lengkap/legal Toko Oleh-oleh Pusaka dan model bisnisnya
2. Minimal 3 masalah/tantangan yang dihadapi Pusaka yang akan diselesaikan proposal ini
3. Model kerja sama (retainer, proyek, berbasis kinerja, hybrid)
4. Kisaran anggaran Pusaka
5. Timeline mulai & milestone
6. 2–3 studi kasus kerja sama serupa dengan hasil terukur
(Opsional: pengambil keputusan, pesaing yang sedang dipertimbangkan, alasan urgensi)
```
Jika pengguna tidak punya studi kasus dan tetap meminta draf, struktur yang dihasilkan: sampul → ringkasan eksekutif 5 paragraf (termasuk "urgensi") → analisis situasi → solusi 3 fase → lingkup kerja → timeline → **tabel investasi 3 tingkat** (mis. "Starter 1 cabang / Growth 3 cabang ★ / Premium 3 cabang + display eksklusif") dengan "ROI 12 bulan" → proyeksi ROI → tim → studi kasus → langkah berikut; panjang ± 8–12 halaman. Tidak ada aturan menyembunyikan modal produsen, dan prinsip "anchor every price to ROI" mendorong mencantumkan margin.

## Output dengan skill kita
Lihat `01-titip-jual-sambal-ke-toko-oleh-oleh.md` (± 300 kata, tabel pendapatan toko per cabang dari script, modal dipisah, WA + email).

## Penilaian

| Kriteria | Pesaing (`sales-proposal`) | Skill kita |
|---|---|---|
| Kualitas untuk kasus ini | Terlalu berat untuk titip jual UMKM; menolak jalan tanpa studi kasus; tiga tingkat harga tidak cocok untuk konsinyasi | Tepat sasaran: menjawab "dapat berapa, repot tidak, kalau tidak laku bagaimana" |
| Konteks Indonesia | Gaya enterprise AS (retainer, ROI, Q-planning); tidak mengenal konsinyasi, meterai, izin PIRT/BPOM, WA | Kerangka konsinyasi/reseller/sponsorship lokal, WA, meterai, UU PDP |
| Akurasi | Tidak ada perhitungan terstruktur (ROI dikira-kira) | Script (rumus benar; ada bug parser koma — lihat HASIL-UJI) |
| Siap pakai | Butuh banyak input & penyuntingan | Siap kirim + pesan pengantar |
| **Total** | Kalah | **Menang** |

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
1. **Memakai bahasa mitra sendiri** (frasa yang mitra ucapkan saat ngobrol) di ringkasan — tambahkan pertanyaan opsional "apa yang pernah dikeluhkan/diinginkan mitra?".
2. **Bagian asumsi eksplisit di bawah tabel simulasi** (dasar angka penjualan per bulan) — kita menulis asumsi di akhir; bisa dipindah tepat di bawah tabel agar mitra tidak menganggapnya janji.
3. **Rangkaian follow-up setelah proposal terkirim** (hari 2/5/7/14) — bisa dirujuk ke skill `follow-up-prospek` di langkah terakhir.
