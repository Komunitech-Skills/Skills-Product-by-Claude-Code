# Gelombang Telegram 11 — 2026-10-06 (percobaan 1 GAGAL, menunggu keputusan no. 21)

Disetujui pemilik (keputusan no. 20, chat "setuju 16 18 19a 20"). Skill: rapikan-data-berantakan, aktifkan-kembali-pelanggan, triase-keluhan-pelanggan, tangani-keberatan-pelanggan, kelayakan-investasi-usaha. Topik G11: 900/901, 902/903, 904/905, 906/907, 908/909 (TANPA/DENGAN). Backup skill bot: `skills-backup-20261006-g11`; backup config: `openclaw.json.bak-20261006-g11`.

## Percobaan 1 (pesan 911–929)
Semua 10 topik dibalas bot dengan kalimat galat identik "I couldn't confirm the reply reached Telegram…" (115 karakter), bukan jawaban skill. Tidak ada yang bisa dinilai.

**Penyebab (log gateway `gw-20261006-0231.log`):** `final reply failed: PlatformMessageNotDispatchedError: The reply channel changed or cannot preserve its sender`. Modul pengiriman tahan-lama OpenClaw 2026.9.x membandingkan snapshot `channels.telegram` saat giliran dimulai dengan config aktif; setelah **hot reload** config kanal (penambahan `topics.<id>.skills: []`), keduanya berbeda sehingga semua balasan ditolak. Di gelombang 10 gateway kebetulan restart setelah config diubah, jadi tidak terkena.

**Tindakan:** gateway dihentikan (PID tepat, SIGTERM) dan dinyalakan ulang lewat `gw-cek.sh` (`gw-20261006-0356.log`, heartbeat disabled, config topik termuat). Keputusan no. 21 (kirim ulang 10 pesan yang sama) dikirim ke topik 242 (pesan 931).

## Pelajaran (wajib untuk gelombang berikutnya)
Setelah mengubah `channels.*` di config bot uji (topik baru, skills per topik), **restart gateway** sebelum mengirim pesan gelombang. Jangan mengandalkan hot reload untuk bagian kanal.
