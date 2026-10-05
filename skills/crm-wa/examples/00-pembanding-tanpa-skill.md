# 00 — Uji A/B: agent umum TANPA skill vs DENGAN crm-wa (skenario 01, toko kue 15 prospek)

- **Penguji:** agent penguji independen. Sisi "tanpa skill" = penguji berperan sebagai agent umum (Claude Code tanpa folder skill, tanpa script) yang menerima **pesan yang sama** dengan skenario 01, dikirim bertahap 10–24 Sep 2026 seperti pemakaian nyata (beberapa sesi chat terpisah). Sisi "dengan skill" = keluaran asli `crm.py` di `01-toko-kue-15-prospek-dua-minggu.md`.
- Data fiktif sama. Angka acuan = hitung ulang independen dari SQLite (0 beda).

## Sisi A — tanpa skill (perilaku agent umum, disimulasikan penguji)
Tanpa skill, agent umum biasanya menawarkan "saya catat di tabel" lalu (a) menyimpan tabel di jendela chat, atau (b) membuat file `prospek.md`/`.csv` ad hoc bila bisa menulis file. Contoh jawaban realistis pada 24 Sep untuk "Hari ini saya harus follow-up siapa?":

> Berdasarkan catatan kita, yang perlu di-follow-up:
> | Nama | Kebutuhan | Status | Terakhir |
> |---|---|---|---|
> | Kak Nia | brownies 5 loyang | tanya harga | 11 Sep |
> | Bu Sari | snack box / kue pengantin | baru | 19 & 23 Sep |
> | Pak Joko | tart pernikahan | baru | 22 Sep |
> | Mbak Wulan | roti sobek | baru | 23 Sep |
> Contoh pesan: "Halo Kak, mau follow up soal pesanannya, jadi order? 😊"
> Link: https://wa.me/+62 812 0000 1002?text=Halo Kak Nia...

Dan untuk "Rekap bulan ini, sumber paling bagus dari mana?":
> Total 15 calon pembeli, 5 order (konversi ±33%). Sumber terbanyak **Instagram (6 orang)**, jadi Instagram paling bagus.

Masalah yang teramati/terukur pada sisi A:
1. **Tidak ada ingatan antar-sesi.** Di sesi baru (mis. OpenClaw/Claude Code dibuka ulang), 14 hari cerita hilang kecuali pemilik menempel ulang. Tidak ada cadangan.
2. **Jadwal follow-up tidak disimpan**: agent menebak dari "terakhir dihubungi"; Kak Yoga (dijanjikan follow-up 16/9) dan Bu Rina/Bu Lilis (deal, perlu konfirmasi order) mudah terlewat.
3. **Dua "Bu Sari" digabung** menjadi satu baris (nomor berbeda, kebutuhan berbeda) — risiko salah kirim.
4. **Nomor tidak dinormalisasi**; tautan wa.me ditulis tangan dengan spasi & tanda "+" → di Telegram/WA tautan terpotong di spasi pertama (tidak bisa diklik utuh).
5. **Definisi angka tidak baku:** "sumber terbaik" dihitung dari jumlah lead (Instagram 6), padahal nilai deal Referensi = Instagram (Rp1.850.000) dengan konversi 50% vs 33,3%; nilai deal, rata-rata lama closing, win rate, alasan batal tidak ada. Tanpa rumus tertulis, angka bisa berubah tiap kali ditanya.
6. **Nada draf** generik dan sedikit mendesak ("jadi order?"), tidak berjenjang (tidak ada pesan pamit / pilihan 1-2-3), tidak disesuaikan tahap.
7. Privasi: tidak ada versi disamarkan; catatan pribadi ("suaminya pelit", "budget ketat") bisa ikut terkutip di draf bila agent menyusun dari catatan.

## Sisi B — dengan crm-wa (keluaran asli)
- Data persisten di SQLite + cadangan harian otomatis; nomor semua jadi `62…` dan tampil `0812-0000-1002`.
- `hari-ini`: **10 terlambat + 1 besok**, lengkap tahap, nilai, catatan terakhir, dan 10 draf berjenjang (sapaan-awal / follow-up-1 / konfirmasi-order) + tautan wa.me ter-encode benar (33/33 tautan diverifikasi).
- Dua "Bu Sari" **ditolak sebagai ambigu** dan agent bertanya "yang mana".
- `rekap`: lead 15, deal 5 senilai Rp3.875.000, rata Rp775.000, closing 2,6 hari, konversi 33,3%, win rate 62,5%, sumber terbaik **Referensi** (seri nilai, menang konversi) + catatan "sampel kecil", alasan batal. **0 beda** dengan hitung ulang independen; rumus bisa ditampilkan (`--rumus`).
- `--samarkan` untuk dibagikan; jadwal Telegram tanpa model AI.

## Skor berdampingan (penguji, skala 1–5)
| Kriteria | Tanpa skill | Dengan crm-wa |
|---|---|---|
| Data tetap ada besok / sesi baru | 1 | 5 |
| Daftar follow-up lengkap & tepat waktu | 2 | 4 (S1: deal lama ikut "terlambat") |
| Ketepatan angka rekap & definisi baku | 2 | 5 |
| Kontak dobel / nama ambigu | 1 | 4 (S2: kasus satu batal) |
| Draf sopan, berjenjang, tautan bisa diklik | 2 | 5 |
| Privasi (samarkan, catatan tidak masuk draf) | 2 | 4 (S5: kolom kebutuhan masuk draf) |
| **Total** | **10/30** | **27/30** |

**Kesimpulan A/B:** dengan skill **jelas lebih baik** — terutama ingatan antar-sesi, daftar follow-up berbasis jadwal, angka yang bisa dipertanggungjawabkan, dan tautan wa.me yang benar. Bahan "sebelum/sesudah" README sudah sesuai temuan ini.
