# Riwayat perubahan — pengingat-pasien-klinik

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.10 (2026-10-17)
- SKILL.md: contoh baris konfirmasi "Tersimpan" disamakan dengan keluaran script (tanggal ditulis `6 Okt 2026`, bukan `Selasa, 6 Oktober 2026`); nama hari lengkap hanya muncul di judul `ringkasan`. Script dan cara kerja tidak berubah.

## Catatan revisi 1.0.9 (2026-10-13)
- `references/openclaw-jadwal.md`: rujukan ke panduan jadwal paket klinik diberi keterangan "hanya di paket VIP" agar pembeli ecer tidak mencari berkas yang tidak ada. Script dan cara kerja tidak berubah.

## Catatan revisi 1.0.8 (2026-10-02)
- Temuan uji ulang paket klinik (1B): agent salah menyebut skill untuk laporan mingguan klinik. Kini rujukan dipertegas: laporan mingguan 3P → `laporan-status-kantor`; rekap dari file CSV kunjungan → `edukasi-pasien-klinik`; skill ini hanya ringkasan pengingat harian. Script tidak berubah.

## Catatan revisi 1.0.7 (2026-10-02)
- Temuan uji gabungan paket klinik: keterangan "diabetes" dibuang diam-diam; agent menawarkan nama + "kontrol gula darah" untuk teks grup staf; daftar pasien yang setuju pengingat ditawarkan untuk promo.
- Kini: wajib memberi tahu bila keterangan medis tidak disimpan; teks grup staf = nama panggilan/inisial tanpa nomor WA & keterangan medis (jenis bernada penyakit ditulis "kontrol"); izin pengingat ≠ izin promo. Script tidak berubah.

## Catatan revisi 1.0.6 (2026-10-01)
- Temuan uji OpenClaw (klinik 03): contoh di SKILL.md (`<perintah> [opsi] --json`) gagal kode 2 karena script hanya menerima `--json` sebelum nama perintah; agent juga sempat mencari script ke seluruh disk.
- Script kini menerima `--json`, `--file`, `--hari-ini`, `--tz` di kedua posisi; contoh SKILL.md & `references/perintah.md` diperbaiki dan diuji; lokasi script ditulis eksplisit (jangan `find /`). Uji regresi 38/38 (4 baru).
