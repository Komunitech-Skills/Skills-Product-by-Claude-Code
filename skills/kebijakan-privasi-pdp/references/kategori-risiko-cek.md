# Kategori Risiko untuk Mode CEK (dibaca agent, bukan dicocokkan kata kunci)

Dipakai di **Mode 3 langkah 1**, sebelum script dijalankan. Tujuannya menilai **makna** setiap kalimat, bukan mencari kata tertentu. Kalimat berisiko sering ditulis dengan eufemisme, bahasa santai, terjemahan mesin, kalimat pasif, atau bahasa hukum yang berbelit. Contoh parafrasa di bawah **bukan daftar lengkap**; kalimat lain dengan makna sama tetap masuk kategori itu.

Dasar pasal mengacu pada UU 27/2022 (UU PDP), dicek 25 September 2026; status verifikasi per pasal ada di `dasar-hukum.md` (pasal bertanda ⚠️ dikutip sebagai rentang). Bukan nasihat hukum.

## Cara memakai
1. Baca dokumen **kalimat demi kalimat**. Tandai setiap kalimat yang membahas: siapa yang menerima data, untuk apa, berapa lama disimpan, bagaimana persetujuan diperoleh, hak pengguna, anak, data kesehatan/biometrik/keuangan, lokasi/perangkat, luar negeri, tanggung jawab & kebocoran, perubahan kebijakan, hukum yang berlaku.
2. Untuk tiap kalimat yang ditandai, tanyakan: **"Apakah kalimat ini, apa pun kata-katanya, termasuk salah satu kategori K1–K16?"**
3. Periksa juga yang **tidak ada**: kategori K9 (hak) dan K12 (data spesifik) sering berisiko karena hal wajib tidak ditulis, bukan karena ada kalimat buruk.
4. Negasi: "Kami **tidak** menjual data Anda kepada siapa pun" = patuh. Tetapi klausa kedua tetap dinilai: "tidak menjual, **tetapi** dapat membagikan ke mitra" = berisiko.
5. Catat tiap temuan: kategori · kutipan kalimat persis · tingkat · risiko (dengan pasal) · teks perbaikan siap tempel.

Tingkat: **TINGGI** = kemungkinan melanggar larangan/kewajiban tegas atau merugikan besar bagi pengguna; **SEDANG** = tidak memenuhi prinsip atau kurang jelas; dapat dinaikkan ke TINGGI bila menyangkut data spesifik atau anak.

## Tabel kategori

### K1 — Penjualan, penyewaan, atau monetisasi data · TINGGI
- ID: "data dapat dialihkan dengan imbalan", "database pelanggan kami salurkan ke rekan bisnis, lumayan buat pemasukan", "memonetisasi wawasan dari profil Anda", "mengkomersialkan basis data pelanggan", "nomor kakak kita titipkan ke partner jualan".
- EN: "may sell, rent or lease", "we may license customer data", "made available to partners for consideration", "we monetize insights about you", "exchange data with partners for value".
- Dasar: Ps. 65 ayat (2)–(3) (larangan mengungkapkan/menggunakan secara melawan hukum), Ps. 67 (pidana), Ps. 20 (tidak ada dasar pemrosesan sah).
- Perbaikan: hapus; tulis "Kami tidak menjual, menyewakan, atau memperdagangkan data pribadi Anda."

### K2 — Berbagi ke pihak lain untuk iklan, pemasaran, atau profiling mereka · TINGGI bila data spesifik/tanpa persetujuan, selain itu SEDANG
- ID: "kami kolaborasikan dengan jaringan UMKM binaan agar Anda dapat penawaran", "diteruskan ke agensi iklan", "dibagikan ke mitra strategis untuk pengembangan produk mereka", "kami bantu salurkan ke rekan bisnis".
- EN: "made available to our affiliates and business partners to develop their products", "shared with our ad buddies/ad partners", "insights shared with data partners for their own marketing", "used to build a profile for tailored offers from third parties".
- Dasar: Ps. 16 ayat (2) (terbatas & spesifik), Ps. 20 ayat (2) huruf a & Ps. 22 (persetujuan eksplisit per tujuan), Ps. 21 (sebut penerima).
- Perbaikan: sebut penerima & tujuan spesifik; hanya dengan persetujuan aktif terpisah yang bisa ditolak tanpa kehilangan layanan.

### K3 — Persetujuan tersirat, diam = setuju, atau persetujuan dibundel · TINGGI
- ID: "dengan melakukan chat kepada admin, Anda dianggap menyetujui (termasuk promo)", "dengan tetap membuka halaman ini", "bila tidak membalas dalam 7 hari kami anggap setuju", satu centang untuk semua tujuan, kotak yang sudah tercentang, "setuju semua ketentuan termasuk data kesehatan".
- EN: "continued use constitutes acceptance", "your silence shall constitute consent", "unless you object", "by registering you agree to all processing including marketing", "opt-out" untuk hal yang wajib opt-in.
- Dasar: Ps. 20 ayat (2) huruf a, Ps. 22 (tertulis/terekam, eksplisit, per tujuan), Ps. 24 (bukti persetujuan).
- Perbaikan: pemberitahuan untuk data yang memang perlu layanan (dasar perjanjian); persetujuan aktif **per tujuan** untuk promo, testimoni, foto, data spesifik.

### K4 — Tujuan tidak terbatas atau perubahan tujuan tanpa persetujuan ulang · SEDANG (TINGGI bila data spesifik)
- ID: "untuk tujuan apa pun yang kami anggap sesuai", "keperluan lain yang berkaitan dengan bisnis kami", "sewaktu-waktu dapat mengubah tujuan pemrosesan tanpa persetujuan ulang".
- EN: "for any purpose we see fit", "for other business purposes", "we may use your data for new purposes without further notice".
- Dasar: Ps. 16 ayat (2) huruf b (tujuan spesifik), Ps. 21 ayat (2) (beri tahu sebelum berubah), Ps. 20 (dasar untuk tujuan baru).
- Perbaikan: daftar tujuan spesifik; "Bila tujuan berubah, kami memberi tahu Anda lebih dulu dan meminta persetujuan baru bila diperlukan."

### K5 — Pengalihan data saat merger/akuisisi/penjualan usaha tanpa pemberitahuan · SEDANG
- ID: "data pelanggan menjadi aset yang ikut dialihkan bila usaha dijual, tanpa pemberitahuan", "pembeli usaha berhak memakai data untuk keperluannya".
- EN: "in a merger or acquisition your data may be transferred as a business asset without notice", "the acquirer may use data for any purpose".
- Dasar: Ps. 48 (pengalihan pengendali wajib diberitahukan kepada subjek data — ⚠️ nomor pasal belum dicocokkan naskah, kutip sebagai "UU PDP tentang penggabungan/pemisahan/pengambilalihan"), Ps. 16, 21.
- Perbaikan: "Bila usaha kami bergabung/diambil alih, kami memberi tahu Anda sebelum dan sesudah data dialihkan, dan pihak baru terikat pada kebijakan ini." (UU PDP Ps. 48: pemberitahuan sebelum dan sesudah pengalihan)

### K6 — Transfer ke luar negeri tanpa jaminan atau tanpa disebut · SEDANG (TINGGI untuk data spesifik)
- ID: "data dapat dipindahkan ke server di negara mana pun", "dikelola mitra di luar negeri" tanpa penjelasan pelindungan, atau klaim "semua data di Indonesia" padahal memakai WhatsApp/Google Sheets/Drive/cloud asing.
- EN: "hosted in Singapore" tanpa jaminan setara, "may be stored in any country where our vendors operate".
- Dasar: Ps. 56 (negara tujuan setara → atau pelindungan memadai & mengikat → atau persetujuan).
- Perbaikan: sebut layanan & negaranya bila diketahui, jelaskan jaminan (perjanjian/standar penyedia) atau minta persetujuan.

### K7 — Masa simpan tidak terbatas atau tidak jelas · TINGGI bila "selamanya"/data identitas & spesifik, SEDANG bila samar
- ID: "disimpan untuk selamanya", "kami arsipkan tanpa batas waktu", "foto KTP kami simpan terus di HP admin, jaga-jaga", "selama diperlukan" tanpa ukuran.
- EN: "retained indefinitely", "kept for as long as we wish", "we never delete".
- Dasar: Ps. 16 ayat (2) (dihapus setelah masa retensi), Ps. 21 ayat (1) (jangka retensi), Ps. 43 (kewajiban hapus).
- Perbaikan: masa simpan per jenis data (mis. transaksi 10 tahun untuk pajak; chat 1 tahun; KTP reseller dihapus saat kerja sama berakhir).

### K8 — Pelepasan tanggung jawab kebocoran, penundaan atau peniadaan pemberitahuan · TINGGI
- ID: "tidak bertanggung jawab jika terjadi kebocoran akibat peretasan", "pengguna melepaskan segala hak untuk menuntut", "pemberitahuan kebocoran disampaikan bila kami anggap perlu", "kami memberi tahu dalam 30 hari".
- EN: "shall bear no liability whatsoever for any unauthorized access or disclosure", "you waive all claims", "we may notify you at our discretion", "we will notify you within a reasonable time".
- Dasar: Ps. 35–39 (keamanan), Ps. 46 (pemberitahuan tertulis ≤ 3×24 jam ke subjek data & lembaga), Ps. 47 (tanggung jawab pengendali), Ps. 5–13 (termasuk hak gugat ganti rugi; pemetaan per pasal ⚠️).
- Perbaikan: komitmen langkah keamanan nyata + "Bila terjadi kegagalan pelindungan data, kami memberi tahu Anda dan lembaga berwenang secara tertulis paling lambat 3×24 jam."

### K9 — Pembatasan atau penolakan hak subjek data, biaya/syarat berlebihan · TINGGI bila menolak/diskresi, SEDANG bila hak tidak lengkap
- ID: "permintaan penghapusan tidak dapat dilayani dalam keadaan apa pun", "hapus data dipertimbangkan sesuai kebijakan kami", "persetujuan bersifat final dan tidak dapat ditarik kembali", "permintaan dikenakan biaya administrasi Rp500.000", "wajib datang langsung membawa surat notaris", "diproses 30 hari kerja".
- EN: "deletion at the Clinic's sole discretion", "consent is irrevocable", "a fee applies to each access request", "requests are handled within 60 days".
- Juga berisiko bila **tidak ditulis**: hak akses, koreksi, hapus, tarik persetujuan, keberatan; cara mengajukan; batas 3×24 jam.
- Dasar: Ps. 5–13 (hak), Ps. 30 & 32 (koreksi/akses 3×24 jam), Ps. 40 (tarik persetujuan, berhenti ≤ 3×24 jam), Ps. 43 (hapus).
- Perbaikan: daftar hak lengkap + kanal pengajuan + 3×24 jam; pengecualian hanya yang diwajibkan hukum (mis. catatan pajak, rekam medis) dengan alasannya.

### K10 — Data anak tanpa persetujuan orang tua/wali · TINGGI
- ID: "anak 10 tahun ke atas dapat mendaftar sendiri tanpa izin orang tua", "siswa cukup mengisi formulir sendiri", batas usia 13 tahun.
- EN: "patients under 18 may register themselves", "users aged 13 and over may sign up without parental consent", "under the age of 13" (COPPA).
- Dasar: Ps. 25 (persetujuan orang tua dan/atau wali), UU 35/2014 Ps. 1 angka 1 (anak = belum 18 tahun).
- Perbaikan: "Data anak di bawah 18 tahun hanya diproses dengan persetujuan orang tua/wali."

### K11 — Data spesifik (kesehatan, biometrik, genetika, keuangan, catatan kejahatan) tanpa dasar & pengamanan · TINGGI
- ID: "foto perkembangan pasien dipakai untuk testimoni kecuali Anda keberatan", "rekap keluhan pasien di Google Form/grup WA", "swafoto sambil memegang KTP" untuk hal yang tidak memerlukannya, "sidik jari untuk absensi" tanpa pilihan.
- EN: "progress photos may be used in testimonials unless you object in writing", "health data shared with partners", "we collect your face scan to personalise ads".
- Dasar: Ps. 4 ayat (2) (data spesifik), Ps. 20 & 22 (persetujuan eksplisit), Ps. 34 (penilaian dampak), Ps. 16 ayat (2) (minimisasi).
- Perbaikan: sebut sebagai data spesifik, dasar pemrosesan yang jelas, persetujuan eksplisit terpisah untuk pemakaian tambahan (testimoni/foto), akses terbatas; hapus pengumpulan yang tidak perlu.

### K12 — Data berlebih, pelacakan lokasi atau akses perangkat yang tak bisa dimatikan · SEDANG (TINGGI bila tak bisa ditolak)
- ID: "aplikasi terus merekam lokasi di latar belakang dan tidak dapat dimatikan", "mengakses seluruh kontak dan galeri", "meminta KTP + swafoto untuk pembelian biasa".
- EN: "we continuously collect precise location even when the app is closed", "access to all data on your device".
- Dasar: Ps. 16 ayat (2) huruf a (terbatas & spesifik), Ps. 5–13 (hak menolak/mengakhiri pemrosesan).
- Perbaikan: batasi ke data yang benar-benar perlu; lokasi hanya saat fitur dipakai dan bisa dimatikan.

### K13 — Perubahan kebijakan sepihak tanpa pemberitahuan · SEDANG
- ID: "kebijakan dapat berubah sewaktu-waktu dan berlaku sejak diunggah", "silakan cek halaman ini secara berkala".
- EN: "we may update this policy at any time without notice", "changes are effective immediately upon posting".
- Dasar: Ps. 21 ayat (2) (beri tahu sebelum perubahan).
- Perbaikan: "Perubahan kami umumkan lewat [kanal] paling lambat [isi: 7] hari sebelum berlaku."

### K14 — Hukum/yurisdiksi asing yang menyingkirkan UU PDP · SEDANG (TINGGI bila menghilangkan hak)
- ID: "kebijakan ini tunduk pada hukum Singapura dan sengketa hanya di pengadilan sana", "hak Anda mengikuti GDPR", "berlaku ketentuan California".
- EN: "governed exclusively by the laws of Delaware", "you waive rights under local law", sisa GDPR/CCPA dari template luar.
- Dasar: Ps. 2 (UU PDP berlaku bagi pemrosesan yang berakibat hukum di Indonesia atau atas WNI di luar negeri — ⚠️ kutip sebagai "ruang lingkup UU PDP"), Ps. 5–13 (hak tidak bisa dilepas).
- Perbaikan: rujuk UU 27/2022; hapus pelepasan hak; bila memakai hukum lain, tegaskan hak menurut UU PDP tetap berlaku.

### K15 — Klaim keamanan berlebihan atau janji palsu · SEDANG
- ID/EN: "100% aman", "tidak mungkin bocor", "completely secure", atau klaim enkripsi/sertifikasi yang tidak dilakukan.
- Dasar: Ps. 35 (keamanan nyata), Ps. 46 (kesiapan menangani kebocoran). "Tidak ada sistem yang 100% aman" **bukan** masalah.
- Perbaikan: tulis langkah keamanan yang benar-benar dilakukan.

### K16 — Isi tidak cocok dengan praktik nyata atau salinan dari usaha lain · SEDANG (TINGGI bila menutupi praktik terlarang)
- Tanda: nama perusahaan lain, mata uang/alamat asing, "tidak ada transfer LN" padahal pakai WA/Google, layanan yang tidak dipakai, tidak ada versi Bahasa Indonesia.
- Dasar: Ps. 16 ayat (2) (transparan), Ps. 21.
- Perbaikan: tulis ulang sesuai praktik (Mode 1 dengan isi lama).

## Selisih dengan script (wajib dijelaskan di laporan)
- **Agent menemukan, script tidak:** tulis "tidak dikenali pola kata kunci (parafrasa)". Ini normal; recall script pada kalimat parafrasa rendah (uji buta v1.0.2: ±4 dari 10).
- **Script menandai, agent tidak setuju:** jelaskan alasannya (mis. kalimat patuh berbentuk negasi, jebakan kata "jual" untuk produk). Jangan ikut menandai hanya karena script.
- **Status unsur script keliru** (sering pada teks EN: identitas "X ("the Clinic")", "Purpose:", "Sharing"): koreksi di tabel unsur, tandai "(dikoreksi manual)", dan jangan mengusulkan menambah hal yang sudah ada. Sebut skor script apa adanya lalu beri catatan bahwa skor terkoreksi lebih tinggi/rendah.
- **Unsur ADA tetapi isinya bermasalah** (mis. hak hapus ada tetapi "sole discretion", transfer LN disebut tetapi tanpa jaminan): status tetap ADA di tabel script, temuan dicatat di kategori terkait.
