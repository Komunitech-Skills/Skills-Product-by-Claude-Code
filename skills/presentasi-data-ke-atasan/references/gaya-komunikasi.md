# Gaya Komunikasi: Sopan-Langsung ala Kantor Indonesia

## Prinsip
- **Kesimpulan dulu, baru penjelasan** ("piramida terbalik"): jangan menyusun cerita
  kronologis ("Bulan lalu kami mulai menganalisis... lalu ditemukan... sehingga
  kesimpulannya..."). Atasan yang sibuk berhenti membaca setelah baris pertama — baris
  itu harus sudah membawa kesimpulan.
- **Langsung tapi tidak kasar.** Sampaikan kabar buruk (omzet turun, target meleset) apa
  adanya dengan angka, tanpa menyalahkan pihak tertentu secara terbuka dan tanpa
  menutup-nutupi dengan eufemisme berlebihan ("kurang optimal" untuk "turun 23%" — sebut
  angkanya).
- **Setiap klaim harus berangka**, tidak ada kata "signifikan", "cukup besar", "lumayan"
  tanpa disertai satuan (Rp, %, unit) di sebelahnya.
- **Rekomendasi = aksi + siapa + kapan.** "Perlu ditingkatkan" bukan rekomendasi.
  "Menambah budget iklan Shopee Rp2.000.000/bulan mulai minggu depan, PIC: Admin Toko"
  adalah rekomendasi.

## Format angka (wajib konsisten)
- Rupiah: `Rp1.250.000` — simbol `Rp` menempel ke angka (tanpa spasi), pemisah ribuan
  titik, **tanpa** `,-` atau `,00` di belakang kecuali memang ada desimal berarti.
- Persen: `23%`, `-23%` untuk penurunan (tanda minus, bukan kata "minus" ditulis dua
  kali). Satu angka di belakang koma bila hasil bukan bilangan bulat (`23,4%`, pakai
  koma sebagai pemisah desimal Indonesia saat ditulis ke pembaca, meski script
  mengeluarkan titik).
- Tanggal & periode: sebutkan eksplisit ("September 2026", "1–30 Sep 2026"), jangan
  memakai "bulan ini/bulan lalu" tanpa nama bulan di badan laporan (boleh di ringkasan WA
  yang sangat singkat).
- Jangan membulatkan rupiah dengan cara berbeda antar bagian dokumen — pakai angka yang
  sama persis dengan hasil `scripts/hitung_perubahan.py` di semua format (WA/email/1
  halaman/skrip bicara) untuk topik yang sama.

## Sapaan & penutup per audiens
| Audiens | Sapaan pembuka (email) | Nada |
|---|---|---|
| Atasan langsung/pemilik usaha | "Selamat pagi/siang, Pak/Bu [Nama]," | Sopan-langsung, boleh singkat |
| Investor | "Yth. Bapak/Ibu [Nama]," atau "Dear [Nama]," bila korespondensi biasanya Inggris | Formal, data-driven, sertakan konteks strategi |
| Bank/lembaga keuangan | "Dengan hormat," | Formal, hati-hati klaim (jangan melebih-lebihkan proyeksi) |
| Klien | "Selamat pagi/siang, [Nama]," | Sopan-formal, fokus ke hasil untuk klien, bukan masalah internal |

## Hindari
- Jargon konsultan/startup: "leverage", "synergy", "low-hanging fruit", "circle back",
  "deep dive" tanpa padanan Indonesia yang jelas.
- Kalimat pembuka basa-basi panjang sebelum kesimpulan ("Berikut kami sampaikan laporan
  terkait dengan perkembangan penjualan pada periode bulan berjalan sebagaimana yang
  telah diminta sebelumnya...").
- Menyalahkan pihak eksternal tanpa data ("karena ekonomi sedang tidak bagus" tanpa
  angka makro/pembanding) — bila memang faktor eksternal, sebut secara spesifik dan
  singkat (mis. "bertepatan dengan bulan puasa, pola musiman yang juga terjadi tahun
  lalu").
