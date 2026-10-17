# Riwayat perubahan — spesifikasi-produk-usaha

Catatan teknis per versi.

## Catatan revisi 1.0.5 (2026-10-17)
- Bagian Contoh di `SKILL.md` disamakan dengan `examples/01-minuman-teh-serai-spesifikasi.md` dan `examples/02-prioritas-rice.md`: ada 4 ide yang diurutkan (termasuk botol mini 100 ml), bukan 3. Tidak ada perubahan perilaku atau skrip.

## Catatan revisi 1.0.4 (2026-10-02)
- Revisi dari temuan uji OpenClaw: skill tidak lagi menulis anjuran takaran konsumsi/dosis (mis. "diminum 2x sehari") untuk minuman atau pangan fungsional kecuali disebut pengguna sendiri, dan itu pun ditandai sebagai kutipan serta diarahkan cek ke BPOM/ahli gizi.
- Daya simpan tidak boleh diusulkan tanpa dasar; ditulis "[perlu uji umur simpan]" sampai ada hasil uji.
- Ringkasan di chat untuk orang awam wajib menjelaskan istilah teknis (RICE, ICE, PIRT, BPOM MD, MOQ) dengan bahasa sehari-hari saat pertama muncul.

## Catatan revisi 1.0.3 (2026-10-01)
- SKILL.md kini menyebut bahwa script ada di subfolder `scripts/` di folder skill, dan agent tidak boleh mencari file ke seluruh disk (mis. `find /`). Logika tidak berubah.

## Catatan revisi 1.0.2 (2026-09-29)
- Script `prioritas.py`: baris yang jumlah nilainya lebih banyak daripada judul kolom (biasanya karena koma di nama atau angka desimal seperti 0,9) kini ditolak dengan pesan yang menyarankan tanda kutip atau titik/titik koma, bukan salah baca diam-diam. Uji regresi ditambah.

## Catatan revisi 1.0.1 (2026-09-29)
- Revisi setelah uji pertama: spesifikasi kini memuat "Ukuran keberhasilan" (1-3 target terukur dengan batas waktu; bila pengguna belum punya angka, diusulkan dan ditandai [ASUMSI]).
- `references/perizinan-produk.md` ditulis ulang: jalur izin ditentukan dulu menurut jenis produk (PIRT hanya untuk pangan suhu ruang berisiko rendah; produk dingin/beku, kemasan kedap, SNI wajib, klaim kesehatan, pangan bayi mengarah ke BPOM MD; jamu/herbal ke BPOM TR; kosmetik ke notifikasi; pakaian bayi dan mainan anak ke SNI wajib), lengkap dengan dasar aturan, tanggal cek 2026-09-29, dan tautan resmi. Tenggat wajib halal 17-10-2026 untuk usaha mikro-kecil pangan dicantumkan.
- Script `prioritas.py` (RICE/ICE): judul kolom Inggris diterima; keyakinan ditulis persen 0-100 (nilai seperti 0,8 tanpa % ditolak dengan pertanyaan "maksudnya 80%?"); angka ambigu seperti `10,000` ditolak; opsi `--kapasitas` dan aturan pembagian tahap Sekarang/Berikutnya/Nanti dijelaskan; 40 uji regresi.
- Cek akhir ditambah: ukuran keberhasilan ada dan jalur izin cocok dengan cara simpan/kemasan/klaim produk (produk dingin tidak diarahkan ke PIRT).

## Catatan revisi 1.0.0 (2026-09-29)
- Rilis awal (uji internal): spesifikasi produk untuk usaha kecil (masalah dan pembeli sasaran, ukuran/bahan/kemasan, HPP maksimal, roadmap), brief satu halaman untuk pihak ketiga (maklon/penjahit/pengrajin), pengurutan ide dengan script RICE/ICE, dan pengingat izin usaha. Struktur diadaptasi dari karya berlisensi Apache-2.0 dan MIT (lihat `ATTRIBUTION.md`).
