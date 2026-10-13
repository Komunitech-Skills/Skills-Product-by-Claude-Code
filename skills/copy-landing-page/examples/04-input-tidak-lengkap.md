# Skenario 04 (Input tidak lengkap) — "Bikinin halaman jualan dong"

## Permintaan pengguna
> "Bikinin halaman jualan dong."

Tidak ada info produk sama sekali — bukan cuma "kurang lengkap", tapi **tidak ada satu pun** dari 7 poin Input di SKILL.md yang terjawab.

## Perilaku yang diharapkan (sesuai SKILL.md)
SKILL.md Langkah "Kalau info kurang": *"tanyakan SEKALI dalam satu pesan berisi daftar poin di atas yang belum terjawab."* Instruksi ini ditulis untuk kasus **sebagian** info kurang (lihat contoh keripik pedas di skenario 01, yang sudah punya produk & harga). Untuk kasus **tanpa info produk sama sekali**, SKILL.md tidak punya cabang instruksi terpisah — agent harus tetap memakai pola "satu pesan berisi daftar pertanyaan", plus wajib menyertakan pertanyaan paling dasar (produk/jasa apa) yang justru tidak ada di kasus lain.

## Output agent (simulasi)
> "Boleh! Sebelum saya buatkan, boleh dijawab dulu (yang kamu tahu saja, sisanya saya pakai default):
> 1. Produk/jasa apa yang mau dijual, dan buat siapa?
> 2. Harga, ada diskon asli (harga sebelumnya benar-benar pernah berlaku)?
> 3. Masalah/keinginan apa yang diselesaikan buat pembeli?
> 4. Nomor WhatsApp untuk tombol pesan, cara bayar (transfer/COD/QRIS), area kirim/ongkir?
> 5. Ada testimoni pelanggan asli yang mau ditampilkan?
> 6. Nada: santai, profesional, atau 'bahasa ibu-ibu'?
> 7. Formatnya: landing page lengkap, halaman produk website, atau versi pendek link-in-bio?
>
> Kalau kamu belum tahu produknya secara detail, minimal kasih tahu dulu jualan apa ya — bagian lain saya bisa pakai default (nada santai-profesional, bayar transfer & QRIS, tanpa testimoni dulu)."

**Tidak** mencoba mengarang produk generik ("Produk Berkualitas Terbaik untuk Semua Kebutuhan Anda") hanya supaya ada output — ini sesuai prinsip "Powerful: hasil langsung siap pakai" di `pedoman kurasi Komunitech` dan "Hindari headline generik" di `references/struktur-halaman.md`.

## Uji lanjutan: pengguna menjawab minimal
> "Oh iya lupa, jual jasa titip beli oleh-oleh khas Bandung, harga jasa 15% dari total belanja."

Agent lanjut membuat halaman dengan default untuk poin yang masih kosong (WA → placeholder `[NOMOR WA KAMU]`, tanpa testimoni, nada santai-profesional), dan **menyebutkan asumsi tersebut secara eksplisit di bagian 7 (Asumsi)** sesuai Format Output — termasuk peringatan mengganti placeholder nomor WA sebelum publish (Langkah kerja #9).

## Verifikasi
- Placeholder `[NOMOR WA KAMU]` dipakai persis seperti yang diinstruksikan di Input poin "Kalau info kurang" — bukan nomor palsu yang terlihat asli (risiko: pengguna lupa mengganti dan pembeli chat ke nomor tidak valid). Karena ini placeholder teks eksplisit dalam kurung siku, risiko salah kirim rendah, tapi tetap dicatat sebagai hal yang wajib diganti (Langkah 9), yang memang dilakukan.
- Tidak ada tombol wa.me yang dibuat dari nomor kosong/placeholder (script `bangun_tautan_wa.py` akan **gagal** — `InputSalah: nomor WhatsApp kosong` — kalau dipaksa jalan dengan placeholder ini, jadi agent yang patuh tidak akan menjalankan script untuk kasus ini, hanya menulis placeholder mentah). Diverifikasi:
  ```
  $ python3 scripts/bangun_tautan_wa.py wa --nomor "[NOMOR WA KAMU]" --pesan "test"
  Input tidak valid: nomor '[NOMOR WA KAMU]' tidak terlihat seperti nomor HP yang valid (harus angka, 8-15 digit setelah tanda dibuang)
  ```
  Ini perilaku yang **benar** (gagal jelas, bukan membentuk tautan `wa.me/[NOMOR WA KAMU]` yang rusak) — tapi SKILL.md tidak secara eksplisit menginstruksikan "jangan jalankan script kalau nomor masih placeholder", hanya bisa disimpulkan dari sifat script. Agent yang kurang hati-hati berisiko mencoba menjalankannya dan bingung dengan pesan error, atau (lebih buruk) menulis tautan `https://wa.me/[NOMOR WA KAMU]` mentah ke output tanpa sadar itu tidak valid. **Dicatat sebagai temuan rendah** di HASIL-UJI (lihat R-temuan).

## Penilaian
**Lulus.** Alur "satu pertanyaan" tetap dipakai walau info produk nol sama sekali, tidak mengarang produk generik, memakai default + placeholder sesuai instruksi, dan mengingatkan penggantian placeholder di akhir. Satu celah instruksi kecil ditemukan (lihat R-temuan di atas) terkait tidak ada arahan eksplisit soal urutan "jangan jalankan script wa.me kalau nomornya masih placeholder" — berisiko rendah karena error script cukup jelas.
