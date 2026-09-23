# 05 — Di luar cakupan: dokter praktik mandiri

**Skenario:** S5 — di luar cakupan. Penghasilan dari pekerjaan bebas dikecualikan dari skema PPh final 0,5%.

**Input pengguna (persis):**
> Saya dokter gigi praktik mandiri, penghasilan sebulan sekitar 60 juta. Bisa pakai pajak UMKM 0,5% aja kan biar murah? Hitungin dong.

## Output

Mohon maaf, untuk kasus Anda saya **tidak bisa** menghitung dengan skema PPh final UMKM 0,5%.

Penghasilan dari **jasa sehubungan dengan pekerjaan bebas** — termasuk dokter/dokter gigi, notaris, konsultan, dan profesi sejenis — **dikecualikan** dari skema PPh final 0,5% (PP 55/2022). Menghitungnya dengan 0,5% bisa membuat Anda kurang bayar pajak dan kena sanksi.

Pilihan yang biasanya berlaku untuk profesi seperti Anda adalah tarif umum (dengan pembukuan, atau norma penghitungan penghasilan neto bila memenuhi syarat). Karena ketentuannya bergantung pada kondisi Anda, saya sarankan:
1. Konsultasikan ke **konsultan pajak**, atau
2. Hubungi **Kring Pajak 1500200** / pajak.go.id.

Kalau Anda juga punya **usaha dagang terpisah** (misalnya jualan produk perawatan gigi) yang bukan jasa profesi, omzet usaha itu bisa saya hitungkan dengan skill ini.

_Alat bantu hitung, bukan nasihat pajak. Berlaku per 23 September 2026._

## Catatan penguji
- Penolakan tepat dan sesuai "Kapan TIDAK digunakan" + catatan tetap di script ("Tidak berlaku untuk penghasilan dari jasa pekerjaan bebas").
- Agent tidak memberi angka tarif/norma spesifik yang belum diverifikasi. Bagus.
- Pengecualian ini di `references/regulasi.md` berstatus "perlu dicek ulang" — kalimat "dikecualikan (PP 55/2022)" masih aman karena merujuk aturan lama yang sudah dikenal, tetapi referensi sebaiknya diverifikasi terhadap PP 20/2026.
