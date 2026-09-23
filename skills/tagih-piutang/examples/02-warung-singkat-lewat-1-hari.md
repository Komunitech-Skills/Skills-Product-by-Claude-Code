# 02 — Permintaan singkat: warung lewat 1 hari (tahap 3)

**Skenario:** S2 — permintaan malas; tidak ada nomor invoice & rekening → placeholder + asumsi.

**Input pengguna:**
> bikinin pesan nagih dong, warung bu tini 850rb jatuh tempo kemarin

**Perintah script:**
```bash
python3 scripts/hitung_telat.py --nominal 850rb --jatuh-tempo 2026-09-22 --tanggal 2026-09-23 --format teks
```
Hasil: sisa Rp 850.000, terlambat 1 hari, **Tahap 3** (konfirmasi ramah).

## Output

### Ringkasan tagihan
Sisa Rp 850.000 · jatuh tempo Selasa, 22 September 2026 · terlambat 1 hari · Tahap 3 (konfirmasi ramah) · tanpa denda.

### Pesan tahap 3 · WA · kirim hari ini (23 September 2026)
Selamat pagi, Bu Tini 🙏 Kami belum menerima pembayaran tagihan [No. Invoice/nota] sebesar Rp 850.000 yang jatuh tempo kemarin, 22 September. Mungkin terlewat ya, Bu. Jika sudah dibayar, mohon kirim bukti transfernya; jika belum, boleh kami tahu perkiraan tanggal pembayarannya? Pembayaran bisa ke [Bank – No. Rek – a.n.]. Terima kasih, Bu.

### Tahap berikutnya (jika belum dibayar)
- 29 September 2026 (lewat 7 hari) → tahap 4: minta tanggal pasti pembayaran, nada tegas-sopan.
- 6 Oktober 2026 (lewat 14 hari) → tahap 5: pemberitahuan tertulis + tawaran cicilan.

### Saran tindakan
- Kalau Bu Tini menjawab "minggu depan ya", minta tanggal pasti (mis. "Baik Bu, kami catat Senin, 28 September ya").
- Simpan chat sebagai bukti.

### Asumsi
- Nomor nota/invoice dan rekening belum diberikan → `[isi]`.
- Tidak ada kesepakatan denda → tanpa denda.
- Sapaan "Bu" dan nada ramah karena pelanggan warung (B2C/usaha kecil).

## Catatan penguji
- Tahap tepat (1 hari → tahap 3, asumsi baik). Jadwal tahap berikutnya dihitung dari jatuh tempo (+7 = 29 Sept, +14 = 6 Okt) — benar.
- Bagus: ringkas, siap kirim, satu placeholder yang jelas.
- Kurang (ringan): script tidak mengeluarkan tanggal tahap berikutnya; agent menghitung sendiri (+7/+14 dari jatuh tempo). Sebaiknya script menambahkan kolom "tahap berikutnya: tanggal" agar tidak dihitung manual.
