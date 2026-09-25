# Skenario 04 — Input tidak lengkap: "mau ikut tender pemerintah gimana?"

> Uji independen, 2026-09-25. Agent mengikuti SKILL.md: info kurang → tanya **sekali**, maks. 5 pertanyaan bernomor; tetap memberi gambaran umum agar tidak kosong. Script tidak dijalankan (belum ada data).

## Input pengguna
"Mau ikut tender pemerintah gimana?"

## Jawaban agent
Bisa, saya bantu dari nol. Supaya sarannya pas, jawab 5 hal ini dalam satu pesan (boleh singkat):
1. Usaha Anda berbentuk apa (perorangan/CV/PT/koperasi) dan di NIB tertulis **usaha mikro/kecil/menengah**? KBLI-nya apa saja?
2. Sudah **PKP** (memungut PPN) atau belum?
3. Mau menjual **barang, jasa konstruksi, jasa lainnya, atau konsultansi**? Contoh barangnya?
4. Sudah punya **akun SPSE/INAPROC** dan pengalaman kontrak dengan instansi?
5. Sudah ada paket incaran? Jika ada: nama paket, HPS, batas unggah.

Sambil menunggu, gambaran jalurnya (paling mudah → paling berat):
| Jalur | Cocok untuk | Nilai (Perpres 16/2018 jo. 46/2025) |
|---|---|---|
| E-katalog / toko daring | Produk standar dengan harga tayang | Tanpa batas; ikuti Peraturan LKPP 2/2026 |
| Pengadaan langsung | Paket kecil, diundang Pejabat Pengadaan | Barang/jasa lainnya s.d. Rp200 jt; konstruksi s.d. Rp400 jt; konsultansi s.d. Rp100 jt |
| Tender | Paket lebih besar, bersaing terbuka di SPSE | Paket s.d. Rp15 M pada dasarnya untuk usaha mikro, kecil & koperasi |

Langkah awal yang pasti berguna:
- [ ] NIB aktif di OSS dengan **KBLI** sesuai barang/jasa yang akan dijual
- [ ] NPWP badan/usaha valid; tentukan status PKP
- [ ] Daftar & verifikasi akun penyedia di SPSE (spse.inaproc.id) / LPSE terdekat
- [ ] Konstruksi: SBU & SKK personel
- [ ] Siapkan arsip kontrak/BAST sebagai bukti pengalaman

Begitu Anda jawab, saya buatkan cek kelayakan, checklist dokumen, jadwal mundur, dan cek rincian harga.

*Ringkasan ini bukan nasihat hukum; yang mengikat adalah dokumen pemilihan & adendum di SPSE. Dasar aturan dicek 2026-09-25.*

## Penilaian penguji
- ✅ Pertanyaan sekali, 5 butir bernomor, bahasa awam; memberi nilai langsung (peta jalur) tanpa mengarang data pengguna.
- ✅ Tidak menjalankan script tanpa data; tidak mengklaim kelayakan.
- Catatan kecil: SKILL.md tabel Input menyebut default "jalankan alur lengkap 1–5" untuk kalimat umum; untuk input sekosong ini, bertanya lebih masuk akal — instruksi sedikit ambigu antara dua perilaku, tapi agent tetap berperilaku benar.
