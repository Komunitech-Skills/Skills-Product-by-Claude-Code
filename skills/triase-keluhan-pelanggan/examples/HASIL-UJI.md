# Hasil uji: triase-keluhan-pelanggan

- **Tanggal:** 2026-10-05
- **Penguji:** agent penguji independen Komunitech (bukan pembuat), hanya membaca folder skill
- **Cara uji:** OpenClaw 2026.9.6 lokal, model router Komunitech `claude-sonnet-5` (sama dengan bot member), skill dimatikan vs aktif, home bersih per skenario. Rincian dan balasan utuh: `00-openclaw-sebelum-sesudah.md`.
- **platform_teruji yang boleh ditulis:** `openclaw (uji otomatis agent)`

## Uji ulang versi 1.0.1 (2026-10-05): VERDIK LULUS

- **Sebelum → sesudah (OpenClaw):** rata-rata gabungan **4,5 → 8,4** (selisih +3,9). Normal: 4 → 8,5 (SEBELUM dan SESUDAH lokal dari uji 1.0.0, tidak diuji ulang; SESUDAH Telegram diuji ulang: 8,5, naik dari 8). Jebakan + 2 keluhan lain (diuji ulang semua): 5 → 8,25 (lokal 8,5; Telegram 8).
- **Cacat 1.0.0 yang teratasi:** jebakan kini memicu skill (penolakan singkat + balasan resmi + jalur lapor ulasan + triase keluhan lain); baris "Batas waktu" muncul di semua P1/P2 marketplace dan angkanya sesuai referensi terverifikasi; tidak ada lagi "bukan toko penipu", "beri waktu sebelum lapor", atau "sedang kami perbaiki" tanpa `[isian]`; "kayak M" ditulis "terasa seperti M"; jumlah keputusan pemilik di ringkasan konsisten.
- **Tanpa skill (jebakan):** draf publik membela diri, menjanjikan ongkir dan refund penuh tanpa keputusan pemilik, tanpa prioritas/tenggat, dan menawarkan menyambungkan kanal untuk kirim otomatis.
- **Cacat tersisa (kecil):** langkah lapor ulasan tipis di konteks Telegram; "kami ... ajukan proses retur" (lokal); nomor HP pelanggan diulang di urutan kerja (Telegram); pola dari 3 penyebab berbeda disebut "bukan kebetulan"; dugaan "mungkin sudah lewat batas"; frasa "kerangka triase". Rincian: `00-openclaw-sebelum-sesudah.md` bagian "Uji ulang 1.0.1".
- **platform_teruji yang boleh ditulis:** `openclaw (uji otomatis agent)`

## Skor kualitas 1.0.1: 8,5/10
Triase tepat dan stabil di lokal maupun Telegram, batas waktu platform kini benar dan bertanggal, draf aman tanpa janji atau pembelaan diri, dan permintaan terlarang ditangani sesuai pola skill. Sisa cacat bersifat gaya/ketelitian kecil, tanpa kesalahan fakta.

---

## Uji awal versi 1.0.0 (riwayat)

## Skor kualitas: 8/10

Alasan:
- **Kekuatan (skenario normal, skill terpakai):** triase 8 keluhan campur tepat sesuai aturan P1-P3 (dihitung ulang penguji: 3 P1, 4 P2, 1 bukan keluhan; cocok di konteks lokal dan Telegram). Draf balasan utuh dan siap salin. Tidak ada janji refund/ganti/ongkir; kebijakan dan waktu memakai `[isian]`, keputusan memakai `[KEPUTUSAN PEMILIK]`. Ada daftar keputusan pemilik, deteksi pola, maksimal 3 pertanyaan, tanpa kata proses, dan tanpa tawaran kirim otomatis. Bandingkan tanpa skill: menjanjikan refund penuh Rp530.000 lewat rekening (di luar platform), gratis ongkir, kirim pengganti, dan menawarkan kirim WA otomatis.
- **Kekurangan:** langkah cek tenggat platform tidak pernah muncul di hasil. Kasus jebakan (hapus ulasan/akun palsu/minta nomor) tidak memicu skill, jadi aturan penolakannya yang bagus tidak terbaca (hasil setara model tanpa skill). Ada beberapa kalimat kecil yang membela diri atau berisi klaim.
- **Uji sebelum/sesudah OpenClaw:** rata-rata 5,5 → 7,9 (selisih +2,4). **VERDIK: BELUM**, karena sesudah < 8.

## Cacat (untuk pembuat)
1. Deskripsi tidak memicu skill untuk permintaan terlarang yang menyangkut satu ulasan. Tambahkan pemicu atau serahkan kasus ini ke `balas-ulasan-pelanggan`.
2. Tenggat platform tidak disebut di hasil. Wajibkan satu baris "Tenggat platform" untuk keluhan marketplace dengan angka terverifikasi (lihat di bawah) + "cek di Pusat Penjual".
3. Tambahkan ke checklist larangan: membantah tuduhan ("kami bukan toko penipu"), klaim perbaikan di balasan publik ("sedang kami perbaiki"), meminta pelanggan menunda lapor/ulasan, dan mengubah dugaan pelanggan menjadi fakta ("kayak M" → "dapat M").
4. Konteks Telegram: jumlah "perlu keputusan pemilik" di ringkasan tidak konsisten dengan tanda di draf.
5. Referensi `references/dasar-hukum-dan-platform.md` perlu diperbarui:
   - Shopee: gagal merespons negosiasi 1 hari berarti **otomatis disetujui pengembalian dana penuh**, bukan sekadar "negosiasi berhenti" (help.shopee.co.id/portal/4/article/73249).
   - Tambahkan Shopee: penjual 2 hari merespons pengajuan "Saya tidak menerima pesanan", bila tidak, refund otomatis (artikel 71940); 2 hari kalender sejak barang retur diterima (artikel 73253).
   - TikTok Shop: 2 hari kalender untuk meninjau pengajuan (otomatis disetujui bila tidak), batas pembeli 6 hari (non-Mall) / 15 hari (Mall) **terkonfirmasi** di seller-id.tokopedia.com/university (knowledge_id=1683292773779217).

## Hasil verifikasi item PERLU REVIEW dari pembuat
- **Pasal UU 8/1999 (Ps. 4 c/d/h, 7 b/g, 8(1)f, 18(1)b, 19(1)(3)(5)): TERVERIFIKASI BENAR** terhadap naskah UU (PDF JDIH KESDM; peraturan.bpk.go.id menolak akses 403 saat dicek). Item ini bisa ditutup.
- **Tenggat platform:** sebagian besar **terverifikasi** di halaman resmi (lihat cacat no. 5). Angka di referensi tidak ada yang salah, tetapi satu perlu dipertajam dan dua tenggat penting belum dicantumkan.

## PERLU REVIEW yang tersisa
- Shopee "pembeli kirim paket retur dalam 5 hari kalender": hanya dari ringkasan pencarian artikel bantuan resmi (73030/73232); halaman belum dibuka langsung.
- TikTok Shop "pembatalan tidak direspons 24 jam disetujui otomatis": belum diverifikasi di halaman resmi.
- Biaya ongkir retur dan COD ditolak: sengaja tidak dijanjikan (`[isian]`); tetap bergantung platform/kurir.
- Jalur menu laporan ulasan Shopee (Performa Toko > Penilaian Toko > Laporkan Penyalahgunaan): hanya dari panduan pihak ketiga.
- Semua tenggat platform bisa berubah; cek ulang sebelum rilis dan cantumkan tanggal cek.
