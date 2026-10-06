# 03 - Input tidak lengkap

**Input:** "bikinin landing page buat jualan saya"

**Output sesudah:**
- Run 1 (lokal): SKILL.md tidak dibaca; 7 pertanyaan (nama & deskripsi, harga, keunggulan, nomor WA, foto, warna, testimoni asli - "aku nggak akan bikin testimoni palsu").
- Run ulang (konteks Telegram): SKILL.md dibaca; 4 pertanyaan ringkas (nama usaha & produk, untuk siapa, harga - boleh kosong, nomor WA - boleh kosong).

**Catatan:** tidak ada bahan minimal, jadi bertanya dulu masih masuk akal, tetapi skill belum mengatur kasus ini (mis. memberi kerangka halaman `[isian]` + maks. 3 pertanyaan). Perbedaan dengan tanpa skill kecil (tanpa skill: 7 pertanyaan). Pemicu skill tidak konsisten untuk frasa "bikinin landing page".

## Uji ulang 1.0.1 (2026-10-06)
**Output sesudah:** "Ini kerangka halamannya, siap diisi — saya belum tahu produk/usaha Anda jadi semua bagian masih `[isian]`." lalu **kerangka `index.html` utuh** (40 `[isian: ...]`, semua bagian template; `data/hasil-sesudah-v101-s3.html`), panduan tayang singkat, checklist, lalu **tepat 3 pertanyaan**: jualan apa & nama usaha, harga, nomor WhatsApp.
- Cacat 1.0.0 (4-7 pertanyaan tanpa kerangka, skill tidak terpicu) teratasi; SKILL.md dibaca.
- Sisa: alamat ditulis `app.netlify.app/drop` (dialihkan 301 ke `app.netlify.com/drop`, tetap jalan), "langsung aktif" tanpa catatan situs sementara. Nilai 8.
