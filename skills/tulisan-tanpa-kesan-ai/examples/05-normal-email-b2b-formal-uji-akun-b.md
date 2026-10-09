# Skenario 5 (uji independen) — Normal 3: Email Penawaran B2B Formal

Kasus ini penting karena menguji batasan "email kantor tetap sopan tapi tidak perlu jadi kaku
birokratis" (Langkah kerja Perbaiki #2) — beda dari WA/caption yang boleh santai.

## Input pengguna
"Perbaiki draf email penawaran ke klien B2B ini biar nggak kelihatan AI, tapi tetap formal dan sopan
karena ini email resmi ke manajer pengadaan:
Yth. Bapak/Ibu Manajer Pengadaan, Dalam dunia yang terus berkembang, kebutuhan perusahaan akan solusi
logistik menjadi semakin penting. Kami dari PT Maju Bersama ingin menginformasikan bahwa layanan
pengiriman kami tidak hanya cepat, tetapi juga aman dan terpercaya. Menurut para ahli, efisiensi
rantai pasok menjadi kunci daya saing perusahaan modern. Kami menyediakan layanan pengiriman ke
seluruh Indonesia dengan armada milik sendiri dan asuransi penuh untuk setiap pengiriman. Demikian
informasi yang dapat kami sampaikan, sekian dan terima kasih."

→ **mode Perbaiki**, konteks eksplisit: email kantor formal (bukan WA/caption) — sapaan resmi "Yth."
dipertahankan, bukan diubah jadi santai (ini beda penting dari skenario 3 & 4).

## Jalankan `scripts/cek_pola.py`
```
Skor kebersihan pola: 67/100 (makin tinggi makin bersih)
1. Pembuka basa-basi — "...Dalam dunia yang terus berkembang, kebutuhan perusahaan akan solusi
   logistik menjadi semakin penting."
2. Kontras biner palsu — "...layanan pengiriman kami tidak hanya cepat, tetapi juga aman dan
   terpercaya."
3. Menjadi kunci / peran penting — "Menurut para ahli, efisiensi rantai pasok menjadi kunci daya
   saing perusahaan modern."
4-5. Pembuka/penutup klise (2x match regex sama) — "Demikian informasi yang dapat kami sampaikan,
   sekian dan terima kasih."
6. Klaim tanpa sumber (weasel-attribution) — "Menurut para ahli, efisiensi rantai pasok menjadi kunci
   daya saing perusahaan modern."
Total temuan: 6
```
Catatan: temuan #4-5 sebenarnya 1 kalimat yang cocok 2 regex penutup-klise berbeda ("demikian
informasi yang dapat kami sampaikan" dan "sekian dan terima kasih" sekaligus) — bukan duplikasi salah,
memang dua frasa klise berbeda dalam satu kalimat.

## Output yang diberikan ke pengguna (mode Perbaiki)

```
✏️ Tulisan hasil perbaikan:
Yth. Bapak/Ibu Manajer Pengadaan,

Kami dari PT Maju Bersama ingin menawarkan layanan pengiriman logistik untuk kebutuhan operasional
perusahaan Bapak/Ibu. Kami mengoperasikan armada pengiriman sendiri ke seluruh Indonesia, dengan
asuransi penuh untuk setiap pengiriman.

Kami terbuka untuk menjadwalkan pertemuan guna membahas kebutuhan pengiriman perusahaan Bapak/Ibu
lebih lanjut.

Hormat kami,
PT Maju Bersama

**Yang diubah:**
- Pembuka basa-basi ("Dalam dunia yang terus berkembang, kebutuhan perusahaan akan solusi logistik
  menjadi semakin penting") → dihapus, langsung ke inti penawaran.
- Kontras biner palsu ("tidak hanya cepat, tetapi juga aman dan terpercaya") → dihapus karena tidak
  ada bukti pendukung khusus untuk klaim itu; diganti fakta konkret yang memang sudah kamu sebutkan
  (armada sendiri, asuransi penuh).
- Klaim tanpa sumber ("Menurut para ahli, efisiensi rantai pasok menjadi kunci daya saing") → dihapus
  sepenuhnya. Kamu tidak menyebut sumber "para ahli" mana, jadi tidak boleh dikarang atau dipertahankan
  (lihat Batasan & Langkah kerja #4 SKILL.md) — kalau ada studi/data spesifik yang mau dicantumkan,
  kasih tahu saya, saya masukkan dengan sumber yang jelas.
- Penutup klise ("Demikian informasi yang dapat kami sampaikan, sekian dan terima kasih") → diganti
  ajakan konkret untuk tindak lanjut (jadwalkan pertemuan) + salam penutup formal standar surat bisnis
  ("Hormat kami") — tetap formal/sopan sesuai konteks email resmi, BUKAN dibuat santai seperti caption/WA.
- Sapaan pembuka "Yth. Bapak/Ibu Manajer Pengadaan," dipertahankan apa adanya — ini bukan pola AI,
  memang format surat resmi Indonesia yang wajar.

Catatan: saya tidak menambahkan klaim baru (mis. testimoni, jumlah klien, angka on-time delivery)
karena tidak ada di draf asli kamu — kalau mau dicantumkan, kasih tahu angka/faktanya dulu.
```

## Penilaian penguji
- Nada tetap **formal & sopan**, TIDAK dijadikan santai — sesuai instruksi eksplisit pengguna dan
  Langkah kerja Perbaiki #2 (email kantor tetap sopan).
- Hasil juga **tidak jadi lebih kaku/birokratis** dari draf asli — justru mengurangi basa-basi
  ("Demikian informasi yang dapat kami sampaikan" itu sendiri birokratis, dihapus, bukan ditambah).
  Sesuai Batasan "Tidak memaksa formal": tujuannya menghilangkan klise, bukan menambah kekakuan baru.
- Tidak mengarang klaim "para ahli"/data efisiensi — dihapus dan diberi keterangan ke pengguna kenapa,
  sesuai Langkah kerja Perbaiki #4.
- Format output sesuai spesifikasi (tulisan lengkap + "Yang diubah" per pola, bukan diff baris).
- **Lulus.** Ini skenario paling ketat menguji "jangan dibuat kaku" karena originalnya sudah formal —
  hasil skill berhasil membedakan "formal yang memang perlu" vs "basa-basi birokratis yang dibuang".
