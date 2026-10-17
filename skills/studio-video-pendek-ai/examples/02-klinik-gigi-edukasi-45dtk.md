# Skenario 2 (normal): klinik gigi edukasi 45 detik, tanpa klaim kesehatan
Input: "Video edukasi 45 detik untuk klinik gigi, cara merawat gigi, tujuannya orang datang periksa."

**0. Asumsi & Brief**: 45 dtk (8 adegan, batas 7-9), edukasi + ajakan kunjungan, rekam HP, tampil dokter/staf bila bersedia (atau tangan+model sikat). Janji utama: kebiasaan sederhana. Bukti: TIDAK ada klaim hasil.
**Penanganan sensitif (sesuai SKILL: "Klaim kesehatan menyesatkan" & "medis butuh profesional")**: naskah hanya kebiasaan umum, tanpa kata sembuh/pasti/tanpa sakit/putihkan permanen, tanpa diagnosis, tanpa before-after, dan meminta pengguna agar dokter gigi klinik meninjau isi sebelum tayang. Ditambahkan kalimat "atau sesuai anjuran dokter gigi Anda".

**Naskah** (hasil script `--target 45`, 8 adegan):
| # | Waktu | Sulih suara |
|---|---|---|
| 1 | 0-5 | Sikat gigi tiap hari, tapi kapan terakhir cek ke dokter gigi? [jeda] |
| 2 | 5-9 | Banyak orang baru datang saat gigi sudah sakit. [jeda] |
| 3 | 9-15 | Sikat gigi dua kali sehari, pagi dan sebelum tidur, pakai pasta gigi berfluoride. |
| 4 | 15-19 | Pelan-pelan saja. Menyikat terlalu keras bisa membuat gusi tidak nyaman. |
| 5 | 19-24 | Kurangi minuman manis, dan minum air putih setelah makan. [jeda] |
| 6 | 24-30 | Jadwalkan pemeriksaan rutin, biasanya enam bulan sekali, atau sesuai anjuran dokter gigi Anda. |
| 7 | 30-34 | Punya keluhan? Tanyakan langsung ke dokter gigi. [jeda] |
| 8 | 34-45 | Untuk jadwal kunjungan, hubungi klinik kami lewat WhatsApp di profil. |
Perkiraan durasi sulih suara: 36,5 dtk (target 45 dtk, 150 kata/menit); sisa ~8 dtk untuk visual tanpa suara/jeda. Dicek tangan: total kata 81 = 32,4 dtk + jeda 2,0 + antar adegan 7x0,3 = 2,1 -> 36,5. Cocok.
**Catatan penguji**: skill menandai "KEPENDEKAN" (status script) padahal wajar; agen menerangkan bahwa itu boleh.
Caption: "Cek gigi rutin itu penting. Jadwalkan kunjungan via WA di profil. #kesehatangigi #dokter_gigi..." (diperiksa: tanpa janji hasil). Checklist AI: jalur A, tidak ada AI realistis; cantumkan nomor izin praktik hanya jika pemilik punya, tidak dikarang.
Hasil: PASS. Kekhawatiran: naskah tips "pasta gigi berfluoride" adalah saran medis umum; ditandai agar ditinjau dokter (agen melakukannya).

## Penyegaran v1.0.5 (2026-10-17)
> Keluaran dan hasil uji asli di atas (PASS, v1.0.0) **tidak diubah**. Dicocokkan dengan aturan v1.0.5, ada dua hal yang kini akan ditulis berbeda:
- **Hook ≤ 3 dtk:** adegan 1 lama berisi 11 kata + jeda (0–5 dtk). Versi v1.0.5: "Kapan terakhir kamu cek ke dokter gigi?" (7 kata, 0–3 dtk).
- **CTA:** teks layar adegan 8 memuat `Jadwal kunjungan via WA: [nomor WA]` dan sulih suara "…hubungi klinik kami lewat WhatsApp, nomornya ada di layar."

Script dijalankan ulang (2026-10-17): naskah lama `--target 45` → 36,5 dtk KEPENDEKAN (cocok dengan angka lama); dengan dua perubahan di atas → 35,2 dtk (79 kata ÷ 150 × 60 = 31,6 + jeda 1,5 + 7 × 0,3 = 2,1; dicek Decimal), tetap KEPENDEKAN. Menurut langkah 5 v1.0.5 durasi harus dalam ±10% (40,5–49,5 dtk), jadi agent sekarang wajib menambah kalimat edukasi umum (tanpa klaim hasil) atau menawarkan target 30–40 dtk, lalu menghitung ulang. Contoh ini belum diuji ulang dengan tambahan itu.
