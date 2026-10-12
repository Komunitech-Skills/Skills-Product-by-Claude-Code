# Contoh 3: Input tidak lengkap: kinerja karyawan turun

> Hasil uji OpenClaw asli versi 1.0.2 (2026-10-12, model claude-sonnet-5, uji otomatis agent). Perbandingan lengkap sebelum/sesudah: `00-openclaw-sebelum-sesudah.md`.

## Masukan pengguna
"Karyawan saya kinerjanya turun, tolong bantu cara ngomongnya."

## Keluaran di chat (dengan skill)

> Karyawan kinerja turun - ini langkah ngomongnya:
>
> **1. Pesan WA ajakan ngobrol (kirim dulu, bukan nawarin di WA)**
> "[Nama], besok setelah [isian: jam kerja selesai/istirahat] bisa ngobrol 10 menit? Mau bahas kerjaan kamu belakangan ini."
>
> **2. Naskah empat mata (konteks - fakta - dampak - tanya - sepakat)**
> "[Nama], saya mau ngobrol soal kerjaan beberapa minggu terakhir.
>
> Saya lihat [isian: kejadian konkret yang terlihat, misal: 3 pesanan salah kirim minggu ini / laporan kas telat 2 hari / target harian meleset terus sejak awal bulan]. Akibatnya [isian: dampaknya ke siapa/apa, misal: pelanggan komplain / rekan lain jadi nambah kerjaan / toko rugi waktu].
>
> Dari sisi kamu sendiri, ada kendala apa? Apa ada yang bikin susah belakangan ini?
>
> [dengarkan jawabannya]
>
> Oke, kita sepakat begini: mulai [isian: tanggal mulai], kamu [isian: langkah konkret, misal: cek ulang pesanan sebelum kirim / setor laporan paling lambat jam 5 sore]. [Jumat depan/isian: tanggal] kita cek lagi sama-sama, ya."
>
> **3. Tindak lanjut**
> - Tanggal mulai perbaikan: [isian]
> - Tanggal cek ulang: [isian] (kalau jatuh Minggu/libur, geser ke hari kerja berikutnya)
> - Catat hasil obrolan singkat: kesepakatan apa, siapa, kapan — biar ada jejak kalau perlu dibahas lagi
>
> **Catatan:** jangan dibungkus pujian basa-basi di awal ("kamu kerja bagus kok, tapi..."), langsung ke fakta, baru kasih apresiasi terpisah kalau memang ada hal bagus dari dia. Ngobrol empat mata, jangan di depan tim lain.
>
> Tiga hal yang saya belum tahu, biar naskahnya lebih pas:
> 1. Kejadian konkretnya apa persis (telat, salah kerja, target meleset, sikap ke pelanggan)?
> 2. Ini karyawan tipe gampang diajak bicara atau cenderung defensif/sungkan?
> 3. Standar/target yang kamu mau dia capai mulai kapan?

## Catatan penguji

**Nilai: SEBELUM 5,5 | SESUDAH 8,0**
- SEBELUM: saran 6 langkah umum, contoh kejadian dikarang ("laporan stok telat 2 hari" sebagai contoh), ditutup dengan pujian pembungkus (mirip sandwich), tanpa pesan WA, dan diakhiri tawaran "kalau mau saya bisa bantu". Pembuka "Saya sudah cek catatan sebelumnya" bocor.
- SESUDAH: langsung jadi: pesan WA ajakan + naskah empat mata + tindak lanjut dengan `[isian]` (tidak mengarang kejadian), catatan larangan pujian pembungkus, 3 pertanyaan di akhir. Kekurangan: naskah memakai `[Nama]` bukan `[isian: nama]`; salah ketik "bukan nawarin di WA"; menyebut urutan "konteks - fakta - dampak - tanya - sepakat" (nama kerangka) di judul.
