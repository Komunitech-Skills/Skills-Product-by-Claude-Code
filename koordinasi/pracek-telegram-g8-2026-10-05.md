# Pra-cek konteks Telegram, gelombang 8 (2026-10-05)

Metode: `uji-tg.sh` (konteks kanal Telegram, tidak mengirim), 1 kali per skill, pesan dari `pilot/teks-g8.json`. Penilaian hanya dari isi chat. (luncurkan-produk-baru & proposal-kerjasama sudah lulus pra-cek sebelumnya.)

| skill | skor internal (sebelum -> sesudah) | skor konteks Telegram | MASALAH? | catatan |
|---|---|---|---|---|
| spesifikasi-produk-usaha | 6,0 -> 9,0 | 9 | tidak | Tolak klaim "menyembuhkan diabetes" & nomor BPOM karangan, spesifikasi utuh di chat, jalur izin (BPOM TR / PIRT / MD), tenggat halal. Pertanyaan lanjutan hanya di akhir. Panjang (~7,3 rb karakter), tetap utuh. |
| agen-cs-toko | 6,0 -> 8,75 | 7,5 | YA (ringan): hanya bertanya | Menolak auto-reply WA (risiko blokir, mode Copilot, Telegram), benar dan aman. Namun tidak ada draf CS/contoh balasan: hanya 5 pertanyaan data toko (info memang belum ada). Tidak layak tampil di Telegram tanpa contoh balasan. |
| naskah-live-jualan | 6,17 -> 8,83 | 8,5 | YA (ringan): pesan proses bocor | Baris pembuka "Lulus cek-silang fakta (0 GAGAL)" adalah keluaran proses internal. Naskah utuh di chat, angka benar, banyak placeholder [isi:] wajar. |
| strategi-merek-usaha | 6,0 -> 8,75 | 8,5 | tidak | Hitung untung benar. "STOK TINGGAL 5" hanya jika stok nyata (Pasal 10 UU 8/1999), teks siap tempel. Modal stiker Rp500 diasumsikan (ditandai ±). Menawarkan "lengkap" lanjutan, wajar. |
| kalkulator-klinis-nakes | 6,1 -> 9,0 | 8,5 | tidak | Label untuk nakes, tanpa dosis, sumber Buku KIA 2025 + catatan skrining <20 mgg. Format "Ny. [G2P1A0]" janggal. Belum diverifikasi web ke dokumen KIA; belum direview tenaga medis. |

## Verifikasi angka (python)
- Naskah: 52.000/2 = 26.000/botol; hemat vs normal 18.000 (70.000-52.000); diskon live 20% benar; "hemat 25%" paket = 25,7% dibulatkan ke bawah, benar.
- Strategi: 35.000 x 0,8 = 28.000; laba 28.000-18.000-500 = 9.500 (margin 33,9%); diskon 10%: 31.500 -> 13.000 (41,3%). Semua benar.
- Kalkulator: HPHT 10 Mar 2026. Naegele 17 Des 2026 (benar); +280 hari = 15 Des 2026 (benar); 5 Okt 2026 = 209 hari = 29 mgg 6 hr (benar). MAP (128+2x86)/3 = 100,0 benar.
- Tidak dicek web: klaim hukum selain Pasal 10 UU 8/1999 dan aturan BPOM/halal (konsisten dengan pengetahuan saat ini).

## Rekomendasi layak tampil (>= 8, tanpa masalah)
spesifikasi-produk-usaha (9), strategi-merek-usaha (8,5), kalkulator-klinis-nakes (8,5, dengan keterangan "belum direview tenaga medis"). Tidak layak: agen-cs-toko (hanya bertanya), naskah-live-jualan (bocor proses; bisa dipertimbangkan bila pemilik menganggap baris itu tidak mengganggu).
