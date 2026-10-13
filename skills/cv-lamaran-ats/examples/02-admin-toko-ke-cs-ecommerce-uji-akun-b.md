# Skenario 2 (Akun B) — Normal: Admin Toko 5 Tahun Pindah ke Customer Service E-commerce

## Input pengguna
```
Saya udah 5 tahun jadi admin toko offline, mau coba lamar jadi CS di marketplace.
Ini lowongannya:

Customer Service Staff (Marketplace)
PT Toko Digital Nusantara - Bandung (WFO)
Kualifikasi:
- Min. SMA/SMK, D3 lebih disukai
- Pengalaman min. 1 tahun di bidang layanan pelanggan/admin/retail
- Terbiasa membalas chat pelanggan dengan cepat dan sopan
- Familiar dengan marketplace (Shopee/Tokopedia/TikTok Shop)
- Mampu multitasking dan bekerja shift

Profil saya: Rina Wulandari, Bandung, 0857xxxxxxx, rina.w@email.com. Admin Toko
Sembako Berkah (2019-sekarang): layani pembeli langsung dan lewat WA, catat stok,
input penjualan harian, kadang bantu jualan di Shopee toko (upload produk & balas
chat). SMA. Ekspektasi gaji 3,8 juta.
```

## Output (ringkas)
```
## Evaluasi Kecocokan Lowongan: CS Staff (Marketplace) di PT Toko Digital Nusantara
**Saringan wajib:** LULUS — pendidikan SMA memenuhi minimal; lokasi Bandung sesuai;
gaji tidak dicantumkan → dicatat "belum diketahui, tanyakan saat proses".

| Dimensi | Skor | Catatan |
|---|---|---|
| Keahlian & alat kerja | 70/100 | Sudah pegang Shopee (upload produk, balas chat) — relevan langsung |
| Pengalaman | 65/100 | 5 tahun layanan pelanggan langsung & WA, fungsi kerja mirip CS meski jabatan beda |
| Preferensi & arah karier | — | Belum cukup data, tidak dinilai |
| Syarat administratif | 100/100 | Pendidikan & lama pengalaman lebih dari cukup |

**Skor akhir: 73,8/100 — Cocok, lamar sambil perkuat celah**
(Preferensi tidak dinilai → bobot 35/30/15 dinormalisasi ke total 0,80:
(70×0,35 + 65×0,30 + 100×0,15) / 0,80 = 59 / 0,80 = 73,75 → 73,8)
### Kenapa cocok: sudah familiar Shopee (bukan cuma teori), 5 tahun terbiasa layani
pembeli langsung — transferable skill kuat ke CS chat.
### Celah: belum disebutkan pengalaman Tokopedia/TikTok Shop atau kerja shift —
sarankan disampaikan kesediaan belajar/menyesuaikan shift di surat lamaran.
### Rekomendasi: Lamar — pengalaman retail + sudah pegang Shopee jadi nilai jual kuat.

## Skor Kecocokan Kata Kunci
(dijalankan pada draf CV — hasil disaring: kata seperti "toko", "digital", "nusantara"
[pecahan nama PT] dibuang manual sebelum ditampilkan, sesuai Langkah 4 SKILL.md)
Sudah ada: pelanggan, chat, admin, shopee, retail, sopan
Belum terlihat: tokopedia, tiktok, shift, multitasking
→ Ditanyakan ke pengguna: pernah pegang toko di Tokopedia/TikTok Shop juga, atau
cuma Shopee? (jawaban menentukan penambahan) — pengguna jawab "cuma Shopee" →
Tokopedia/TikTok TIDAK ditambahkan ke CV.

## CV Versi ATS
Rina Wulandari
Bandung · 0857xxxxxxx · rina.w@email.com

RINGKASAN PROFIL
Berpengalaman 5 tahun sebagai Admin Toko dengan interaksi langsung ke pelanggan
(tatap muka & WhatsApp), termasuk mengelola penjualan di Shopee (upload produk,
membalas chat pembeli)...

PENGALAMAN KERJA
Admin Toko — Toko Sembako Berkah (2019-sekarang)
- Melayani pembeli langsung dan lewat WhatsApp dengan ramah dan responsif
- Mencatat stok dan menginput data penjualan harian
- Mengelola toko di Shopee: upload produk dan membalas chat pembeli

PENDIDIKAN
SMA — (nama sekolah belum diisi pengguna, ditandai [belum diisi])

KEAHLIAN
Layanan pelanggan, Shopee (upload produk, chat), pencatatan stok
[isi hanya bila benar-benar Anda kuasai: multitasking, bekerja shift]
[Tokopedia/TikTok Shop TIDAK dicantumkan — pengguna konfirmasi belum pernah pakai]

## Surat Lamaran (Formal) / Email Singkat
(menonjolkan pengalaman Shopee + 5 tahun layanan pelanggan, menyebut kesediaan
menyesuaikan shift kerja)

## Checklist
- [x] Jabatan "Admin Toko" tidak diubah jadi "Customer Service" meski melamar CS —
      dibiarkan sesuai fakta, kecocokan dijelaskan lewat isi poin
- [x] Tokopedia/TikTok tidak dikarang sebagai pengalaman
- [x] "Multitasking" (kata dari lowongan, tidak ada di data pelamar) tidak diklaim —
      dijadikan isian `[...]` untuk dikonfirmasi pengguna
- [x] Gaji 3,8 juta dari isian pengguna sendiri
```

## Catatan penguji (audit contoh 2026-10-13)
- **Skill tidak boleh memasukkan keahlian/pengalaman yang tidak dimiliki pelamar.**
  Versi awal contoh ini mencantumkan "multitasking" di KEAHLIAN padahal kata itu
  hanya ada di lowongan (dan di daftar "belum terlihat"), bukan di data pelamar.
  Kini diganti `[isi hanya bila benar-benar Anda kuasai: ...]` (SKILL.md Langkah 5 &
  checklist "tidak dikarang").
- Skor akhir evaluasi: versi awal menulis 71,7/100; dihitung ulang dengan rumus bobot
  `references/evaluasi-kecocokan.md` = **73,75 → 73,8/100** — label tetap "Cocok".
  Perbaikan keahlian di atas tidak mengubah skor dimensi (Keahlian 70 dinilai dari
  pengalaman Shopee, bukan dari "multitasking"). Skill ini tidak punya script untuk
  skor evaluasi; `scripts/skor_kecocokan.py` hanya menghitung kata kunci.

## Verifikasi manual (uji awal Akun B)
- Skor evaluasi kecocokan dihitung ulang: (70×0.35 + 65×0.30 + 100×0.15) /
  (0.35+0.30+0.15) = (24,5+19,5+15) / 0,80 = 59 / 0,80 = 73,75 — **berbeda dari
  71,7 yang ditulis simulasi di atas.** Ini defect kecil di simulasi/perhitungan
  manual (bukan bug script, karena evaluasi kecocokan dihitung manual oleh agent,
  tidak lewat script Python). `references/evaluasi-kecocokan.md` **tidak
  menyediakan rumus pembulatan/pembobotan ulang eksplisit** saat satu dimensi
  "tidak dinilai" — hanya dicontohkan sekali di `06-profil-induk-dan-evaluasi-
  kecocokan.md` (uji v1.1.0 asli). Berisiko agent lain menghitung ulang bobot
  dengan cara berbeda dan mendapat skor label yang bisa berbeda tipis. Temuan RINGAN.
- Jabatan asli "Admin Toko" **tidak diganti** jadi "Customer Service" — sesuai
  aturan tidak mengarang riwayat jabatan.
