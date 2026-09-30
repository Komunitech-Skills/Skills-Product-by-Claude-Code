# 04 — Input tidak lengkap

**Input pengguna (persis):**
> tolong hitungin spt tahunan saya dong, saya kerja kantoran sama ada kerjaan sampingan

**Output (agent bertanya sekali, sesuai SKILL.md):**

> Siap, saya bantu hitung. Mohon jawab singkat:
> 1. Tahun pajak berapa (2025 yang dilaporkan tahun ini?), dan status Anda per 1 Januari tahun itu: belum/sudah menikah, berapa tanggungan (anak/orang tua yang ditanggung, maks 3)?
> 2. Dari bukti potong kantor (A1/A2): angka **penghasilan neto** dan **PPh 21 yang dipotong**. Kalau pindah kerja, sebutkan untuk setiap kantor.
> 3. Kerja sampingannya apa (mis. desain, les, jualan online) dan berapa total pemasukan kotor setahun? Kalau pakai norma (NPPN): persen normanya berapa dan apakah sudah memberitahukan DJP paling lambat 31 Maret tahun itu? Kalau jualan dengan PPh final 0,5%, sebutkan omzet setahun.
> 4. Ada potongan pajak dari klien (bukti potong PPh 21/23) atau angsuran PPh 25 yang sudah dibayar? Totalnya berapa?
> 5. Bayar zakat sendiri ke BAZNAS/LAZ (bukan lewat kantor)? Berapa setahun?
>
> Kalau mau cepat: sebutkan saja status dan dua angka di A1 (neto & PPh 21) serta pemasukan sampingan setahun — sisanya saya anggap 0 dan saya tulis asumsinya.

**Tindak lanjut (pengguna menjawab):** "2025, TK/0, A1 neto 114 juta PPh 21 3 juta. Sampingan ngajar les privat 36 juta setahun, norma 50% katanya, belum pernah lapor norma. Nggak ada potongan lain, zakat nggak."

**Perintah:**
```bash
python3 scripts/spt_op.py --status TK/0 --tahun 2025 --a1 114jt 3jt --nppn 36jt 50 --nppn-diberitahukan tidak --hari-ini 2026-09-30
```

**Inti output (disalin dari script):** neto Rp114.000.000 + Rp18.000.000 = Rp132.000.000 → PKP Rp78.000.000 → PPh Rp3.000.000 + Rp2.700.000 = **Rp5.700.000**; kredit Rp3.000.000 → **KURANG BAYAR Rp2.700.000**; perkiraan PPh 25 2026 Rp225.000/bulan. Peringatan: NPPN belum diberitahukan → menurut DJP dianggap memilih **pembukuan**, jadi hasil norma hanya simulasi; batas lapor TP 2025 sudah lewat.

**Catatan agent ke pengguna:** karena belum memberitahukan NPPN, penghasilan les harus dihitung dari catatan pemasukan dikurangi biaya yang benar-benar dikeluarkan (pembukuan). Kalau Anda punya catatannya, sebutkan neto (pemasukan − biaya) dan saya hitung ulang dengan `--pembukuan-neto`. Untuk memastikan status norma Anda, tanyakan Kring Pajak 1500200 atau konsultan.

**Verifikasi manual:** 36.000.000 × 50% = 18.000.000; 132.000.000 − 54.000.000 = 78.000.000; 3.000.000 + 15% × 18.000.000 = 5.700.000; − 3.000.000 = 2.700.000 KB; PPh 25 = (5.700.000 − 3.000.000)/12 = 225.000 ✔.
