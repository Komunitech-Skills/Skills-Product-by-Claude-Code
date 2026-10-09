# 08 (uji ulang v1.0.1) — Normal 3: klinik gigi kecil, Medan (usaha jasa profesi)

- Tanggal: 2026-10-09 · Penguji independen · `claude-code (simulasi agent)`
- Data risiko: `data/08-klinik-gigi-medan-uji-ulang.json`. Tujuan: menguji cakupan "jasa" di description pada usaha profesi kesehatan.

## Pesan
> sy dokter gigi, buka klinik kecil di ruko medan, cuma sy dokternya + 2 asisten + 1 admin. sewa 5jt, gaji 3 staf total 9jt, listrik air 1,5jt, cicilan dental unit 4jt. bahan habis pakai sekitar 3jt tp naik turun. kas 30jt. perlu asuransi malpraktik ga? data pasien gimana? dana darurat brp?

## Jalannya script
`dana --biaya "Sewa ruko=5.000.000,Gaji 3 staf=9.000.000,Listrik air=1.500.000,Cicilan dental unit=4.000.000" --bulan 3 --kas 30.000.000 --cicil 12` (bahan habis pakai tidak dihitung: biaya variabel, disebut sebagai asumsi) dan `risiko data.json --dana 58.500.000`.

## Output SESUDAH (ringkas)
> **Asumsi:** klinik di ruko sewa, Medan; 1 dokter gigi (Anda) + 3 staf; bahan habis pakai tidak masuk biaya tetap karena naik-turun.
>
> | No | Risiko | K | D | Skor/Tingkat | Langkah murah | Perlu asuransi? |
> |---|---|---|---|---|---|---|
> | 1 | Anda sakit/cedera tangan (satu-satunya dokter) | 2 | 5 | 10 TINGGI | Kesepakatan dokter gigi pengganti (praktik bersama/locum), jadwal ulang pasien tertulis | Ya, pertimbangkan (kecelakaan diri/kesehatan pribadi) |
> | 2 | Kebakaran (kompresor, autoclave, korsleting) | 2 | 5 | 10 TINGGI | APAR, kompresor di ruang berventilasi, cek kabel autoclave | Ya, pertimbangkan |
> | 3 | Tuntutan pasien (komplikasi/dugaan malpraktik) | 2 | 5 | 10 TINGGI | Informed consent tertulis tiap tindakan, rekam medis lengkap, foto/rontgen sebelum-sesudah | Ya, pertimbangkan (tanggung gugat **profesi**, bukan tanggung gugat umum; tanyakan ke agen/organisasi profesi) |
> | 4 | Asisten tertusuk jarum/cedera kerja | 3 | 3 | 9 SEDANG | Wadah benda tajam, SOP pasca-tertusuk | BPJS (wajib bagi pemberi kerja, cek aturan terbaru) |
> | 5 | Dental unit rusak, praktik berhenti | 3 | 3 | 9 SEDANG | Servis berkala, nomor teknisi cadangan | Tidak perlu |
> | 6 | Izin praktik/STR/SIP terlambat diperpanjang | 2 | 4 | 8 SEDANG | Kalender pengingat 6 bulan sebelum habis | Tidak ada asuransi umum; pakai mitigasi lain |
> | 7 | Kebocoran data rekam medis pasien | 2 | 4 | 8 SEDANG | Kata sandi & akses terbatas, salinan cadangan, lemari arsip terkunci | Ya, pertimbangkan (tanyakan ketersediaan ke agen) |
> | 8 | Listrik padam saat tindakan | 3 | 2 | 6 SEDANG | UPS untuk alat kunci, lampu darurat | Tidak perlu |
> | 9 | Infeksi silang karena sterilisasi gagal | 1 | 5 | 5 SEDANG | Log autoclave harian, indikator sterilisasi | Ya, pertimbangkan (masuk tanggung gugat profesi) |
>
> Dana darurat 3 bulan: biaya tetap Rp19.500.000/bln → target **Rp58.500.000**; kas Rp30.000.000 (cukup 1,5 bulan); kekurangan **Rp28.500.000** → **Rp2.375.000/bulan selama 12 bulan**.
> Perlindungan umum tanpa merek, cek OJK, disclaimer; 3 pertanyaan (bahan habis pakai mau dimasukkan? nilai alat? sudah punya perlindungan profesi lewat organisasi?).

## Verifikasi (independen, Decimal)
Skor 10, 10, 10, 9, 9, 8, 8, 6, 5 cocok. 5.000.000 + 9.000.000 + 1.500.000 + 4.000.000 = 19.500.000; ×3 = 58.500.000; −30.000.000 = 28.500.000; /12 = 2.375.000 (pas); 30/19,5 = 1,54 → 1,5. Cocok.

## Catatan penguji
- **Cacat R2 (sedang):** `references/jenis-perlindungan.md` tidak memuat **tanggung gugat profesi** (malpraktik). Satu-satunya pilihan rujukan adalah "tanggung gugat umum", yang pada umumnya tidak menjamin kesalahan layanan profesi. Agent di uji ini menambahkannya dari pengetahuan sendiri; model yang patuh rujukan bisa menulis "tanggung gugat umum" untuk malpraktik, dan itu salah isi. Hal yang sama berlaku untuk kendaraan titipan (07) dan kerusakan mesin/alat (dental unit, mesin espresso).
- Data pasien: skill tidak menyebut kewajiban pelindungan data pribadi (UU 27/2022 PDP) atau rekam medis; agent hanya memberi langkah murah. Wajar untuk skill awam, tapi pertanyaan pengguna "data pasien gimana?" hanya terjawab sebagian.
- Skill tidak menyatakan tidak cocok untuk usaha kesehatan; tidak ada nasihat klinis yang diberikan.

**Skor: SESUDAH 8** (angka benar, struktur rapi; dikurangi karena kualitas jawaban malpraktik bergantung pengetahuan model, bukan skill).
