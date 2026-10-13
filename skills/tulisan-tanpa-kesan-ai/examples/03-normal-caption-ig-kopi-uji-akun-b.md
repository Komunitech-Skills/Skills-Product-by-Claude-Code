# Skenario 3 (uji independen) — Normal 1: Caption IG promo kopi penuh gaya AI

Diuji oleh agen penguji terpisah yang **hanya membaca folder skill** (SKILL.md + references), sesuai
pedoman kurasi Komunitech tahap 6.

## Input pengguna
"Tolong bikin caption promo kopi ini lebih natural, jangan kedengeran AI:
Halo teman-teman! Di tengah persaingan yang semakin ketat di dunia kopi, kami hadir dengan solusi
terbaik untuk kamu pecinta kopi sejati! ☕✨🔥 Kopi susu gula aren kami tidak hanya nikmat, tetapi juga
menggunakan biji kopi pilihan langsung dari petani lokal. Yuk simak promo spesial minggu ini — beli 2
gratis 1 — buruan sebelum kehabisan! Semoga hari kalian menyenangkan ya! 🙏"

Instruksi eksplisit "bikin lebih natural" → **mode Perbaiki** (SKILL.md tabel Input & Langkah kerja).
Konteks: caption Instagram (disebut eksplisit) → boleh santai + 1-2 emoji wajar (Langkah kerja Perbaiki #2).

## Langkah 1-2 — jalankan `scripts/cek_pola.py`
```
$ python3 scripts/cek_pola.py --teks "<draf di atas>"
Skor kebersihan pola: 75/100 (makin tinggi makin bersih)

1. Pola: Pembuka basa-basi — "Di tengah persaingan yang semakin ketat di dunia kopi, kami hadir
   dengan solusi terbaik untuk kamu pecinta kopi sejati!"
2. Pola: Kontras biner palsu — "☕✨🔥 Kopi susu gula aren kami tidak hanya nikmat, tetapi juga
   menggunakan biji kopi pilihan langsung dari petani lokal."
3. Pola: Ajakan generik — "Yuk simak promo spesial minggu ini — beli 2 gratis 1 — buruan sebelum
   kehabisan!"
4. Pola: Emoji berderet — "☕✨🔥 ..."
5. Pola: Klaim superlatif tanpa bukti — "...solusi terbaik untuk kamu pecinta kopi sejati!"

Total temuan: 5
```

**Catatan verifikasi manual (agen, sesuai Batasan SKILL.md — script bukan penentu akhir):** script
TIDAK menangkap "Semoga hari kalian menyenangkan ya! 🙏" sebagai penutup klise karena regex daftar
pola hanya cocok frasa persis ("semoga bermanfaat", dst.), bukan variasi bebas. Secara semangat pola
#9 (`references/pola-ai-indonesia.md`), ini tetap basa-basi penutup generik yang bisa ditempel ke
caption apa pun — agen menambahkannya sebagai temuan ke-6 dari pembacaan manual, bukti bahwa
verifikasi manual tetap wajib (poin ini konsisten dengan yang sudah didokumentasikan di
`examples/02-pesan-wa-follow-up.md`, jadi bukan bug baru).

Em-dash tunggal pasangan "— beli 2 gratis 1 —" (2 tanda pisah, bukan 3+) **benar tidak terdeteksi** —
sesuai pola #7 (wajar untuk menyisipkan info singkat).

## Output yang diberikan ke pengguna (mode Perbaiki)

```
✏️ Tulisan hasil perbaikan:
Halo teman-teman! Kopi susu gula aren kami dibuat dari biji kopi pilihan langsung dari petani lokal —
rasanya beda karena bijinya kami pilih sendiri. Promo minggu ini: beli 2 gratis 1, selama stok masih
ada ya. Order sekarang sebelum kehabisan! ☕

**Yang diubah:**
- Pembuka basa-basi ("Di tengah persaingan yang semakin ketat...solusi terbaik untuk kamu pecinta
  kopi sejati!") → dihapus, langsung ke fakta produk (biji kopi lokal).
- Kontras biner palsu ("tidak hanya nikmat, tetapi juga menggunakan biji kopi pilihan") → diganti
  kalimat langsung yang lebih spesifik ("rasanya beda karena bijinya kami pilih sendiri").
- Klaim superlatif tanpa bukti ("solusi terbaik untuk kamu pecinta kopi sejati") → dihapus, tidak ada
  data yang menopangnya.
- Ajakan generik ("Yuk simak promo spesial minggu ini") → diganti info promo langsung ("Promo minggu
  ini: beli 2 gratis 1").
- Emoji berderet (☕✨🔥, 3 emoji beruntun) → dipangkas jadi 1 emoji wajar (☕) sesuai konteks caption
  IG yang boleh santai tapi tidak berlebihan.
- Penutup basa-basi generik ("Semoga hari kalian menyenangkan ya! 🙏") → diganti CTA konkret ("Order
  sekarang sebelum kehabisan!") — penutup basa-basi bisa ditempel ke caption produk apa pun, CTA
  spesifik lebih sesuai konteks promo.
```

## Penilaian penguji
- Makna asli (kopi susu gula aren, biji lokal, promo beli 2 gratis 1) **dipertahankan**, tidak ada
  klaim/angka baru ditambahkan (tidak mengarang testimoni/statistik).
- Suara tetap santai khas caption IG (bukan jadi kaku/formal) — sesuai batasan "Tidak memaksa formal".
- Panjang & isi caption wajar untuk Instagram, siap tempel langsung.
- **Lulus.** Satu-satunya catatan: script melewatkan 1 pola penutup klise berbentuk variasi bebas —
  bukan cacat fatal karena SKILL.md sudah eksplisit menyebut script hanya alat bantu dan verifikasi
  manual wajib; agen tetap menangkapnya lewat pembacaan `references/pola-ai-indonesia.md`.
