# Skenario 2: Normal kedua: warung bakso + es campur (daging giling seharian, es pinggir jalan)

- Tanggal: 2026-10-12 | skill v1.0.2 | OpenClaw, model claude-sonnet-5
- Nilai: SEBELUM 5.0 -> SESUDAH 8.0

## Input

Warung bakso + es campur, 2 gerobak, stok daging giling dibeli pagi dipakai sampai malam, es batu beli di pinggir jalan: apa yang harus saya ubah dulu?

## Output SESUDAH (dengan skill)

> Dari gambaran usaha Anda, ada **2 titik paling rawan** yang perlu diubah lebih dulu dibanding yang lain — baru setelah itu checklist harian umum.
>
> ## Prioritas #1 — Es batu dari pinggir jalan
> Ganti sumbernya dulu, karena ini paling cepat diperbaiki dan risikonya langsung masuk ke tubuh pelanggan tanpa proses masak apa pun.
>
> - **Masalah:** Banyak es balok/es curah yang dijual di pinggir jalan sebenarnya "es industri" — dibuat untuk mengawetkan ikan, bukan untuk dikonsumsi. Airnya tidak diproses sesuai standar air minum, dan cara potong/angkutnya di jalan sering kena tangan, karung, aspal. Es ini masuk langsung ke es campur tanpa dimasak — kalau airnya tercemar bakteri (E. coli dll.), tidak ada proses yang membunuhnya.
> - **Ubah:** Cari pemasok es kristal/es tube/es kemasan yang jelas berlabel "food grade" atau "layak konsumsi" — biasanya lebih bening, dikemas, bukan balok kotor yang diseret di jalan. Tanya sumber airnya (air matang/RO, bukan air sumur mentah).
>
> ## Prioritas #2 — Daging giling dipakai dari pagi sampai malam
> Ini bahan paling rawan di menu bakso karena bakterinya tercampur merata ke seluruh daging (bukan cuma di permukaan seperti daging utuh).
>
> - **Masalah:** Zona bahaya bakteri berkembang biak ada di **5–60°C**. Daging matang/mentah aman di suhu ruang **maksimal 2 jam** (jadi **1 jam saja** kalau gerobak kena terik siang >32°C). Kalau dibiarkan di wadah terbuka gerobak dari pagi sampai malam (10+ jam), bakteri sudah berkembang biak jauh sebelum direbus — dan sebagian racun bakteri (mis. Bacillus cereus) tidak hilang walau direbus ulang.
> - **Ubah:** Jangan taruh semua stok daging giling di gerobak seharian. Simpan sebagian besar di cooler box berisi es batu/ice gel, ambil secukupnya untuk 1–2 jam jualan, isi ulang tiap kali habis. Bakso (jadi atau baru dibentuk) tetap wajib matang inti **≥71°C**; kalau beli bakso matang dari pemasok, tetap rebus ulang di kuah mendidih sebelum disajikan — jangan cuma dicelup sebentar.
>
> **Kalau harus pilih satu minggu ini dulu:** ganti sumber es lebih dulu (tidak perlu beli alat, tinggal ganti pemasok), sambil cari cool box kecil untuk daging giling — bisa jalan paralel.
>
> Dua hal ini baru titik paling kritis, bukan paket lengkap. Kalau mau, saya bisa susun **paket keamanan pangan lengkap** untuk warung bakso + es campur Anda: checklist harian buka-tutup, log suhu, kartu aturan staf, peta risiko bahan (daging giling, es, kuah, topping), dan ringkasan izin (termasuk sertifikasi halal — **wajib**, UMK mulai 18 Okt 2026, tinggal beberapa hari lagi).
>
> Supaya pas, boleh dijawab (maksimal 3, boleh skip):
> 1. Ada termometer makanan (tusuk) untuk cek suhu bakso/kuah? Kalau belum, saya sarankan beli yang murah dulu.
> 2. Jam buka gerobak dari jam berapa sampai jam berapa?
> 3. Bakso dibuat sendiri di rumah lalu dibawa, atau beli jadi dari pemasok?
>
> *Catatan: ini panduan kebiasaan kerja aman, bukan pengganti pemeriksaan resmi Dinkes/BPOM setempat.*

## Catatan

SEBELUM 5,0: urutan prioritas masuk akal (daging giling dulu, es kedua), tetapi menyarankan batas "±4-6 jam di suhu ruang panas" = KESALAHAN FAKTA KESELAMATAN (standar 2 jam, 1 jam bila >32 °C), tidak menyebut suhu apa pun (5/60/71 °C), tanpa halal/izin. SESUDAH 8,0: fakta benar (zona 5-60 °C, 2 jam/1 jam >32 °C, bakso ≥71 °C, rebus ulang), es batu: pemasok food grade/air matang-RO, jawaban fokus pada "apa yang diubah dulu" lalu menawarkan paket. Kekurangan: memilih es dulu padahal daging giling seharian paling berisiko (debatable), tidak menyebut target ≤5 °C untuk cooler box maupun buang stok yang sudah lewat, halal hanya di tawaran.

Perbandingan lengkap dengan hasil SEBELUM: `00-openclaw-sebelum-sesudah.md`.
