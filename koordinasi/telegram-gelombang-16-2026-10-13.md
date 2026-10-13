# Gelombang Telegram 16 — 2026-10-13 (bot kedua, Akun B)

Keputusan otomatis **63** (2026-10-13). Pra-cek: `koordinasi/pracek-telegram-g16-2026-10-13.md` (2 dari 5 calon memenuhi syarat & lolos). Penilai: agent penilai independen (bukan pembuat). Pesan: `alat-uji/pilot/msgs-g16.json` + `msgs-g16b.json`; topik: `topik-g16.json` (1403–1406) + `topik-g16b.json` (1420–1421). 6 pesan terkirim (4 + 2 ulang), semua dibalas.

**Insiden:** saat kirim pertama kedua skill target BELUM ADA di home bot kedua (salinan repo lama; 6 skill baru belum disalin), sehingga sisi DENGAN topik 1404/1406 tidak sahih (bot memakai `surat-resmi` / mencari SKILL.md lewat `find /`). Perbaikan: 6 skill disalin ke home bot, gateway restart, sisi DENGAN diulang di topik baru 1420/1421. Sisi TANPA (1403/1405) tetap sah. Pelajaran dicatat di `alat-uji/README.md`.

## Skor & verdik (TANPA = topik tanpa skill; DENGAN = ulang, skill terpasang)

| Skill (versi) | TANPA | DENGAN | Selisih | Verdik | Pembeda (satu kalimat) |
|---|---|---|---|---|---|
| ubah-draf-ke-dokumen (1.0.1) | 7 | 8 | +1,0 | **BELUM** | Tabel harga lama/baru, baris lampiran, ringkasan isi di chat — tetapi bot membaca `surat-resmi`, bukan skill target (pemicu kalah). |
| kartu-belajar-anki (1.0.1) | 7,5 | 8 | +0,5 | **BELUM** | 16 kartu utuh di chat + pratinjau + rencana 5 hari dari skrip; TANPA juga sudah membuat 10 kartu + file CSV. |

Angka dan fakta benar di semua sisi (harga 85→92 rb/250 g, robusta 60 rb, 1 Nov, 31 Okt, maks 5 bungkus, kop; 8 butir SOP). Cacat yang tercatat: surat utuh hanya di .docx (kedua sisi), nomor surat & jabatan dikarang di sisi DENGAN; blok TSV Anki kehilangan tab saat lewat Telegram (32 tab → 0) sehingga tidak bisa diimpor dengan menyalin, dan "pilih file ini" tanpa berkas.

## Keputusan (keputusan otomatis 66)

Kedua skill tetap `lulus` (uji internal LULUS), **tidak dipromosikan sebagai tampilan Telegram** dan tidak diiterasi lagi (aturan 2026-10-03 selisih < 1,5). Catatan untuk kurator bila pemilik ingin satu revisi: (a) `ubah-draf-ke-dokumen` — pertajam pemicu di `description` ("ada draf/catatan → rapikan jadi dokumen") dan persempit `surat-resmi` agar tidak merebut permintaan berawal draf; (b) `kartu-belajar-anki` — di kanal chat kirim berkas TSV/CSV sungguhan, jangan andalkan tab di teks.
