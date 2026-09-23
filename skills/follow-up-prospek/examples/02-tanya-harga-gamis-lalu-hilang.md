# 02 — Permintaan singkat: "tanya harga lalu hilang" (B2C, online shop)

**Skenario:** S2 — permintaan malas/singkat; tahap D (B2C), akhir pekan boleh, 3 pesan.

**Input pengguna:**
> bikinin follow up dong buat yg nanya harga gamis terus ngilang, hari ini ada 5 orang

**Perintah script:**
```bash
python3 scripts/jadwal_followup.py --mulai 2026-09-23 --hari "1,3,7" --termasuk-akhir-pekan
```

## Output

### Jadwal follow-up – pembeli yang tanya harga gamis (tanya harga lalu hilang)
Kontak terakhir (H+0): Rabu, 23 September 2026

| Ke | Rencana | Tanggal kirim | Catatan |
|---|---|---|---|
| 1 | H+1 | Kamis, 24 September 2026 | - |
| 2 | H+3 | Sabtu, 26 September 2026 | - |
| 3 | H+7 | Rabu, 30 September 2026 | - |

Kirim ke masing-masing dari 5 orang itu **satu per satu** (bukan broadcast/grup), ganti `[Nama]` dan `[model]` sesuai yang ditanyakan.

### Pesan ke-1 · Kamis, 24 September 2026 · WA
Halo Kak [Nama] 😊 Kemarin sempat tanya gamis [model] ya. Mau aku bantu cekkan ukuran atau warna yang paling cocok, Kak? Tinggal kirim tinggi & berat badan aja.

### Pesan ke-2 · Sabtu, 26 September 2026 · WA
Kak [Nama], ini foto asli gamis [model] dari pembeli lain biar kebayang jatuhnya bahan. Kalau ada pertanyaan soal bahan, ukuran, atau ongkir ke kota Kakak, tanya aja ya.

### Pesan ke-3 · Rabu, 30 September 2026 · WA
Kak [Nama], aku nggak akan spam kok 🙏 Kalau nanti butuh gamis [model] atau model lain, chat aja kapan pun ya. Makasih sudah mampir!

### Aturan main
- Kirim 09.00–11.00, 13.00–15.00, atau 19.00–20.30 (pembeli perorangan sering membalas malam); hindari larut malam.
- Kalau pembeli membalas → hentikan urutan, layani pertanyaannya.
- Kalau dijawab "nggak jadi" → "Siap Kak, makasih ya 🙏" lalu berhenti.
- "Mahal" → jelaskan bahan & jahitan, tawarkan model lain yang lebih terjangkau (jangan langsung diskon).

### Asumsi
- Foto testimoni di pesan ke-2 hanya dikirim bila **benar ada** dan pembelinya sudah mengizinkan fotonya dipakai; jika tidak ada, ganti dengan foto produk asli buatan sendiri.
- Tidak ada promo/gratis ongkir karena tidak disebutkan.
- Kontak berasal dari pembeli yang chat duluan (boleh dihubungi untuk urusan ini).

## Catatan penguji
- Tanggal benar (Sabtu tidak digeser karena `--termasuk-akhir-pekan`).
- Bagus: mengikuti tahap D di `references/urutan-per-tahap.md`, 3 pesan saja, menekankan kirim satu per satu (bukan broadcast) sesuai prinsip privasi.
- Kurang (ringan): jam kirim malam untuk B2C tidak ada di SKILL.md ("Aturan main" hanya jam kantor); agent menambahkan sendiri. Pertimbangkan aturan jam kirim terpisah untuk B2C.
