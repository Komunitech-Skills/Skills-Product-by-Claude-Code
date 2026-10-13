# Balas Chat Pelanggan Cepat, Ramah, Minim Salah Janji

**Tempel chat pelanggan, dapat balasan siap kirim yang menenangkan dan menyelesaikan masalah.**

*Diuji AI penguji independen di OpenClaw: 6,4 → 8,8 dari 10 pada uji ulang v1.0.5 (13 Okt 2026; uji pertama 6,5 → 8,25; skenario klinik gigi 5,9 → 9,0) (pembedanya: tanpa skill AI mengarang voucher dan diskon yang tidak pernah Anda tawarkan dan mengabaikan kata "mau balikin"; dengan skill balasan hanya memakai kebijakan toko yang Anda berikan dan permintaan refund pembeli ditanggapi).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Balasan pertanyaan stok, ongkir, cara order, dan pembayaran langsung dibuatkan, tinggal Anda baca dan kirim
- ✅ Komplain barang rusak, telat, atau salah kirim ditangani dengan alur minta maaf, beri solusi, lalu tindak lanjut
- ✅ Bisa membuat "bank jawaban" 15–30 template balasan cepat (quick reply) dari info toko Anda
- ✅ Nada menyesuaikan brand: santai, ramah, atau formal
- ✅ Dirancang agar tidak mengarang stok, ongkir, atau kebijakan retur dan tidak menjanjikan hal yang belum Anda setujui (bagian yang belum diketahui ditandai `[isi ...]`). Tetap baca draf sebelum mengirim; pada uji masih ada satu kalimat atas nama toko yang lolos

## Cocok untuk siapa
- Pemilik online shop dan admin CS di WhatsApp, Shopee, Tokopedia, atau TikTok Shop
- Usaha kuliner, fashion, skincare, dan jasa yang chat-nya ramai setiap hari
- Pemilik usaha yang ingin admin baru langsung bisa membalas dengan standar yang sama
- Klinik atau praktik kecil: untuk chat pasien, skill hanya menyiapkan draf tanpa dosis dan tanpa diagnosis, serta mengarahkan ke dokter dan menyebut tanda bahaya (IGD/119). Aturan medis ini belum direview tenaga medis, jadi gunakan sebagai draf dan tinjau oleh tenaga medis Anda sebelum dikirim.

## Contoh sebelum & sesudah
**Sebelum:** Pembeli kecewa karena barang tidak sesuai, admin panik dan membalas "maaf kak, nanti dicek". Atau AI biasa menjawab rapi, tetapi mengabaikan kata "mau balikin" dan menjanjikan hal yang tidak pernah Anda tawarkan.

**Sesudah (cukup ketik):** "Tolong bikinin balesan chat buat toko sepatu anak aku "Langkah Kecil" di Shopee. Pembeli chat: "Min sepatu ukuran 28 yg dateng kekecilan, padahal udah ikutin size chart!! Kecewa bgt, mau balikin aja." Kita bisa tukar ukuran, tapi ongkir tukarnya ditanggung pembeli." Cuplikan jawaban asli (dipotong) dari uji otomatis di OpenClaw, 1 Okt 2026:
```
**Balasan (siap kirim):**
Hai Kak, mohon maaf banget ukuran 28 yang sampai ternyata kekecilan, padahal sudah ikutin size chart ya 🙏 Pasti bikin kecewa, kami ngerti.

Untuk solusinya, kami bisa bantu tukar ke ukuran yang lebih pas. Catatannya, ongkir tukar nanti ditanggung dari Kakak ya. Soal "mau balikin", boleh dikonfirmasi dulu maksudnya tukar ukuran atau refund (pengembalian dana)? ...

**Catatan untuk admin:**
- Pelanggan minta "balikin" (bisa berarti refund) — ini di luar kebijakan tukar yang Kakak kasih, jadi di balasan diarahkan ke fitur Pengembalian Shopee, bukan dijanjikan refund langsung. ...
- Isi jam/waktu tindak lanjut di bagian `[isi: ...]` sebelum dikirim, sesuai jam operasional toko.
```

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Balas chat ini: 'kak paketku udah 5 hari belum sampe'"
- "Buatin bank jawaban CS untuk toko sambal kemasan, kirim pakai JNE & SiCepat, bayar transfer BCA & QRIS"
- "Bikin auto reply WA di luar jam kerja, toko buka Senin–Sabtu 08.00–17.00"

## Instalasi singkat
Salin folder `balas-chat-cs` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

**Hasil uji (angka nyata):**
- **Uji OpenClaw, uji ulang v1.0.3, 1 Oktober 2026** (penguji AI independen; angka dari `examples/00-openclaw-sebelum-sesudah.md`, dua skenario): rata-rata nilai 6,5 tanpa skill menjadi 8,25 dengan skill (skala 10). Tanpa skill, AI mengarang voucher toko, gratis ongkir, dan diskon yang tidak pernah Anda tawarkan; dengan skill, balasan hanya memakai kebijakan toko yang Anda berikan, menanggapi permintaan refund pembeli, dan menandai bagian yang perlu Anda konfirmasi.
- Uji pertama (sebelum perbaikan) belum lulus: 6,75 menjadi 7,75, karena masih ada janji karangan atas nama toko. Pada uji ulang masih ada satu kalimat atas nama toko yang tidak Anda berikan ("harga di etalase sudah harga pas"), jadi baca draf sebelum mengirim. Aturan chat pasien klinik (ditambahkan setelah uji ini) tidak termasuk dalam angka di atas.

- **Uji ulang v1.0.5, 13 Okt 2026** (OpenClaw 2026.10.2, penguji independen, pesan identik dengan uji pertama): toko online tanpa skill **6,4** → dengan skill **8,8**; klinik gigi tanpa skill **5,9** → dengan skill **9,0** (LULUS). Dengan skill hanya kebijakan toko yang dipakai, keputusan refund ditandai [KEPUTUSAN PEMILIK], balasan klinik tanpa diagnosis dan tanpa dosis obat serta menyebut IGD/119; tanpa skill ada janji "tanpa biaya tambahan", kata "mau balikin" diabaikan, dan untuk klinik AI menebak abses dan menyarankan paracetamol. Catatan: tanda [KEPUTUSAN PEMILIK] baru muncul di catatan admin, belum di draf balasan.

**Status uji (jujur):** diuji di OpenClaw (uji otomatis agent) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama).

## FAQ
**Apa bedanya dengan skill balas ulasan?**
Skill ini untuk chat pribadi dengan pelanggan (WA atau chat marketplace). Untuk membalas ulasan bintang yang tampil publik, pakai skill `balas-ulasan-pelanggan` (khusus balasan ulasan).

**Apakah bisa langsung terhubung ke WhatsApp atau Shopee saya?**
Tidak terhubung otomatis. Anda menempelkan chat-nya, lalu menyalin balasan yang dibuat. Skill ini tidak mengirim data toko Anda ke mana pun (isi chat yang Anda tempel tetap diproses layanan AI yang Anda pakai, seperti biasa).

**Bagaimana kalau info toko saya belum lengkap?**
Balasan tetap dibuat, dengan bagian `[isi ...]` yang tinggal Anda lengkapi, misalnya estimasi restok atau nomor rekening.

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
