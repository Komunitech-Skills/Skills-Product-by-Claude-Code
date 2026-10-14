# Riwayat perubahan — arus-kas-13minggu

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.5 (2026-10-14)
Perbaikan dari uji sebelum/sesudah OpenClaw 2026-10-14 (versi 1.0.4: 6,75 → 8,5 pada 4 skenario; satu skenario habis waktu):
- **Waktu jalan:** script kini menghitung sampai 4 opsi buatan sendiri dalam **satu panggilan** (`--opsi "Nama | aksi; aksi"`, boleh diulang, atau `--file-opsi opsi.txt`). Aksi: geser/tunda/majukan, ubah, kurangi/naikkan (% atau nominal), hapus, cicil, tambah masuk/keluar. Keluaran ringkas per opsi (`opsi_pengguna`): titik terendah (minggu + saldo), minggu minus, minggu di bawah batas, saldo akhir, kewajiban tertunda. `--ringkas` membuang rincian per minggu untuk jalan opsi; `--terapkan` membuat tabel "sesudah tindakan" tanpa mengubah CSV; file CSV keluaran memuat baris simulasi opsi. Opsi ke-5 dst. tidak dihitung dan dilaporkan. SKILL.md membatasi: 1 jalan dasar + 1 jalan semua opsi (target balasan < 3 menit).
- **Deskripsi opsi persis:** setiap opsi (bawaan maupun buatan sendiri) kini punya `deskripsi` — pos, nominal, minggu asal → tujuan, plus nomor baris CSV di `rincian`. Opsi bawaan "percepat piutang" yang memajukan lebih dari satu pembayaran diberi catatan. SKILL.md mewajibkan agent menyalin `deskripsi`, bukan mengarang (temuan: DP disebut sendirian padahal angka simulasi juga memajukan pelunasan Januari).
- **Pemisah CSV:** `csv.Sniffer` diganti deteksi dari baris judul (`;`, `,`, tab, `|`; dipilih yang mengenali kolom wajib terbanyak, baris judul dicari di 10 baris berisi pertama). `;` berlebih / sel kosong di akhir baris diterima. Baris dengan isian lebih banyak dari judul dilewati dengan nomor baris + isinya; galat "Kolom wajib tidak ditemukan" menyebut baris judul dan kolom yang terbaca. `--pemisah` tetap hanya untuk keluaran.
- **Pengaman:** gaji/upah/THR/cicilan/pajak/BPJS ditolak bila diminta digeser, dikurangi, dicicil, atau dihapus lewat opsi (galat per opsi, opsi lain tetap dihitung).
- **Aturan kerja:** blok baru "UNTUK AGENT SAJA" — cari berkas hanya di lampiran/folder kerja (dilarang `find /`), minta pengguna menempel data bila berkas tidak ada; semua berkas kerja ditulis di folder kerja saat ini (bukan `/tmp`).
- Konstanta `VERSI = "1.0.5"` + `--versi`; `references/opsi-tindakan.md` disesuaikan (tidak lagi "ubah CSV lalu jalankan ulang"). Tes regresi bertambah (total 71 cek): `;` berlebih, koma/tab, baris kelebihan isian, beberapa opsi satu panggilan dicocokkan dengan hitungan manual, deskripsi opsi, pengaman gaji, batas 4 opsi, `--file-opsi`, `--terapkan`, cicil.
- Rumus arus kas tidak berubah (tabel 13 minggu tetap sama dengan versi 1.0.4).

## Catatan revisi 1.0.4 (2026-10-13)
- Batasan di SKILL.md ditambah satu aturan: setiap tarif/aturan disebut dengan dasar aturan + tahun; angka hanya dari script/input pengguna; nilai yang tidak diberikan pengguna ditandai asumsi (tanpa label "wajar/umum/lazim" yang tidak bersumber).
- Contoh uji `examples/02`: THR diberi dasar Permenaker 6/2016 (masa kerja ≥ 12 bulan = 1 bulan upah; < 12 bulan proporsional); tanggal Lebaran tidak lagi ditebak, pengguna mengisi tanggal Idulfitri menurut kalender resmi. Saldo minggu 10 dengan THR (Rp 90.500.000) dicek ulang dengan script.

## Catatan revisi 1.0.3 (2026-10-01)
Perbaikan dari uji OpenClaw asli (arus kas 13 minggu, info kurang lalu dilengkapi):
- Script kini mencetak **kejadian per minggu** (pos masuk/keluar apa saja yang jatuh di tiap minggu) dan rincian minggu kritis. AI wajib mengutip nomor minggu dan pos dari daftar ini, sehingga tidak ada lagi salah sebut "cicilan di minggu 12" padahal di minggu 11.
- Pos yang ditanyakan tetapi belum dijawab (mis. BPJS, PPh 21) ditulis jelas sebagai "Belum termasuk" di Asumsi.
- Path script ditulis jelas (subfolder `scripts/`); AI dilarang mencari file ke seluruh disk.
