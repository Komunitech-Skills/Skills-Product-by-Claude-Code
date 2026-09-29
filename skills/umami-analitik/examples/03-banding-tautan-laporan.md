# 03 — Normal: "Minggu ini dibanding minggu lalu gimana? Link di bio IG diklik berapa? Kirim laporan tiap Senin ke Telegram."

**Pembuat:** uji pembuat 29 Sep 2026 terhadap **Umami 3.4.0 asli** (Docker resmi, 127.0.0.1) dengan data fiktif landing page "Keripik Bu Sri" (`tests/isi_data_fiktif.py`). Akun AI `agen-baca` (view-only via tim), kunci API. Penguji independen menulis hasilnya sendiri di `HASIL-UJI.md`.

## Yang dijalankan agent
```
umami.py banding                      # Selasa 29 Sep 16.00 WIB
umami.py tautan --periode 7hari
umami.py laporan-mingguan             # isi pesan Telegram
```
Jadwal: agent menunjukkan perintah `openclaw automations add ... --cron "0 7 * * 1" --tz Asia/Jakarta ...` dari `references/openclaw-jadwal.md` lalu bertanya "Lanjut? (ya/tidak)" — **pengiriman Telegram belum diuji** (butuh bot asli).

## Keluaran skill (apa adanya)
```
PERBANDINGAN: Keripik Bu Sri (landing) (keripikbusri.contoh.id)
Periode: minggu ini, Senin 28 Sep 2026 s.d. Selasa, 29 September 2026 pukul 16.00
Pembanding: 21 Sep 2026 - 22 Sep 2026 pukul 16.00 (sama panjang)
  Ukuran                  Periode ini    Pembanding            Perubahan
  Pengunjung unik                   7             2       naik 5 (+250%)
  Kunjungan                         7             2       naik 5 (+250%)
  Tayangan halaman                 13             5       naik 8 (+160%)
  Bounce rate                   28,6%            0%       naik 28,6 poin
  Rata-rata lama               44 dtk  1 mnt 37 dtk  turun 53 dtk (-55%)
  Event 'klik-wa'                   2             1       naik 1 (+100%)
  Event 'beli'                      1             0                 baru
Catatan: periode berjalan dibandingkan dengan rentang yang SAMA PANJANG sampai jam yang sama (adil, bukan minggu penuh vs setengah minggu).

TAUTAN PELACAK (Umami Links)
Periode: 7 hari terakhir, 23 Sep 2026 - 29 Sep 2026 (s.d. pukul 17.00)
Pembanding: 16 Sep 2026 - 22 Sep 2026 pukul 17.00 (sama panjang)
  Tautan                      Klik  Pengunjung  Sebelumnya    Asal klik teratas
  WA order (bio IG)              3           3           0  l.instagram.com (3)
Klik = berapa kali tautan dibuka (termasuk orang yang sama berulang). Tautan dibuka dari aplikasi WA/Telegram biasanya tanpa asal klik.

Laporan web Keripik Bu Sri (landing) (keripikbusri.contoh.id)
Periode: minggu lalu, Senin 21 Sep 2026 - Minggu 27 Sep 2026
Pembanding: 14 Sep 2026 - 20 Sep 2026

- Pengunjung unik       : 11   (sebelumnya 4; naik 7 (+175%))
- Kunjungan             : 12   (sebelumnya 4; naik 8 (+200%))
- Tayangan halaman      : 23   (sebelumnya 6; naik 17 (+283%))
- Bounce rate           : 25% (3 dari 12 kunjungan hanya 1 halaman tanpa klik)   (sebelumnya 50%)
- Rata-rata lama        : 48 dtk per kunjungan   (sebelumnya 17 dtk)
- Halaman per kunjungan : 1,9

Konversi:
- klik-wa: 3x oleh 3 pengunjung (27,3%); sebelumnya 1x
- beli: 2x oleh 2 pengunjung (18,2%); sebelumnya 0x

Halaman teratas:
1. / - 11 tayangan, 10 pengunjung
2. /produk/keripik-balado - 5 tayangan, 5 pengunjung
3. /cara-pesan - 3 tayangan, 3 pengunjung
4. /produk/keripik-original - 2 tayangan, 2 pengunjung
5. /terima-kasih - 2 tayangan, 2 pengunjung

Sumber:
- Media sosial: 6 kunjungan (50%)
- Langsung: 4 kunjungan (33%)
- Pencarian Google dll: 2 kunjungan (17%)

Kampanye UTM (pengunjung):
- kampanye promo-gajian-sep: 7
- sumber instagram: 3
- sumber tiktok: 2
- sumber whatsapp: 2

Perangkat: HP 73%, Komputer (layar besar) 18%, Tablet 9%
Kota teratas: Jakarta (2), Surabaya (2), Denpasar (1)

Sumber data: Umami milik Anda (tanpa cookie). Pengunjung unik = perangkat+browser.
```

## Verifikasi independen
- Banding adil: minggu ini (Senin 00.00 – Selasa 16.00) vs Senin 21 Sep 00.00 – Selasa 22 Sep 16.00. Kunjungan F (20.15) & G (21.40) tanggal 22 **tidak** ikut → pembanding 2 pengunjung (A, E), 5 tayangan, rata-rata (45+150)÷2 = 97 dtk = 1 mnt 37 dtk. Minggu ini 7/13, 310÷7 = 44 dtk. **Cocok.**
- Tautan: 3 klik `curl` ke `/q/wa-busri-bio` dengan Referer Instagram → 3 klik, 3 pengunjung. **Cocok.**
- Laporan mingguan 1.342 karakter (< 4.096 batas satu pesan Telegram).
