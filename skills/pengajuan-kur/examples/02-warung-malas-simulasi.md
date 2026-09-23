# 02 — "Bikinin dong" simulasi KUR warung sembako (cicilan terlalu berat)

**Skenario:** S2 — permintaan singkat/malas, pengguna hanya ingin simulasi. Fiktif.

**Input pengguna (persis):**
> bikinin dong simulasi kur 25jt 2 thn, laba warung sembako aku 4jt sebulan, masih nyicil motor 1,2jt

Perintah:
```bash
python3 scripts/simulasi_kur.py --plafon 25jt --tenor 24 --kur --sektor perdagangan --akad-ke 1 \
  --penggunaan modal-kerja --laba-bersih 4jt --cicilan-lain "1,2 juta"
```
(Asumsi disebut ke pengguna: KUR pertama, untuk modal kerja/stok.)

## Output (mengikuti SKILL.md)

## Simulasi KUR — Warung Sembako
⚠️ Bunga **6% efektif/tahun = ACUAN Permenko Perekonomian 1/2026 Pasal 37** (KUR Mikro, sektor perdagangan, **akad pertama**) — konfirmasi ke bank penyalur. *Asumsi saya: ini KUR pertama Anda dan dipakai untuk stok (modal kerja).*

| Rp 25.000.000, 24 bulan | Anuitas (efektif) — berlaku untuk KUR | Flat 6% (ilustrasi) |
|---|---:|---:|
| Cicilan/bulan | **Rp 1.108.015** | Rp 1.166.667 |
| Total bunga | Rp 1.592.366 | Rp 3.000.000 |
| Total dibayar | Rp 26.592.366 | Rp 28.000.000 |

Bunga flat yang setara 6% efektif untuk 24 bulan hanya ±3,18%/tahun — kalau bank menyebut "flat 6%", tanyakan.

### Kemampuan bayar
Laba Rp 4.000.000/bulan, cicilan motor Rp 1.200.000 + cicilan KUR Rp 1.108.015 = **Rp 2.308.015 (57,7% dari laba) → 🔴 TERLALU BERAT.** Sisa laba hanya Rp 1.691.985/bulan, dan itu belum dikurangi kebutuhan rumah tangga.

🔴 **Saran tegas:** dengan cicilan motor yang sudah 30% dari laba, **tidak ada ruang cicilan baru di batas aman 30%** (plafon maks aman = Rp 0). Pilihan yang lebih aman:
1. Tunggu cicilan motor lunas, lalu ajukan lagi (di laba 4 jt, plafon aman 24 bulan ± Rp 27 juta tanpa cicilan lain).
2. Ajukan jauh lebih kecil, mis. KUR Super Mikro ≤ Rp 10 juta (bunga acuan 3%), dan pastikan tambahan stok benar-benar menaikkan laba.
3. Rapikan pencatatan laba dulu — bank juga akan menilai kemampuan bayar (Pasal 35 ayat 3).

Info penting untuk warung (perdagangan non-ekspor): KUR Mikro hanya boleh **2 kali akad**, dan akad kedua bunganya 7% (Pasal 36 ayat 3, Pasal 37). Plafon ≤ Rp100 juta: bank tidak boleh minta agunan tambahan (Pasal 20).

Mau saya lanjutkan dengan checklist dokumen & profil usaha untuk diajukan nanti?

Catatan: Simulasi ini bukan penawaran atau jaminan persetujuan kredit. Keputusan & angka final ada di bank. Dasar: Permenko 1/2026 (dicek 2026-09-23).

## Catatan penguji
- ✅ Pengguna minta "simulasi" saja → skill cukup plafon, tenor, laba (sesuai bagian Input); asumsi akad & penggunaan disebut.
- ✅ Diverifikasi independen: anuitas 1.108.015,26; rasio (1.108.015+1.200.000)/4.000.000 = 57,7%; plafon maks 0 karena 30%×4 jt − 1,2 jt = 0 — cocok. Angka "± Rp 27 juta" dihitung agent dengan rumus fallback SKILL.md (1.200.000 × (1−1,005^−24)/0,005 = Rp 27,07 jt) — sebaiknya script juga memberi skenario "tanpa cicilan lain".
- ✅ Peringatan tegas + alternatif konkret sesuai langkah 3.
- ➖ `plafon_maks = 0` tanpa penjelasan di output script; agent harus menerangkan sendiri.
