# Uji banding pesaing: panduan-wawancara-kerja

- **Tanggal:** 2026-10-14
- **Penguji:** agent penguji independen Komunitech (bukan pembuat skill)
- **Cara uji:** skenario normal utama (pesan identik dengan skenario 1 di `00-openclaw-sebelum-sesudah.md`) dijalankan di OpenClaw 2026.10.2 lokal, model router Komunitech (`claude-sonnet-5`), di home terpisah `pwk-p1` yang berisi **hanya** skill pesaing. Hasil skill kita diambil dari sisi SESUDAH skenario 1 (lokal) di sesi yang sama.
- **Skill pesaing hanya dibaca untuk dinilai, tidak disalin** ke repo ini. Teksnya diunduh dari `raw.githubusercontent.com` ke folder uji sementara (scratchpad), dipasang di home uji, lalu dinilai. Tidak ada kalimat, templat, atau contoh pesaing yang dipakai di skill kita.

## Pencarian pesaing
Kata kunci (dari catatan riset kurator 2026-10-14, bagian 3): interview guide, structured interview, interview scorecard, interview rubric, hiring interview skill, panduan wawancara. Sumber: skills.sh (lewat pencarian web), ClawHub/getclawkit, prompts.chat, GitHub (raw). Tidak ditemukan skill agen berbahasa Indonesia untuk wawancara kerja.

| Pesaing | Pembuat / lisensi | Sinyal | Dijalankan? |
|---|---|---|---|
| **anthropics/knowledge-work-plugins `human-resources/skills/interview-prep`** (terkuat) | Anthropic, Apache-2.0 | repo ±29,6 rb bintang; ±2.786 instal (cermin skills.sh, akhir Jul 2026) | **Ya** (skenario 1) |
| mohitagw15856/pm-claude-skills `hiring-rubric` | MIT | repo ±1,4 rb bintang, ±1.285 skill (waspada slop) | Tidak, dinilai dari catatan riset |
| onewave-ai/claude-skills `hiring-scorecard` | MIT | 342 bintang, 172 instal | Tidak, dinilai dari catatan riset |

URL pesaing utama: https://github.com/anthropics/knowledge-work-plugins/tree/main/human-resources/skills/interview-prep

**Isi skill pesaing (ringkasan penguji, bukan kutipan):** SKILL.md ±1,4 KB, bahasa Inggris, generik: prinsip wawancara terstruktur, 4-6 kompetensi, 2-3 pertanyaan perilaku + 1-2 situasional + probe per kompetensi, skala 1-4 berdeskripsi, templat debrief, pembagian panel. Tanpa referensi, templat terpisah, script, bobot, aturan pertanyaan terlarang, atau konteks hukum Indonesia.

## Hasil skill pesaing (skenario 1)
Alat yang dipanggil: `skills_read` (SKILL.md pesaing), `write`. Paket disimpan sebagai berkas; chat hanya ringkasan.

**Jawaban di chat:**

> Paket wawancara lengkap sudah jadi — **Paket_Wawancara_Admin_OL_CS_RumahKerudungAlya.md** di workspace. Isinya:
>
> **1. Ringkasan posisi** — ditarik langsung dari iklan.
>
> **2. 5 kompetensi dinilai:**
> A. Kecakapan e-commerce (Shopee/TikTok) · B. Excel/Sheet & laporan · C. Fast response & CS · D. Ketelitian & kejujuran · E. Daya tahan kerja/lembur
>
> **3. Pembagian peran** — karena wawancara berdua, bukan gantian ruang tapi bagi fokus: kamu pegang teknis (e-commerce, Excel, jam kerja), adik pegang CS/kejujuran/kesan umum. Keduanya tetap isi scorecard sendiri → didiskusikan pas debrief.
>
> **4. Rundown 40 menit** per kandidat + contoh jadwal 4 orang mulai jam 09.00 dengan jeda 15 menit antar sesi buat isi scorecard.
>
> **5. Bank pertanyaan** — tiap kompetensi ada 2-4 pertanyaan behavioral + situasional + follow-up probe. Contoh konkret: "Pas promo ada 100+ chat masuk bareng, strategi kamu gimana biar nggak keteteran?"
>
> **6. Scorecard skala 1-4** per kompetensi dengan deskripsi tiap level, siap print/fotokopi 4x.
>
> **7. Template debrief** buat bandingkan 4 kandidat sekaligus setelah semua sesi selesai.
>
> **8. Tips praktis** — ada saran kecil: bawa contoh data order mentah buat tes "rapiin di Excel 5 menit", dan simulasi 2-3 chat WA customer biar lihat langsung gaya balas aslinya (lebih akurat daripada tanya doang).
>
> Catatan kecil: kriteria "berpenampilan menarik" dari iklan saya arahkan jadi penilaian kerapihan/representasi brand untuk live & foto produk — biar tetap relevan secara bisnis tanpa jadi penilaian fisik subjektif. Kalau mau diubah balik, bilang aja.

<details><summary>Isi berkas yang ditulis agent dengan skill pesaing (tidak tampil di chat)</summary>

````markdown
# Paket Wawancara — Admin OL Shop + CS WA
**Rumah Kerudung Alya — Bekasi Timur**
Dibuat: 14 Okt 2026 | Durasi per kandidat: 40 menit | Jumlah kandidat: 4 | Pewawancara: Owner + Adik (2 orang)

---

## 1. Ringkasan Posisi (dari iklan)

| Aspek | Detail |
|---|---|
| Kriteria dasar | Wanita, maks 28 th, jujur, teliti, fast respon |
| Tools | MS Excel / Google Sheet |
| Platform | Shopee & TikTok Shop (proses pesanan, cetak resi, chat pembeli) |
| CS | Balas chat WA customer (bisa 100+/hari saat promo) |
| Admin | Rekap orderan harian + stok, laporan penjualan mingguan |
| Jam kerja | Senin–Sabtu 08.00–16.00, lembur saat campaign tanggal kembar |
| Gaji | UMR + bonus |

## 2. Kompetensi yang Dinilai (5 kompetensi)

1. **Kecakapan E-commerce** — Shopee/TikTok Shop: proses pesanan, cetak resi, atur chat
2. **Excel / Google Sheet & Pelaporan** — rekap harian, stok, laporan mingguan
3. **Fast Response & Komunikasi CS** — kecepatan & kualitas balas chat volume tinggi
4. **Ketelitian & Kejujuran** — handling stok, retur, uang COD/transfer
5. **Daya Tahan Kerja & Fleksibilitas** — jam kerja panjang, lembur saat campaign

*(Catatan: kriteria "berpenampilan menarik" dari iklan sebaiknya dinilai lewat kerapihan & representasi brand saat live/foto produk, bukan penilaian fisik — biar aman dan tetap profesional. Sudah dimasukkan sebagai sub-poin di kompetensi #3.)*

---

## 3. Pembagian Panel (Owner + Adik)

Karena cuma berdua, wawancara dilakukan bareng (bukan gantian ruang), tapi **bagi fokus pertanyaan** biar efisien dan ada 2 sudut pandang:

| Pewawancara | Fokus Utama |
|---|---|
| **Owner (Kamu)** | Kompetensi #1 (E-commerce), #2 (Excel/Laporan), #5 (Jam kerja/lembur) — + keputusan akhir |
| **Adik** | Kompetensi #3 (Fast response/CS), #4 (Ketelitian/kejujuran), kesan umum & sikap |

Keduanya tetap isi scorecard sendiri-sendiri untuk semua kompetensi, lalu didiskusikan pas sesi debrief (lihat bagian 6).

---

## 4. Rundown 40 Menit per Kandidat

| Menit | Durasi | Agenda | PIC |
|---|---|---|---|
| 0–5 | 5' | Pembukaan, perkenalan, cairkan suasana | Owner |
| 5–15 | 10' | Pertanyaan teknis: e-commerce (Shopee/TikTok) + Excel | Owner |
| 15–25 | 10' | Pertanyaan CS & fast response | Adik |
| 25–32 | 7' | Ketelitian, kejujuran, jam kerja & lembur | Bergantian |
| 32–37 | 5' | Sesi tanya-jawab dari kandidat + info gaji/benefit | Owner |
| 37–40 | 3' | Closing, info timeline keputusan | Owner |

> Sisakan jeda 10–15 menit antar kandidat buat isi scorecard & diskusi kilat.

### Contoh Jadwal 4 Kandidat (mulai jam 09.00)
| Kandidat | Jam |
|---|---|
| Kandidat 1 | 09.00 – 09.40 |
| Kandidat 2 | 09.55 – 10.35 |
| Kandidat 3 | 10.50 – 11.30 |
| Kandidat 4 | 11.45 – 12.25 |

(Geser sesuai jadwal kandidat yang sebenarnya — tinggal kirim jam konfirmasi masing-masing.)

---

## 5. Bank Pertanyaan per Kompetensi

### A. Kecakapan E-commerce (Shopee & TikTok Shop)
*Behavioral:*
1. "Ceritakan pengalaman kamu pakai Seller Center Shopee atau TikTok Shop — bagian mana yang paling sering kamu kerjakan?"
2. "Pernah ada kejadian salah proses pesanan atau salah cetak resi? Gimana cara kamu benerinnya?"

*Situasional:*
3. "Kalau ada 50 pesanan masuk dan beberapa stoknya ternyata habis, apa langkah pertama yang kamu lakukan?"
4. "Gimana cara kamu memastikan resi yang dicetak nggak ketuker antar pesanan saat lagi ramai?"

*Follow-up probe:* "Pakai aplikasi/tools apa buat bantu kerja lebih cepat? (misal cetak resi massal, auto-reply, dll)"

### B. Excel / Google Sheet & Pelaporan
*Behavioral:*
1. "Fungsi/rumus Excel apa yang paling sering kamu pakai di kerjaan sebelumnya?"
2. "Ceritakan pengalaman bikin laporan mingguan atau rekap data — formatnya kayak gimana?"

*Situasional:*
3. "Misal saya kasih data orderan sebulan berantakan (beda format tanggal, ada yang dobel), gimana cara kamu rapihin jadi laporan yang enak dibaca?"
4. "Kalau diminta bikin rekap stok otomatis update tiap hari, kira-kira kamu akan pakai cara apa?"

*Follow-up probe:* "Pernah pakai Google Sheet buat kerja bareng tim (real-time)? Gimana pengalamannya?"

### C. Fast Response & Komunikasi CS
*Behavioral:*
1. "Ceritakan pengalaman kamu handle chat customer yang banyak banget dalam waktu bersamaan — gimana caranya tetap semua kebalas?"
2. "Pernah ketemu customer yang marah-marah atau komplain? Gimana cara kamu nanganin?"

*Situasional:*
3. "Pas lagi promo, ada 100+ chat masuk bareng dan semua nanya hal yang sama. Gimana strategi kamu biar nggak keteteran?"
4. "Kalau ada customer nanya di luar jam kerja (malam/weekend), apa yang biasanya kamu lakukan?"

*Follow-up probe:* "Gimana caranya kamu tetap ramah ke customer walau udah capek balas chat seharian?"
*Catatan representasi brand:* "Kalau diminta tampil di live Shopee/TikTok atau foto produk sesekali, kamu nyaman nggak? Pernah pengalaman serupa?"

### D. Ketelitian & Kejujuran
*Behavioral:*
1. "Pernah nggak nemu selisih stok atau uang yang nggak sesuai? Apa yang kamu lakukan?"
2. "Ceritakan momen kamu harus teliti banget supaya nggak ada kesalahan (misal input data, hitung uang, dll)."

*Situasional:*
3. "Misal kamu sadar ada kesalahan input yang bikin laporan ke owner jadi salah, dan belum ada yang nyadar — apa yang kamu lakukan?"
4. "Kalau ketemu barang retur yang kondisinya beda dari laporan customer, gimana cara kamu melaporkannya ke saya?"

### E. Daya Tahan Kerja & Fleksibilitas
*Behavioral:*
1. "Gimana pengalaman kamu kerja dengan jam yang panjang atau lembur mendadak?"

*Situasional:*
2. "Jam kerja di sini Senin–Sabtu 08.00–16.00, dan pas tanggal kembar (campaign) biasanya lembur. Gimana kesiapan kamu soal ini?"
3. "Kalau H-1 campaign besar dan diminta lembur sampai malam, gimana responmu?"

---

## 6. Scorecard (isi per kandidat, skala 1–4)

**Nama Kandidat:** _______________  **Tanggal/Jam:** _______________  **Pewawancara:** _______________

| Kompetensi | 1 (Kurang) | 2 (Cukup) | 3 (Baik) | 4 (Sangat Baik) | Skor |
|---|---|---|---|---|---|
| A. Kecakapan E-commerce | Belum paham Shopee/TikTok sama sekali | Paham dasar, butuh diajari banyak | Sudah biasa pakai, minim kesalahan | Mahir, bisa kasih solusi efisiensi | ___ |
| B. Excel/Sheet & Laporan | Belum bisa Excel/Sheet | Bisa dasar (input, sort) | Bisa rumus dasar & bikin rekap rapi | Mahir rumus, bisa bikin laporan otomatis | ___ |
| C. Fast Response & CS | Lambat, jawaban kaku | Cukup responsif, kadang telat | Cepat & ramah, bisa handle volume tinggi | Sangat cepat, tenang di tekanan, komunikatif | ___ |
| D. Ketelitian & Kejujuran | Ragu-ragu/jawaban tidak konsisten | Cukup jujur tapi kurang detail | Jujur & cukup teliti, ada bukti konkret | Sangat jujur & detail, ada contoh kuat | ___ |
| E. Daya Tahan & Fleksibilitas | Keberatan jam kerja/lembur | Bisa tapi ragu-ragu | Siap dan terbiasa | Sangat siap, pernah sukses di kondisi serupa | ___ |

**Total Skor (maks 20):** ___

**Catatan tambahan (kesan umum, red flag, kecocokan budaya kerja):**
_______________________________________________

**Rekomendasi:** ☐ Lanjut/Terima ☐ Pertimbangkan ☐ Tolak

---

## 7. Template Debrief (setelah semua 4 kandidat selesai)

Isi bareng Owner + Adik, bandingkan 4 kandidat dalam satu tabel:

| Kandidat | Skor Owner | Skor Adik | Total Rata-rata | Kelebihan | Kekurangan | Keputusan |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |

**Pertanyaan pemandu diskusi:**
- Siapa yang paling kuat di sisi teknis (Excel + Shopee/TikTok)?
- Siapa yang paling meyakinkan soal kecepatan & keramahan balas chat?
- Ada yang terasa ragu-ragu soal jam kerja/lembur campaign? Ini bisa jadi masalah besar ke depan.
- Kalau ada 2 kandidat skornya mirip, siapa yang lebih cocok sama budaya kerja toko (misalnya: lebih teliti vs lebih cepat)?

**Keputusan akhir:** _______________ (isi setelah diskusi, idealnya maks H+1 setelah wawancara biar kandidat nggak nunggu lama)

---

## 8. Tips Praktis Hari-H

- Siapkan laptop/HP + screenshot contoh tampilan Seller Center Shopee/TikTok buat tes langsung "coba cari menu X" kalau mau lihat kecakapan nyata, bukan cuma ngaku-ngaku.
- Siapkan 1 contoh data mentah (order list acak) buat tes cepat "coba rapiin di Excel" — bisa kasih waktu 5 menit, lihat caranya mikir.
- Kalau mau, simulasikan 2-3 chat WA customer (komplain, nanya stok, nego harga) dan minta kandidat balas langsung di depan kalian — paling efektif menilai fast response & nada bicara aslinya.
- Jangan lupa infokan di akhir: kapan kandidat bisa mulai kerja, dan kapan keputusan dikabari (biar nggak gantung).
````
</details>

## Penilaian berdampingan (skenario 1, iklan admin OL shop + CS WA)

| Kriteria | Pesaing `interview-prep` | Skill kita `panduan-wawancara-kerja` |
|---|---|---|
| Paket utuh di chat (siap tempel/cetak) | Tidak: hanya ringkasan, isi di berkas workspace | Ya, utuh di chat |
| Syarat diskriminatif di iklan ("wanita, maks. 28, berpenampilan menarik") | **Dipakai**: "Wanita, maks 28 th" ditulis sebagai *kriteria dasar*; "penampilan menarik" diubah jadi pertanyaan nyaman tampil live/foto produk (tugas yang tidak ada di iklan) | Disebut tidak dipakai dalam 1 kalimat; diganti pertanyaan sah di tabel "tidak boleh ditanyakan" |
| Kompetensi + bobot + kritis | 5 kompetensi, tanpa bobot | 5 kompetensi, bobot 30/25/20/15/10, 2 kritis |
| Tanda jawaban kuat/lemah per pertanyaan | Tidak ada (hanya probe) | Ada di setiap pertanyaan + pertanyaan lanjutan |
| Rubrik | Skala 1-4 dengan deskripsi singkat per tingkat (baik) | Skala 1-5, lima tingkat berupa perilaku teramati |
| Tes praktik berkunci | Tidak ada (hanya tips "rapikan data 5 menit", tanpa data/kunci) | Ada, data contoh + kunci (30 pesanan; kurang 3 pcs) - angka benar |
| Alur waktu | 5+10+10+7+5+3 = 40, benar; plus jadwal 4 kandidat dengan jeda 15 menit | 4+10+5x4+4+2 = 40, benar (dihitung) |
| Pertanyaan terlarang + dasar aturan | Tidak ada | Tabel + UU 13/2003 Pasal 5-6, SE Menaker M/6/HK.04/V/2025, UU 27/2022, bertanggal + PERLU REVIEW |
| Setelah wawancara | Templat debrief (skor owner/adik, rata-rata manual) | Hitung total tertimbang, selisih > 1,5, peringkat, saran (terbukti di skenario 5) |
| Fakta karangan | Tugas live/foto produk tidak ada di iklan | `[isian]` untuk yang tidak diberikan |
| **Nilai** | **5,0** | **8,5** |

**Verdik banding: skill kita unggul jelas (8,5 vs 5,0).** Skill pesaing tidak mengenali syarat diskriminatif khas iklan Indonesia dan malah memasukkannya ke ringkasan posisi, tidak memberi bobot/kunci/tanda jawaban, dan hasilnya tidak di chat.

**Kelebihan pesaing yang patut dipelajari (ditulis ulang dengan cara sendiri bila dipakai):**
- Contoh jadwal untuk beberapa kandidat sekaligus dengan jeda isi kartu skor di antara sesi (pengguna menyebut "4 pelamar"; skill kita tidak memanfaatkan info itu).
- Pembagian fokus per pewawancara yang eksplisit dan pertanyaan pemandu debrief.
- Rubrik satu tabel ringkas yang mudah dicetak.

**Pesaing lain (dari catatan riset, tidak dijalankan):** `hiring-rubric` (MIT) punya aturan rekomendasi tetap dan penanganan input kurang, tetapi tanpa pertanyaan terlarang dan tanpa agregasi lintas pewawancara. `hiring-scorecard` (MIT) satu-satunya yang menyebut agregasi skor panel lewat kalkulator dan matriks penilaian independen, tetapi tanpa daftar pertanyaan terlarang dan tanpa konteks Indonesia. Keduanya tidak diuji langsung, jadi tidak diberi nilai.
