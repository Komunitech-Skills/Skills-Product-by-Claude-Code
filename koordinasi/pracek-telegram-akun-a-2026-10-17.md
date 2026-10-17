# Pra-cek Telegram Akun A (A-cepat) — 2026-10-17

Penguji: sub-agent penguji. Cara: uji simulasi kanal Telegram (`uji-tg.sh`, OpenClaw 2026.10.2 lokal, `--channel telegram`, tanpa kirim apa pun), HOME uji berisi hanya skill terkait, satu giliran, pesan = skenario normal pertama dari `examples/00-openclaw-sebelum-sesudah.md`. Hanya sisi DENGAN skill; pembanding TANPA skill memakai uji internal yang ada. Skor 1-10 menurut `koordinasi/alat-uji/brief/tester-umum.md`; angka kunci dihitung ulang penguji dengan Python. Daftar siap kirim: `scratchpad/openclaw-real/pilot/kandidat-a-cepat.json`.

## Kelompok 1

| Skill | Versi | Skor | Verdik | Catatan |
|---|---|---:|---|---|
| laporan-otomatis-terjadwal | 1.1.9 | 8,0 | SIAP KIRIM | CSV fiktif 57 nota 5-11 Okt dibuat penguji (CSV asli uji 1 Okt tidak tersimpan; pesan sama persis). Omzet Rp1.861.000, 103 pcs, rata-rata/hari Rp265.857, hari terbaik 6 Okt Rp311.000, terendah 7 Okt Rp209.000, terlaris Roti Bakar Keju 29 pcs Rp580.000: benar. Kurang: nama berkas CSV disebut; di HOME uji kanal Telegram belum terpasang sehingga jawaban berisi langkah pasang bot (di bot asli kanal sudah ada). Perlu rekap-penjualan-csv terpasang |
| checklist-keamanan-pangan-usaha | 1.0.3 | 8,0 | SIAP KIRIM | Ayam inti >=74 C (63 C ditolak), alergen telur + kelapa, halal UMK wajib 18 Okt 2026, SPP-IRT tidak untuk nasi box: benar. Panjang 8.697 karakter, tanpa tabel (dikirim sebagai 3 pesan). Perizinan ditandai PERLU REVIEW |
| pph21-ter | 1.0.6 | 8,5 | SIAP KIRIM | Jan-Nov Rp2.040.000 (Maret 7% Rp1.190.000), setahun Rp1.945.750 (neto Rp101.915.000, PKP Rp38.915.000), Desember lebih potong Rp94.250: dihitung ulang, benar. Tabel 4 kolom, 2.939 karakter. Disclaimer ada |
| hitung-thr | 1.0.11 | 8,0 | SIAP KIRIM | Andi Rp4.200.000, Sari Rp2.933.333, Dodi Rp1.808.333, Yanto Rp3.500.000, total Rp12.441.666, batas Rabu 3 Maret 2027, masa kerja 74/11/7/13 bulan: benar. Tabel 6 kolom agak lebar; draf grup tanpa nominal. 2.512 karakter |
| pph-final-umkm | 1.0.5 | 7,5 | TIDAK SIAP | Semua angka benar (Rp107.500 / Rp330.000 / total Rp437.500; kurang setor Rp165.000; sisa batas Rp4.212.500.000). Cacat tampilan: tabel 10 kolom di blok kode selebar ~120 karakter, harus digeser di ponsel (uji 16 Okt memakai tabel Markdown). Bila dikirim, hasil kemungkinan tetap sama; saran: kurator mempersempit kolom (mis. gabung "Kena pajak" dan "Batas setor" ke baris catatan) |

## Kelompok 2

Data contoh yang tidak tersimpan di `examples/` (absen-sept.csv, produk.csv) dan data kasir+CRM dibuat ulang oleh penguji (fiktif) di `scratchpad/openclaw-real/pilot/data-a-cepat/` dan `pilot/seed-laporan-harian.sh`; pesan uji sama persis dengan uji internal. Skenario dua giliran dijalankan dua giliran di sesi yang sama.

| Skill | Versi | Skor | Verdik | Catatan |
|---|---|---:|---|---|
| laporan-harian-usaha | 1.1.4 | 8,0 | SIAP KIRIM | Data diisi lewat skrip alat (kasir 16-17 Okt, CRM 3 kontak). Hari ini Rp172.600 (4 nota) vs kemarin Rp179.000 turun 3,6%, terlaris Kopi Susu Gula Aren 5x Rp84.600, metode bayar QRIS Rp88.000 / tunai Rp84.600: dihitung ulang, benar. Kurang: "Konversi 0,0% (0 dari 1)" di samping "Deal 1" terbaca kontradiktif (cacat lama S2). Data wajib ditanam di HOME bot; kasir-lokal + crm-wa harus terpasang |
| buku-stok | 1.1.6 | 7,5 | TIDAK SIAP | Angka benar: HPP kaos hitam M (24x35.000 + 50x34.500)/74 = Rp34.662, stok 74, nilai persediaan Rp3.825.000. Cacat: jalur `~/KomunitechData/stok.db` dan folder cadangan disebut di dua balasan; istilah SKU/HPP tanpa penjelasan |
| kasir-lokal | 1.1.7 | 8,0 | SIAP KIRIM | 2 kopi susu + 1 roti bakar Rp39.000, diskon 10% Rp3.900, total Rp35.100, kembalian Rp64.900: benar. Struk teks 32 kolom muat di ponsel. Kecil: nama perintah `buka-kasir` bocor di balasan ke-2; perlu produk.csv di workspace |
| absensi-lokal | 1.0.7 | 7,0 | TIDAK SIAP | Angka benar (Andi 3x/66 mnt, Joko 3x/75 mnt, Sari 0; bolong 14/09, Sari 21-22/09, Andi 25/09 tanpa tap pulang). Cacat: balasan pertama bertanya 5 hal (batas 3) tanpa mengerjakan apa pun dan menyebut jalur `~/KomunitechData/absensi/absensi.db`; rekap baru muncul setelah "ya". Berkas absen-sept.csv dibuat ulang penguji (121 tap) |
| buku-piutang | 1.0.5 | 8,0 | SIAP KIRIM | Jatuh tempo Bu Tini 15 Sep (lewat 32 hari), Kafe Senja 12 Sep sisa Rp1.400.000 (lewat 35 hari), Pak Joko 25 Okt; total lewat Rp2.650.000: benar. Draf tagih + tautan wa.me (manusia yang kirim). Tautan panjang ±900 karakter |

## Kelompok 3

Berkas contoh yang tidak tersimpan (meta-minggu-ini/lalu.csv, penjualan-september.csv) dibuat ulang penguji (fiktif) di `scratchpad/openclaw-real/pilot/data-a-cepat/`, dirancang agar angkanya sama dengan uji 1 Okt. Pesan uji sama persis dengan uji internal. kalender-pajak diuji sendirian (uji 1 Okt memakai paket 25 skill) dalam dua giliran.

| Skill | Versi | Skor | Verdik | Catatan |
|---|---|---:|---|---|
| laporan-iklan-mingguan | 1.0.11 | 7,0 | TIDAK SIAP | Semua angka benar (belanja Rp4.200.000 naik 40,0%; 114 chat naik 22,6% dari 93; Rp36.842/chat; 22,7% dari omzet; Hijab Instan Baru Rp91.667/chat = 2,5x; CPC/CTR iklan trafik benar). Cacat: kalimat "hasilnya itu chat WA masuk" disalahpahami sebagai perintah kirim ke WA, jawaban dibuka dengan "gateway", "pairing", "script resmi" dan menawarkan menyambung WhatsApp (bertentangan dengan aturan kanal); baris teknis "Kolom dibaca: nama='Campaign name' ..." ikut tampil |
| kalender-pajak | 1.0.7 | 8,0 | SIAP KIRIM | Giliran 1: 4 pertanyaan + tawaran asumsi cepat (sesuai desain skill, 513 karakter). Giliran 2: omzet Rp600jt merata -> kumulatif Rp500jt di Oktober (belum lewat), lewat di November, setoran pertama masa November paling lambat Selasa 15 Des 2026, SPT Tahunan 31 Maret 2027: benar. Kecil: kata "skill" muncul sekali |
| rekap-penjualan-csv | 1.2.5 | 8,5 | SIAP KIRIM | Omzet Rp5.519.000 (hanya Selesai), batal Rp238.000, refund Rp272.000, produk terlaris, tertinggi 5 Sep Rp549.000, terendah 18 Sep Rp35.000, seri 5 pesanan di 1 & 5 Sep: semua dihitung ulang, benar. Kecil: kata "script" sekali |

## Rangkuman pra-cek A-cepat (13 skill)

SIAP KIRIM (9): laporan-otomatis-terjadwal, checklist-keamanan-pangan-usaha, pph21-ter, hitung-thr, laporan-harian-usaha, kasir-lokal, buku-piutang, kalender-pajak, rekap-penjualan-csv. TIDAK SIAP (4): pph-final-umkm (tabel 10 kolom), buku-stok (jalur file), absensi-lokal (5 pertanyaan + jalur), laporan-iklan-mingguan (salah paham WA + istilah proses). Daftar siap kirim: `scratchpad/openclaw-real/pilot/kandidat-a-cepat.json`.

## gaji-umkm 1.0.13 (2026-10-17)

Uji simulasi kanal Telegram (uji-tg.sh), sisi DENGAN, HOME baru berisi hanya gaji-umkm 1.0.13 (versi repo), dua giliran di sesi yang sama: pesan `koordinasi/alat-uji/pilot/msgs-g21b.json` idx 9 (mention dihapus) lalu idx 10 "ya". Data fiktif `koordinasi/alat-uji/pilot/data/g21/karyawan.csv` (jalur `pilot/data/karyawan.csv` di papan tugas tidak ada; isinya sama dengan examples/08) → `data/karyawan.csv` di workspace uji. Tidak ada yang dikirim.

| Skill | Versi | Skor | Verdik | Catatan |
|---|---|---:|---|---|
| gaji-umkm | 1.0.13 | 8,5 | SIAP KIRIM | Giliran 1 (3.379 karakter, 1 bagian): 11 karyawan langsung dihitung, Lina **tertunda** dengan pilihan (a) data Jan–Agu / (b) angka SEMENTARA + tanya penuh/prorata (4.666.667 / 466.667). Setoran tanpa Lina: transfer Rp 65.412.866, BPJS Kes Rp 3.265.000, BPJS TK Rp 5.581.620, PPh 21 Rp 522.059, biaya Rp 75.031.545; Kiki prorata 5.400.000 × 16 ÷ 30 = 2.880.000 sebagai pilihan. Semua angka per karyawan & total dihitung ulang penguji (Decimal, TER A/B/C, BPJS, lembur Indah 9 × 5.400.000/173 = 280.925): **identik**. Tanpa nama perintah/opsi/jalur file. Giliran 2 "ya" (1.448 karakter): dianggap "simpan", data benar-benar tersimpan (database terbentuk di HOME uji), periode jujur belum dikunci, pertanyaan Lina & Kiki diulang, menawarkan slip draf 11 karyawan. Kurang: tabel Markdown 7 kolom tampil mentah di Telegram; prorata Kiki/Lina disebut "hari kerja" padahal hitungannya hari kalender (16/30, 14/30); label (a)/(b) hilang di giliran 2 |

## Kelompok 5 (pra-cek ulang, 2026-10-17)

Uji simulasi kanal Telegram (uji-tg.sh), sisi DENGAN, HOME baru berisi hanya skill versi repo, pesan sama dengan pra-cek lama (`pilot/kandidat-a-cepat.json`), data fiktif yang sama di `pilot/data-a-cepat/`. Tidak ada yang dikirim. Angka dihitung ulang penguji dengan Python.

| Skill | Versi | Skor | Verdik | Catatan |
|---|---|---:|---|---|
| pph-final-umkm | 1.0.6 | 8,5 | SIAP KIRIM | Cacat lama (tabel 10 kolom) hilang: daftar per bulan, 2.497 karakter. Agustus Rp107.500 (kena pajak Rp21.500.000), September Rp330.000, total Rp437.500; PPh 22 Rp345.000; kurang setor Rp165.000 (batas 15 Okt sudah lewat); Agustus lebih Rp72.500; sisa batas Rp4.212.500.000: benar. Disclaimer & pembulatan Coretax ada. Satu pertanyaan penutup |
| buku-stok | 1.1.7 | 8,5 | SIAP KIRIM | Cacat lama (jalur file) hilang. Pratinjau dulu, "Balas ya". SKU & HPP dijelaskan. HPP (24x35.000 + 50x34.500)/74 = Rp34.662, ongkir 25.000/50 = Rp500 per pcs, persediaan Rp3.825.000: benar. Giliran "ya" menyimpan dan jujur |
| absensi-lokal | 1.0.8 | 8,5 | SIAP KIRIM | Cacat lama hilang: giliran 1 langsung merekap (telat Andi 3x/66 mnt, Joko 3x/75 mnt, Sari 0; bolong 14/09, Sari 21-22/09, Andi 25/09 tanpa tap pulang) + 3 pertanyaan di akhir, tanpa jalur file. Giliran "ya" menyimpan 121 catatan (41+38+42). Kecil: total jam kerja selisih <=10 menit dari hitung detik penguji. Berkas absen-sept.csv fiktif dibuat penguji |
| laporan-iklan-mingguan | 1.0.12 | 8,0 | SIAP KIRIM | Cacat lama hilang: tidak lagi menawarkan sambung WhatsApp / gateway / pairing, tanpa baris "Kolom dibaca". Belanja Rp4.200.000 (+40,0%), 114 chat (+22,6%), Rp36.842/chat (+14,2%), 22,7% omzet, Hijab Instan Baru Rp91.667/chat (2,5x) disarankan ditinjau, iklan trafik/awareness tidak dinilai dari chat: semua benar. Kecil: periode tampil format ISO, istilah CPC/CPM/CTR tanpa penjelasan |

Rangkuman kelompok 5: keempatnya SIAP KIRIM; `pilot/kandidat-a-cepat.json` diperbarui (kelompok 5).

## Kelompok 6 (C10, 2026-10-17)

Uji simulasi kanal Telegram (uji-tg.sh), sisi DENGAN, HOME baru berisi hanya skill versi repo, satu giliran, pesan = skenario normal `examples/00-openclaw-sebelum-sesudah.md` (vikunja: kalimat "Hari ini" diganti Sabtu 17 Oktober 2026). Data/mock fiktif dibuat ulang penguji di `scratchpad/openclaw-real/pilot/data-a-cepat/<skill>/`. Tidak ada yang dikirim; tidak ada paket dipasang. Angka dihitung ulang penguji dengan Python. Daftar: `pilot/kandidat-a-cepat.json` (kelompok 6).

| Skill | Versi | Skor | Verdik | Catatan |
|---|---|---:|---|---|
| frappe-books-usaha | 1.0.10 | 8,5 | SIAP KIRIM | Berkas SQLite fiktif dibangun ulang (`buat_data.py`; generator bawaan `tests/data` tanpa buku besar menghasilkan laba rugi Rp0, dibuang). Penjualan Sep DPP Rp4.810.000 + PPN Rp511.500 = Rp5.321.500 (terbayar Rp2.934.000, belum Rp2.387.500), piutang keseluruhan Rp3.231.100 (3 invoice), HPP Rp3.770.000, laba kotor Rp1.040.000, beban Rp800.000, laba bersih Rp240.000: benar. Draf & invoice batal tidak dihitung. Kecil: rekap piutang pelanggan ikut dikirim ke "grup keluarga" tanpa peringatan privasi |
| grist-usaha | 1.0.10 | 8,5 | SIAP KIRIM | Berkas .grist tiruan 12 barang. Habis 2, menipis 5, aman 5; total nilai stok Rp2.698.000 (12 baris dihitung ulang): benar. Status disebut dari rumus Grist, total disebut hitungan sendiri. Tanpa jalur file |
| actual-budget-usaha | 1.0.8 | 7,5 | TIDAK SIAP | CSV mutasi BCA fiktif (angka sama dengan uji 2 Okt). 15 transaksi, 5 dilewati, masuk Rp12.958.125,40, keluar Rp7.499.875,08, saldo COCOK Rp9.708.250,32: benar. Cacat: 8 baris ditanyakan (3 kelompok, banyak sub-butir) tanpa default; istilah "Baris 7", nama berkas `-actual.csv`/`-ragu.csv`, "Split/Flip amount mati"; transfer pribadi tampil "450000.0 (keterangan terpotong)"; "Belum berkategori Rp5.833.750" tanpa tanda (bersih masuk) |
| vikunja-tugas | 1.0.13 | 7,5 | TIDAK SIAP | Tiga putaran (notulen fiktif buatan penguji). Putaran 1 (notulen berisi "Rabu depan"): **bug skrip** `vikunja.py` `cocok_tanggal_kata` menambah 7 hari ekstra pada "<hari> depan" (Sabtu 17 Okt: "Rabu depan" -> 28 Okt, benar 21 Okt; "Jumat depan" -> 30 Okt, benar 23 Okt; dicek dengan menjalankan fungsi); agen menandai selisih tapi jawaban penuh kata proses (skill, `dari-teks`, script, JSON `--batch`, nama berkas draf). Putaran 3 (notulen "sebelum hari Rabu", tanpa "depan"): tanggal benar (besok 18 Okt, Rabu 21 Okt, akhir bulan 31 Okt, Jumat depan 23 Okt; PIC/tenggat kosong ditandai), tetapi kalimat pembuka "pakai skill Vikunja (mode `dari-teks`...)". Perbaikan: koreksi aritmetika "<hari> depan" (hari X di minggu kalender berikutnya) dan larang menyebut skill/mode/berkas draf |
| umami-analitik | 1.0.6 | 8,5 | SIAP KIRIM | Perlu server tiruan Umami (stdlib, port 3000) hidup di mesin bot: `pilot/data-a-cepat/umami-analitik/CARA-JALAN.txt`. Putaran 1 gagal (server tiruan belum punya /api/heartbeat), putaran 2 salah geseran tanggal (kedua minggu sama), diperbaiki di server tiruan; putaran 3: minggu lalu (5-11 Okt) vs sebelumnya pengunjung 11 vs 4 (+175%), kunjungan 12 vs 4 (+200%), tayangan 23 vs 6 (+283%), bounce 50% -> 25%, halaman teratas, sumber (sosial 50% / langsung 33% / Google 17%): cocok rekaman, benar. Kecil: tabel tanpa, saran agak umum |

Rangkuman kelompok 6: SIAP KIRIM 3 (frappe-books-usaha, grist-usaha, umami-analitik), TIDAK SIAP 2 (actual-budget-usaha, vikunja-tugas). Catatan untuk gelombang: umami butuh server tiruan hidup; frappe pakai berkas dari `buat_data.py`; vikunja menunggu perbaikan `<hari> depan`.
