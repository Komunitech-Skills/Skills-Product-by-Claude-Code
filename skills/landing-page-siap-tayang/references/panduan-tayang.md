# Panduan Tayang Gratis (untuk orang awam)

Diperiksa terhadap dokumentasi resmi pada 2026-10-06. Tampilan menu situs-situs ini sering berubah: **PERLU REVIEW** bila nama tombol di layar berbeda; ikuti istilah yang paling mirip. Semua pilihan di bawah memakai file `index.html` yang sama.

## Persiapan (semua pilihan)
1. Buat folder baru, mis. `landing-saya`. Taruh `index.html` di dalamnya (nama WAJIB `index.html`, huruf kecil). Foto (bila ada) ditaruh di folder yang sama dan ditulis di HTML dengan nama file, mis. `foto1.jpg`.
2. Buka `index.html` dengan klik dua kali: harus tampil di browser. Lanjut ke checklist di bawah dulu, baru unggah.

## Pilihan 1 - Netlify Drop (paling mudah, tanpa akun untuk mencoba)
1. Buka `https://app.netlify.com/drop`.
2. Seret **folder** `landing-saya` ke kotak yang tersedia.
3. Tunggu beberapa detik; alamat sementara muncul (berakhiran `.netlify.app`).
4. Tanpa akun, situs bersifat sementara dan harus "diklaim": masuk/daftar (gratis) dalam batas waktu yang tertera (dokumentasi menyebut sekitar satu jam) agar tidak hilang.
5. Ubah isi: buat akun, buka situsnya, menu **Deploys**, seret folder terbaru ke kotak unggah.
6. Ganti nama alamat: di pengaturan situs cari **Project/Site configuration** lalu ganti nama (mis. `keripik-bu-dewi.netlify.app`).

## Pilihan 2 - GitHub Pages (gratis, agak teknis)
1. Daftar di github.com, klik **New repository**, beri nama (mis. `landing-saya`), pilih **Public**, buat.
2. Klik **uploading an existing file**, seret `index.html` dan foto, lalu **Commit changes**.
3. Buka tab **Settings** > **Pages**. Pada "Build and deployment" pilih **Deploy from a branch**, branch `main`, folder `/ (root)`, klik **Save**.
4. Tunggu beberapa menit (bisa sampai sekitar 10 menit). Alamat: `https://<nama-akun>.github.io/<nama-repo>/`.
5. Perhatian: repositori Public berarti siapa pun bisa melihat isi file. Jangan taruh data rahasia.

## Pilihan 3 - Cloudflare Pages (gratis, stabil)
1. Daftar/masuk di dash.cloudflare.com.
2. Menu **Workers & Pages** > **Create application** > cari opsi unggah langsung (**Get started** > **Drag and drop your files**; nama menu bisa berubah, PERLU REVIEW).
3. Isi nama proyek, seret folder `landing-saya`, klik **Deploy site**.
4. Alamat: `<nama-proyek>.pages.dev`.
5. Catatan resmi: proyek yang dibuat lewat unggah langsung tidak bisa dialihkan ke sambungan Git nanti (harus buat proyek baru).

## Pilihan 4 - Hosting/cPanel yang sudah dimiliki
1. Masuk cPanel dari penyedia hosting Anda > **File Manager**.
2. Buka folder `public_html` (atau folder domain Anda). Bila di sana sudah ada situs lain, jangan timpa `index.html` yang lama: buat subfolder (mis. `promo`) agar alamatnya `domain-anda.com/promo/`.
3. Klik **Upload**, pilih `index.html` dan foto.
4. Buka `https://domain-anda.com/` di browser (tekan Ctrl+F5 bila masih tampil versi lama).
5. Tidak perlu CNAME: domain sudah mengarah ke hosting.

## Memasang domain sendiri (umum)
Domain dibeli di pendaftar domain (mis. .com, .id, .co.id). Prinsipnya sama di semua layanan:
1. Di layanan tayang (Netlify/GitHub/Cloudflare), buka pengaturan **Custom domain / Domain management**, tambahkan domain Anda; layanan menampilkan nilai yang harus dipasang.
2. Di panel DNS pendaftar domain, tambah catatan **CNAME**: Nama/Host `www`, Tujuan/Value alamat dari layanan (mis. `situs-anda.netlify.app`, `akun.github.io`, atau `proyek.pages.dev`).
3. Domain "telanjang" (tanpa www, mis. `tokoanda.com`) umumnya tidak bisa CNAME biasa; layanan akan menunjukkan catatan A/ALIAS/ANAME khusus. Ikuti angka yang ditampilkan layanan, jangan menebak. Alternatif mudah: pakai `www` dan alihkan domain telanjang ke www lewat pengaturan layanan.
4. Tunggu penyebaran DNS (beberapa menit sampai 24-48 jam). HTTPS (gembok) biasanya diaktifkan otomatis oleh layanan; di GitHub Pages ada kotak **Enforce HTTPS** yang perlu dicentang.
5. Hapus catatan DNS lama yang bentrok (mis. catatan `www` yang sudah ada).

## Checklist sebelum tayang
- [ ] Buka di HP asli (bukan hanya komputer): teks terbaca, tidak perlu geser ke samping.
- [ ] Ketuk semua tombol WhatsApp: terbuka ke nomor yang benar dengan pesan terisi.
- [ ] Tidak ada tulisan `[isian...]` tersisa (testimoni, harga, nama, tahun).
- [ ] Setiap foto <= 300 KB (kecilkan lewat aplikasi galeri/compress online; format JPG/WebP).
- [ ] Harga, jam layanan, garansi, area kirim sesuai kenyataan.
- [ ] Testimoni hanya yang asli dan sudah diizinkan pemiliknya.
- [ ] Izin edar/sertifikat yang disebut benar-benar ada (BPOM, halal, dll.).
- [ ] Judul tab dan deskripsi (yang tampil di Google/WA) sudah sesuai.
- [ ] Sudah dikirim ke 2-3 teman untuk dicoba.
