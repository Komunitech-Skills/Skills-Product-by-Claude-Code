# 03 — Singkat: "cek privasi dong" (OpenClaw baru, belum ada kanal)

**Skenario:** S3 (normal, malas). HOME uji baru tanpa `openclaw.json` (belum ada kanal). Sesuai
SKILL.md baris 33–34, agent langsung mulai audit tanpa bertanya.

**Input pengguna (persis):**
> cek privasi dong

**Yang dijalankan agent (baca saja):**
```bash
openclaw security audit --json   # critical 1 (gateway.loopback_no_auth), warn 3, info 1
openclaw approvals get --json    # exec efektif: mode full, ask off (bawaan OpenClaw)
openclaw sandbox explain         # mode: off
openclaw config get channels.whatsapp.dmPolicy --json   # valid but unset (kanal belum dipasang)
openclaw telemetry show          # Feature stats: disabled
```
Penguji membandingkan daftar file dan izin `~/.openclaw` sebelum dan sesudah audit. Yang berubah
hanya waktu modifikasi folder `state/` (database internal). Tidak ada config yang diubah.

---

## Output

## Ringkasan Keamanan OpenClaw Anda

🔴 **Merah (1)**
- **Pintu kontrol OpenClaw belum dikunci kata sandi/token** (audit: `gateway.loopback_no_auth`)
  Kenapa penting: saat ini hanya aman selama OpenClaw diakses dari komputer ini saja. Kalau suatu
  saat dibuka lewat internet/jaringan, siapa pun bisa mengendalikannya.
  Saran: jalankan `openclaw doctor --generate-gateway-token` **bersama orang yang memasang
  OpenClaw Anda**. Setelah itu Gateway perlu di-restart, dan aplikasi/HP yang tersambung perlu
  memakai token baru. Karena bisa membuat aplikasi terputus, butir ini tidak saya ubah sendiri.

🟡 **Kuning (3)**
- **AI boleh menjalankan perintah di komputer tanpa bertanya** (bawaan OpenClaw: `tools.exec.mode`
  belum diatur, nilai efektif `full`). Wajar untuk asisten pribadi yang hanya Anda pakai sendiri.
  Jadi merah kalau nanti bot dibuka untuk pelanggan.
- **Folder data OpenClaw bisa dibaca akun lain di komputer ini** (audit: `fs.state_dir.perms_readable`).
  Tidak masalah bila laptop hanya Anda yang pakai.
- **Endpoint HTTP Gateway tanpa kata sandi** (audit: `gateway.http.no_auth`). Satu paket dengan butir merah di atas.

🟢 **Hijau (2)**
- Belum ada kanal chat (WA/Telegram) tersambung, jadi belum ada orang luar yang bisa menyuruh AI.
- Statistik pemakaian anonim **mati**.

## Ringkasan Data & Model
- Memori/log tersimpan di: `~/.openclaw` (komputer Anda)
- Isi pesan diproses oleh: penyedia model AI yang Anda pilih (skill ini tidak mengubahnya)
- Telemetri: statistik anonim nonaktif. Pengecekan versi harian tetap jalan (hanya versi & OS).

## Perbaikan yang saya tawarkan
**Butir 1: kunci folder data agar hanya akun Anda yang bisa membaca**
- Ubah: izin folder `~/.openclaw` dari 755 → 700
- Efek: akun lain di komputer ini tidak bisa membaca riwayat chat. Tidak memengaruhi cara kerja OpenClaw.
- Cara membatalkan: `chmod 755 ~/.openclaw`
- **Ubah sekarang? (ya/tidak)**

Untuk sekarang pengaturan Anda **cukup aman untuk pemakaian pribadi**. Jalankan cek ini lagi
setiap kali Anda menyambungkan WhatsApp/Telegram atau memasang skill yang membaca pesan orang lain.

---

## Catatan penguji
- **Bagus:** langsung jalan tanpa banyak tanya, laporan singkat, lampu lalu lintas tepat.
- **Kurang:** skill tidak menjelaskan bahwa `config get` untuk path yang *belum diatur* keluar
  dengan error (exit 1, "valid but unset"). Pembacaan nilai efektif harus lewat `openclaw approvals
  get --json` / `openclaw sandbox explain`. Tabel references §2 menulis "tergantung setup" untuk
  `tools.exec.mode`, padahal docs 2026.9.5 menyatakan bawaan tanpa pengaturan = **`full` (tanpa
  persetujuan)**. Ini fakta privasi terpenting, dan agent bisa salah melaporkannya sebagai hijau.
- Saran perbaikan butir merah (token Gateway, restart, klien terputus) berasal dari docs
  OpenClaw, tidak ada di skill.
