# Riwayat perubahan — bandingkan-pemasok-vendor

Catatan teknis per versi (dipisah dari README agar halaman pembeli ringkas).

## 1.0.3 (2026-10-14)
Rujukan aturan dicocokkan ke sumber resmi 14 Okt 2026; tanpa perubahan hitungan (rumus, script, dan tes sama dengan 1.0.2; hanya konstanta versi).
- `references/membaca-penawaran.md`: ongkir di faktur pemasok PKP = Harga Jual/DPP (UU PPN Pasal 1 angka 18); titipan murni ke ekspedisi tanpa mark-up tetap PERLU REVIEW konsultan pajak. Pengkreditan Pajak Masukan merujuk UU PPN Pasal 9 ayat (2), (2b), (8) huruf b, faktur sah Pasal 13. Pembebasan gula PP 49/2022 Pasal 6 hanya gula kristal putih tebu tanpa perasa/pewarna. Bagian sumber + tanggal akses ditambahkan.
- SKILL.md (Batasan) dan README (catatan kaki di FAQ PPN, status uji) diselaraskan.

## 1.0.2 (2026-10-14)
Patch dari uji ulang 1.0.1 (LULUS, 6,5 → 8,2; dua slip kecil di skenario tambahan tanpa dampak rupiah/peringkat).
- **Termin DP + sisa ditempokan dikenali:** "DP 30% sisa 30 hari", "30% di muka, sisa 2 minggu", "DP 40% lunas dalam 14 hari", "sisa/pelunasan saat kirim/terima". DP tanpa keterangan sisa ditulis terbuka "(diasumsikan)". Termin tak terbaca (mis. konsinyasi) → `[isian]`, skor netral, tidak lagi disebut "tunai". Cara pembacaan termin/hari kerja ditulis di ringkasan ("Dibaca dari penawaran").
- **Contoh ringkas SKILL.md diganti** (plastik klip, 2 pemasok) agar tidak memakai data uji; agent dilarang membuka `examples/`.
- **Keluaran lebih pendek (target ≤ 3.500 karakter):** tabel 6 kolom (termasuk kirim & bayar dari hitungan), ringkasan inti dengan maks. 2 kalimat data kosong + maks. 2 kalimat sensitivitas; kalimat lain ke blok TAMBAHAN dan rincian per pemasok hanya bila pengguna membalas "rincian". Panjang inti ditampilkan. Rincian harga per kemasan ditulis utuh (12 karton x Rp380.000, bukan harga per kg yang dibulatkan).
- **Kutipan angka:** agent wajib menyalin INTI utuh dan tidak menulis ulang skor/lama kirim/termin di luar blok.
- **PP 49/2022 dipersempit:** hanya frasa seperti gula pasir/gula konsumsi/gula kristal putih, beras, telur, daging/sayur/buah segar; gula aren/cair/industri/rafinasi, olahan, premium tidak dianggap bebas PPN dan diberi catatan "belum tentu termasuk; cek status barang Anda".
- README: hasil uji nyata 1.0.1 dan status uji jujur. Uji regresi menjadi 75.

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
