# Skenario 6 — Normal: Profil Pengalaman Induk + Evaluasi Kecocokan Lowongan

Fitur baru versi 1.1.0. Menguji alur: pengguna belum punya profil induk → dibuat sekali →
dipakai untuk menilai kecocokan lowongan (skor + alasan + celah) sebelum CV disusun.

## Input pengguna
```
Saya belum pernah pakai skill ini. Tolong bikinkan profil pengalaman saya dulu, terus
nilai cocok nggak saya sama lowongan ini:

Lowongan: Staff Finance & Accounting
PT Cahaya Abadi Sejahtera - Surabaya (WFO, tidak bisa remote)

Kualifikasi:
- Min. D3/S1 Akuntansi
- Pengalaman min. 2 tahun di bidang finance/accounting
- Menguasai software akuntansi (Accurate/MYOB/SAP)
- Memahami perpajakan dasar (PPN, PPh 21/23)
- Teliti dan mampu bekerja dengan target closing bulanan
- Domisili Surabaya atau bersedia pindah

Gaji: Rp 6.000.000 - Rp 7.500.000

Data saya: Dewi Anggraini, tinggal di Malang, HP 0813-1111-2222, email dewi.a@email.com.
Pendidikan: D3 Akuntansi, Politeknik Negeri Malang, lulus 2019.
Pengalaman: Staff Accounting di CV Mitra Jaya (2020-2024), input jurnal harian pakai
Excel, bantu rekap PPN bulanan (dibantu konsultan pajak), belum pernah pakai software
akuntansi khusus. Ekspektasi gaji saya sekitar Rp 6.500.000. Saya bersedia pindah ke
Surabaya kalau diterima.
```

## Output (ringkas)
```
## Profil Pengalaman Induk
(disusun lengkap sesuai references/profil-induk.md — Data Diri, Pendidikan, Pengalaman
Kerja, Keahlian, Preferensi Karier. Ditampilkan penuh ke pengguna dengan catatan:
"Simpan teks ini sebagai file di komputermu, tempel lagi untuk lamaran berikutnya.")

## Evaluasi Kecocokan Lowongan: Staff Finance & Accounting di PT Cahaya Abadi Sejahtera

**Saringan wajib:** LULUS semua — pendidikan D3 Akuntansi memenuhi syarat minimal;
lokasi: bersedia pindah ke Surabaya (sesuai pernyataan pengguna); gaji: ekspektasi
Rp 6.500.000 berada dalam rentang lowongan (Rp 6.000.000–7.500.000) → PAS.

| Dimensi | Skor | Catatan |
|---|---|---|
| Keahlian & alat kerja | 45/100 | Excel dikuasai, tapi belum pernah pakai Accurate/MYOB/SAP (disebut wajib di lowongan) |
| Pengalaman | 70/100 | 4 tahun di accounting, fungsi kerja relevan (jurnal, PPN), meski belum pegang PPh 21/23 langsung |
| Preferensi & arah karier | — | Belum cukup data di profil induk, tidak dinilai |
| Syarat administratif | 90/100 | Pendidikan & lama pengalaman terpenuhi |

**Skor akhir: 63/100 — Cocok, lamar sambil perkuat celah**

### Kenapa cocok
- Pengalaman 4 tahun di accounting dengan tanggung jawab yang relevan (jurnal, rekap PPN)
- Ekspektasi gaji pas di rentang yang ditawarkan
- Bersedia pindah sesuai syarat lokasi

### Celah yang perlu diperhatikan
- Belum pernah memakai software akuntansi (Accurate/MYOB/SAP) — sebutkan kesediaan
  belajar cepat di surat lamaran, jangan mengaku sudah bisa
- Pemahaman PPh 21/23 masih dibantu konsultan pajak, bukan dikerjakan mandiri

### Rekomendasi
Lamar — skor cukup baik dan gaji sesuai. Di surat lamaran, tonjolkan pengalaman jurnal &
PPN, dan sebutkan jujur bahwa kamu cepat belajar sistem baru (bukan berpura-pura sudah
menguasai Accurate/MYOB/SAP).

Lanjut ke penyusunan CV & surat lamaran?
```

## Verifikasi manual
- Skor akhir bukan skor kata kunci (yang dihitung script terpisah) — ini skor evaluasi
  kecocokan berbasis profil induk, dihitung manual mengikuti bobot di
  `references/evaluasi-kecocokan.md` (Keahlian 35%, Pengalaman 30%, Preferensi 20% — di
  sini tidak dinilai karena data belum ada, jadi bobot dihitung ulang proporsional dari
  dua dimensi yang tersedia + administratif 15%). Dicek manual: (45×0.35 + 70×0.30 +
  90×0.15) / (0.35+0.30+0.15) = 5025/80 = 62,8 → dibulatkan 63. Konsisten dengan output.
- Tidak ada angka gaji pasar yang dikarang — hanya membandingkan angka yang sudah
  dinyatakan pengguna dan lowongan.
- Software akuntansi yang "belum dikuasai" tidak dipaksakan masuk CV sebagai keahlian.
