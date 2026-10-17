# Program Beta Tester

Tujuan: menguji skill di tangan **pengguna sungguhan** (pengusaha & profesional awam) sebelum dijual.

## Alur
1. **Pilih skill**: status `beta` di `catalog.csv` (sudah lulus uji agent; uji platform asli dicatat di `platform_teruji` / `examples/UJI-PLATFORM.md`). **Batch VIP Oktober 2026:** fokus **10 skill** bernama di `docs/panduan-beta-tester.md` §5 (bukan seluruh baris `beta` di katalog).
2. **Rekrut 5–10 member VIP** yang cocok dengan target skill (mis. skill marketplace → pemilik toko online). Campur pengguna OpenClaw, Codex, Claude Code, Cursor, dan Windows/Mac.
3. **Kirim paket**: `python3 scripts/build.py --pembeli "Beta - <nama>" --vip --beta` (ZIP berisi seluruh library; opsi `--beta` juga menaruh `PANDUAN-BETA-TESTER.html` dan `.md` di akar ZIP, salinan dari `docs/panduan-beta-tester.*` saat build). Watermark tetap berlaku. Untuk uji satu skill saja: `--skill <nama> --beta`.
   - **Kirim panduan juga secara terpisah**, sebelum ZIP dibuka: berkas `panduan-beta-tester-komunitech.html` (salinan `docs/panduan-beta-tester.html`) + teks ringkas di jalur yang sama dengan ZIP. Tester perlu membacanya lebih dulu untuk tahu cara membuka dan memasang ZIP.
   - **Satu topik atau obrolan pribadi per tester** untuk pengiriman ZIP (tiap ZIP ber-watermark nama masing-masing; jangan ditaruh di topik yang dibaca tester lain).
   - **Jalur masukan per tester wajib jelas sebelum kirim:** default topik Telegram "Beta VIP — panduan tester" di grup uji. Untuk tester yang tidak memakai Telegram: "kirim lewat kontak admin Komunitech yang biasa". Tulis kontak itu di pesan pengantar (panduan memuat tanda `[KONTAK ADMIN]` dan menyuruh tester bertanya ke pengirim bila belum terisi). **Jangan menulis nomor telepon atau handle di repo.**
4. **Masa uji 7 hari sejak ZIP diterima** (tester 1: 13–19 Oktober 2026). Minta mereka memakai skill untuk pekerjaan nyata minimal 3 kali; masukan paling lambat 1 hari sesudah hari ke-7.
5. **Kumpulkan masukan** dengan formulir di `docs/panduan-beta-tester.md` bagian 7 (**satu-satunya sumber formulir**; jangan menyalinnya ke berkas lain agar tidak menyimpang).
6. **Rangkum** di `skills/<nama>/examples/MASUKAN-BETA.md` (tanpa data pribadi: pakai "Beta 1", "Beta 2", dst.). Catatan jujur ke tester: saat mengirim lewat Telegram, nama akun mereka terlihat oleh pemilik Komunitech (dan anggota grup bila dikirim di topik); hanya laporan kita yang tanpa nama.
7. **Revisi** → uji ulang singkat → status `rilis` → naikkan `versi`.
8. **Minta testimoni** (dengan izin tertulis) untuk halaman jualan.

**Imbalan** (member VIP sudah punya akses penuh ke library, jadi imbalan **bukan uang dan bukan akses skill**): (1) akses lebih awal ke skill-skill berikutnya, (2) prioritas untuk permintaan skill dari tester, (3) hanya bila tester setuju (butir 12 formulir), nama atau nama usaha dicantumkan di daftar terima kasih. Tanpa uang, tanpa diskon, tanpa janji hasil. Diberikan setelah formulir diterima.

## Perawatan panduan
- `docs/panduan-beta-tester.md` dan `docs/panduan-beta-tester.html` berisi teks yang sama; tidak ada skrip pembangkit, jadi **setiap perubahan di `.md` harus disalin ke `.html` dengan tangan** (dan sebaliknya).
- Salinan Artifact (tautan claude.ai) bersifat terpisah dan privat; terbitkan ulang dari `.html` bila isinya berubah.
- ZIP beta membawa salinan panduan saat build, jadi bangun ulang ZIP untuk tester baru setelah panduan diubah.

## Formulir masukan
Ada di `docs/panduan-beta-tester.md` bagian 7 (12 pertanyaan: platform, keberhasilan pasang, frekuensi pakai, kegunaan, hasil siap pakai, waktu hemat, hasil salah/aneh, yang disukai, yang diperbaiki, harga wajar, izin testimoni, izin daftar terima kasih). Satu formulir per skill yang dicoba; butir 12 cukup di formulir pertama.

## Kriteria naik ke `rilis`
- ≥ 80% beta tester berhasil instal tanpa bantuan.
- Rata-rata nilai kegunaan ≥ 4.
- Tidak ada laporan hasil salah yang belum diperbaiki.
