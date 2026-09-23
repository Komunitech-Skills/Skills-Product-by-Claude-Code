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
    --warna-kartu: rgba(37, 99, 235, .07);   /* latar kartu KPI/kotak — turunan lembut dari aksen */
    --warna-garis: rgba(15, 23, 42, .12);    /* garis pembatas tabel/kartu/timeline */
    --font-judul: Georgia, 'Times New Roman', serif;   /* pilih sesuai gaya di aturan-desain.md */
    --font-isi: system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
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
    overflow: hidden;
    visibility: hidden; opacity: 0; pointer-events: none;
    display: flex; flex-direction: column; justify-content: center;
  }
  .slide.aktif { visibility: visible; opacity: 1; pointer-events: auto; z-index: 1; }

  .slide h1 { font-family: var(--font-judul); font-size: var(--ukuran-judul); line-height: 1.1; color: var(--warna-teks); }
  .slide h2 { font-family: var(--font-judul); font-size: 56px; margin-bottom: 32px; color: var(--warna-aksen); }
  .slide p, .slide li { font-size: var(--ukuran-isi); line-height: 1.5; color: var(--warna-teks-lembut); }

  img { max-width: 100%; max-height: 100%; }

  /* ====== KOMPONEN SIAP PAKAI (lihat contoh pemakaian di bawah kode) ====== */

  /* Kartu angka / KPI */
  .kartu-kpi { display: flex; gap: 32px; margin-top: 24px; flex-wrap: wrap; }
  .kpi { flex: 1; min-width: 280px; background: var(--warna-kartu); border: 1px solid var(--warna-garis); border-radius: 16px; padding: 32px; }
  .kpi .angka { font-family: var(--font-judul); font-size: 72px; font-weight: bold; color: var(--warna-aksen); line-height: 1; }
  .kpi .label { font-size: 24px; color: var(--warna-teks-lembut); margin-top: 12px; }

  /* Dua kolom */
  .dua-kolom { display: flex; gap: 64px; align-items: flex-start; }
  .dua-kolom > div { flex: 1; }

  /* Tabel data — angka uang rata kanan & sejajar (tabular-nums) */
  table.tabel-data { width: 100%; border-collapse: collapse; font-size: 28px; }
  table.tabel-data th, table.tabel-data td { padding: 16px 20px; border-bottom: 1px solid var(--warna-garis); text-align: left; }
  table.tabel-data th { color: var(--warna-teks-lembut); font-weight: 600; font-size: 24px; }
  table.tabel-data td.uang, table.tabel-data th.uang {
    text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap;
  }

  /* Penanda bagian yang belum diisi pengguna — dibuat mencolok, TIDAK ikut tercetak sebagai warna aneh */
  .isi { background: #fef08a; color: #713f12; padding: 2px 10px; border-radius: 4px; font-weight: 600; }

  /* Timeline / langkah-langkah */
  .timeline { display: flex; gap: 0; margin-top: 40px; }
  .timeline .langkah { flex: 1; position: relative; padding-top: 44px; padding-right: 32px; }
  .timeline .langkah::before {
    content: attr(data-nomor); position: absolute; top: 0; left: 0;
    width: 32px; height: 32px; border-radius: 50%;
    background: var(--warna-aksen); color: #fff;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; font-weight: bold;
  }
  .timeline .langkah::after {
    content: ""; position: absolute; top: 16px; left: 32px; right: 0; height: 2px;
    background: var(--warna-garis);
  }
  .timeline .langkah:last-child::after { display: none; }
  .timeline .langkah h3 { font-family: var(--font-judul); font-size: 26px; margin-bottom: 8px; color: var(--warna-teks); }
  .timeline .langkah p { font-size: 22px; }

  /* Kutipan / testimoni */
  .kutipan { border-left: 6px solid var(--warna-aksen); padding: 8px 32px; font-style: italic; font-size: 34px; color: var(--warna-teks); }
  .kutipan .sumber { display: block; margin-top: 16px; font-style: normal; font-size: 22px; color: var(--warna-teks-lembut); }

  /* --- Navigasi (disembunyikan saat cetak) --- */
  .kontrol {
    position: fixed; left: 50%; bottom: 24px; transform: translateX(-50%);
    z-index: 1000; display: flex; gap: 12px; align-items: center;
    font-family: var(--font-isi); font-size: 14px; color: #fff;
    background: rgba(0,0,0,.5); padding: 8px 16px; border-radius: 999px;
  }
  .kontrol button { border: none; background: transparent; color: #fff; font-size: 16px; cursor: pointer; }

  /* Di HP posisi mendatar, layar pendek — kecilkan & pudarkan kontrol supaya tidak menutupi isi slide */
  @media (orientation: landscape) and (max-height: 500px) {
    .kontrol { transform: translateX(-50%) scale(.75); opacity: .45; bottom: 4px; }
    .kontrol:hover, .kontrol:active, .kontrol:focus-within { opacity: .95; }
  }

  /* --- Tombol mode edit teks (opsional, offline, tanpa library) --- */
  .btn-edit {
    position: fixed; right: 20px; bottom: 20px; z-index: 1000;
    border: none; border-radius: 999px; padding: 10px 18px;
    background: rgba(0,0,0,.5); color: #fff; font-family: var(--font-isi);
    font-size: 14px; cursor: pointer;
  }
  .btn-edit.aktif { background: #16a34a; }
  [contenteditable] { outline: 2px dashed var(--warna-aksen); outline-offset: 4px; cursor: text; }

  /* --- Overlay "putar HP" saat layar lebih tinggi dari lebar (potret) --- */
  .putar-hp {
    display: none;
    position: fixed; inset: 0; z-index: 2000;
    background: rgba(15, 23, 42, .96); color: #fff;
    align-items: center; justify-content: center; text-align: center;
    font-family: var(--font-isi); font-size: 22px; line-height: 1.5; padding: 40px;
  }
  @media (orientation: portrait) and (max-width: 600px) {
    .putar-hp { display: flex; }
  }
  .putar-hp.tutup { display: none !important; }

  @media (prefers-reduced-motion: reduce) {
    * { transition: none !important; animation: none !important; }
  }

  /* ====== UKURAN HALAMAN CETAK — WAJIB, mencegah sisi kanan slide terpotong ====== */
  @page {
    size: 1920px 1080px;
    margin: 0;
  }

  /* ====== MODE CETAK: WAJIB — supaya "Print > Save as PDF" rapi 1 slide/halaman, utuh, warna ikut tercetak ====== */
  @media print {
    * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
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
    .kontrol, .btn-edit, .putar-hp { display: none !important; }
    [contenteditable] { outline: none !important; }
  }
</style>
</head>
<body>
<div class="putar-hp" id="putarHp">
  <div>
    🔄 Putar HP ke posisi mendatar (landscape) agar teks presentasi ini terbaca dengan baik.
    <div style="margin-top:20px;"><button id="btnTetapLihat" style="font:inherit;padding:8px 20px;border-radius:999px;border:1px solid #fff;background:transparent;color:#fff;cursor:pointer;">Tetap lihat</button></div>
  </div>
</div>

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

<button id="btnEdit" class="btn-edit" title="Ubah teks langsung di slide">✏️ Edit</button>

<script>
(function () {
  var slide = document.querySelectorAll('.slide');
  var indeks = 0;
  var panggung = document.getElementById('panggung');
  var labelHalaman = document.getElementById('halaman');
  var btnEdit = document.getElementById('btnEdit');

  // Bersihkan sisa mode edit: kalau file ini disimpan (Ctrl+S) SAAT mode edit masih
  // aktif, atribut contenteditable ikut tersimpan di file. Lepas semuanya saat dibuka
  // ulang supaya presentasi selalu terbuka dalam mode lihat (bukan mode edit).
  document.querySelectorAll('[contenteditable]').forEach(function (el) {
    el.removeAttribute('contenteditable');
  });
  document.body.classList.remove('mode-edit');

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

  // Sedang mengetik di teks yang bisa diedit? Jangan pindah slide (spasi/panah harus
  // masuk ke teks, bukan menggerakkan presentasi).
  function sedangMengedit(e) {
    return e.target.isContentEditable || document.body.classList.contains('mode-edit');
  }

  document.addEventListener('keydown', function (e) {
    if (sedangMengedit(e)) return;
    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') { tampilkan(indeks + 1); e.preventDefault(); }
    if (e.key === 'ArrowLeft' || e.key === 'PageUp') { tampilkan(indeks - 1); e.preventDefault(); }
  });

  // Geser jari di HP/tablet
  var xAwal = null;
  document.addEventListener('touchstart', function (e) {
    if (sedangMengedit(e)) return;
    xAwal = e.touches[0].clientX;
  });
  document.addEventListener('touchend', function (e) {
    if (sedangMengedit(e)) return;
    if (xAwal === null) return;
    var beda = e.changedTouches[0].clientX - xAwal;
    if (beda > 50) tampilkan(indeks - 1);
    if (beda < -50) tampilkan(indeks + 1);
    xAwal = null;
  });

  // Mode edit teks langsung di browser (offline, tanpa library)
  var editAktif = false;
  if (btnEdit) {
    btnEdit.addEventListener('click', function () {
      editAktif = !editAktif;
      document.body.classList.toggle('mode-edit', editAktif);
      document.querySelectorAll('.slide h1, .slide h2, .slide p, .slide li, .slide .angka, .slide .label, .slide td, .slide th')
        .forEach(function (el) {
          if (editAktif) { el.setAttribute('contenteditable', 'true'); }
          else { el.removeAttribute('contenteditable'); }
        });
      btnEdit.textContent = editAktif ? '✔ Selesai edit' : '✏️ Edit';
      btnEdit.classList.toggle('aktif', editAktif);
      if (editAktif) {
        alert('Mode edit aktif. Klik teks lalu ketik langsung — Spasi dan tombol panah tidak akan memindah slide selama Anda mengetik. Setelah selesai, klik "✔ Selesai edit" dulu, baru tekan Ctrl+S (Windows/Linux) atau Cmd+S (Mac) dan pilih "Webpage, HTML only" / "Laman Web, HTML saja" untuk menyimpan. Catatan: menyimpan file (Ctrl+S/Cmd+S) hanya bisa dilakukan di laptop/komputer — di HP, browser tidak punya cara menyimpan ulang file lokal seperti ini, jadi minta AI agent yang mengubah teksnya lalu kirim ulang filenya.');
      }
    });
  }

  // Tombol "Tetap lihat" pada overlay putar HP (mis. untuk HP yang kunci rotasinya aktif)
  var btnTetapLihat = document.getElementById('btnTetapLihat');
  var putarHp = document.getElementById('putarHp');
  if (btnTetapLihat && putarHp) {
    btnTetapLihat.addEventListener('click', function () { putarHp.classList.add('tutup'); });
  }
})();
</script>
</body>
</html>
```

## Contoh pemakaian komponen siap pakai

Sisipkan potongan ini di dalam `<section class="slide">...</section>` sesuai kebutuhan
konten — kelasnya sudah didefinisikan di kerangka di atas, tinggal pakai.

**Kartu angka (KPI)** — untuk highlight 2–4 angka penting (omzet, cicilan, rasio, dsb.):
```html
<div class="kartu-kpi">
  <div class="kpi"><div class="angka">Rp 35.000.000</div><div class="label">Omzet rata-rata/bulan</div></div>
  <div class="kpi"><div class="angka">4 tahun</div><div class="label">Lama usaha berjalan</div></div>
  <div class="kpi"><div class="angka">46,6%</div><div class="label">Rasio cicilan terhadap laba</div></div>
</div>
```

**Tabel data dengan kolom uang rata kanan:**
```html
<table class="tabel-data">
  <tr><th>Aset</th><th class="uang">Perkiraan Nilai</th></tr>
  <tr><td>Etalase & rak</td><td class="uang">Rp 8.000.000</td></tr>
  <tr><td>Sepeda motor operasional</td><td class="uang">Rp 15.000.000</td></tr>
</table>
```

**Dua kolom** (mis. teks + daftar, atau sebelum/sesudah):
```html
<div class="dua-kolom">
  <div><h3>Sebelum</h3><p>...</p></div>
  <div><h3>Sesudah</h3><p>...</p></div>
</div>
```

**Penanda `[isi]` mencolok** — untuk bagian yang belum dilengkapi pengguna:
```html
<p>Alamat usaha: <span class="isi">[isi alamat usaha Anda]</span></p>
```

**Timeline / langkah kerja:**
```html
<div class="timeline">
  <div class="langkah" data-nomor="1"><h3>Survei lokasi</h3><p>Analis KUR datang ke tempat usaha.</p></div>
  <div class="langkah" data-nomor="2"><h3>Verifikasi berkas</h3><p>KTP, NPWP, dan legalitas dicek.</p></div>
  <div class="langkah" data-nomor="3"><h3>Pencairan</h3><p>Dana masuk ke rekening usaha.</p></div>
</div>
```

**Kutipan / testimoni:**
```html
<blockquote class="kutipan">
  "Sejak pakai layanan ini, antrian laundry jadi lebih rapi."
  <span class="sumber">— Ibu Sari, pelanggan tetap</span>
</blockquote>
```

## Tema warna siap pakai

Pakai salah satu dari 4 palet di `references/aturan-desain.md` #5 (Biru Korporat, Hijau
Amanah, Hitam Emas Premium, Putih Minimalis) untuk `--warna-latar-slide`, `--warna-teks`,
**`--warna-teks-lembut`** (WAJIB diganti sesuai tabel di `aturan-desain.md` #5 — jangan
biarkan nilai bawaan `#475569` pada tema berlatar gelap, kontrasnya jatuh jauh di bawah
4,5:1), dan `--warna-aksen`. Untuk `--warna-kartu` dan `--warna-garis`, turunkan dari
warna aksen dengan opacity rendah (`.06`–`.12`) agar kartu/tabel tetap kontras dengan
latar — untuk tema gelap (Hitam Emas Premium), pakai warna terang dengan opacity rendah,
misalnya `--warna-kartu: rgba(245, 241, 230, .08); --warna-garis: rgba(245, 241, 230, .18);`.

Contoh lengkap variabel tema **Hitam Emas Premium** (latar gelap):
```css
--warna-latar-slide: #111111;
--warna-teks: #f5f1e6;
--warna-teks-lembut: #cfc8b8;  /* BUKAN #475569 — itu hanya aman di latar terang */
--warna-aksen: #c9a227;
--warna-kartu: rgba(245, 241, 230, .08);
--warna-garis: rgba(245, 241, 230, .18);
```

## Aturan wajib saat mengisi kerangka ini

1. **Jangan tambahkan `<link>` atau `<script src>` eksternal apa pun** (font Google, CDN
   ikon, library JS). Semua styling & interaksi cukup CSS + JavaScript polos di atas.
2. **Font:** pakai kombinasi font sistem yang tersedia lintas OS (Windows, macOS, Linux,
   Android) tanpa perlu koneksi internet. Lihat pilihan tumpukan font di
   `references/aturan-desain.md`. Jangan memakai satu nama font tunggal (mis.
   `font-family: 'Poppins'`) karena kalau font itu tidak terpasang di komputer pengguna,
   browser diam-diam mengganti ke font lain yang tampilannya bisa berbeda jauh — selalu
   tulis daftar cadangan seperti contoh di atas. Tampilan tidak akan identik 100% di
   setiap OS (mis. `Segoe UI` hanya ada di Windows, `Roboto` umum di Android/Chrome OS),
   tapi tetap rapi dan terbaca karena ada cadangan `system-ui`/`sans-serif`.
3. **Gambar/logo:** jika pengguna memberi file logo/gambar, ubah ke `base64` dan tempel
   langsung di `src="data:image/png;base64,...."` supaya file tetap satu berkas mandiri
   dan tidak bergantung pada folder gambar terpisah yang bisa hilang saat dikirim.
   **Jangan pernah** memakai path lokal (mis. `src="C:\Users\...\logo.png"` atau
   `src="logo.png"`) — path seperti itu hanya berfungsi di komputer pembuatnya dan akan
   rusak (gambar hilang) begitu file HTML dikirim ke orang lain lewat WA/email.
4. **Rupiah:** setiap angka uang wajib format `Rp 1.250.000` (titik pemisah ribuan, tanpa
   desimal kecuali memang perlu, tanpa disingkat "1,2jt" kecuali pengguna secara eksplisit minta ringkas).
5. **Cetak ke PDF:** blok `@page { size: 1920px 1080px; margin: 0; }` dan `@media print`
   di atas **wajib** ada persis seperti contoh — ini yang membuat setiap slide jadi satu
   halaman PDF penuh tanpa terpotong di sisi kanan, dan warna latar/aksen ikut tercetak.
   **Jangan** menyarankan pengguna memilih kertas A4/Letter atau orientasi
   Lanskap/Landscape di dialog cetak — ukuran halaman sudah diatur otomatis oleh
   `@page` di atas; menu orientasi/ukuran kertas di dialog cetak cukup dibiarkan default
   (browser akan mengikuti `@page`). Yang perlu dipastikan pengguna hanya: tujuan cetak
   = "Simpan sebagai PDF"/"Save as PDF", margin = "Tidak ada"/"None", dan centang
   "Grafis latar"/"Background graphics" bila tersedia supaya warna ikut tercetak.
6. **Kontras warna teks:** jika mengganti tema/warna (terutama latar gelap),
   `--warna-teks` dan `--warna-teks-lembut` wajib punya kontras minimal **4,5:1**
   terhadap `--warna-latar-slide` (lihat tabel di `aturan-desain.md` #5). Jangan biarkan
   `--warna-teks-lembut` bawaan `#475569` terpakai di latar gelap.
7. Setelah HTML jadi, jalankan `python3 <folder-skill-ini>/scripts/validasi_html.py <file.html>` untuk memastikan
   tidak ada rujukan internet, ada `@page` dengan ukuran serta CSS cetak, tidak ada gambar
   dengan path lokal, tidak ada slide yang terlalu padat teks, dan kontras warna teks
   cukup.
