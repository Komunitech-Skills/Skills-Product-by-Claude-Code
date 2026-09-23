# Uji A/B — Tanpa Skill vs Dengan Skill (Skenario 1: Admin Gudang)

Input pengguna sama persis dengan `01-admin-gudang.md`.

## Output TANPA skill (AI agent biasa, tanpa membaca SKILL.md apa pun)

```
Tentu, ini CV yang sudah disesuaikan untuk Anda:

SITI RAHMA
Bekasi | 0812-0000-1111 | siti.rahma@email.com

RINGKASAN
Admin Gudang berpengalaman dengan kemampuan manajemen inventory, WMS, dan
sistem barcode scanning. Teliti, disiplin, dan mampu bekerja di bawah tekanan
untuk memastikan kelancaran operasional gudang.

PENGALAMAN KERJA
Admin Gudang, CV Berkah Jaya (2022-2024)
• Mengelola sistem inventory dan stock opname menggunakan aplikasi WMS
• Mengoperasikan barcode scanner untuk pencatatan barang masuk/keluar
• Berkoordinasi dengan tim purchasing dan pengiriman untuk kelancaran logistik
• Menjaga kerapian dan keamanan gudang sesuai SOP

PENDIDIKAN
SMK Akuntansi, SMK Negeri 3 Bekasi (2020)

SKILLS
Microsoft Excel (VLOOKUP, Pivot Table) | Inventory Management | WMS | Barcode
Scanning | Teliti | Disiplin

Semoga membantu! CV ini sudah saya sesuaikan dengan kata kunci di lowongan biar
peluang lolos ATS-nya lebih tinggi.
```

## Output DENGAN skill
Lihat `01-admin-gudang.md`.

## Penilaian singkat
Tanpa skill, AI **mengarang** tiga hal yang tidak pernah disebutkan pengguna:
"aplikasi WMS", "barcode scanner", dan "sesuai SOP" — padahal di input pengguna
hanya disebut "catat keluar masuk barang pakai Excel dan kartu stok manual" dan
"bantu stock opname". AI tanpa skill langsung menambahkan kata kunci dari
lowongan ke CV tanpa mengecek apakah pengguna benar-benar punya pengalaman itu —
persis pola berbahaya yang secara eksplisit dilarang di SKILL.md (Langkah 4,
bagian "Kapan TIDAK digunakan"). Ini bukan cuma soal gaya tulisan: kalau CV ini
dipakai melamar, Siti bisa ditanya soal WMS/barcode scanner saat wawancara dan
ketahuan tidak pernah memakainya — merusak kredibilitasnya.

Dengan skill: kata kunci yang belum ada di CV pengguna (WMS, barcode) **ditanyakan
dulu**, bukan langsung ditambahkan, dan baru dimasukkan setelah dikonfirmasi.
Skill juga menghitung skor kecocokan lewat script (bukan diperkirakan), menyaring
kata kunci yang tidak relevan (nama perusahaan, kata umum), dan menyertakan
checklist etika data pribadi + disclaimer ATS yang tidak muncul sama sekali di
output tanpa skill.

**Kesimpulan: skill memberi nilai tambah yang jelas dan signifikan** — bukan cuma
hasil yang lebih rapi, tapi mencegah cacat serius (CV berisi klaim palsu) yang
justru muncul secara default pada AI tanpa skill.
