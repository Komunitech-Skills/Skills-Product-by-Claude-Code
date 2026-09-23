# Batasan: Kapan Menolak dan Merujuk ke Profesional

Skill ini untuk perjanjian **sederhana** antar pelaku usaha kecil/menengah atau perorangan di Indonesia. Untuk hal di bawah ini, **jangan menyusun draf perjanjian**. Jelaskan alasannya dengan sopan, lalu bantu persiapan konsultasi.

## A. Tolak menyusun draf, rujuk ke profesional
| Situasi | Rujuk ke | Alasan singkat |
|---|---|---|
| Jual beli, hibah, tukar-menukar, atau balik nama **tanah/rumah/bangunan/apartemen**, termasuk PPJB | Notaris/PPAT | Pengalihan hak atas tanah hanya dapat didaftarkan dengan akta PPAT (PP 24/1997 Ps. 37) |
| **Investasi**, penyertaan modal/saham, pendirian atau jual beli saham PT/CV, janji **imbal hasil tetap/pasti**, atau **mengumpulkan dana dari banyak orang** | Pengacara/notaris; cek aturan OJK | Risiko pelanggaran aturan penghimpunan dana & pasar modal |
| Pihak **asing** (WNA, perusahaan luar negeri), pembayaran valuta asing, atau pilihan hukum negara lain | Pengacara | Wajib dwibahasa (UU 24/2009 Ps. 31) dan ada isu hukum yang berlaku |
| Utang-piutang uang dengan **jaminan** (sertifikat, BPKB/fidusia, hak tanggungan, gadai) atau pinjaman berbunga | Notaris/pengacara | Jaminan perlu akta & pendaftaran khusus |
| **Perjanjian kerja karyawan** (PKWT/PKWTT), outsourcing, PHK, pesangon | Konsultan HR/pengacara ketenagakerjaan | Aturan ketenagakerjaan khusus dan dinamis |
| **Waralaba**, lisensi merek/paten, pengalihan hak cipta bernilai besar | Pengacara/konsultan KI | Ada aturan & pendaftaran khusus |
| Kontrak dengan **instansi pemerintah/BUMN/BUMD** (pengadaan) | Bagian hukum instansi/pengacara | Mengikuti aturan pengadaan dan dokumen standar instansi |
| **Sudah ada sengketa**: somasi, wanprestasi berjalan, laporan polisi, gugatan | Pengacara/LBH | Butuh strategi hukum, bukan template |
| Perjanjian perkawinan, waris, wasiat, hak asuh, pengakuan anak | Notaris/pengacara keluarga | Hukum keluarga/waris |
| Hal ilegal atau melanggar kesusilaan (mis. jual beli barang terlarang, "pinjam nama", nominee, suap, menghindari pajak) | Tidak dilayani | Sebab tidak halal, batal demi hukum (Ps. 1320 & 1337 KUHPerdata) |

**Template jawaban penolakan (sesuaikan):**
> Untuk [situasi], saya tidak menyusun draf perjanjian karena [alasan singkat]. Kesalahan kecil di dokumen seperti ini bisa berakibat besar, jadi sebaiknya dibuat/diperiksa oleh [notaris/PPAT/pengacara].
> Yang bisa saya bantu sekarang:
> 1. Daftar dokumen yang perlu disiapkan: [KTP, KK, NPWP, sertifikat, akta pendirian, dll.]
> 2. Daftar pertanyaan untuk ditanyakan ke [profesional]: [3–6 pertanyaan].
> 3. Ringkasan kesepakatan (bukan perjanjian) untuk dibawa saat konsultasi.
> Bila biaya menjadi kendala, bisa mencari Lembaga Bantuan Hukum (LBH) atau layanan konsultasi hukum kampus di kota Anda.

## B. Boleh dibantu, tetapi dengan peringatan keras
- Nilai perjanjian **≥ Rp500.000.000** atau jangka waktu **> 5 tahun** (patokan kebijakan skill). Tandai di atas draf: **"DRAF BAHAN DISKUSI, WAJIB DITINJAU PENGACARA SEBELUM DITANDATANGANI"**.
- Wilayah **eksklusif**, larangan bersaing (non-compete), denda besar atau ganti rugi pasti, pengalihan hak kekayaan intelektual, atau klausul arbitrase. Beri tanda `> ⚠ TINJAU PENGACARA` di pasalnya.
- Salah satu pihak **badan usaha** (PT/CV/koperasi/yayasan). Minta dasar kewenangan penanda tangan (akta/anggaran dasar/surat kuasa).
- Pihak di bawah 21 tahun dan belum menikah. Perlu wali/orang tua; sarankan konsultasi.

## C. Deteksi otomatis
`python3 <folder-skill-ini>/scripts/perjanjian.py cek draf.md` menandai kata kunci risiko (tanah/PPAT, saham/investasi, pihak asing/valas, jaminan, perjanjian kerja, waralaba) serta nilai ≥ Rp500 juta sebagai **RUJUK PROFESIONAL**. Deteksi ini hanya bantuan. Tetap nilai konteksnya sendiri.
