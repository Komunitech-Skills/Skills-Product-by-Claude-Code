# HASIL UJI - studio-video-pendek-ai v1.0.0
Penguji: agen independen (simulasi agent; BUKAN uji platform asli). Tanggal: 2026-09-29. Membaca hanya folder skill + CLAUDE.md.
Skenario: 01 laundry 15 dtk PASS; 02 klinik gigi 45 dtk PASS (tanpa klaim kesehatan); 03 hijab UGC 30 dtk PASS; 04 info kurang PASS (catatan); 05 luar cakupan (suara artis, testimoni palsu, >60 dtk, auto-post) PASS. A/B: menang jelas. Pesaing: menang untuk konteks Indonesia/keamanan/durasi, kalah kedalaman hook & konsistensi visual (pembacaan terbatas README).

## Skor: 8/10
Alasan: alur konsisten, penolakan tepat, durasi dihitung benar (28,3 / 13,5 / 36,5 / 25,0 dtk semua cocok hitung tangan; uji regresi 10/10 lulus; validate.py lolos). Dikurangi: script lolos input degenerat tanpa peringatan, verifikasi label AI belum tuntas, output berat untuk video 15 dtk.

## Script (durasi_naskah.py)
OK: kosong (rc2 pesan jelas), berkas tidak ada, biner/bukan UTF-8 (rc2), wpm 0/negatif/teks (rc2), target negatif, stdin, --json, --strict (rc1 saat melebihi), teks 100 ribu kata (0,05 dtk, benar 40000 dtk).
## Temuan
**Sedang**
1. Adegan hanya emoji/simbol dihitung 0 kata dan 0 dtk tanpa peringatan; "Hook | emoji Halo" total 1,1 dtk, status "KEPENDEKAN" - pengguna bisa mengira naskah valid. Saran: peringatan untuk adegan 0 kata.
2. Verifikasi label AI (lihat bawah): TikTok halaman bantuan resmi tidak bisa dibaca (hanya newsroom); Meta help center 404. Header label-ai.md masih "belum diverifikasi"; perbarui setelah pemilik cek manual.
**Rendah**
3. `--wpm` ekstrem (mis. 5000) diterima tanpa peringatan, padahal SKILL melarang >±170.
4. `[jeda abc]` (angka salah) tidak dikenali: "jeda abc" dihitung 2 kata dan jeda bawaan tidak berlaku.
5. Kolom tabel script melebur untuk angka besar ("0.040000.0").
6. Status "KEPENDEKAN" muncul untuk 45 dtk dengan 36,5 dtk suara, padahal wajar (ruang visual); pesannya bisa membingungkan awam.
7. SKILL tidak menjelaskan perilaku bila produk sama sekali tidak disebut dan pengguna menjawab "lanjut" (skenario 4).
8. Output 7 bagian berat untuk video 15 dtk; tawarkan mode ringkas.
9. Tema visual bersama antaradegan (jalur AI) belum ada (pesaing punya).
10. Contoh sulih suara: "dua hari" dsb harus dari pengguna; agen bisa tergoda mengisi.
**Info (lolos)**: tidak ada merek alat/artis disebut (grep bersih), tidak ada klaim posting otomatis (ditolak eksplisit), tidak ada testimoni/endorsement, bahasa Indonesia natural (kalimat pendek, angka dibaca); frontmatter deskripsi 494 karakter; uji A/B nyata.

## Verifikasi label-ai.md vs halaman resmi (2026-09-29)
- TikTok: newsroom resmi (newsroom.tiktok.com, "Partnering with our industry to advance AI transparency") COCOK: label manual untuk konten AI realistis, alat/toggle pembuat, pelabelan otomatis lewat C2PA. Kekurangan di file: TikTok juga wajib melabeli hasil efek AI bawaan TikTok dan melarang AI menyesatkan walau berlabel. Halaman support (faq_detail) tidak bisa dibaca; belum terverifikasi.
- YouTube (support.google.com/youtube/answer/14328491): COCOK: pengungkapan untuk konten realistis yang bisa disangka nyata; tidak perlu untuk non-realistis/efek; bantuan AI untuk naskah/outline/judul dikecualikan; lokasi di YouTube Studio (bagian Attributes "AI use"). Selisih: halaman tidak menyebut "Shorts" (skill menulis "YouTube (Shorts)" - wajar tapi tidak eksplisit); YouTube dapat menambah label sendiri (player untuk fotorealistis, deskripsi untuk lainnya) - tidak ada di file.
- Meta: help center 404; transparency.meta.com/about.fb.com COCOK: label "AI info" otomatis via indikator C2PA/IPTC + pengungkapan mandiri untuk posts/Reels/Stories. Frasa "label kreator AI (opsional)" tidak terverifikasi.
Ketidakcocokan yang mengubah tindakan: tidak ada. Hanya kelengkapan.
Rekomendasi: perbarui header (sebagian terverifikasi tanggal ini via sumber resmi) dan tambahkan poin di atas.

## Keputusan: LULUS bersyarat (>=7). Perbaiki 1-2 (dan 3-4 murah) lalu uji ulang script. Tidak ada temuan Kritis/Tinggi.

## Uji ulang (2026-09-29, patch) - v1.0.1 - penguji independen
Tes regresi 17/17 OK. Dicoba langsung: adegan hanya emoji/kosong -> peringatan jelas; `[jeda abc]`, `[jeda -2]`, `[JEDA 1e3]` -> jeda bawaan 0,5 + peringatan; `--wpm` 60/300 -> peringatan, 30/5000/nan -> ditolak (kode 2); jeda 40000 dtk -> kolom tabel tidak melebur; `[jeda 1,5]` = 1,5 dtk. Mode Ringkas (video <=15 dtk) ada di SKILL.md dengan bagian yang benar.
Verifikasi `references/label-ai.md` ke URL resmi (diambil ulang hari ini): YouTube 14328491 (wajib bila realistis; pengecualian naskah/judul/thumbnail/sulih suara suara sendiri; "AI use" di YouTube Studio; label otomatis; musik AI; tidak ada kata Shorts, sudah dicatat jujur), Meta about.fb.com (C2PA/IPTC; wajib ungkap video/audio realistis; sanksi), TikTok newsroom 2023 (label AIGC realistis; stiker/keterangan; efek AI berlabel) dan 2024 (Content Credentials/C2PA) - semua COCOK. Klaim "jangan menyesatkan meski berlabel" (TikTok) tidak tampak di kutipan yang saya baca; kecil, sebaiknya dilepas atau diberi sumber.
Temuan RENDAH: tabel jeda absurd tetap diterima tanpa peringatan (mis. [jeda 40000]).
**Skor: 8/10. Lulus.**
