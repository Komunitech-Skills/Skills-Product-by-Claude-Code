# Pilot tampilan bot-to-bot Telegram (2026-10-02)

Dasar: keputusan pemilik 2026-10-02 ("setuju pilot Telegram"). Pelaksana: agent Komunitech. Semua data uji fiktif.
Path `$R` = `scratchpad/openclaw-real` (sesi ini).

## Yang diubah
| Apa | Detail | Backup |
|---|---|---|
| Skill bot produksi (@KTclaude1_bot) | 111 folder di `$R/home/.openclaw/skills/` diganti versi repo `skills/` terbaru (tanpa `__pycache__`). Tidak ada skill baru ditambahkan. 3 skill pilot dicek identik dengan repo (`diff -rq`). | `$R/skills-backup-20261002-0712/` |
| Setelan OpenClaw | **Tidak diubah.** Bot produksi sudah membalas bot penguji dengan setelan lama (grup uji `groupPolicy: open` + `requireMention: true`; OpenClaw 2026.9.6 tidak menyaring pengirim bot di Telegram). `cmp` memastikan file sama dengan backup. | `$R/openclaw.json.before-pilot-20261002-0712` (cadangan saja) |
| Gateway | Dinyalakan ulang 14:14 WIB lewat `gw-cek.sh` agar skill baru termuat. Log: `$R/gw-20261002-0714.log`. | – |

### Cara revert
```bash
R=<scratchpad>/openclaw-real
rm -rf $R/home/.openclaw/skills && cp -a $R/skills-backup-20261002-0712 $R/home/.openclaw/skills
pkill -TERM -x openclaw-gateway   # jangan pakai pkill -f dari shell yang command-line-nya memuat kata itu
bash $R/gw-cek.sh
```

## Pesan yang dikirim (bot penguji, 3 dari maks. 10, jeda ≥25 detik, tanpa balasan otomatis)
| # | Skill | Topik | Waktu kirim (WIB) | Isi |
|---|---|---|---|---|
| 1 | hitung-thr | 280 | 14:15:50 | Skenario uji ulang OpenClaw (gaji 4,5 jt, mulai 1 Mar 2026, "lebaran" 20 Mar 2027) |
| 2 | rencana-marketing-usaha | 435 | 14:16:54 | Skenario 1 `00-openclaw-sebelum-sesudah.md` (brownies, budget Rp4,5 jt) |
| 3 | peringatan-dini-operasional | 272 | 14:17:20 | Skenario 1 (log katering 4 minggu; CSV ditempel di pesan karena tidak bisa melampirkan file) |

Bot penguji hanya memanggil `sendMessage` (3x) dan `getUpdates` (baca). Balasan dibaca lewat getUpdates bot penguji (bot penguji ternyata menerima pesan bot produksi) + log gateway.

## Hasil
| Skill | Membalas? | Lama balas | Tampilan di Telegram |
|---|---|---|---|
| hitung-thr | Ya | 43 detik | 1 pesan (2.028 karakter). Pesan status "**Working**" muncul dulu. Tabel markdown jadi blok kode monospace (rapi, bisa digeser), tebal/miring/tautan rapi. Isi benar: koreksi 20 Mar = 11 Syawal, pakai perkiraan 10 Mar 2027, batas bayar 3 Mar, THR Rp4.500.000, draf pengumuman, disclaimer. |
| rencana-marketing-usaha | Ya | 2 menit 12 detik | Terpecah **4 pesan** (3.645 + 265 + 3.533 + 327 karakter). Pecahan ke-2 hanya 1 butir (Desember) — pemotongan kurang rapi di tengah bagian "Kalender". Tebal rapi, tanpa tabel. Angka cocok: margin Rp25.000 / Rp42.000, alokasi total pas Rp4.500.000, ROAS impas 3,40 / 2,03, ada peringatan target 300/bln tidak realistis untuk budget itu. Typo kecil: "target 300 kemustahilan". |
| peringatan-dini-operasional | Ya | 33 detik | 1 pesan (3.170 karakter). Laporan script tampil dalam blok kode (emoji 🔴/✅ tetap terbaca). Menemukan 4 🔴 (porsi rusak, keluhan, porsi terkirim, stok beras → pesan hari ini) & mengaitkan dengan "ganti pemasok sayur" 28 Sep secara hati-hati. Tidak menawarkan kirim ke grup WA. Status "Working" sempat diedit menjadi "📝 1 files +30" (agent menyimpan CSV ke workspace). |

Tidak ada pesan terpotong/hilang; tidak ada error markdown. Satu-satunya catatan tampilan: pesan status "Working" tertinggal di topik, dan pemecahan pesan panjang (>4.096 karakter) kadang menyisakan potongan pendek.

## Rekomendasi peluncuran ke semua skill beta
1. **Bot-to-bot jalan tanpa ubah setelan** → tidak perlu `allowBots`/ubah grup. Tetap jaga pengaman: bot penguji hanya kirim pesan terjadwal, tidak membalas; jeda ≥20 detik; batasi per gelombang (mis. 10 pesan) karena satu balasan bisa 2+ menit.
2. **Menu /skill maks 100:** log gateway sudah menulis "menu pressure omitted per-skill commands … keeping /skill" (111 skill). Untuk peluncuran: satu agent OpenClaw per bundle (`agents` + `skills` per agent, atau `channels.telegram.groups.<id>.topics.<topik>.skills` / `agentId` per topik) sehingga tiap agent ≤100 skill dan menu per-skill bisa tampil lagi. Uji dulu di grup uji.
3. Skill dengan balasan panjang (rencana-marketing-usaha dkk.): pertimbangkan instruksi "ringkasan dulu, rincian bila diminta" untuk kanal chat, agar tidak terpecah 4 pesan.
4. Skill yang butuh file (peringatan-dini): pilot membuktikan CSV ditempel di chat bisa dipakai; panduan member perlu menyebut cara kirim file/teks.
5. Saat menyalakan ulang gateway, pakai `pkill -x openclaw-gateway` (bukan `-f`) agar tidak mematikan shell pemanggil.

Berkas kerja (scratchpad, bukan repo): `scratchpad/pilot/` (msgs.json, sent.jsonl, updates.jsonl, script tg.py/send.py/poll.py; token hanya dibaca dari env).
