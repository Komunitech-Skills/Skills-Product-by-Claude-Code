# Riwayat perubahan — pph-final-umkm

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.4 (2026-10-14)
Perbaikan dari uji OpenClaw sebelum/sesudah penguji independen 14 Oktober 2026 atas versi 1.0.3 (belum lolos: rata-rata tanpa skill 6,8, dengan skill 6,1).
- **PPh 22 marketplace kini dikreditkan** sesuai FAQ DJP PMK 37/2025 versi 1 Juli 2026 (no. 14–15): per bulan dihitung kurang setor (disetor sendiri) atau lebih dipungut (dapat diajukan pengembalian), selisih dibulatkan ke bawah. Status "SUDAH LEWAT" hanya untuk bulan yang masih kurang setor. Pengingat surat pernyataan omzet ke marketplace (FAQ no. 9 & 16).
- **Jangka waktu tarif 0,5% mengikuti PP 20/2026** (naskah resmi JDIH Kemenkeu): orang pribadi & PT perorangan tanpa batas tahun (Pasal 59 PP 55/2022 dihapus); koperasi 4 tahun dengan peralihan s.d. 2029; CV/firma/PT biasa hanya meneruskan sisa jangka waktu lama. Kalimat "tahun TERAKHIR" untuk orang pribadi/PT perorangan dihapus.
- **Script mencetak sendiri** tanggal acuan ("Hari ini"), status BESOK/HARI INI/SUDAH LEWAT, batas setor terdekat, subtotal data nyata vs total + proyeksi (`--proyeksi-mulai`), sehingga AI tidak menghitung/menambah tanggal sendiri. SKILL.md melarang AI menghitung ulang atau menambah angka; bila hitungan gagal, AI mengatakannya dan meminta data.
- Mode `--kemungkinan` untuk data belum lengkap (satu bulan omzet): tabel kemungkinan orang pribadi/badan + batas setor, lalu tanya maks. 3 hal.
- Format Rupiah standar library ("Rp1.250.000", tanpa spasi); tanggal ditulis lengkap dengan nama hari; teks hasil tanpa istilah teknis (mis. nama opsi).
- Tes: 18 tes (termasuk kredit PPh 22 kurang/lebih/tanpa PPh 22, pembulatan selisih, 300 kasus acak dicocokkan dengan hitungan independen, jangka waktu PP 20/2026, proyeksi, mode kemungkinan).

## Catatan revisi 1.0.3 (2026-10-01)
- Batas setor yang jatuh di hari libur (Sabtu, Minggu, libur nasional, cuti bersama 2026–2027) kini otomatis digeser ke hari kerja berikutnya sesuai PMK 81/2024 Pasal 100, dan wajib disebut AI di balasan (temuan uji OpenClaw: 15 Nov 2026 hari Minggu tidak disebut).
- Opsi `--tahun-terdaftar`: menghitung batas jangka waktu tarif 0,5% menurut PP 55/2022 Pasal 59 (orang pribadi 7 tahun; mis. NPWP 2021 → s.d. 2027), dengan peringatan bahwa perubahan oleh PP 20/2026 belum diverifikasi.
- Instruksi: script dijalankan dari subfolder `scripts/` di folder skill; catatan & dasar aturan disalin apa adanya ke chat. 5 tes otomatis baru (`tests/`).
