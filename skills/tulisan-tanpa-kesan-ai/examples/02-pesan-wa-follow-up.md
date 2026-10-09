# Contoh 2 — Pesan WhatsApp Follow-up ke Pelanggan (B2B)

## Input pengguna
"Cek dulu pesan follow-up WA ini, kedengaran AI banget nggak?"

## Draf sebelum (ditempel pengguna)
> Selamat siang Pak Budi, semoga email ini menemukan Bapak dalam keadaan baik. Kami dari Toko Berkah
> ingin menginformasikan bahwa produk yang Bapak tanyakan menjadi solusi terbaik untuk kebutuhan usaha
> Bapak. Penelitian menunjukkan bahwa produk kami lebih unggul dibanding kompetitor. Jangan ragu untuk
> merasa bebas menghubungi kami kembali. Sekian dan terima kasih.

## Hasil `scripts/cek_pola.py` (dijalankan langsung, tidak diedit)
```
Skor kebersihan pola: 75/100 (makin tinggi makin bersih)
Catatan: heuristik pencocokan kata, bukan pendeteksi AI — baca ulang sendiri.

1. Pola: Menjadi kunci / peran penting (menjadi-kunci)
   Kutipan: "Kami dari Toko Berkah ingin menginformasikan bahwa produk yang Bapak tanyakan
   menjadi solusi terbaik untuk kebutuhan usaha Bapak."
2. Pola: Pembuka/penutup klise (penutup-klise)
   Kutipan: "Sekian dan terima kasih."
3. Pola: Klaim superlatif tanpa bukti (klaim-superlatif)
   Kutipan: "...menjadi solusi terbaik untuk kebutuhan usaha Bapak."
4. Pola: Klaim tanpa sumber (weasel-attribution)
   Kutipan: "Penelitian menunjukkan bahwa produk kami lebih unggul dibanding kompetitor."

Total temuan: 4
```

**Catatan penting soal batas script (lihat "Batasan" di SKILL.md):** script tidak menangkap
"semoga email ini menemukan Bapak dalam keadaan baik" (variasi dengan sapaan "Bapak", regex hanya
cocok kata "anda") dan "merasa bebas menghubungi kami" — keduanya adalah **pola khusus terjemahan
kaku** dari `references/pola-ai-indonesia.md`. Ini contoh nyata kenapa mode periksa tetap wajib dibaca
ulang manual oleh agent, bukan cuma mengandalkan skor script.

## Temuan tambahan dari pembacaan manual (agent, sesuai `pola-ai-indonesia.md`)
5. Pola khusus terjemahan kaku: "semoga email ini menemukan Bapak dalam keadaan baik" (dari "I hope
   this email finds you well") — tidak wajar dipakai untuk chat WA singkat.
6. Pola khusus terjemahan kaku: "merasa bebas menghubungi kami kembali" (dari "feel free to reach
   out") — kaku untuk chat WA.

## Hasil perbaikan (mode perbaiki)
> Selamat siang Pak Budi, ini Rian dari Toko Berkah. Produk yang Bapak tanyakan kemarin ready stock,
> pengiriman 1-2 hari ke area Bapak. Kalau ada pertanyaan soal harga atau cara order, langsung chat
> aja ya Pak. Ditunggu kabarnya 🙏

**Yang diubah:**
- "Semoga email ini menemukan Bapak dalam keadaan baik" → dihapus, diganti sapaan wajar untuk chat WA
  ("ini Rian dari Toko Berkah").
- "Menjadi solusi terbaik untuk kebutuhan usaha Bapak" (klaim superlatif tanpa bukti) → diganti fakta
  konkret yang relevan untuk follow-up (status stok, estimasi kirim) — bukan klaim kosong.
- "Penelitian menunjukkan bahwa produk kami lebih unggul" (klaim tanpa sumber) → dihapus sepenuhnya;
  pengguna tidak menyebut sumber penelitian apa pun, jadi tidak boleh dikarang (lihat Batasan &
  Langkah kerja #4 di SKILL.md).
- "Jangan ragu untuk merasa bebas menghubungi kami kembali" (kaku, terjemahan) → diganti "langsung
  chat aja ya Pak", lebih wajar untuk WA.
- "Sekian dan terima kasih" (penutup klise) → diganti penutup personal + emoji wajar 1x ("Ditunggu
  kabarnya 🙏"), sesuai konteks chat WA yang boleh sedikit personal (beda dari email formal).

## Catatan
Contoh ini menunjukkan konteks mengubah batas kewajaran: emoji 1x di penutup WA masih wajar (beda
dari email kantor formal), tapi klaim tanpa sumber tetap harus dihapus di konteks apa pun.
