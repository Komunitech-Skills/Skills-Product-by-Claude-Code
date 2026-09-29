# Privasi & etika KPI tim

Skor kinerja per orang adalah **data pribadi karyawan** (UU No. 27 Tahun 2022 tentang
Pelindungan Data Pribadi). Pegangan skill ini:

## Penyimpanan & akses
- Semua file (rencana, realisasi, hasil) disimpan **di komputer pengguna**. Script tidak
  mengirim data ke mana pun.
- Laporan per orang hanya untuk **pemilik/manajer yang berwenang**. Jangan kirim ke grup kantor.
  Untuk papan target/grup, pakai `--tanpa-nama` (perusahaan & divisi saja; di teks maupun JSON
  tidak ada nama orang, hanya hitungan seperti "1 orang belum lengkap"). Skor divisi berisi satu
  orang dinilai = skor pribadi, jadi di `--tanpa-nama` divisi seperti itu digabung dengan divisi kecil
  lain (bobot rata-rata sama dengan skor perusahaan, sehingga tidak bisa dihitung balik) atau, bila
  tidak ada divisi lain, disembunyikan. Jangan menambahkan kembali skor divisi itu secara manual.
- Setiap karyawan berhak melihat **rincian KPI miliknya sendiri** (`--orang "Nama"`), bukan
  milik rekan kerja.
- Laporan per orang **diurutkan per divisi & nama, bukan peringkat**. Jangan membuat "papan
  juara/terburuk" yang mempermalukan.
- Simpan secukupnya: nama panggilan + divisi sudah cukup. Tidak perlu NIK, alamat, atau nomor HP
  di file KPI.
- Saran: jalankan skill `cek-privasi-openclaw` sebelum mengaktifkan laporan terjadwal.

## Dasbor lokal (`ekspor-db`)
- `kpi.db`, `kpi-metadata.yml`, dan CSV Grist berisi skor per orang = data pribadi. Simpan di komputer
  pemilik/manajer yang berwenang; jangan di folder bersama, drive publik, atau dikirim lewat grup.
- Datasette/Grist dijalankan **hanya di `127.0.0.1`/`localhost`**. Jangan `--host 0.0.0.0`,
  port-forward, tunnel (ngrok dsb.), atau tautan publik Grist.
- Untuk layar bersama atau berbagi dengan konsultan: `--anonim` (kode P01.. acak, bukan urut abjad;
  catatan realisasi tidak ikut). Simpan `kunci-kode-RAHASIA.csv` terpisah. Divisi berisi 1 orang
  tetap mudah ditebak: `--anonim-divisi`. Kode anonim bukan jaminan mutlak (orang yang tahu angka
  targetnya bisa menebak); untuk tim sangat kecil pakai laporan `--tanpa-nama`.
- Hapus `kpi.db`/CSV bila sudah tidak diperlukan; bisa dibuat ulang dari file rencana & realisasi.

## KPI bukan pengawasan
- Ukur **hasil kerja** (omzet, pesanan terkirim, komplain selesai), bukan gerak-gerik orang.
- Skill ini **menolak** membantu: pelacakan lokasi diam-diam, membaca chat pribadi karyawan,
  rekam layar/keystroke, atau menilai dari media sosial pribadi.
- Teks grup WA hanya dipakai bila grup itu memang grup kerja untuk melapor angka, dan hasilnya
  hanya **draf** yang wajib dikonfirmasi.

## Bukan dasar keputusan otomatis
- Skor KPI adalah **bahan diskusi & pembinaan**. Skill ini tidak memutuskan PHK, sanksi,
  penurunan gaji, atau bonus secara otomatis, dan tidak menulis rekomendasi "pecat".
- Sebelum keputusan kepegawaian: dengarkan penjelasan karyawan (1:1), periksa faktor di luar
  kendalinya (stok kosong, target tidak realistis, alat rusak), beri waktu perbaikan tertulis.
- Sanksi/PHK mengikuti peraturan perusahaan, PKB/PK, dan UU Ketenagakerjaan (termasuk perubahan
  dalam UU Cipta Kerja dan PP 35/2021). Untuk surat peringatan pakai skill
  `surat-peringatan-karyawan`; untuk sengketa, konsultasikan ke HR/konsultan hukum atau Disnaker.
  Skill ini tidak memberi nasihat hukum.
- Bila KPI dikaitkan dengan bonus/insentif: tuliskan aturannya di awal periode, disepakati,
  dan sama untuk semua orang di peran yang sama. Menghitung bonus bukan bagian skill ini.

## Adil
- Target disepakati bersama dan berdasar data (lihat `katalog-kpi.md` §11).
- Data yang telat dilaporkan **tidak otomatis** dianggap gagal (mode default `tandai`).
- Catat konteks di kolom `catatan` (sakit, cuti, stok kosong, banjir) dan bahas di 1:1.
- Karyawan baru (< 3 bulan): pakai target masa belajar atau tanpa penilaian.
