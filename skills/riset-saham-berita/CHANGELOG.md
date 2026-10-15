# Riwayat perubahan — riset-saham-berita

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.7 (2026-10-15) — koreksi tanggal POJK 5/2019
- Koreksi tanggal POJK 5/POJK.04/2019 di README (catatan kaki dasar aturan) dan `references/sumber-data.md`: sebelumnya tertulis "berlaku 2 Agustus 2019" (salah baca kolom "Tanggal Berlaku 2/8/2019" di halaman regulasi OJK yang berformat bulan/hari/tahun). Yang benar menurut salinan resmi OJK: **ditetapkan 8 Februari 2019, diundangkan 11 Februari 2019** (LN 2019 No. 27, TLN 6312), dan Pasal 7 menyatakan berlaku sejak tanggal diundangkan. Sumber: https://www.ojk.go.id/id/regulasi/Documents/Pages/Perilaku-yang-Dilarang-bagi-Penasihat-Investasi/pojk%205-2019.pdf (diakses 2026-10-15).
- Tidak ada perubahan perilaku, script, atau angka.

## Catatan revisi 1.0.6 (2026-10-15)
- Dari verifikasi rujukan aturan C32 (2026-10-15): README (FAQ & catatan kaki) dan `references/sumber-data.md` kini menyebut dasar aturan — kegiatan penasihat investasi diatur UU No. 8 Tahun 1995 Pasal 34 (larangan rekomendasi tanpa ungkap kepentingan: Pasal 35 huruf d) dan POJK 5/POJK.04/2019 (~~berlaku 2 Agustus 2019~~ — tanggal ini keliru, dikoreksi di 1.0.7); izin & pengawasan ditulis **"OJK (dulu Bapepam)"**, bukan "Bapepam" saja.
- Tidak ada perubahan perilaku, script, atau angka; penolakan rekomendasi beli/jual/target harga tetap sama.

## Catatan revisi 1.0.5 (2026-10-01)
- Jadwal cek level harga (OpenClaw) hanya dibuat setelah Anda melihat perintah + jamnya dan membalas **"ya"** — tidak ada percobaan membuat jadwal sebelum itu.
