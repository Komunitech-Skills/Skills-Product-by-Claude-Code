# Uji banding pesaing — S1 (Toko kue rumahan Bekasi) vs skill publik terbaik yang ditemukan

## Sumber yang dicari
Kata kunci: `github "SKILL.md" weekly content plan / social media content calendar skill`,
`coreyhaines31/marketingskills content calendar`, juga dicek (tidak dipakai karena kurang relevan/tidak
ditemukan): ClawHub, skills.sh (hasil `skills.sh/coreyhaines31/marketingskills/social-content` muncul —
sama dengan repo GitHub di bawah), `anthropics/skills` (tidak ada skill social-media-calendar di sana per
pengecekan ini), VoltAgent/awesome-openclaw-skills (tidak diakses langsung, hasil pencarian mengarah ke
repo yang sama), `manairalabs/bicara-skills` dan `alvinindra/bahasa-skills` (dicoba, tidak ditemukan skill
konten sosmed mingguan yang relevan di repo tersebut lewat pencarian umum — kemungkinan repo kecil/privat
atau nama berbeda; tidak dipaksakan sebagai pesaing).

**Pesaing yang dipilih:** [`coreyhaines31/marketingskills` — skill `social`](https://github.com/coreyhaines31/marketingskills/blob/main/skills/social/SKILL.md)
(dibaca via raw.githubusercontent.com, TIDAK dijalankan, TIDAK disalin isinya).
- **Popularitas/kredibilitas:** repo berisi 43 skill, dibuat Corey Haines (praktisi marketing dengan
  rekam jejak publik), banyak dirujuk di direktori pihak ketiga (AgenticSkills, skills.sh) — lolos
  sinyal bukti pemakaian nyata.
- **Lisensi:** dicek `LICENSE` repo (MIT, per pengecekan halaman repo GitHub) — boleh jadi referensi
  penilaian, TIDAK disalin ke skill kita.
- **Cakupan:** skill `social` mencakup strategi konten LinkedIn/Twitter/Instagram/TikTok/Facebook secara
  umum (global, gaya SaaS founder/personal brand Amerika), termasuk pillar konten, hook formula, struktur
  video pendek, engagement, analytics.

## Menjalankan skenario S1 dengan pendekatan pesaing (simulasi, mengikuti `skills/social/SKILL.md`)

Input pengguna sama seperti S1 (toko kue Bu Sari, Bekasi, IG+TikTok, minggu 5-11 Okt 2026).

Skill pesaing dimulai dengan wawancara 4 kategori (Goals, Audience, Brand Voice, Resources) — mirip
konsepnya dengan wawancara profil kita, tapi **tidak menanyakan hal spesifik operasional UMKM** seperti
cara order/kontak WA, izin PIRT/BPOM, atau larangan klaim. Setelah itu skill pesaing memberi **kerangka**
(bukan konten jadi), kira-kira begini kalau diikuti persis:

```
## Kerangka konten pesaing (contoh output mengikuti frameworknya)

Content Pillars (isi manual oleh pengguna):
| Pillar | % | Topics |
|---|---|---|
| Industry insights | 30% | (isi sendiri) |
| Behind-the-scenes | 25% | (isi sendiri) |
| Educational | 25% | (isi sendiri) |
| Personal | 15% | (isi sendiri) |
| Promotional | 5% | (isi sendiri) |

Weekly Planning Template:
| Day | Instagram | TikTok |
|-----|-----------|--------|
| Mon | Carousel | - |
| Tue | Story | Short-form video |
| Wed | Reel | - |
| Thu | Educational | Short-form video |
| Fri | Story | - |

Hook formula yang disarankan dipakai (pilih & isi sendiri):
- Curiosity: "I was wrong about [common belief]."
- Story: "3 years ago, I [past state]. Today, [current state]."
- Value: "[Number] [things] that [outcome]:"

Video structure (Problem-Solution, 15-30 detik):
[0-3s] Hook: State the problem
[3-10s] Agitate: Why it matters
[10-25s] Solution
[25-30s] CTA
```

Pengguna (toko kue Bekasi, awam, gunakan Bahasa Indonesia) masih harus **menerjemahkan sendiri** template
di atas ke: caption Bahasa Indonesia yang benar-benar siap tempel, hashtag yang relevan untuk pasar
Indonesia, jam posting yang relevan untuk audiens Indonesia (skill pesaing tidak punya acuan jam WIB),
tanggal & momen lokal (tidak ada perhitungan tanggal kembar/gajian sama sekali — konsep "tanggal kembar"
dan "gajian tanggal 25" tidak dikenal di framework ini karena memang dibuat untuk pasar global/US),
serta tidak ada pengecekan aturan iklan Indonesia (BPOM/PIRT/UU PDP) sama sekali.

## Tabel penilaian berdampingan

| Aspek | Pesaing (`coreyhaines31/marketingskills` — `social`) | Skill kita (`konten-mingguan`) |
|---|---|---|
| Kualitas isi | Framework matang & teruji untuk strategi umum (hook formula, video structure jelas dan berguna) | Konten jadi langsung: hook, caption, naskah, brief, hashtag, CTA per hari |
| Kesesuaian konteks Indonesia | Tidak ada — bahasa Inggris, contoh U.S./SaaS, tidak ada Rupiah/WA/marketplace lokal | Penuh: Bahasa Indonesia, WA sebagai CTA utama, hashtag lokal, gajian/tanggal kembar/hari besar RI |
| Akurasi tanggal/momen | Tidak ada perhitungan tanggal sama sekali (murni template hari generik "Mon-Fri") | Dihitung & diverifikasi lewat `nomor_minggu.py`, momen lokal (gajian, tanggal kembar, hari besar) |
| Siap pakai langsung | Tidak — perlu diisi/diterjemahkan manual oleh pengguna, cocok untuk marketer yang sudah paham strategi | Ya — siap tempel, cocok untuk UMKM awam yang tidak sempat menyusun strategi sendiri |
| Kepatuhan iklan lokal | Tidak dibahas (tidak relevan untuk pasar target mereka) | Eksplisit: BPOM/PIRT/klaim dilarang/UU PDP dicek tiap hari |
| Dukungan platform | LinkedIn & Twitter/X termasuk (lebih luas) | Tidak ada LinkedIn/Twitter/X — **ini kekurangan nyata skill kita** (lihat cacat di `03-konsultan-pajak.md`) |
| Jam posting | Tidak ada acuan jam spesifik per wilayah | Ada acuan jam WIB per platform, ditandai jelas "perkiraan umum" |

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
1. **Struktur video 3-hook simultan** ("[VISUAL HOOK] + [VERBAL HOOK] + [TEXT OVERLAY]" dalam 1 detik
   pertama) — skill kita hanya punya "hook 3 detik" tekstual; bisa diperkaya dengan penekanan bahwa hook
   verbal, visual, dan teks overlay harus selaras, bukan cuma kalimat pembuka.
2. **Dukungan platform lebih luas (LinkedIn/Twitter-X)** — memperkuat temuan cacat di S3: skill kita
   perlu menambah cakupan LinkedIn minimal, karena target pasar (termasuk profesional/konsultan) memakai
   platform itu.
3. **Bagian "Content Ideas by Situation" (Starting Out / Stuck)** — ide bagus untuk pengguna yang
   kehabisan ide bulan berikutnya; skill kita fokus ke "1 minggu" tapi tidak punya fallback ide kalau
   pemilik usaha merasa buntu — bisa jadi bahan untuk skill `kalender-konten-30hari` atau ditambah
   sebagai 1-2 baris tips di README skill ini.
4. Konsep **"Batching Strategy"** (blok waktu tetap untuk produksi mingguan) bisa disebut singkat di
   README sebagai tips penggunaan, walau bukan bagian inti skill ini.

## Kesimpulan
Skill kita **menang telak untuk target pasar yang dituju** (UMKM/profesional Indonesia awam, butuh
konten siap pakai tanpa strategi manual) — pesaing unggul di kedalaman *framework strategi* dan cakupan
platform, tapi tidak menghasilkan konten siap pakai dan sama sekali tidak melokalkan ke Indonesia. Ini
BUKAN kekalahan telak skill kita; tidak ada dasar untuk skor ≤ 6 dari kriteria ini. Kekurangan cakupan
platform (LinkedIn) tetap dicatat sebagai cacat SEDANG terpisah di `HASIL-UJI.md`.
