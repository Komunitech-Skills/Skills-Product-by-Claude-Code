# HASIL UJI — balas-chat-cs

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Lingkungan:** simulasi agent; skill tanpa script
- **Skenario:** 01–05 + uji A/B (`00-pembanding-tanpa-skill.md`) + banding pesaing (`00-banding-pesaing.md`)

## Audit keamanan
- Tidak ada script. SKILL.md, README, `references/alur-komplain.md`, `references/nada-brand.md`, `templates/bank-jawaban.md`: tidak ada prompt injection, tidak ada instruksi mengirim data. Ada pengaman yang baik: larangan meminta KTP/PIN/OTP/password, template "waspada penipuan", data pelanggan tidak disimpan ke bank jawaban (UU PDP). **Aman.**

## Verifikasi fakta
- Tidak ada angka yang dihitung (tidak ada script) — verifikasi angka: **tidak ada script**.
- Dasar hukum di `references/alur-komplain.md`: UU 8/1999 Perlindungan Konsumen dan UU 27/2022 PDP — relevan dan benar; tanpa tanggal "berlaku per" (ringan).
- Klaim tentang aturan marketplace (larangan transaksi di luar platform, larangan imbalan ulasan) diberi catatan "cek Seller Center" — jujur, tidak dikarang sebagai kepastian.

## Skor

| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description) | 9 | WA + marketplace, FAQ & komplain, quick reply; batas dengan balas-ulasan jelas |
| Kemudahan awam | 9 | Tempel chat → balasan; bank jawaban dengan `[isi]` |
| Kualitas output | 9 | E-S-T konsisten, versi singkat, catatan admin yang praktis |
| Akurasi (angka/fakta) | 9 | Tidak mengarang stok/estimasi/kebijakan; dasar hukum benar |
| Penanganan input kurang | 9 | Tanya sekali, default jelas |
| Penanganan di luar cakupan | 8 | Rujukan ke skill lain; tanpa kalimat cadangan bila skill rujukan tidak ada |
| Keamanan | 10 | Bersih, ada pengaman data sensitif |

## SKOR AKHIR: **8 / 10** — LULUS

Uji A/B: skill jelas lebih baik (versi tanpa skill menjanjikan "pasti sampai sebelum lusa" dan defensif menyalahkan kurir). Banding pesaing: `wa-reply-id` (manairalabs/bicara-skills, MIT) adalah pesaing Indonesia yang kompetitif dan natural, tetapi kalah pada larangan salah janji (contohnya sendiri mengarang estimasi & kompensasi), panduan admin, aturan marketplace, mode bank jawaban, dan kasus sensitif. Selisih "sedang", bukan telak — nilai tambah perlu dijaga. Tidak ada cacat berat.

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
- Tidak ada.

### Ringan
1. `templates/bank-jawaban.md` tidak punya template untuk kategori berizin (kosmetik/pangan: nomor BPOM/PIRT, halal, klaim manfaat, kedaluwarsa), padahal README menyasar skincare & kuliner. **Saran:** tambah bagian "Izin edar & klaim produk" dengan peringatan "hanya bila benar ada".
2. Janji waktu tindak lanjut ("paling lambat [waktu]") tidak dikaitkan dengan jam operasional toko. **Saran:** di Input, tambah "jam operasional" dengan default `[isi]`, dan di langkah 3 minta waktu tindak lanjut dalam jam kerja.
3. `references/alur-komplain.md` bagian "Dasar" tanpa tanggal cek ("per 2026-09-23"), padahal CLAUDE.md Tahap 4.5 memintanya. **Saran:** tambahkan.
4. Dari banding pesaing (ide): deteksi register dari gaya chat pelanggan ("dong/sih" → santai), katalog frasa kaku vs natural, dan aturan "jangan minta pelanggan mengulang info yang sudah diberikan" sebagai butir checklist.
5. Tidak ada kalimat cadangan bila `balas-ulasan-pelanggan`/`tagih-piutang`/`follow-up-prospek` tidak dimiliki pembeli. **Saran:** satu kalimat di "Kapan TIDAK digunakan": "jika skill itu tidak ada, beri satu draf netral singkat dan jelaskan perbedaannya".
