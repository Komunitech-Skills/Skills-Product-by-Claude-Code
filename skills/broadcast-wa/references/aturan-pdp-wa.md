# Aturan Broadcast WA: UU PDP & Kebijakan WhatsApp

Dicatat 2026-09-23. Ringkasan praktis, **bukan nasihat hukum**. Untuk kasus khusus (data sensitif,
kebocoran data, database besar) konsultasikan dengan konsultan hukum.

## 1. UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP)
Berlaku penuh sejak Oktober 2024. Nomor HP dan nama pelanggan termasuk data pribadi. Poin yang relevan
untuk broadcast promosi:
- **Perlu dasar pemrosesan yang sah**, untuk promosi praktisnya **persetujuan** pelanggan.
- **Beri tahu tujuannya** saat meminta nomor ("untuk info promo & pesanan via WhatsApp").
- **Minimalkan data**: simpan hanya yang perlu (nama, nomor, persetujuan, tanggal setuju).
- **Hak pelanggan**: melihat, memperbaiki, menghapus data, dan **menarik persetujuan** kapan saja.
  → Setiap broadcast wajib punya cara berhenti yang mudah (balas STOP/BERHENTI), dan permintaan itu dipatuhi.
- **Kebocoran data** wajib diberitahukan (paling lambat 3 × 24 jam kepada pihak terkait).
- Peraturan pelaksana (PP) masih perlu dicek statusnya — **BELUM TERVERIFIKASI** di skill ini.

Sumber: https://www.hukumonline.com/klinik/a/uu-pdp--landasan-hukum-pelindungan-data-pribadi-lt5d588c1cc649e/
(teks resmi: cari "UU 27 Tahun 2022" di https://peraturan.bpk.go.id)

### Cara praktis mengumpulkan persetujuan
- Di kasir/form order: kotak centang "Saya bersedia menerima info promo via WhatsApp".
- Via chat: "Boleh kami kirimi info promo lewat WA sesekali, Kak? Bisa berhenti kapan saja." → catat "ya" + tanggal.
- **Jangan** membeli/menyewa database nomor, mengambil nomor dari grup WA, atau memakai nomor
  pelanggan yang hanya pernah bertanya harga tanpa setuju dikirimi promo.
- Simpan kolom di spreadsheet: `Nama | Nomor | Persetujuan (ya/tidak) | Tanggal setuju | Berhenti`.
  Kolom Berhenti: kosong (atau "tidak"/"0"/"-") = masih aktif; isi apa pun lainnya ("ya", "STOP", "x",
  tanggal berhenti) = **berhenti**. Script menganggap nomor itu berhenti di semua baris, termasuk baris duplikat.

## 2. Kebijakan & fitur WhatsApp (cek ketentuan terbaru — fitur sering berubah)
- **Daftar siaran (broadcast list) di WhatsApp/WhatsApp Business**: pesan hanya sampai ke kontak yang
  **menyimpan nomor kamu**. Jumlah kontak per daftar dibatasi (lama dikenal 256 — cek batas terbaru).
  Pesan terkirim sebagai chat pribadi, penerima tidak saling melihat.
- **Aplikasi "blast"/WA mod tidak resmi** melanggar Ketentuan Layanan WhatsApp dan berisiko nomor diblokir
  permanen. Skill tidak membantu setup alat seperti itu.
- **Volume besar & resmi**: WhatsApp Business Platform (API) lewat penyedia resmi, memakai template pesan
  yang disetujui dan wajib opt-in; ada biaya per percakapan/pesan (cek harga terbaru di penyedia).
- Nomor terkena pembatasan umumnya karena **banyak penerima memblokir/melaporkan**. Cara paling efektif
  mencegahnya: kirim hanya ke yang setuju, pesan relevan & singkat, frekuensi wajar, opt-out jelas.

## 3. Soal "variasi supaya tidak dianggap spam"
Variasi pesan + nama personal membuat pesan terasa seperti chat biasa dan **mengurangi laporan spam dari
penerima**. Variasi **bukan** cara mengakali sistem untuk mengirim ke orang yang tidak setuju — skill
menolak permintaan seperti itu.

## 4. Frekuensi & jam kirim (saran umum, bukan aturan resmi)
- Promo: maksimal ±1–2 kali per minggu per kontak. Info pesanan/transaksi tidak dihitung.
- Jam kirim: ±09.00–11.00, ±15.30–17.00, ±19.00–20.30 waktu setempat. Hindari larut malam, dini hari,
  dan jam salat Jumat (±11.30–13.00 Jumat) untuk audiens muslim. Saat Ramadan: setelah berbuka
  (±19.00–21.00) atau selepas sahur/pagi.
- Script otomatis melewati Jumat 11.30–13.00 (digeser ke 13.00).
- Kirim bertahap (default script: 20 pesan per batch, jeda 60 detik antarpesan, 30 menit antarbatch,
  maks. 100 per hari). Angka ini saran konservatif, bukan batas resmi WhatsApp.
- Perhatikan zona waktu: WIB, WITA (+1 jam), WIT (+2 jam).

## 5. Teks opt-out siap pakai (wajib ada di setiap pesan)
- "Tidak ingin menerima info promo lagi? Balas STOP."
- "Balas BERHENTI kalau tidak mau dapat info lagi ya, Kak."
- "Kamu menerima pesan ini karena bersedia dikirimi info dari <nama toko>. Balas STOP untuk berhenti."

Setelah ada yang membalas STOP: masukkan nomornya ke daftar berhenti (kolom Berhenti = ya) sebelum
broadcast berikutnya, dan balas singkat: "Baik Kak, nomor Kakak sudah kami hapus dari daftar info promo. Terima kasih."
