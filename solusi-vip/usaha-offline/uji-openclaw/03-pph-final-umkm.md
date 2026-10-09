# Uji 03 — PPh Final UMKM 0,5% (orang pribadi, batas Rp500 juta)

Tanggal uji: 2026-10-01 · OpenClaw lokal (`openclaw agent --local`), model router Komunitech (`ninerouter/komunitech`, sama dengan bot). SEBELUM = home tanpa skill; SESUDAH = home dengan paket skill usaha-offline. Teks balasan disalin utuh, tanpa suntingan.

## Pesan member
> Saya punya warung makan, atas nama pribadi, NPWP dari 2021. Omzet 2026: Jan 48jt, Feb 45jt, Mar 52jt, Apr 70jt, Mei 55jt, Jun 50jt, Jul 53jt, Agu 58jt, Sep 61jt. Okt kira2 60jt. Pajak 0,5% nya tiap bulan berapa dan setornya kapan? Ada yg telat ga?

## Giliran 1

Alat — SEBELUM: `tool_search`, `memory_search`, `tool_call` (mencoba web search, tidak tersedia; hitung manual). SESUDAH: baca `pph-final-umkm/SKILL.md`, jalankan `scripts/pph_final.py --jenis op --tahun 2026 --omzet …`. **Skill benar-benar terpakai.**

### SEBELUM (tanpa skill)
> Saya cek dulu pakai aturan PPh Final UMKM (PP 23/2018 jo PP 55/2022) — alat pencarian web sedang tidak tersedia, jadi ini saya hitung manual dari aturan yang berlaku. Dua hal penting buat warung Bapak/Ibu:
>
> **1. Jangka waktu pakai tarif 0,5% final**
> NPWP pribadi terdaftar 2021 → untuk WP Orang Pribadi, jatah pakai skema 0,5% ini 7 tahun dari tahun terdaftar = **2021–2027**. Jadi 2026 masih aman pakai tarif final 0,5%. Mulai 2028 wajib pindah ke tarif normal (Pasal 17, pakai pembukuan/NPPN).
>
> **2. Fasilitas omzet tidak kena pajak Rp500 juta/tahun**
> Khusus WP Orang Pribadi, omzet kumulatif sampai Rp500jt dalam satu tahun pajak **tidak kena pajak sama sekali**. Baru setelah kumulatif lewat 500jt, kelebihannya yang kena 0,5%.
>
> **Hitung kumulatif omzet 2026 warung Bapak/Ibu:**
> - Jan 48jt → kum 48jt → bebas pajak
> - Feb 45jt → kum 93jt → bebas pajak
> - Mar 52jt → kum 145jt → bebas pajak
> - Apr 70jt → kum 215jt → bebas pajak
> - Mei 55jt → kum 270jt → bebas pajak
> - Jun 50jt → kum 320jt → bebas pajak
> - Jul 53jt → kum 373jt → bebas pajak
> - Agu 58jt → kum 431jt → bebas pajak
> - Sep 61jt → kum 492jt → bebas pajak (masih di bawah 500jt)
> - **Okt ~60jt → kum ~552jt** → jatah bebas pajak tersisa cuma 8jt (500jt−492jt), sisanya **52jt kena pajak**
>   → PPh Final Okt = 0,5% × 52jt = **Rp260.000**, setor paling lambat **15 November 2026** (catatan: 15 Nov 2026 jatuh hari Minggu, jadi kemungkinan maju ke hari kerja berikutnya — cek kalender pajak DJP buat pastinya).
>
> Jadi: **Jan–Sep 2026 tidak ada setoran PPh final sama sekali** (bukan telat, memang nihil karena belum lewat threshold 500jt). Baru mulai **Oktober 2026** ada kewajiban setor Rp260rb, dan deadlinenya (15 Nov) belum lewat — jadi **belum ada yang telat**.
>
> Heads-up: karena jatah 500jt sudah habis per Oktober, mulai **November & Desember** seluruh omzet bulan itu kena 0,5% penuh (bukan cuma kelebihannya lagi). Kalau omzet Nov/Des sekitar 60jt juga, berarti PPh-nya ~Rp300.000/bulan, jatuh tempo 15 Des 2026 dan 15 Jan 2027.
>
> Mau saya buatkan reminder otomatis tiap tanggal segitu biar gak kelewat setor?

### SESUDAH (paket skill)
> Sudah saya hitung pakai skema PPh Final UMKM 0,5% (NPWP pribadi, pembebasan Rp500 juta pertama per tahun):
>
> **Omzet kumulatif 2026 Anda melewati Rp500 juta di bulan Oktober** (kumulatif s.d. September = Rp492 juta, lalu +60 juta Oktober = Rp552 juta).
>
> | Bulan | Omzet | Kumulatif | Kena pajak | PPh 0,5% | Setor plg lambat |
> |---|---:|---:|---:|---:|---|
> | Jan–Sep | 48–61jt/bln | s.d. Rp492jt | Rp0 | **Rp0** | - (tidak ada kewajiban, masih bebas pajak) |
> | Okt (estimasi) | Rp60jt | Rp552jt | Rp52jt (bagian di atas 500jt) | **Rp260.000** | **15 November 2026** |
>
> **Jadi:**
> - Jan–Sep: **tidak ada PPh final yang perlu disetor** (Rp0), karena omzet kumulatif Anda masih di bawah Rp500 juta sepanjang periode itu.
> - Oktober: baru mulai kena pajak, tapi hanya atas selisih Rp52 juta (bagian yang melewati Rp500jt), jadi PPh = **Rp260.000**, jatuh tempo setor **15 November 2026**.
> - **Tidak ada yang telat** — belum ada kewajiban setor yang jatuh tempo dan terlewat sampai hari ini (1 Okt 2026). Kewajiban setor pertama Anda tahun ini justru baru di November nanti (untuk masa Oktober).
>
> Catatan penting:
> - Batas Rp500 juta ini dihitung dari **total omzet semua usaha** Anda (bukan cuma warung), jadi kalau ada penghasilan usaha lain, perlu digabung.
> - Kalau omzet November–Desember juga sekitar 55–65jt, seluruhnya akan kena pajak penuh 0,5% (karena sudah lewat batas bebas).
> - Ini alat bantu hitung, bukan nasihat pajak resmi — untuk kepastian terutama soal cara setor/lapor di Coretax, cek ke pajak.go.id atau Kring Pajak 1500200.
>
> Mau saya hitung sekalian estimasi Nov–Des kalau Anda punya perkiraan omzetnya?

## Verifikasi independen
- Kumulatif (Python): 48, 93, 145, 215, 270, 320, 373, 431, **492 jt** (s.d. Sep) → Jan–Sep PPh = **Rp0** (PP 55/2022 Pasal 60: omzet s.d. Rp500 jt/tahun WP OP tidak dikenai PPh final).
- Okt 60 jt → kumulatif 552 jt → bagian kena pajak 52 jt × 0,5% = **Rp260.000**. Kedua sisi benar.
- Batas setor masa Oktober: tanggal 15 bulan berikutnya = **15 November 2026, hari Minggu** → bergeser ke hari kerja berikutnya (Senin 16 Nov) sesuai PMK 81/2024. SEBELUM menyebut hal ini (dengan saran cek kalender DJP). SESUDAH **tidak**, padahal script mengeluarkan catatan "cek DJP bila jatuh di hari libur" — model tidak meneruskannya.
- Jangka waktu tarif 0,5% WP OP: 7 tahun pajak (PP 55/2022 Pasal 59) → terdaftar 2021 berarti s.d. 2027. SEBELUM menyebutnya (tegas "mulai 2028 wajib pindah" — sesuai teks PP 55/2022; perubahan kebijakan setelahnya tidak diverifikasi di uji ini). SESUDAH **tidak menyinggung sama sekali** (SKILL.md memang melarang menyatakan pasti, tapi seharusnya tetap memberi peringatan "perlu dicek").
- SESUDAH menambah poin benar yang tidak ada di SEBELUM: batas Rp500 jt dihitung dari gabungan semua usaha OP; rujukan Kring Pajak.
- Tidak ada yang telat — kedua sisi benar.

## Nilai
| | Ketepatan | Siap pakai | Aturan ID | Keamanan | Kejelasan | **Skor** |
|---|---|---|---|---|---|---|
| SEBELUM | 9 | 8 | 9 | 9 | 8 | **8** |
| SESUDAH | 9 | 8 | 7 | 9 | 9 | **7** |

Alasan: angka identik dan benar. SEBELUM lebih lengkap secara aturan (tanggal setor jatuh hari Minggu, batas 7 tahun). SESUDAH lebih ringkas (tabel) tapi melewatkan dua hal yang penting bagi pemilik warung. Skill tidak menang di skenario ini.
