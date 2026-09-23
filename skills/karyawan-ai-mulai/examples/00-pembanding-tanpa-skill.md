# 00 — Uji A/B: S1 tanpa skill vs dengan skill

**Input (sama dengan S1):**
> mulai karyawan AI dong. saya punya rumah makan 2 cabang (kemang & bekasi), karyawan 55 orang. yang paling nyita waktu: bikin laporan penjualan harian, laporan keuangan bulanan buat bank, sama ngecek stok bahan baku. saya biasa pakai telegram, laptop kantor nyala terus. data karyawan jangan sampai kemana2 ya

## A. Tanpa skill (agent OpenClaw biasa, tanpa membaca skill apa pun)

> Wah, keren sekali Pak! Berikut langkah-langkah memulai "karyawan AI" untuk rumah makan Anda:
>
> **1. Laporan penjualan harian**
> - Gunakan aplikasi POS seperti Moka, Majoo, atau Pawoon yang punya laporan otomatis.
> - Ekspor data ke Google Sheets, lalu gunakan AI untuk meringkas.
> - Anda bisa membuat automasi dengan Zapier/Make untuk mengirim laporan ke Telegram.
>
> **2. Laporan keuangan bulanan**
> - Gunakan software akuntansi seperti Jurnal.id atau Accurate.
> - Pastikan laporan mengikuti standar SAK EMKM bila untuk bank.
>
> **3. Stok bahan baku**
> - Terapkan sistem FIFO, catat di spreadsheet, atau gunakan fitur inventori di POS.
>
> **4. Menjadikan saya karyawan AI**
> - Anda bisa menyuruh saya membaca file laporan dan meringkasnya.
> - Untuk otomasi, gunakan fitur cron di OpenClaw: `openclaw cron add ...`
>
> **5. Keamanan data**
> - Gunakan password kuat, aktifkan 2FA, dan batasi akses karyawan.
>
> Mau saya bantu salah satu langkah di atas?

## B. Dengan skill `karyawan-ai-mulai`
Lihat output lengkap di `01-owner-resto-50-karyawan-laporan.md`. Ringkasnya: ringkasan profil
untuk dikoreksi → 3 skill Komunitech yang spesifik (rekap-penjualan-csv, laporan-keuangan-emkm,
arus-kas-13minggu) + jujur "stok belum ada skill" → cek skill terpasang dan minta izin pasang
dengan perintah yang terverifikasi → **hasil nyata** berupa rekap omzet data contoh (angka
diverifikasi) → rencana 7 hari → tawaran cek privasi.

## Penilaian
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Hasil nyata di menit pertama | Tidak ada, hanya saran | Ada (rekap omzet + insight, angka benar) |
| Spesifik ke alat yang dimiliki | Menyarankan SaaS berbayar (Moka, Jurnal, Zapier) | Memakai skill yang sudah dibeli, jalan lokal |
| Langkah berikutnya jelas | "Mau saya bantu?" | Rencana 7 hari per hari + skill |
| Keamanan/izin | Tips umum 2FA | Izin eksplisit sebelum install, arah ke cek privasi |
| Perintah OpenClaw | `cron add ...` tidak lengkap | Perintah terverifikasi, Telegram default |
| Jujur soal batas | Tidak | Ya (stok belum ada) |

**Kesimpulan:** dengan skill **jelas lebih baik**. Hasilnya siap pakai, konsisten, dan sesuai
kendala member ("tidak tahu mulai", "tidak ada waktu", "privasi"). Catatan: keunggulan ini
bergantung pada agent yang **tidak** mempercayai rekomendasi script yang salah (lihat 03).

## Pembaruan uji ulang v1.1.0
Catatan "bergantung pada agent yang tidak mempercayai script yang salah" **tidak berlaku lagi**.
Script v1.1.0 mencocokkan kata utuh, lulus `--self-test` 25/25, dan tidak menghasilkan salah
cocok berbahaya pada frasa persona. Kesimpulan A/B tetap: **dengan skill jelas lebih baik**.
