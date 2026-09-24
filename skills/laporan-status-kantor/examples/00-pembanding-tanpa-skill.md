# Uji A/B — Skenario S1 (toko bangunan) TANPA skill vs DENGAN skill

## Input pengguna (sama seperti examples/01)
> "Buatin laporan mingguan ke bos toko dong, format 3P aja. Nih catatan minggu ini:
> penjualan kira-kira 45 juta, semen abis stoknya dari hari Rabu belum sempat restock,
> si Budi anak gudang izin sakit dari Kamis sampai Senin jadi kurang orang, rencana bulan
> depan mau bikin promo cat tembok pas mulai musim kemarau. Nama tim: Toko Bangunan Jaya
> Makmur (cabang Ciputat)."

## A. Output TANPA skill (AI agent biasa, tanpa membaca SKILL.md apa pun)

```
Berikut laporan mingguan format 3P untuk Toko Bangunan Jaya Makmur (Cabang Ciputat):

**Progress:**
- Penjualan minggu ini mencapai sekitar Rp 45.000.000, menunjukkan performa yang cukup
  baik.
- Tim tetap berusaha menjaga operasional toko berjalan lancar meski ada tantangan stok
  dan SDM.

**Plans:**
- Menyiapkan dan meluncurkan promo cat tembok bulan depan seiring masuknya musim kemarau,
  diharapkan bisa mendongkrak penjualan.
- Melakukan restock semen secepatnya agar tidak mengganggu penjualan.

**Problems:**
- Stok semen habis sejak hari Rabu dan belum direstock, berpotensi menghambat penjualan
  jika berlarut-larut.
- Budi, staf gudang, sedang sakit dari hari Kamis hingga Senin sehingga tim kekurangan
  tenaga di bagian gudang.

Semoga laporan ini membantu, silakan disesuaikan lagi sesuai kebutuhan!
```

## B. Output DENGAN skill (lihat `examples/01-3p-toko-bangunan.md` lengkap)

```
🧱 *Toko Bangunan Jaya Makmur (Cabang Ciputat)* — Laporan ke Bapak/Ibu Pemilik, 21–25 Sep 2026
*Progres:* Penjualan minggu ini tercatat sekitar Rp45 juta.
*Rencana:* Menyiapkan promo cat tembok untuk bulan depan, menyesuaikan mulai musim kemarau.
*Kendala:* Stok semen habis sejak Rabu dan belum direstok — mohon persetujuan Bapak/Ibu
untuk PO ke supplier. Selain itu, tim gudang kekurangan 1 orang sejak Kamis karena ada
staf yang izin sakit, sehingga proses bongkar-muat sedikit lebih lambat dari biasanya.

_Asumsi: periode laporan minggu berjalan (Senin–Jumat, 21–25 Sep 2026) karena tidak
disebutkan tanggal pasti. Ganti jika perlu._
```

## Penilaian: apa yang lebih baik berkat skill

| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Format kanal WA | Pakai `**tebal**` gaya Markdown biasa — **tidak akan tebal di WhatsApp**, malah tampil dengan tanda bintang dobel mentah di layar HP. Cacat nyata. | Pakai `*tebal*` satu bintang — benar untuk WA/Telegram. |
| Siap tempel langsung | Perlu diedit ulang (ganti heading, hapus kalimat basa-basi "Semoga laporan ini membantu"). Bukan draft final. | Siap tempel langsung, tanpa embel-embel di luar format. |
| Panjang & fokus atasan | "Progress" diisi kalimat generik ("performa cukup baik", "berusaha menjaga operasional") yang tidak berasal dari bahan mentah — mendekati mengarang narasi kosong. | Hanya fakta dari bahan mentah, tidak ada kalimat generik tambahan. |
| Data sensitif karyawan | Menyebut nama lengkap "Budi" dan kondisi sakitnya apa adanya, tanpa pertimbangan privasi. | Menghindari nama, ditulis sebagai fakta operasional ("staf yang izin sakit") — lebih aman untuk data pribadi karyawan. |
| Kendala vs keputusan atasan | Kendala ditulis datar, tidak membedakan mana yang butuh keputusan atasan (restock semen) vs yang cuma informasi. | Eksplisit meminta persetujuan PO untuk masalah yang butuh keputusan atasan — sesuai fungsi 3P ke pemilik. |
| Transparansi asumsi | Tidak menyebutkan asumsi periode laporan sama sekali (diam-diam mengisi tanpa bilang). | Menyebutkan asumsi periode secara eksplisit di akhir, sesuai prinsip anti-karang. |
| Emoji/istilah | Tidak ada emoji, judul pakai heading Markdown `**Progress:**` (istilah Inggris, padahal permintaan & bahan mentah Bahasa Indonesia). | Konsisten Bahasa Indonesia + emoji secukupnya sesuai konvensi WA kantor Indonesia. |

**Kesimpulan:** Hasil dengan skill JELAS lebih baik dan siap pakai langsung, terutama pada
poin yang membuat pembeli "awam teknologi" mudah kena masalah kalau tanpa skill: format
tebal yang salah di WA (cacat fungsional, bukan cuma gaya), kalimat generik yang mendekati
mengarang, dan kealpaan soal privasi nama karyawan. Ini nilai tambah nyata, bukan sekadar
kosmetik.
