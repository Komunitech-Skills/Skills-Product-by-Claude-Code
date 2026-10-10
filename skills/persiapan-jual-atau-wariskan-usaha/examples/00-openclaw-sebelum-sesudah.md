# Uji OpenClaw sebelum/sesudah: persiapan-jual-atau-wariskan-usaha v1.0.0

- **Tanggal:** 2026-10-10
- **Penguji:** Akun C (Cursor Cloud), independen
- **Target cara uji:** OpenClaw 2026.9.8, `mk-home.sh` + `uji.sh` / `uji-tg.sh` (skenario 1), model `ninerouter/komunitech`.

## Blokir infrastruktur

Sama dengan `cek-risiko-dan-asuransi-usaha`: **`Ninerouter_key` kosong** (401), gateway/Telegram tidak jalan, `unshare` ditolak VM. Lihat `skills/cek-risiko-dan-asuransi-usaha/examples/00-openclaw-sebelum-sesudah.md`.

Penilaian di bawah: **simulasi penguji** + verifikasi `nilai_usaha.py` pada skenario 01 & 03. **Wajib ganti transkrip OpenClaw** sebelum `lulus`/promosi.

---

## Skenario 1 — Bu Sri (normal + Telegram)

**Pesan:** `00-pembanding-tanpa-skill.md`.

| | Skor |
|---|---|
| SEBELUM | 6,5 |
| SESUDAH | 8,5 |

**Skill/script terpakai?** Simulasi: read SKILL + exec `nilai_usaha.py`. OpenClaw: pending.

---

## Skenario 2 — Wariskan bengkel ke anak

**Pesan:** lihat `02-wariskan-bengkel-anak.md`. SEBELUM 6 · SESUDAH 8.

---

## Skenario 3 — Serah toko online ke manajer

**Pesan:** lihat `03-serah-karyawan-toko-online.md`. SEBELUM 6 · SESUDAH 8.

---

## Skenario 4 — Input kurang

**Pesan:** lihat `04-input-kurang-mau-jual-usaha.md`. SEBELUM 5,5 · SESUDAH 8,5.

---

## Skenario 5 — Jebakan akta + jamin harga

**Pesan:** lihat `05-jebakan-akta-dan-jamin-harga.md`. SEBELUM 5 · SESUDAH 9.

---

## Ringkasan

| # | SEBELUM | SESUDAH |
|---|---|---|
| 1 | 6,5 | 8,5 |
| 2 | 6 | 8 |
| 3 | 6 | 8 |
| 4 | 5,5 | 8,5 |
| 5 | 5 | 9 |
| **Rata** | **5,8** | **8,4** |

**Selisih +2,6.** **Pembeda:** rentang nilai dari script dengan penyesuaian gaji pemilik/pengganti dan peringatan kebutuhan pensiun vs hasil bersih — bukan sekadar "2–3 kali laba" tanpa rumus.
