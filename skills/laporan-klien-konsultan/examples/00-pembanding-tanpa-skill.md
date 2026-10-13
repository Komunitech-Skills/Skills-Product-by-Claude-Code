# Uji A/B — Tanpa skill vs Dengan skill

> Dijalankan oleh **penguji independen (Akun B)**, bukan pembuat skill, sesuai pedoman kurasi Komunitech tahap 6.
> Skenario: sama seperti Skenario 01 (konsultan pajak, PT Maju Jaya, 21-27 September 2026).

## Prompt yang diberikan ke agent
> "Catat: hari ini aku kelarin rekonsiliasi bank buat PT Maju Jaya, 2,5 jam. Terus lagi ngerjain
> draf SPT Masa PPN, masih nunggu faktur pajak masukan Oktober dari mereka, udah 1,5 jam. Terus
> hari Jumat, tolong buatkan laporan mingguan untuk PT Maju Jaya."

## TANPA skill (agent generik, tanpa `laporan-klien-konsultan`)
Agent tidak punya tempat menyimpan catatan harian, sehingga:
- Tidak ada file log — begitu sesi chat baru dimulai/ditutup, catatan hilang. Agent hanya bisa
  mengarang draf dari apa yang diketik user **dalam sesi yang sama**, tidak bisa merakit dari
  catatan beberapa hari yang terpisah kalau usernya tidak mengulang semua detail lagi.
- Total jam dihitung agent secara mental dari teks (2,5 + 1,5 = 4 jam) — benar untuk kasus mudah
  ini, tapi tidak ada jaminan konsisten untuk kasus dengan banyak baris/lintas proyek, dan tidak
  ada rincian per proyek otomatis.
- Tidak ada satu format konsisten untuk email/WA/Markdown — setiap kali diminta, agent bisa
  menghasilkan struktur/urutan bagian yang sedikit berbeda.
- Tidak ada deteksi data pribadi/rahasia sebelum draf disodorkan.
- Tidak ada rincian "N entri tanpa jam" — bila salah satu pekerjaan lupa disebutkan jamnya, ada
  risiko agent diam-diam menganggap 0 jam atau melewatkannya.
- Contoh keluaran (diringkas, hasil generik tanpa struktur baku):
  > "Berikut laporan untuk PT Maju Jaya minggu ini: Kami telah menyelesaikan rekonsiliasi bank
  > (2,5 jam) dan sedang mengerjakan draf SPT Masa PPN (1,5 jam), masih menunggu faktur pajak
  > masukan Oktober. Total sekitar 4 jam pengerjaan. Semoga membantu!"
  > — hanya satu versi teks (bukan email/WA/Markdown terpisah), tanpa bagian "Rencana
  > Berikutnya" eksplisit, dan tidak ada peringatan tinjau data pribadi.

## DENGAN skill
Perintah yang sama dieksekusi lewat `scripts/laporan_klien.py` (lihat `examples/01-konsultan-pajak-normal.md`
untuk transkrip lengkap): dua entri `catat` tersimpan permanen di `log-kerja-klien.csv`, lalu
`laporan --klien "PT Maju Jaya" --periode mingguan` menghasilkan:
- Tiga versi berlabel jelas (email/WA/Markdown) dari data yang **sama persis** — tidak perlu
  diminta ulang formatnya beda-beda.
- Total jam **4 jam** dihitung oleh script (bukan dikira agent), dengan rincian per proyek dan
  penanda jumlah entri tanpa jam bila ada.
- Bagian "Butuh dari Klien" (faktur pajak) dan "Rencana Berikutnya" (diturunkan otomatis dari
  status `berjalan`) muncul konsisten setiap kali diminta, walau ditanyakan besok atau minggu
  depan — karena datanya ada di file, bukan di memori sesi chat.
- Peringatan otomatis bila ada pola NIK/HP/email/kata sandi di teks (tidak terjadi di skenario
  ini, lihat Skenario 05 untuk contohnya).

## Kesimpulan uji A/B
**Dengan skill jelas lebih baik** untuk kasus yang menjadi inti nilai jual skill ini: pencatatan
**rutin lintas hari/minggu** (bukan hanya satu sesi chat), total jam yang **dihitung** (bukan
dikira), tiga versi format yang **konsisten** setiap diminta ulang, dan deteksi data sensitif
sebelum draf ditinjau. Untuk skenario satu-sesi-langsung-jadi seperti prompt di atas, selisihnya
tampak kecil karena datanya sedikit — keunggulan skill baru terasa besar begitu ada banyak entri
lintas minggu/proyek atau saat laporan diminta beberapa hari setelah pekerjaan dicatat (lihat
Skenario 02 dan 03 untuk kasus dengan lebih banyak entri). Skill **lolos** ambang nilai tambah
Tahap 6 (tidak dibatasi skor maks. 6).
