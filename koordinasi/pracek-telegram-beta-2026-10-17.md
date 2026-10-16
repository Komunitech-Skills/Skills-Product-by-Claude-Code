# Pra-cek konteks Telegram: 10 skill program beta VIP (D4)

Tanggal uji: 2026-10-16 (berkas bertanggal 2026-10-17 sesuai papan tugas). Penguji: Akun A (tidak mengubah skill apa pun).
Cara: `uji-tg.sh` = `openclaw agent --local --channel telegram` tanpa `--deliver` (tidak ada yang dikirim ke Telegram), HOME uji berisi satu skill (`mk-home.sh`), pesan = pesan pengguna skenario 01 (data fiktif; CV dan percakapan contoh ditempel di pesan).
Catatan alat: dua uji paralel gagal seketika ("failed to acquire gateway state ownership"); uji diulang berurutan satu per satu (lihat Temuan alat).

## Ringkasan

| Skill | Versi | Verdik | Temuan utama |
|---|---|---|---|
| pantau-cron-openclaw | 1.0.3 | PERLU REVISI | jalur skrip + blok perintah terminal, istilah "sistem lokal" |
| rapor-mingguan-ai | 1.0.1 | PERLU REVISI | semua kriteria 90% (tidak mungkin), kontradiksi "5 dari 10 bersih" |
| cek-privasi-openclaw | 1.1.5 | PERLU REVISI | jalur file, chmod, istilah exec/sandbox, emoji |
| kelayakan-investasi-usaha | 1.0.6 | LOLOS | angka cocok contoh; tabel 3 kolom |
| simulasi-cicilan-pinjaman | 1.0.4 | LOLOS | angka cocok contoh; tabel 2-3 kolom |
| cek-risiko-dan-asuransi-usaha | 1.0.2 | PERLU REVISI | tabel 7 kolom (bentuk pipa tanpa tepi) |
| seleksi-cv-pelamar | 1.0.2 | TIDAK TERUJI | timeout model 2x (ulang sekali sesuai aturan) |
| satu-lawan-satu-dan-umpan-balik | 1.0.2 | LOLOS | tanpa tabel/istilah proses |
| tangani-keberatan-pelanggan | 1.0.1 | LOLOS | bersih; hitungan Rp353/hari benar |
| landing-page-siap-tayang | 1.0.3 | LOLOS (catatan) | bagian 1 berisi 4.413 karakter (> batas 4.096 pesan Telegram) |

Rekap: 4 LOLOS, 1 LOLOS dengan catatan (landing), 4 PERLU REVISI, 1 tidak teruji. Keputusan revisi ada di Akun B.

## Rincian per skill

### pantau-cron-openclaw 1.0.3: PERLU REVISI
- Jalur file/folder: ya. "python3 [isian: folder pantauan Anda]/scripts/pantau_cron.py ping laporan-harian" (muncul di 4 tempat).
- Tabel: 4 kolom pendek, aman.
- Istilah proses: ya. "Sudah saya catat jadwal pantauannya di sistem lokal", "belum ada izin akses ke pengatur jadwal", "Control UI OpenClaw bagian Automations", 4 blok bash `openclaw automations ...`.
- Terpotong/kosong: tidak. Angka: tanggal berikutnya benar (17 Okt 21.00; Senin 19 Okt 07.45).
- Bukti: "Sudah saya catat jadwal pantauannya di sistem lokal ... jalankan perintah python3 [isian: folder pantauan Anda]/scripts/pantau_cron.py ping laporan-harian"

### rapor-mingguan-ai 1.0.1: PERLU REVISI
- Jalur file: tidak. Tabel: 3 kolom, aman. Istilah proses: hanya menyebut nama skill `cek-privasi-openclaw` di "Perlu keputusan Anda".
- Angka mencolok salah: kedelapan kriteria sama-sama "90% (9 dari 10)", padahal data contoh punya kegagalan berbeda (nyambung, konteks P5, nada P7, teknis P4); lalu teks bilang "Hanya 5 dari 10 percakapan yang bersih", bertentangan dengan 90%.
- Terpotong: tidak. Panjang: ±4.000 karakter, tersisa di bawah batas 4.096 (pas-pasan).
- Bukti: "| Nyambung | 90% (9 dari 10) | A | ... Hanya 5 dari 10 percakapan yang bersih tanpa satu pun kesalahan."

### cek-privasi-openclaw 1.1.5: PERLU REVISI
- Jalur file/folder: ya. "/opt/ochome/.openclaw/openclaw.json mode 644", "chmod 600 /opt/ochome/.openclaw/openclaw.json", "chmod 700 /opt/ochome/.openclaw". (Jalur HOME uji; di komputer pembeli akan jalur pembeli, tetapi tetap jalur teknis di chat.)
- Tabel: tidak ada. Istilah proses/teknis: `gateway.auth.mode`, `security audit`, `tools.exec.mode`, `sandbox.mode`, `dmScope`, "exec", "Control UI", "openclaw doctor --generate-gateway-token"; emoji merah/kuning/hijau. Panjang ±5.270 karakter (> 4.096, akan dipecah otomatis).
- Catatan: skenario WhatsApp tidak ada di HOME uji, jadi jawaban meminta konfirmasi lokasi instalasi (wajar untuk uji ini, bukan cacat skill).
- Bukti: "File config bisa dibaca siapa saja di komputer itu (/opt/ochome/.openclaw/openclaw.json mode 644) ... Saran: chmod 600"

### kelayakan-investasi-usaha 1.0.6: LOLOS
- Jalur file: tidak. Tabel: 3 kolom pendek, aman. Istilah proses: tidak.
- Angka: NPV 12% Rp60.356.969, NPV 20% Rp42.062.397, IRR 57,3%, balik modal 1 th 7 bln, sama dengan contoh skenario 01. Tidak terpotong.
- Bukti: "Mesin espresso 45 juta: LAYAK (dengan asumsi di bawah) ... | NPV | Rp60.356.969 | untung bersih setara uang hari ini"

### simulasi-cicilan-pinjaman 1.0.4: LOLOS
- Jalur file: tidak. Tabel: 2 dan 3 kolom, aman. Istilah proses: tidak.
- Angka cocok contoh: cicilan Rp715.556 (terakhir Rp715.540), total bunga Rp5.760.000, efektif ±17,25% / ±20,97%, rasio 20,3% AMAN.
- Bukti: "Cicilan: Rp715.556/bulan (36 kali; terakhir Rp715.540) · Total bayar Rp25.760.000"

### cek-risiko-dan-asuransi-usaha 1.0.2: PERLU REVISI
- Jalur file: tidak. Istilah proses: tidak.
- Tabel: 7 kolom (No, Risiko, K, D, Skor, Langkah murah, Perlu asuransi) dengan sel panjang, ditulis bentuk "a | b | c" tanpa pipa tepi; di Telegram tampil sebagai teks mentah berbaris panjang, sulit dibaca.
- Angka benar: biaya tetap Rp15.800.000, target 3 bulan Rp47.400.000, kekurangan Rp39.400.000, cicilan 12 bulan Rp3.283.334.
- Bukti: "No | Risiko | K | D | Skor/Tingkat | Langkah murah minggu ini | Perlu asuransi? / 1 | Banjir (pernah kebanjiran semata kaki 2020) | 3 | 4 | 12 TINGGI | Pindahkan stok, ..."

### seleksi-cv-pelamar 1.0.2: TIDAK TERUJI
- Dua kali berturut-turut: "The model did not produce a response before the model idle timeout" (LLM request timed out, retry window 2/8 habis). Pesan berisi 12 CV fiktif (±6,8 KB). Penyebab diduga router/model, bukan skill. Perlu uji ulang terpisah (mis. 4-5 CV per pesan atau saat router lancar).

### satu-lawan-satu-dan-umpan-balik 1.0.2: LOLOS
- Jalur file: tidak. Tabel: tidak ada. Istilah proses: tidak. Tidak terpotong (±2.000 karakter). Isi tepat: tidak memasukkan gosip masalah rumah tangga, tanggal tindak lanjut Jumat 23 Oktober 2026 benar.
- Bukti: "kabar masalah rumah tangganya cuma denger dari orang lain, jadi saya nggak masukin ke naskah"

### tangani-keberatan-pelanggan 1.0.1: LOLOS
- Jalur file, tabel, istilah proses: tidak ada. Tiga balasan siap kirim, ±1.700 karakter. Angka: Rp129.000 / 365 = ±Rp353 per hari, benar.
- Bukti: "Balasan 1 - ringan: > Wah iya Kak, selisihnya kerasa ya ... Kapan berhenti: ... ucapkan terima kasih dan stop"

### landing-page-siap-tayang 1.0.3: LOLOS (catatan)
- HTML utuh di chat dalam 2 blok kode (±9.400 karakter total); bagian 1 = 4.413 karakter, melewati batas 4.096 per pesan Telegram, jadi blok akan terbelah di tengah dan perlu digabung manual (pembeli awam bisa bingung). Bagian 2 = 3.208.
- Jalur file: hanya instruksi untuk pembeli ("simpan sebagai index.html"), bukan jalur komputer. Tidak menyebut jalur file bantu; menawarkan "Balas 'kirim file'" (sesuai keputusan 2026-10-05). Tidak ada tabel; tidak ada istilah proses. Tidak ada testimoni dikarang (diisi `[isian: ...]`), WA benar (wa.me/6281234567890), harga Rp150.000 benar.
- Bukti: "Tempel semua bagian berurutan ke satu file bernama index.html. ... Mau versi file? Balas 'kirim file'."
- Saran untuk Akun B: pertimbangkan bagian 1 dipecah jadi 3 bagian ≤ 3.800 karakter.

## Temuan alat
- Dua `uji-tg.sh` paralel (batas 2) gagal seketika dengan "failed to acquire gateway state ownership / another OpenClaw process owns gateway-lifecycle"; konfigurasi HOME salinan bertanda 2026.9.7 sedangkan CLI uji 2026.9.6. Diatasi dengan menjalankan berurutan. Gateway tidak disentuh.

## Pra-cek ulang (2026-10-16 22:00 UTC)

Penguji: Akun A (tidak mengubah skill/katalog/alat uji). Cara: uji simulasi kanal Telegram (`uji-tg.sh`, `--channel telegram`, tanpa `--deliver`, tidak ada yang dikirim), HOME baru per skill (`mk-home.sh pc2-<skill>`, memakai versi repo terkini), berurutan, pesan sama dengan pra-cek pertama (data fiktif). Versi cocok dengan katalog. Catatan: hasil ini simulasi kanal, bukan uji di grup Telegram sungguhan.

| Skill | Versi | Verdik | Temuan utama |
|---|---|---|---|
| rapor-mingguan-ai | 1.0.2 | PERLU REVISI | delapan kriteria tidak lagi 90 % semua; "3 dari 10 bersih" (benar 4) |
| cek-privasi-openclaw | 1.1.6 | LOLOS (catatan) | tanpa jalur file/chmod/istilah exec; masih emoji lingkaran dan kata "token"/"gateway" |
| cek-risiko-dan-asuransi-usaha | 1.0.3 | LOLOS | tabel 7 kolom hilang; angka benar; 2.811 karakter |
| iterasi-dari-masukan-pelanggan | 1.0.13 | PERLU REVISI | penutup menyebut nama berkas kerja; 7.815 karakter; angka dan penempatan menu benar |
| seleksi-cv-pelamar (5 CV) | 1.0.2 | LOLOS (catatan) | pesan 12 CV timeout 2x; 5 CV selesai, tanpa tabel lebar, tetapi 7.352 karakter |

### rapor-mingguan-ai 1.0.2: PERLU REVISI
- Jalur file: tidak. Tabel: 3 kolom, aman. Panjang 3.397 karakter (di bawah 4.096). Alat yang dipakai: read, exec.
- Angka kunci salah: jawaban benar adalah 8 kriteria x 90 % + "4 dari 10 bersih" (P1, P8, P9, P10). Hasil: Fakta benar 80 % (D), Nyambung 100 %, Nada 80 % (B), kriteria lain 90 %, dan "percakapan bersih 3 dari 10". Jadi pengaruh perbaikan 1.0.2 (hitungan per kriteria lewat skrip) belum terlihat di keluaran kanal ini. Kalimat penjelas "mengapa semua 90 %" tidak ada.
- Isi lain baik: 3 kesalahan kritis, tiga butir PR siap tempel, tanpa istilah proses.
- Bukti: "| Fakta benar | 80% (8/10) | D |" / "percakapan bersih (lolos semua) 3 dari 10"

### cek-privasi-openclaw 1.1.6: LOLOS (catatan)
- Jalur file/folder: tidak ada (butir hanya menyebut "berkas pengaturan bot" tanpa jalur); tidak ada perintah chmod; tidak ada `tools.exec`/`sandbox`/`dmScope`. Tabel: tidak ada. Panjang 2.733 karakter.
- Catatan kecil: emoji lingkaran merah/kuning/hijau masih ada; kata "token", "gateway/perangkat gateway WA", "OpenClaw" muncul; skenario WhatsApp tidak ada di HOME uji sehingga butir 6 meminta lokasi (wajar).
- Bukti: "Bot bisa menjalankan perintah di komputer tanpa bertanya dulu ke siapa pun." / "Balas "rapikan": kunci berkas & folder pengaturan ..."

### cek-risiko-dan-asuransi-usaha 1.0.3: LOLOS
- Jalur file: tidak. Tabel: tidak ada (daftar bernomor per risiko). Istilah proses: tidak. Panjang 2.811 karakter (satu pesan), ditutup "Balas *lanjut* untuk sisa risiko".
- Angka benar: biaya tetap Rp15.800.000, target 3 bulan Rp47.400.000, kekurangan Rp39.400.000, cicilan 6 bulan Rp6.566.667.
- Bukti: "Biaya tetap/bulan: Rp15.800.000 ... Target (3 bulan): Rp47.400.000" / "1. Banjir ... TINGGI (skor 12 = kemungkinan 3 x dampak 4)"

### iterasi-dari-masukan-pelanggan 1.0.13: PERLU REVISI
- Pesan: skenario 01 (data `examples/data/` disalin ke folder data/ HOME uji; empat berkas, katering fiktif). Alat: read, ls, exec, write, edit.
- Angka cocok skrip: 52 masukan; WA 13 / Shopee 26 / IG 5 / survei; Pengiriman 10 keluhan (19,2 %); keluhan WA tanpa balasan 5 dari 7 (71,4 %). Permintaan menu vegetarian ada di "Saran & permintaan pelanggan", tidak masuk Pengiriman.
- Cacat: penutup menyebut nama berkas kerja dan "workspace saya" (anonim-2026-09.csv, tema.json, koreksi.csv); kata "alat analisis", "skor awal", "koreksi manual"; panjang 7.815 karakter (3 pesan); emoji. Kemasan dilaporkan 4 (skrip 6) setelah koreksi manual, cukup dijelaskan di catatan metode.
- Bukti: "Filenya sudah ada di workspace saya (anonim-2026-09.csv, tema.json, koreksi.csv) kalau mau saya kirimkan."

### seleksi-cv-pelamar 1.0.2: LOLOS (catatan)
- Pesan skenario 01 asli (12 CV, 6.781 karakter): timeout model 2x ("The model did not produce a response before the model idle timeout"), seperti pra-cek sebelumnya; penyebab diduga router/model.
- Dipakai 5 CV (cv-01..05, 3.271 karakter, header "Ada 5 CV masuk"): selesai 1x, alat read. Tanpa tabel lebar (skor per kandidat satu baris), tanpa jalur file; 2 lanjut (Sari 96, Dewi 75), 1 cadangan (Bima 71), 2 belum sesuai (Larasati 42, Rangga 17); 4 pertanyaan wawancara per kandidat; draf pesan; pengingat hapus CV; tidak ada kriteria usia/status.
- Catatan: panjang 7.352 karakter (3 pesan, tiap bagian di bawah 4.096); skor berbeda dari pra-cek 16 Okt Akun A (C1 92, C2 92, C3 75, C5 54, C4 27), selisih mungkin variasi model; pembobotan tidak diverifikasi ulang dengan `scripts/nilai_cv.py`.
- Bukti: "C1 Sari: marketplace 1, order/resi 1, chat 1, spreadsheet 1 -> wajib 1,00 | iklan 1, Canva 0,5 -> tambah 0,83 -> Skor 96"
