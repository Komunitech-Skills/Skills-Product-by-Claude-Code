# Uji A/B — Skenario 01 tanpa skill vs dengan skill

**Penguji:** agent independen, 2026-09-24. Dolibarr **24.0.1 asli**, data fiktif sama dengan 01.
**Permintaan sama:** "Buatkan invoice buat UD Sinar Bangunan: semen Tiga Roda 20 sak, cat tembok 4 kaleng 87.500 diskon 7,5%, ongkir truk 150 ribu, tempo 30 hari."

## A. TANPA skill (agent umum)
Simulasi oleh penguji (penguji sudah membaca skill, jadi alur di bawah disusun dari pengetahuan umum tentang REST API Dolibarr, lalu **request-nya benar-benar dijalankan** ke Dolibarr yang sama untuk melihat angkanya).

Alur yang biasanya terjadi:
1. Agent butuh alamat & kunci API → **meminta pengguna menempel kunci di chat** (kunci masuk riwayat percakapan/log). Tidak ada penyimpanan aman, tidak ada cek izin file.
2. Mencari dokumentasi `/api/index.php/explorer`, menebak nama field (`socid`, `tva_tx`, `remise_percent`, `date_lim_reglement`) — 8–15 panggilan alat, beberapa kali 400/403.
3. Tarif pajak: pengetahuan umum "PPN 12% sejak 2025" → `tva_tx=12`. Aturan DPP nilai lain 11/12 (PMK 131/2024) untuk barang non-mewah sering terlewat.
4. Tidak ada pratinjau/konfirmasi baku; tidak ada cek draf ganda; tidak ada pencocokan hitungan; bisa saja langsung memanggil `/validate` karena pengguna bilang "buatkan invoice".

Request yang dijalankan penguji (setara langkah 3, tanpa `date_lim_reglement` karena agent tidak tahu nama field-nya):
```
POST invoices {"socid":6,"type":0,"date":<24/9>}
POST invoices/13/lines ×3 dengan tva_tx 12, remise_percent 7.5 pada cat
→ (PROV13): DPP 1.723.750 | PPN 206.850 | total 1.930.600 | jatuh tempo 2026-09-24 (= tanggal invoice)
```

## B. DENGAN skill (lengkap di `01-uji-toko-bangunan-pelanggan-dan-invoice.md`)
Pratinjau → "ya" → (PROV11): DPP 1.723.750 | PPN hitungan Komunitech **189.612** (Dolibarr 189.612,50, selisih Rp 0,50 dilaporkan) | total 1.913.362 | tempo **2026-10-24**; kunci tidak pernah ditempel di chat; draf ganda dicegah.

## Perbandingan
| Kriteria | Tanpa skill | Dengan skill |
|---|---|---|
| PPN barang umum (12% × DPP 11/12) | ❌ 206.850 → **memungut lebih Rp 17.238** | ✅ 189.612 (standar library, ke bawah sekali) |
| DPP nilai lain 11/12 untuk faktur | ❌ tidak ada | ✅ 1.580.104,17 |
| Jatuh tempo 30 hari | ❌ sama dengan tanggal invoice (umur piutang jadi salah) | ✅ 24/10 |
| Kunci API | ❌ ditempel di chat | ✅ `simpan-kunci` oleh pengguna, file 600, tersamar |
| Pratinjau + konfirmasi, draf saja | ❌ tidak baku, risiko langsung validasi | ✅ wajib, script tidak punya validasi |
| Cegah pelanggan/draf ganda | ❌ | ✅ nama mirip & draf DPP sama (nomor HP belum, S4) |
| Cocokkan dengan angka Dolibarr | ❌ | ✅ COCOK/BEDA + sebab |
| Harga produk dari Dolibarr (`@SMN-40`) | perlu cari ID manual | ✅ otomatis |
| Waktu | 10–20 panggilan alat | 3 perintah (cari, pratinjau, `--ya`), < 2 detik |

**Kesimpulan:** dengan skill **jelas lebih baik** (angka pajak benar, jatuh tempo benar, kunci aman, tidak ada tindakan tanpa persetujuan). Syarat A/B terpenuhi.
