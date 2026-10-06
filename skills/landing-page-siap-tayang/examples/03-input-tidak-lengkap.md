# 03 - Input tidak lengkap

**Input:** "bikinin landing page buat jualan saya"

**Output sesudah:**
- Run 1 (lokal): SKILL.md tidak dibaca; 7 pertanyaan (nama & deskripsi, harga, keunggulan, nomor WA, foto, warna, testimoni asli - "aku nggak akan bikin testimoni palsu").
- Run ulang (konteks Telegram): SKILL.md dibaca; 4 pertanyaan ringkas (nama usaha & produk, untuk siapa, harga - boleh kosong, nomor WA - boleh kosong).

**Catatan:** tidak ada bahan minimal, jadi bertanya dulu masih masuk akal, tetapi skill belum mengatur kasus ini (mis. memberi kerangka halaman `[isian]` + maks. 3 pertanyaan). Perbedaan dengan tanpa skill kecil (tanpa skill: 7 pertanyaan). Pemicu skill tidak konsisten untuk frasa "bikinin landing page".
