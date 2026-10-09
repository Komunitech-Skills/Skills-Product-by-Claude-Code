# Uji 09 - Input tidak lengkap: "iklan saya harus mulai dari mana?"

Penguji independen, 2026-09-30, simulasi agent mengikuti SKILL.md v1.0.0.

## Permintaan
"Saya jual keripik pedas online, mau mulai iklan 2 juta. Bagusnya gimana? Oh ya margin saya 0,35."

## Perilaku sesuai skill
Info wajib yang kurang: harga rata-rata per pesanan, kanal/toko yang dimiliki, dan margin ambigu. Agent tidak menjalankan rencana; bila script dicoba dengan data yang ada, hasilnya:
```
GAGAL: Untuk tujuan 'penjualan' wajib isi --aov (harga rata-rata per pesanan) dan --margin (margin kotor, mis. 40%). Tanpa keduanya target CPA/ROAS tidak bisa dihitung.
GAGAL: --margin '0,35' ambigu: 0,4 berarti 0,4% atau 40%? Tulis '40%' (atau '0,4%').
```
Balasan agent (satu pesan, <= 6 pertanyaan bernomor):
> Siap bantu. Supaya pembagian uang dan batas ruginya dihitung, bukan dikira, saya perlu beberapa hal:
> 1. Harga rata-rata sekali pesan (mis. Rp85.000)?
> 2. Margin "0,35" maksudnya 35% atau 0,35%? (margin = sisa dari harga setelah modal, admin marketplace, dan ongkir yang Anda tanggung)
> 3. Jualan di mana saja: Shopee, TikTok Shop, IG, WA?
> 4. Tujuan bulan ini: penjualan langsung, atau dikenal dulu?
> 5. Ada momen khusus bulan depan (gajian, 11.11, promo)?
> 6. Sanggup bikin berapa video per minggu?
> Kalau ingin cepat, saya pakai asumsi: tujuan penjualan, Shopee + IG, 3 konten/minggu - tinggal kirim harga rata-rata dan margin.

## Penilaian
- Sesuai: tanya sekali, maks 6 butir, tidak menebak margin ambigu (script menolak `0,35` dengan pesan jelas), tawaran jalur cepat dengan asumsi.
- Kecil: pesan GAGAL margin memakai contoh "0,4" meski input "0,35" (sedikit membingungkan jika ditampilkan mentah).
