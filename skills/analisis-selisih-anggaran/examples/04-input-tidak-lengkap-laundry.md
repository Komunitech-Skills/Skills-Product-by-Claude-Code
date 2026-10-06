# 04 — Input tidak lengkap: laundry, sebagian realisasi kosong

> Contoh pembuat skill (v1.0.0). Angka dari `scripts/selisih.py --file examples/data/04-laundry-tidak-lengkap.csv --format teks`; diverifikasi ulang dengan Python terpisah: laba (tanpa gaji & gas) 36.700.000 → 32.800.000; kiloan −10,86%; satuan +13,75%; deterjen +11,43%; listrik +28,57%.

## Pesan pengguna
"Laundry saya bulan ini: anggaran laundry kiloan 35 jt, dapat 31,2 jt. Satuan 8 jt dapat 9,1 jt. Deterjen & pewangi 3,5 jt jadi 3,9 jt. Listrik air 2,8 jt jadi 3,6 jt. Gaji 9 jt sama gas 1,2 jt, realisasinya belum saya rekap. Gimana?"

## Perilaku yang diharapkan
Gaji dan gas tidak punya realisasi → tidak dihitung, dan laba **tidak** disebut laba akhir. Tetap kerjakan 4 pos yang lengkap, lalu tanya di akhir (maks. 3).

## Contoh balasan chat
**Rekap sementara (4 dari 6 pos): pendapatan kurang Rp2.700.000 (−6,3%), biaya yang sudah ada naik Rp1.200.000 (+19,0%)**
Penyebab terbesar: laundry kiloan kurang Rp3,8 jt. Gaji dan gas belum dihitung, jadi laba bulan ini belum bisa disimpulkan.

| Pos | Selisih | Keterangan |
|---|---|---|
| Laundry kiloan | −Rp3.800.000 (−10,9%) | merugikan; terbesar |
| Laundry satuan | +Rp1.100.000 (+13,8%) | menguntungkan |
| Listrik & air | +Rp800.000 (+28,6%) | merugikan |
| Deterjen & pewangi | +Rp400.000 (+11,4%) | merugikan |
| Gaji, gas | belum dihitung | realisasi belum ada |

Dari 4 pos ini saja, laba turun Rp3.900.000 dibanding rencana (Rp36.700.000 → Rp32.800.000, belum termasuk gaji & gas).

**Yang perlu dicek**
1. Kiloan: jumlah kilo yang turun, atau harga per kilo (promo/member)? Ada pelanggan langganan (kos, hotel kecil) yang berhenti?
2. Listrik & air +28,6%: mesin baru/pengering lebih sering dipakai, tarif naik, atau ada kebocoran?
3. Deterjen naik padahal kiloan turun: harga beli naik atau takaran per mesin bertambah?

**Tindakan:** cek daftar pelanggan langganan kiloan bulan lalu vs bulan ini; catat meteran listrik & air mingguan; samakan takaran deterjen per mesin.

**Asumsi:** ambang 5% atau Rp500 rb; gaji & gas belum dihitung.
Catatan: analisis untuk manajemen, bukan audit/nasihat keuangan; penyebab perlu dicek ke nota, rekening, dan catatan.

Supaya lengkap, mohon kirim:
1. Realisasi gaji dan gas bulan ini?
2. Berapa kilo laundry kiloan (rencana vs nyata)? Bisa saya pisahkan karena jumlah kilo atau harga.
3. Ada biaya lain yang belum masuk (sewa, plastik, internet)?
