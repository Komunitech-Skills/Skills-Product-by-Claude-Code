# 01 - Normal utama: 3 balasan WA pemasok tepung (600 kg, tenggat 5 hari)

- **Tanggal:** 2026-10-14 (putaran 2, versi 1.0.1) · **Penguji:** agent penguji independen (bukan pembuat) · OpenClaw 2026.10.2 lokal, model `claude-sonnet-5`, home bersih berisi hanya skill ini. Hasil SEBELUM/SESUDAH utuh: `00-openclaw-sebelum-sesudah.md`.

## Input (pesan pengguna)
> Tolong bandingin 3 supplier tepung ini ya. Saya punya toko bahan kue, butuh terigu protein sedang 600 kg, harus sudah sampai paling lambat 5 hari lagi soalnya stok tinggal dikit. Ini balasan WA mereka:
>
> [Toko Tepung Sentosa] Siang bu 🙏 terigu protein sedang ready. hrg 118rb/dus isi 10kg. kalo ambil diatas 50 dus kami kasih disc 5% bu. ongkir ke tempat ibu 100rb. kirim 2-3 hari stlh order. bayar cash pas barang dtg ya bu
>
> [PT Mitra Pangan Jaya] Selamat siang Ibu. Penawaran kami: Tepung terigu protein sedang Rp11.200/kg, harga belum termasuk PPN (kami PKP, faktur pajak tersedia). Minimal order 300 kg. Ongkir Rp150.000 ditagihkan di invoice. Estimasi kirim 3-4 hari. Pembayaran tempo 30 hari setelah barang diterima.
>
> [CV Berkah Gandum] bu harga 11.900/kg udh franco sampai gudang ibu ya, kami blm PKP jadi ga ada ppn. kirim 5-7 hari soalnya nunggu stok masuk. bayar transfer full dulu baru kami kirim
>
> Mana yang paling untung?

## Output SESUDAH (skill 1.0.1, uji lokal)
> **Perbandingan 3 penawaran terigu protein sedang: 600 kg, butuh dalam 5 hari**
>
> | Pemasok | Total bayar (per kg) | Selisih vs termurah | Skor (peringkat) |
> |---|---|---|---|
> | Toko Tepung Sentosa | Rp6.826.000 (Rp11.377) | termurah sementara | 86,5 (1) |
> | PT Mitra Pangan Jaya | Rp7.625.700 (Rp12.710) | lebih mahal Rp799.700 (11,7%) | 85,8 (2) |
> | CV Berkah Gandum | Rp7.140.000 (Rp11.900) | lebih mahal Rp314.000 (4,6%) | 63,0 (3, telat) |
>
> **Rekomendasi: Toko Tepung Sentosa**
> - Peringkat: 1. Toko Tepung Sentosa (skor 86,5), 2. PT Mitra Pangan Jaya (skor 85,8), 3. CV Berkah Gandum (skor 63,0, melewati tenggat).
> - Skornya hampir seri dengan PT Mitra Pangan Jaya (beda 0,7 poin).
> - Toko Tepung Sentosa adalah yang termurah (sementara: status PPN belum jelas): lebih murah Rp314.000 daripada CV Berkah Gandum untuk 600 kg, termurah berikutnya.
> - Bila jumlahnya 2x (1.200 kg): termurah tetap Toko Tepung Sentosa (Rp13.552.000); rekomendasi tetap Toko Tepung Sentosa.
> - Bila Toko Tepung Sentosa (termurah) telat 7 hari (tiba hari ke-10, melewati tenggat 5 hari): rekomendasi pindah ke PT Mitra Pangan Jaya, yang lebih mahal Rp799.700 (11,7%) daripada Toko Tepung Sentosa.
> - Bila pesanan dibagi 70/30 (Toko Tepung Sentosa 420 kg + PT Mitra Pangan Jaya 180 kg; PT Mitra Pangan Jaya wajib beli 300 kg karena minimal order): total Rp8.952.100, lebih mahal Rp2.126.100 (31,1%) daripada membeli semua dari Toko Tepung Sentosa.
> - Bila Toko Tepung Sentosa ternyata PKP dan harganya belum termasuk PPN: total naik jadi Rp7.576.860; Toko Tepung Sentosa tetap lebih murah Rp48.840 daripada PT Mitra Pangan Jaya, tapi rekomendasi berubah ke PT Mitra Pangan Jaya karena skor gabungannya lebih tinggi (unggul di termin).
> - Asumsi pajak: ongkir PT Mitra Pangan Jaya ikut kena PPN karena ditagih di fakturnya (PPN atas ongkir Rp16.500); bila ongkir itu cuma titipan biaya ekspedisi atas nama Ibu, total PT Mitra Pangan Jaya turun Rp16.500.
>
> **Rincian singkat:**
> 1. Toko Tepung Sentosa — Rp118.000/dus isi 10kg (≈Rp11.800/kg), diskon 5% dari dus ke-51 jadi efektif ≈Rp11.210/kg, ongkir Rp100.000, status PPN belum disebut, kirim 2-3 hari (masuk tenggat), bayar cash saat barang datang.
> 2. PT Mitra Pangan Jaya — Rp11.200/kg belum PPN (PKP, ada faktur pajak), min. 300 kg, ongkir Rp150.000, kirim 3-4 hari (masuk tenggat), tempo 30 hari.
> 3. CV Berkah Gandum — Rp11.900/kg franco (ongkir gratis), non-PKP, kirim 5-7 hari (melewati tenggat 5 hari ibu), bayar transfer penuh di muka.
>
> **Risiko:**
> - Toko Tepung Sentosa belum menyebut status PKP — kalau ternyata PKP dan harga belum termasuk PPN, total naik dan peringkatnya bisa tersalip PT Mitra (lihat skenario di atas).
> - CV Berkah Gandum minta bayar penuh di muka ke pemasok yang belum dicoba — risiko kas & kepercayaan lebih tinggi, plus lead time-nya sudah pasti telat dari tenggat 5 hari.
> - Harga yang ditawarkan via chat WA bisa berubah; pastikan dikunci tertulis sebelum order.
>
> **Pesan WA (siap kirim) — ke Toko Tepung Sentosa:**
> "Terima kasih atas penawarannya 🙏 Sebelum kami order 600 kg, mohon konfirmasi: 1) Tokonya PKP atau bukan? Kalau PKP, harga Rp118.000/dus itu sudah termasuk PPN atau belum, dan bisa terbit faktur pajak? 2) Harga dan diskon 5% ini berlaku sampai kapan? 3) Bisa dipastikan kirim tiba dalam 5 hari dari sekarang? Terima kasih."
>
> **Pesan WA (siap kirim) — ke PT Mitra Pangan Jaya:**
> "Terima kasih atas penawarannya. Mohon info: apakah untuk order 600 kg bisa dapat harga lebih rendah dari Rp11.200/kg, dan apakah estimasi kirim 3-4 hari bisa dipastikan tiba maksimal hari ke-5? Terima kasih."
>
> **Data yang belum ada:** [isian: status PKP & kelengkapan PPN Toko Tepung Sentosa] **Asumsi:** Ibu dianggap bukan PKP, jadi PPN dari pemasok PKP dihitung sebagai biaya; harga bertingkat/diskon dianggap berlaku untuk seluruh 600 kg.
>
> Catatan: perbandingan ini alat bantu keputusan, bukan nasihat pajak/hukum — pastikan harga, PPN, dan syarat tertulis di faktur/penawaran resmi sebelum order.
>
> Pertanyaan saya:
> 1. Mau saya langsung siapkan draf PO/chat order ke Toko Tepung Sentosa setelah dikonfirmasi PPN-nya?
> 2. Stok tinggal berapa hari lagi — kalau Sentosa ternyata telat, mau saya siapkan rencana cadangan ke PT Mitra dari sekarang?
> 3. Kualitas tepung dari ketiga pemasok ini ada yang sudah pernah dicoba sebelumnya?

## Catatan penguji (1.0.1)
- **Nilai SESUDAH 8,5** (SEBELUM 6). Konteks Telegram: SESUDAH **8,5** (SEBELUM 6,5); isi dan angkanya sama, 4.115 karakter.
- Semua angka cocok dengan hitung ulang independen (`05`, bagian A). Semua selisih ditulis bersubjek dan benar arahnya.
- **Kasus PKP Sentosa (dinilai khusus):** "Bila Sentosa PKP dan belum termasuk PPN: total Rp7.576.860; Sentosa **tetap lebih murah Rp48.840** daripada PT Mitra, tetapi rekomendasi berubah ke PT Mitra (unggul di termin)."
  - **Benar.** Bila PPN Sentosa ditambahkan, CV Berkah (telat) menjadi termurah keseluruhan. Skor dihitung ulang penguji: Mitra 87,45 vs Sentosa 84,19. Sentosa unggul di biaya dan lead time, Mitra hanya di termin (tempo 30 hari vs COD, skor 100 vs 50).
  - **Masuk akal secara ekonomi:** menahan ±Rp7,6 juta selama 30 hari bernilai lebih dari Rp48.840 (±0,6%).
  - **Penjelasan agent jelas** (lokal dan Telegram), dan konsisten dengan bagian risiko ("peringkatnya bisa tersalip PT Mitra"; "selisihnya jadi sangat tipis").
- Asumsi pajak terbuka: PPN atas ongkir Mitra Rp16.500, beserta total alternatifnya bila ongkir hanya titipan.
- Catatan jujur: "Contoh ringkas" di SKILL.md 1.0.1 memakai data dan jawaban skenario ini, jadi hasil bagus di sini sebagian bisa karena contoh. Data baru diuji di `06` (hasilnya juga benar).
- Kekurangan kecil: 4.279 karakter (sedikit di atas ±4.000); 3 pertanyaan penutup lemah.

## Riwayat
- 1.0.0: SESUDAH 7,5 (lokal) / 6 (Telegram). Selisih Rp314.000 disematkan ke Mitra; di Telegram agent menyimpulkan "bila Sentosa PKP, Mitra lebih murah" (salah); agent membaca kode script ±700 baris (155-164 detik). Kini 70 detik, tanpa membaca kode.
