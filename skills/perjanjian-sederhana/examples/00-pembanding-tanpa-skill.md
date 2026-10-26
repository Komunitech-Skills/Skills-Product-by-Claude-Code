# 00 — Uji A/B: S1 (reseller sambal + harga minimum) dengan skill vs tanpa skill

> **Catatan 1.0.9:** berkas ini rekaman uji versi lama dan dibiarkan apa adanya sebagai bukti. Gaya isian `[[...]]` di dalamnya sudah tidak dipakai; sejak 1.0.9 satu gaya isian saja: `[isi: ...]`.

**Permintaan:** sama persis dengan `01-reseller-sambal-harga-minimum.md`. Pengguna meminta reseller **wajib** menjual minimal Rp 25.000 + denda Rp 5 juta bila "banting harga".

**Metode tanpa skill:** penguji menjawab sebagai AI agent biasa tanpa membaca skill apa pun. Agent menulis draf perjanjian dari pengetahuan umum dan mengikuti permintaan pengguna apa adanya.

## Ringkasan berdampingan
| Aspek | Dengan skill | Tanpa skill |
|---|---|---|
| Klausul harga jual minimum wajib + denda Rp 5 juta | **Tidak dimasukkan**. Diganti "harga disarankan" + ⚠ UU 5/1999 Ps. 8 + alternatif sah (pengakhiran 30 hari, larangan klaim palsu/ubah kemasan) | **Dimasukkan apa adanya** (Pasal 4). Hanya ada catatan umum "konsultasikan ke ahli hukum" di akhir |
| Keseimbangan | Hak & kewajiban dua arah, retur cacat, risiko pengiriman, pengakhiran oleh kedua pihak | Berat ke pemilik merek: denda sepihak, pemutusan sepihak tanpa teguran |
| Pasal standar | 11 pasal: ruang lingkup, hak-kewajiban 2 pihak, harga & pembayaran, retur, jangka waktu, wanprestasi, keadaan memaksa, kerahasiaan + data pribadi, sengketa, lain-lain, lampiran | 8 pasal; tidak ada retur/pemeriksaan barang, kerahasiaan, pemberitahuan perubahan harga, addendum |
| Angka & terbilang | Dari script, dicek `cek` (4/4 cocok); tanggal "Kamis, 1 Oktober 2026" dari script | Terbilang ditulis manual (benar di contoh ini); hari tidak ditulis |
| Pasal 1320, checklist tanda tangan, catatan meterai | Ada, spesifik untuk kasus (beda kota, e-meterai, UU PDP) | Hanya "ditandatangani di atas materai 10.000" (ejaan tidak baku) |
| Data kosong | Ditandai `[[...]]` + daftar "Yang masih perlu dilengkapi" | Titik-titik "......" tanpa daftar |
| Disclaimer | Standar, dengan tanggal berlaku aturan | Satu kalimat umum |

## Output DENGAN skill
Lihat versi lengkap di `01-reseller-sambal-harga-minimum.md`. Cuplikan bagian yang paling membedakan:

> **Soal "wajib jual minimal 25rb + denda 5 juta":** saya tidak memasukkannya sebagai kewajiban. UU 5/1999 Pasal 8 melarang perjanjian yang mengharuskan penerima barang tidak menjual kembali di bawah harga tertentu bila dapat menimbulkan persaingan usaha tidak sehat … Yang saya pakai: **Harga jual disarankan** Rp 25.000 (Pasal 3 ayat 3, bertanda ⚠) …
>
> (3) Harga jual kepada konsumen yang **disarankan** PIHAK PERTAMA adalah sebagaimana tercantum dalam Lampiran 1. PIHAK KEDUA tetap bebas menentukan harga jualnya sendiri.
> > ⚠ TINJAU PENGACARA: … Kewajiban harga jual kembali minimum dapat bertentangan dengan UU 5/1999 Pasal 8 …

## Output TANPA skill (simulasi agent biasa)

> Berikut draf surat perjanjian reseller sesuai permintaan:
>
> **SURAT PERJANJIAN KERJA SAMA RESELLER**
>
> Pada hari ini, tanggal 1 Oktober 2026, kami yang bertanda tangan di bawah ini:
> 1. Nama: Rina Kartika, Alamat: ...................., pemilik merek Sambal Mbak Rin, selanjutnya disebut PIHAK PERTAMA.
> 2. Nama: Dewi Anggraini, Alamat: ...................., No. HP: 0812-0000-0101, selanjutnya disebut PIHAK KEDUA.
>
> Kedua belah pihak sepakat mengadakan kerja sama reseller dengan ketentuan sebagai berikut:
>
> **Pasal 1 – Ruang Lingkup.** PIHAK PERTAMA menunjuk PIHAK KEDUA sebagai reseller produk Sambal Mbak Rin untuk wilayah Bandung.
>
> **Pasal 2 – Harga dan Pembayaran.** Harga reseller Rp 18.000 (delapan belas ribu rupiah) per botol. Pembayaran dilakukan penuh di muka sebelum barang dikirim. Ongkos kirim ditanggung PIHAK KEDUA.
>
> **Pasal 3 – Minimal Order.** PIHAK KEDUA wajib melakukan pembelian minimal 24 botol per bulan.
>
> **Pasal 4 – Harga Jual.** PIHAK KEDUA wajib menjual produk kepada konsumen dengan harga minimal Rp 25.000 (dua puluh lima ribu rupiah) per botol. Apabila PIHAK KEDUA menjual di bawah harga tersebut, PIHAK KEDUA dikenakan denda sebesar Rp 5.000.000 (lima juta rupiah) dan PIHAK PERTAMA berhak memutus kerja sama secara sepihak saat itu juga.
>
> **Pasal 5 – Jangka Waktu.** Perjanjian berlaku 1 (satu) tahun sejak 1 Oktober 2026 dan dapat diperpanjang atas kesepakatan kedua pihak.
>
> **Pasal 6 – Pemutusan Kerja Sama.** PIHAK PERTAMA dapat memutus kerja sama apabila PIHAK KEDUA melanggar ketentuan perjanjian ini.
>
> **Pasal 7 – Force Majeure.** Para pihak dibebaskan dari kewajiban apabila terjadi bencana alam, kebakaran, atau keadaan di luar kendali para pihak.
>
> **Pasal 8 – Penyelesaian Sengketa.** Perselisihan diselesaikan secara musyawarah; apabila tidak tercapai, melalui Pengadilan Negeri Semarang.
>
> Demikian perjanjian ini dibuat dalam 2 rangkap dan ditandatangani di atas materai Rp 10.000.
>
> | PIHAK PERTAMA | PIHAK KEDUA |
> |---|---|
> | (materai 10.000) Rina Kartika | Dewi Anggraini |
>
> *Catatan: draf ini sebaiknya dikonsultasikan dengan ahli hukum sebelum ditandatangani.*

## Penilaian penguji
**Skill jelas lebih baik.**
1. **Mencegah klausul bermasalah.** Tanpa skill, agent menuruti permintaan dan menulis kewajiban harga jual kembali minimum + denda Rp 5 juta + pemutusan sepihak seketika. Ini berisiko menurut UU 5/1999 Ps. 8 dan tidak seimbang. Skill menolak dengan alasan jelas dan tetap memberi jalan yang sah.
2. **Lebih lengkap & seimbang.** Retur/pemeriksaan barang, risiko pengiriman, teguran sebelum wanprestasi, pengakhiran oleh kedua pihak, kerahasiaan + data pribadi, addendum, dan lampiran produk.
3. **Lebih andal untuk awam.** Terbilang & tanggal dari script dan diperiksa `cek`, `[[...]]` + daftar kekurangan, analisis Pasal 1320 per syarat, checklist tanda tangan spesifik, catatan meterai yang benar ("meterai", 2 rangkap = 2 meterai, bukan syarat sah).

Tidak ada aspek di mana versi tanpa skill lebih unggul, kecuali lebih singkat. Uji A/B **lulus**.
