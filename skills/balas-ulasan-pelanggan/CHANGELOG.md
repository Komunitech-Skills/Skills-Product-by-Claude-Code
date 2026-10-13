# Riwayat perubahan — balas-ulasan-pelanggan

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.5 (2026-10-01)
- Temuan uji ulang OpenClaw: balasan menulis "sudah kami bahas bersama tim" tanpa konfirmasi pemilik.
- Kini klaim tindakan jadi isian/pilihan untuk dikonfirmasi pemilik; default versi netral.

## Catatan revisi 1.0.4 (2026-10-01)
- Temuan uji ulang OpenClaw (faskes): frasa "saat berkunjung ke klinik kami" masih mengonfirmasi kunjungan.
- Mode `--faskes` kini menandai GAGAL "saat berkunjung/datang/berobat" (tanpa subjek) + 1 uji regresi baru; aturan di SKILL.md diperbarui.

## Catatan revisi 1.0.3 (2026-10-01)
- Temuan uji OpenClaw (klinik): balasan publik Google Maps menyebut "saat periksa gigi putra/putri Bapak" — mengonfirmasi perawatan pasien di ruang publik.
- Aturan baru khusus klinik/faskes: balasan publik tidak menyebut status pasien, kunjungan, tindakan, atau kondisi kesehatan, dan mengalihkan ke kanal pribadi (rahasia kesehatan UU 17/2023 Ps. 301; data kesehatan = data pribadi spesifik UU 27/2022 Ps. 4 ayat (2) huruf a). `cek_balasan.py --faskes` menandai GAGAL frasa semacam itu. Ditambah 3 uji regresi. **PERLU REVIEW** tenaga medis/kepatuhan.
