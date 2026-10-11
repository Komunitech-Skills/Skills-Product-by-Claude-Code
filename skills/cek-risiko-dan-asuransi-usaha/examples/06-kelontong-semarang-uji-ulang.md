# 06 (uji ulang v1.0.1) — Normal 1: toko kelontong di rumah, Semarang Utara (rob)

- Tanggal: 2026-10-09 · Penguji independen (bukan pembuat) · `claude-code (simulasi agent)`. Router model OpenClaw mati (HTTP 530), jadi ini **uji isi oleh agent**, bukan uji OpenClaw sebelum/sesudah.
- Data risiko: `data/06-kelontong-semarang-uji-ulang.json`. Pembanding tanpa skill: `00-pembanding-tanpa-skill.md` bagian "Uji ulang v1.0.1".

## Pesan
> min sy pny toko kelontong di rumah, semarang utara deket pelabuhan, kalo musim hujan + rob suka masuk air sebetis. stok sembako + rokok kira2 45jt, ada kulkas & freezer es krim titipan. jaga sendiri sm istri + 1 pegawai harian 1,8jt/bln (blm bpjs). listrik 650rb, cicilan motor buat kulakan 900rb, setor arisan 500rb. tabungan toko 6jt. sering ada yg ngutang. perlu asuransi ga? dana darurat brp?

## Perintah yang dijalankan (seperti agent mengikuti SKILL.md)
```
python3 scripts/cek_risiko.py dana --biaya "Gaji pegawai=1.800.000,Listrik=650.000,Cicilan motor=900.000" --bulan 3 --kas 6.000.000 --cicil 6
python3 scripts/cek_risiko.py risiko data.json --dana 10.050.000
```

## Output SESUDAH (dengan skill)
> **Asumsi:** toko kelontong di rumah sendiri, Semarang Utara (rawan rob), dijaga Bapak/Ibu + 1 pegawai; stok ±Rp45 jt; arisan Rp500 rb **tidak** saya hitung sebagai biaya tetap (itu tabungan, bukan pengeluaran usaha).
>
> | No | Risiko | Kemungkinan | Dampak | Skor/Tingkat | Langkah murah minggu ini | Perlu asuransi? |
> |---|---|---|---|---|---|---|
> | 1 | Banjir rob masuk toko | 4 | 3 | 12 TINGGI | Semua stok di palet/rak ≥ 40 cm, karung beras & gula di rak atas, colokan kulkas dipindah lebih tinggi | Tidak perlu (terlalu sering; kurangi dengan langkah murah) |
> | 2 | Kebakaran (kabel, kompor dapur, stok rokok) | 2 | 5 | 10 TINGGI | APAR 3 kg dekat pintu, cek kabel & stop kontak kulkas/freezer, kompor jangan ditinggal | Ya, pertimbangkan |
> | 3 | Utang pelanggan macet | 5 | 2 | 10 TINGGI | Buku utang dengan batas per orang, tidak ada utang baru sebelum yang lama lunas | Tidak ada asuransi umum; pakai mitigasi lain |
> | 4 | Pencurian rokok/uang laci | 3 | 3 | 9 SEDANG | Rokok di etalase terkunci, setor uang laci tiap sore, CCTV murah | Tidak perlu |
> | 5 | Bapak/Ibu sakit, toko tutup | 2 | 3 | 6 SEDANG | Catat harga & pemasok di satu buku agar pegawai bisa jaga | Tidak perlu |
> | 6 | Bukti transfer/QRIS palsu | 3 | 2 | 6 SEDANG | Barang diserahkan setelah notifikasi masuk terlihat di HP toko | Tidak perlu |
> | 7 | Freezer/kulkas rusak, listrik padam | 3 | 2 | 6 SEDANG | Tanyakan pemilik freezer titipan siapa yang tanggung isi bila rusak; simpan nomor teknisi | Tidak perlu |
> | 8 | Gempa bumi | 1 | 4 | 4 RENDAH | Rak tinggi diikat ke dinding | Ya, pertimbangkan (sebagai perluasan polis kebakaran, cek ke agen) |
> | 9 | Pegawai cedera angkat karung | 2 | 2 | 4 RENDAH | Angkat berdua, troli | BPJS (wajib bagi pemberi kerja, cek aturan terbaru) |
>
> **Dana darurat (3 bulan)**
> - Biaya tetap per bulan: Rp3.350.000 (gaji pegawai 1,8 jt + listrik 650 rb + cicilan motor 900 rb)
> - Target: **Rp10.050.000**
> - Kas sekarang: Rp6.000.000 (cukup 1,8 bulan biaya tetap)
> - Kekurangan: **Rp4.050.000** → sisihkan **Rp675.000 per bulan selama 6 bulan**.
>
> **Jenis perlindungan umum (tanpa merek)**
> - Asuransi kebakaran/properti untuk stok & isi toko: tanyakan apakah banjir dan gempa termasuk atau perlu perluasan terpisah. Karena rob datang hampir tiap musim, perluasan banjir bisa mahal atau dikecualikan; langkah murah lebih penting.
> - BPJS Ketenagakerjaan & BPJS Kesehatan untuk pegawai: kewajiban pemberi kerja dan iuran dicek di sumber resmi BPJS per hari ini.
> Asuransi mengalihkan kerugian besar yang jarang terjadi, bukan pengganti langkah murah; selalu ada premi, pengecualian, dan batas klaim. Cek izin perusahaan di OJK dan bayar ke rekening perusahaan, bukan pribadi.
>
> **3 prioritas minggu ini:** (1) naikkan semua stok ke palet/rak sebelum musim hujan; (2) APAR + cek kabel kulkas/freezer; (3) buat batas utang per pelanggan.
>
> *Ini alat bantu awam, bukan nasihat asuransi, keuangan, atau hukum.*
> Pertanyaan: 1) Saat rob terakhir, kira-kira berapa rupiah barang yang rusak? 2) Rumah milik sendiri atau sewa? 3) Mau target dana darurat 3 atau 6 bulan?

## Verifikasi (independen, `data/verifikasi-uji-ulang.py`, Decimal)
Skor 12, 10, 10, 9, 6, 6, 6, 4, 4 dan tingkatnya cocok. 1.800.000 + 650.000 + 900.000 = 3.350.000; ×3 = 10.050.000; − 6.000.000 = 4.050.000; /6 = 675.000 (pas); 6/3,35 = 1,79 → 1,8. Cocok.

## Catatan penguji
- Baris 9: script memberi "Terima / Tidak", SKILL.md menyuruh menulis label BPJS. Agent harus menimpa kolom hasil script (bertentangan dengan "ikuti kolom hasil script"). Lihat cacat R1 di HASIL-UJI-uji-ulang-v1.0.1.md.
- Baris 1 (rob sering → "Tidak perlu") dan baris 8 (gempa jarang → "Ya, pertimbangkan") tampak terbalik bagi awam; skill sudah menjelaskan prinsipnya, agent perlu satu kalimat penjelas (ditulis di atas).
- Utang macet ditandai `bisa_diasuransikan: false` → kolom benar (perbaikan B2 bekerja).

**Skor: SESUDAH 8,5.**
