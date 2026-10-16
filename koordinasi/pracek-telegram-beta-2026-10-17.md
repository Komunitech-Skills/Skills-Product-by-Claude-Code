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
