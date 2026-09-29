# 07 - Normal 2: draf kampanye + uji kirim (listmonk 6.2.0 asli)
- `buat-kampanye` -> draf #2, tanpa GALAT. Email uji ke owner@example.test tiba: subjek benar, pengirim "Keripik Bu Sari", `Halo Uji,` (FirstName terisi), tautan berhenti ada, `@TrackLink` ditulis ulang jadi `/link/...`.
- `kirim` sebelum uji -> DITOLAK (6). Setelah `uji-kirim`: tanpa `--ya` ditahan; `--ya` tanpa N ditahan; N=99 dan N=0 ditolak; ringkasan menampilkan 3 penerima.
- Isi diubah lewat API setelah uji -> `kirim --ya --konfirmasi-penerima 3` ditolak ("isi berubah"): sidik isi bekerja.
- Kampanye #4 dikirim dengan konfirmasi benar: terkirim tepat 3 (yang 4 belum-konfirmasi, 2 berhenti/blocklist tidak menerima).
- Templat tanpa `{{ UnsubscribeURL }}` -> GALAT saat buat & `kirim` DITOLAK. `<script>` di isi -> ditolak (3). Subjek "PROMO GILA!!! PASTI UNTUNG" -> 3 saran spam.
