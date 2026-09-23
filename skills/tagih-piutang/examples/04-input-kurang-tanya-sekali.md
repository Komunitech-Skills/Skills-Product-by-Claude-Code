# 04 — Input tidak lengkap (tanya sekali)

**Skenario:** S4 — pengguna tidak memberi nama, nominal, maupun jatuh tempo.

**Input pengguna:**
> tolong tagihin pelanggan saya yang belum bayar dong, udah lama banget

## Output

Siap, saya bantu buatkan pesan penagihannya. Supaya nominal dan nadanya tepat, saya perlu beberapa info (jawab singkat saja):

1. **Siapa pelanggannya?** Nama orang/usaha (+ nama PIC kalau perusahaan).
2. **Berapa tagihannya** dan nomor invoice/nota (kalau ada)? Sudah ada yang dibayar sebagian?
3. **Tanggal jatuh temponya** kapan? (Kira-kira juga boleh, mis. "awal Agustus".)
4. **Sudah pernah diingatkan?** Kapan dan lewat apa (WA/telepon/email)?
5. **Ada denda keterlambatan yang tertulis** di kontrak/PO/invoice? Kalau tidak ada, pesan dibuat **tanpa denda**.

Kalau punya banyak pelanggan yang menunggak, kirim saja daftarnya (nama, nomor invoice, nominal, jatuh tempo, yang sudah dibayar) — saya buatkan rekap siapa yang perlu ditagih duluan.

## Catatan penguji
- Sesuai SKILL.md: tanya sekali, 5 pertanyaan; menyebut default "tanpa denda" dan menawarkan mode CSV.
- Pertanyaan ke-4 (riwayat penagihan) penting untuk memilih nada, walau SKILL.md tidak memakai jawabannya untuk menentukan tahap (lihat HASIL-UJI).
