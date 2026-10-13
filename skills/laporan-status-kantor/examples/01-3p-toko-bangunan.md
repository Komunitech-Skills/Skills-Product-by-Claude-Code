# Skenario 1 (S1, normal) — 3P mingguan toko bangunan ke pemilik

## Skenario
Manajer toko bangunan kirim catatan acak lewat chat (angka penjualan, stok habis, 1
karyawan sakit, rencana promo) → minta laporan 3P mingguan ke pemilik, siap tempel WA.

## Input pengguna (persis)
> "Buatin laporan mingguan ke bos toko dong, format 3P aja. Nih catatan minggu ini:
> penjualan kira-kira 45 juta, semen abis stoknya dari hari Rabu belum sempat restock,
> si Budi anak gudang izin sakit dari Kamis sampai Senin jadi kurang orang, rencana bulan
> depan mau bikin promo cat tembok pas mulai musim kemarau. Nama tim: Toko Bangunan Jaya
> Makmur (cabang Ciputat)."

## Output (mengikuti SKILL.md, template `3p-ke-atasan-pemilik.md`, WA, sopan-formal default)

```
🧱 *Toko Bangunan Jaya Makmur (Cabang Ciputat)* — Laporan ke Bapak/Ibu Pemilik, 21–25 Sep 2026
*Progres:* Penjualan minggu ini tercatat sekitar Rp45 juta.
*Rencana:* Menyiapkan promo cat tembok untuk bulan depan, menyesuaikan mulai musim kemarau.
*Kendala:* Stok semen habis sejak Rabu dan belum direstok — mohon persetujuan Bapak/Ibu
untuk PO ke supplier. Selain itu, tim gudang kekurangan 1 orang sejak Kamis karena ada
staf yang izin sakit, sehingga proses bongkar-muat sedikit lebih lambat dari biasanya.

_Asumsi: periode laporan minggu berjalan (Senin–Jumat, 21–25 Sep 2026) karena tidak
disebutkan tanggal pasti. Dampak "bongkar-muat sedikit lebih lambat" adalah perkiraan
penulis, tidak ada di catatan Anda — hapus bila tidak sesuai. Ganti jika perlu._
```

## Catatan penguji

**Bagus:**
- Semua angka (Rp45 juta) dan fakta persis dari bahan mentah, tidak ada yang dikarang
  (satu-satunya tambahan, dampak "bongkar-muat sedikit lebih lambat", kini ditandai
  sebagai asumsi di baris Asumsi).
- Kendala dipilah tepat sesuai aturan template "ke atasan/pemilik": hanya yang butuh
  keputusan (restok semen) yang ditonjolkan; catatan kekurangan staf disertakan karena
  berdampak operasional, ditulis sebagai fakta bukan tuduhan.
- Format WA benar: `*tebal*` untuk label, satu emoji per bagian, baris pendek, tidak ada
  markdown yang rusak di WA (tidak ada `**`, tidak ada `#`).
- Asumsi periode disebutkan eksplisit di akhir sesuai instruksi Langkah 3/SKILL.md.
- Nada sopan-formal konsisten dari awal sampai akhir, sesuai default untuk laporan ke
  pemilik.

**Temuan (dibahas juga di HASIL-UJI.md):**
- **Nama karyawan ("si Budi") sengaja dihilangkan** oleh saya sebagai agen penguji dan
  diganti "staf" karena mengacu ke checklist SKILL.md: "Data sensitif karyawan ... alasan
  cuti pribadi ... tidak dicantumkan tanpa izin eksplisit". Namun **SKILL.md tidak
  memberi instruksi eksplisit** apakah nama boleh disebut ke pemilik (penerima berwenang)
  untuk laporan 3P biasa (bukan laporan insiden) — beda agen bisa membuat keputusan
  berbeda (ada yang tetap menyebut "Budi izin sakit"). Ini celah instruksi yang sebaiknya
  diperjelas di SKILL.md/template (lihat cacat SEDANG di HASIL-UJI.md).
