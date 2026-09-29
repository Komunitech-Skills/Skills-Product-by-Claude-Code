# Atribusi

## Jalur produksi
**Kurasi (ATM = Amati, Tiru, Modifikasi).** Skill ini mengadaptasi *struktur ide* dari skill publik
berlisensi MIT — dua "mode" kerja (periksa vs. perbaiki), prinsip menjaga suara asli penulis, dan
sebagian prinsip umum lintas bahasa (aktif > pasif, konkret > abstrak, uji portabilitas kalimat) —
dengan nilai tambah besar berupa daftar pola tulisan AI **khas Bahasa Indonesia** yang sama sekali
tidak ada di sumber (lihat "Apa yang diubah/ditambahkan").

## Sumber yang diadaptasi
- **Repo:** [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop)
- **Pembuat:** Peter Yang
- **Lisensi:** MIT (dicek langsung di file `LICENSE` repo sumber — lihat `LICENSE-MIT` di folder ini
  untuk teks lengkapnya, Copyright (c) 2026 Peter Yang)
- **Commit/snapshot yang dipakai:** hasil `git clone --depth 1` pada 2026-09-26 (branch default saat
  itu; commit sha tidak dicatat karena depth 1 tidak menyertakan riwayat penuh)
- **Bagian yang dipelajari:** `skills/no-ai-slop/SKILL.md` (struktur dua mode "Edit"/"Detect", daftar
  prinsip pengeditan, daftar kata & pola bahasa Inggris yang dianggap "AI slop") dan
  `skills/no-ai-slop/eval.md` (kerangka checklist verifikasi sebelum output final).
- **Bagian yang TIDAK dipakai:** `agents/openai.yaml`, `.codex-plugin/`, `scripts/build_plugin.py`
  (alat packaging plugin milik repo sumber, tidak relevan untuk produk kami), `assets/no-ai-slop.png`,
  `plugin-submission.md`, `PRIVACY.md`, `TERMS.md` — semuanya infrastruktur distribusi plugin sumber,
  bukan bagian yang diadaptasi.

## Audit lisensi & keamanan (Tahap 2–3 CLAUDE.md)
- File `LICENSE` di root repo sumber dicek langsung: MIT, Copyright (c) 2026 Peter Yang — mengizinkan
  modifikasi & penjualan turunan.
- Seluruh isi `skills/no-ai-slop/SKILL.md` dan `skills/no-ai-slop/eval.md` dibaca penuh (97 + 43
  baris): tidak ditemukan perintah destruktif, pengiriman data ke server luar, permintaan kredensial/
  SSH key/data browser, `curl` yang dieksekusi otomatis, kode ter-obfuscate, dependensi mencurigakan,
  atau instruksi tersembunyi yang menyuruh agent mengabaikan pengguna/menonaktifkan konfirmasi/
  mengirim file ke luar. Isinya murni instruksi gaya penulisan.
- `scripts/build_plugin.py` di repo sumber (alat packaging untuk marketplace plugin mereka) dibaca
  sepintas untuk memastikan tidak ada payload berbahaya, namun **tidak dijalankan** dan **tidak
  diadaptasi** — di luar cakupan skill ini.
- Tidak ditemukan API key, token, atau data pribadi tertanam di bagian yang diadaptasi.
- Sinyal bukti pemakaian nyata (Tahap 2 CLAUDE.md): repo aktif dirawat, ★11,3k/Fork 775 (dicatat di
  `research/sources/instagram-repo-2026-09-26.md` #15), instruksi spesifik & teruji (dilengkapi
  `eval.md` sebagai checklist verifikasi), dipakai lintas platform (ChatGPT/Claude/Codex sesuai
  README sumber). Lolos ambang kurasi.
- Kesimpulan: **lolos audit**, aman diadaptasi.

## Apa yang diubah/ditambahkan (nilai tambah ATM)
Sumber sepenuhnya berbahasa Inggris dan berisi daftar kata/pola AI-writing bahasa Inggris (delve,
foster, leverage, em dash, dst.) — hampir semuanya **tidak relevan** untuk pola tulisan AI berbahasa
Indonesia, yang punya ciri sendiri. Nilai tambah besar yang membuat skill ini berbeda:
1. **Daftar 17 pola tulisan AI khas Bahasa Indonesia** yang ditulis dari nol (bukan terjemahan pola
   Inggris): "Di era digital ini", "Mari kita simak/Yuk simak", "Tidak hanya X tetapi juga Y",
   "Menjadi kunci", "Tak bisa dipungkiri", "Semoga bermanfaat!", tiga-serangkai Indonesia
   ("cepat, mudah, dan terpercaya"), dan pola khusus terjemahan kaku Inggris→Indonesia — tidak ada
   satu pun di sumber.
2. **Konteks pasar Indonesia**: caption Instagram/TikTok, deskripsi produk marketplace, pesan WA ke
   pelanggan, email kantor, artikel blog — sumber tidak membedakan konteks/platform sama sekali.
3. **Kaitan risiko hukum periklanan**: pola klaim superlatif & weasel attribution dikaitkan ke risiko
   UU Perlindungan Konsumen (dirujuk silang ke `copy-landing-page`) — tidak ada di sumber.
4. **Script Python teruji** `scripts/cek_pola.py` (25 kasus uji termasuk input rusak: teks kosong,
   hanya spasi, hanya emoji) untuk deteksi & skor otomatis — sumber sama sekali tidak menyertakan
   script/kode, hanya instruksi teks.
5. **`references/panduan-gaya.md`** sebagai panduan gaya bersama yang bisa dirujuk skill konten lain
   di library (`konten-mingguan`, `kalender-konten-30hari`, `copy-landing-page`, `pesan-prospek-wa`,
   `balas-chat-cs`) — mekanisme integrasi lintas-skill ini tidak ada di sumber.
6. **Batasan eksplisit**: skill ini secara tegas menolak klaim "membuktikan tulisan bukan AI" atau
   "menjamin lolos AI-detector" — kejelasan batas ini ditulis baru, diperluas dari prinsip "Detect"
   sumber yang hanya menyebut "AI detectors guess" secara singkat.
7. **Contoh kasus lokal nyata** (`examples/`) dan dokumentasi pembeli awam (`README.md`) — sumber
   adalah instruksi agent untuk pengguna teknis, bukan produk siap jual ke pembeli awam.

## Pembagian lisensi bagian ini
- **Kerangka dua mode kerja (periksa/perbaiki) dan prinsip umum menjaga suara penulis** yang
  disebutkan di `SKILL.md` bagian "Langkah kerja": ide strukturnya dipelajari dari MIT
  `petergyang/no-ai-slop`, ditulis ulang penuh dalam Bahasa Indonesia dan dilokalkan — tunduk pada
  ketentuan MIT (lihat `LICENSE-MIT`).
- **Semua bagian lain** — daftar 17 pola di `references/pola-ai-indonesia.md`,
  `references/panduan-gaya.md`, `scripts/cek_pola.py`, `tests/`, `examples/`, dan `README.md` — adalah
  karya orisinal Komunitech, tidak mengandung materi pihak ketiga, dan boleh diperlakukan sebagai
  proprietary Komunitech.

Penggunaan tunduk pada `LISENSI.txt` yang disertakan dalam paket pembelian, ditambah ketentuan MIT
pada bagian yang disebut di atas.
