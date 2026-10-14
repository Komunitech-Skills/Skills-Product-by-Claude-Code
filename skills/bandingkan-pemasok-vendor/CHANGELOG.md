# Riwayat perubahan — bandingkan-pemasok-vendor

Catatan teknis per versi (dipisah dari README agar halaman pembeli ringkas).

## 1.0.1 (2026-10-14)
Revisi dari uji OpenClaw independen 1.0.0 (6,5 → 7,0, BELUM; angka script 100% cocok, cacat ada di kalimat kesimpulan agent).
- **Arah selisih eksplisit:** script mengeluarkan blok "RINGKASAN SIAP SALIN" berisi kalimat utuh bersubjek ("A lebih MURAH/MAHAL Rp… daripada B"), menggantikan kalimat menggantung "Hemat vs Y"; SKILL.md mewajibkan blok itu disalin apa adanya dan melarang agent menghitung ulang/menyimpulkan sendiri. Kolom tabel "selisih vs termurah" kini "lebih mahal Rp… (x%)".
- **Kamus kolom PPN seragam** (`termasuk`/`belum`/`non-pkp`/`bebas`/`?`) di script, template, references, dan SKILL.md. Perbaikan cacat: nilai `belum` sebelumnya terbaca "tidak diketahui". Cara pakai script ditulis ringkas di SKILL.md + opsi `--contoh` (agent tidak perlu membaca kode).
- **Ongkir yang belum diketahui** tidak lagi diam-diam Rp0: label "termurah sementara" + kalimat batas ongkir (ongkir impas, total dan per satuan, memperhitungkan PPN); sama untuk biaya ambil sendiri (loco). Skenario "bila status PKP ternyata belum termasuk PPN" kini dihitung script (total baru, pembanding, rekomendasi).
- **Rekomendasi = peringkat 1:** pemasok yang melewati tenggat diurutkan di bawah yang tepat waktu; opsi `--pilihan` membandingkan pemasok yang dicondongi pengguna secara terbuka (tanpa "sesuai pilihanmu"). Kalimat bagi pesanan memakai "lebih MURAH/MAHAL" (tanpa tanda "+-"). Subjek skenario telat = termurah yang tepat waktu.
- **Asumsi pajak terbuka di keluaran:** PPN atas ongkir pemasok PKP (dengan angkanya), syarat ringkas pengkreditan PPN untuk pembeli PKP, dan catatan bahan pokok bebas PPN (PP 49/2022) + opsi `--barang`/`--bebas-ppn`. Ditandai PERLU REVIEW konsultan pajak.
- Uji regresi bertambah menjadi 66 (arah selisih, kamus PPN + template CSV, ongkir impas brute force, rekomendasi/pilihan, tanda bagi pesanan).

## 1.0.0 (2026-10-14)
- Rilis awal: biaya sampai di tempat (harga grosir bertingkat, MOQ/kelipatan/isi dus, minimal belanja, diskon, ongkir franco/loco/ekspedisi, PPN PKP vs non-PKP dengan pembulatan standar library, pembeli PKP), skor tertimbang 5 kriteria dengan bobot yang bisa diubah, sensitivitas (jumlah 2x, termurah telat + hari impas, bagi pesanan 70/30), daftar `[isian]`, template pesan WA klarifikasi/negosiasi.
- Script `scripts/banding_pemasok.py` (Decimal, Python standar) + `tests/uji_regresi.py` (47 uji).
