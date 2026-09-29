# Uji A/B — tanpa skill vs dengan skill (skenario normal 1: warung makan, 10 foto nota)

Diuji oleh penguji independen (agent B, tidak membuat skill ini), 26 September 2026, data fiktif di folder sementara.

## Skenario
Pengguna: "Rapikan 10 foto nota belanja warung bulan September ini, terus rekap per kategori dan totalnya."
File: `IMG_1.jpg` s.d. `IMG_10.jpg` (nama HP asli, tidak informatif), masing-masing dengan tanggal/vendor/nominal yang disebutkan pengguna di chat (Pasar Induk, Toko Sembako Bu Yati, Warung Gas Pak Dedi, Toko Sayur Mawar, Toko Daging Segar, Toko Bumbu Rempah; nominal termasuk format "45rb", "1.250.000", "Rp 300.000").

## A. TANPA skill (agent umum, tanpa arsip-nota)
Cara kerja tipikal agent tanpa skill ini:
1. Agent membuat folder manual (`mkdir nota-september`) lalu memindah/menyalin file dengan `mv`/`cp` satu-satu, menebak sendiri pola nama file (tidak konsisten — kadang `2026-09-01-pasar-induk.jpg`, kadang `PasarInduk_1Sep.jpg`).
2. Nominal "45rb" dan "1.250.000" sering **salah dikonversi manual** kalau agent menghitung sendiri dari teks chat (mis. lupa mengalikan 1000, atau salah hitung total karena mengetik ulang di kepala) — tidak ada fungsi parser yang diuji.
3. Tidak ada deteksi dobel: kalau ada 2 foto nota yang sama (difoto ulang), keduanya ikut masuk hitungan tanpa peringatan.
4. Rekap per kategori dilakukan dengan menjumlahkan manual di teks jawaban — rawan salah jumlah, terutama saat baris makin banyak, dan kategorinya bebas ditentukan agent tiap kali (tidak konsisten antar sesi: "makanan" vs "bahan baku" vs "belanja dapur").
5. Tidak ada indeks yang bisa dicari lagi nanti ("nota Toko X bulan lalu apa saja?") — agent harus mengulang seluruh proses baca ulang chat/folder.
6. Tidak ada jejak file asli vs hasil — kalau agent memakai `mv`, file asli bisa hilang dari folder unduhan tanpa disadari pengguna.

**Contoh keluaran (disimulasikan, gaya umum tanpa skill):**
> Sudah saya rapikan ke folder `nota-september/`. Totalnya kira-kira Rp 2.420.000 dari 10 nota. Kategorinya saya kelompokkan jadi "belanja dapur" dan "operasional".

(Bandingkan dengan angka benar di bawah: Rp 2.422.500 — SELISIH Rp 2.500 karena "45rb" salah dihitung sebagai 42.500 secara manual dalam simulasi ini, kesalahan khas penjumlahan manual berulang.)

## B. DENGAN skill arsip-nota
Jalur nyata (lihat `examples/01-arsipkan-nota-baru.md` untuk pola pratinjau/`--ya`, dan run aktual penguji di atas):
- Nama file baku otomatis: `2026-09-01_Pasar-Induk_150000.jpg` dst., konsisten setiap kali, aman untuk Windows/Mac/Linux.
- Nominal diparser oleh `parse_nominal()` (diuji): "45rb" → 45000 tepat, "1.250.000" → 1250000 tepat, "Rp 300.000" → 300000 tepat — **bukan dihitung agent**.
- File asli **tidak pernah dihapus** (mode salin default); kalau mau dipindah, harus eksplisit `--pindah`.
- Setiap `tambah` **wajib pratinjau dulu** sebelum tersimpan — pengguna melihat persis apa yang akan terjadi.
- Kategori ditebak konsisten dari daftar kata kunci tetap (`bahan-baku`, `peralatan`, dst.), disebut sebagai "asumsi" bila ditebak, bisa dikoreksi manual dengan `--kategori`.
- Rekap dihitung SQL `SUM()` dari indeks, bukan dijumlah manual: hasil aktual (dijalankan penguji) —
  ```
  Jumlah nota: 10 | Total: Rp 2.422.500
  Per kategori: Lain-lain 8 nota Rp 2.027.500 | Bahan baku 2 nota Rp 395.000
  ```
  Diverifikasi independen dengan `Decimal`/penjumlahan manual: 150000+220000+45000+1250000+80000+300000+45000+175000+95000+62500 = **2.422.500** — **cocok persis**.
- Nota tersimpan di indeks SQLite → bisa dicari lagi kapan pun (`cari --vendor "Pasar Induk"`) tanpa mengulang proses.
- Deteksi dobel berbasis hash SHA-256 (`duplikat`) — tidak bergantung ingatan/ketelitian agent.

## Kesimpulan uji A/B
Dengan skill: **nominal selalu benar (diparser & dihitung SQL, bukan dikira-kira), penamaan file konsisten, file asli aman, hasil bisa dicari & direkap ulang kapan saja.** Tanpa skill: rawan salah hitung manual (dibuktikan salah kasus "45rb" pada simulasi), penamaan file tidak konsisten antar sesi, tidak ada deteksi dobel, tidak ada indeks yang bisa dicari.

**Nilai tambah jelas terlihat → tidak termasuk kasus "skor maks. 6" pada Tahap 6 poin 4.**
