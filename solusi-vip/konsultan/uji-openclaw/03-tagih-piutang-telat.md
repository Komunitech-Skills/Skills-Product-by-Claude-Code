# 03 — Tagih piutang telat 21 hari dengan denda kontrak

Tanggal uji: 2026-10-01 (Asia/Jakarta). OpenClaw lokal (`openclaw agent --local`), model router Komunitech (`ninerouter/komunitech`, sama dengan bot). SEBELUM = home `kosong-konsultan` (tanpa skill). SESUDAH = home `sol-konsultan` (paket skill solusi konsultan terpasang). Pesan identik di kedua sisi.

## Pesan member (giliran 1)

```
Klien saya PT Maju Mundur belum bayar invoice INV/2026/08/014 Rp 12.000.000, jatuh tempo 10 September kemarin. Udah saya WA 2x nggak dibales. Bikinin pesan tagihan yang tegas tapi tetap sopan. Di kontrak ada denda 0,1% per hari, maksimal 5%.
```

## SEBELUM (tanpa skill)

### Giliran 1 — tools: []; lampiran file ke chat: tidak; durasi 19 dtk

````markdown
Tagihan ke 2 dan masa tenggat lewat tanpa respons — pesan yang tegas tapi tetap profesional, siap kirim via WA:

---

Yth. Bapak/Ibu PT Maju Mundur,

Kami ingin menindaklanjuti invoice berikut yang hingga saat ini belum kami terima pembayarannya:

*No. Invoice:* INV/2026/08/014
*Nilai Invoice:* Rp 12.000.000
*Jatuh Tempo:* 10 September 2026
*Status:* Terlambat 21 hari (per 1 Oktober 2026)

Kami sudah mengirimkan pengingat sebanyak 2 kali melalui WhatsApp namun belum mendapat tanggapan. Sesuai ketentuan kontrak, keterlambatan pembayaran dikenakan denda 0,1% per hari dari nilai invoice (maksimal 5%).

Rincian denda saat ini:
- Denda: 0,1% x 21 hari x Rp 12.000.000 = Rp 252.000
- *Total tagihan saat ini: Rp 12.252.000*

Denda akan terus berjalan setiap hari keterlambatan hingga maksimal 5% (Rp 600.000) apabila pembayaran belum juga diterima.

Mohon kesediaan Bapak/Ibu untuk menyelesaikan pembayaran *paling lambat 3 hari kerja* sejak pesan ini diterima. Jika ada kendala atau sudah melakukan pembayaran, mohon konfirmasi beserta bukti transfer agar dapat segera kami catat.

Terima kasih atas perhatian dan kerja samanya.

Hormat kami,
[Nama Anda / Nama Perusahaan]

---

Catatan: ganti nomor rekening/kontak Anda kalau mau saya tambahkan di bagian penutup. Mau saya kirimkan langsung ke kontak PT Maju Mundur via WhatsApp, atau ini cukup untuk Anda kirim sendiri?
````

**Jejak tool (sebelum):** Tidak memanggil tool apa pun (hitung di kepala model).

## SESUDAH (dengan paket skill)

### Giliran 1 — tools: ['read', 'exec']; lampiran file ke chat: tidak; durasi 45 dtk

````markdown
Sudah saya hitung pakai skill penagihan piutang. Karena sudah 2x diingatkan tanpa respons dan telat 21 hari, ini masuk **Tahap 5 — pemberitahuan resmi** (belum somasi, tapi sudah formal dan menyebut denda).

### Ringkasan tagihan
- Invoice: INV/2026/08/014
- Nominal: Rp 12.000.000
- Jatuh tempo: 10 September 2026
- Dihitung per: 1 Oktober 2026 → **terlambat 21 hari**
- Denda: Rp 12.000.000 × 0,1% × 21 hari = **Rp 252.000** (dasar: klausul denda di kontrak, maks. 5%)
- **Total ditagih: Rp 12.252.000**

### Pesan tahap 5 · Email/Surat resmi + WA pengantar · kirim hari ini (1 Okt 2026)

**Surat/email (kirim sebagai PDF/email resmi):**
```
Perihal: Pemberitahuan Tagihan Lewat Jatuh Tempo – Invoice INV/2026/08/014

Dengan hormat,

Bersama ini kami sampaikan bahwa Invoice No. INV/2026/08/014 senilai Rp 12.000.000 telah jatuh tempo pada 10 September 2026, dan hingga saat ini (1 Oktober 2026) belum kami terima pembayarannya — keterlambatan sudah mencapai 21 hari. Kami telah mengirimkan pengingat melalui WhatsApp sebanyak 2 kali, namun belum mendapat tanggapan dari pihak PT Maju Mundur.

Sesuai ketentuan pada kontrak kerja sama, keterlambatan pembayaran dikenai denda sebesar 0,1% per hari dari nilai tagihan (maksimal 5%). Per 1 Oktober 2026, denda yang berjalan adalah Rp 252.000, sehingga total kewajiban yang perlu diselesaikan menjadi Rp 12.252.000.

Kami mohon pembayaran dapat diselesaikan paling lambat 8 Oktober 2026, ke rekening [Bank – No. Rek – a.n. ...]. Apabila terdapat kendala di pihak PT Maju Mundur, kami terbuka untuk membahas jadwal pembayaran bertahap yang dituangkan secara tertulis sebelum tanggal tersebut.

Apabila hingga batas waktu tersebut belum ada pembayaran maupun tanggapan, dengan menyesal kami akan mempertimbangkan langkah penyelesaian lebih lanjut sesuai ketentuan yang berlaku.

Atas perhatian dan kerja samanya, kami ucapkan terima kasih.

Hormat kami,
[Nama Anda] – [Jabatan], [Nama Usaha Anda]
```

**WA pengantar (kirim bareng/setelah email):**
> Selamat siang Bapak/Ibu, kami dari [Nama Usaha] ingin menyampaikan bahwa invoice INV/2026/08/014 (Rp 12.000.000, jatuh tempo 10 September) sampai hari ini belum kami terima pembayarannya meski sudah kami ingatkan 2 kali sebelumnya. Kami baru saja kirim surat pemberitahuan resmi ke email PT Maju Mundur, mohon dicek dan dikonfirmasi ya. Mohon pelunasan dilakukan paling lambat 8 Oktober 2026. Terima kasih atas perhatiannya 🙏

### Tahap berikutnya (jika belum dibayar)
- **8–11 Oktober 2026** (lewat tenggat 7 hari, total keterlambatan ≈30 hari) → naik ke **Tahap 6: Surat Teguran (Somasi)** resmi dengan tenggat baru dan menyebut kemungkinan langkah hukum sesuai ketentuan yang berlaku.

### Saran tindakan
- Lengkapi `[Bank – No. Rek – a.n. ...]` dan nama/jabatan Anda sebelum kirim — saya pakai placeholder karena belum disebutkan.
- Simpan bukti pengiriman (screenshot WA, email terkirim/read receipt) untuk dokumentasi bila nanti perlu somasi.
- Kalau PT Maju Mundur menawarkan cicilan, buat kesepakatan tertulis bermeterai Rp10.000 (berapa pun nilainya) — bukan cukup janji lisan.
- Kalau sampai 8 Oktober tetap tidak ada respons sama sekali, saya bisa langsung siapkan draf surat somasi (Tahap 6).

### Catatan hukum
Bukan nasihat hukum. Dasar: KUHPerdata (wanprestasi/somasi), UU ITE, UU Bea Meterai — per 1 Oktober 2026. Untuk sengketa/gugatan, konsultasikan ke advokat.

Asumsi: belum ada pembayaran sebagian, tenggat baru 7 hari, PIC/rekening belum diisi karena tidak disebutkan.
````

**Jejak tool (sesudah):** Baca `tagih-piutang/SKILL.md`; jalankan `scripts/hitung_telat.py --nominal 12.000.000 --jatuh-tempo 2026-09-10 --tanggal 2026-10-01 --sudah-diingatkan 2 --denda-persen 0,1 --denda-per hari --denda-maks 5%`; baca template tahap 5. **Skill terpakai, angka dari script.**

## Verifikasi independen

| Pos | Benar | SEBELUM | SESUDAH |
|---|---|---|---|
| Hari terlambat (10 Sep → 1 Okt 2026) | 21 | ✔ | ✔ |
| Denda 0,1% × 21 × 12.000.000 | 252.000 | ✔ | ✔ |
| Batas denda 5% | 600.000 | ✔ | ✔ (disebut sebagai dasar) |
| Total ditagih | 12.252.000 | ✔ | ✔ |
| Tenggat bayar baru | — | 3 hari kerja | 8 Okt 2026 (Kamis, 7 hari) ✔ |

Aturan/etika: SEBELUM menutup dengan **"Mau saya kirimkan langsung ke kontak PT Maju Mundur via WhatsApp?"** — bertentangan dengan kebijakan solusi (bot tidak pernah mengirim ke klien; WA hanya untuk notifikasi ke diri sendiri) dan menawarkan kemampuan yang tidak terpasang. SESUDAH: meterai Rp10.000 untuk perjanjian cicilan tertulis berapa pun nilainya ✔ (UU 10/2020, surat perjanjian tanpa ambang nominal); menyebut KUHPerdata (wanprestasi/somasi) ✔; penyebutan "UU ITE" sebagai dasar kurang relevan (kecil). Kalimat "8–11 Oktober (lewat tenggat 7 hari)" agak membingungkan.

## Nilai

| Aspek | SEBELUM | SESUDAH |
|---|---|---|
| Ketepatan angka | Benar | Benar (script) |
| Siap pakai | Satu pesan WA siap kirim | Surat/email resmi + WA pengantar + tahap berikutnya + saran bukti |
| Kepatuhan aturan ID | Cukup | Tahapan penagihan, somasi, meterai, disclaimer hukum |
| Keamanan/privasi | Menawarkan kirim langsung ke klien via WA (melanggar kebijakan Copilot) | Tegas: draf hanya untuk member |
| Kejelasan | Ringkas | Panjang tapi terstruktur |
| **Total (1–10)** | **7** | **9** |

Angka sama, tetapi SESUDAH memberi strategi bertahap (tahap 5 → somasi), surat resmi + WA pengantar, tenggat konkret, opsi cicilan tertulis, dan dokumentasi bukti — jelas lebih siap pakai untuk konsultan. SEBELUM dikurangi karena menawarkan pengiriman langsung ke klien. Ini skenario dengan selisih paling meyakinkan.
