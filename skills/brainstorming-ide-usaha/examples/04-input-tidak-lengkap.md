# Uji 04 — Input tidak lengkap: "kasih ide usaha dong"

Penguji independen (Tahap 6), 2026-09-25. Jawaban pengguna disimulasikan.

## Permintaan awal

> "kasih ide usaha dong"

## Dialog (mengikuti SKILL.md apa adanya)

**Agent (klasifikasi):** "Karena ini mulai usaha dari nol, saya pakai **Jalur C (Perlu Rencana)** — saya tanya beberapa hal dulu supaya idenya cocok dengan kondisi Anda. Kalau mau cepat, bilang 'langsung kasih ide aja', nanti saya pakai asumsi umum."

**Agent (C.2, satu pertanyaan, pilihan ganda):** "Usaha ini mau dijalankan bagaimana? (a) sambilan di luar kerja, (b) full waktu, (c) belum tahu."
**Pengguna:** "a, saya karyawan."

**Agent:** "Modal yang siap dipakai untuk coba-coba kira-kira? (a) < Rp1 juta, (b) Rp1–5 juta, (c) Rp5–20 juta, (d) > Rp20 juta."
**Pengguna:** "b, sekitar 2 juta."

**Agent:** "Tinggal/berjualan di mana, dan lebih nyaman jualan online, di rumah, atau titip ke tempat lain?"
**Pengguna:** "Bekasi, perumahan. Online atau dari rumah aja."

**Agent:** "Ada keahlian/hobi atau aset yang bisa dipakai (masak, jahit, motor, desain, mengajar, dll.)?"
**Pengguna:** "Masak lumayan, istri jago bikin kue."

**Agent:** "Hasil seperti apa yang dianggap berhasil dalam 1–2 bulan pertama?"
**Pengguna:** "Nambah 1–2 juta sebulan udah seneng."

**Agent (tulis ulang pemahaman):**
> **Disebut:** karyawan, usaha sambilan, modal ±Rp2 juta, perumahan di Bekasi, jual online/dari rumah, bisa masak & istri bisa bikin kue, target tambahan Rp1–2 juta/bulan.
> **Asumsi:** dikerjakan berdua (Anda + istri), waktu luang malam & akhir pekan; tidak mengejar momen tertentu dulu (catatan: Ramadan 2027 sekitar Februari — tanggal pasti mengikuti penetapan resmi, jadi perlu dicek).
> Betul?

**Pengguna:** "Betul."

Setelah itu sesi berlanjut seperti Jalur C biasa (ide → skor → persetujuan → MVP → aksi 7 hari); tidak diulang di sini karena alur yang sama sudah diuji di skenario 01–03.

## Varian: pengguna tidak menjawab/tetap minim

> Pengguna: "terserah, pokoknya ide aja"

**Agent (prinsip instan):** "Siap, saya pakai asumsi umum: modal < Rp5 juta, paruh waktu, sendiri/dibantu 1 orang, rumahan/online, berhasil = 10 pembeli pertama dalam 1 minggu tanpa rugi. Karena saya belum tahu keahlian & lokasi Anda, ini ide yang **paling umum cocok** — hasilnya akan jauh lebih tepat kalau Anda beri tahu 3 hal: modal, keahlian, lokasi.
1. Pre-order makanan rumahan/frozen food ke tetangga & grup perumahan (uji: 10 pesanan via status WA).
2. Jasa titip belanja (jastip) dari pasar/grosir terdekat.
3. Jualan ulang (reseller) produk kebutuhan rutin dari pemasok lokal, tanpa stok besar.
4. Jasa keahlian yang sudah Anda punya (les, servis, desain, jahit) — sebutkan keahlian Anda, saya rinci.
Mau pilih satu untuk saya buatkan rencana uji 7 harinya, atau jawab 3 pertanyaan tadi dulu?"

## Catatan penguji
- Skill menangani input minim dengan benar: klasifikasi, opsi "langsung kasih ide aja", asumsi disebut, tidak mengarang data pasar.
- **Temuan (sedang):** aturan "satu pertanyaan per pesan" (warisan skill coding sumber) membuat pengguna awam menjawab **5 giliran** sebelum melihat satu ide pun. Ini bertentangan dengan prinsip rumah pedoman kurasi Komunitech §1 "Jika info kurang, tanyakan **sekali** dalam satu pesan berisi daftar pertanyaan singkat." Usul: untuk Jalur B/C, satu pesan berisi 3–5 pertanyaan pilihan ganda singkat (modal, waktu, lokasi, keahlian, target), lalu hanya tanya susulan bila jawaban ambigu.
- Ramadan 2027 disebut sebagai perkiraan dan "perlu dicek", sesuai peringatan di `references/musim-dan-momentum.md`.
