# Dasar aturan — SPT Tahunan PPh Orang Pribadi

Dicek **30 September 2026**. ✅ = diverifikasi dari naskah resmi/situs DJP · 🟡 = sumber sekunder konsisten · ⚠️ = PERLU REVIEW.
Riset lengkap + URL: `research/sources/spt-tahunan-op-2026-09-30.md` (repo kurator).

| Topik | Aturan yang dipakai | Status | Dasar |
|---|---|---|---|
| Tarif | 5% s.d. Rp60 jt · 15% >60–250 jt · 25% >250–500 jt · 30% >500 jt–5 M · 35% >5 M | ✅ | UU PPh Ps. 17 ayat (1) huruf a s.t.d.t.d. UU 7/2021 (HPP), sejak TP 2022 |
| PTKP | Diri Rp54 jt; kawin +Rp4,5 jt; istri digabung +Rp54 jt; tanggungan +Rp4,5 jt/orang, maks 3; keadaan 1 Januari | ✅ (istri digabung 🟡) | UU HPP Ps. 7 ayat (1); PMK 101/PMK.010/2016; PMK 168/2023 Ps. 9. Tidak ada perubahan PTKP sampai 2026 (🟡) |
| PKP | Dibulatkan ke bawah hingga ribuan rupiah penuh | ✅ | PMK 168/2023 Ps. 8 ayat (3)–(4) |
| Biaya jabatan (helper `--a1-bruto`) | 5% bruto, maks Rp500.000 × bulan (Rp6 jt/tahun) | ✅ | PMK 168/2023 Ps. 10 ayat (2) |
| NPPN | Peredaran bruto < Rp4,8 M; beritahu DJP ≤ 3 bulan pertama tahun pajak (Coretax, layanan AS.04-01); tanpa pemberitahuan dianggap pembukuan. Persen per KLU & wilayah di lampiran PER-17/PJ/2015 | ✅ syarat (situs DJP) · ⚠️ nomor pasal (450 vs 463 PMK 81/2024 s.t.d.d. PMK 1/2026) & klaim "selamanya pembukuan" | pajak.go.id/en/node/119175 |
| PPh final UMKM | Omzet 0,5% (PP 55/2022 jo. PP 20/2026) tidak ikut tarif Ps. 17; dilaporkan di lampiran penghasilan final/L-3B | 🟡 | DJP & Ortax 2026 |
| Zakat | Pengurang penghasilan bruto bila ke BAZNAS/LAZ/lembaga disahkan pemerintah + bukti setor; yang dipotong kantor sudah ada di bukti potong | 🟡 / ✅ (lewat kantor: PMK 168/2023 Ps. 10) | UU PPh Ps. 9 ayat (1) huruf g; PP 60/2010 |
| Kredit pajak | PPh 21 (A1/A2, bukan pegawai), PPh 22, PPh 23, PPh 24, PPh 25 dibayar; PPh final tidak dikreditkan | 🟡 | UU PPh Ps. 28 |
| PPh 25 tahun depan | (PPh terutang − PPh 21/22/23/24) ÷ 12 | 🟡 · ⚠️ penerapan untuk karyawan-saja (script hanya menampilkan bila ada usaha) | UU PPh Ps. 25 ayat (1) |
| Kurang bayar | Dilunasi sebelum SPT dikirim; Coretax membuat kode billing otomatis | ✅ | Coretaxpedia DJP |
| Lebih bayar | Restitusi atau kompensasi; pengembalian pendahuluan untuk OP tanpa usaha & OP usaha dengan LB ≤ Rp100 jt | 🟡 | UU KUP Ps. 17D; PMK 39/2018 s.t.d.t.d. PMK 209/2021 |
| Batas lapor | 31 Maret tahun berikutnya, tidak bergeser walau libur. TP 2025: diperpanjang ke 30 April 2026 (KEP-55/PJ/2026) | ✅ / 🟡 | PMK 81/2024 Ps. 169 |
| Sanksi | Telat lapor Rp100.000 (lewat STP); telat bayar KB → bunga per bulan tarif KMK (tidak dihitung) | 🟡 / ⚠️ | UU KUP Ps. 7 ayat (1), Ps. 9 |
| Formulir | 1770/1770S/1770SS dihapus sejak TP 2025 → satu SPT OP dinamis; induk Bagian A–K, Lampiran 1–5 | ✅ (DJP) · 🟡 kode lampiran | PER-11/PJ/2025; pajak.go.id/en/node/118848 |

**Pembulatan (standar library Komunitech):** neto NPPN ke rupiah terdekat; PKP ke bawah ribuan; PPh ke bawah rupiah. **Belum dicocokkan dengan hitungan otomatis Coretax.**

Kontak resmi: Kring Pajak 1500200 · https://www.pajak.go.id
