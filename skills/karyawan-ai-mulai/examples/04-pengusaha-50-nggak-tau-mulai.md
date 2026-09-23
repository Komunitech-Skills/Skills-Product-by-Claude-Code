# 04 — Input tidak lengkap: pengusaha 50 tahun "nggak tau mulai dari mana", khawatir privasi

**Skenario:** S4 (input kurang). Kendala #1 (25 member) + #4 (17 member). Profesi dan tugas
(pertanyaan wajib) belum ada. Skill harus bertanya **sekali**, dalam satu pesan bernomor yang
singkat, tanpa jargon.

**Input pengguna (persis):**
> saya udah 50 tahun, udah pasang openclaw dibantu anak saya tapi nggak ngerti mau dipake buat apa. nggak tau mulai dari mana. terus takut juga data usaha saya bocor ke mana2

---

## Output

Tenang, Pak/Bu. Justru ini tempat yang tepat untuk mulai. Saya bantu pelan-pelan dan **tidak
akan mengubah apa pun di komputer tanpa izin Anda.**

Supaya saran saya pas, boleh jawab 5 pertanyaan singkat ini? Cukup balas dengan angka/kata
singkat. Yang tidak tahu boleh dilewati.

1. **Usaha/pekerjaan Anda apa?** (contoh: toko bangunan, rumah makan, konsultan, klinik, kantor)
2. **Berapa orang di tim Anda?**
   1️⃣ sendiri  2️⃣ 2–15 orang  3️⃣ 16–50 orang  4️⃣ lebih dari 50
3. **Tiga pekerjaan yang paling menyita waktu Anda?** (bebas, contoh: "bikin laporan jualan", "balas chat pelanggan", "nagih utang pelanggan")
4. **Anda paling nyaman dibantu lewat mana?**
   1️⃣ Telegram  2️⃣ WhatsApp  3️⃣ langsung di komputer
5. **Komputer/laptop Anda biasanya menyala terus?**
   1️⃣ ya, 24 jam  2️⃣ hanya saat kerja

Soal **data bocor**, singkatnya:
- Semua skill Komunitech berjalan **di komputer Anda sendiri**. Data usaha **tidak** dikirim ke Komunitech.
- Yang perlu Anda tahu: isi percakapan yang diproses AI dikirim ke **penyedia model AI** yang
  dipasang anak Anda (misalnya Anthropic/OpenAI/Google). Itu cara kerja semua AI.
- Setelah paket pertama siap, saya tawarkan **cek privasi** (`cek-privasi-openclaw`). Isinya
  memeriksa siapa saja yang bisa chat ke AI Anda dan apakah AI boleh menjalankan perintah tanpa
  izin, dengan laporan warna 🟢🟡🔴. Tidak ada yang diubah tanpa persetujuan Anda.

Kalau ingin langsung coba tanpa menjawab, ketik saja **"terserah"**. Saya pakai paket umum dulu
dan Anda bisa koreksi kapan saja.

---

## Catatan penguji (uji ulang v1.1.0)
- **Bagus:** satu pesan, 5 pertanyaan, pilihan bernomor, jalan pintas "terserah", dan privasi
  dijawab tanpa menjalankan audit sendiri. Di v1.1.0 skala tim sudah **4 opsi baku** (sama
  persis dengan pesan di atas), dan kanal default = **Telegram** dengan opsi WA bertanda "nomor
  terpisah, baca risikonya dulu". Isi pesan di atas sekarang sesuai skill tanpa penyesuaian
  penguji. Satu penyesuaian: opsi 4 "belum tahu/terserah" di skill dilebur ke jalan pintas
  "terserah" di akhir pesan.
- **Catatan kecil:** pertanyaan 5 di SKILL.md masih menggabungkan privasi + komputer menyala.
  Di contoh ini privasi dijawab sebagai penjelasan, cara yang lebih ramah untuk usia 50+.
