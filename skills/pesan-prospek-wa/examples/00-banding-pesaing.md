# Uji banding pesaing — Skenario 01

> Penguji independen, 2026-09-25. Skill pesaing hanya **dibaca untuk dinilai** (tidak disalin, tidak ada script pesaing yang dijalankan). Permintaan identik dengan `01-katering-kantor-dari-pameran.md`.

## Pencarian pesaing (kata kunci & sumber)
| Kata kunci | Sumber | Hasil |
|---|---|---|
| `SKILL.md WhatsApp outreach skill cold message prospect clawhub OR skills.sh` | Web search | coreyhaines31/marketingskills `cold-email`; clawskills.sh: `jk-0001-outreach-and-prospecting`, `brianrwagner-brw-cold-outreach-sequence`, `strouddustinn-bot-outbound-prospecting` (**tidak bisa dibuka — domain clawskills.sh diblokir proxy sesi ini**) |
| `github agent skill "whatsapp" "outreach" SKILL.md sales prospecting` | Web search | lucaslinares1/gtm-skills, hyperfx-ai/marketing-skills, gokapso/agent-skills & 2ChatCo/agent-skills (integrasi API WA, bukan penulisan pesan), awesome-sales-automation-skills |
| `"whatsapp" cold message prospect skill SKILL.md github "first message" template small business` | Web search | borghei/Claude-Skills `cold-email` (repo 373 SKILL.md — pola "puluhan–ratusan skill", tidak dipilih), sbl.so "WhatsApp Cold Outreach Templates" (**diblokir proxy**), gtmagents/gtm-agents |

Tidak ditemukan skill **khusus WhatsApp + Bahasa Indonesia** untuk pesan pertama ke prospek. Pesaing yang dipakai:
1. **`cold-email`** — https://github.com/coreyhaines31/marketingskills/tree/main/skills/cold-email (commit `5b2c000`, 4 Sep 2026, MIT). Pesaing terkuat & sumber ATM skill kita.
2. **`email-writer`** — https://github.com/lucaslinares1/gtm-skills/tree/main/skills/email-writer (commit `d5799d2`, 1 Jun 2026, MIT). Dipilih karena punya rujukan `cold-outreach.md` + `warm-intros.md` dan aturan format ketat. Popularitas tidak bisa diverifikasi (API GitHub tidak tersedia di sesi ini).

## Output mengikuti instruksi pesaing
Agar adil, prinsip pesaing diterapkan ke pesan WA berbahasa Indonesia (pesaing tidak melarang bahasa lain; saluran email diterjemahkan ke WA dengan membuang baris subjek).

### P1 — mengikuti `cold-email` (Observation → Problem → Proof → Ask; "lead with their world, don't open with who you are"; interest CTA)
```
Bu Maya, waktu kita ngobrol di booth Jakarta Food & Franchise Expo, Ibu cerita karyawan di PT Sinar Logistik Nusantara mulai bosan dengan menu kantin.

Biasanya kalau menu sudah terasa itu-itu saja, makin banyak karyawan yang pesan online sendiri dan jam istirahat jadi molor.

Kami menyiapkan makan siang harian untuk 3 pabrik di Cikarang dengan menu yang berganti tiap minggu.

Layak dilihat contoh menunya?
```
(Subjek email yang disarankan skill: "menu kantin" — tidak relevan di WA.)
Script kita: 409 karakter, asal kontak ✔ secara makna (script: false negative), opsi keluar ✗, nama pengirim/usaha ✗ (tidak disebut sama sekali).

### P2 — mengikuti `email-writer` (≤ 5 kalimat, tanpa emoji/tanda seru/tanda tangan, "Poke the Bear", social proof terukur)
```
Bu Maya, soal menu kantin yang Ibu ceritakan di Jakarta Food & Franchise Expo kemarin.

Bagaimana Ibu tahu berapa karyawan yang sekarang memilih beli makan di luar karena bosan dengan menu yang sama?

Tiga pabrik di Cikarang yang kami layani mengganti menu mingguan dan tidak lagi menerima keluhan soal menu.

Kalau saya kirim contoh menu dua minggu untuk 120 porsi, apakah Ibu mau melihatnya?
```
Script kita: 393 karakter, opsi keluar ✗, identitas pengirim ✗. ⚠️ "tidak lagi menerima keluhan soal menu" muncul karena kerangka pesaing meminta *social proof — quantified, specific*; pengguna tidak pernah memberi data itu → risiko klaim karangan.

### K — skill kita
Lihat `01-katering-kantor-dari-pameran.md` (3 varian + wa.me + jam kirim + checklist).

## Penilaian berdampingan (0–2 per kriteria)
| # | Kriteria | P1 cold-email | P2 email-writer | K pesan-prospek-wa |
|---|---|---|---|---|
| 1 | Relevan dengan saluran WA & budaya Indonesia (sapaan, identitas di awal) | 1 | 0 | 2 |
| 2 | Identitas pengirim jelas (penting di WA agar tidak dikira penipuan) | 0 | 0 | 2 |
| 3 | Asal kontak disebut | 2 | 2 | 2 |
| 4 | Personalisasi nyambung ke masalah | 2 | 2 | 2 |
| 5 | Opsi keluar sopan | 0 | 0 | 2 |
| 6 | CTA ringan | 2 | 1 (lebih berat, pertanyaan "poke the bear" bisa terasa menggurui HRD) | 2 |
| 7 | Tidak mengarang klaim | 2 | 0 | 2 |
| 8 | Kepatuhan hukum lokal (UU PDP, sumber kontak sah) | 0 | 0 | 2 |
| 9 | Siap pakai (wa.me, jam kirim WIB/WITA/WIT, checklist) | 0 | 0 | 2 |
| 10 | Kualitas copywriting (ringkas, "peer tone", tiap kalimat bermakna) | 2 | 1 | 1 |
| | **Total (maks 20)** | **11** | **6** | **19** |

## Kesimpulan
**Skill kita menang jelas** (19 vs 11 vs 6), terutama pada hal yang spesifik WA-Indonesia (identitas pengirim di awal, opsi keluar, UU PDP, wa.me, zona waktu) dan larangan mengarang bukti.

**Kelebihan pesaing yang patut dipelajari (ditulis ulang dengan cara kita, bukan disalin):**
- `cold-email` P1 lebih tajam di satu hal: kalimat masalah ("karyawan pesan online sendiri, jam istirahat molor") membuat penerima merasa dipahami. Varian 3 kita cenderung mendaftar fitur (menu berganti, diantar sebelum istirahat) tanpa menyebut akibat bagi penerima. Usulan: template Varian 3 menambahkan panduan "sebut akibat masalah bagi penerima dalam 1 kalimat, hanya jika pengguna mengonfirmasi/wajar" — itu sebabnya kriteria 10 kita 1, bukan 2.
- `email-writer` punya aturan "paste-back learning" (belajar dari versi yang benar-benar dikirim pengguna) — ide fitur untuk versi berikutnya, bukan kekurangan inti.
