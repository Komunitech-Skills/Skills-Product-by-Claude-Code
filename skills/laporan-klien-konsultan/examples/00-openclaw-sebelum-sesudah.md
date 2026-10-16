# Uji OpenClaw SEBELUM vs SESUDAH — laporan-klien-konsultan

Sumber (ada di paket VIP): `solusi-vip/konsultan/UJI-OPENCLAW.md` (rincian: `solusi-vip/konsultan/uji-openclaw/04-laporan-progres-klien.md` dan `04-laporan-progres-klien-ulang.md`). Tanggal uji: 2026-10-01 (Asia/Jakarta). Versi skill saat uji: uji pertama tidak dicatat di sumber (sebelum revisi 1.0.5); uji ulang = 1.0.5. Versi katalog saat ini 1.0.6 belum diuji ulang sebelum/sesudah di OpenClaw (menurut `CHANGELOG.md`, 1.0.6 hanya merapikan referensi jadwal dan penanda versi; cara kerja tidak berubah). Penguji: agent penguji independen (bukan pembuat skill).

Berkas ini hanya menyalin ringkasan dari catatan uji internal di atas; balasan utuh kedua sisi ada di berkas sumber. Hasil uji pemasangan/pemicu OpenClaw (6 dari 6 butir) ada terpisah di `UJI-PLATFORM.md`; itu bukan uji sebelum/sesudah.

## Cara uji
- OpenClaw lokal (`openclaw agent --local`, tanpa Telegram/gateway), model router Komunitech yang sama dengan bot member (`ninerouter/komunitech`, jawaban `claude-sonnet-5`).
- SEBELUM = home tanpa skill; SESUDAH = home dengan paket skill Konsultan & Freelancer. File fiktif `catatan-kerja.csv` identik di kedua workspace (9 baris, 2 klien, format awam "2,5 jam", "90 menit", "3,25 jam").
- Pesan member: laporan progres mingguan 22-26 Sep untuk PT Sentosa Makmur dari file `catatan-kerja.csv`; member mengirim sendiri ke klien lewat WA.
- Hitungan benar menurut penguji: 2,5 + 1,5 + 3,25 + 1 + 1,5 = 9,75 jam (9 jam 45 menit).

## Skor (skala 10)

| # | Skenario | Tanpa skill | Dengan skill (uji pertama) | Dengan skill (uji ulang, v1.0.5) | Pembeda satu kalimat |
|---|---|---|---|---|---|
| 1 | Laporan progres mingguan klien dari file CSV catatan kerja | 8 | 7 | 8,5 | Uji pertama: tanpa skill menjumlah tepat 9 jam 45 menit sedangkan skill membulatkan satu desimal (3,25 menjadi "3,2", total "9,8" tidak sama dengan jumlah item 9,7); setelah revisi: "9,75 jam (9 jam 45 menit)", CSV member dibaca langsung, bagian "Rencana berikutnya" berupa isian `[isi: ...]` yang tidak dikarang, dan tidak mengirim apa pun ke klien. |
| | **Rata-rata** (satu skenario) | **8** | **7** | **8,5** | |

## Verdik
**LULUS uji ulang** (8,5). Pada uji pertama skill KALAH dari model tanpa skill (7 melawan 8), dan sumber melarang pemakaiannya sebagai materi jualan sampai pembulatan jam diperbaiki; larangan itu dicabut setelah uji ulang.

## Catatan jujur
- Selisih pada uji ulang hanya 0,5 poin dibanding sisi tanpa skill uji pertama (sisi tanpa skill tidak diulang). Sumber menulis: model tanpa skill juga menjumlah benar; pembeda skill ada pada rencana yang tidak dikarang dan format yang konsisten.
- Cacat uji pertama yang hilang pada uji ulang: pembulatan jam, teks "Periode periode kustom", CSV member tidak terbaca (agent menyalin baris satu per satu), "Rencana berikutnya" mekanis ("Lanjutkan ..." tiga kali). Pencarian ke seluruh disk (`find /`): kemungkinan besar hilang (panggilan alat turun dari 8 ke 5; argumen tidak dibaca).
- Draf belum langsung bisa dikirim: ada 3 isian `[isi: ...]` yang harus dilengkapi member (disengaja agar tidak mengarang), sehingga butuh satu giliran tambahan dibanding model tanpa skill yang menulis kalimat penutup sendiri (dikarang). Rentang tanggal tertulis dua kali berturut-turut (redundan).
- Hanya satu skenario di OpenClaw.
