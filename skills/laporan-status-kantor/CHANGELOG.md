# Riwayat perubahan — laporan-status-kantor

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.3 (2026-10-01)
- Dari uji OpenClaw sebelum/sesudah: AI sempat memasukkan gaji dan THR per orang ke teks pengumuman grup dan menghitung THR sendiri. Kini pengumuman grup tidak pernah memuat nominal per orang (hanya tanggal bayar & dasar aturan); rincian per orang hanya lewat pesan pribadi/HR. Perhitungan THR diarahkan ke skill `hitung-thr` bila terpasang; bila tidak, AI menjelaskan nominal perlu dihitung terpisah.

## Catatan revisi 1.0.4 (2026-10-02)
- Aturan privasi pengumuman grup kini ditaruh paling atas dan **tetap berlaku walau skill lain ikut dipakai** (mis. `hitung-thr`, `gaji-umkm`): gaji/THR per orang tidak pernah masuk teks grup; rincian per orang dipisah di blok khusus pemilik/HR. (Temuan uji 2026-10-02: saat dipasang bersama `hitung-thr`, nominal per orang sempat masuk teks grup.)
- AI tidak menawarkan menyambungkan WhatsApp atau kirim otomatis ke grup — hasilnya draf yang kamu tempel sendiri.
- Tanggal libur/cuti bersama yang tidak kamu sebut: maksimal satu pencarian, selebihnya ditandai `[isi: ...]` agar balasan tidak macet.

## Catatan revisi 1.0.6 (2026-10-05)
- Temuan uji Telegram: bot hanya bertanya 5 hal tanpa memberi teks pengumuman. Kini aturannya "kerjakan dulu, tanya di akhir": teks pengumuman libur & cuti bersama (tanggal dari rujukan, THR per orang tidak dicantumkan, batas bayar H-7) langsung diberikan, `[isian]` untuk yang belum diketahui, maks. 3 pertanyaan di akhir.

## Catatan revisi 1.0.7 (2026-10-05)
- Dari uji ulang Telegram 1.0.6 (rata-rata 7,43): ucapan "Tahun Baru 2026" salah (seharusnya 2027) dan kata "Skill ini" bocor ke chat. Kini tahun ucapan wajib sama dengan tahun tanggal liburnya, dan balasan dilarang memuat kata "skill", "script", "file", "cek" (butir checklist baru).
