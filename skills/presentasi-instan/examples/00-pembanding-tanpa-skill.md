# Uji A/B — S1 tanpa skill vs dengan skill

Permintaan sama dengan `01-pitch-investor-laundry.md` (pitch deck laundry Bersih Kilat ke investor). Versi "tanpa skill" dikerjakan sebagai AI agent biasa tanpa membaca skill apa pun; keduanya lalu dites dengan alat yang sama (Playwright/Chromium 1194, `validasi_html.py`, Chromium `--print-to-pdf`).

## Output A — tanpa skill
Satu file HTML, 10 "slide" berupa section tinggi layar (scroll-snap), font Inter dari Google Fonts. Kode lengkap:

```html
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bersih Kilat — Pitch Deck</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<style>
  :root { --primary:#0ea5e9; --dark:#0f172a; }
  html { scroll-snap-type: y mandatory; }
  body { margin:0; font-family:'Inter',sans-serif; color:var(--dark); }
  section { height:100vh; scroll-snap-align:start; display:flex; flex-direction:column; justify-content:center; padding:0 10vw; box-sizing:border-box; }
  section:nth-child(odd){ background:#f0f9ff; }
  h1 { font-size:4rem; margin:0; color:var(--primary); }
  h2 { font-size:2.5rem; color:var(--primary); margin-bottom:1rem; }
  li, p { font-size:1.4rem; line-height:1.6; }
  .grid { display:grid; grid-template-columns:repeat(3,1fr); gap:2rem; }
  .card { background:#fff; border-radius:12px; padding:1.5rem; box-shadow:0 4px 12px rgba(0,0,0,.08); }
  .big { font-size:2.2rem; font-weight:800; }
</style>
</head>
<body>
<section><h1>Bersih Kilat Laundry</h1><p>Laundry kiloan antar-jemput · Depok &amp; Bogor</p><p>Pitch Deck Investor 2026</p></section>
<section><h2>Masalah</h2><ul><li>Keluarga urban sibuk tidak sempat mencuci</li><li>Laundry lokal sering telat &amp; tidak konsisten</li><li>Tidak ada layanan antar-jemput yang terjangkau</li></ul></section>
<section><h2>Solusi</h2><p>Laundry kiloan Rp 8.000/kg dengan antar-jemput dan pemesanan via WhatsApp.</p></section>
<section><h2>Traksi</h2><div class="grid"><div class="card"><div class="big">Rp 38 jt</div>omzet/bulan</div><div class="card"><div class="big">620</div>pelanggan aktif</div><div class="card"><div class="big">40%</div>order via WA</div></div></section>
<section><h2>Peluang Pasar</h2><p>Pasar laundry Indonesia diperkirakan bernilai triliunan rupiah dan terus tumbuh seiring urbanisasi. Depok &amp; Bogor memiliki jutaan penduduk dengan banyak pekerja komuter ke Jakarta.</p></section>
<section><h2>Model Bisnis</h2><ul><li>Cuci kiloan Rp 8.000/kg</li><li>Layanan express &amp; satuan</li><li>Paket langganan bulanan (rencana)</li></ul></section>
<section><h2>Rencana Ekspansi</h2><p>3 outlet baru di Depok &amp; Bogor dalam 12 bulan → total 5 outlet, target omzet Rp 95 jt/bulan.</p></section>
<section><h2>Tim</h2><ul><li>Founder — 6 tahun supervisor laundry hotel</li><li>Co-founder — keuangan</li></ul></section>
<section><h2>Pendanaan</h2><div class="grid"><div class="card"><div class="big">Rp 450 jt</div>dana dicari</div><div class="card"><div class="big">15%</div>saham ditawarkan</div><div class="card"><div class="big">Rp 3 M</div>valuasi post-money</div></div><p>Penggunaan: mesin cuci &amp; pengering, sewa tempat, renovasi, marketing, modal kerja.</p></section>
<section><h1>Terima kasih</h1><p>Mari tumbuh bersama Bersih Kilat.</p></section>
</body>
</html>
```

Balasan agent tanpa skill (ringkas): "Sudah saya buatkan pitch deck 10 slide di `bersih-kilat-pitch.html`. Buka di browser lalu scroll ke bawah. Silakan sesuaikan angka proyeksinya."

## Output B — dengan skill
Lihat `01-pitch-investor-laundry.md` dan file `pitch-bersih-kilat.html` (13 slide).

## Perbandingan berdampingan

| Aspek | A — tanpa skill | B — dengan skill |
|---|---|---|
| Tanpa internet | ✗ memanggil `fonts.googleapis.com` (tercatat 1 request); offline font jatuh ke cadangan | ✔ 0 request jaringan |
| `validasi_html.py` | GAGAL (rujukan internet, 0 slide terdeteksi) | LULUS tanpa peringatan |
| Format Rupiah | ✗ "Rp 38 jt", "Rp 450 jt", "Rp 3 M" | ✔ Rp 38.000.000, Rp 450.000.000, Rp 3.000.000.000 |
| Angka dikarang | ✗ "target omzet Rp 95 jt/bulan", "pasar triliunan rupiah", "jutaan penduduk" tanpa dasar | ✔ angka yang tidak diberikan pengguna jadi placeholder kuning `[isi]` + daftar "perlu dilengkapi" |
| Struktur pitch | 10 slide, tanpa kompetitor & proyeksi berasumsi | 13 slide sesuai template (masalah → … → kebutuhan dana → proyeksi → penutup) |
| Angka turunan | valuasi Rp 3 M (benar, tapi disingkat) | valuasi, dana per outlet, kg/bulan dengan rumus tertulis |
| HP 390px tegak | teks besar & terbaca, tetapi slide 4 dan 9 **meluber ke samping** (scrollWidth 479 & 433 px > 390) | tidak meluber, tetapi teks isi hanya ±6,5px (harus putar HP ke lanskap → ±11,6px) |
| Cetak PDF (Chromium, kertas bawaan) | 10 halaman tegak, tanpa CSS cetak khusus | 13 halaman = 1 slide/halaman ✔, **tetapi sisi kanan terpotong** (kolom nominal hilang) |
| Navigasi presentasi | scroll | panah, spasi, geser jari, tombol ‹ › + nomor halaman |
| Petunjuk untuk awam | 1 kalimat | cara buka, navigasi, cetak PDF, asumsi, bagian yang perlu diisi, hasil cek otomatis |

## Penilaian
Dengan skill **jelas lebih baik** untuk pembeli awam Indonesia: benar-benar tanpa internet, disiplin tidak mengarang angka, format Rupiah benar, struktur pitch lebih lengkap, dan balasan memberi langkah pakai + daftar isian. Kelemahan versi skill yang harus diperbaiki (bukan alasan kalah A/B, tetapi cacat mandiri): PDF terpotong di sisi kanan dan teks sangat kecil di HP posisi tegak — sebaliknya, versi tanpa skill justru lebih terbaca di HP tegak.
