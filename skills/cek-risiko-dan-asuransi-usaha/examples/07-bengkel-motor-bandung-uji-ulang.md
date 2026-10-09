# 07 (uji ulang v1.0.1) — Normal 2: bengkel motor, Bandung Barat (gaji "@ x 3", kerugian vs dana darurat)

- Tanggal: 2026-10-09 · Penguji independen · `claude-code (simulasi agent)`
- Data risiko: `data/07-bengkel-bandung-uji-ulang.json`. Tujuan khusus: memancing cacat lama B1 (nama biaya dobel) dan memakai `--dana` untuk `kerugian_rp`.

## Pesan
> bengkel motor sy nyewa kios di padalarang, sy sendiri kepala mekaniknya + 3 mekanik gaji @2,5jt. sewa kios 2jt/bln, listrik 800rb, cicilan kompresor 600rb. motor pelanggan sering nginep 3-5 unit. kas 12jt. kalo kebakaran kira2 rugi 120jt (alat + sparepart). perlu asuransi apa aja?

## Jalannya script
- Percobaan pertama ditulis seperti pesan: `--biaya "Sewa kios=2.000.000,Gaji=2.500.000,Gaji=2.500.000,Gaji=2.500.000,..."` → **ditolak**: `nama biaya 'Gaji' dobel. Jumlahkan dulu jadi satu angka ...` (exit 2). Di v1.0.0 ini menghasilkan Rp2,5 jt diam-diam; kini aman.
- Ulang: `dana --biaya "Sewa kios=2.000.000,Gaji 3 mekanik=7.500.000,Listrik=800.000,Cicilan kompresor=600.000" --bulan 3 --kas 12.000.000 --cicil 12`
- `risiko data.json --dana 32.700.000`

## Output SESUDAH (ringkas)
> **Asumsi:** kios sewa di Padalarang (Bandung Barat), 3 mekanik + Bapak; nilai alat & sparepart ±Rp120 jt (dari Bapak).
>
> | No | Risiko | K | D | Skor/Tingkat | Langkah murah | Perlu asuransi? |
> |---|---|---|---|---|---|---|
> | 1 | Kebakaran (bensin, oli, las, korsleting) | 2 | 5 | 10 TINGGI | APAR di dekat area las, bensin bekas di jeriken tertutup jauh dari gerinda, cek kabel kompresor | Ya, pertimbangkan |
> | 2 | Mekanik cedera kerja | 3 | 3 | 9 SEDANG | Kacamata gerinda, sarung tangan, dongkrak dicek | BPJS (wajib bagi pemberi kerja, cek aturan terbaru) |
> | 3 | Mekanik terbaik pindah ke bengkel lain | 3 | 3 | 9 SEDANG | Catat SOP servis, bonus bulanan, latih mekanik kedua | Tidak ada asuransi umum; pakai mitigasi lain |
> | 4 | Gempa bumi (cek peta resmi BMKG/BNPB untuk lokasi) | 2 | 4 | 8 SEDANG | Rak sparepart diikat ke dinding, barang berat di bawah | Ya, pertimbangkan (perluasan polis) |
> | 5 | Komplain servis gagal (rem blong) | 2 | 4 | 8 SEDANG | Checklist uji rem sebelum motor diserahkan, nota mencantumkan pekerjaan | Ya, pertimbangkan (tanggung gugat) |
> | 6 | Motor pelanggan hilang/rusak saat dititip | 2 | 4 | 8 SEDANG | Tanda terima titipan, kunci ganda, CCTV | Ya, pertimbangkan (tanyakan ke agen apakah kendaraan titipan bisa dijamin) |
> | 7 | Bapak (kepala mekanik) sakit/kecelakaan | 2 | 4 | 8 SEDANG | Satu mekanik dilatih jadi kepala pengganti | Ya, pertimbangkan (kecelakaan diri/kesehatan pribadi) |
> | 8 | Pencurian alat/sparepart | 3 | 2 | 6 SEDANG | Lemari alat terkunci, stok opname mingguan | Tidak perlu |
>
> Dana darurat 3 bulan: biaya tetap Rp10.900.000/bln → target **Rp32.700.000**; kas Rp12.000.000 (cukup 1,1 bulan); kekurangan **Rp20.700.000** → **Rp1.725.000/bulan selama 12 bulan**. Kerugian kebakaran Rp120 jt jauh di atas dana darurat, karena itu baris 1 layak dialihkan.
> Perlindungan umum, pertanyaan ke agen (8 butir), disclaimer, 3 prioritas (APAR & area las, checklist rem, tanda terima titipan) dan 3 pertanyaan (kios: siapa yang mengasuransikan bangunan? nilai motor titipan rata-rata? sudah ada BPJS TK?).

## Verifikasi (independen, Decimal)
Skor 10, 9, 9, 8, 8, 8, 8, 6 cocok. 2.000.000 + 7.500.000 + 800.000 + 600.000 = 10.900.000; ×3 = 32.700.000; −12.000.000 = 20.700.000; /12 = 1.725.000 (pas); 12/10,9 = 1,10 → 1,1. Cocok.

## Catatan penguji
- Perbaikan B1 (dobel) dan B4 (cicilan) bekerja di alur nyata.
- Baris 2 lagi-lagi harus ditimpa agent (script: "Tidak perlu") → cacat R1.
- Motor titipan: rujukan `jenis-perlindungan.md` hanya punya "tanggung gugat umum"; polis umum sering mengecualikan barang milik pihak lain yang dalam penguasaan tertanggung. Agent menulis "tanyakan ke agen" (aman), tetapi rujukan tidak membantu (lihat R2).

**Skor: SESUDAH 8,5.**
