# Kerangka HTML dasar (wajib dipakai)

Setiap presentasi dihasilkan sebagai **satu file HTML mandiri**: semua CSS dan JavaScript
ditulis inline di dalam file itu sendiri. Tidak ada `<link>` atau `<script src>` yang
menunjuk ke internet (Google Fonts, CDN, dsb.) — presentasi harus tetap bisa dibuka
tanpa koneksi internet sama sekali, kapan pun, di laptop maupun HP.

Gunakan kerangka di bawah ini sebagai titik awal, lalu isi kontennya sesuai template
di folder `templates/` dan aturan desain di `references/aturan-desain.md`.

## Struktur panggung tetap 16:9

Setiap slide "ditulis" di kanvas tetap berukuran 1920×1080, lalu seluruh panggung
diskalakan (bukan disusun ulang / reflow) agar pas di layar apa pun — laptop, tablet,
atau HP. Ini membuat tata letak selalu konsisten dan tidak pernah berantakan di HP.

```html
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Judul Presentasi</title>
<style>
  /* ====== VARIABEL TEMA — ganti di sini untuk ubah seluruh tampilan ====== */
  :root {
    --warna-latar: #0f172a;        /* latar panggung di luar slide (saat letterbox) */
    --warna-latar-slide: #ffffff;  /* latar tiap slide */
    --warna-teks: #0f172a;
    --warna-teks-lembut: #475569;
    --warna-aksen: #2563eb;        /* warna brand / merek pengguna */
    --font-judul: Georgia, 'Times New Roman', serif;   /* pilih sesuai gaya di aturan-desain.md */
    --font-isi: 'Segoe UI', Arial, Helvetica, sans-serif;
    --ukuran-judul: 96px;   /* diukur pada kanvas 1920x1080 */
    --ukuran-subjudul: 36px;
    --ukuran-isi: 32px;
    --padding-slide: 96px;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  html, body {
    width: 100%; height: 100%; margin: 0; overflow: hidden;
    background: var(--warna-latar);
    font-family: var(--font-isi);
  }

  /* --- Panggung 16:9 tetap --- */
  .panggung-luar { position: fixed; inset: 0; overflow: hidden; background: var(--warna-latar); }
  .panggung {
    position: absolute; left: 0; top: 0;
    width: 1920px; height: 1080px;
    transform-origin: 0 0;
    overflow: hidden;
  }

  .slide {
    position: absolute; inset: 0;
    width: 1920px; height: 1080px;
    padding: var(--padding-slide);
    background: var(--warna-latar-slide);
    color: var(--warna-teks);
    visibility: hidden; opacity: 0; pointer-events: none;
    display: flex; flex-direction: column; justify-content: center;
  }
  .slide.aktif { visibility: visible; opacity: 1; pointer-events: auto; z-index: 1; }

  .slide h1 { font-family: var(--font-judul); font-size: var(--ukuran-judul); line-height: 1.1; color: var(--warna-teks); }
  .slide h2 { font-family: var(--font-judul); font-size: 56px; margin-bottom: 32px; color: var(--warna-aksen); }
  .slide p, .slide li { font-size: var(--ukuran-isi); line-height: 1.5; color: var(--warna-teks-lembut); }

  img { max-width: 100%; max-height: 100%; }

  /* --- Navigasi (disembunyikan saat cetak) --- */
  .kontrol {
    position: fixed; left: 50%; bottom: 24px; transform: translateX(-50%);
    z-index: 1000; display: flex; gap: 12px; align-items: center;
    font-family: var(--font-isi); font-size: 14px; color: #fff;
    background: rgba(0,0,0,.5); padding: 8px 16px; border-radius: 999px;
  }
  .kontrol button { border: none; background: transparent; color: #fff; font-size: 16px; cursor: pointer; }

  @media (prefers-reduced-motion: reduce) {
    * { transition: none !important; animation: none !important; }
  }

  /* ====== MODE CETAK: WAJIB — supaya "Print > Save as PDF" rapi 1 slide/halaman ====== */
  @media print {
    html, body { width: 1920px; height: auto; overflow: visible; background: #fff; }
    .panggung-luar { position: static; overflow: visible; background: #fff; }
    .panggung { position: static; width: auto; height: auto; transform: none !important; }
    .slide {
      position: relative; display: flex !important;
      visibility: visible !important; opacity: 1 !important;
      width: 1920px; height: 1080px;
      break-after: page; page-break-after: always;
    }
    .slide:last-child { break-after: auto; page-break-after: auto; }
    .kontrol { display: none !important; }
  }
</style>
</head>
<body>
<div class="panggung-luar">
  <main class="panggung" id="panggung">
    <section class="slide aktif">
      <h1>Judul Presentasi</h1>
      <p>Anak judul / nama perusahaan / tanggal</p>
    </section>

    <section class="slide">
      <h2>Judul Slide</h2>
      <p>Isi slide...</p>
    </section>

    <!-- slide berikutnya... -->
  </main>
</div>

<div class="kontrol">
  <button id="btnMundur" title="Sebelumnya (←)">‹</button>
  <span id="halaman">1 / 1</span>
  <button id="btnMaju" title="Berikutnya (→ / Spasi)">›</button>
</div>

<script>
(function () {
  var slide = document.querySelectorAll('.slide');
  var indeks = 0;
  var panggung = document.getElementById('panggung');
  var labelHalaman = document.getElementById('halaman');

  function skalakan() {
    var faktor = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
    var x = (window.innerWidth - 1920 * faktor) / 2;
    var y = (window.innerHeight - 1080 * faktor) / 2;
    panggung.style.transform = 'translate(' + x + 'px,' + y + 'px) scale(' + faktor + ')';
  }
  window.addEventListener('resize', skalakan);
  skalakan();

  function tampilkan(i) {
    indeks = Math.max(0, Math.min(i, slide.length - 1));
    slide.forEach(function (s, n) { s.classList.toggle('aktif', n === indeks); });
    labelHalaman.textContent = (indeks + 1) + ' / ' + slide.length;
  }
  tampilkan(0);

  document.getElementById('btnMaju').addEventListener('click', function () { tampilkan(indeks + 1); });
  document.getElementById('btnMundur').addEventListener('click', function () { tampilkan(indeks - 1); });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') { tampilkan(indeks + 1); e.preventDefault(); }
    if (e.key === 'ArrowLeft' || e.key === 'PageUp') { tampilkan(indeks - 1); e.preventDefault(); }
  });

  // Geser jari di HP/tablet
  var xAwal = null;
  document.addEventListener('touchstart', function (e) { xAwal = e.touches[0].clientX; });
  document.addEventListener('touchend', function (e) {
    if (xAwal === null) return;
    var beda = e.changedTouches[0].clientX - xAwal;
    if (beda > 50) tampilkan(indeks - 1);
    if (beda < -50) tampilkan(indeks + 1);
    xAwal = null;
  });
})();
</script>
</body>
</html>
```

## Aturan wajib saat mengisi kerangka ini

1. **Jangan tambahkan `<link>` atau `<script src>` eksternal apa pun** (font Google, CDN
   ikon, library JS). Semua styling & interaksi cukup CSS + JavaScript polos di atas.
2. **Font:** pakai kombinasi font sistem yang tersedia di semua OS tanpa perlu koneksi
   internet. Lihat pilihan tumpukan font di `references/aturan-desain.md`. Jangan
   memakai satu nama font tunggal (mis. `font-family: 'Poppins'`) karena kalau font itu
   tidak terpasang di komputer pengguna, browser diam-diam mengganti ke font lain yang
   tampilannya bisa berbeda jauh — selalu tulis daftar cadangan seperti contoh di atas.
3. **Gambar/logo:** jika pengguna memberi file logo/gambar, ubah ke `base64` dan tempel
   langsung di `src="data:image/png;base64,...."` supaya file tetap satu berkas mandiri
   dan tidak bergantung pada folder gambar terpisah yang bisa hilang saat dikirim.
4. **Rupiah:** setiap angka uang wajib format `Rp 1.250.000` (titik pemisah ribuan, tanpa
   desimal kecuali memang perlu, tanpa disingkat "1,2jt" kecuali pengguna secara eksplisit minta ringkas).
5. Setelah HTML jadi, jalankan `python3 <folder-skill-ini>/scripts/validasi_html.py <file.html>` untuk memastikan
   tidak ada rujukan internet, ada CSS cetak, dan tidak ada slide yang terlalu padat teks.
