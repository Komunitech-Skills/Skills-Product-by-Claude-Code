# Riwayat perubahan — promo-kalender

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## 1.0.4 (2026-10-13) — rujukan ke skill arsip (`kalender-konten-30hari`) diganti `konten-mingguan` (`SKILL.md` termasuk deskripsi). Script hanya naik konstanta `VERSI`; logika tidak berubah.

## Catatan revisi 1.0.3 (2026-10-01)
- Temuan uji OpenClaw: target dihitung untuk promo 3 hari, tetapi linimasa & S&K memakai 1 hari; S&K memuat janji "dikirim maks 2 hari kerja" yang tidak disebut pemilik.
- Durasi promo kini ditetapkan sekali di awal dan wajib sama di target, linimasa, dan S&K (ada butir checklist). Hal operasional yang tidak diberikan pemilik (waktu kirim, kuota, retur) ditulis `[isi: …]`, bukan dikarang. Script tidak berubah.
