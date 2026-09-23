# Contoh 01 — Pitch deck UMKM ke investor (laundry kiloan)

## Skenario
S1, permintaan normal. Pemilik laundry kiloan dua outlet mencari dana ekspansi dari investor. Data cukup lengkap untuk traksi & kebutuhan dana, tapi data pasar, kompetitor, dan proyeksi belum ada.

## Input pengguna
```
Halo, tolong bikinin pitch deck buat ketemu investor minggu depan. Usahaku laundry kiloan namanya Bersih Kilat, udah 2 outlet di Depok sejak 2023. Omzet gabungan sekarang sekitar Rp 38 juta sebulan, pelanggan aktif 620 orang, 40% pesan lewat WA. Harga Rp 8.000/kg, ada layanan antar-jemput. Mau cari dana Rp 450 juta buat buka 3 outlet baru di Depok & Bogor, tawarkan 15% saham. Timnya aku (owner, dulu supervisor laundry hotel 6 tahun) sama adik aku yg pegang keuangan.
```

## Output
File nyata: [`pitch-bersih-kilat.html`](pitch-bersih-kilat.html) (13 slide, 13,7 KB, palet "Biru Korporat", font Georgia + Segoe UI/Arial).

Susunan slide (mengikuti `templates/pitch-investor.md`):
1. Sampul — Bersih Kilat Laundry, tagline, `[isi nama Anda]`
2. Masalah — 3 poin + `[isi data/survei pelanggan jika ada]`
3. Solusi — 3 kartu: pesan via WA (40%), antar-jemput, Rp 8.000/kg
4. Cara kerja — 4 langkah
5. Pasar — semua angka pasar berupa placeholder berlabel "estimasi" (tidak dikarang)
6. Model bisnis — tabel harga (ongkir & layanan satuan `Rp [isi]`)
7. Traksi — Rp 38.000.000/bulan · 620 pelanggan · ±4.750 kg/bulan (Rp 38.000.000 ÷ Rp 8.000)
8. Kompetitor — tabel 3 kolom, harga pesaing `Rp [isi]`
9. Rencana pertumbuhan — 2 → 5 outlet
10. Tim — 2 kartu
11. Kebutuhan dana — Rp 450.000.000 untuk 15% saham; Rp 150.000.000 per outlet; valuasi tersirat pasca-pendanaan Rp 3.000.000.000
12. Proyeksi — omzet per outlet saat ini Rp 19.000.000; proyeksi & asumsi `[isi]`
13. Penutup — WA 0812-0000-xxxx

Balasan ke pengguna:
```
Presentasi Pitch Deck Bersih Kilat Laundry sudah jadi: pitch-bersih-kilat.html (13 slide)

Cara pakai:
- Buka file-nya dua kali klik, atau tarik ke jendela browser (Chrome/Edge/Safari) — bisa dibuka di laptop maupun HP, tanpa internet.
- Navigasi: tombol panah kiri/kanan atau geser jari (di HP), atau klik tombol ‹ › di bawah layar.
- Cetak jadi PDF: buka file → Ctrl+P (Windows) / Cmd+P (Mac) → pilih "Simpan sebagai PDF" → orientasi Lanskap.

Asumsi yang dipakai: palet "Biru Korporat" (belum ada warna brand); dana dibagi rata Rp 150.000.000 per outlet (Rp 450.000.000 ÷ 3); valuasi Rp 3.000.000.000 = Rp 450.000.000 ÷ 15% (pasca-pendanaan).
Bagian yang masih perlu Anda lengkapi: nama Anda & adik, data pasar (BPS/estimasi), harga pesaing, ongkos antar-jemput, rincian penggunaan dana per pos, proyeksi omzet 5 outlet + asumsinya, email.
Hasil cek otomatis: LULUS, tanpa peringatan.
```

## Catatan penguji
- **Bagus:** struktur 13 slide sesuai template; tidak ada angka pasar/proyeksi yang dikarang (placeholder kuning jelas); semua Rupiah format `Rp 1.250.000`; angka turunan (kg/bulan, valuasi, per outlet) dihitung eksplisit dan benar (diverifikasi: 38.000.000/8.000 = 4.750; 450.000.000/0,15 = 3.000.000.000).
- **Uji teknis:** 0 permintaan jaringan (Playwright, halaman dimuat dari `file://`); tidak ada elemen meluber di 13 slide pada kanvas 1920×1080; `validasi_html.py` LULUS.
- **Cacat (dari kerangka skill, bukan dari isi):** cetak PDF lewat Chromium memotong sisi kanan setiap slide — kolom "Nominal" (Rp 150.000.000 / Rp 450.000.000) hilang di A4 lanskap maupun Letter tegak. Di HP tegak 390px, skala panggung 0,203 → teks isi ±6,5px (harus diputar ke lanskap: ±11,6px, terbaca). Lihat HASIL-UJI.md.
- Kerangka hanya menyediakan gaya h1/h2/p/li; kartu angka, tabel, dua kolom, penanda `[isi]` harus dirancang sendiri oleh agent → tampilan antar-agent bisa tidak konsisten.
