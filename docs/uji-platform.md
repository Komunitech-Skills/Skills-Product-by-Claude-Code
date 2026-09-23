# Checklist Uji Platform Asli (±10 menit per skill)

Dipakai pemilik/tim untuk menguji skill berstatus `lulus` di aplikasi sungguhan sebelum naik ke `beta`.
Uji minimal di **satu** platform; idealnya OpenClaw + satu lainnya (Cursor/Codex/Claude Code).

## Uji otomatis OpenClaw (tanpa API key)
`bash scripts/uji_openclaw.sh` memasang OpenClaw terbaru di `/tmp`, memuat semua skill, lalu memastikan
setiap skill **eligible, terlihat oleh model, dan bisa dipanggil sebagai perintah**. Jalankan setiap ada
skill baru. Ini BUKAN pengganti uji manual di bawah (perilaku agent butuh API key model).

## Persiapan (sekali saja)
1. Buat paket uji: `python3 scripts/build.py --pembeli "UJI INTERNAL" --skill <nama> --izinkan-draft`
2. Pasang ZIP dari `dist/` mengikuti `docs/instalasi.md` (Anggap dirimu pembeli awam — kalau panduan instalasi membingungkan, catat!).
3. Buka **sesi/chat baru**.

## Langkah uji
| # | Uji | Cara | Lulus jika |
|---|---|---|---|
| 1 | Terpasang | Claude Code/Codex: `/skills` · Cursor: ketik `/` · OpenClaw: `openclaw skills list` | Nama skill muncul |
| 2 | Terpicu otomatis | Ketik permintaan biasa dari bagian "Cara pakai" README, **tanpa** menyebut nama skill | Agent memakai skill (lihat gaya output sesuai format di SKILL.md) |
| 3 | Permintaan malas | Ketik versi singkat, mis. "bikinin dong ..." | Agent bertanya sekali ATAU langsung jalan dengan asumsi yang disebutkan |
| 4 | Script (jika ada) | Jalankan skenario yang butuh hitungan | Script berjalan tanpa error; angka sama dengan contoh di `examples/` |
| 5 | Tidak salah picu | Minta hal yang tidak berkaitan (mis. "resep nasi goreng") | Skill **tidak** dipakai |
| 6 | Kualitas | Bandingkan dengan `examples/01-*.md` | Kualitas setara atau lebih baik |

## Catat hasil
Tulis di `skills/<nama>/examples/UJI-PLATFORM.md`:

```
## <Platform> <versi> — <tanggal> — <nama penguji>
OS: Windows / Mac / Linux
1 Terpasang: ✅/❌
2 Terpicu otomatis: ✅/❌ (catatan)
3 Permintaan malas: ✅/❌
4 Script: ✅/❌/— (catatan)
5 Tidak salah picu: ✅/❌
6 Kualitas: ✅/❌
Masalah: ...
```

Lalu tambahkan platform ke kolom `platform_teruji` di `catalog.csv` (pisahkan dengan `;`, mis. `claude-code (simulasi agent);openclaw;cursor`).
Jika ada ❌ di nomor 1, 2, atau 4 → skill kembali ke `uji` untuk diperbaiki.
