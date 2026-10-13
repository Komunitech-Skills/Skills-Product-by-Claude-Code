# Riwayat perubahan — agen-cs-toko

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.6 (2026-10-01)
- Dari uji OpenClaw sebelum/sesudah: draf penahan sempat berbunyi "data rekening kami simpan" dan janji jam 09.00 muncul tanpa disebut sebagai asumsi. Kini draf tidak boleh mengklaim menyimpan data pembayaran/KTP pelanggan (rekening diminta lagi lewat kanal resmi saat klaim disetujui), dan jam kerja default selalu disebut sebagai asumsi.

## Catatan revisi 1.0.7 (2026-10-02)
- Dari uji gabungan paket Toko Online: permintaan "aktifin bot WA biar balas otomatis semua chat" tidak membuka skill ini, sehingga risiko WhatsApp tidak resmi tidak dijelaskan.
- Pemicu baru untuk permintaan bot WA auto-reply, plus "Jawaban baku": kenapa tidak dipasang (WhatsApp Web tidak resmi, nomor bisa diblokir), mode Copilot (AI siapkan draf, manusia kirim), dan batas yang boleh (notifikasi ke pemilik lewat Telegram; WA hanya nomor terpisah). Promo massal/broadcast ditolak lewat alat apa pun; promo hanya ke pelanggan yang setuju, satu per satu.

## Catatan revisi 1.0.8 (2026-10-05)
- Dari pra-cek Telegram: untuk "bikinin CS toko hijab + pasang bot WA auto-balas", bot benar menolak auto-balas tetapi hanya mengajukan 5 pertanyaan tanpa hasil. Kini aturan "kerjakan dulu, tanya di akhir": penolakan singkat + alasan (WhatsApp Web tidak resmi, risiko blokir) + mode Copilot, lalu paket siap pakai ([isian] bila data kosong: template balasan stok/ongkir/retur + situasi umum, aturan nada, alur kerja admin 1 orang), baru maks. 3 pertanyaan di akhir. Contoh: `examples/06-toko-hijab-kerjakan-dulu-tanya-di-akhir.md`.

## Catatan revisi 1.0.9 (2026-10-05)
- Dari uji ulang Telegram 1.0.8 (0/3 lulus): penolakan auto-balas WA benar, tetapi template stok/ongkir/retur hanya dirangkum sebagai file `cs/PENGETAHUAN.md` & `cs/ATURAN.md` yang tidak terlihat pengguna Telegram. Kini aturan pertama: semua template (maks. ~8 pendek), aturan nada (3-5 butir), dan alur admin (3-5 langkah) wajib tampil lengkap di chat; file hanya bila diminta "simpan/pasang di OpenClaw", dibuat setelah isi tampil. Checklist baru: "Apakah semua template ada di balasan chat ini?".

## Catatan revisi 1.0.10 (2026-10-05)
- Dari uji Telegram: template "cara bayar" kini diberi catatan "khusus chat WhatsApp; di chat Shopee/marketplace jangan arahkan transaksi ke luar platform" agar toko tidak melanggar kebijakan marketplace (sumber di `references/eskalasi-dan-kanal.md`).

## Catatan revisi 1.0.11 (2026-10-05)
- Dari uji ulang Telegram 1.0.10 (rata-rata 7,75): balasan menyebut `cs/PENGETAHUAN.md` dan "belum saya buatkan file" ke pengguna, dan memakai nama bank contoh. Kini nama file/folder/path dilarang di balasan chat (aturan atas + checklist); bank ditulis `[isi: bank]`.
