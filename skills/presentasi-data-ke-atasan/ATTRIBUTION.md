# Atribusi

Skill `presentasi-data-ke-atasan` **diadaptasi dan diubah secara substansial** dari dua
skill dalam koleksi **data-analytics-skills** karya **Nimrod Fisher**:

- Sumber: https://github.com/nimrodfisher/data-analytics-skills
  (folder `04-data-storytelling-visualization/executive-summary-generator` dan
  `04-data-storytelling-visualization/visualization-builder`)
- Lisensi sumber: MIT (teks lengkap di `LICENSE-MIT`)
- Ditinjau: 2026-09-26 (audit keamanan: tidak ditemukan perintah destruktif, pengiriman
  data ke server luar, pembacaan kredensial, `curl | bash`, kode ter-obfuscate, atau
  instruksi tersembunyi/prompt injection di SKILL.md sumber maupun script Python-nya)

Adaptasi oleh Komunitech (komunitech.com). Penggunaan versi adaptasi ini tunduk pada
`LISENSI.txt` yang disertakan dalam paket pembelian, **tanpa mengurangi** ketentuan
lisensi MIT di atas untuk bagian yang berasal dari karya asli.

## Yang diambil dari sumber
- Gagasan inti "executive-summary-generator": memimpin dengan kesimpulan lebih dulu baru
  bukti (prinsip piramida — governing thought → key lines → evidence), memaksa setiap
  temuan membawa angka dampak bisnis, dan menutup dengan blok keputusan/rekomendasi yang
  menyebut aksi + PIC + tenggat.
- Gagasan inti "visualization-builder": memilih jenis grafik berdasarkan **jenis pesan**
  (perbandingan → batang, tren waktu → garis, komposisi → batang bertumpuk/pie terbatas,
  distribusi → histogram) lewat pohon keputusan, dan aturan judul grafik berisi
  kesimpulan bukan nama variabel.
- Gagasan umum: batasi jumlah insight/angka kunci ke 3–5 agar tidak membanjiri pembaca,
  dan sebutkan sumber data & periode di bagian bawah dokumen ringkasan.

## Yang diubah / ditambahkan oleh Komunitech
1. **100% Bahasa Indonesia**, termasuk seluruh instruksi, template, dan gaya komunikasi
   — sumber sepenuhnya berbahasa Inggris dan ditujukan untuk analis data profesional di
   perusahaan besar/startup.
2. **4 format output siap kirim yang benar-benar baru**: ringkasan WA 5 baris, email
   formal, 1 halaman eksekutif, dan skrip bicara 2 menit (`templates/`) — sumber hanya
   punya satu jenis output (dokumen "executive summary" 1–2 halaman generik) dan tidak
   membahas kanal WhatsApp maupun naskah bicara lisan sama sekali, karena bukan konteks
   pasar Indonesia.
3. **Angka wajib dihitung lewat script Decimal** (`scripts/hitung_perubahan.py`, ditulis
   dari nol, Python standar tanpa dependensi) untuk selisih & persen perubahan, dengan
   aturan pembulatan eksplisit (rupiah dibulatkan ke rupiah terdekat, persen 1 desimal).
   Sumber tidak menyediakan script perhitungan sama sekali — hanya instruksi tekstual
   "quantify the business impact", tanpa jaminan angka benar-benar dihitung, bukan
   dikira-kira oleh model.
4. **Gaya komunikasi kantor Indonesia ditulis dari nol**
   (`references/gaya-komunikasi.md`): sapaan per audiens (atasan/investor/bank/klien),
   format angka Rupiah & persen yang konsisten, larangan jargon konsultan, dan prinsip
   "sopan-langsung" (jujur soal kabar buruk tanpa menyalahkan pihak lain secara
   terbuka) — sumber tidak membahas norma komunikasi kantor Indonesia maupun format
   mata uang Rupiah sama sekali.
5. **Panduan pilih grafik dilokalkan & disederhanakan untuk audiens awam**
   (`references/pilih-grafik.md`): ditulis ulang jadi langkah pilih cepat dengan contoh
   kasus lokal (omzet turun bulan puasa) dan aturan eksplisit sumbu-Y batang harus mulai
   dari 0 (mencegah grafik menyesatkan) — versi sumber (`chart_selection_guide.md`)
   membahas DPI ekspor cetak dan palet warna colorblind teknis yang di luar cakupan
   audiens awam non-desainer di sini, sehingga tidak disalin.
6. **Contoh kasus lokal ditulis dari nol**: omzet turun bulan puasa, biaya iklan naik,
   stok menumpuk (`examples/`) — sumber memakai contoh generik "mobile churn $800K
   ARR", "EMEA underperformance" yang tidak relevan untuk UMKM/profesional Indonesia.
7. **Dihapus:** konsep `dashboard-specification` & `insight-synthesis` (skill terpisah
   di sumber, di luar cakupan "ubah angka jadi pesan siap kirim" yang jadi fokus skill
   ini), rujukan ke `matplotlib`/`seaborn` (`scripts/chart_builder.py` sumber butuh
   instalasi paket pihak ketiga — bertentangan dengan prinsip "tanpa setup" library
   ini; skill ini hanya menentukan **jenis** grafik yang tepat, pembuatan gambarnya
   diserahkan ke tool visualisasi yang tersedia di environment), dan format ekspor
   300/150 DPI (tidak relevan untuk kanal WA/email/1 halaman digital).
8. **Ditambahkan** batasan eksplisit "tidak boleh mengarang angka" dan penanganan kasus
   data kualitatif-saja/angka mencurigakan (Batasan & Penanganan Error di SKILL.md) —
   sumber mengasumsikan analis profesional yang sudah punya data valid, tidak membahas
   penanganan input awam/tidak lengkap.
9. **Disebutkan integrasi** dengan skill lain di library ini (`analisis-excel`,
   `rekap-penjualan-csv` sebagai sumber data; `presentasi-instan` untuk deck
   bertahap; `laporan-status-kantor` untuk laporan rutin non-satu-angka-kunci) agar
   tidak tumpang tindih — konsep ini tidak ada di sumber karena sumber berdiri sendiri.

Seluruh teks SKILL.md, README, referensi, dan template ditulis ulang dalam Bahasa
Indonesia dengan struktur dan penekanan berbeda untuk pengguna bisnis Indonesia yang
awam teknologi; tidak ada bagian teks sumber yang disalin utuh — hanya konsep
struktural (piramida kesimpulan-dulu, pohon keputusan pilih grafik) yang dipelajari lalu
ditulis ulang dengan implementasi dan contoh sendiri.
