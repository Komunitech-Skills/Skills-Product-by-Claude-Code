# Pra-cek konteks Telegram: sop-onboarding 1.0.6 (2026-10-05)

Penguji independen. Alat: uji-tg.sh (`--channel telegram`, tanpa kirim), home bersih hanya skill ini. Keluaran: `scratchpad/openclaw-real/hasil/sop16-a.txt`, `sop16-b.txt`.

Pesan: "Bikinin paket onboarding buat kasir baru minimarket saya, karyawan tetap, masa percobaan 3 bulan, mulai kerja Senin 12 Oktober 2026. Gaji Rp2.800.000."

Catatan proses: percobaan b pertama (jalan bersamaan dengan a) gagal rc=1 (galat state SQLite OpenClaw, bukan masalah skill); diulang sendirian, rc=0.

Verifikasi python: 12 Okt 2026 = Senin; +29/+59/+89 hari = 10 Nov 2026 / 10 Des 2026 / 9 Jan 2027; 3 bulan = 12 Jan 2027 dikurangi 1 hari = batas 11 Jan 2027 (Senin); 6 Jan 2027 = Rabu (5 hari kerja mundur dari 11 Jan, 6 hari kerja/minggu).

## Cuplikan penting (kedua percobaan hampir identik)
- Jadwal: daftar bernomor 7 butir kronologis: 12 Okt, 19 Okt (minggu 1, digeser dari Minggu 18 Okt), 10 Nov, 10 Des, **Rabu 6 Jan 2027 evaluasi keputusan "sebelum batas masa percobaan Senin 11 Januari 2027"**, Sabtu 9 Jan (90 hari, pemantauan rutin), Senin 11 Jan (batas).
- Catatan aturan: UU 13/2003 Ps 60 jo. UU 6/2023, PP 35/2021; gaji Rp2.800.000 dibandingkan `[isian: UMK kota ... tahun 2026]`; pengecualian usaha mikro/kecil.
- Pertanyaan akhir: 3 butir (kota/UMK, nama usaha/karyawan/buddy, hari kerja & shift).

## Checklist
| | a | b |
|---|---|---|
| (a) tanpa tabel berpipa | lolos | lolos |
| (b) daftar kronologis, evaluasi 6 Jan sebelum 11 Jan, tanggal cocok python | lolos | lolos |
| (c) tanpa kata proses | catatan: tidak ada skill/script/file/path/folder; kata biasa "cek" (4x: "cek pemahaman", "cek koneksi", "cek kategori usaha") dan "tafsir" (2x: frasa yang diwajibkan SKILL.md "tafsir yang lazim dipakai") | catatan: "folder" 1x ("bukan folder bersama", konteks penyimpanan dokumen), "cek" 4x, "tafsir" 2x |
| (d) isi utuh (jadwal, SOP, BPJS, pengingat UMK) | lolos | lolos |
| (e) maks 3 pertanyaan di akhir | lolos (3) | lolos (3) |

Tidak ada kebocoran kata proses dalam arti "saya sudah cek/jalankan skill/script". Kata "cek" dipakai sebagai kata kerja sehari-hari; "tafsir" mengikuti kalimat yang ditetapkan SKILL.md.

## Skor
- a: 8,5 (isi utuh, tanggal benar, urutan jelas; pesan sambutan + pengumuman sudah ada)
- b: 8 (sama; "folder" dan "cek capaian target" sedikit bernuansa proses)

## Verdik pra-cek: LOLOS (dengan catatan)
Cacat versi 1.0.5 (tabel berpipa, kata "skill" bocor, evaluasi setelah batas) hilang di kedua percobaan. Catatan untuk pemilik: bila kriteria (c) dibaca harfiah (kata "cek"/"tafsir" dilarang), keduanya gagal; usul ringan: ganti frasa wajib "tafsir yang lazim dipakai" menjadi "perhitungan tanggal ini perkiraan lazim" dan "cek" menjadi "periksa/pastikan" di SKILL.md. Panjang balasan sekitar 7,2 ribu karakter (akan terpecah beberapa pesan Telegram, seperti g10).
