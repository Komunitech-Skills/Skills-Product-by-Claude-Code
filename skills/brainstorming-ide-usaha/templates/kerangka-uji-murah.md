# Kerangka Uji Murah (MVP Ide Usaha)

Dipakai di Langkah Kerja B.6/C.8 SKILL.md untuk merancang uji coba ide sebelum dieksekusi penuh. Isi tiap bagian dengan konkret, bukan kalimat umum.

## 1. Cara uji (pilih yang paling murah & cepat dulu)
Contoh cara uji dari paling murah ke lebih besar — pilih yang paling murah yang masih bisa menjawab pertanyaan intinya:
- **Pre-order via status/story WA atau Instagram** — tawarkan ide ke kontak/follower yang ada, hitung berapa yang serius mau pesan (bukan cuma "like").
- **Tawarkan langsung ke pelanggan tetap** (bukan pasar umum dulu) — lebih cepat dapat jawaban jujur.
- **Produksi kecil, jual terbatas** (mis. 10–20 pcs) di satu kanal saja sebelum produksi massal.
- **Survei singkat 3–5 pertanyaan** ke pelanggan/kontak (harga yang mau dibayar, seberapa sering butuh) — hanya kalau butuh info sebelum berani jual, jangan jadi pengganti benar-benar mencoba jual.

## 2. Durasi
Default: **1 minggu** kalau tidak ditentukan pengguna. Sebutkan tanggal mulai & selesai kasar (mis. "mulai besok, evaluasi 7 hari kemudian").

## 3. Target ukuran berhasil (harus angka, bukan perasaan)
Default kalau tidak disebutkan: **minimal 10 pelanggan/pesanan** dalam durasi uji, **tanpa rugi** (harga jual uji ≥ modal + biaya yang jelas). Sesuaikan angka dengan skala usaha pengguna — untuk usaha yang baru dari nol, 10 mungkin sudah bagus; untuk usaha yang sudah punya ribuan follower, mungkin perlu target lebih tinggi supaya berarti.

## 4. Kapan berhenti / kapan lanjut
Tentukan sebelum mulai uji, bukan sesudah (supaya keputusan tidak bias karena "sudah terlanjur"):
- **Lanjut/perbesar** jika: target ukuran berhasil tercapai (100%) DAN tidak ada keluhan besar berulang.
- **Perbaiki dulu, uji ulang** jika: hasil **30–99% dari target** (mis. 3–9 dari target 10) atau ada 1–2 keluhan yang jelas bisa diperbaiki (harga, rasa, kemasan) meski target tercapai.
- **Hentikan/ganti ide** jika: hasil **di bawah 30% dari target** (mis. <3 dari target 10) atau keluhan mendasar yang sulit diperbaiki tanpa mengubah ide itu sendiri.

(Ketiga ambang ini saling berurutan tanpa celah: 0–29% berhenti, 30–99% perbaiki, 100%+ lanjut — sesuaikan angka target sendiri dengan proporsi yang sama.)

## 5. Biaya uji (agar tidak rugi besar di tahap coba-coba)
Sebutkan perkiraan biaya maksimal yang rela dikeluarkan untuk uji ini (bagian dari modal yang disebutkan di Input) — jangan biarkan uji coba menghabiskan seluruh modal yang sebenarnya disiapkan untuk produksi penuh.

## 6. Hitungan rupiah & tabel Rencana Uji 7 Hari (wajib di balasan kedua)
Hitung dulu: `python3 scripts/skor_ide.py rencana --harga <jual/unit> --modal-unit <modal/unit> --potongan-persen <komisi aplikasi; 0 via WA> --biaya-uji <total 7 hari> --target <unit> --harga-lama <harga sendiri/satuan> --harga-pesaing <harga pesaing/satuan>` (harga baru: ganti `--harga` dengan `--margin-target <persen>`; paket: tambah `--isi-per-unit <n> --satuan <kg/porsi>`). Cek kewajaran harus WAJAR, atau jelaskan nilai tambahnya; tanpa acuan pasar tulis `[isi: harga pesaing per satuan]`.

| Hari | Tugas konkret | Target angka | Biaya (Rp) |
|---|---|---|---|
| 1 | Siapkan penawaran + foto/daftar harga; kirim ke N kontak pelanggan lama via WA (satu per satu) | N pesan, ≥X balasan | … |
| 2 | Pasang di status WA/IG + 1–2 grup lokal (izin admin); buka PO dengan DP/QRIS | ≥Y peminat | … |
| 3 | Layani pesanan pertama; catat keluhan. **Berhenti dini:** masih 0 → ganti tawaran/kanal | kumulatif ≥ angka "Hari 3" script | … |
| 4 | Perbaiki 1 hal dari keluhan; minta testimoni | ≥1 testimoni | … |
| 5 | Ulangi penawaran ke kontak yang belum membalas / titip jual. **Berhenti dini:** di bawah ambang "Hari 5" script → hentikan, hemat sisa biaya | kumulatif ≥ angka "Hari 5" script | … |
| 6 | Dorong momen (Jumat/gajian/weekend) | … | … |
| 7 | Rekap & putuskan dengan ambang dari script (lanjut/perbaiki/hentikan) | kumulatif ≥ target | Rp0 |

Total kolom biaya = `--biaya-uji`. Ganti contoh tugas sesuai ide; setiap baris wajib punya angka.

**Tanda bahaya (pre-mortem):** 2 alasan paling mungkin gagal + sinyal awal yang dipantau Hari 1–3.
