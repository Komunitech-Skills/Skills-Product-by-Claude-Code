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

## Pembaruan uji ulang v1.1.0 (2026-09-23)
File HTML di folder ini sudah **dibuat ulang dengan kerangka v1.1.0** (komponen `kartu-kpi`/`tabel-data`/`timeline`/`isi`, `@page 1920×1080`, overlay "putar HP", tombol Edit). Isi & angka sama dengan catatan di atas; cacat teknis v1.0 yang disebut di atas (PDF terpotong, teks kecil di HP tegak) sudah tidak terjadi — lihat bagian "Uji ulang v1.1.0" di `HASIL-UJI.md`.

## Penyegaran v1.1.6 (2026-10-17)
> Bagian ini menyegarkan **format balasan** agar sesuai SKILL.md v1.1.6. Isi slide, angka, catatan penguji, dan skor di atas **tidak diubah** (itu hasil uji asli v1.0–v1.1.x). Berkas `pitch-bersih-kilat.html` dicek ulang dengan `scripts/validasi_html.py`: lolos tanpa peringatan.

Perubahan format sejak uji asli: baris "Hasil cek otomatis: LULUS" diganti kalimat awam "Sudah dicek: ..."; cara cetak PDF mengikuti `@page 1920×1080` (margin "Tidak ada" + "Grafis latar", tanpa pilih orientasi); di kanal chat berkas `.html` dilampirkan sebagai dokumen dan jalur/folder komputer tidak disebut.

Balasan ke pengguna (format v1.1.6, kanal chat):
```
Presentasi Pitch Deck Bersih Kilat Laundry sudah jadi (13 slide). Filenya saya lampirkan sebagai dokumen.

Cara pakai:
- Buka file-nya dua kali klik, atau tarik ke jendela browser (Chrome/Edge/Safari) — bisa dibuka di laptop maupun HP, tanpa internet.
- Navigasi: tombol panah kiri/kanan atau geser jari (di HP), atau klik tombol ‹ › di bawah layar. Kalau HP dipegang tegak, akan muncul pesan untuk memutar ke posisi mendatar.
- Mau edit teks langsung? Klik "✏️ Edit" di pojok kanan bawah (hanya di laptop/komputer); di HP, minta saya yang mengubah teksnya lalu saya kirim ulang filenya.
- Cetak jadi PDF: buka file → Ctrl+P / Cmd+P → "Simpan sebagai PDF" → margin "Tidak ada" → centang "Grafis latar".

Asumsi yang dipakai: palet "Biru Korporat" (belum ada warna brand); dana dibagi rata Rp 150.000.000 per outlet (Rp 450.000.000 ÷ 3); valuasi Rp 3.000.000.000 = Rp 450.000.000 ÷ 15% (sesudah pendanaan; sebelum pendanaan Rp 2.550.000.000).
Bagian yang masih perlu Anda lengkapi: nama Anda & adik, data pasar, harga pesaing, ongkos antar-jemput, rincian penggunaan dana per pos, proyeksi omzet 5 outlet + asumsinya, email.
Sudah dicek: file bisa dibuka tanpa internet dan siap dicetak jadi PDF.
```

Angka dihitung ulang (Decimal, 2026-10-17): 38.000.000 ÷ 8.000 = 4.750 kg; 450.000.000 ÷ 3 = 150.000.000; 450.000.000 ÷ 0,15 = 3.000.000.000; 3.000.000.000 − 450.000.000 = 2.550.000.000; 38.000.000 ÷ 2 = 19.000.000. Semua cocok dengan isi di atas.

Rujukan bot Telegram asli (skenario yang sama, v1.1.6): `koordinasi/telegram-gelombang-A1-2026-10-17.md` — topik 1880/1881, TANPA 6,5 → DENGAN 8,0 (+1,5) **LULUS**; berkas `pitch-bersih-kilat.html` (13 slide) benar-benar terkirim sebagai dokumen. Sisa temuan di sana: satu pesan tambahan berisi kalimat proses, angka "2–3 jam/minggu" di slide Masalah tanpa label perkiraan, dan valuasi sebelum pendanaan tidak disebut (di balasan contoh di atas sudah ditambahkan sebagai saran format).
