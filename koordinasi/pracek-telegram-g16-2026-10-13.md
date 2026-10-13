# Pra-cek konteks Telegram — calon gelombang 16 (2026-10-13, Akun B, agent pra-cek)

Metode: `uji-tg.sh` (OpenClaw 2026.10.2, `--channel telegram` tanpa `--deliver`), satu pesan per skill, HOME hanya berisi skill itu, data fiktif ditempel di pesan. Tidak ada pesan Telegram terkirim. Syarat gelombang (keputusan 2026-10-03): `lolos_promosi` true (sesudah ≥ 8 dan selisih ≥ 1,5 pada putaran uji lengkap terakhir).

| Skill (versi) | Syarat gelombang | Pra-cek | Catatan |
|---|---|---|---|
| ubah-draf-ke-dokumen (1.0.1) | ya (5,63 → 8,28) | LOLOS | surat utuh di chat + .docx terlampir; 133 s |
| kartu-belajar-anki (1.0.1) | ya (5,75 → 8,5) | LOLOS | 19 kartu TSV utuh di chat, rencana 5 hari, cara impor; 162 s |
| broadcast-wa (1.0.12; teruji 1.0.10) | tidak (`selisih` putaran terakhir 0,9) | lolos teknis | 266 s (dekat batas 300 s); bocor kata "script" & nama berkas folder kerja |
| asisten-tulis-riset (1.0.7; teruji 1.0.5) | tidak (`selisih` 0,0; putaran terakhir 7,5 → 7,5 BELUM) | GAGAL 2× | timeout 300 s; `web_search` tidak aktif di HOME pra-cek, `web_fetch` bi.go.id timeout |
| pantau-website-toko (1.0.10; teruji 1.0.9) | tidak (`selisih` −0,15) | lolos teknis | 22 s; cek cepat jalan, tidak menjanjikan pasang monitor |

**Keputusan (lanjutan keputusan otomatis 63):** gelombang 16 = 2 skill (ubah-draf-ke-dokumen, kartu-belajar-anki), 4 pesan (sebelum + sesudah), bot kedua, topik baru. Tiga skill lain tetap `lulus` tanpa bukti bot asli (tidak dipromosikan; aturan 2026-10-03).

Catatan untuk kurator: kolom `skor_sebelum/skor_sesudah` di `promosi/sebelum-sesudah.jsonl` untuk broadcast-wa, asisten-tulis-riset, pantau-website-toko memakai putaran terbaik, sedangkan `selisih` memakai putaran lengkap terakhir — perlu diselaraskan agar tidak membingungkan (tidak tampil di halaman promosi karena `lolos_promosi` false).
