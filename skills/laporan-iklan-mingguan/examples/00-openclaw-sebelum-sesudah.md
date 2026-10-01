# Uji OpenClaw SEBELUM vs SESUDAH — laporan-iklan-mingguan

## Cara uji
- **Tanggal:** 2026-10-01. Penguji independen Komunitech (bukan pembuat skill); folder skill hanya dibaca, tidak diubah.
- **Agent:** OpenClaw **2026.9.6** lokal (`openclaw agent --local`, tanpa Telegram/gateway), model router Komunitech **claude-sonnet-5** (sama dengan bot member), TZ Asia/Jakarta.
- **SEBELUM** = home OpenClaw bersih **tanpa skill**; **SESUDAH** = home bersih berisi **hanya skill ini**. Home dibuat ulang per skenario; file data fiktif identik disalin ke workspace kedua home. Pesan identik di kedua sisi; pertanyaan balik agent dijawab sekali dengan jawaban yang sama.
- Catatan teknis: home `s-*` di folder uji bersama sempat dihapus oleh proses penguji lain yang berjalan paralel (`rm -rf homes/s-*`), sehingga beberapa giliran gagal dan diulang dengan home bernama unik (`u6s-…`/`u6k-…`, isi sama). Balasan yang dikutip di bawah adalah giliran yang berjalan utuh.
- Angka diverifikasi ulang dengan Python secara independen (dan dengan script skill sebagai pembanding bila relevan); fakta aturan dicek terhadap aturan Indonesia yang berlaku.

## Skenario 1 — Normal: ekspor Meta Ads minggu ini vs minggu lalu + omzet

**Pesan pengguna:**

> Min ini ekspor iklan FB/IG minggu ini (meta-minggu-ini.csv) sama minggu lalu (meta-minggu-lalu.csv). Tolong bikinin laporan mingguan yg gampang dibaca, hasilnya itu chat WA masuk. Omzet toko minggu ini 18,5 jt. Iklan mana yg mending dimatiin?

### Balasan SEBELUM (tanpa skill)

*tools: ls, read*

> *LAPORAN IKLAN FB/IG MINGGUAN*
> Periode: 21–27 Sep 2026 vs 14–20 Sep 2026
>
> *RINGKASAN UTAMA*
> - Total spend minggu ini: Rp4.200.000 (naik 40% dari Rp3.000.000 minggu lalu)
> - Total hasil chat WA masuk: 114 (naik dari 93, +23%)
> - Tapi biaya per hasil (CPR) gabungan malah naik dari ~Rp19.900 jadi ~Rp25.900 → iklan jadi lebih boros, 1 campaign baru yang "makan" budget tanpa hasil sebanding
> - Omzet minggu ini Rp18.500.000, spend iklan = 22,7% dari omzet (lumayan tinggi, perlu dijaga)
>
> *DETAIL PER CAMPAIGN*
>
> 1. *WA - Promo Gamis* (Sep→Okt)
>    Rp1.300.000→Rp1.250.000 | Hasil 52→64 | CPR Rp25.000→Rp19.531
>    📈 Makin efisien, hasil naik, biaya turun. Pertahankan, bisa naikkan budget.
>
> 2. *WA - Retarget Pengunjung*
>    Rp550.000→Rp600.000 | Hasil 41→38 | CPR Rp13.415→Rp15.789
>    ✅ Tetap campaign termurah per hasil meski naik dikit. Pertahankan.
>
> 3. *Traffic - Katalog IG*
>    Rp700.000→Rp850.000 | Klik 2.410→2.950 | Biaya/klik stabil ~Rp288
>    ➖ Performa konsisten, cuma tidak ada data konversi chat. Oke dilanjut untuk dorong trafik katalog.
>
> 4. *WA - Hijab Instan Baru* (campaign baru minggu ini)
>    Rp1.100.000 | Hasil cuma 12 | CPR Rp91.667
>    🔴 Paling boros jauh — hampir 5x lipat CPR campaign lain. Ini biang keladi naiknya biaya minggu ini.
>
> 5. *Awareness - Video Reels*
>    Rp450.000→Rp400.000 | Reach 161rb→150rb | CTR cuma 0,3%
>    ⚠️ Engagement rendah, tapi ini tipe awareness (bukan buat hasil chat langsung). Boleh dikecilin kalau mau hemat.
>
> *REKOMENDASI: IKLAN YANG SEBAIKNYA DIMATIKAN*
> 🔴 *"WA - Hijab Instan Baru"* — matikan atau revisi total dulu (ganti foto/copy/target audiens). Spend Rp1,1 juta cuma hasilkan 12 chat, CPR Rp91.667 itu 5x lebih mahal dari Promo Gamis.
>
> Kalau butuh potong budget lagi, kandidat kedua: *Awareness Video Reels* (turunkan budget, bukan matikan total, karena fungsinya beda untuk brand awareness).
>
> Sisa budget dari "Hijab Instan Baru" lebih baik dialihkan ke *Promo Gamis* atau *Retarget Pengunjung* yang CPR-nya jauh lebih murah dan sedang tren membaik.

### Balasan SESUDAH (dengan skill)

*tools: read, ls, exec (skill terpakai: `laporan_iklan.py analisis … --sebelumnya … --omzet`)*

> Ini laporan iklan Meta (FB/IG) minggu ini vs minggu lalu, sudah dibandingkan sama omzet toko Rp18,5 jt:
>
> *LAPORAN IKLAN MINGGUAN — Meta Ads (FB/IG)*
> Periode: 21–27 Sep 2026
>
> Total belanja iklan: *Rp 4.200.000*
> Tayangan: 535.500 | Klik: 6.400 | Pesan WA masuk: 114
> CPC: Rp 656 | CPM: Rp 7.843 | CTR: 1,2%
> Biaya per pesan WA: *Rp 36.842*
> Biaya iklan vs omzet: 22,7% dari omzet Rp 18.500.000
>
> *VS MINGGU LALU*
> - Biaya iklan: Rp 4.200.000 (naik 40,0% dari Rp 3.000.000)
> - Pesan WA: 114 (naik 22,6% dari 93)
> - Biaya per pesan WA: Rp 36.842 (naik 14,2% dari Rp 32.258)
> → Minggu ini lebih boros, tapi hasilnya juga lebih banyak. Efisiensi sedikit turun.
>
> *PALING OKE* 🏆
> 1. WA - Retarget Pengunjung: Rp 15.789/pesan (38 pesan, Rp 600rb)
> 2. WA - Promo Gamis Oktober: Rp 19.531/pesan (64 pesan, Rp 1,25jt)
>
> *PERLU DIPERHATIKAN* ⚠️
> 1. Traffic - Katalog IG: Rp 850.000 habis, 0 pesan WA
> 2. Awareness - Video Reels: Rp 400.000 habis, 0 pesan WA
> 3. WA - Hijab Instan Baru: Rp 91.667/pesan (cuma 12 pesan, Rp 1,1jt) — 2,5x lebih mahal dari rata-rata
>
> *Iklan mana yang mending dimatiin?*
> 1. *Traffic - Katalog IG* — udah habis Rp850rb, 0 pesan WA sama sekali, nggak jelas hasilnya kemana.
> 2. *Awareness - Video Reels* — habis Rp400rb, 0 pesan WA juga, sama-sama nggak nyumbang hasil.
> 3. *WA - Hijab Instan Baru* — hasilnya ada tapi mahal banget (Rp91.667/pesan, 2,5x rata-rata). Kalau mau dipertahankan, coba ganti materi/gambar dulu sebelum lanjut.
>
> Sebaliknya, *WA - Retarget Pengunjung* paling murah dan efisien — ini yang layak ditambah budgetnya.
>
> Catatan kecil:
> - Biaya di atas belum termasuk PPN platform, jadi cek invoice Meta — persentase vs omzet bisa sedikit lebih tinggi dari 22,7%.
> - Ada 2 iklan yang kolom "Results"-nya kosong (dihitung 0, bukan error) — itu Traffic-Katalog IG & Awareness-Video Reels.

### Verifikasi

Data fiktif: 5 kampanye minggu ini (total Rp4.200.000; tayangan 535.500; klik 6.400; hasil 114), 4 kampanye minggu lalu (Rp3.000.000; hasil 93); 2 kampanye bersel `Results` kosong.
Python independen: CPC 4.200.000/6.400 = 656,25 → Rp656; CPM = 7.843,1 → Rp7.843; CTR 1,195% → 1,2%; biaya/hasil 36.842,1 → Rp36.842; minggu lalu 32.258,1; naik 14,21%; biaya vs omzet 22,70%. Hijab Instan 91.667 = 2,49× rata-rata. **Semua angka SESUDAH benar** dan identik dengan keluaran script.
SEBELUM: angka per kampanye benar, tetapi "CPR gabungan ~Rp19.900 → ~Rp25.900" ternyata hanya kampanye WA (Rp1.850.000/93 dan Rp2.950.000/114) tanpa disebut; biaya per hasil seluruh belanja sebenarnya Rp32.258 → Rp36.842. Tidak ada CPC/CPM/CTR total.
Catatan SESUDAH: agent menyarankan mematikan kampanye *Traffic* dan *Awareness* karena "0 pesan WA" — ambang skill tidak mempertimbangkan tujuan kampanye (SEBELUM justru membedakannya). Bagian "Kolom dibaca: …" dari Catatan script tidak ikut disampaikan.

### Skor

| Kriteria | SEBELUM | SESUDAH |
|---|---|---|
| Ketepatan angka | 6 | 10 |
| Siap pakai (format laporan) | 7 | 9 |
| Penilaian/saran | 8 | 7 |
| Kejelasan | 8 | 9 |
| **Skor** | **7** | **8,5** |

Skill terpakai (ya).

## Skenario 2 — Jebakan: ekspor berbiaya USD, pengguna minta "langsung aja" dalam rupiah

**Pesan pengguna:**

> ini laporan iklan FB minggu ini (iklan-fb-minggu-ini.csv), usaha jasa renovasi rumah. Berapa biaya per lead nya dalam rupiah? yg minggu lalu gak ada filenya. langsung aja ya

### Balasan SEBELUM (tanpa skill)

*tools: exec, read*

> Berikut hasil analisis **iklan-fb-minggu-ini.csv** (periode 21–27 Sep 2026), kurs USD→IDR: **1 USD = Rp17.891** (Frankfurter, 30 Sep 2026):
>
> **Biaya per lead per campaign:**
> - Lead Form - Konsultasi Gratis: $3.88 → **Rp69.417** (47 lead, spend $182,40)
> - Lead Form - Promo Renovasi: $10.57 → **Rp189.108** (9 lead, spend $95,10)
> - Traffic - Website: 0 lead (bukan campaign lead gen, dikecualikan dari hitungan)
>
> **Blended cost per lead (2 campaign lead gen):**
> Total spend $277,50 ÷ 56 lead = $4,96 → **≈ Rp88.656/lead**
>
> Catatan: file minggu lalu tidak ditemukan, jadi tidak bisa dibandingkan week-over-week. Campaign "Promo Renovasi" jauh lebih mahal per lead-nya (hampir 3x) dibanding "Konsultasi Gratis" — mungkin layak dicek kreatif/targeting-nya.

### Balasan SESUDAH (dengan skill)

*Giliran 1 — tools: read, exec (script berhenti karena mata uang bukan IDR)*

> File CSV-nya (`iklan-fb-minggu-ini.csv`) ternyata pakai mata uang **USD** (kolom "Amount spent (USD)"), bukan Rupiah — jadi saya tidak bisa langsung hitung, nanti angkanya salah kalau saya tebak kursnya sendiri.
>
> Boleh kasih tahu kurs yang mau dipakai (1 USD = berapa Rupiah)? Atau kalau ternyata angka di file itu sebenarnya sudah Rupiah (cuma label kolomnya salah tulis USD), bilang aja dan saya proses sebagai IDR langsung.

*Giliran 2 — jawaban pengguna: "pake kurs 16.700 aja, itu yg di tagihan kartu kredit saya" — tools: exec*

> Biaya per lead minggu ini: **Rp 100.647/lead** (total belanja Rp 5.636.250 ÷ 56 lead, kurs 1 USD = Rp 16.700 dari tagihan kartu kredit kamu).
>
> Rincian per kampanye:
> - Lead Form - Konsultasi Gratis: Rp 64.810/lead (47 lead) — paling murah
> - Lead Form - Promo Renovasi: Rp 176.463/lead (9 lead) — mahal
> - Traffic - Website: Rp 1.002.000 habis, 0 lead — sia-sia, pertimbangkan matikan
>
> Gak ada pembanding minggu lalu karena filenya memang nggak ada, jadi belum bisa bilang naik/turun dari minggu sebelumnya.

### Verifikasi

Kolom file: `Amount spent (USD)`; total $337,50, lead 47 + 9 + 0.
- SEBELUM mengambil kurs dari internet sendiri (Rp17.891, "Frankfurter") **tanpa bertanya**, lalu membulatkan USD sebelum dikalikan (Rp69.417 vs persis 69.432; Rp189.108 vs 189.048) dan menghitung CPL gabungan hanya dari 2 kampanye (Rp88.656) — belanja Traffic $60 dikeluarkan. Kurs ini berbeda dari kurs tagihan kartu pengguna, jadi angka rupiahnya tidak cocok dengan pengeluaran nyata.
- SESUDAH menolak menebak kurs, lalu dengan kurs pengguna 16.700: total $337,50 × 16.700 = Rp5.636.250 ✔; CPL 5.636.250/56 = 100.647,3 → Rp100.647 ✔; 182,40×16.700/47 = Rp64.810 ✔; 95,10×16.700/9 = Rp176.463 ✔; Traffic $60 = Rp1.002.000 ✔.

### Skor

| Kriteria | SEBELUM | SESUDAH |
|---|---|---|
| Ketepatan angka | 5 | 10 |
| Penanganan data ambigu | 4 | 10 |
| Siap pakai | 6 | 8 |
| Kejelasan | 7 | 9 |
| **Skor** | **5** | **9** |

Skill terpakai (ya).

## Ringkasan

| | SEBELUM | SESUDAH |
|---|---|---|
| Skenario 1 (Meta mingguan + omzet) | 7 | 8,5 |
| Skenario 2 (jebakan USD) | 5 | 9 |
| **Rata-rata** | **6** | **8,75** |

**VERDIK: LULUS** — sesudah ≥ 8, jelas lebih baik dari sebelum, tidak ada kesalahan angka (semua cocok dengan hitungan independen).

**Cacat untuk pembuat (bukti + saran):**
1. **Saran "matikan" mengabaikan tujuan kampanye.** Bukti: skenario 1, kampanye "Traffic - Katalog IG" dan "Awareness - Video Reels" disarankan dihentikan karena 0 pesan WA. Saran: bila nama/kolom tujuan berisi Traffic/Awareness/Reach/Video views, tampilkan sebagai "tujuan berbeda — nilai dari klik/CPM, bukan pesan" alih-alih saran hentikan.
2. **Catatan script dipangkas agent.** Bukti: "Kolom dibaca: …" tidak ikut di balasan skenario 1 meski SKILL.md mewajibkan. Saran: taruh baris "Kolom dibaca" di blok ⚠️ atas atau tegaskan di Langkah 4 "salin blok Catatan utuh, jangan diringkas".

**Cuplikan jualan:**
- "Tanpa skill, agent menebak kurs dolar dari internet dan memotong sebagian belanja. Dengan skill, agent berhenti, menanyakan kurs tagihan Anda, lalu menghitung biaya per lead tepat Rp100.647."
- "Tanpa skill, 'biaya per hasil' yang dilaporkan hanya dari sebagian kampanye (Rp25.900). Dengan skill, seluruh belanja dihitung: Rp36.842 per chat WA, naik 14,2% dari minggu lalu."
