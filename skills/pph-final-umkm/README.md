# Hitung Pajak UMKM 0,5% Tiap Bulan

**Masukkan omzet, langsung tahu pajak per bulan, sisa yang harus disetor setelah dipotong marketplace, dan batas setornya.**

*Angka pajak dihitung program kecil (bukan dikira-kira) dan dicocokkan dengan hitungan independen. Diuji ulang penguji AI independen di OpenClaw pada 16 Oktober 2026 (versi 1.0.5, 5 skenario): tanpa skill 6,8 → dengan skill 8,8 dari 10, tanpa salah angka. Hasil uji dijelaskan apa adanya di bagian "Hasil uji" di bawah.*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Rincian PPh final (pajak penghasilan tetap 0,5% dari omzet) per bulan, ringkas untuk chat (satu baris pendek per bulan) atau tabel lengkap untuk disimpan, dengan omzet kumulatif (dijumlah sejak Januari) dan batas setor yang sudah digeser ke hari kerja bila tanggal 15 jatuh hari libur
- ✅ Otomatis menerapkan Rp500 juta pertama bebas pajak untuk orang pribadi, termasuk bulan saat batas terlewati
- ✅ PPh 22 yang sudah dipotong marketplace (Shopee, Tokopedia, Lazada, Blibli) langsung diperhitungkan: terlihat per bulan berapa yang masih harus disetor sendiri dan berapa yang kelebihan dan bisa diminta kembali
- ✅ Langsung terlihat bulan mana yang batas setornya sudah lewat, mana yang jatuh besok, plus perkiraan pajak sampai akhir tahun
- ✅ Dasar aturan terbaru disebut (PP 20/2026: orang pribadi dan PT perorangan tidak lagi dibatasi 7/4 tahun)

## Cocok untuk siapa
- Penjual online, warung, katering, bengkel, dan UMKM perorangan yang memakai tarif 0,5%
- PT perorangan dan koperasi
- Admin atau keluarga yang membantu mengurus pajak usaha

## Contoh sebelum & sesudah
**Sebelum:** Menjumlah omzet di buku, bingung bulan mana mulai bayar pajak, dan tidak tahu apakah potongan PPh 22 dari Shopee sudah cukup atau masih harus setor lagi.

**Sesudah (cukup ketik):** "Saya jualan baju di Shopee sama toko kecil di rumah, atas nama pribadi. Omzet 2026: Jan 52jt, Feb 48,5jt, Mar 95jt, Apr 61jt, Mei 58jt, Jun 64jt, Jul 70jt, Agu 73jt, Sep 66jt. Shopee potong PPh 22 Agu 180rb, Sep 165rb. Ada yang telat?"

*Cuplikan hasil hitungan versi 1.0.6 (tampilan chat) untuk pesan di atas (data fiktif, tanggal acuan 14 Oktober 2026; judul, sebagian ringkasan, dan catatan dipotong):*

> **Per bulan**
> **Januari–Juli** · omzet Rp448.500.000 · PPh Rp0
> Total 7 bulan; masih dalam Rp500 juta bebas. Tidak ada setoran.
> **Agustus** · omzet Rp73.000.000 · PPh Rp107.500
> Melewati Rp500 juta; yang kena pajak hanya Rp21.500.000. Dipungut marketplace Rp180.000; lebih Rp72.500 (bisa diminta kembali), tidak perlu setor.
> **September** · omzet Rp66.000.000 · PPh Rp330.000
> Dipungut marketplace Rp165.000; kurang Rp165.000, setor sendiri paling lambat Kamis 15 Okt 2026 (BESOK).
>
> **Ringkasan**
> - Total PPh final Januari–September: Rp437.500
> - Kurang setor (setor sendiri): Rp165.000
> - Lebih dipungut (bisa diminta kembali): Rp72.500
> - Setor terdekat: Rp165.000 (masa September)
> - Paling lambat: Kamis 15 Okt 2026 (besok)

Artinya: tidak ada yang telat. Agustus sudah tertutup potongan Shopee (malah lebih Rp72.500), September tinggal Rp165.000 yang disetor sendiri paling lambat besok. Tanpa memperhitungkan PPh 22, Anda bisa menyetor Rp272.500 lebih banyak dari yang perlu.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Hitung PPh final UMKM saya dari file omzet-2026.csv."
- "PT perorangan saya omzet Agustus 120 juta, pajaknya berapa?"
- "Shopee sudah potong PPh 22 bulan ini 250 ribu, saya masih harus setor berapa?"
- "Pajak UMKM saya bulan ini berapa? Omzet Oktober kira-kira 85 juta." (AI langsung memberi kemungkinan hasilnya, lalu menanyakan data yang kurang)

## Instalasi singkat
Salin folder `pph-final-umkm` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** penguji AI independen, skor 1–10.
- **Uji ulang di OpenClaw, 16 Oktober 2026 (versi 1.0.5, 5 skenario termasuk yang dengan pengaturan seperti bot Telegram (bukan bot sungguhan)):** rata-rata tanpa skill 6,8 (skor uji 14 Oktober, dipakai ulang) → dengan skill **8,8**, selisih +2,0, **lulus**. Semua angka cocok dengan hitungan independen: potongan PPh 22 marketplace dikurangkan per bulan (contoh: Agustus lebih Rp72.500 yang bisa diminta kembali, September kurang Rp165.000), batas setor digeser ke hari kerja dan masa yang sudah lewat batas ditandai per "hari ini", tarif 0,5% orang pribadi dan PT perorangan tanpa batas tahun sesuai PP 20/2026. Catatan jujur: jawaban masih panjang untuk chat (tabel 9 kolom; satu jawaban ±4.200 karakter), dan di satu sampel AI menulis kalimat soal pengembalian kelebihan PPh 22 lebih pasti daripada rujukan.
- **Uji ulang di OpenClaw, 14 Oktober 2026 (versi 1.0.3, 5 skenario):** rata-rata tanpa skill 6,8 → dengan skill 6,1, jadi versi itu **belum lolos**. Angka PPh final dari hitungan selalu benar dan tabel batas setor per bulan unggul, tetapi versi 1.0.3 belum memperhitungkan PPh 22 marketplace sebagai bagian pelunasan PPh final (aturan yang dipakai sudah usang; di salah satu contoh pembeli bisa menyetor Rp272.500 lebih banyak dari yang perlu), masih menyebut batas 7 tahun yang sudah dihapus PP 20/2026, dan AI sempat menulis tanggal "hari ini" serta satu subtotal sendiri yang keliru. **Versi 1.0.4 memperbaiki ketiganya** (PPh 22 dikurangkan per bulan, aturan batas waktu mengikuti naskah resmi PP 20/2026, tanggal acuan dan subtotal dicetak oleh hitungan sehingga AI tidak menjumlah sendiri) dan versi 1.0.5 lulus uji ulang 16 Oktober 2026 (butir pertama).
- Uji yang lebih lama: OpenClaw 1 Oktober 2026 (versi 1.0.3, satu skenario orang pribadi) tanpa skill 8 → dengan skill 9; uji simulasi agent 23 September 2026, angka cocok dengan hitungan independen pada 400 kasus acak (0 selisih). Keduanya sebelum aturan PPh 22 dan PP 20/2026 diperbarui, jadi bukan bukti untuk versi terbaru.

**Status uji (jujur):** versi 1.0.5 lulus uji ulang penguji AI independen di OpenClaw 2026.10.2 pada 16 Oktober 2026 (6,8 → 8,8; 5 skenario termasuk yang dengan pengaturan seperti bot Telegram (bukan bot sungguhan); tanpa salah angka). Belum diuji manusia dan belum melalui program beta. Versi lama pernah diuji di Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama). Aturan pajak dicek ke naskah resmi pada 14 Oktober 2026; pembulatan belum dicocokkan dengan Coretax.

## FAQ
**Apakah hasil ini bisa langsung dipakai untuk setor pajak?**
Hasilnya adalah hitungan bantu. Setoran dan pelaporan tetap lewat Coretax (sistem pajak online) atau DJP. Untuk kasus khusus, konfirmasi ke DJP (Kring Pajak 1500200) atau konsultan pajak.

**PPh 22 yang dipotong Shopee/Tokopedia mengurangi pajak saya?**
Ya. Menurut FAQ DJP tentang PMK 37/2025 (versi terbaru 2.0, 24 September 2026), potongan itu bagian dari pelunasan PPh final 0,5% Anda. Bila potongannya kurang, sisanya disetor sendiri; bila lebih, kelebihannya bisa diajukan permohonan pengembalian ke DJP. FAQ itu tidak mengatur pemindahan kelebihan ke bulan berikutnya, jadi skill menghitungnya per bulan.

**NPWP saya sudah lebih dari 7 tahun, atau usaha saya CV. Masih bisa pakai 0,5%?**
Orang pribadi dan PT perorangan: bisa, karena PP 20/2026 menghapus batas 7 tahun (orang pribadi) dan 4 tahun (PT perorangan), selama omzet setahun tidak melebihi Rp4,8 miliar. CV, firma, dan PT biasa sudah dikeluarkan dari skema 0,5%; yang terdaftar sebelum 22 April 2026 hanya boleh meneruskan sisa jangka waktu lamanya. Sebutkan tahun NPWP terdaftar, AI akan menghitung sampai tahun berapa.

> **Catatan penting:** alat bantu hitung, bukan nasihat pajak. Dasar aturan (PP = Peraturan Pemerintah, PMK = Peraturan Menteri Keuangan; dicek ke sumber resmi 14 Oktober 2026): PP 55/2022 sebagaimana diubah PP 20/2026 (PPh final 0,5%; omzet Rp500 juta pertama bebas untuk orang pribadi; batas omzet Rp4,8 miliar; batas waktu orang pribadi dan PT perorangan dihapus; PT perorangan yang batas lamanya berakhir 2024 belum tegas di aturan peralihan, jadi pastikan ke Kring Pajak 1500200); PPh 22 marketplace PMK 37/2025 dan FAQ DJP versi 1 Juli 2026 serta versi 2.0 24 September 2026 (potongan = bagian pelunasan PPh final); batas setor tanggal 15 bulan berikutnya dan digeser ke hari kerja bila libur (PMK 81/2024 Pasal 94 dan 100). PPh dan selisihnya dengan PPh 22 dibulatkan ke bawah; pembulatan ini belum dicocokkan dengan Coretax, bila berbeda ikuti Coretax. Kepastian: DJP (Kring Pajak 1500200) atau konsultan pajak.

## Riwayat perubahan

Versi terkini: **1.0.6** — tampilan hasil untuk Telegram/WhatsApp dirancang tanpa tabel lebar (satu baris pendek per bulan) dan akan diuji ulang di bot asli; angka hitungan tidak berubah. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
