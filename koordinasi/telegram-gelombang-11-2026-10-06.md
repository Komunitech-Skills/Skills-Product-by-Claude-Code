# Gelombang Telegram 11 — 2026-10-06 (percobaan 1 GAGAL, menunggu keputusan no. 21)

Disetujui pemilik (keputusan no. 20, chat "setuju 16 18 19a 20"). Skill: rapikan-data-berantakan, aktifkan-kembali-pelanggan, triase-keluhan-pelanggan, tangani-keberatan-pelanggan, kelayakan-investasi-usaha. Topik G11: 900/901, 902/903, 904/905, 906/907, 908/909 (TANPA/DENGAN). Backup skill bot: `skills-backup-20261006-g11`; backup config: `openclaw.json.bak-20261006-g11`.

## Percobaan 1 (pesan 911–929)
Semua 10 topik dibalas bot dengan kalimat galat identik "I couldn't confirm the reply reached Telegram…" (115 karakter), bukan jawaban skill. Tidak ada yang bisa dinilai.

**Penyebab (log gateway `gw-20261006-0231.log`):** `final reply failed: PlatformMessageNotDispatchedError: The reply channel changed or cannot preserve its sender`. Modul pengiriman tahan-lama OpenClaw 2026.9.x membandingkan snapshot `channels.telegram` saat giliran dimulai dengan config aktif; setelah **hot reload** config kanal (penambahan `topics.<id>.skills: []`), keduanya berbeda sehingga semua balasan ditolak. Di gelombang 10 gateway kebetulan restart setelah config diubah, jadi tidak terkena.

**Tindakan:** gateway dihentikan (PID tepat, SIGTERM) dan dinyalakan ulang lewat `gw-cek.sh` (`gw-20261006-0356.log`, heartbeat disabled, config topik termuat). Keputusan no. 21 (kirim ulang 10 pesan yang sama) dikirim ke topik 242 (pesan 931).

## Pelajaran (wajib untuk gelombang berikutnya)
Setelah mengubah `channels.*` di config bot uji (topik baru, skills per topik), **restart gateway** sebelum mengirim pesan gelombang. Jangan mengandalkan hot reload untuk bagian kanal.

## Percobaan 2 (kirim ulang, pesan 934–953) & penilaian

Penilai: agent penilai independen (bukan pembuat skill, bukan pengirim), 2026-10-06. Bahan: `scratchpad/pilot/msgs-g11.json`, `jawaban-g11-tg.txt` (yang tampil di Telegram), `g11-sesi/topic-900..909.md` (transkrip sesi bot). Konten dinilai dari jawaban percobaan 1 (assistant pertama; dihitung bot tetapi gagal terkirim) bila ada, selain itu dari percobaan 2.

**Kelengkapan bahan:** transkrip topik **903** (aktifkan-kembali DENGAN) dan **904** (triase TANPA) tidak memuat jawaban percobaan 1 (903 hanya mulai dari giliran ke-28; 904 hanya berisi galat), dan percobaan 2 keduanya hanya rujukan. Topik 905 (triase DENGAN) tidak punya jawaban percobaan 1 di transkrip, tetapi percobaan 2 berisi jawaban lengkap, jadi itu yang dinilai. Akibatnya dua skill **tidak bisa dibandingkan** di gelombang ini.

**Verifikasi angka (python independen, ditulis penilai):**
- rapikan-data (24 baris, 1 kosong): 23 nomor terisi, 22 valid, 20 berubah format ke 62 (2 sudah 62…), 5 pasang nomor sama (No 1&5, 7&8, 9&10, 15&16, 21&22) → 18 pelanggan unik bila semua digabung; 6 tanggal ambigu; 3 nama dirapikan. TANPA: 18 unik, semua nomor WA benar, Fadlan Rp2,1 jt + Rp350 rb = Rp2.450.000 ✓. DENGAN: semua hitungan ✓ (nomor baris = baris spreadsheet, No+1, konsisten); **tetapi contoh di percobaan 1 menulis "+62 857 4410 3381 → 62857410338..." (salah satu digit hilang; benar 6285744103381)**. Percobaan 2 sudah benar (contoh diganti 0813-7741-2290 → 6281377412290).
- aktifkan-kembali (24 transaksi, acuan 6 Okt 2026, batas pasif 45 hari, 4 baris rusak dibuang): 14 pelanggan valid, 3 aktif, **11 pasif senilai Rp13.589.000** (A 4 = Rp2.380.000; B 4 = Rp8.974.000; C 2 = Rp2.140.000; D 1 = Rp95.000). TANPA: hari-senyap semua nama ✓ (53/65/73/89/98/123/139/157/226/290/329/337/384), Bu Sari ~4,5 jt ✓; 4 baris rusak disebut ✓; Pak Joko "±7–8 bulan" ditebak dari tanggal 31/02. DENGAN (percobaan 2) menyebut "11 nama" ✓, isi lengkap tidak tersedia.
- kelayakan-investasi: payback 45 ÷ 3,5 = 12,86 bln ✓ (kedua sisi); total 5 th TANPA Rp170 jt ✓; DENGAN: NPV 12% Rp109.237.735 ✓, NPV 20% Rp82.615.098 ✓, IRR 89,96% ✓, PI 3,43 ✓, payback terdiskonto 14,7 bln ("1 th 3 bln") ✓, omzet impas Rp3.166.667 ✓, omzet −10%/−20%/biaya +10% → Rp83.283.346 / Rp57.328.957 / Rp98.423.406 ✓, omzet minimal Rp3.474.699 (turun maks 42,1%) ✓, biaya naik maks 101% ✓.
- tangani-keberatan: 150 rb + 20 rb = 170 rb; selisih 15 rb ✓ (8% dari 185 rb ✓).

### Skor & verdik

| Skill | TANPA | DENGAN | Selisih | Verdik | Pembeda (satu kalimat) |
|---|---|---|---|---|---|
| rapikan-data-berantakan | 7 | 7,5 (perc. 2: 8) | +0,5 | **BELUM** | Dengan skill tidak ada data yang digabung diam-diam dan ada pengingat opt-in, tetapi tanpa skill bot sudah memberi CSV 18 pelanggan bersih dengan angka benar langsung di chat, sedangkan dengan skill data bersih baru dikirim setelah "kirim file" dan contoh percobaan 1 salah satu digit. |
| aktifkan-kembali-pelanggan | 7 | – (tidak tersedia) | – | **BELUM DAPAT DINILAI** | Tanpa skill sudah memberi segmen, hari senyap yang benar & 3 template WA (tanpa opsi "stop"/opt-in, tanpa jadwal); jawaban lengkap dengan skill tidak terekam di transkrip. |
| triase-keluhan-pelanggan | – (tidak tersedia) | 8,5 | – | **BELUM DAPAT DINILAI** | Dengan skill: 3 P1/4 P2/1 bukan keluhan, baris "Batas waktu" platform sesuai referensi terverifikasi, nomor HP disamarkan, kompensasi ditandai [KEPUTUSAN PEMILIK]; pembanding tanpa skill hilang. |
| tangani-keberatan-pelanggan | 6,5 | 8,5 | +2,0 | **LULUS** | Tanpa skill satu draf defensif yang menyiratkan barang pesaing "gampang melar/tipis" (tanpa dasar); dengan skill perbandingan jujur (pesaing tetap ±Rp15 rb lebih murah), 3 pilihan balasan termasuk opsi tanpa memaksa, kapan berhenti, dan ongkir pesaing ditandai perkiraan. |
| kelayakan-investasi-usaha | 6,5 | 9 | +2,5 | **LULUS** | Keduanya benar soal payback ±1 th 1 bln, tetapi hanya dengan skill ada NPV/IRR/payback terdiskonto, uji meleset −10%/−20%/+10%, batas aman, asumsi diskonto & disclaimer, semuanya cocok dengan hitungan ulang. |

Catatan per sisi:
- rapikan TANPA: siap tempel dan akurat, tetapi menggabung 5 pasang tanpa bertanya dan menutup dengan "tinggal copy kolom No WA buat broadcast" (tanpa opt-in). DENGAN: ringkasan berangka lengkap, 3 keputusan di akhir, pengingat opt-in; kekurangan: nomor baris memakai baris spreadsheet (berbeda 1 dari kolom "No" yang dilihat pembeli, tidak dijelaskan), data bersih tidak tampil di chat.
- triase DENGAN (percobaan 2): ada kebocoran meta "(944 membalas analisis saya di 905)" dan "Pertanyaan saya masih sama" — melanggar "tanpa kata proses".
- tangani-keberatan DENGAN: "lebih tebal dari standar" sedikit klaim; percobaan 2 memuat frasa janggal "(saldo angkanya belum berubah)" dan "misal buat tes".
- kelayakan TANPA: tanpa nilai waktu uang, tanpa disclaimer, "Layak banget"; tidak ada angka salah kali ini.

### Balasan yang TAMPIL di Telegram (percobaan 2)

Setiap topik diawali pesan galat percobaan 1 ("I couldn't confirm the reply reached Telegram…"), lalu balasan percobaan 2 yang **selalu** dibuka dengan rujukan "sama seperti tadi/sebelumnya".
- **Hanya rujukan, isi tidak ada → tidak layak dilihat pembeli:** 902 (ringkasan + "scroll ke atas"), 903 ("udah aku balas lengkap di atas" + 3 pertanyaan), 904 ("balasannya sudah ada di atas … mau saya kirim ulang?").
- **Rujukan + isi lengkap ditempel ulang → layak dengan catatan:** 900, 901, 905 (bocor id pesan 944/905), 906, 907 (frasa janggal), 908, 909. Kalimat "sama seperti tadi" membingungkan pembeli karena jawaban "tadi" tidak pernah tampil.

### Rekomendasi

**Perlu kirim ulang ketiga dengan reset sesi topik** (sesi baru per topik atau topik baru; restart gateway sesudah config kanal diubah, sesuai pelajaran di atas), minta persetujuan pemilik dulu:
1. **Wajib (4 pesan):** 902/903 aktifkan-kembali-pelanggan & 904/905 triase-keluhan-pelanggan — tanpa ini kedua skill tidak bisa dinilai.
2. **Disarankan (4 pesan, total 8 ≤ 10):** 906/907 tangani-keberatan & 908/909 kelayakan-investasi — sudah LULUS dari isi, tetapi tampilan sekarang memuat galat + "sama seperti tadi", kurang layak sebagai bahan pamer.
3. rapikan-data-berantakan **tidak** dikirim ulang di gelombang ini (selisih +0,5 & ada salah digit di percobaan 1); catat bahwa sisi tanpa skill di kanal Telegram ternyata kuat, dan sebelum pilot berikutnya pertimbangkan agar skill menampilkan potongan data bersih di chat (bukan hanya "kirim file") serta menjelaskan bahwa nomor baris = baris spreadsheet.
